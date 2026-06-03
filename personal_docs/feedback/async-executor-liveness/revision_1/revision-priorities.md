# async-executor-liveness — revision_1 priorities

## P0 — platform blockers

1. Add the explicit root-parent sentinel sentence requested by the reviewer: root records must emit `parent` as the string `"-"` in JSON, ledger JSONL, and journal output.
2. Rerun the dirty-flag chain after the instruction edit: `./scripts/check-task.sh`, oracle 1x, and NOP.

## P1 — agent failure drivers

- Both failed agents independently selected `null`/`None`; keep the fix limited to this spec gap.
- Preserve the existing tests and oracle behavior, which platform says pass offline with 12/12 tests, reward 1, and CTRF present.

## P2 — convention nits / adjudication candidates

- Agent review warns about Dockerfile-baked pytest, but the human note explicitly says not to hold that against the task under no-internet verifier setup.
- Cargo PATH was previously a concern in failed-agent analysis, but the human note says Cargo is on PATH in the normal container shell.

## P3 — passed / no change needed

- Rubric panel is fully green per revision notes.
- Test names are descriptive.
- Prompt already clarifies child rows are scheduled by their own arrival turn.
- Oracle and mounted verifier pass offline.
