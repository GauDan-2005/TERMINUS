#!/usr/bin/env python3
"""Check and register Step-1 seed uniqueness against prior specs and tasks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:  # works both as a CLI script (scripts/ on sys.path) and as scripts.seed_uniqueness_check
    from tb3_categories import BLOCKED_CATEGORIES
except ModuleNotFoundError:  # pragma: no cover - package-style import
    from scripts.tb3_categories import BLOCKED_CATEGORIES

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "prompts" / "seed-registry.jsonl"

TOPOLOGY_RE = re.compile(r"^\s*-\s*\*\*Topology\*\*:\s*`?([^`\n]+)`?", re.MULTILINE)
CATEGORY_RE = re.compile(
    r"(?:^|\n)\s*-\s*Category:\s*([a-z0-9-]+)|"
    r'category\s*=\s*"([a-z0-9-]+)"|'
    r"### Category:\s*`?([a-z0-9-]+)`?",
    re.MULTILINE | re.IGNORECASE,
)
TASK_NAME_RE = re.compile(
    r"(?:^|\n)\s*-\s*Task name:\s*([a-z0-9-]+)|"
    r"tasks/([a-z0-9-]+)/",
    re.MULTILINE | re.IGNORECASE,
)


def _normalize_token(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def _collect_from_text(path: Path, text: str) -> dict[str, set[str]]:
    rel = str(path.relative_to(REPO_ROOT))
    topologies: set[str] = set()
    categories: set[str] = set()
    task_names: set[str] = set()

    for match in TOPOLOGY_RE.finditer(text):
        topologies.add(_normalize_token(match.group(1)))

    for match in CATEGORY_RE.finditer(text):
        cat = next(g for g in match.groups() if g)
        categories.add(cat.lower())

    for match in TASK_NAME_RE.finditer(text):
        name = next(g for g in match.groups() if g)
        task_names.add(name.lower())

    stem = path.stem.lower()
    if stem.endswith("-validation-log"):
        stem = stem[: -len("-validation-log")]
    if not stem.endswith("-validation-log") and "-" in stem:
        task_names.add(stem)

    return {
        "path": {rel},
        "topology": topologies,
        "category": categories,
        "task_name": task_names,
    }


def scan_repo() -> dict[str, set[str]]:
    aggregate: dict[str, set[str]] = {
        "path": set(),
        "topology": set(),
        "category": set(),
        "task_name": set(),
    }
    for pattern in ("specs/*.md", "tasks/*/task.toml", "tasks/*/instruction.md"):
        for path in REPO_ROOT.glob(pattern):
            if path.name.endswith("-validation-log.md"):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            found = _collect_from_text(path, text)
            for key in aggregate:
                aggregate[key].update(found[key])
    if REGISTRY_PATH.exists():
        for line in REGISTRY_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("topology"):
                aggregate["topology"].add(_normalize_token(entry["topology"]))
            if entry.get("task_name"):
                aggregate["task_name"].add(entry["task_name"].lower())
            if entry.get("seed_id"):
                aggregate["task_name"].add(entry["seed_id"].lower())
    return aggregate


def check_seed(
    *,
    seed_id: str,
    topology: str,
    category: str,
    task_name: str | None,
    known: dict[str, set[str]],
) -> list[str]:
    failures: list[str] = []
    norm_topology = _normalize_token(topology)
    norm_seed = seed_id.strip().lower()
    norm_task = (task_name or "").strip().lower()
    cat = category.strip().lower()

    if cat in BLOCKED_CATEGORIES:
        failures.append(
            f"category '{cat}' is BLOCKED for new tasks; remap before Step 2a "
            f"(see @idea-validation.mdc Blocked Task Categories)."
        )

    if norm_topology in known["topology"]:
        failures.append(
            f"topology collision: '{topology}' already used in repo/registry "
            f"(choose a distinct 3–6 word topology token)."
        )

    for token in (norm_seed, norm_task):
        if token and token in known["task_name"]:
            failures.append(
                f"seed/task name collision: '{token}' already exists; pick a new slug/seed_id."
            )

    if not norm_topology or len(norm_topology.split()) < 2:
        failures.append("topology must be a distinct 3–6 word phrase.")

    if not norm_seed:
        failures.append("seed_id is required (unique kebab-case identifier for this seed).")

    return failures


def register_seed(args: argparse.Namespace) -> int:
    known = scan_repo()
    failures = check_seed(
        seed_id=args.seed_id,
        topology=args.topology,
        category=args.category,
        task_name=args.task_name,
        known=known,
    )
    if failures:
        for msg in failures:
            print(f"FAIL: {msg}", file=sys.stderr)
        return 1

    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "seed_id": args.seed_id,
        "topology": args.topology,
        "category": args.category,
        "task_name": args.task_name,
        "task_shape": args.task_shape,
        "registered_at": datetime.now(timezone.utc).isoformat(),
        "notes": args.notes or "",
    }
    with REGISTRY_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, sort_keys=True) + "\n")
    print(f"Registered seed '{args.seed_id}' -> {REGISTRY_PATH}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="Check a seed without registering")
    check.add_argument("--seed-id", required=True)
    check.add_argument("--topology", required=True)
    check.add_argument("--category", required=True)
    check.add_argument("--task-name")
    check.add_argument("--json", action="store_true")

    reg = sub.add_parser("register", help="Register a seed after uniqueness check")
    reg.add_argument("--seed-id", required=True)
    reg.add_argument("--topology", required=True)
    reg.add_argument("--category", required=True)
    reg.add_argument("--task-name")
    reg.add_argument("--task-shape")
    reg.add_argument("--notes")

    audit = sub.add_parser("audit", help="List known topologies and blocked-category specs")
    audit.add_argument("--json", action="store_true")

    args = parser.parse_args()

    if args.command == "audit":
        known = scan_repo()
        blocked_specs = []
        for path in REPO_ROOT.glob("specs/*.md"):
            text = path.read_text(encoding="utf-8", errors="replace")
            cats = _collect_from_text(path, text)["category"]
            if cats & BLOCKED_CATEGORIES:
                blocked_specs.append(str(path.relative_to(REPO_ROOT)))
        payload = {
            "topology_count": len(known["topology"]),
            "task_name_count": len(known["task_name"]),
            "blocked_category_specs": sorted(blocked_specs),
        }
        if args.json:
            print(json.dumps(payload, indent=2))
        else:
            print(f"Known topologies: {payload['topology_count']}")
            print(f"Known task/seed names: {payload['task_name_count']}")
            if blocked_specs:
                print("Specs with BLOCKED category (fix before Step 2b):")
                for item in blocked_specs:
                    print(f"  - {item}")
        return 0

    known = scan_repo()
    failures = check_seed(
        seed_id=args.seed_id,
        topology=args.topology,
        category=args.category,
        task_name=getattr(args, "task_name", None),
        known=known,
    )

    if args.command == "register":
        if failures:
            for msg in failures:
                print(f"FAIL: {msg}", file=sys.stderr)
            return 1
        return register_seed(args)

    if args.json:
        print(json.dumps({"ok": not failures, "failures": failures}, indent=2))
    elif failures:
        for msg in failures:
            print(f"FAIL: {msg}", file=sys.stderr)
    else:
        print(f"OK: seed '{args.seed_id}' is unique and category '{args.category}' is allowed.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
