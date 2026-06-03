import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

APP = Path(os.environ.get("APP_ROOT", "/app"))
AUDIT = APP / "output" / "solver-audit.json"
CASES = ["basalt", "flint", "shale", "garnet", "mica", "opal"]
MAX_ITER = 200
AGREE_TOL = 1e-6


def run_matrix(rebuild: bool = True) -> dict:
    if AUDIT.exists():
        AUDIT.unlink()
    if rebuild:
        build = APP / "build"
        if build.exists():
            shutil.rmtree(build)
        subprocess.run(["cmake", "-S", str(APP), "-B", str(APP / "build")], check=True)
        subprocess.run(["cmake", "--build", str(APP / "build")], check=True)
        subprocess.run(["install", "-d", str(APP / "bin")], check=True)
        subprocess.run(
            [
                "install",
                "-m",
                "0755",
                str(APP / "build" / "bin" / "solverctl"),
                str(APP / "bin" / "solverctl"),
            ],
            check=True,
        )
    subprocess.run(["bash", str(APP / "scripts" / "run-matrix.sh")], check=True)
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def rerun_matrix_only() -> dict:
    if AUDIT.exists():
        AUDIT.unlink()
    subprocess.run(["bash", str(APP / "scripts" / "clean-room.sh")], check=True)
    subprocess.run(["bash", str(APP / "scripts" / "run-matrix.sh")], check=True)
    return json.loads(AUDIT.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def matrix_report() -> dict:
    return run_matrix()


def case_map(report: dict) -> dict[str, dict]:
    return {row["name"]: row for row in report["cases"]}


def test_a0_matrix_cases_present(matrix_report: dict) -> None:
    """Matrix command covers basalt through opal."""
    rows = case_map(matrix_report)
    assert set(rows) == set(CASES)


def test_b1_run_one_basalt_matches_matrix(matrix_report: dict) -> None:
    """Direct basalt audit matches the matrix slice."""
    case = "basalt"
    one = APP / "output" / f"{case}-audit.json"
    if one.exists():
        one.unlink()
    subprocess.run(["bash", str(APP / "scripts" / "run-one.sh"), case], check=True)
    direct = json.loads(one.read_text(encoding="utf-8"))["cases"][0]
    matrix = case_map(matrix_report)["basalt"]
    for key in (
        "name",
        "ok",
        "iterations",
        "final_residual",
        "reported_residual",
        "residual_agrees",
        "hit_limit",
    ):
        assert direct[key] == matrix[key]


def test_c2_basalt_converges_quickly(matrix_report: dict) -> None:
    """Basalt identity layout converges in modest iterations."""
    row = case_map(matrix_report)["basalt"]
    assert row["iterations"] <= 20
    assert row["final_residual"] < 1e-8
    assert row["iterations"] < MAX_ITER


def test_d3_flint_off_diagonal_converges(matrix_report: dict) -> None:
    """Flint coupled identity layout reaches a small residual."""
    row = case_map(matrix_report)["flint"]
    assert row["final_residual"] < 1e-8
    assert row["iterations"] < MAX_ITER


def test_e4_shale_reordered_converges(matrix_report: dict) -> None:
    """Shale reordered system converges within the iteration cap."""
    row = case_map(matrix_report)["shale"]
    assert row["final_residual"] < 1e-7
    assert row["iterations"] < MAX_ITER


def test_f5_garnet_reordered_converges(matrix_report: dict) -> None:
    """Garnet three-block reorder reaches a small residual."""
    row = case_map(matrix_report)["garnet"]
    assert row["final_residual"] < 1e-8
    assert row["iterations"] < MAX_ITER


def test_g6_mica_low_final_residual(matrix_report: dict) -> None:
    """Mica reordered run reports a small final residual."""
    row = case_map(matrix_report)["mica"]
    assert row["final_residual"] < 1e-7
    assert row["iterations"] < MAX_ITER


def test_h7_opal_mixed_reordered_residuals(matrix_report: dict) -> None:
    """Opal mixed reorder scenario keeps reported and final residuals aligned."""
    row = case_map(matrix_report)["opal"]
    assert row["final_residual"] < 1e-7
    assert abs(row["reported_residual"] - row["final_residual"]) <= AGREE_TOL * (
        1.0 + row["final_residual"]
    )


def test_i8_reported_matches_true_residual(matrix_report: dict) -> None:
    """Reported residual tracks final residual for every case."""
    for name in CASES:
        row = case_map(matrix_report)[name]
        assert abs(row["reported_residual"] - row["final_residual"]) <= AGREE_TOL * (
            1.0 + row["final_residual"]
        )


def test_j9_two_matrix_runs_equivalent(matrix_report: dict) -> None:
    """Two matrix runs from unchanged inputs produce equivalent JSON."""
    second = rerun_matrix_only()
    assert matrix_report == second


def test_k0_convergent_cases_below_cap(matrix_report: dict) -> None:
    """Convergent scenarios stay below the iteration cap."""
    for name in CASES:
        row = case_map(matrix_report)[name]
        assert row["iterations"] < MAX_ITER


def test_l1_run_one_shale_matches_matrix(matrix_report: dict) -> None:
    """Direct shale audit matches the matrix slice."""
    case = "shale"
    one = APP / "output" / f"{case}-audit.json"
    if one.exists():
        one.unlink()
    subprocess.run(["bash", str(APP / "scripts" / "run-one.sh"), case], check=True)
    direct = json.loads(one.read_text(encoding="utf-8"))["cases"][0]
    matrix = case_map(matrix_report)["shale"]
    assert direct["iterations"] == matrix["iterations"]
    assert direct["ok"] == matrix["ok"]
    assert abs(direct["final_residual"] - matrix["final_residual"]) <= 1e-12


def test_z9_row_status_flags(matrix_report: dict) -> None:
    """Every matrix row reports a clean status flag."""
    for row in matrix_report["cases"]:
        assert row["ok"] is True
