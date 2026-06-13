# Audit output layout

`/app/output/conservation_audit.json` holds a single object with a `cases`
array. The per-case helpers emit the same object shape with one entry.

Each entry has these fields:

- `name` — scenario identifier.
- `base_total` — three running sums of the starting state, one per tracked
  quantity.
- `after_total` — the same three sums measured once the structural phases of
  the run have completed.
- `resumed_total` — a position-weighted moment of the final state (each cell's
  contribution scaled by its ordinal position). Two runs of the same scenario
  that reach the same end arrangement report the same moment.
- `drift_ratio` — the largest relative gap between `after_total` and
  `base_total` across the three quantities.
- `balanced` — true when the seam accounting over every coarse-fine interface
  closed out.
- `base_match` — true when `after_total` matches `base_total` within the
  numerical floor.
- `adjacency` — count of parent/child links resolved at the structural peak of
  the run; it must match the independent recomputation for the scenario, so a
  row that reports no resolved links has not held up.
- `halo_q` — three sampled ghost-band values taken at the first refined seam.

`/app/output/persistence_audit.log` records one line per snapshot load attempt
during the runs that round-trip through `/app/work/vault.bin`. A line begins
with `ACCEPTED` or `REJECTED`; rejected lines name the reason. A snapshot is
accepted only when its stored signature matches the active configuration; one
whose signature disagrees must be rejected rather than applied, and its
`REJECTED` line must name `SIGNATURE_MISMATCH` as the reason. Resuming a run
therefore depends on the saved checkpoint being consistent with the scenario it
belongs to.
