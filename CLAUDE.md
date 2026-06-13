# CLAUDE.md

Claude Code adapter for this TB3 Edition 2 authoring harness.

## Source of truth

Platform Snorkel reviews are authoritative. The archived reviewer feedback under
`personal_docs/feedback/` records what the platform actually accepts and rejects; when a repo
rule, doc, or gate (`run_static_checks.py`, `collapse_check.py`, `approve_task.py`) contradicts
a review, **the review wins and the rule/gate is updated to match** — not the other way around.
`personal_docs/feedback/` is read-only evidence; never edit it to fit a rule.

Below the reviews, the shared repository contract is:

1. `AGENTS.md` — mandatory repo-level instructions.
2. `.cursor/rules/00-authoring-critical.mdc` — critical TB3 policy. Read before task edits, gates, submission prep, or `approve_task.py`.
3. Workflow-specific rule files:
   - Step 2a idea validation: `.cursor/rules/idea-validation.mdc`
   - Step 2b task construction: `.cursor/rules/task-creation.mdc`
   - Step 3b paper review / Step 4 packaging: `.cursor/rules/review-and-submit.mdc`
   - Difficulty and collapse calibration: `.cursor/rules/difficulty-calibration.mdc`
4. Exact commands and conventions: `commands.md`, `workflow-prompts.md`, `REPO_CONVENTIONS.md`.
5. Canonical image-quality + review references: `docs/DOCKER_REQUIREMENTS.md`, `docs/REVIEW_CHECKLIST.md`.

The `.cursor/` files remain canonical across agents (Cursor, Claude Code, OpenCode) so tooling
does not drift — but they are canonical *relative to each other*, beneath the platform reviews.

## Non-negotiables

- Never claim PASS, READY, APPROVED, or SUBMIT without command output.
- Do not invent paths, commands, `task.toml` fields, verifier paths, or package exclusions. Open the relevant file first.
- After any edit inside `tasks/<task-name>/`, Step 2b evidence is stale. Re-run the cheap gates before relying on it.
- Cheap Step 2b order: `./scripts/check-task.sh --strict --report-dir /tmp/tb3-gates tasks/<task-name>` + the `scripts/task_gate.py` gates (incl. `hard_difficulty_predictor` — Python ≤20% worst-model blocker — `spec_test_alignment`, `spec_gap_detector`, `sandbox_risk_gate`) → `harbor_gate.py --oracle --oracle-stress 3 --nop --nop-stress 3` (oracle 3/3 = 1.0, NOP 3/3 = 0.0). Do not run oracle 10x for Step 2b.
- Final approval (Step 4) requires oracle 10x (`harbor_gate.py --oracle-repeat 10`), verifier 20x (`--test-repeat 20`), `reviewer_simulation.py --strict` (reviewer_confidence ≥ 90), submission zip validation, and `approve_task.py --strict` exit 0.
- New multi-container and UI-building tasks are blocked. Tasks must be substantively different from your prior submissions — templated / re-skin tasks are rejected.
- Canonical base image: build from the canonical per-language base (list pending; sanctioned families in `docs/DOCKER_REQUIREMENTS.md`); a pinned-but-non-canonical base needs a justification recorded in `construction_manifest.json` `base_image`. Record the website `inspiration_id` in the spec `reference_pattern` when the task uses a site inspiration.
- Milestone tasks use `task.toml` v2 `[[steps]]` plus `steps/milestone_N/{instruction.md,tests/,solution/}`. Do not use deprecated root milestone layouts.
- Do not put AI-scaffolding files (`CLAUDE.md`, `AGENTS.md`, `.cursor/`, `.claude/`, `.opencode/`, `skills.md`, etc.) inside `tasks/<task-name>/` or submission zips.

## Claude Code affordances

Slash commands are available under `.claude/commands/`:

- `/tb3-validate` — Step 2a idea validation/spec workflow.
- `/tb3-author` — Step 2b construction workflow.
- `/tb3-review` — Step 3b paper review workflow.
- `/tb3-package` — Step 4 final approval/packaging workflow.

Subagents are available under `.claude/agents/`:

- `tb3-idea-validator`
- `tb3-task-author`
- `tb3-reviewer`
- `tb3-packager`

Skills are mirrored under `.claude/skills/` and point back to the canonical Cursor skills/rules.

## Working style

- Use a todo list for multi-step task authoring, review, or packaging work.
- Prefer reading the canonical files over relying on memory.
- Use exact command lines from `commands.md` or the relevant rule file.
- Keep local agent optimization files at the repo root only; task archives must remain clean.
