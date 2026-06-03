import json
import os
import subprocess
from pathlib import Path

import pytest

APP = Path(os.environ.get("APP_ROOT", "/app"))
AUDIT = APP / "output" / "alloc-audit.json"
BIN = APP / "bin" / "allocctl"
CASES = ["cedar", "jade", "slate", "coral", "onyx", "pearl"]

HDR = 16
FTR = 8
MIN_BLK = 40
ALIGN = 8
HEAP = 65536


def align(n: int) -> int:
    return (n + ALIGN - 1) & ~(ALIGN - 1)


def load_plan(name: str) -> list[tuple]:
    path = APP / "data" / "cases" / f"{name}.plan"
    ops = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if parts[0] == "ALLOC":
            ops.append(("alloc", int(parts[1])))
        elif parts[0] == "FREE":
            ops.append(("free", int(parts[1])))
        elif parts[0] == "REALLOC":
            ops.append(("realloc", int(parts[1]), int(parts[2])))
    return ops


class ModelArena:
    def __init__(self) -> None:
        self.used = HEAP
        self.size_at: dict[int, int] = {0: HEAP}
        self.alloc_at: dict[int, bool] = {0: False}
        self.fl_head: int | None = 0
        self.fl_next: dict[int, int | None] = {0: None}
        self.fl_prev: dict[int, int | None] = {0: None}
        self.slots: list[int] = []
        self.payload: list[int] = []
        self.live: list[bool] = []
        self.allocated = 0
        self.peak = 0

    def _blk_size(self, off: int) -> int:
        return self.size_at[off]

    def _set_blk(self, off: int, size: int, is_alloc: bool) -> None:
        self.size_at[off] = size
        self.alloc_at[off] = is_alloc

    def _phys_prev(self, off: int) -> int | None:
        if off == 0:
            return None
        cur = 0
        while cur < off:
            nxt = cur + self._blk_size(cur)
            if nxt == off:
                return cur
            cur = nxt
        return None

    def _fl_remove(self, off: int) -> None:
        nxt = self.fl_next.get(off)
        prv = self.fl_prev.get(off)
        if nxt is not None:
            self.fl_prev[nxt] = prv
        elif self.fl_head == off:
            self.fl_head = prv
        if prv is not None:
            self.fl_next[prv] = nxt
        else:
            self.fl_head = nxt
        self.fl_next[off] = None
        self.fl_prev[off] = None

    def _fl_insert(self, off: int) -> None:
        self.fl_next[off] = self.fl_head
        self.fl_prev[off] = None
        if self.fl_head is not None:
            self.fl_prev[self.fl_head] = off
        self.fl_head = off

    def _coalesce(self, off: int) -> int:
        total = self._blk_size(off)
        prv = self._phys_prev(off)
        if prv is not None and not self.alloc_at.get(prv, True):
            self._fl_remove(prv)
            total += self._blk_size(prv)
            off = prv
        nxt = off + total
        if nxt < self.used and not self.alloc_at.get(nxt, True):
            self._fl_remove(nxt)
            total += self._blk_size(nxt)
        self._set_blk(off, total, False)
        self._fl_insert(off)
        return off

    def _find_fit(self, need: int) -> int | None:
        off = 0
        while off < self.used:
            sz = self._blk_size(off)
            if sz == 0:
                break
            if not self.alloc_at.get(off, False) and sz >= need:
                return off
            off += sz
        return None

    def _note(self, delta: int) -> None:
        self.allocated += delta
        if self.allocated > self.peak:
            self.peak = self.allocated

    def _split(self, off: int, req: int) -> None:
        need = align(req + HDR + FTR)
        total = self._blk_size(off)
        rem = total - need
        self._fl_remove(off)
        self._set_blk(off, need, True)
        tail = off + need
        self._set_blk(tail, rem, False)
        self._fl_insert(tail)
        self._note(need)

    def heap_sig(self) -> int:
        sig = 0
        off = 0
        while off < self.used:
            sz = self._blk_size(off)
            if sz == 0:
                break
            if self.alloc_at.get(off, False):
                sig += sz * 17
            off += sz
        return sig

    def fl_sig(self) -> int:
        sig = 0
        off = 0
        while off < self.used:
            sz = self._blk_size(off)
            if sz == 0:
                break
            if not self.alloc_at.get(off, False):
                sig += sz
            off += sz
        return sig

    def fl_count(self) -> int:
        c = 0
        off = 0
        while off < self.used:
            sz = self._blk_size(off)
            if sz == 0:
                break
            if not self.alloc_at.get(off, False):
                c += 1
            off += sz
        return c

    def run_ops(self, ops: list[tuple]) -> list[dict]:
        steps = []
        seq = 0
        for op in ops:
            rec = {"seq": seq, "op": op[0], "index": -1, "size": 0, "result_index": -1}
            seq += 1
            if op[0] == "alloc":
                rec["size"] = op[1]
                need = align(op[1] + HDR + FTR)
                fit = self._find_fit(need)
                if fit is None:
                    rec["result_index"] = -1
                else:
                    total = self._blk_size(fit)
                    if total >= need + MIN_BLK:
                        self._split(fit, op[1])
                    else:
                        self._fl_remove(fit)
                        self._set_blk(fit, total, True)
                        self._note(total)
                    idx = len(self.slots)
                    self.slots.append(fit)
                    self.payload.append(op[1])
                    self.live.append(True)
                    rec["result_index"] = idx
            elif op[0] == "free":
                rec["index"] = op[1]
                idx = op[1]
                if idx < 0 or idx >= len(self.live) or not self.live[idx]:
                    rec["result_index"] = -1
                else:
                    off = self.slots[idx]
                    total = self._blk_size(off)
                    self._set_blk(off, total, False)
                    self._fl_remove(off)
                    self._note(-total)
                    self.live[idx] = False
                    self._coalesce(off)
                    rec["result_index"] = 0
            elif op[0] == "realloc":
                rec["index"] = op[1]
                rec["size"] = op[2]
                idx = op[1]
                if idx < 0 or idx >= len(self.live) or not self.live[idx]:
                    rec["result_index"] = -1
                else:
                    off = self.slots[idx]
                    need = align(op[2] + HDR + FTR)
                    old_total = self._blk_size(off)
                    if need <= old_total:
                        if old_total >= need + MIN_BLK:
                            self._fl_remove(off)
                            self._set_blk(off, old_total, False)
                            self._note(-old_total)
                            self._split(off, op[2])
                        self.payload[idx] = op[2]
                        rec["result_index"] = idx
                    else:
                        nxt = off + old_total
                        merged = False
                        if nxt < self.used and not self.alloc_at.get(nxt, True):
                            ntotal = self._blk_size(nxt)
                            if old_total + ntotal >= need:
                                self._fl_remove(nxt)
                                merged_size = old_total + ntotal
                                self._set_blk(off, merged_size, True)
                                self._note(ntotal)
                                if merged_size >= need + MIN_BLK:
                                    self._fl_remove(off)
                                    self._set_blk(off, merged_size, False)
                                    self._note(-merged_size)
                                    self._split(off, op[2])
                                self.payload[idx] = op[2]
                                rec["result_index"] = idx
                                merged = True
                        if not merged:
                            new_fit = self._find_fit(need)
                            if new_fit is None:
                                rec["result_index"] = -1
                            else:
                                total = self._blk_size(new_fit)
                                if total >= need + MIN_BLK:
                                    self._split(new_fit, op[2])
                                else:
                                    self._fl_remove(new_fit)
                                    self._set_blk(new_fit, total, True)
                                    self._note(total)
                                nidx = len(self.slots)
                                self.slots.append(new_fit)
                                self.payload.append(op[2])
                                self.live.append(True)
                                old_off = self.slots[idx]
                                ototal = self._blk_size(old_off)
                                self._set_blk(old_off, ototal, False)
                                self._fl_remove(old_off)
                                self._note(-ototal)
                                self.live[idx] = False
                                self._coalesce(old_off)
                                rec["result_index"] = nidx
            rec["heap_sig"] = self.heap_sig()
            rec["fl_count"] = self.fl_count()
            rec["fl_sig"] = self.fl_sig()
            rec["byte_total"] = self.allocated
            steps.append(rec)
        return steps

    def expected_case(self, name: str) -> dict:
        steps = self.run_ops(load_plan(name))
        last = steps[-1] if steps else {}
        return {
            "name": name,
            "ok": True,
            "steps": steps,
            "heap_sig": last.get("heap_sig", 0),
            "fl_count": last.get("fl_count", 0),
            "fl_sig": last.get("fl_sig", 0),
            "byte_total": last.get("byte_total", 0),
        }


def build_binary() -> None:
    proc = subprocess.run(
        ["make", "-C", str(APP)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=240,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert BIN.exists()


def run_matrix(fresh: bool = False) -> dict:
    if AUDIT.exists():
        AUDIT.unlink()
    build_binary()
    proc = subprocess.run(
        ["bash", str(APP / "scripts" / "run-matrix.sh")],
        cwd=APP,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def case_by_name(data: dict, name: str) -> dict:
    matches = [c for c in data["cases"] if c.get("name") == name]
    assert matches, f"missing case {name}"
    return matches[0]


@pytest.fixture(scope="session")
def matrix_data() -> dict:
    """Run the matrix once and return parsed audit JSON."""
    return run_matrix()


def test_a0(matrix_data: dict) -> None:
    """Matrix includes all six scenarios with clean status and nonempty steps."""
    names = [c["name"] for c in matrix_data["cases"]]
    assert names == CASES
    for name in CASES:
        case = case_by_name(matrix_data, name)
        exp = ModelArena().expected_case(name)
        assert case["ok"] is True
        assert case["steps"]
        assert case["heap_sig"] == exp["heap_sig"]
        assert case["fl_count"] == exp["fl_count"]
        assert case["fl_sig"] == exp["fl_sig"]
        assert case["byte_total"] == exp["byte_total"]


def test_b1(matrix_data: dict) -> None:
    """Direct one-case helper matches the matrix slice for cedar."""
    build_binary()
    proc = subprocess.run(
        ["bash", str(APP / "scripts" / "run-one.sh"), "cedar"],
        cwd=APP,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    direct = json.loads((APP / "output" / "cedar-audit.json").read_text(encoding="utf-8"))
    matrix_case = case_by_name(matrix_data, "cedar")
    direct_case = direct["cases"][0]
    assert direct_case["heap_sig"] == matrix_case["heap_sig"]
    assert direct_case["byte_total"] == matrix_case["byte_total"]


def test_c2(matrix_data: dict) -> None:
    """Cedar step records and accounting match the plan model."""
    case = case_by_name(matrix_data, "cedar")
    exp = ModelArena().expected_case("cedar")
    for got, want in zip(case["steps"], exp["steps"], strict=True):
        assert got["heap_sig"] == want["heap_sig"]
        assert got["byte_total"] == want["byte_total"]


def test_d3(matrix_data: dict) -> None:
    """Jade split-heavy scenario matches expected heap signature progression."""
    case = case_by_name(matrix_data, "jade")
    exp = ModelArena().expected_case("jade")
    assert case["heap_sig"] == exp["heap_sig"]
    assert case["steps"][-1]["fl_count"] == exp["steps"][-1]["fl_count"]


def test_e4(matrix_data: dict) -> None:
    """Slate coalesce reduces free-list node count versus broken forward-only merge."""
    case = case_by_name(matrix_data, "slate")
    exp = ModelArena().expected_case("slate")
    assert case["fl_count"] == exp["fl_count"]
    assert case["fl_sig"] == exp["fl_sig"]


def test_f5(matrix_data: dict) -> None:
    """Coral in-place realloc keeps slot index and final heap signature."""
    case = case_by_name(matrix_data, "coral")
    exp = ModelArena().expected_case("coral")
    assert case["heap_sig"] == exp["heap_sig"]
    assert case["steps"][-1]["result_index"] == exp["steps"][-1]["result_index"]


def test_g6(matrix_data: dict) -> None:
    """Onyx growth realloc produces relocated payload integrity in signatures."""
    case = case_by_name(matrix_data, "onyx")
    exp = ModelArena().expected_case("onyx")
    assert case["heap_sig"] == exp["heap_sig"]
    assert case["byte_total"] == exp["byte_total"]


def test_h7(matrix_data: dict) -> None:
    """Pearl mixed scenario end-state matches model tallies."""
    case = case_by_name(matrix_data, "pearl")
    exp = ModelArena().expected_case("pearl")
    assert case["heap_sig"] == exp["heap_sig"]
    assert case["fl_count"] == exp["fl_count"]


def test_i8(matrix_data: dict) -> None:
    """Ledger JSONL rows mirror steps array for slate."""
    case = case_by_name(matrix_data, "slate")
    ledger = Path(case["ledger"])
    lines = ledger.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == len(case["steps"])
    for line, step in zip(lines, case["steps"], strict=True):
        row = json.loads(line)
        assert row["seq"] == step["seq"]
        assert row["heap_sig"] == step["heap_sig"]


def test_j9() -> None:
    """Two matrix runs from unchanged inputs yield identical audits."""
    first = run_matrix(fresh=True)
    second = run_matrix(fresh=True)
    assert first == second


def test_k0(matrix_data: dict) -> None:
    """Every case byte_total matches the reference model."""
    for name in CASES:
        case = case_by_name(matrix_data, name)
        exp = ModelArena().expected_case(name)
        assert case["byte_total"] == exp["byte_total"]


def test_l1(matrix_data: dict) -> None:
    """Slate free-list signature after middle frees matches bidirectional coalesce."""
    case = case_by_name(matrix_data, "slate")
    exp = ModelArena().expected_case("slate")
    assert case["fl_sig"] == exp["fl_sig"]
