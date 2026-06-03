### Decision
GO — Attempt 1. The idea has a distributed Rust/Go fix surface, symptoms-only prompt, and deterministic verifier plan.

### Metadata
- Task name: quantized-beam-alignment
- Title: Local Inference Drift
- Category: machine-learning
- Languages: ["Rust", "Go"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["inference", "rust", "go", "debugging", "runtime"]
- Milestones: 0

### Discovery budget
- Discovery: Packed numeric rows carry per-column metadata that must survive grouped execution.
  Planned location: `environment/src/a0/mod.rs` and `environment/data/*.txt`.
  Why instruction must not reveal it: it would disclose the first fix site.
- Discovery: Candidate movement changes logical order without moving every associated local handle.
  Planned location: `environment/src/b1/mod.rs` and `environment/src/c2/mod.rs`.
  Why instruction must not reveal it: it would collapse the diagnosis to remapping.
- Discovery: Reused local state appears healthy in single-request runs but contaminates grouped cases.
  Planned location: `environment/src/c2/mod.rs` and scenario fixtures.
  Why instruction must not reveal it: it would over-narrow the coupled condition.
- Discovery: The Go collation stage can hide or expose disagreements independently of raw Rust traces.
  Planned location: `environment/cmd/align/main.go` and `environment/internal/collate/table.go`.
  Why instruction must not reveal it: it would reduce cross-language discovery.

### Anti-trivialization verdict
All 21 checks are PASS for attempt 1. The task is not hidden-instance, not one-file repair, not a small declarative table, and not a known recipe. The prompt can stay honest without naming the defect.

### Topology enumeration (3 candidate fix topologies)
- T1 numeric-first: `src/a0/mod.rs::ax`, `src/b1/mod.rs::bx`, `cmd/align/main.go::fold`; no single location suffices because correct values alone do not align traces or summary.
- T2 state-first: `src/b1/mod.rs::bx`, `src/c2/mod.rs::cx`, `src/d3/mod.rs::dx`; no single location suffices because state movement cannot repair compressed values.
- T3 report-consistency: `src/e4/mod.rs::ex`, `cmd/align/main.go::fold`, `internal/collate/table.go::mix`; no single location suffices because collation cannot forge raw trace correctness.

### Rubric axes
Verifiable PASS; well-specified PASS; solvable PASS; difficult PASS; interesting PASS; outcome-verified PASS.

### Hardness axes
Discover PASS, Synthesize PASS, Diagnose PASS, Navigate coupling PASS, Reason beyond training PASS. The finished task requires runtime experiments and cross-language code reading.

### Instruction completeness test
Can the agent solve this by reading ONLY instruction.md without deeply engaging with the codebase? No. The instruction only names symptoms and the report surface.

## Reviewer Appendix

### Implementation plan
Build a small Rust command that emits raw rows for several local inference scenarios and a Go command that collates those rows into `/app/output/report.json`. The baseline should be wrong only when compressed integer execution combines grouped requests, changed candidate order, and local state reuse.

### Proposed file inventory
See the authoring spec's Initial Draft Commitments; it lists over 20 environment files plus standard task files.

### Oracle notes
The oracle should patch Rust numeric expansion, Rust handle movement/reuse behavior, trace emission, and Go final collation. It should not write expected JSON directly.

### Collapse audit
Stage: implementation-plan

Smallest plausible successful patch: coordinate value expansion, item movement, local reuse, raw trace recording, and Go report collation.

Likely editable frontier:
- `src/a0/mod.rs`
- `src/b1/mod.rs`
- `src/c2/mod.rs`
- `src/e4/mod.rs`
- `cmd/align/main.go`

Requirement-to-file map:
- compressed and uncompressed agreement -> Rust numeric and trace modules
- grouped requests and changed order -> Rust movement modules
- report summary -> Go collation

Oracle estimated complexity: 90-130 semantic LOC.

Red flags:
- none

Residual hardness:
After the file tree is visible, a solver must still determine which scenario combination exposes the coupled defect and repair multiple layers without report forgery.

Collapse verdict: PASS

### Naming-pass record

**Instruction nouns extracted:** runtime, sequence, outputs, compressed, integer, paths, grouped, requests, candidate, order, state, slots, report, rows, tokens, traces, summary

**Renames during drafting:**
- `quant_expand` -> `ax`: Removed a prompt noun from the fix-path symbol.
- `test_grouped_slots` -> `test_zeta_path`: Removed instruction nouns from planned test names.

**Test names audited:**
- test_alpha_path
- test_beta_path
- test_gamma_path
- test_delta_path
- test_epsilon_path
- test_zeta_path
- test_eta_path
- test_theta_path
- test_iota_path
- test_kappa_path

**Concentration math:**
- Total tests across `flipping_point_contract`: 10
- Per location:
  - A (`src/a0/mod.rs`): 2/10 = 0.2
  - B (`src/b1/mod.rs`): 2/10 = 0.2
  - C (`src/c2/mod.rs`): 2/10 = 0.2
  - D (`src/e4/mod.rs`): 2/10 = 0.2
  - E (`cmd/align/main.go`): 2/10 = 0.2
- Cap: 0.5. Max ratio observed: 0.2. Status: PASS

### Per-test feasibility pre-check
- Test: test_alpha_path. Checks uncompressed grouped rows. Valid approaches: 2+. Chain-dependent: no. Feasibility risk: LOW.
- Test: test_beta_path. Checks compressed single request. Valid approaches: 2+. Chain-dependent: no. Feasibility risk: LOW.
- Test: test_gamma_path. Checks grouped compressed output. Valid approaches: 2+. Chain-dependent: no. Feasibility risk: LOW.
- Test: test_delta_path. Checks changed order identity. Valid approaches: 2+. Chain-dependent: no. Feasibility risk: LOW.
- Test: test_epsilon_path. Checks local reuse isolation. Valid approaches: 2+. Chain-dependent: no. Feasibility risk: LOW.
- Test: test_zeta_path. Checks raw/final agreement. Valid approaches: 2+. Chain-dependent: no. Feasibility risk: LOW.
- Test: test_eta_path. Checks order traces. Valid approaches: 2+. Chain-dependent: no. Feasibility risk: LOW.
- Test: test_theta_path. Checks summary markers. Valid approaches: 2+. Chain-dependent: no. Feasibility risk: LOW.
- Test: test_iota_path. Checks collation cardinality. Valid approaches: 2+. Chain-dependent: no. Feasibility risk: LOW.
- Test: test_kappa_path. Checks determinism. Valid approaches: 2+. Chain-dependent: no. Feasibility risk: LOW.
