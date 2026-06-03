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

The `.cursor/` files remain canonical across agents (Cursor, Claude Code, OpenCode) so tooling
does not drift — but they are canonical *relative to each other*, beneath the platform reviews.

## Non-negotiables

- Never claim PASS, READY, APPROVED, or SUBMIT without command output.
- Do not invent paths, commands, `task.toml` fields, verifier paths, or package exclusions. Open the relevant file first.
- After any edit inside `tasks/<task-name>/`, Step 2b evidence is stale. Re-run the cheap gates before relying on it.
- Cheap Step 2b order: `./scripts/check-task.sh tasks/<task-name>` → oracle 1x → NOP. Do not run oracle 10x for Step 2b.
- Final approval requires oracle 10x, NOP score 0.0, submission zip validation, and `approve_task.py` exit 0.
- New multi-container and UI-building tasks are blocked.
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
