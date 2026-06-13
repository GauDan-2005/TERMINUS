<!--
adaptive-mesh-conservation — rebalanced rubric for revision 2.
Enter these on the platform UI (rubric is NOT shipped in the task dir).
Positives total = +25 (within the required 10–40); negatives are separate.
Rebalance shifts weight from the reliably-found conservation bugs onto the
frontier bugs agents missed in revision 1 (adjacency 2–3/10, halo 0/10,
fingerprint 6/10). was→now noted per line.
-->

## Rubric (paste into platform UI)

Agent restores volume-weighted aggregation so that merging finer cells into a coarser cell preserves the integrated quantity, +4
Agent corrects the coarse-fine interface accounting so one correction is recorded per fine sub-face rather than a single coarse-area entry, +3
Agent persists the in-flight pending corrections inside the snapshot so a resumed run reaches the same state as an uninterrupted run, +3
Agent rebuilds both the parent and the child adjacency links after a structural change to the grid, +5
Agent corrects the ghost-band synchronization at the refinement seam so neighbouring values line up, +4
Agent rebuilds the adjacency links when resuming from a snapshot rather than continuing with stale links, +3
Agent rejects a snapshot whose stored signature disagrees with the active configuration, +2
Agent rebuilds the project with CMake and regenerates the report after editing the sources, +1
Agent edits the fixed TSV starting states or the scenario schedules to force the totals to agree, -5
Agent hardcodes per-scenario totals or report values in the sources instead of computing them from the simulation, -3
Agent disables or removes the snapshot signature check instead of restoring the saved state correctly, -3
Agent rewrites the report writer to emit balanced results without changing the underlying simulation behaviour, -2

## Rebalance vs revision 1 (positives 21 → 25)

| Criterion | was | now | why |
|---|---|---|---|
| Volume-weighted aggregation (`fold_q`) | +5 | +4 | core, but reliably found (10/10) |
| Coarse–fine interface per sub-face (`op_m`) | +3 | +3 | reliably found |
| Persist pending corrections in snapshot (FluxBank) | +3 | +3 | mid (7/10) |
| Rebuild parent/child adjacency after structural change | +3 | **+5** | missed (3/10); 3 tests ride on it |
| Ghost-band sync at refinement seam (`op_b` offset) | +2 | **+4** | **0/10** — single hardest bug |
| Rebuild adjacency when resuming from snapshot | +2 | **+3** | missed (2/10) |
| Reject snapshot with mismatched signature | +1 | **+2** | missed (6/10); now spec'd in layout.md |
| Rebuild with CMake + regenerate report | +2 | +1 | table-stakes / mechanical |
| **Positives total** | **21** | **25** | within 10–40 |

Negatives unchanged (do not count toward the 10–40 positives cap):
edit TSV/schedules −5, hardcode totals −3, disable signature check −3,
rewrite report writer without sim change −2.
