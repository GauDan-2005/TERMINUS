### Decision
GO — Attempt 1.
- The seed is shaped into a hard local inference-runtime debugging task with Rust numeric execution and Go report collation.
- The planned fix surface spans compressed numeric handling, grouped request movement, local state reuse, trace emission, and final collation.
- The public contract stays symptoms-only and does not label the internal defect.

### Metadata
- version: 2
- Task name: quantized-beam-alignment
- Title: Local Inference Drift
- Category: machine-learning
- Languages: ["Rust", "Go"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["inference", "rust", "go", "debugging", "runtime"]
- Milestones: 0

## Authoring Brief
This file is the only drafting input for Step 2b. Do not include reviewer-only notes or solution steps in solver-visible files.

### Public contract
Create a standard task where the agent repairs a local Rust and Go inference sandbox under `/app`. The human prompt should say that the local runner writes `/app/output/report.json` and that sequence outputs from compressed integer paths must agree with the same requests run without compression, including grouped requests and changed candidate order. The report should include case names, produced token lists, trace rows, and a summary showing whether the local runs agree. Do not name the internal metadata, state-handle, or collation defects.

The verifier should execute the local runner, parse the report, and independently derive expected values from scenario descriptions embedded in test code. A valid solution can reorganize the implementation as long as the final behavior is deterministic and the runner/report contract remains intact.

### Failure topology
Single-request and uncompressed cases should look mostly healthy. The visible drift should appear when compressed integer paths are combined with grouped requests, changed candidate order, and reused local state. The task should force the solver to compare raw Rust trace rows with the Go-collated report.

The hard part is that each local-looking repair leaves a different gap: numeric reconstruction alone does not move the associated local handles, state movement alone does not repair compressed values, and report collation alone cannot make the raw traces coherent.

### Environment shape
Use a single Docker image with a Rust crate, a Go collation command, shell runner, scenario data, and brief operational docs. Major directories: `src/` for the Rust runtime, `cmd/` and `internal/` for Go report assembly, `tools/` for the local runner, `data/` for input scenario files, `config/` for metadata, and `docs/` for normal engineering context. Keep at least 20 files under `environment/` excluding Dockerfile/docker-compose.

### Required artifacts
Step 2b must create `instruction.md`, `task.toml`, `output_contract.toml`, `construction_manifest.json`, `environment/Dockerfile`, environment source/config/data files, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. The task is single-step, single-container, non-UI, not long-context, hard difficulty, anonymous author metadata, `version = "2.0"`, and `[environment].allow_internet = false`.

The Dockerfile must include Rust, Go, pytest, tmux, and asciinema; use a digest-pinned base, narrow COPY commands, `.dockerignore`, OCI labels, and no runtime installs in the verifier.

### Test plan
- `test_alpha_path`: verifies baseline uncompressed grouped output against a derived model. Multiple approaches: yes. Chain-dependent: no.
- `test_beta_path`: checks compressed single-request output agrees with the derived model. Multiple approaches: yes. Chain-dependent: no.
- `test_gamma_path`: checks grouped compressed output for one scenario. Multiple approaches: yes. Chain-dependent: no.
- `test_delta_path`: checks changed candidate order preserves produced token identity. Multiple approaches: yes. Chain-dependent: no.
- `test_epsilon_path`: checks reused local state is isolated between adjacent requests. Multiple approaches: yes. Chain-dependent: no.
- `test_zeta_path`: checks raw trace rows and final rows agree for compressed grouped runs. Multiple approaches: yes. Chain-dependent: no.
- `test_eta_path`: checks every final row records the order used by that run. Multiple approaches: yes. Chain-dependent: no.
- `test_theta_path`: checks summary disagreement markers reject drift instead of hiding it. Multiple approaches: yes. Chain-dependent: no.
- `test_iota_path`: checks the Go collation layer keeps one row per case and does not merge reused local rows. Multiple approaches: yes. Chain-dependent: no.
- `test_kappa_path`: checks repeated runner invocations are deterministic. Multiple approaches: yes. Chain-dependent: no.

### Drafting guardrails
The instruction should read like a short bug report, not a repair recipe. Avoid exact file names, function names, algorithms, thresholds, and cause statements. Tests must compute expected values in Python from embedded scenario parameters, not read golden outputs. Environment comments must describe normal mechanics only and avoid correctional vocabulary near changed lines.

### Triviality Ledger
- Report-forgery trap: blocked because tests inspect raw trace rows and final summary consistency.
- Numeric-only trap: blocked because ordering and local state trace tests still fail.
- State-only trap: blocked because compressed integer outputs remain wrong.
- Collation-only trap: blocked because raw rows are checked independently.
- One-case literal trap: blocked by ten scenario-focused tests covering multiple combinations.

### Per-gate Pitfall Inventory
- RC1: oracle must add real Rust and Go logic, not delete code or bypass the compressed path.
- RC2: file and test names must stay neutral; no broken/golden/expected/fix tokens.
- RC3: tests assert domain-correct token lists, traces, and summaries, not file existence.
- RC4: expected values are re-derived in test code and not read from solver-modifiable files.
- RC5: environment data can hold scenario inputs, not expected outputs or answer hashes.
- RC6: instruction stays symptoms-only and avoids named algorithms, thresholds, files, functions, and causes.
- RC7/GX3: solve.sh should make 80+ substantive semantic-diff LOC across Rust and Go.
- CR1/CR7: use the manifest's opaque symbols on the fix path and keep instruction nouns out of those symbols.
- CR2: no single location controls a majority of tests.
- CR8: avoid a single visible orchestrator referencing more than two manifest symbols.
- GX1: no correctional comments near oracle-changed lines.
- GX9/GX10: instruction must not enumerate answer rows or create polarity contradictions.
- Static checks: use the canonical test.sh, output contract, Docker rules, and 20+ environment files.

### Initial Draft Commitments
- `instruction.md`
- `task.toml`
- `output_contract.toml`
- `construction_manifest.json`
- `environment/Dockerfile`
- `environment/.dockerignore`
- `environment/Cargo.toml`
- `environment/Cargo.lock`
- `environment/go.mod`
- `environment/go.sum`
- `environment/README.md`
- `environment/docs/architecture.md`
- `environment/docs/operations.md`
- `environment/config/sets.txt`
- `environment/config/runtime.txt`
- `environment/data/alpha.txt`
- `environment/data/beta.txt`
- `environment/data/gamma.txt`
- `environment/data/delta.txt`
- `environment/src/main.rs`
- `environment/src/a0/mod.rs`
- `environment/src/b1/mod.rs`
- `environment/src/c2/mod.rs`
- `environment/src/d3/mod.rs`
- `environment/src/e4/mod.rs`
- `environment/src/f5/mod.rs`
- `environment/src/g6/mod.rs`
- `environment/cmd/align/main.go`
- `environment/internal/collate/table.go`
- `environment/tools/run_local.sh`
- `solution/solve.sh`
- `tests/test.sh`
- `tests/test_outputs.py`

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table
```
- path: src/a0/mod.rs
  symbol: A0
  kind: class
  signature: pub struct A0
  purpose: stores packed numeric column parameters
- path: src/a0/mod.rs
  symbol: ax
  kind: function
  signature: pub fn ax(a: &A0, b: &[i32], c: usize) -> Vec<i32>
  purpose: expands integer rows into working values
- path: src/b1/mod.rs
  symbol: B0
  kind: class
  signature: pub struct B0
  purpose: stores per-item working handles
- path: src/b1/mod.rs
  symbol: bx
  kind: function
  signature: pub fn bx(a: &mut B0, b: &[usize]) -> Vec<usize>
  purpose: moves working handles according to a provided order
- path: src/c2/mod.rs
  symbol: C0
  kind: class
  signature: pub struct C0
  purpose: stores reusable local rows
- path: src/c2/mod.rs
  symbol: cx
  kind: function
  signature: pub fn cx(a: &mut C0, b: usize, c: &[i32]) -> i32
  purpose: folds a working row into reusable local state
- path: src/d3/mod.rs
  symbol: dx
  kind: function
  signature: pub fn dx(a: &[i32], b: &[usize]) -> Vec<i32>
  purpose: returns selected working values
- path: src/e4/mod.rs
  symbol: E0
  kind: class
  signature: pub struct E0
  purpose: stores trace rows for output
- path: src/e4/mod.rs
  symbol: ex
  kind: function
  signature: pub fn ex(a: &mut E0, b: &str, c: &[i32], d: &[usize])
  purpose: records output rows
- path: cmd/align/main.go
  symbol: fold
  kind: function
  signature: func fold(a []entry) []entry
  purpose: collates raw rows into the final report
```

#### flipping_point_contract
```
locations:
  - id: A
    path: src/a0/mod.rs
    controls_tests: [test_alpha_path, test_beta_path]
  - id: B
    path: src/b1/mod.rs
    controls_tests: [test_gamma_path, test_delta_path]
  - id: C
    path: src/c2/mod.rs
    controls_tests: [test_epsilon_path, test_zeta_path]
  - id: D
    path: src/e4/mod.rs
    controls_tests: [test_eta_path, test_theta_path]
  - id: E
    path: cmd/align/main.go
    controls_tests: [test_iota_path, test_kappa_path]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest
```
- path: src/f5/mod.rs
  kind: helper
  rhymes_with: ax
  non_fix_purpose: formats diagnostics for dry-run rows
- path: src/g6/mod.rs
  kind: helper
  rhymes_with: bx
  non_fix_purpose: sorts display-only identifiers
- path: internal/collate/table.go
  kind: helper
  rhymes_with: fold
  non_fix_purpose: normalizes presentation labels
```

#### code_forbidden_tokens
```
code_forbidden_tokens: [runtime, sequence, outputs, compressed, integer, paths, grouped, requests, candidate, order, state, slots, report, rows, tokens, traces, summary]
```
