---
name: tb3-idea-validator
description: Use when validating a TB3 task idea before file creation, producing Step 2a specs/evidence with validate_loop.py and the idea-validation/difficulty rules.
---

# tb3-idea-validator

This is an OpenCode adapter for TB3 Step 2a idea validation.

Read first:

- `AGENTS.md`
- `.cursor/rules/00-authoring-critical.mdc`
- `.cursor/rules/idea-validation.mdc`
- `.cursor/rules/difficulty-calibration.mdc`
- `workflow-prompts.md`
- `commands.md`

Do not create `tasks/<task-name>/` in Step 2a. Reject medium/easy ideas and new multi-container/UI-building tasks. Use `validate_loop.py` exactly as documented. Do not claim a GO spec without command output.
