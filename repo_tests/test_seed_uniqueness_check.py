"""Smoke tests for the Step-1 seed uniqueness gate (`scripts/seed_uniqueness_check.py`).

The script is referenced as a required Step-1 check by `AGENTS.md`,
`workflow-prompts.md`, and `prompts/Step1.md`/`step2a.md`. These tests pin the
pure `check_seed()` contract so the gate keeps rejecting blocked categories,
topology/name collisions, and malformed seeds.
"""

from __future__ import annotations

import unittest

from scripts import seed_uniqueness_check as suc
from scripts import tb3_categories


def _known(*, topology=(), task_name=()) -> dict[str, set[str]]:
    return {
        "path": set(),
        "topology": set(topology),
        "category": set(),
        "task_name": set(task_name),
    }


class SeedUniquenessCheckTest(unittest.TestCase):
    def test_unique_seed_with_allowed_category_passes(self) -> None:
        failures = suc.check_seed(
            seed_id="fenced-lease-recovery",
            topology="distributed lease fencing recovery",
            category="security",
            task_name="fenced-lease-recovery",
            known=_known(),
        )
        self.assertEqual(failures, [])

    def test_blocked_category_is_rejected(self) -> None:
        failures = suc.check_seed(
            seed_id="some-seed",
            topology="three word topology",
            category="debugging",
            task_name="some-seed",
            known=_known(),
        )
        self.assertTrue(any("BLOCKED" in f for f in failures), failures)

    def test_topology_collision_is_rejected(self) -> None:
        failures = suc.check_seed(
            seed_id="brand-new-seed",
            topology="Shared Cache Eviction Race",
            category="systems",
            task_name="brand-new-seed",
            known=_known(topology={"shared cache eviction race"}),
        )
        self.assertTrue(any("topology collision" in f for f in failures), failures)

    def test_name_collision_is_rejected(self) -> None:
        failures = suc.check_seed(
            seed_id="existing-task",
            topology="distinct enough topology phrase",
            category="systems",
            task_name="existing-task",
            known=_known(task_name={"existing-task"}),
        )
        self.assertTrue(any("name collision" in f for f in failures), failures)

    def test_too_short_topology_is_rejected(self) -> None:
        failures = suc.check_seed(
            seed_id="seed-x",
            topology="cache",
            category="systems",
            task_name="seed-x",
            known=_known(),
        )
        self.assertTrue(any("topology must be" in f for f in failures), failures)

    def test_blocked_categories_constant(self) -> None:
        self.assertIn("debugging", tb3_categories.BLOCKED_CATEGORIES)
        self.assertIn("software-engineering", tb3_categories.BLOCKED_CATEGORIES)


if __name__ == "__main__":
    unittest.main()
