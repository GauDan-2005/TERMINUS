"""Shared Terminal-Bench category policy for validators and seed tooling."""

from __future__ import annotations

ALLOWED_CATEGORIES: frozenset[str] = frozenset(
    {
        "build-and-dependency-management",
        "data-processing",
        "games",
        "machine-learning",
        "scientific-computing",
        "security",
        "system-administration",
    }
)

BLOCKED_CATEGORIES: frozenset[str] = frozenset(
    {
        "software-engineering",
        "debugging",
    }
)

# Remap guidance when a seed naturally sounds like a blocked category.
CATEGORY_REMAP: dict[str, str] = {
    "software-engineering": (
        "Use build-and-dependency-management, data-processing, games, "
        "machine-learning, or system-administration based on the real substrate."
    ),
    "debugging": (
        "Use repair_existing_system task_shape under an accepted category "
        "(system-administration, security, scientific-computing, build-and-dependency-management, "
        "data-processing, games, or machine-learning). Do not use category=debugging."
    ),
}

# Wording that usually means the idea still belongs to a blocked category surface.
BLOCKED_CATEGORY_PROXIMITY_PHRASES: tuple[str, ...] = (
    "category: debugging",
    "category: software-engineering",
    "category = debugging",
    "category = software-engineering",
    "category=debugging",
    "category=software-engineering",
    "under debugging category",
    "debugging category",
    "software-engineering category",
    "generic debugging task",
    "debug this script",
    "find the bug in",
    "simple bug fix",
    "straightforward bug fix",
    "course-project crud",
    "fastapi crud",
)
