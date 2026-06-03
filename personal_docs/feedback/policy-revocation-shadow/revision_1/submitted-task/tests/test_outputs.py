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
