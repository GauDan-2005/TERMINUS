---
description: Run TB3 Step 4 final approval and packaging gates for a reviewed task.
argument-hint: <task-name>
---

You are running TB3 Step 4 final approval for `tasks/$ARGUMENTS`.

Read first, in this order:

1. `AGENTS.md`
2. `.cursor/rules/00-authoring-critical.mdc`
3. `.cursor/skills/tb3-packager/SKILL.md`
4. `.cursor/rules/review-and-submit.mdc`
5. `commands.md`

Required pre-check:

```bash
python3 task_integrity.py verify tasks/$ARGUMENTS
```

Then run only the gates documented in `.cursor/skills/tb3-packager/SKILL.md` and `commands.md`, in order:

1. Oracle 10x.
2. NOP; score must be 0.0.
3. Build the shipping zip using the full exclusion list from `commands.md`.
4. `python3 validate_submission_zip.py Task_Ready_To_Submit/$ARGUMENTS.zip`.
5. `python3 approve_task.py ...` with only documented flags.
6. Mirror approved fixtures to `repo_tests/fixtures/` as documented.

Stop on first failure. Do not claim READY, APPROVED, or SUBMIT without command output.
