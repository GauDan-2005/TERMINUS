### Decision
GO — Attempt 1.
- The raw snapshot/restore idea is shaped into a single-container hard system-administration task with symptoms gated on restart, rollover-style accounting, and dense file identity reuse.
- The planned fix surface is distributed across capture, replay, metadata propagation, and native inspection roots so no one location can satisfy the verifier.
- The public contract stays behavioral: restored output must agree with source observations, but the instruction must not name journal order, inode identity, or quota propagation as causes.

### Metadata
- version: 2
- Task name: staged-snapshot-drift
- Title: Restored Tree Drift
- Category: system-administration
- Languages: ["Go", "shell", "C"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["filesystem", "snapshots", "restore", "quotas", "hardlinks"]
- Milestones: 0

## Authoring Brief
This file is the only drafting input for Step 2b. Do not include reviewer-only notes, oracle patch recipes, or a full solution walkthrough in solver-visible files.

### Public contract
Create a standard task in which the agent repairs a local filesystem snapshot utility under `/app`. The user-facing goal is that the shipped audit command produces `/app/output/restore-audit.json` showing restored filesystem trees agree with their sources across normal runs, service restarts, quota-period transitions, and hardlink-heavy layouts. The instruction should mention the output path, that the JSON report identifies the checked scenarios, and that equivalence covers file content, directory shape, link relationships, and accounting records. It must not prescribe algorithms, file names, function names, journal mechanics, inode identity rules, or exact numeric thresholds.

The verifier should run the repaired utility in multiple isolated working directories, then parse the generated report and independently inspect the produced source/restored trees. A valid solution may rework internal data structures, replay logic, persistence boundaries, or scanner interfaces, as long as the observable audit contract is satisfied without replacing the harness or weakening checks.

### Failure topology
The visible symptom is a restored-tree drift that only appears when several ordinary operating conditions coincide: the service is restarted between staging and replay, accounting data crosses a period boundary, and the dataset contains many names sharing underlying file identity. The finished environment should make each condition look mundane on its own, with the inconsistent output emerging only from their interaction.

The hard part is reconstructing the system model across a Go service, a persisted operation log, a native filesystem scanner, shell orchestration, and accounting metadata. A local change that makes one scenario pass should be able to break another unless the solver understands how replay ordering, identity grouping, and metadata emission are coupled.

### Environment shape
Use a single Docker image with a small but realistic codebase. Major components should include: a Go command that runs the local service, a Go CLI that drives capture and materialization, internal Go packages with neutral path names, a C inspection helper invoked by the Go code, shell scenario scripts, config/profile data, and documentation that describes operations at a subsystem level without giving a repair recipe. Keep at least 20 files under `environment/` excluding Dockerfile/docker-compose.

### Required artifacts
Step 2b must create the standard layout: `instruction.md`, `task.toml`, `output_contract.toml`, `environment/Dockerfile`, all environment source/config/data files, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. The task must be single-container, non-UI, hard difficulty, anonymous author metadata, and `version = "2.0"`. The Dockerfile must install solution-time dependencies only, pin base image and package versions, set `WORKDIR /app`, and never copy tests or solution files.

The output contract should declare `/app/output/restore-audit.json` as the user-visible structured output. Tests should build the Go/C components if needed, run the same audit command that the instruction names, and write a binary reward.

### Test plan
- `test_alpha_matrix` (medium-hard calibration): builds a fresh small tree, runs the audit without interruption, and compares the report to verifier-side filesystem inspection. It must assert real content, directory shape, and emitted record agreement, not just JSON existence. Multiple valid approaches: yes. Chain-dependent: no; the test creates and removes its own workspace.
- `test_beta_matrix` (hard calibration): creates cross-directory names that share backing file identity, interrupts the service between staging and materialization, and verifies that the restored output preserves the same grouping derived from the source. Multiple valid approaches: yes. Chain-dependent: no; it owns the interruption sequence and computes expected groups at test time.
- `test_gamma_matrix` (hard calibration): captures a profile with interleaved create/update/remove operations, restarts the daemon before replay, and verifies repeated restore attempts produce the same independently inspected tree. Multiple valid approaches: yes. Chain-dependent: no; it launches a fresh service instance and does not rely on earlier tests.
- `test_delta_matrix` (hard calibration): verifies accounting records travel with the restored output by deriving expected records from source-side observations and comparing those records to both the report and restored filesystem state. Multiple valid approaches: yes. Chain-dependent: no; expected values come from the test's generated source tree.
- `test_epsilon_matrix` (hard calibration): runs a period-transition profile, restarts the service around the transition, and verifies the restored tree and accounting attribution agree with source observations. Multiple valid approaches: yes. Chain-dependent: no; the test uses a self-contained profile and does not import state from any other case.
- `test_zeta_matrix` (hard calibration): combines interruption, transition, nested directories, and identity-dense data. It should fail unless replay ordering, file identity grouping, and accounting propagation are all coordinated. Multiple valid approaches: yes. Chain-dependent: no; although it is a coupled scenario, the test sets all prerequisites itself and reports the first behavioral mismatch it finds.

Per `difficulty-calibration.mdc`, the suite should be hard even if one baseline check is medium-hard: no single test should force one exact implementation technique, every exact assertion should be computed from runtime-created inputs, and the tests must remain randomized-order safe.

### Drafting guardrails
The instruction should read like a concise bug report from an engineer, not a benchmark recipe. Do not name the journal, inode, quota metadata propagation, replay order, or any fix-path files/functions. Tests may assert computed equivalence and report schema fields that are documented in the instruction or visible code stubs, but must not expose golden answers, expected hashes, or answer-shaped fixture files. Environment comments must describe mechanics only and avoid correctional language near fix sites.

### Triviality Ledger
- Replay-order-only trap: blocked because tests separately cover identity grouping and accounting propagation; changing only operation ordering cannot satisfy all six scenario checks.
- Identity-map-only trap: blocked because accounting records are independently derived by verifier-side inspection, so preserving file links without moving metadata still fails.
- Accounting-only trap: blocked because tree digests and link-group checks are computed from actual restored files, not the JSON report alone.
- Harness-replacement trap: blocked because tests call native inspection and compare filesystem state outside the generated report, so replacing the runner cannot fake correctness.
- One-scenario patch trap: blocked by six scenario profiles with different combinations of clean/interrupted/transition/dense layouts; a literal case table cannot generalize without reimplementing the intended state model.

### Per-gate Pitfall Inventory
- RC1: avoid a solve that deletes checks or reverts a toggle; the oracle must add coordinated logic in Go and C paths.
- RC2: keep solver-visible names neutral; no `broken`, `buggy`, `golden`, `expected`, `journal_fix`, or cause-shaped file names.
- RC3: tests must inspect real filesystem output and accounting records, not just report existence or JSON shape.
- RC4: expected values are derived inside verifier code from generated source trees; no modifiable golden files under `environment/`.
- RC5: sample data may describe inputs, but no reference restore trees, expected digests, or answer-shaped ledgers may be visible.
- RC6: instruction stays symptoms-only and avoids naming replay order, inode identity, quota propagation, concrete files, flags, algorithms, or thresholds.
- RC7: oracle should contain at least 80 substantive non-boilerplate lines across the transitive fix; do not pad with cosmetic rewrites.
- GX1: no comments on fix paths should use correctional vocabulary; do not alter comments in the oracle.
- GX3: semantic edit distance must reflect real coordination code, not byte-equivalent heredocs or comment shuffles.
- GX9: instruction must not enumerate per-scenario expected values; describe the audit outcome and let tests derive values.
- GX10: avoid mixed-polarity prose such as saying one case is both clean and stale in the same sentence.
- Static checks: pin Docker sources and apt packages, keep environment file count above 20, use the exact `test.sh` reward footer, and declare the structured output in `output_contract.toml`.

### Initial Draft Commitments
- `instruction.md`
- `task.toml`
- `output_contract.toml`
- `construction_manifest.json`
- `environment/Dockerfile`
- `environment/go.mod`
- `environment/Makefile`
- `environment/README.md`
- `environment/docs/architecture.md`
- `environment/docs/operators.md`
- `environment/config/profiles.toml`
- `environment/config/layouts.toml`
- `environment/cmd/apex/main.go`
- `environment/cmd/ctl/main.go`
- `environment/internal/a0/core.go`
- `environment/internal/a0/scan.go`
- `environment/internal/a0/pack.go`
- `environment/internal/b1/log.go`
- `environment/internal/b1/replay.go`
- `environment/internal/b1/checkpoint.go`
- `environment/internal/c2/table.go`
- `environment/internal/c2/roll.go`
- `environment/internal/d3/map.go`
- `environment/internal/d3/pair.go`
- `environment/internal/e4/io.go`
- `environment/internal/e4/walk.go`
- `environment/internal/f5/types.go`
- `environment/internal/f5/encode.go`
- `environment/internal/g6/cache.go`
- `environment/internal/h7/rollup.go`
- `environment/probe/fswalk.c`
- `environment/probe/fswalk.h`
- `environment/probe/measure.c`
- `environment/probe/list.c`
- `environment/scripts/run-matrix.sh`
- `environment/scripts/make-case.sh`
- `environment/scripts/clean-room.sh`
- `environment/data/profiles/basic.toml`
- `environment/data/profiles/roll.toml`
- `environment/data/layouts/alpha.manifest`
- `environment/data/layouts/beta.manifest`
- `environment/data/layouts/gamma.manifest`
- `environment/data/layouts/delta.manifest`
- `solution/solve.sh`
- `tests/test.sh`
- `tests/test_outputs.py`

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table
```
- path: internal/a0/core.go
  symbol: phase_a
  kind: function
  signature: func phase_a(a *stateX, b itemY) error
  purpose: merges an incoming item into an in-memory graph used by later materialization
- path: internal/b1/replay.go
  symbol: fold_b
  kind: function
  signature: func fold_b(a []rowX, b uint64) ([]rowX, error)
  purpose: orders persisted rows into a deterministic stream consumed by the caller
- path: internal/c2/roll.go
  symbol: mark_c
  kind: function
  signature: func mark_c(a *mapX, b uint64, c []entryX) error
  purpose: carries per-period attributes from input entries into emitted records
- path: internal/d3/pair.go
  symbol: bind_d
  kind: function
  signature: func bind_d(a *nodeX, b tokenX) bool
  purpose: decides whether two graph nodes should share the same emitted backing object
- path: probe/measure.c
  symbol: walk_e
  kind: function
  signature: int walk_e(struct qx *a, const char *b, unsigned long c)
  purpose: records stable observations from a filesystem traversal for the Go caller
```

#### flipping_point_contract
```
locations:
  - id: A
    path: internal/a0/core.go
    controls_tests: [test_alpha_matrix, test_beta_matrix]
  - id: B
    path: internal/b1/replay.go
    controls_tests: [test_gamma_matrix, test_delta_matrix]
  - id: C
    path: internal/c2/roll.go
    controls_tests: [test_epsilon_matrix, test_zeta_matrix]
  - id: D
    path: internal/d3/pair.go
    controls_tests: [test_beta_matrix, test_zeta_matrix]
  - id: E
    path: probe/measure.c
    controls_tests: [test_delta_matrix, test_epsilon_matrix]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest
```
- path: internal/g6/cache.go
  kind: helper
  rhymes_with: phase_a
  non_fix_purpose: maintains transient CLI display state for non-service commands
- path: internal/h7/rollup.go
  kind: helper
  rhymes_with: mark_c
  non_fix_purpose: summarizes profile statistics for documentation and dry-run output
- path: probe/list.c
  kind: helper
  rhymes_with: walk_e
  non_fix_purpose: implements a shallow listing mode used by diagnostics but not the audit path
```

#### code_forbidden_tokens
```
code_forbidden_tokens: [service, audit, trees, source, restart, problem, quota, period, data, directory, layouts, hardlinks, command, report, scenarios, link, relationships, accounting, records, runner, checks, completion]
```
