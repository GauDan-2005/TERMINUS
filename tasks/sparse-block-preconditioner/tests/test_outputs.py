import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

APP = Path(os.environ.get("APP_ROOT", "/app"))
AUDIT = APP / "output" / "solver-audit.json"
CASE_DIR = APP / "data" / "cases"
CASES = ["basalt", "flint", "shale", "garnet", "mica", "opal"]
MAX_ITER = 200
MAX_BLOCKS = 8
MAX_BS = 4
MAX_NNZ = 64
MAX_DIM = 32
AGREE_TOL = 1e-6
RES_RTOL = 1e-5


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


def _l2_norm(v: list[float]) -> float:
    return sum(x * x for x in v) ** 0.5


def load_case(path: Path) -> dict:
    spec: dict = {
        "name": "",
        "nblocks": 0,
        "bs": 0,
        "reorder": 0,
        "perm": list(range(MAX_BLOCKS)),
        "blocks": [],
        "rhs": [0.0] * (MAX_BLOCKS * MAX_BS),
    }
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("name "):
            spec["name"] = line[5:].strip()
        elif line.startswith("nblocks "):
            spec["nblocks"] = int(line.split()[1])
        elif line.startswith("bs "):
            spec["bs"] = int(line.split()[1])
        elif line.startswith("reorder "):
            spec["reorder"] = int(line.split()[1])
        elif line.startswith("perm "):
            spec["perm"] = [int(x) for x in line.split()[1:]]
        elif line.startswith("block "):
            parts = line.split()
            rb, cb = int(parts[1]), int(parts[2])
            vals = [float(x) for x in parts[3:]]
            spec["blocks"].append({"rb": rb, "cb": cb, "vals": vals})
        elif line.startswith("rhs "):
            spec["rhs"] = [float(x) for x in line.split()[1:]]
    return spec


def matrix_from_case(spec: dict) -> dict:
    dim = spec["nblocks"] * spec["bs"]
    view = {
        "n": dim,
        "bs": spec["bs"],
        "nblocks": spec["nblocks"],
        "reorder": spec["reorder"],
        "perm": list(spec["perm"][: spec["nblocks"]]),
        "a": [[0.0] * dim for _ in range(dim)],
        "b": list(spec["rhs"][:dim]),
    }
    for be in spec["blocks"]:
        rb, cb, bs = be["rb"], be["cb"], spec["bs"]
        for r in range(bs):
            for c in range(bs):
                gr, gc = rb * bs + r, cb * bs + c
                view["a"][gr][gc] = be["vals"][r * bs + c]
    return view


def _block_present(view: dict, row_blk: int, col_blk: int) -> bool:
    bs = view["bs"]
    for r in range(bs):
        for c in range(bs):
            gr, gc = row_blk * bs + r, col_blk * bs + c
            if view["a"][gr][gc] != 0.0:
                return True
    return False


def pack_from_view(view: dict) -> dict:
    nb, bs, dim = view["nblocks"], view["bs"], view["n"]
    reorder = view["reorder"]
    pack = {
        "n": dim,
        "bs": bs,
        "nblocks": nb,
        "reorder": reorder,
        "perm": list(view["perm"]),
        "row_ptr": [0] * (nb + 1),
        "col_idx": [],
        "data": [],
        "diag_inv": [1.0] * dim,
    }
    ptr = 0
    for bi in range(nb):
        row_blk = view["perm"][bi] if reorder else bi
        pack["row_ptr"][bi] = ptr
        for bj in range(nb):
            col_blk = view["perm"][bj] if reorder else bj
            if _block_present(view, row_blk, col_blk):
                pack["col_idx"].append(bj)
                block = [[0.0] * bs for _ in range(bs)]
                for r in range(bs):
                    for c in range(bs):
                        gr, gc = row_blk * bs + r, col_blk * bs + c
                        block[r][c] = view["a"][gr][gc]
                pack["data"].append(block)
                ptr += 1
    pack["row_ptr"][nb] = ptr
    for bi in range(nb):
        start, end = pack["row_ptr"][bi], pack["row_ptr"][bi + 1]
        for k in range(start, end):
            if pack["col_idx"][k] == bi:
                for r in range(bs):
                    d = pack["data"][k][r][r]
                    if abs(d) > 1e-14:
                        pack["diag_inv"][bi * bs + r] = 1.0 / d
    return pack


def bsr_matvec(pack: dict, x: list[float]) -> list[float]:
    dim, bs, nb = pack["n"], pack["bs"], pack["nblocks"]
    y = [0.0] * dim
    for bi in range(nb):
        for k in range(pack["row_ptr"][bi], pack["row_ptr"][bi + 1]):
            bj = pack["col_idx"][k]
            block = pack["data"][k]
            for r in range(bs):
                for c in range(bs):
                    gi, gj = bi * bs + r, bj * bs + c
                    y[gi] += block[r][c] * x[gj]
    return y


def map_p(src: list[float], perm: list[int], n: int, bs: int) -> list[float]:
    nb = n // bs
    out = [0.0] * n
    for bi in range(nb):
        src_blk = perm[bi]
        for r in range(bs):
            out[bi * bs + r] = src[src_blk * bs + r]
    return out


def step_r(pack: dict, b: list[float]) -> list[float]:
    bs = pack["bs"]
    out = [0.0] * pack["n"]
    for i in range(pack["n"]):
        blk, loc = i // bs, i % bs
        inv = pack["diag_inv"][blk * bs + loc]
        if inv == 0.0:
            inv = 1.0
        out[i] = inv * b[i]
    return out


def norm_q(v: list[float]) -> float:
    return _l2_norm(v)


def pcg_solve(pack: dict, rhs: list[float]) -> tuple[int, int, list[float]]:
    n = pack["n"]
    tol = 1e-9
    x = [0.0] * n
    r = [rhs[i] - bsr_matvec(pack, x)[i] for i in range(n)]
    rs = _l2_norm(r)
    if rs < tol:
        return 0, 0, x
    z = step_r(pack, r)
    p = list(z)
    rz_old = sum(r[i] * z[i] for i in range(n))
    hit = 1
    iters = MAX_ITER
    for k in range(1, MAX_ITER + 1):
        ap = bsr_matvec(pack, p)
        denom = sum(p[i] * ap[i] for i in range(n))
        if abs(denom) < 1e-30:
            break
        alpha = rz_old / denom
        for i in range(n):
            x[i] += alpha * p[i]
            r[i] -= alpha * ap[i]
        rs = _l2_norm(r)
        if rs < tol:
            return k, 0, x
        z = step_r(pack, r)
        beta = sum(r[i] * z[i] for i in range(n)) / rz_old
        p = [z[i] + beta * p[i] for i in range(n)]
        rz_old = sum(r[i] * z[i] for i in range(n))
        iters = k
    return iters, hit, x


def reference_row(name: str) -> dict:
    spec = load_case(CASE_DIR / f"{name}.case")
    view = matrix_from_case(spec)
    pack = pack_from_view(view)
    rhs = map_p(view["b"], view["perm"], view["n"], view["bs"])
    iters, hit, x = pcg_solve(pack, rhs)
    n, bs, nb = view["n"], view["bs"], view["nblocks"]
    xo = [0.0] * n
    for bi in range(nb):
        dst = view["perm"][bi] if view["reorder"] else bi
        for t in range(bs):
            xo[dst * bs + t] = x[bi * bs + t]
    ax = [sum(view["a"][i][j] * xo[j] for j in range(n)) for i in range(n)]
    resid = [view["b"][i] - ax[i] for i in range(n)]
    true_res = _l2_norm(resid)
    rep_res = norm_q(resid)
    agrees = abs(rep_res - true_res) <= AGREE_TOL * (1.0 + true_res)
    ok = (not hit) and (true_res < 1e-8) and agrees
    return {
        "name": name,
        "ok": ok,
        "iterations": iters,
        "final_residual": true_res,
        "reported_residual": rep_res,
        "residual_agrees": agrees,
        "hit_limit": bool(hit),
    }


def res_close(a: float, b: float, rtol: float = RES_RTOL) -> bool:
    scale = max(abs(a), abs(b), 1.0)
    return abs(a - b) <= rtol * scale


def assert_row_matches(audit: dict, expected: dict) -> None:
    assert audit["name"] == expected["name"]
    assert audit["iterations"] == expected["iterations"]
    assert audit["hit_limit"] == expected["hit_limit"]
    assert audit["ok"] == expected["ok"]
    assert audit["residual_agrees"] == expected["residual_agrees"]
    assert res_close(audit["final_residual"], expected["final_residual"])
    assert res_close(audit["reported_residual"], expected["reported_residual"])


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
    """Basalt identity layout matches the independent reference."""
    row = case_map(matrix_report)["basalt"]
    expected = reference_row("basalt")
    assert_row_matches(row, expected)
    assert expected["iterations"] <= 20


def test_d3_flint_off_diagonal_converges(matrix_report: dict) -> None:
    """Flint coupled identity layout matches the independent reference."""
    row = case_map(matrix_report)["flint"]
    assert_row_matches(row, reference_row("flint"))


def test_e4_shale_reordered_converges(matrix_report: dict) -> None:
    """Shale reordered system matches the independent reference."""
    row = case_map(matrix_report)["shale"]
    assert_row_matches(row, reference_row("shale"))


def test_f5_garnet_reordered_converges(matrix_report: dict) -> None:
    """Garnet three-block reorder matches the independent reference."""
    row = case_map(matrix_report)["garnet"]
    assert_row_matches(row, reference_row("garnet"))


def test_g6_mica_low_final_residual(matrix_report: dict) -> None:
    """Mica reordered run matches the independent reference."""
    row = case_map(matrix_report)["mica"]
    assert_row_matches(row, reference_row("mica"))


def test_h7_opal_mixed_reordered_residuals(matrix_report: dict) -> None:
    """Opal mixed reorder scenario matches the independent reference."""
    row = case_map(matrix_report)["opal"]
    expected = reference_row("opal")
    assert_row_matches(row, expected)
    assert abs(row["reported_residual"] - row["final_residual"]) <= AGREE_TOL * (
        1.0 + row["final_residual"]
    )


def test_i8_reported_matches_true_residual(matrix_report: dict) -> None:
    """Every case matches the independent reference for residual fields."""
    for name in CASES:
        row = case_map(matrix_report)[name]
        expected = reference_row(name)
        assert_row_matches(row, expected)


def test_j9_two_matrix_runs_equivalent(matrix_report: dict) -> None:
    """Two matrix runs from unchanged inputs produce equivalent JSON."""
    second = rerun_matrix_only()
    assert matrix_report == second


def test_k0_convergent_cases_below_cap(matrix_report: dict) -> None:
    """Convergent scenarios match reference and stay below the iteration cap."""
    for name in CASES:
        row = case_map(matrix_report)[name]
        expected = reference_row(name)
        assert_row_matches(row, expected)
        assert expected["iterations"] < MAX_ITER


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
    assert res_close(direct["final_residual"], matrix["final_residual"])


def test_z9_row_status_flags(matrix_report: dict) -> None:
    """Every matrix row status matches the independent reference."""
    for row in matrix_report["cases"]:
        assert_row_matches(row, reference_row(row["name"]))
