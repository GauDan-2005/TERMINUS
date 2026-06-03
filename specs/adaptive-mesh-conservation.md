### Decision

GO — Attempt 1. The adaptive-mesh conservation idea is shaped into a single-container hard scientific-computing task gated on coarse-fine edge correction, parent-child relink after structural change, volume-weighted aggregation when collapsing cells, vault-format payload composition with pending pulses, post-resume relink of cross-collection indices, and ghost-cell halo synchronization at refinement seams. The planned fix surface is distributed across six opaque module roots so no one location satisfies the verifier. The public contract stays behavioral: the simulator audit must report balanced totals and match the uninterrupted baseline across six bundled scenarios, but the instruction must not name coarse-fine sub-face area splitting, parent-child reindexing, volume-weighting in the aggregation, vault payload composition, or halo synchronization as causes.

### Metadata

- version: 2
- Task name: adaptive-mesh-conservation
- Title: Adaptive Grid Audit Drift
- Category: scientific-computing
- Languages: ["cpp", "cmake", "shell"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["cpp", "amr", "finite-volume", "scientific-computing", "checkpoint-restart"]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do not include reviewer-only notes, oracle patch recipes, or a full solution walkthrough in solver-visible files.

### Public contract

Create a standard task in which the agent repairs a local adaptive-grid finite-volume simulator under `/app`. The user-facing goal is that the shipped audit command produces `/app/output/conservation_audit.json` showing each bundled scenario reports balanced totals, matches the clean baseline across the structural changes, and matches an uninterrupted run when the harness interrupts at a midway snapshot and resumes from `/app/work/vault.bin`. The instruction should mention the output path, the six scenario names, per-case helper outputs (`<name>-audit.json` and `<name>-replay.json`), and the schema field names (`name`, `base_total`, `after_total`, `resumed_total`, `drift_ratio`, `balanced`, `base_match`). It must not prescribe sub-face area splitting on coarse-fine seams, parent-child reindex direction, weighting recipes in the aggregation, vault payload composition, post-resume relink, or halo copy order on the fix path.

The verifier should run the repaired simulator across six shipped scenarios, then parse the generated audit and independently re-derive expectations from the TSV initial conditions and the scenario schedules in `config/cases.toml`. A valid solution may rework internal seam accumulation, relink, aggregation, payload composition, resume, or halo synchronization, as long as the observable audit contract is satisfied without replacing the harness or weakening checks.

### Failure topology

The visible symptom is audit drift that only appears once the grid's structural decomposition shifts: identity-tier runs may look healthy while runs with growth or collapse phases stall, diverge, or show resumed totals that disagree with their uninterrupted counterparts. A scenario whose schedule only collapses cells, with no growth phase, also shows a drift row. The hard part is reconstructing how coarse-fine seam accumulation, relink after structural change, volume-weighted aggregation, vault payload composition, post-resume reattachment, and halo synchronization interact across opaque module roots.

### Environment shape

Use a single Docker image with a small C++17 CMake codebase: a control binary, neutral internal module directories, scenario specs under `data/cases/`, scenario-derived initial-condition payloads under `data/init/`, shell orchestration, config and documentation, and at least 20 files under `environment/` excluding Dockerfile. Keep decoy helpers that rhyme structurally with fix-path modules but perform non-fix work. Embed a build-stamp into the vault fingerprint so a pre-baked vault from a different build is rejected.

### Required artifacts

Step 2b must create the standard layout with `instruction.md`, `task.toml`, `output_contract.toml`, `construction_manifest.json`, digest-pinned `environment/Dockerfile`, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. Single-container, non-UI, hard difficulty, `[environment].allow_internet = false`.

### Test plan

Each test recomputes its expected value in Python from the `.case` schedule plus the scenario-seeded initial conditions; none reads an environment-side golden. Each fails against the broken baseline. Location letters refer to the flipping_point_contract.

- `test_a0` (A): storm seam-balance flag true (flux register records one sub-pulse per fine sub-face).
- `test_b1` (A): canyon seam-balance flag true under a multi-tier layout.
- `test_c2` (B): plume adjacency count equals the recomputed parent-child link total after growth.
- `test_d3` (B): spire adjacency count equals the recomputed link total under a collapse layout.
- `test_e4` (C): spire collapse total matches the volume-weighted recomputed integral (uneven children).
- `test_f5` (C): plume growth-then-collapse total returns to baseline within the numerical floor.
- `test_g6` (D): basin resumed position-weighted moment matches the uninterrupted reference (pending pulses survive the snapshot).
- `test_h7` (D): dune resumed moment matches the uninterrupted reference.
- `test_i8` (E): a tampered vault is rejected with a mismatched-signature line in the persistence audit log.
- `test_j9` (E): basin post-resume adjacency count is rebuilt correctly (relink on load).
- `test_k0` (F): canyon ghost column at the refinement seam matches the recomputed reference.
- `test_l1` (F): dune ghost column matches the recomputed reference.
- plus `test_no_canary_in_sources`: the fix-path source tree does not embed the anti-cheating canary token (not part of the flipping contract).

### Drafting guardrails

Symptoms-only instruction; opaque fix-path symbols; no golden audit under `environment/`; tests re-derive expectations from `.case` files and `cases.toml`; oracle substantive across six roots; CR8 limits symbols per visible orchestration file. Canary token lives only in tests and in a stale comment.

### Triviality Ledger

- Canned `/app/output/conservation_audit.json` blocked: verifier deletes outputs and regenerates via matrix, per-case, and replay runs.
- Seam-correction-only patch blocked: replay-equivalence and halo tests still fail.
- Relink-only patch blocked: aggregation and replay tests still fail.
- Vault-format-only patch blocked: aggregation and halo tests still fail.
- Halo-only patch blocked: matrix balance and replay tests still fail.
- Prompt-grep patch blocked: opaque module roots and `code_forbidden_tokens`.
- Pre-baked vault blocked: build-stamp embedded in fingerprint and verified on load.
- Hardcoded expected totals blocked: tests re-derive from scenario-seeded initial conditions; each scenario has distinct numeric fingerprint.

### Per-gate Pitfall Inventory

- RC1/RC7: substantive `solve.sh` across six fix-path C++ files (~120 semantic LOC).
- RC6/GX9/GX10: symptoms-only; no per-scenario answer recital; single polarity for binary status fields.
- CR1/CR2/CR8: manifest verbatim; four logical flip locations across six module roots; orchestration split across `drv_u/{run,run_refine,run_blend,run_sync}.cpp` to keep ≤2 fix-path symbols per visible file.
- CR7: fix-path function names and parameter names avoid every instruction noun; reviewer must re-grep after instruction is final.
- Docker: tmux, asciinema, digest-pinned FROM, narrow per-directory COPY, `.dockerignore`, OCI labels, `SOURCE_DATE_EPOCH`, build-stamp embedded in image.
- NOP/oracle: broken baseline fails domain assertions; oracle deterministic with no randomness, network, or time-coupling.

### Initial Draft Commitments

- `tasks/adaptive-mesh-conservation/instruction.md`
- `tasks/adaptive-mesh-conservation/task.toml`
- `tasks/adaptive-mesh-conservation/output_contract.toml`
- `tasks/adaptive-mesh-conservation/construction_manifest.json`
- `tasks/adaptive-mesh-conservation/environment/Dockerfile`
- `tasks/adaptive-mesh-conservation/environment/.dockerignore`
- `tasks/adaptive-mesh-conservation/environment/CMakeLists.txt`
- `tasks/adaptive-mesh-conservation/environment/include/cell_view.h`
- `tasks/adaptive-mesh-conservation/environment/include/flow_record.h`
- `tasks/adaptive-mesh-conservation/environment/include/vault_layout.h`
- `tasks/adaptive-mesh-conservation/environment/include/topo_link.h`
- `tasks/adaptive-mesh-conservation/environment/include/audit_emit.h`
- `tasks/adaptive-mesh-conservation/environment/include/case_spec.h`
- `tasks/adaptive-mesh-conservation/environment/include/ic_loader.h`
- `tasks/adaptive-mesh-conservation/environment/src/main.cpp`
- `tasks/adaptive-mesh-conservation/environment/src/case_io.cpp`
- `tasks/adaptive-mesh-conservation/environment/src/vault_io.cpp`
- `tasks/adaptive-mesh-conservation/environment/src/audit_emit.cpp`
- `tasks/adaptive-mesh-conservation/environment/acc_m/edge_corr.cpp`
- `tasks/adaptive-mesh-conservation/environment/lnk_n/relate.cpp`
- `tasks/adaptive-mesh-conservation/environment/agg_q/blend.cpp`
- `tasks/adaptive-mesh-conservation/environment/srl_p/serial.cpp`
- `tasks/adaptive-mesh-conservation/environment/rsm_k/resume.cpp`
- `tasks/adaptive-mesh-conservation/environment/sync_b/halo.cpp`
- `tasks/adaptive-mesh-conservation/environment/drv_u/run.cpp`
- `tasks/adaptive-mesh-conservation/environment/drv_u/run_refine.cpp`
- `tasks/adaptive-mesh-conservation/environment/drv_u/run_blend.cpp`
- `tasks/adaptive-mesh-conservation/environment/drv_u/run_sync.cpp`
- `tasks/adaptive-mesh-conservation/environment/swp_t/sweep.cpp`
- `tasks/adaptive-mesh-conservation/environment/emt_e/report.cpp`
- `tasks/adaptive-mesh-conservation/environment/prb_v/hist.cpp`
- `tasks/adaptive-mesh-conservation/environment/tap_w/trace.cpp`
- `tasks/adaptive-mesh-conservation/environment/cch_z/ring.cpp`
- `tasks/adaptive-mesh-conservation/environment/config/limits.toml`
- `tasks/adaptive-mesh-conservation/environment/config/cases.toml`
- `tasks/adaptive-mesh-conservation/environment/data/cases/storm.case`
- `tasks/adaptive-mesh-conservation/environment/data/cases/canyon.case`
- `tasks/adaptive-mesh-conservation/environment/data/cases/plume.case`
- `tasks/adaptive-mesh-conservation/environment/data/cases/spire.case`
- `tasks/adaptive-mesh-conservation/environment/data/cases/basin.case`
- `tasks/adaptive-mesh-conservation/environment/data/cases/dune.case`
- `tasks/adaptive-mesh-conservation/environment/data/init/profile_a.dat`
- `tasks/adaptive-mesh-conservation/environment/data/init/profile_b.dat`
- `tasks/adaptive-mesh-conservation/environment/data/init/profile_c.dat`
- `tasks/adaptive-mesh-conservation/environment/docs/layout.md`
- `tasks/adaptive-mesh-conservation/environment/docs/operations.md`
- `tasks/adaptive-mesh-conservation/environment/scripts/run-matrix.sh`
- `tasks/adaptive-mesh-conservation/environment/scripts/run-one.sh`
- `tasks/adaptive-mesh-conservation/environment/scripts/run-replay.sh`
- `tasks/adaptive-mesh-conservation/environment/scripts/clean-room.sh`
- `tasks/adaptive-mesh-conservation/tests/test.sh`
- `tasks/adaptive-mesh-conservation/tests/test_outputs.py`
- `tasks/adaptive-mesh-conservation/solution/solve.sh`

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: acc_m/edge_corr.cpp
  symbol: op_m
  kind: function
  signature: void op_m(const EdgePulse *a, FluxBank *b)
  purpose: Accumulates per-edge corrections at adjacent collection seams.
- path: lnk_n/relate.cpp
  symbol: step_n
  kind: function
  signature: int step_n(CellGrid *a, const int *b, int c, TopoLink *d)
  purpose: Rebuilds parent and child index relationships after the population changes.
- path: agg_q/blend.cpp
  symbol: fold_q
  kind: function
  signature: void fold_q(const CellPatch *a, int b, CellPatch *c)
  purpose: Combines child payloads into a coarser cell payload.
- path: srl_p/serial.cpp
  symbol: emit_p
  kind: function
  signature: int emit_p(const SimState *a, const char *b)
  purpose: Writes the runtime layout into the vault payload per the declared serializer ABI.
- path: rsm_k/resume.cpp
  symbol: load_k
  kind: function
  signature: int load_k(const char *a, SimState *b, VaultAudit *c)
  purpose: Reads a vault and reattaches cross-collection indices so the next step can run.
- path: sync_b/halo.cpp
  symbol: op_b
  kind: function
  signature: void op_b(CellPatch *a, const CellPatch *b, int c, int d)
  purpose: Synchronizes ghost payloads at the seam between adjacent collections.
```

The orchestration in `drv_u/{run,run_refine,run_blend,run_sync}.cpp` is correct scaffold (not on the fix path); it exists so no single visible file references more than two fix-path symbols (CR8). The drafter must not introduce bugs there.

#### flipping_point_contract

```
locations:
  - id: A
    path: acc_m/edge_corr.cpp
    controls_tests: [test_a0, test_b1]
  - id: B
    path: lnk_n/relate.cpp
    controls_tests: [test_c2, test_d3]
  - id: C
    path: agg_q/blend.cpp
    controls_tests: [test_e4, test_f5]
  - id: D
    path: srl_p/serial.cpp
    controls_tests: [test_g6, test_h7]
  - id: E
    path: rsm_k/resume.cpp
    controls_tests: [test_i8, test_j9]
  - id: F
    path: sync_b/halo.cpp
    controls_tests: [test_k0, test_l1]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: prb_v/hist.cpp
  kind: helper
  rhymes_with: op_m
  non_fix_purpose: Buckets per-cell values for documentation tables.
- path: tap_w/trace.cpp
  kind: helper
  rhymes_with: step_n
  non_fix_purpose: Formats stderr diagnostics not used in the audit path.
- path: cch_z/ring.cpp
  kind: helper
  rhymes_with: fold_q
  non_fix_purpose: Maintains a recent-step ring buffer for verbose mode only.
```

#### code_forbidden_tokens

```
code_forbidden_tokens: [finite, volume, sweep, scenarios, scenario, grid, structure, structural, decomposition, run, totals, balance, picture, baseline, harness, snapshot, vault, schedule, schedules, cells, growth, phase, drift, row, CMake, JSON, cases, array, entry, name, base_total, after_total, resumed_total, drift_ratio, balanced, base_match, helpers, audit, replay, matrix, slice, TSV, conditions, inputs, simulator, runs, clean, equivalent, output, conservation, mass, energy, flux, mesh, refine, refinement, coarsen, restart, checkpoint, register, boundary, level, amr]
```
