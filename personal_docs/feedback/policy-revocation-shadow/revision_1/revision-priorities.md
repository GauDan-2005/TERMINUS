# policy-revocation-shadow — revision_1 priorities

## P0 — platform blockers

1. Add verifier coverage for required decision metadata fields: `principal`, `resource`, and `action`.
2. Add at least one dynamic trace/generalization check so the suite proves the engine processes current inputs instead of accepting a canned `/app/output/policy-audit.json`.
3. Add a source-level or runtime guard against precomputed audit output if needed, while preserving oracle/NOP behavior.

## P1 — agent failure drivers

- Keep the hard diagnostic surface: common misses were cache invalidation after grant/revoke, group-slot keying by subject, and per-subject epoch/reuse logic.
- Do not leak exact module locations while strengthening tests.

## P2 — convention nits / adjudication candidates

- Agent review recommends moving pytest into `tests/test.sh` via networked install/uv. That conflicts with the repo's offline policy; use the offline verifier convention or adjudicate the warning.
- Consider documenting cargo PATH only if the live image still lacks it during agent sessions.

## P3 — passed / no change needed

- Difficulty is HARD and solvable.
- Instruction sufficiency and all quality axes passed.
- NOP fails and oracle passes in platform runs.
