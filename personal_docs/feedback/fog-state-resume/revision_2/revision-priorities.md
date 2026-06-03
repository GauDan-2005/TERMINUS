# fog-state-resume — revision_2 priorities

## P0 — platform blockers

1. Add the missing public contract for ward modifier active-state preservation after restore. The current tests require `ward[0]["active"] is True`, but `instruction.md` only defines clean rows through `ok`, `illegal`, signatures, and sidecars.
2. Decide whether to make the audit `ok` field reflect active-state divergence, or keep `ok` narrow and document the separate active-state requirement clearly enough that agents do not stop at `ok=True`.
3. Remove caching files/folders named in reviewer notes before resubmission.

## P1 — agent failure drivers

- Failed agents converge at 15/16 tests and miss `test_modifier_active_05`; revise the task so this invariant is discoverable without giving away the exact `mod/effect.go` fix.
- Keep the task in the hard band: the latest difficulty check is HARD with GPT-5.2 at 1/5 and Opus at 5/5.

## P2 — convention nits / adjudication candidates

- The agent review repeats the Dockerfile-baked pytest warning. This conflicts with the repo's offline-runtime convention; use the repo's adjudication/waiver workflow rather than moving to a networked verifier install.
- The agent review suggests adding subsystem symptoms. Avoid fix-location leakage; prefer one behavioral sentence about active modifier state surviving restore.

## P3 — passed / no change needed

- Oracle and NOP behaved correctly in platform runs.
- Automated quality check reported 10/10 pass.
- All tests except the active-state one passed in all 10 frontier runs.
