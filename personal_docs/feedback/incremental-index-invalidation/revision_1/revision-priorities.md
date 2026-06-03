# incremental-index-invalidation — revision_1 priorities

## P0 — platform blockers

1. Fix `tests/test.sh` to capture the pytest status, write `reward.txt` from that result, and exit with the pytest status as requested by platform feedback.
2. After editing the task file, rerun Step 2b's dirty-flag chain: `./scripts/check-task.sh`, oracle 1x, and NOP.

## P1 — agent failure drivers

- Preserve the existing behavioral tests. The platform did not ask for additional semantic coverage.
- Failed agents mainly missed `r4/e.rs` epoch propagation; do not soften this unless a later review asks for a difficulty change.

## P2 — convention nits / adjudication candidates

- Agent review's wheel visibility warning is a consequence of offline verifier dependency placement and was marked READY TO USE.
- Be careful reconciling the platform's `exit "$PYTEST_RC"` request with repo-local canonical `test.sh` expectations; rerun local static checks after the edit.

## P3 — passed / no change needed

- Instruction sufficiency passed.
- Quality check passed 10/10.
- Agent review was READY TO USE.
- Oracle/NOP platform runs were healthy.
