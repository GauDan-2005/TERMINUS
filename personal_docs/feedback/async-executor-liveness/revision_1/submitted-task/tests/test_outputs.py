import json
import os
import shutil
import subprocess
from pathlib import Path


APP = Path(os.environ.get("APP_ROOT", "/app"))
OUT = APP / "output" / "executor-audit.json"
BIN = APP / "target" / "release" / "executor-ctl"
CASES = ["amber", "cobalt", "drake", "ember", "flint", "graphite"]
PLAN_ROWS = {
    "amber": [
        "CAP 2",
        "ROOT amber-root lane-a 0",
        "CHILD amber-root amber-left lane-a 0",
        "CHILD amber-left amber-leaf lane-b 1",
        "ROOT amber-side lane-b 1",
    ],
    "cobalt": [
        "CAP 1",
        "ROOT cobalt-root lane-a 0",
        "CHILD cobalt-root cobalt-a lane-a 0",
        "CHILD cobalt-root cobalt-b lane-a 0",
        "CHILD cobalt-root cobalt-c lane-a 0",
        "CHILD cobalt-c cobalt-tail lane-b 1",
    ],
    "drake": [
        "CAP 2",
        "ROOT drake-root lane-a 0",
        "CHILD drake-root drake-keep lane-b 0",
        "CHILD drake-root drake-cut lane-a 0",
        "CHILD drake-cut drake-shadow lane-b 1",
        "DROP drake-cut",
        "ROOT drake-late lane-a 2",
    ],
    "ember": [
        "CAP 1",
        "ROOT ember-root lane-a 0",
        "CHILD ember-root ember-left lane-a 0",
        "CHILD ember-left ember-deep lane-a 0",
        "CHILD ember-left ember-side lane-b 1",
        "DROP ember-left",
        "ROOT ember-after lane-b 1",
    ],
    "flint": [
        "CAP 2",
        "ROOT flint-root lane-a 0",
        "CHILD flint-root flint-a lane-a 0",
        "CHILD flint-root flint-a lane-a 0",
        "CHILD flint-root flint-b lane-b 0",
        "CHILD flint-b flint-c lane-b 0",
        "DROP flint-c",
    ],
    "graphite": [
        "CAP 1",
        "ROOT graphite-root lane-a 0",
        "CHILD graphite-root graphite-a lane-a 0",
        "CHILD graphite-root graphite-b lane-b 0",
        "CHILD graphite-a graphite-c lane-a 1",
        "CHILD graphite-b graphite-d lane-b 1",
        "CHILD graphite-d graphite-e lane-b 1",
        "DROP graphite-d",
        "ROOT graphite-tail lane-a 2",
    ],
}
_BUILT = False
_MATRIX = None


def plan_rows(name: str) -> list[str]:
    path = APP / "data" / "cases" / f"{name}.plan"
    rows = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert rows == PLAN_ROWS[name]
    return rows


def expected_trace(name: str) -> list[dict]:
    nodes: dict[str, dict] = {}
    order: list[str] = []
    removed: set[str] = set()
    cap = 1
    for seq, line in enumerate(plan_rows(name)):
        parts = line.split()
        if parts[0] == "CAP":
            cap = int(parts[1])
        elif parts[0] == "ROOT":
            ident, lane, at = parts[1], parts[2], int(parts[3])
            if ident not in nodes:
                nodes[ident] = {
                    "task": ident,
                    "parent": "-",
                    "lane": lane,
                    "base": at,
                    "seq": seq,
                    "depth": 0,
                    "chain": [ident],
                }
                order.append(ident)
        elif parts[0] == "CHILD":
            parent, ident, lane, at = parts[1], parts[2], parts[3], int(parts[4])
            if ident not in nodes:
                prior = nodes[parent]
                nodes[ident] = {
                    "task": ident,
                    "parent": parent,
                    "lane": lane,
                    "base": at,
                    "seq": seq,
                    "depth": prior["depth"] + 1,
                    "chain": prior["chain"] + [ident],
                }
                order.append(ident)
        elif parts[0] == "DROP":
            removed.add(parts[1])
    candidates = [nodes[key] for key in order if not any(part in removed for part in nodes[key]["chain"])]
    return drain_expected(name, candidates, cap)


def drain_expected(name: str, rows: list[dict], cap: int) -> list[dict]:
    pending = sorted(rows, key=lambda row: (row["base"], row["seq"]))
    if not pending:
        return []
    turn = pending[0]["base"]
    out = []
    while pending:
        if all(row["base"] > turn for row in pending):
            turn = min(row["base"] for row in pending)
            continue
        ready = [row for row in pending if row["base"] <= turn]
        future = [row for row in pending if row["base"] > turn]
        chosen = set()
        for lane in sorted({row["lane"] for row in ready}):
            lane_ready = sorted(
                [row for row in ready if row["lane"] == lane],
                key=lambda row: (row["base"], row["seq"]),
            )
            for row in lane_ready[:cap]:
                chosen.add(row["task"])
                out.append(
                    {
                        "case": name,
                        "task": row["task"],
                        "parent": row["parent"],
                        "depth": row["depth"],
                        "lane": row["lane"],
                        "turn": turn,
                    }
                )
        pending = sorted(
            [row for row in ready if row["task"] not in chosen] + future,
            key=lambda row: (row["base"], row["seq"]),
        )
        turn += 1
    return out


def build_binary() -> Path:
    global _BUILT
    if _BUILT and BIN.exists():
        return BIN
    proc = subprocess.run(
        ["cargo", "build", "--release", "--bin", "executor-ctl"],
        cwd=APP,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=240,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert BIN.exists()
    _BUILT = True
    return BIN


def run_matrix(fresh: bool = False) -> dict:
    global _MATRIX
    if _MATRIX is not None and not fresh:
        return _MATRIX
    if OUT.exists():
        OUT.unlink()
    build_binary()
    proc = subprocess.run(
        ["bash", str(APP / "scripts" / "run-matrix.sh")],
        cwd=APP,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=240,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    data = json.loads(OUT.read_text(encoding="utf-8"))
    if not fresh:
        _MATRIX = data
    return data


def run_direct(name: str) -> dict:
    build_binary()
    out = APP / "output" / f"direct-{name}.json"
    work = APP / "output" / f"direct-work-{name}"
    if out.exists():
        out.unlink()
    if work.exists():
        shutil.rmtree(work)
    proc = subprocess.run(
        ["bash", str(APP / "scripts" / "run-one.sh"), name, str(out), str(work)],
        cwd=APP,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=240,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    data = json.loads(out.read_text(encoding="utf-8"))
    assert [case["name"] for case in data["cases"]] == [name]
    return data["cases"][0]


def case_from_matrix(name: str) -> dict:
    matches = [case for case in run_matrix()["cases"] if case["name"] == name]
    assert len(matches) == 1
    return matches[0]


def ledger_rows(case: dict) -> list[dict]:
    path = Path(case["ledger"])
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def journal_rows(case: dict) -> list[dict]:
    rows = []
    for line in Path(case["journal"]).read_text(encoding="utf-8").splitlines():
        parts = line.split()
        rows.append(
            {
                "case": parts[0],
                "task": parts[1],
                "parent": parts[2],
                "depth": int(parts[3]),
                "lane": parts[4],
                "turn": int(parts[5]),
            }
        )
    return rows


def assert_clean(case: dict) -> None:
    assert set(case) == {"name", "ok", "finished", "pending", "trace", "ledger", "journal"}
    assert case["ok"] is True
    assert case["finished"] is True
    assert case["pending"] == []
    assert case["trace"] == expected_trace(case["name"])


def test_matrix_all_six_cases_clean():
    """The matrix command emits the six clean case reports in the requested order."""
    data = run_matrix()
    assert [case["name"] for case in data["cases"]] == CASES
    for case in data["cases"]:
        assert_clean(case)
        assert case["trace"]


def test_single_case_helper_matches_matrix():
    """The direct helper produces the same reports as the matrix run."""
    for name in CASES:
        direct = run_direct(name)
        assert_clean(direct)
        assert direct["trace"] == case_from_matrix(name)["trace"]


def test_amber_nested_parent_depth_preserved():
    """Amber keeps nested parent and depth fields stable."""
    case = case_from_matrix("amber")
    assert_clean(case)
    assert {row["task"]: row["depth"] for row in case["trace"]}["amber-leaf"] == 2


def test_cobalt_overflow_carried_to_later_turns():
    """Cobalt pressure carries overflow rows into later turns."""
    case = case_from_matrix("cobalt")
    assert_clean(case)
    assert max(row["turn"] for row in case["trace"] if row["lane"] == "lane-a") >= 3


def test_drake_dropped_branch_and_descendants_excluded():
    """Drake excludes the named removed row and its descendant."""
    case = case_from_matrix("drake")
    assert_clean(case)
    tasks = {row["task"] for row in case["trace"]}
    assert "drake-cut" not in tasks
    assert "drake-shadow" not in tasks


def test_ember_branch_removal_with_nested_rows():
    """Ember combines nested rows with branch removal."""
    case = case_from_matrix("ember")
    assert_clean(case)
    tasks = {row["task"] for row in case["trace"]}
    assert tasks == {"ember-root", "ember-after"}


def test_flint_duplicate_logical_rows_deduped():
    """Flint accepts duplicate logical rows only once."""
    case = case_from_matrix("flint")
    assert_clean(case)
    tasks = [row["task"] for row in case["trace"]]
    assert tasks.count("flint-a") == 1


def test_graphite_mixed_pressure_and_removed_descendants():
    """Graphite keeps mixed pressure and removed descendants consistent."""
    case = case_from_matrix("graphite")
    assert_clean(case)
    tasks = {row["task"] for row in case["trace"]}
    assert "graphite-d" not in tasks
    assert "graphite-e" not in tasks
    assert "graphite-tail" in tasks


def test_ledger_jsonl_matches_trace():
    """Every JSONL ledger mirrors its JSON trace exactly."""
    for case in run_matrix()["cases"]:
        assert ledger_rows(case) == case["trace"]


def test_text_journal_matches_trace():
    """Every text journal mirrors its JSON trace exactly."""
    for case in run_matrix()["cases"]:
        assert journal_rows(case) == case["trace"]


def test_matrix_output_deterministic_across_runs():
    """Two fresh matrix runs are byte-for-byte equivalent after parsing."""
    first = run_matrix(fresh=True)
    second = run_matrix(fresh=True)
    assert first == second


def test_cobalt_capacity_delays_acceptance_turns():
    """At least one bounded case shows delayed acceptance derived from capacity."""
    delayed = [row for row in case_from_matrix("cobalt")["trace"] if row["task"] in {"cobalt-b", "cobalt-c"}]
    assert delayed
    assert min(row["turn"] for row in delayed) > 0
