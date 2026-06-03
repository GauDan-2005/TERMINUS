---
description: Draft or repair TB3 Step 2b task files from an approved Step 2a spec.
argument-hint: <task-name>
---

You are running TB3 Step 2b task construction for `tasks/$ARGUMENTS`.

Read first, in this order:

1. `AGENTS.md`
2. `.cursor/rules/00-authoring-critical.mdc`
3. `.cursor/skills/tb3-task-author/SKILL.md`
4. `.cursor/rules/task-creation.mdc`
5. `.cursor/rules/difficulty-calibration.mdc`
6. `commands.md`
7. `specs/$ARGUMENTS.md` Authoring Brief only

Rules:

- Stop if the Step 2a spec is missing, malformed, or lacks Triviality Ledger, Per-gate Pitfall Inventory, or Initial Draft Commitments.
- Create exactly the files committed by the spec. Do not add uncommitted files without returning to Step 2a.
- Use the canonical milestone layout when `number_of_milestones > 0`.
- Do not create new multi-container or UI-building tasks.
- Do not put AI-scaffolding names anywhere under `tasks/$ARGUMENTS/`.
- After edits, run the cheap gates in order: `./scripts/check-task.sh tasks/$ARGUMENTS`, oracle 1x, NOP.
- Do not claim Step 2b PASS without the relevant command output.
