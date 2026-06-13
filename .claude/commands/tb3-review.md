---
description: Paper-review a constructed TB3 task after current Step 2b evidence exists.
argument-hint: <task-name>
---

You are running TB3 Step 3b paper review for `tasks/$ARGUMENTS`.

Read first, in this order:

1. `AGENTS.md`
2. `.cursor/rules/00-authoring-critical.mdc`
3. `.cursor/skills/tb3-reviewer/SKILL.md`
4. `.cursor/rules/review-and-submit.mdc`
5. `.cursor/rules/difficulty-calibration.mdc`
6. `.cursor/rules/task-creation.mdc`
7. `commands.md`

Required pre-check:

```bash
python3 scripts/task_integrity.py verify tasks/$ARGUMENTS
```

Rules:

- If integrity is dirty/missing/stale, stop and send the task back to Step 2b.
- Review the full surface listed in `.cursor/skills/tb3-reviewer/SKILL.md`; partial reads miss defects.
- Walk `review-and-submit.mdc` sections 1-7 and `difficulty-calibration.mdc` Part A/Part B.
- Any edit during review dirty-flags the task and returns it to Step 2b.
- Do not run approval gates from this command; this is paper review only.
