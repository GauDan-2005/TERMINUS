from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import spec_gap_detector


class SpecGapDetectorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp(prefix="spec-gap-detector-test-"))
        self.addCleanup(shutil.rmtree, self.tmpdir, ignore_errors=True)
        self.task_dir = self.tmpdir / "tasks" / "fixture"
        (self.task_dir / "tests").mkdir(parents=True)

    def _write(self, instruction: str, test_body: str) -> None:
        (self.task_dir / "instruction.md").write_text(instruction, encoding="utf-8")
        (self.task_dir / "tests" / "test_outputs.py").write_text(test_body, encoding="utf-8")

    def test_python_method_call_is_not_a_spec_gap(self) -> None:
        # `tasks.count(...)` / `.split()` are stdlib method calls, not agent-facing
        # data fields — the gate must not demand the instruction explain them.
        self._write(
            "Produce the audit so each task appears the right number of times.\n",
            "def test_dedup():\n"
            '    """Rows are deduplicated."""\n'
            "    tasks = [row for row in load()]\n"
            '    assert tasks.count("flint-a") == 1\n'
            '    assert "x y".split() == ["x", "y"]\n',
        )
        report = spec_gap_detector.evaluate(self.task_dir, strict=True)
        self.assertEqual(report["status"], "PASS", report["findings"])

    def test_undocumented_data_field_is_still_a_spec_gap(self) -> None:
        # A genuine undocumented output field must still be flagged.
        self._write(
            "Produce the audit.\n",
            "def test_field():\n"
            '    """Checks a field."""\n'
            "    case = load()\n"
            '    assert case["reconciliation_token"] == 7\n',
        )
        report = spec_gap_detector.evaluate(self.task_dir, strict=True)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn(
            "reconciliation_token",
            {finding["test_token"] for finding in report["findings"]},
        )


if __name__ == "__main__":
    unittest.main()
