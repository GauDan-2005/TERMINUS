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
python3 scripts/task_integrity.py verify tasks/$ARGUMENTS
```

Then run only the gates documented in `.cursor/skills/tb3-packager/SKILL.md` and `commands.md`, in order:

1. Oracle 10x — `python3 scripts/harbor_gate.py tasks/$ARGUMENTS --oracle-repeat 10` (all 10 trials at 1.0).
2. Verifier 20x — `python3 scripts/harbor_gate.py tasks/$ARGUMENTS --test-repeat 20` (all 20 trials at 1.0).
3. Reviewer simulation — `python3 scripts/reviewer_simulation.py tasks/$ARGUMENTS --strict ...`; block if `would_reject` is true or `reviewer_confidence < 90`.
4. Build the shipping zip using the full exclusion list from `commands.md`.
5. `python3 scripts/validate_submission_zip.py Task_Ready_To_Submit/$ARGUMENTS.zip`.
6. `python3 scripts/approve_task.py --strict ...` with only documented flags.
7. Mirror approved fixtures to `repo_tests/fixtures/` as documented.

Stop on first failure. Do not claim READY, APPROVED, or SUBMIT without command output.
