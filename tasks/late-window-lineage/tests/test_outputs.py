import json
import os
import subprocess
from pathlib import Path


APP = Path(os.environ.get("APP_ROOT", "/app"))
OUT = APP / "output" / "window-audit.json"

NAMES = ["aurora", "boreal", "cirrus", "drift", "ember", "flux"]

_CACHE = None


def load_raw() -> dict[str, list[tuple[int, str, int, str, int, str]]]:
    out = {}
    for name in NAMES:
        rows = []
        path = APP / "data" / "cases" / f"{name}.csv"
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            seq, part, slot, key, delta, row_id = line.split(",", 5)
            rows.append((int(seq), part, int(slot), key, int(delta), row_id))
        out[name] = rows
    return out


def bucket(slot: int) -> int:
    return (slot // 10) * 10


def expected_corrections(name: str) -> list[dict]:
    seen = set()
    events = []
    for seq, part, slot, key, delta, row_id in sorted(load_raw()[name], key=lambda row: (row[0], row[5])):
        if row_id in seen:
            continue
        seen.add(row_id)
        events.append((part, bucket(slot), key, seq, row_id, delta))
    events.sort(key=lambda item: (item[0], item[1], item[2], item[3], item[4]))
    totals = {}
    trails = {}
    out = []
    for part, win, key, _seq, row_id, delta in events:
        group = (part, win, key)
        totals[group] = totals.get(group, 0) + delta
        trails.setdefault(group, [])
        trails[group].append(row_id)
        out.append(
            {
                "partition": part,
                "window": win,
                "key": key,
                "value": totals[group],
                "lineage": list(trails[group]),
            }
        )
    return sorted(out, key=lambda row: (row["partition"], row["window"], row["key"], row["lineage"]))


def expected_totals(name: str) -> list[dict]:
    latest = {}
    for row in expected_corrections(name):
        latest[(row["partition"], row["window"], row["key"])] = {
            "partition": row["partition"],
            "window": row["window"],
            "key": row["key"],
            "value": row["value"],
        }
    return sorted(latest.values(), key=lambda row: (row["partition"], row["window"], row["key"]))


def compact(rows: list[dict]) -> list[dict]:
    return [
        {
            "partition": row["partition"],
            "window": row["window"],
            "key": row["key"],
            "value": row["value"],
            "lineage": row["lineage"],
        }
        for row in rows
    ]


def project(rows: list[dict]) -> list[dict]:
    return sorted(compact(rows), key=lambda row: (row["partition"], row["window"], row["key"], row["lineage"]))


def expected_id(case_name: str, row: dict) -> str:
    return (
        f"{case_name}:{row['partition']}:{row['window']}:"
        f"{row['key']}:{row['value']}:{':'.join(row['lineage'])}"
    )


def run_matrix(force: bool = False) -> dict:
    global _CACHE
    if _CACHE is not None and not force:
        return _CACHE
    if OUT.exists():
        OUT.unlink()
    proc = subprocess.run(
        ["bash", str(APP / "scripts" / "run-matrix.sh")],
        cwd=APP,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert OUT.exists()
    data = json.loads(OUT.read_text(encoding="utf-8"))
    if not force:
        _CACHE = data
    return data


def cases_by_name(force: bool = False) -> dict[str, dict]:
    data = run_matrix(force=force)
    assert set(data) == {"cases"}
    assert [case["name"] for case in data["cases"]] == NAMES
    return {case["name"]: case for case in data["cases"]}


def test_r01():
    """The documented command writes one audit row per named case."""
    cases = cases_by_name()
    assert set(cases) == set(NAMES)
    assert all(OUT.is_file() for _ in [0])


def test_r02():
    """Every case reports a clean direct, restarted, and repeat surface."""
    for case in cases_by_name().values():
        assert case["ok"] is True
        assert case["repeat"] is True
        assert set(case) == {"name", "ok", "direct", "replay", "repeat"}
        assert set(case["direct"]) == {"totals", "corrections"}
        assert set(case["replay"]) == {"totals", "corrections"}


def test_r03():
    """Uninterrupted totals match values derived from input rows."""
    for name, case in cases_by_name().items():
        assert case["direct"]["totals"] == expected_totals(name)


def test_r04():
    """Restarted totals match both derived totals and uninterrupted totals."""
    for name, case in cases_by_name().items():
        assert case["replay"]["totals"] == expected_totals(name)
        assert case["replay"]["totals"] == case["direct"]["totals"]


def test_r05():
    """Correction rows stay derived and aligned across both views."""
    for name, case in cases_by_name().items():
        expected = expected_corrections(name)
        for view in ["direct", "replay"]:
            for row in case[view]["corrections"]:
                assert set(row) == {"partition", "window", "key", "value", "id", "lineage"}
        assert compact(case["direct"]["corrections"]) == expected
        assert compact(case["replay"]["corrections"]) == expected
        left = [row["id"] for row in case["direct"]["corrections"]]
        right = [row["id"] for row in case["replay"]["corrections"]]
        assert left == right


def test_r06():
    """Duplicate input ids are suppressed without removing real changes."""
    cases = cases_by_name()
    assert project(cases["aurora"]["replay"]["corrections"]) == expected_corrections("aurora")
    assert project(cases["flux"]["replay"]["corrections"]) == expected_corrections("flux")
    for name in ["aurora", "flux"]:
        for row in cases[name]["replay"]["corrections"]:
            assert len(row["lineage"]) == len(set(row["lineage"]))


def test_r07():
    """Out-of-file-order rows keep lineage sorted by row semantics."""
    cirrus = cases_by_name()["cirrus"]
    assert project(cirrus["direct"]["corrections"]) == expected_corrections("cirrus")
    assert [row["lineage"] for row in cirrus["direct"]["corrections"]][:2] == [["c1"], ["c1", "c3"]]


def test_r08():
    """Shared keys stay separated by partition in mixed cases."""
    boreal = cases_by_name()["boreal"]
    flux = cases_by_name()["flux"]
    assert {row["partition"] for row in boreal["direct"]["totals"]} == {"p0", "p1"}
    assert {row["partition"] for row in flux["direct"]["totals"]} == {"p0", "p1"}
    assert boreal["direct"]["totals"] == expected_totals("boreal")
    assert flux["direct"]["totals"] == expected_totals("flux")


def test_r09():
    """Late-heavy cases preserve all derived correction rows."""
    for name in ["drift", "ember"]:
        case = cases_by_name()[name]
        assert project(case["replay"]["corrections"]) == expected_corrections(name)
        assert len(case["replay"]["corrections"]) == len(expected_corrections(name))


def test_r10():
    """Restarted correction records do not contain repeated ids."""
    for case in cases_by_name().values():
        ids = [row["id"] for row in case["replay"]["corrections"]]
        assert len(ids) == len(set(ids))


def test_r11():
    """Correction ids bind the row fields and every lineage member."""
    for case in cases_by_name().values():
        for row in case["replay"]["corrections"]:
            assert row["id"] == expected_id(case["name"], row)


def test_r12():
    """Full invocations are stable and remain derived from case inputs."""
    global _CACHE
    first = cases_by_name()
    second = cases_by_name(force=True)
    assert first == second

    paths = {
        "boreal": APP / "data" / "cases" / "boreal.csv",
        "flux": APP / "data" / "cases" / "flux.csv",
    }
    originals = {name: path.read_text(encoding="utf-8") for name, path in paths.items()}
    try:
        boreal_lines = originals["boreal"].rstrip("\n").splitlines()
        changed_boreal = ["9,p9,32,zeta,17,b3", "0,p8,32,zeta,-19,b3"] + boreal_lines
        changed_boreal.extend(["6,p0,22,beta,11,b_dyn", "7,p1,22,beta,2,b_extra"])
        paths["boreal"].write_text("\n".join(changed_boreal) + "\n", encoding="utf-8")

        flux_lines = originals["flux"].rstrip("\n").splitlines()
        changed_flux = ["9,p9,30,omega,21,f3", "0,p8,30,omega,-13,f3"] + flux_lines
        changed_flux.extend(["7,p0,20,flux,8,f_dyn", "8,p1,20,flux,-6,f_extra"])
        paths["flux"].write_text("\n".join(changed_flux) + "\n", encoding="utf-8")

        changed_cases = cases_by_name(force=True)
        for name in ["boreal", "flux"]:
            changed = changed_cases[name]
            assert changed["direct"]["totals"] == expected_totals(name)
            assert changed["replay"]["totals"] == expected_totals(name)
            assert compact(changed["direct"]["corrections"]) == expected_corrections(name)
            assert compact(changed["replay"]["corrections"]) == expected_corrections(name)
    finally:
        for name, path in paths.items():
            path.write_text(originals[name], encoding="utf-8")
        _CACHE = None
        if OUT.exists():
            OUT.unlink()
