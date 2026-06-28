from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import spec_test_alignment


class SpecTestAlignmentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp(prefix="spec-test-alignment-test-"))
        self.addCleanup(shutil.rmtree, self.tmpdir, ignore_errors=True)
        self.task_dir = self.tmpdir / "tasks" / "fixture"
        (self.task_dir / "tests").mkdir(parents=True)
        (self.task_dir / "environment" / "data").mkdir(parents=True)
        (self.task_dir / "instruction.md").write_text(
            "Produce the audit for the shipped cases from the data files.\n",
            encoding="utf-8",
        )
        (self.task_dir / "tests" / "test_outputs.py").write_text(
            "def test_scenario():\n"
            '    """Scenario nodes resolve correctly."""\n'
            "    trace = load()\n"
            '    assert "amber-leaf" in trace\n',
            encoding="utf-8",
        )

    def _literal_findings(self) -> list[dict]:
        report = spec_test_alignment.evaluate(self.task_dir, strict=True)
        return [f for f in report["findings"] if f["kind"] == "undocumented_literal"]

    def test_literal_homed_in_environment_is_not_flagged(self) -> None:
        # 'amber-leaf' lives in a solver-visible plan file -> discoverable.
        (self.task_dir / "environment" / "data" / "amber.plan").write_text(
            "ROOT amber-root\nLEAF amber-leaf parent=amber-root\n", encoding="utf-8"
        )
        self.assertEqual(self._literal_findings(), [])

    def test_literal_homed_nowhere_is_still_flagged(self) -> None:
        # No plan file defines 'amber-leaf' anywhere solver-visible -> genuine gap.
        (self.task_dir / "environment" / "data" / "amber.plan").write_text(
            "ROOT amber-root\n", encoding="utf-8"
        )
        findings = self._literal_findings()
        self.assertTrue(
            any("amber-leaf" in f["message"] for f in findings), findings
        )


if __name__ == "__main__":
    unittest.main()
