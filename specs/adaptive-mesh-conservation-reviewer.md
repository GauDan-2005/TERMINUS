# Reviewer appendix — adaptive-mesh-conservation

Internal notes only. Not shipped in the task zip.

## Oracle patch summary

1. **acc_m/edge_corr.cpp (`op_m`)**: At adjacent-collection seams where the two sides sit at different tiers of refinement, the coarse area must be sub-divided across the fine sub-faces and one pulse recorded per sub-face. Broken baseline records a single pulse using the coarse area, double-counting mass across the seam.
2. **lnk_n/relate.cpp (`step_n`)**: After a structural change (growth or collapse), parent-of and child-of arrays must be rebuilt by walking the current cell array. Broken baseline only rebuilds parent-of, leaving child-of pointing at stale indices.
3. **agg_q/blend.cpp (`fold_q`)**: When collapsing children into a parent, the payload must be the volume-weighted mean (sum of child q*vol divided by sum of child vol). Broken baseline uses arithmetic mean, leaking mass when child volumes are unequal.
4. **srl_p/serial.cpp (`emit_p`)**: The vault payload must include the pending-pulse block (the FluxBank slice that has been accumulated but not applied). Broken baseline writes only the cell array, losing in-flight corrections on restart.
5. **rsm_k/resume.cpp (`load_k`)**: After reading a vault, the topo link's parent/child indices must be rebuilt by calling `step_n`. Broken baseline writes zero indices into the topo link and runs forward with broken adjacency.
6. **sync_b/halo.cpp (`op_b`)**: Ghost-cell payloads at refinement seams must be copied from the adjacent collection with the correct stride (one ghost per fine sub-face on the coarse side, one ghost per coarse face on the fine side). Broken baseline copies the wrong side's payload, leaving ghost cells stale.

## Flipping-point mapping (each function controls exactly two tests)

- `op_m` (acc_m) -> test_a0, test_b1 (seam-balance flag on storm, canyon).
- `step_n` (lnk_n) -> test_c2, test_d3 (adjacency count on plume, spire).
- `fold_q` (agg_q) -> test_e4, test_f5 (collapse conservation on spire, plume).
- `emit_p` (srl_p) -> test_g6, test_h7 (resumed moment on basin, dune).
- `load_k` (rsm_k) -> test_i8 (tampered-vault rejection), test_j9 (post-resume adjacency relink on basin).
- `op_b` (sync_b) -> test_k0, test_l1 (ghost column on canyon, dune).

`run_u` plus the `drv_u/run_refine.cpp`, `drv_u/run_blend.cpp`, `drv_u/run_sync.cpp` helpers are correct scaffold (not on the fix path). They distribute the calls to the six fix-path symbols so no single visible file references more than two of them (CR8): `run_refine` calls `op_m`+`step_n`, `run_blend` calls `fold_q`+`op_b`, `run_sync` calls `emit_p`+`load_k`, and `run.cpp` only calls the three phase helpers.

## Partial-oracle ablation expectations

- Fix only `op_m`: seam-balance flags flip true on storm/canyon; all other tests still fail.
- Fix only `step_n`: adjacency counts flip true on plume/spire; conservation, replay, halo still fail.
- Fix only `fold_q`: collapse-conservation tests pass on spire/plume; seam, replay, halo still fail.
- Fix only `emit_p`: resumed moments still wrong unless `load_k` also reads the pulse block; pairing matters.
- Fix only `load_k`: tampered-vault rejection passes and post-resume adjacency rebuilds, but resumed moments need `emit_p` too.
- Fix only `op_b`: ghost columns match; everything else still fails.
- Fix all six: all twelve tests pass.

## Reviewer checklist highlights

- Confirm instruction does not name sub-face area splitting, parent-child reindex direction, volume-weighting recipe, vault payload composition, post-resume relink, or halo copy order as causes.
- Confirm tests re-derive expected totals from TSV + cases.toml (not from env golden JSON).
- Confirm Dockerfile has tmux + asciinema + digest-pinned FROM + .dockerignore + OCI labels + SOURCE_DATE_EPOCH.
- Confirm `construction_manifest.json` mirrors spec manifest verbatim.
- Confirm `drv_u/` split into four files keeps ≤2 fix-path symbol references per file (CR8).
- Confirm canary token `tb_amr_noembed_8d7a4c2f` lives only in tests and the stale `vault_layout.h` comment.
- Confirm scenario-seeded initial conditions are generated at Docker build time (deterministic from `seed = hash(scenario_name + global_seed)`); not at test time and not shipped as goldens.
