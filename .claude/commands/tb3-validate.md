---
description: Validate a TB3 task idea and produce the Step 2a spec/evidence package.
argument-hint: <task-name-or-idea>
---

You are running TB3 Step 2a idea validation for: `$ARGUMENTS`.

Read first, in this order:

1. `AGENTS.md`
2. `.cursor/rules/00-authoring-critical.mdc`
3. `.cursor/rules/idea-validation.mdc`
4. `.cursor/rules/difficulty-calibration.mdc`
5. `workflow-prompts.md`
6. `commands.md`

Rules:

- Do not create or edit `tasks/<task-name>/` during Step 2a.
- Reject ideas that are medium, easy, new multi-container, or new UI-building tasks.
- Validate the 5 hardness axes, anti-trivialization checks, rubric axes, discovery budget, instruction specificity, naming pass, and topology distribution.
- Use `validate_loop.py` exactly as documented. Do not invent flags or output paths.
- A GO spec must satisfy the v2 spec contract in `.cursor/rules/idea-validation.mdc`.
- Keep reviewer-only analysis out of `specs/<task-name>.md`; put it in the reviewer appendix path required by the validation workflow.

Before saying the idea is accepted, show the command output that proves the validation loop accepted it.
