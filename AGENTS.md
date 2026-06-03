# AGENTS.md

TB3 Edition 2 authoring harness. Unit: `tasks/<task-name>/`. New here? Read `docs/ARCHITECTURE.md`.

## Lookups

- Before task edits, pull `.cursor/rules/00-authoring-critical.mdc`.
- Authoring: `task-creation.mdc`; validation: `idea-validation.mdc`; review: `review-and-submit.mdc`; hardness: `difficulty-calibration.mdc`.
- Commands/workflow/conventions: `commands.md`, `workflow-prompts.md`, `REPO_CONVENTIONS.md`.

## Tool adapters

- Cursor canonical files remain under `.cursor/rules/` and `.cursor/skills/`.
- Claude Code uses `CLAUDE.md`, `.claude/commands/`, `.claude/agents/`, and `.claude/skills/` as thin adapters back to the canonical files.
- OpenCode uses `.opencode/opencode.json`, `.opencode/agent/`, and `.opencode/skills/` as thin adapters back to the canonical files.
- Keep adapter files at the repo root only; never copy them under `tasks/<task-name>/` or into submission zips.

## Must fire

1. Never claim PASS / READY / APPROVED / SUBMIT without command output.
2. Cheap gates: `run_static_checks.py` → `collapse_check.py` → oracle 1x → NOP. No oracle 10x in Step 2b.
3. Do not invent paths, `task.toml` fields, or commands; open the file or `commands.md`.
4. After any task-file edit, Step 2b evidence is stale; rerun cheap gates. `approve_task.py` rejects checksum mismatch.
5. Preflight: `./scripts/check-task.sh tasks/<task-name>`. Still run oracle 1x + NOP for Step 2b PASS.
6. Milestones: use `task.toml` v2 `[[steps]]` plus `steps/milestone_N/{instruction.md,tests/,solution/}`. No root `instruction.md` / `tests/` / `solution/` / `milestones.md`.
7. No new multi-container or UI-building tasks; in-progress ones may finish.

## Submission bans

Never ship `output_contract.toml`, `quality_check_adjudication.json`, `construction_manifest.json`, `rubric*.txt`, `.step2b-checksum`, or AI-scaffolding names (`CLAUDE.md`, `AGENTS.md`, `skills.md`, `.cursor/`, `.aider/`, `.continue/`, `.claude/`) at any depth.
