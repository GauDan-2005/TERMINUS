import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

APP = Path(os.environ.get("APP_ROOT", "/app"))
AUDIT = APP / "output" / "conservation_audit.json"
AUDIT_LOG = APP / "output" / "persistence_audit.log"
CASES_TOML = APP / "config" / "cases.toml"
INIT_DIR = APP / "data" / "init"
BUILD = APP / "build"

NVAR = 3
REFLUX_RATE = 0.25
LEAF_SPREAD = 0.1
SCENARIOS = ["storm", "canyon", "plume", "spire", "basin", "dune"]
CANARY = "tb_amr_noembed_8d7a4c2f"
FIX_DIRS = ["acc_m", "lnk_n", "agg_q", "srl_p", "rsm_k", "sync_b"]


def _parse_cases():
    """Parse the scenario sections from config/cases.toml into dicts."""
    secs = {}
    cur = None
    for raw in CASES_TOML.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith("[") and s.endswith("]"):
            cur = s[1:-1]
            secs[cur] = {}
            continue
        if cur is None or "=" not in s:
            continue
        k, v = s.split("=", 1)
        secs[cur][k.strip()] = v.strip()
    return secs


def _profile_rows(profile_id):
    """Read the initial-condition rows for one profile letter."""
    letter = chr(ord("a") + profile_id)
    rows = []
    text = (INIT_DIR / f"profile_{letter}.dat").read_text(encoding="utf-8")
    for raw in text.splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.split()
        rows.append([float(parts[0]), float(parts[1]), float(parts[2])])
    return rows


def _spec(name):
    """Build a scenario spec dict from the cases table."""
    sec = _parse_cases()[name]
    leaves = []
    for grp in sec["leaves"].split("|"):
        leaves.append([int(x) for x in grp.split(",")])
    return {
        "name": name,
        "profile": int(sec["profile"]),
        "n_coarse": int(sec["n_coarse"]),
        "do_flux": int(sec["do_flux"]),
        "do_collapse": int(sec["do_collapse"]),
        "do_restart": int(sec["do_restart"]),
        "leaves": leaves,
    }


def simulate(name):
    """Independent reference for one scenario's conserved end state."""
    sp = _spec(name)
    rows = _profile_rows(sp["profile"])
    nc = sp["n_coarse"]
    coarse = [{"vol": 1.0, "q": list(rows[c])} for c in range(nc)]
    base = [0.0] * NVAR
    for c in range(nc):
        for v in range(NVAR):
            base[v] += coarse[c]["vol"] * coarse[c]["q"][v]

    leaves = []
    groups = []
    for c in range(nc):
        w = sp["leaves"][c] if c < len(sp["leaves"]) else [1]
        k = len(w)
        sumw = sum(w) or 1
        vj = [coarse[c]["vol"] * w[j] / sumw for j in range(k)]
        vtot = sum(vj)
        jbar = (sum(vj[j] * j for j in range(k)) / vtot) if vtot > 0 else 0.0
        start = len(leaves)
        for j in range(k):
            f = (1.0 + LEAF_SPREAD * (j - jbar)) if k > 1 else 1.0
            leaves.append({
                "vol": vj[j],
                "q": [coarse[c]["q"][v] * f for v in range(NVAR)],
            })
        groups.append((start, k))

    adjacency = sum(k for (_, k) in groups if k > 1)

    expected_seam = 0
    if sp["do_flux"]:
        for c in range(nc):
            start, k = groups[c]
            if k < 2:
                continue
            expected_seam += k
            vtot = sum(leaves[start + j]["vol"] for j in range(k))
            qbar = [
                sum(leaves[start + j]["vol"] * leaves[start + j]["q"][v] for j in range(k)) / vtot
                for v in range(NVAR)
            ]
            for j in range(k):
                lf = leaves[start + j]
                for v in range(NVAR):
                    lf["q"][v] += REFLUX_RATE * (qbar[v] - lf["q"][v])

    halo = [0.0] * NVAR
    for c in range(nc):
        start, k = groups[c]
        if k > 1:
            halo = list(leaves[start]["q"])
            break

    if sp["do_collapse"]:
        final = []
        for c in range(nc):
            start, k = groups[c]
            if k < 2:
                final.append(dict(leaves[start]))
            else:
                vtot = sum(leaves[start + j]["vol"] for j in range(k))
                q = [
                    sum(leaves[start + j]["vol"] * leaves[start + j]["q"][v] for j in range(k)) / vtot
                    for v in range(NVAR)
                ]
                final.append({"vol": vtot, "q": q})
    else:
        final = leaves

    after = [0.0] * NVAR
    moment = [0.0] * NVAR
    for i, cell in enumerate(final):
        for v in range(NVAR):
            m = cell["vol"] * cell["q"][v]
            after[v] += m
            moment[v] += (i + 1) * m

    drift = 0.0
    for v in range(NVAR):
        denom = abs(base[v]) or 1e-12
        drift = max(drift, abs(after[v] - base[v]) / denom)

    return {
        "base_total": base,
        "after_total": after,
        "resumed_total": moment,
        "drift_ratio": drift,
        "adjacency": adjacency,
        "halo_q": halo,
        "expected_seam": expected_seam,
    }


def _close(a, b):
    return abs(a - b) <= 1e-9 * max(abs(a), abs(b)) + 1e-12


def _vec_close(a, b):
    return len(a) == len(b) and all(_close(x, y) for x, y in zip(a, b))


def _run_matrix():
    if BUILD.exists():
        shutil.rmtree(BUILD)
    subprocess.run(["cmake", "-S", str(APP), "-B", str(BUILD)], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    subprocess.run(["cmake", "--build", str(BUILD), "-j2"], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    subprocess.run(["bash", str(APP / "scripts" / "run-matrix.sh")], check=True)
    return json.loads(AUDIT.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def report():
    return _run_matrix()


def _row(report, name):
    rows = [c for c in report["cases"] if c["name"] == name]
    assert len(rows) == 1, f"expected exactly one row for {name}"
    return rows[0]


def test_a0_storm_seam_balance(report):
    """storm closes its seam accounting and conserves its running sums."""
    row = _row(report, "storm")
    ref = simulate("storm")
    assert row["balanced"] is True
    assert _vec_close(row["after_total"], ref["base_total"])


def test_b1_canyon_seam_balance(report):
    """canyon closes its seam accounting across a multi-tier layout."""
    row = _row(report, "canyon")
    ref = simulate("canyon")
    assert row["balanced"] is True
    assert _vec_close(row["after_total"], ref["base_total"])


def test_c2_plume_adjacency(report):
    """plume resolves every parent/child link after growth."""
    row = _row(report, "plume")
    ref = simulate("plume")
    assert ref["adjacency"] == 4
    assert row["adjacency"] == ref["adjacency"]


def test_d3_spire_adjacency(report):
    """spire resolves the expected link count under a collapse layout."""
    row = _row(report, "spire")
    ref = simulate("spire")
    assert ref["adjacency"] == 2
    assert row["adjacency"] == ref["adjacency"]


def test_e4_spire_collapse_conserves(report):
    """spire's collapse returns the volume-weighted reference integral."""
    row = _row(report, "spire")
    ref = simulate("spire")
    assert row["base_match"] is True
    assert _vec_close(row["after_total"], ref["base_total"])


def test_f5_plume_round_trip_conserves(report):
    """plume's growth-then-collapse round trip returns to baseline."""
    row = _row(report, "plume")
    ref = simulate("plume")
    assert row["base_match"] is True
    assert _vec_close(row["after_total"], ref["base_total"])


def test_g6_basin_resumed_moment(report):
    """basin's resumed moment matches the uninterrupted reference."""
    row = _row(report, "basin")
    ref = simulate("basin")
    assert _vec_close(row["resumed_total"], ref["resumed_total"])


def test_h7_dune_resumed_moment(report):
    """dune's resumed moment matches the uninterrupted reference."""
    row = _row(report, "dune")
    ref = simulate("dune")
    assert _vec_close(row["resumed_total"], ref["resumed_total"])


def test_i8_tampered_snapshot_rejected(report):
    """a tampered snapshot is rejected with a mismatched-signature line."""
    assert AUDIT_LOG.exists()
    text = AUDIT_LOG.read_text(encoding="utf-8")
    rejected = [ln for ln in text.splitlines()
                if "REJECTED" in ln and "SIGNATURE_MISMATCH" in ln]
    assert len(rejected) >= 1


def test_j9_basin_resumed_adjacency(report):
    """basin rebuilds its parent/child links after resuming from a snapshot."""
    row = _row(report, "basin")
    ref = simulate("basin")
    assert ref["adjacency"] == 3
    assert row["adjacency"] == ref["adjacency"]


def test_k0_canyon_halo_band(report):
    """canyon's ghost band at the first seam matches the reference sample."""
    row = _row(report, "canyon")
    ref = simulate("canyon")
    assert _vec_close(row["halo_q"], ref["halo_q"])


def test_l1_dune_halo_band(report):
    """dune's ghost band at the first seam matches the reference sample."""
    row = _row(report, "dune")
    ref = simulate("dune")
    assert _vec_close(row["halo_q"], ref["halo_q"])


def test_no_canary_in_sources():
    """The fix-path source tree does not embed the reserved diagnostic marker."""
    for d in FIX_DIRS:
        root = APP / d
        for path in root.rglob("*"):
            if path.is_file():
                assert CANARY not in path.read_text(encoding="utf-8", errors="replace")
