# Reviewer appendix — sparse-block-preconditioner

Internal notes only. Not shipped in the task zip.

## Oracle patch summary

1. **bsr_n/layout.cpp (`fn_n`)**: Use symmetric block indexing when filling BSR row/column block maps after reorder — the broken baseline indexes rows with `perm[i]` but columns with raw `j`.
2. **perm_p/order.cpp (`map_p`)**: Apply the same block map to the RHS vector when reorder is active — broken baseline leaves RHS in natural order.
3. **prec_r/apply.cpp (`step_r`)**: Apply block diagonal inverse in the permuted layout space — broken baseline gathers diagonals from natural block order.
4. **scale_q/metric.cpp (`norm_q`)**: Return true Euclidean L2 norm — broken baseline scales by `sqrt(n)` after max-norm hack.

## Partial-oracle ablation expectations

- Fix only `fn_n`: basalt/flint may pass residual if scale fixed? No scale still broken. Reorder layout tests may improve but perm/prec still fail.
- Fix only `map_p`: reorder cases improve residual mismatch; layout/prec/scale may still fail.
- Fix only `step_r`: iteration cap tests on reorder cases flip; others may remain.
- Fix only `norm_q`: all cases gain `residual_agrees`; reorder convergence may still fail.

## Reviewer checklist highlights

- Confirm instruction does not name CSR/BSR/permutation/preconditioner as causes.
- Confirm tests re-derive from `.case` files without env golden JSON.
- Confirm Dockerfile has tmux + asciinema + digest-pinned FROM.
- Confirm `construction_manifest.json` mirrors spec manifest verbatim.
