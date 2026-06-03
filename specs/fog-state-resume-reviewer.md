# fog-state-resume — reviewer appendix

## Residual risks

- First `games` category task: confirm legality rules are documented in instruction and derivable from `/app/config` without metaphor jargon.
- GX9: instruction must not list per-case move coordinates or sig integers.

## Ablation expectations

- Revert `phase_a` only: rook/gamma fail on seen-tile persistence across restore.
- Revert `fold_b` only: bishop/gamma fail on stale observation merge.
- Revert `mark_c` only: sentinel/warden fail on modifier epoch boundaries.
- Revert `bind_d` only: knight/warden fail on hostile steps through walls or from hidden tiles.
- Revert `walk_e` only: lancer/warden fail when native wall check disagrees with Go planner.

## Empirical hard target

≤1/6 frontier pass with deterministic oracle 10/10.
