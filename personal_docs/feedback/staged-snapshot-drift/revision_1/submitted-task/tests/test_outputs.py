import json
import os
import subprocess
from pathlib import Path

import pytest


APP = Path(os.environ.get("APP_ROOT", "/app"))
AUDIT = APP / "output" / "restore-audit.json"


@pytest.fixture(scope="session")
def matrix_data() -> dict:
    """Run the matrix once and return the parsed audit."""
    if AUDIT.exists():
        AUDIT.unlink()
    proc = subprocess.run(
        ["bash", str(APP / "scripts" / "run-matrix.sh")],
        cwd=APP,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (APP / "bin" / "snapctl").exists()
    assert (APP / "bin" / "fsmeasure").exists()
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert "cases" in data and data["cases"]
    assert {case.get("name") for case in data["cases"]} == {
        "alpha",
        "beta",
        "gamma",
        "delta",
        "epsilon",
        "zeta",
    }
    return data


def case_by_name(data: dict, name: str) -> dict:
    matches = [case for case in data["cases"] if case.get("name") == name]
    assert matches
    return matches[0]


def tree_entries(root: Path):
    entries = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_dir():
            entries.append(("dir", rel, ""))
        elif path.is_file():
            entries.append(("file", rel, path.read_text(encoding="utf-8")))
    return entries


def groups_for(root: Path):
    groups = {}
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        st = path.stat()
        groups.setdefault((st.st_dev, st.st_ino), []).append(path.relative_to(root).as_posix())
    return sorted(sorted(v) for v in groups.values() if len(v) > 1)


def account_for(root: Path, name: str):
    roll = name in {"epsilon", "zeta"}
    items = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix()
        period = "p1" if roll and rel.startswith("d/") else "p0"
        items.append({"path": rel, "bytes": len(path.read_bytes()), "period": period})
    return items


def normalize_groups(value):
    return sorted(sorted(group) for group in value)


def assert_group_order(value) -> None:
    assert value == sorted(value, key=lambda group: group[0] if group else "")
    for group in value:
        assert group == sorted(group)


def normalize_accounting(value):
    return sorted(value, key=lambda item: (item["path"], item["bytes"], item["period"]))


def assert_case_clean(case: dict) -> None:
    assert set(case) >= {"name", "source", "restored", "ok", "digest", "groups", "accounting"}
    src = Path(case["source"])
    dst = Path(case["restored"])
    assert src.exists() and dst.exists()
    assert src != dst
    assert case["ok"] is True
    assert tree_entries(src) == tree_entries(dst)
    assert groups_for(src) == groups_for(dst)
    assert set(case["digest"]) == {"source", "restored"}
    assert isinstance(case["digest"]["source"], str) and case["digest"]["source"]
    assert isinstance(case["digest"]["restored"], str) and case["digest"]["restored"]
    assert case["digest"]["source"] == case["digest"]["restored"]
    assert set(case["groups"]) == {"source", "restored"}
    assert_group_order(case["groups"]["source"])
    assert_group_order(case["groups"]["restored"])
    assert normalize_groups(case["groups"]["source"]) == groups_for(src)
    assert normalize_groups(case["groups"]["restored"]) == groups_for(dst)
    assert normalize_groups(case["groups"]["source"]) == normalize_groups(case["groups"]["restored"])
    assert normalize_accounting(case["accounting"]) == account_for(src, case["name"])
    assert normalize_accounting(case["accounting"]) == account_for(dst, case["name"])


def test_run_matrix_produces_output(matrix_data):
    """The documented matrix command writes the all-case audit file."""
    assert AUDIT.exists()
    assert matrix_data["cases"]


def test_alpha_matrix(matrix_data):
    """Baseline restore still has to match independent tree inspection."""
    assert_case_clean(case_by_name(matrix_data, "alpha"))


def test_beta_matrix(matrix_data):
    """Dense file identity groups survive a stop/start boundary."""
    case = case_by_name(matrix_data, "beta")
    assert groups_for(Path(case["source"]))
    assert_case_clean(case)


def test_gamma_matrix(matrix_data):
    """Interleaved row history reaches the same restored final tree after restart."""
    case = case_by_name(matrix_data, "gamma")
    assert (Path(case["source"]) / "a" / "flow.txt").read_text(encoding="utf-8") == "second\n"
    assert_case_clean(case)


def test_delta_matrix(matrix_data):
    """Accounting rows agree with source-side observations."""
    assert_case_clean(case_by_name(matrix_data, "delta"))


def test_epsilon_matrix(matrix_data):
    """Period transition records move with the restored tree."""
    case = case_by_name(matrix_data, "epsilon")
    assert any(item["period"] == "p1" for item in account_for(Path(case["source"]), "epsilon"))
    assert_case_clean(case)


def test_zeta_matrix(matrix_data):
    """The mixed case requires ordering, file identity, and accounting to agree."""
    case = case_by_name(matrix_data, "zeta")
    assert groups_for(Path(case["source"]))
    assert any(item["period"] == "p1" for item in account_for(Path(case["source"]), "zeta"))
    assert_case_clean(case)
