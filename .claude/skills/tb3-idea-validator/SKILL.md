---
name: tb3-idea-validator
description: Use when validating a TB3 task idea before file creation, producing Step 2a specs/evidence with validate_loop.py and the idea-validation/difficulty rules.
---

# tb3-idea-validator

This is a Claude Code adapter. Canonical rules live in:

- `AGENTS.md`
- `.cursor/rules/00-authoring-critical.mdc`
- `.cursor/rules/idea-validation.mdc`
- `.cursor/rules/difficulty-calibration.mdc`
- `workflow-prompts.md`
- `commands.md`

Read those files before making judgments. Do not create `tasks/<task-name>/` in Step 2a. Use `validate_loop.py` exactly as documented and show command output before claiming a GO spec.
