import json
import os
import shutil
import subprocess
import tempfile
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


# ---------------------------------------------------------------------------
# Pipeline-integrity checks.
#
# The matrix tests above grade only the on-disk source/restored trees and the
# audit JSON, recomputing every value from the filesystem. That alone cannot
# tell a real restore apart from one that copies the source verbatim and emits
# a plausible report, so these checks pin the audit to the actual subsystems
# that must produce it: the native measurement binary, the row-fold and
# hardlink-keying packages, and the wiring that drives them.
# ---------------------------------------------------------------------------


def test_fsmeasure_reports_true_sizes(matrix_data):
    """The native measurement binary must report real on-disk byte sizes."""
    binary = APP / "bin" / "fsmeasure"
    assert binary.exists()
    fixture = Path(tempfile.mkdtemp(prefix="fsm-"))
    try:
        plan = [
            (["a", "one.txt"], b"abc"),          # 3 bytes (odd)
            (["c", "three.txt"], b"hello!"),     # 6 bytes (even)
            (["d", "roll.txt"], b"0123456789"),  # 10 bytes (even)
        ]
        for segments, content in plan:
            target = fixture.joinpath(*segments)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        # A hardlinked pair sharing one inode exercises the per-path byte
        # contract (each linked name is measured at its real size).
        shared = fixture.joinpath("deep", "x", "shared.dat")
        shared.parent.mkdir(parents=True, exist_ok=True)
        shared.write_bytes(b"payload\n")
        alias = fixture.joinpath("b", "shared.dat")
        alias.parent.mkdir(parents=True, exist_ok=True)
        os.link(shared, alias)

        expected = {}
        for item in fixture.rglob("*"):
            if item.is_file():
                expected[item.relative_to(fixture).as_posix()] = item.stat().st_size

        proc = subprocess.run(
            [str(binary), str(fixture)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
        )
        assert proc.returncode == 0, proc.stderr
        reported = {}
        for line in proc.stdout.splitlines():
            if not line.strip():
                continue
            rel, size = line.rsplit("\t", 1)
            reported[rel] = int(size)
        assert reported == expected, f"fsmeasure reported {reported}, expected {expected}"
    finally:
        shutil.rmtree(fixture, ignore_errors=True)


GO_VERIFY_TESTS = {
    "a0": r'''package a0_test

import (
	"os"
	"path/filepath"
	"syscall"
	"testing"

	"staged.local/snapshot/internal/a0"
	"staged.local/snapshot/internal/f5"
)

func buildRestored(t *testing.T, name string) string {
	t.Helper()
	p := f5.ProfileFor(name)
	src := t.TempDir()
	dst := t.TempDir()
	if err := a0.CreateTree(src, p); err != nil {
		t.Fatalf("CreateTree: %v", err)
	}
	rows, err := a0.RowsFromTree(src, p)
	if err != nil {
		t.Fatalf("RowsFromTree: %v", err)
	}
	if err := a0.Materialize(rows, dst, p); err != nil {
		t.Fatalf("Materialize: %v", err)
	}
	return dst
}

func TestMaterializeReplaysFinalContent(t *testing.T) {
	dst := buildRestored(t, "gamma")
	flow, err := os.ReadFile(filepath.Join(dst, "a", "flow.txt"))
	if err != nil {
		t.Fatalf("read flow.txt: %v", err)
	}
	if string(flow) != "second\n" {
		t.Fatalf("flow.txt = %q, want second-newline", string(flow))
	}
	one, err := os.ReadFile(filepath.Join(dst, "a", "one.txt"))
	if err != nil {
		t.Fatalf("read one.txt: %v", err)
	}
	if string(one) != "gamma:one\n" {
		t.Fatalf("one.txt = %q, want gamma:one-newline", string(one))
	}
}

func TestMaterializePreservesHardlinks(t *testing.T) {
	dst := buildRestored(t, "beta")
	rels := []string{"deep/x/shared.dat", "a/shared-a.dat", "b/shared-b.dat", "c/shared-c.dat"}
	var base uint64
	for i, rel := range rels {
		info, err := os.Stat(filepath.Join(dst, filepath.FromSlash(rel)))
		if err != nil {
			t.Fatalf("stat %s: %v", rel, err)
		}
		ino := uint64(info.Sys().(*syscall.Stat_t).Ino)
		if i == 0 {
			base = ino
		} else if ino != base {
			t.Fatalf("%s is not hardlinked with shared.dat", rel)
		}
	}
}
''',
    "b1": r'''package b1_test

import (
	"testing"

	"staged.local/snapshot/internal/b1"
	"staged.local/snapshot/internal/f5"
)

func TestFoldRowsKeepsAscendingOrder(t *testing.T) {
	p := f5.ProfileFor("gamma")
	rows := []f5.Row{
		{Seq: 0, Op: "write", Path: "a/flow.txt", Data: "first\n"},
		{Seq: 1, Op: "remove", Path: "a/flow.txt"},
		{Seq: 2, Op: "write", Path: "a/flow.txt", Data: "second\n"},
	}
	out, err := b1.FoldRows(rows, p)
	if err != nil {
		t.Fatalf("FoldRows: %v", err)
	}
	if len(out) == 0 {
		t.Fatalf("FoldRows returned no rows")
	}
	for i := 1; i < len(out); i++ {
		if out[i].Seq < out[i-1].Seq {
			t.Fatalf("rows are not ascending by Seq: %+v", out)
		}
	}
	last := out[len(out)-1]
	if last.Op != "write" || last.Data != "second\n" {
		t.Fatalf("final row must be the latest write, got %+v", last)
	}
}
''',
    "c2": r'''package c2_test

import (
	"os"
	"path/filepath"
	"testing"

	"staged.local/snapshot/internal/c2"
	"staged.local/snapshot/internal/f5"
)

func writeFixture(t *testing.T, path, content string) {
	t.Helper()
	if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(path, []byte(content), 0o644); err != nil {
		t.Fatal(err)
	}
}

func TestItemsCPeriodsAndBytes(t *testing.T) {
	p := f5.ProfileFor("epsilon")
	root := t.TempDir()
	writeFixture(t, filepath.Join(root, "d", "roll.txt"), "0123456789")
	writeFixture(t, filepath.Join(root, "c", "three.txt"), "abcd")
	writeFixture(t, filepath.Join(root, "a", "one.txt"), "xyz")
	items, err := c2.ItemsC(root, p)
	if err != nil {
		t.Fatalf("ItemsC: %v", err)
	}
	byPath := map[string]f5.AccountItem{}
	for _, it := range items {
		byPath[it.Path] = it
	}
	roll, ok := byPath["d/roll.txt"]
	if !ok {
		t.Fatalf("missing d/roll.txt in %+v", items)
	}
	if roll.Period != "p1" {
		t.Fatalf("d/roll.txt period = %q, want p1", roll.Period)
	}
	if roll.Bytes != 10 {
		t.Fatalf("d/roll.txt bytes = %d, want 10", roll.Bytes)
	}
	if byPath["c/three.txt"].Bytes != 4 {
		t.Fatalf("c/three.txt bytes = %d, want 4", byPath["c/three.txt"].Bytes)
	}
	if byPath["a/one.txt"].Bytes != 3 {
		t.Fatalf("a/one.txt bytes = %d, want 3", byPath["a/one.txt"].Bytes)
	}
}
''',
    "d3": r'''package d3_test

import (
	"testing"

	"staged.local/snapshot/internal/d3"
	"staged.local/snapshot/internal/f5"
)

func TestKeyForGroupsSharedInode(t *testing.T) {
	p := f5.ProfileFor("beta")
	r1 := f5.Row{Op: "write", Path: "deep/x/shared.dat", Dev: 7, Ino: 42}
	r2 := f5.Row{Op: "write", Path: "a/shared-a.dat", Dev: 7, Ino: 42}
	r3 := f5.Row{Op: "write", Path: "c/three.txt", Dev: 7, Ino: 99}
	if d3.KeyFor(r1, p) != d3.KeyFor(r2, p) {
		t.Fatalf("rows sharing dev:ino must share a key: %q vs %q", d3.KeyFor(r1, p), d3.KeyFor(r2, p))
	}
	if d3.KeyFor(r1, p) == d3.KeyFor(r3, p) {
		t.Fatalf("rows with a distinct inode must not share a key")
	}
}
''',
}


def test_internal_pipeline_units(matrix_data):
    """The restore audit must be produced by the real internal packages.

    Verifier-only Go tests are injected into each package directory and run
    with ``go test``. They call the exported functions directly, so a solution
    that bypasses the pipeline (for example rewriting cmd/ctl to copy the
    source tree verbatim and hand-emit the audit) fails here even though the
    matrix JSON would look correct.
    """
    written = []
    gocache = tempfile.mkdtemp(prefix="goc-")
    try:
        for pkg, src in GO_VERIFY_TESTS.items():
            dest = APP / "internal" / pkg / "zz_test.go"
            dest.write_text(src, encoding="utf-8")
            written.append(dest)
        env = dict(os.environ)
        env.update(
            {
                "GOTOOLCHAIN": "local",
                "GOPROXY": "off",
                "GOFLAGS": "-mod=mod",
                "GOCACHE": gocache,
                "CGO_ENABLED": "0",
            }
        )
        proc = subprocess.run(
            [
                "go",
                "test",
                "./internal/a0/",
                "./internal/b1/",
                "./internal/c2/",
                "./internal/d3/",
            ],
            cwd=str(APP),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=240,
            env=env,
        )
        assert proc.returncode == 0, proc.stdout
    finally:
        for dest in written:
            try:
                dest.unlink()
            except FileNotFoundError:
                pass
        shutil.rmtree(gocache, ignore_errors=True)


def test_pipeline_wiring_intact():
    """The audit must still be driven through the documented subsystems."""
    main_go = (APP / "cmd" / "ctl" / "main.go").read_text(encoding="utf-8")
    for call in (
        "a0.CreateTree",
        "a0.RowsFromTree",
        "a0.Materialize",
        "c2.ItemsC",
        "e4.Digest",
        "e4.Groups",
    ):
        assert call in main_go, f"cmd/ctl/main.go must still call {call}"
    core_go = (APP / "internal" / "a0" / "core.go").read_text(encoding="utf-8")
    assert "b1.FoldRows" in core_go, "Materialize must fold rows via b1.FoldRows"
    assert "d3.KeyFor" in core_go, "Materialize must key hardlinks via d3.KeyFor"
    roll_go = (APP / "internal" / "c2" / "roll.go").read_text(encoding="utf-8")
    assert "e4.NativeBytes" in roll_go, "ItemsC must measure bytes via e4.NativeBytes"
