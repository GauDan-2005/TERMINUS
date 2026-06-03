import json
import subprocess
from pathlib import Path


APP = Path("/app")
OUT = Path("/app/output/report.json")
RAW = Path("/app/output/raw.json")
RUNNER = "/app/tools/run_local.sh"
ALIGN = "/app/cmd/align/main.go"
CHECK_RAW = Path("/tmp/check_raw.json")

SCALES = [2, 3, 5]
BIASES = [1, -1, 2]

CASES = {
    "alpha": {"packed": False, "group": True, "reuse": False, "order": [0, 1], "rows": [[21, 10, 4], [15, 8, 6]]},
    "beta": {"packed": True, "group": False, "reuse": False, "order": [0], "rows": [[10, 4, 1]]},
    "gamma": {"packed": True, "group": True, "reuse": False, "order": [0, 1], "rows": [[8, 3, 2], [6, 5, 1]]},
    "delta": {"packed": True, "group": True, "reuse": False, "order": [1, 0], "rows": [[7, 4, 2], [5, 6, 3]]},
    "epsilon": {"packed": True, "group": True, "reuse": True, "order": [1, 0, 2], "rows": [[4, 7, 2], [9, 2, 3], [3, 8, 1]]},
    "zeta": {"packed": False, "group": True, "reuse": True, "order": [2, 0, 1], "rows": [[12, 9, 5], [18, 4, 7], [10, 6, 8]]},
}


def run_report():
    subprocess.run([RUNNER], cwd=APP, check=True)
    return json.loads(OUT.read_text()), json.loads(RAW.read_text())


def run_align_only():
    subprocess.run(
        ["go", "run", ALIGN, "/app/output/raw.json", "/app/output/report.json"],
        cwd=APP,
        check=True,
    )
    return json.loads(OUT.read_text())


def expand(row, packed):
    if not packed:
        return row
    return [value * SCALES[idx] + BIASES[idx] for idx, value in enumerate(row)]


def expected_tokens(name):
    spec = CASES[name]
    tokens = []
    for slot in spec["order"]:
        total = sum(expand(spec["rows"][slot], spec["packed"]))
        value = total + slot * 7
        if spec["packed"]:
            value += 3
        if spec["group"]:
            value += 5
        if spec["reuse"]:
            value += 11
        tokens.append(value % 101)
    return tokens


def rows_by_name(report):
    return {row["case"]: row for row in report["rows"]}


def raw_by_name(raw):
    return {row["case"]: row for row in raw["raw"]}


def corrupt_raw_field(raw, field, index=0):
    corrupted = json.loads(json.dumps(raw))
    entry = corrupted["raw"][index]
    if field == "produced":
        entry["produced"][0] += 1
    elif field in ("slot_trace", "order_used"):
        entry[field][0] += 1
    elif field in ("packed", "grouped", "reuse"):
        entry[field] = not entry[field]
    else:
        raise ValueError(f"unknown field: {field}")
    return corrupted


def test_alpha_path():
    """Uncompressed grouped rows keep their derived token values."""
    report, _ = run_report()
    row = rows_by_name(report)["alpha"]
    assert row["produced"] == expected_tokens("alpha")


def test_beta_path():
    """Compressed single-request rows use per-column reconstruction."""
    report, _ = run_report()
    row = rows_by_name(report)["beta"]
    assert row["produced"] == expected_tokens("beta")


def test_gamma_path():
    """Compressed grouped rows match independently derived values."""
    report, _ = run_report()
    row = rows_by_name(report)["gamma"]
    assert row["produced"] == expected_tokens("gamma")


def test_delta_path():
    """Changed candidate order preserves token identity."""
    report, _ = run_report()
    row = rows_by_name(report)["delta"]
    assert row["produced"] == expected_tokens("delta")
    assert row["slot_trace"] == CASES["delta"]["order"]


def test_epsilon_path():
    """Reusable local storage stays isolated across adjacent requests."""
    report, _ = run_report()
    row = rows_by_name(report)["epsilon"]
    assert row["produced"] == expected_tokens("epsilon")
    assert row["slot_trace"] == CASES["epsilon"]["order"]


def test_zeta_path():
    """Raw trace rows agree with final rows for plain shuffled grouped runs."""
    report, raw = run_report()
    assert rows_by_name(report)["zeta"]["produced"] == expected_tokens("zeta")
    assert rows_by_name(report)["zeta"]["produced"] == raw_by_name(raw)["zeta"]["produced"]
    assert rows_by_name(report)["zeta"]["slot_trace"] == CASES["zeta"]["order"]


def test_eta_path():
    """Every final row carries the order used by that case."""
    report, _ = run_report()
    for name, spec in CASES.items():
        assert rows_by_name(report)[name]["order_used"] == spec["order"]


def test_theta_path():
    """The summary reports the full built-in case count."""
    report, _ = run_report()
    assert report["summary"]["total"] == len(CASES)


def test_iota_path():
    """The collation layer keeps one final row per built-in case."""
    report, _ = run_report()
    assert sorted(rows_by_name(report)) == sorted(CASES)


def test_kappa_path():
    """Repeated local runs produce identical reports."""
    first, _ = run_report()
    second, _ = run_report()
    assert first == second


def test_lambda_path():
    """Each row carries the correct packed, grouped, and reuse flags."""
    report, _ = run_report()
    for name, spec in CASES.items():
        row = rows_by_name(report)[name]
        assert row["packed"] == spec["packed"]
        assert row["grouped"] == spec["group"]
        assert row["reuse"] == spec["reuse"]


def test_nu_path():
    """Every final row produced values match the corresponding raw entry."""
    report, raw = run_report()
    for name in CASES:
        assert rows_by_name(report)[name]["produced"] == raw_by_name(raw)[name]["produced"]


def test_mu_path():
    """Summary agree is true when aligned and false after any raw field mismatch."""
    report, raw = run_report()
    assert report["summary"]["agree"] is True

    for field in ("produced", "slot_trace", "order_used", "packed", "grouped", "reuse"):
        corrupted = corrupt_raw_field(raw, field)
        RAW.write_text(json.dumps(corrupted, indent=2) + "\n")
        report = run_align_only()
        assert report["summary"]["agree"] is False, field
        _, raw = run_report()

    corrupted_mid = corrupt_raw_field(raw, "produced", index=3)
    RAW.write_text(json.dumps(corrupted_mid, indent=2) + "\n")
    report = run_align_only()
    assert report["summary"]["agree"] is False, "mid-entry corruption"


def test_rust_stage_produces_raw():
    """raw.json is produced by the Rust binary, not a stub script."""
    result = subprocess.run(
        [
            "cargo",
            "run",
            "--quiet",
            "--manifest-path",
            "/app/Cargo.toml",
            "--",
            str(CHECK_RAW),
        ],
        cwd=APP,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    raw = json.loads(CHECK_RAW.read_text())
    assert sorted(row["case"] for row in raw["raw"]) == sorted(CASES)
    for name in CASES:
        entry = next(row for row in raw["raw"] if row["case"] == name)
        assert entry["produced"] == expected_tokens(name)
