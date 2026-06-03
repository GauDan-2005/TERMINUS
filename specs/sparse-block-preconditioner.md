### Decision

GO — Attempt 1. The sparse block solver audit idea is shaped into a single-container hard scientific-computing task with symptoms gated on block layout assembly, vector reordering, preconditioner application space, and residual reporting under six bundled linear systems. The planned fix surface is distributed across four opaque module roots so no one location satisfies the verifier. The public contract stays behavioral: the solver audit must agree with independently recomputed residuals and convergence, but the instruction must not name layout conversion rules, permutation direction, preconditioner order, or norm recipes as causes.

### Metadata

- version: 2
- Task name: sparse-block-preconditioner
- Title: Block Solver Audit Drift
- Category: scientific-computing
- Languages: ["cpp", "cmake", "shell"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["cpp", "sparse", "linear-algebra", "preconditioner", "scientific-computing"]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do not include reviewer-only notes, oracle patch recipes, or a full solution walkthrough in solver-visible files.

### Public contract

Create a standard task in which the agent repairs a local block-sparse iterative solver harness under `/app`. The user-facing goal is that the shipped audit command produces `/app/output/solver-audit.json` showing each bundled linear system reports clean status with iteration counts, final residual, reported residual, and residual agreement aligned to the true linear system. The instruction should mention the output path, the six case names, per-case helper output, and that agreement covers convergence status, iteration tally, both residual fields, and the agreement flag. It must not prescribe block layout indexing, permutation direction, preconditioner application order, or norm scaling recipes on the fix path.

The verifier should run the repaired harness across six shipped scenarios, then parse the generated report and independently re-derive expectations from the bundled case specifications. A valid solution may rework internal layout assembly, vector reordering, preconditioner stepping, or metric routines, as long as the observable audit contract is satisfied without replacing the harness or weakening checks.

### Failure topology

The visible symptom is audit drift that only appears once block reordering enters the pipeline: identity-order systems may look healthy while reordered systems stall, diverge, or show reported residuals that disagree with independently measured values. Smoke-length runs can look healthy while the matrix scenarios fail. The hard part is reconstructing how layout assembly, vector reordering, preconditioner application, and residual reporting interact across opaque module roots.

### Environment shape

Use a single Docker image with a small C++17 CMake codebase: a control binary, neutral internal module directories, scenario specs under `data/cases/`, shell orchestration, config and documentation, and at least 20 files under `environment/` excluding Dockerfile. Keep decoy helpers that rhyme structurally with fix-path modules but perform non-fix work.

### Required artifacts

Step 2b must create the standard layout with `instruction.md`, `task.toml`, `output_contract.toml`, `construction_manifest.json`, digest-pinned `environment/Dockerfile`, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. Single-container, non-UI, hard difficulty, `[environment].allow_internet = false`.

### Test plan

- `test_a0`: matrix command; six cases basalt through opal; each `ok` true.
- `test_b1`: direct-case helper matches matrix slice for basalt.
- `test_c2`: basalt identity-order convergence and low iteration count.
- `test_d3`: flint identity-order convergence with off-diagonal coupling.
- `test_e4`: shale reordered system converges within iteration cap.
- `test_f5`: garnet reordered system converges with coupling blocks.
- `test_g6`: mica reordered system reaches low final residual.
- `test_h7`: opal mixed reordered system reports clean status.
- `test_i8`: reported residual matches independently computed norm for all cases.
- `test_j9`: two matrix runs produce equivalent JSON.
- `test_k0`: convergent cases stay below iteration cap without hitting limit.
- `test_l1`: run-one shale matches matrix slice fields.

### Drafting guardrails

Symptoms-only instruction; opaque fix-path symbols; no golden audit under `environment/`; tests re-derive expectations from `.case` files; oracle substantive across four roots; CR8 limits symbols per visible orchestration file.

### Triviality Ledger

- Canned `/app/output/solver-audit.json` blocked: verifier deletes output and regenerates via matrix and direct runs.
- One-file layout-only patch blocked: perm, prec, and scale tested separately on reorder and residual cases.
- Permutation-only patch blocked: layout indexing and preconditioner order fail independently.
- Preconditioner-only patch blocked: residual reporting and layout cases still fail.
- Prompt-grep patch blocked: opaque module roots and `code_forbidden_tokens`.

### Per-gate Pitfall Inventory

- RC1/RC7: substantive `solve.sh` across layout, perm, prec, scale modules (≥80 semantic LOC).
- RC6/GX9/GX10: symptoms-only; no per-case answer recital.
- CR1/CR2/CR8: manifest verbatim; four flip locations; ≤2 symbols per orchestration file.
- Docker: tmux, asciinema, digest-pinned FROM, narrow COPY, `.dockerignore`.
- NOP/oracle: broken baseline fails domain assertions; oracle deterministic.

### Initial Draft Commitments

- `tasks/sparse-block-preconditioner/instruction.md`
- `tasks/sparse-block-preconditioner/task.toml`
- `tasks/sparse-block-preconditioner/output_contract.toml`
- `tasks/sparse-block-preconditioner/construction_manifest.json`
- `tasks/sparse-block-preconditioner/environment/Dockerfile`
- `tasks/sparse-block-preconditioner/environment/CMakeLists.txt`
- `tasks/sparse-block-preconditioner/environment/include/case_spec.h`
- `tasks/sparse-block-preconditioner/environment/include/matrix_view.h`
- `tasks/sparse-block-preconditioner/environment/include/solver_report.h`
- `tasks/sparse-block-preconditioner/environment/csr_m/assemble.cpp`
- `tasks/sparse-block-preconditioner/environment/bsr_n/layout.cpp`
- `tasks/sparse-block-preconditioner/environment/perm_p/order.cpp`
- `tasks/sparse-block-preconditioner/environment/prec_r/apply.cpp`
- `tasks/sparse-block-preconditioner/environment/scale_q/metric.cpp`
- `tasks/sparse-block-preconditioner/environment/solve_s/driver.cpp`
- `tasks/sparse-block-preconditioner/environment/flow_t/report.cpp`
- `tasks/sparse-block-preconditioner/environment/drive_u/run.cpp`
- `tasks/sparse-block-preconditioner/environment/spill_v/bucket.cpp`
- `tasks/sparse-block-preconditioner/environment/mirror_w/trace.cpp`
- `tasks/sparse-block-preconditioner/environment/src/main.cpp`
- `tasks/sparse-block-preconditioner/environment/config/limits.toml`
- `tasks/sparse-block-preconditioner/environment/docs/operations.md`
- `tasks/sparse-block-preconditioner/environment/docs/layout.md`
- `tasks/sparse-block-preconditioner/environment/data/cases/basalt.case`
- `tasks/sparse-block-preconditioner/environment/data/cases/flint.case`
- `tasks/sparse-block-preconditioner/environment/data/cases/shale.case`
- `tasks/sparse-block-preconditioner/environment/data/cases/garnet.case`
- `tasks/sparse-block-preconditioner/environment/data/cases/mica.case`
- `tasks/sparse-block-preconditioner/environment/data/cases/opal.case`
- `tasks/sparse-block-preconditioner/environment/scripts/run-matrix.sh`
- `tasks/sparse-block-preconditioner/environment/scripts/run-one.sh`
- `tasks/sparse-block-preconditioner/environment/scripts/clean-room.sh`
- `tasks/sparse-block-preconditioner/tests/test.sh`
- `tasks/sparse-block-preconditioner/tests/test_outputs.py`
- `tasks/sparse-block-preconditioner/solution/solve.sh`

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: bsr_n/layout.cpp
  symbol: fn_n
  kind: function
  signature: void fn_n(const MatrixView *a, int b, BsrPack *c)
  purpose: Builds block-row layout storage after reordering metadata is applied.
- path: perm_p/order.cpp
  symbol: map_p
  kind: function
  signature: void map_p(const double *a, const int *b, int c, int d, double *e)
  purpose: Reorders dense vectors according to the active block map.
- path: prec_r/apply.cpp
  symbol: step_r
  kind: function
  signature: void step_r(const BsrPack *a, const double *b, double *c)
  purpose: Applies the block diagonal preconditioner to a workspace vector.
- path: scale_q/metric.cpp
  symbol: norm_q
  kind: function
  signature: double norm_q(const double *a, int b)
  purpose: Computes the scalar residual metric recorded in the audit report.
- path: flow_t/report.cpp
  symbol: emit_t
  kind: function
  signature: int emit_t(const SolveResult *a, const char *b)
  purpose: Writes JSON audit output for one scenario run.
- path: drive_u/run.cpp
  symbol: run_u
  kind: function
  signature: int run_u(const CaseSpec *a, const char *b, SolveResult *c)
  purpose: Orchestrates one scenario through assembly, solve, and metric capture.
```

#### flipping_point_contract

```
locations:
  - id: A
    path: bsr_n/layout.cpp
    controls_tests: [test_e4, test_f5, test_g6, test_h7]
  - id: B
    path: perm_p/order.cpp
    controls_tests: [test_b1, test_e4, test_f5, test_l1, test_i8]
  - id: C
    path: prec_r/apply.cpp
    controls_tests: [test_k0, test_g6, test_h7, test_a0]
  - id: D
    path: scale_q/metric.cpp
    controls_tests: [test_i8, test_c2, test_d3, test_j9]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: spill_v/bucket.cpp
  kind: helper
  rhymes_with: fn_n
  non_fix_purpose: Buckets small integers for documentation tables.
- path: mirror_w/trace.cpp
  kind: helper
  rhymes_with: emit_t
  non_fix_purpose: Formats stderr diagnostics not used in the audit path.
```

#### code_forbidden_tokens

```
code_forbidden_tokens: [solver, block, sparse, iterative, harness, audit, bundled, linear, systems, matrix, output, JSON, cases, convergence, status, iteration, tally, residual, agreement, flag, basalt, flint, shale, garnet, mica, opal, name, ok, iterations, final, reported, residual_agrees, cap, limit, clean, pipeline, reordering, identity, order, reordered, independently, measured, values, equivalent, fields, slice, helper, command, script, run, path, report, scenario, specifications, observable, contract, agreement, converge, stall, diverge, disagree]
```
