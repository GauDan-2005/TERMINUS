import json
import subprocess
from pathlib import Path

import pytest


APP = Path("/app")
REPORT = APP / "output" / "policy-audit.json"
OUTCOME_OK = "allow"
OUTCOME_NO = "deny"


@pytest.fixture(scope="session")
def report_data():
    """Run the matrix once and return the parsed report."""
    subprocess.run(["bash", "/app/scripts/run-matrix.sh"], cwd=APP, check=True, timeout=180)
    return json.loads(REPORT.read_text(encoding="utf-8"))


def case_by_name(data, name):
    cases = {item["name"]: item for item in data["cases"]}
    assert name in cases, (name, sorted(cases))
    return cases[name]


def row_by_label(case, label):
    rows = {item["label"]: item for item in case["decisions"]}
    assert label in rows, (label, sorted(rows))
    return rows[label]


def test_t01_flow(report_data):
    """Alpha denies inherited rows once a subject is blocked."""
    alpha = case_by_name(report_data, "alpha")
    before = row_by_label(alpha, "before")
    batch = row_by_label(alpha, "batch")
    after = row_by_label(alpha, "after")

    assert before["verdict"] == OUTCOME_OK
    assert before["delegated_from"] == "boss"
    assert batch["verdict"] == OUTCOME_NO
    assert batch["batch_id"] == "b1"
    assert after["verdict"] == OUTCOME_NO


def test_t02_flow(report_data):
    """Beta clears an earlier miss once a direct row is granted."""
    beta = case_by_name(report_data, "beta")
    miss = row_by_label(beta, "miss")
    solo = row_by_label(beta, "solo")

    assert miss["verdict"] == OUTCOME_NO
    assert solo["verdict"] == OUTCOME_OK
    assert solo["reused"] is False


def test_t03_flow(report_data):
    """Gamma blocks inherited rows when an upstream subject is blocked."""
    gamma = case_by_name(report_data, "gamma")
    batch = row_by_label(gamma, "batch")

    assert batch["verdict"] == OUTCOME_NO
    assert batch["delegated_from"] == ""


def test_t04_flow(report_data):
    """Delta keeps reuse for an unchanged subject across an unrelated block."""
    delta = case_by_name(report_data, "delta")
    first = row_by_label(delta, "first")
    second = row_by_label(delta, "second")

    assert first["verdict"] == OUTCOME_OK
    assert first["reused"] is False
    assert second["verdict"] == OUTCOME_OK
    assert second["reused"] is True


def test_t05_flow(report_data):
    """Epsilon blocks inherited rows when a middle link is blocked."""
    epsilon = case_by_name(report_data, "epsilon")
    check = row_by_label(epsilon, "check")

    assert check["verdict"] == OUTCOME_NO


def test_t06_flow(report_data):
    """Zeta grouped replay isolates blocked and clean subjects."""
    zeta = case_by_name(report_data, "zeta")
    alpha_row = row_by_label(zeta, "a")
    beta_row = row_by_label(zeta, "b")

    assert alpha_row["verdict"] == OUTCOME_NO
    assert beta_row["verdict"] == OUTCOME_OK
    assert alpha_row["batch_id"] == "mix"
    assert beta_row["batch_id"] == "mix"


def test_t07_flow(report_data):
    """Every case is clean with an empty stale list."""
    for case in report_data["cases"]:
        assert case["ok"] is True
        assert case["stale"] == []


def test_t08_flow(report_data):
    """Post-block rows in alpha stay rejected."""
    alpha = case_by_name(report_data, "alpha")
    for row in alpha["decisions"]:
        if row["label"] in {"batch", "after"}:
            assert row["verdict"] == OUTCOME_NO


def test_t09_flow(report_data):
    """Epochs are monotonic and blocked subjects carry updated ticks."""
    alpha = case_by_name(report_data, "alpha")
    epochs = [row["epoch"] for row in alpha["decisions"]]
    assert epochs == sorted(epochs)
    before = row_by_label(alpha, "before")
    after = row_by_label(alpha, "after")
    assert after["epoch"] > before["epoch"]


def test_t10_flow(report_data):
    """Delegated_from names the grantor on inherited ok rows and stays empty on direct rows."""
    alpha = case_by_name(report_data, "alpha")
    before = row_by_label(alpha, "before")
    assert before["delegated_from"] == "boss"

    delta = case_by_name(report_data, "delta")
    first = row_by_label(delta, "first")
    assert first["delegated_from"] == ""


def test_t11_flow(report_data):
    """Batch_id is populated only inside grouped checks."""
    alpha = case_by_name(report_data, "alpha")
    assert row_by_label(alpha, "before")["batch_id"] == ""
    assert row_by_label(alpha, "batch")["batch_id"] == "b1"
    assert row_by_label(alpha, "after")["batch_id"] == ""


def test_t12_flow(report_data):
    """Two consecutive matrix runs produce byte-identical output."""
    subprocess.run(["bash", "/app/scripts/run-matrix.sh"], cwd=APP, check=True, timeout=180)
    first = REPORT.read_bytes()
    subprocess.run(["bash", "/app/scripts/run-matrix.sh"], cwd=APP, check=True, timeout=180)
    second = REPORT.read_bytes()
    assert first == second


def test_t13_flow(report_data):
    """Decision rows carry the correct principal, resource, and action for each subject."""
    expected = {
        ("alpha", "before"): ("clerk", "vault", "read"),
        ("beta", "solo"): ("intern", "vault", "read"),
        ("gamma", "batch"): ("intern", "vault", "write"),
        ("epsilon", "check"): ("leaf", "api", "invoke"),
        ("zeta", "a"): ("alpha", "secret", "read"),
        ("zeta", "b"): ("beta", "secret", "read"),
    }
    for (case_name, label), (principal, resource, action) in expected.items():
        row = row_by_label(case_by_name(report_data, case_name), label)
        assert row["principal"] == principal, (case_name, label, row)
        assert row["resource"] == resource, (case_name, label, row)
        assert row["action"] == action, (case_name, label, row)


def _run_engine(trace_text, work_dir):
    """Write a trace at runtime, run the engine on it, and return the parsed report."""
    trace_path = work_dir / "alpha.trace"
    out_path = work_dir / "policy-audit.json"
    trace_path.write_text(trace_text, encoding="utf-8")
    subprocess.run(
        [
            "cargo", "run", "--offline", "--quiet",
            "--manifest-path", str(APP / "Cargo.toml"),
            "--", str(out_path), str(trace_path),
        ],
        cwd=str(APP),
        check=True,
        timeout=180,
    )
    return json.loads(out_path.read_text(encoding="utf-8"))


def test_t14_flow(tmp_path):
    """A trace built at runtime is evaluated live: the same delegated check flips to deny once the
    grantor is revoked, so no precomputed report can satisfy both variants."""
    obj, act = "vault", "read"
    base = f"grant boss {obj}/{act}\ndelegate boss clerk\n"
    probe = f"check before clerk:{obj}/{act}\n"

    allow = _run_engine(base + probe, tmp_path)
    row = row_by_label(case_by_name(allow, "alpha"), "before")
    assert row["principal"] == "clerk"
    assert row["resource"] == obj
    assert row["action"] == act
    assert row["verdict"] == OUTCOME_OK
    assert row["delegated_from"] == "boss"

    deny = _run_engine(base + "revoke boss -\n" + probe, tmp_path)
    row2 = row_by_label(case_by_name(deny, "alpha"), "before")
    assert row2["verdict"] == OUTCOME_NO
    assert row2["delegated_from"] == ""
