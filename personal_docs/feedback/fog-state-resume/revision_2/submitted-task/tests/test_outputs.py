import json
import os
import subprocess
from pathlib import Path

import pytest


APP = Path(os.environ.get("APP_ROOT", "/app"))
AUDIT = APP / "output" / "resume-audit.json"
CASE_NAMES = ["rook", "bishop", "knight", "lancer", "sentinel", "warden", "ranger"]


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
    assert (APP / "bin" / "rogctl").exists()
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert "cases" in data and data["cases"]
    assert {case.get("name") for case in data["cases"]} == set(CASE_NAMES)
    return data


def case_by_name(data: dict, name: str) -> dict:
    matches = [case for case in data["cases"] if case.get("name") == name]
    assert matches
    return matches[0]


def load_layout(name: str):
    walls = []
    player = (0, 0)
    hostiles = []
    path = APP / "data" / "layouts" / f"{name}.map"
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    height = len(lines)
    width = max(len(line) for line in lines)
    for y, line in enumerate(lines):
        for x in range(width):
            ch = line[x] if x < len(line) else "."
            if ch == "#":
                walls.append((x, y))
            elif ch == "@":
                player = (x, y)
            elif ch.isdigit():
                hostiles.append((ch, x, y))
    return width, height, set(walls), player, hostiles


def final_player_pos(name: str):
    width, height, walls, player, _ = load_layout(name)
    px, py = player
    script = APP / "data" / "scripts" / f"{name}.tsv"
    for line in script.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("turn"):
            continue
        parts = line.split("\t")
        if len(parts) >= 4 and parts[1] == "P":
            dx, dy = (int(x) for x in parts[3].split(","))
            nx, ny = px + dx, py + dy
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in walls:
                px, py = nx, ny
        if len(parts) >= 3 and parts[2] == "save":
            break
    return px, py


def load_radius(name: str) -> int:
    path = APP / "config" / "sight.tsv"
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("case"):
            continue
        parts = line.split("\t")
        if parts[0] == name:
            return int(parts[1])
    return 3


def lit_tiles(width, height, walls, player, radius):
    px, py = player
    seen = set()
    queue = [(px, py, 0)]
    while queue:
        x, y, d = queue.pop(0)
        if (x, y) in seen or (x, y) in walls:
            continue
        seen.add((x, y))
        if d >= radius:
            continue
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            queue.append((x + dx, y + dy, d + 1))
    return seen


def step_legal(walls, x0, y0, x1, y1) -> bool:
    if (x1, y1) in walls:
        return False
    return abs(x0 - x1) + abs(y0 - y1) == 1


def assert_case_clean(case: dict) -> None:
    assert set(case) >= {
        "name",
        "ok",
        "fresh",
        "resume",
        "moves",
        "visibility",
        "effects",
        "records",
        "log",
    }
    assert case["ok"] is True
    assert case["fresh"]["illegal"] == 0
    assert case["resume"]["illegal"] == 0
    assert case["fresh"]["sig"] == case["resume"]["sig"]
    width, height, walls, _, _hostiles = load_layout(case["name"])
    player = final_player_pos(case["name"])
    radius = load_radius(case["name"])
    visible = lit_tiles(width, height, walls, player, radius)
    for move in case["moves"]:
        assert move["legal"] is True
        if move["kind"] == "step":
            assert step_legal(walls, move["from_x"], move["from_y"], move["to_x"], move["to_y"])
            assert (move["to_x"], move["to_y"]) in visible


def test_audit_file_written(matrix_data):
    """Matrix command produces the all-case audit file."""
    assert AUDIT.exists()
    assert matrix_data["cases"]


@pytest.mark.parametrize("case_name", CASE_NAMES)
def test_case_row_clean(matrix_data, case_name):
    """Each matrix row reports clean dual-path results."""
    assert_case_clean(case_by_name(matrix_data, case_name))


def test_single_case_parity(matrix_data):
    """Single-case output matches the matrix row for the same name."""
    for name in ("rook", "sentinel"):
        out = APP / "output" / f"single-{name}.json"
        if out.exists():
            out.unlink()
        proc = subprocess.run(
            ["bash", str(APP / "scripts" / "one-case.sh"), name],
            cwd=APP,
            text=True,
            capture_output=True,
            timeout=60,
        )
        assert proc.returncode == 0, proc.stderr
        single = json.loads(out.read_text(encoding="utf-8"))
        matrix_row = case_by_name(matrix_data, name)
        assert single["cases"][0]["name"] == matrix_row["name"]
        assert single["cases"][0]["fresh"] == matrix_row["fresh"]
        assert single["cases"][0]["resume"] == matrix_row["resume"]


def test_path_sig_match_01(matrix_data):
    """First case fresh and restored summaries share the same signature."""
    case = case_by_name(matrix_data, "rook")
    assert case["fresh"]["sig"] == case["resume"]["sig"]


def test_step_geometry_03(matrix_data):
    """Third case hostile steps stay on adjacent non-wall tiles."""
    case = case_by_name(matrix_data, "knight")
    _, _, walls, _, _ = load_layout("knight")
    for move in case["moves"]:
        if move["actor"].isdigit():
            assert step_legal(walls, move["from_x"], move["from_y"], move["to_x"], move["to_y"])


def test_target_visibility_02(matrix_data):
    """Second case hostile targets lie in the lit tile set at script end."""
    case = case_by_name(matrix_data, "bishop")
    width, height, walls, _, _ = load_layout("bishop")
    player = final_player_pos("bishop")
    visible = lit_tiles(width, height, walls, player, load_radius("bishop"))
    for move in case["moves"]:
        if move["actor"].isdigit():
            assert (move["to_x"], move["to_y"]) in visible


def test_modifier_active_05(matrix_data):
    """Fifth case timed modifier rows stay active after restore."""
    case = case_by_name(matrix_data, "sentinel")
    ward = [row for row in case["effects"] if row["id"] == "ward"]
    assert ward
    assert ward[0]["active"] is True


def test_jsonl_order_04(matrix_data):
    """Fourth case records sidecar mirrors move array order."""
    case = case_by_name(matrix_data, "lancer")
    lines = [
        json.loads(line)
        for line in Path(case["records"]).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert len(lines) == len(case["moves"])
    for left, right in zip(lines, case["moves"]):
        assert left["turn"] == right["turn"]
        assert left["actor"] == right["actor"]


def test_trace_align_06(matrix_data):
    """Sixth case log sidecar aligns with move rows."""
    case = case_by_name(matrix_data, "warden")
    rows = Path(case["log"]).read_text(encoding="utf-8").splitlines()
    assert len(rows) == len(case["moves"])
    for row, move in zip(rows, case["moves"]):
        parts = row.split("\t")
        assert int(parts[1]) == move["turn"]
        assert parts[2] == move["actor"]
        assert parts[-1] == str(move["legal"])


def test_driver_binary_present(matrix_data):
    """Matrix driver leaves the rogctl binary in place."""
    assert (APP / "bin" / "rogctl").exists()
    assert matrix_data["cases"]
