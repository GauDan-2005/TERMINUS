### Decision
GO — Attempt 1. Same distributed lifecycle design as the authoring spec, with hard-only expectations and no long-context label.

### Metadata
- Task name: module-hot-reload-epoch
- Title: Reload Epoch Drift
- Category: software-engineering
- Languages: ["Node.js", "Rust"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["nodejs", "rust", "hot-reload", "state", "debugging"]
- Milestones: 0

### Discovery budget
- Discovery: Deferred work belongs to the cycle that scheduled it even if the visible run has moved forward.
  Planned location: environment/src/core/b2/beta.js and scenario execution traces
  Why instruction must not reveal it: Naming this would point directly at the ordering fix.
- Discovery: Numeric records from older native revisions must be normalized before participating in the next row.
  Planned location: environment/src/native/src/lib.rs and cargo-run output
  Why instruction must not reveal it: It would disclose that the native helper is on the fix path.
- Discovery: Dependency factors are selected by the active descriptor for the row, not by a process-global cached value.
  Planned location: environment/src/core/c3/gamma.js plus fixture descriptors
  Why instruction must not reveal it: It would collapse the search to one cache helper.
- Discovery: The exported summary cross-checks per-row fields, so local row repairs must also update aggregate folding.
  Planned location: environment/src/core/d4/delta.js and report output
  Why instruction must not reveal it: It would reveal the summary layer as a required edit.

### Anti-trivialization verdict
All 21 checks PASS for the reasons recorded in the evidence sidecar: the task is not hidden-instance, not single-artifact, symptoms-only, distributed across roots, and has three topology candidates.

### Topology enumeration (3 candidate fix topologies)
- T1: Keep lifecycle memory in the JavaScript runner and normalize native rows at the boundary. Locations: src/core/a1/alpha.js, src/core/b2/beta.js, src/native/src/lib.rs. No single location covers both callback order and native normalization.
- T2: Attach row ownership to scheduled work and make descriptor reads row-local. Locations: src/core/b2/beta.js, src/core/c3/gamma.js, src/core/d4/delta.js. No single location covers ordering, descriptor choice, and aggregate checks.
- T3: Represent every cycle as a durable row and fold summaries from rows only. Locations: src/core/a1/alpha.js, src/native/src/lib.rs, src/core/d4/delta.js. Rows can be built, normalized, or summarized incorrectly independently.

### Rubric axes
All six rubric axes PASS: deterministic, well-specified, solvable by an expert, hard, useful, and outcome-verified.

### Hardness axes
All five axes PASS: the solver must discover runtime behavior, synthesize Node/Rust layers, diagnose symptoms, navigate coupling, and reason beyond a textbook recipe.

### Instruction completeness test
No. Reading only the instruction does not reveal the row model, deferred ordering, descriptor rule, or native normalization.

## Reviewer Appendix

### Implementation plan
Build a small mixed Node/Rust project with a scenario runner. The broken baseline emits a report but mishandles several local-run lifecycle boundaries. The oracle edits the opaque fix-path functions to make rows, deferred work, descriptor factors, native numeric records, and summary folding agree.

### Proposed file inventory
The proposed inventory is the Initial Draft Commitments from the authoring spec; it contains more than 20 substantive environment files excluding Dockerfile.

### Oracle notes
The oracle should rewrite the five fix-path functions to carry prior rows explicitly, preserve scheduled item ownership, select descriptor factors per row, normalize old native numeric records, and fold status from row invariants. It should not hardcode report answers.

### Collapse audit
Stage: implementation-plan

Smallest plausible successful patch:
Patch five coordinated functions across JavaScript and Rust so row assembly, deferred ordering, descriptor selection, native numeric normalization, and summary folding agree for all scenarios.

Likely editable frontier:
- src/core/a1/alpha.js
- src/core/b2/beta.js
- src/core/c3/gamma.js
- src/native/src/lib.rs
- src/core/d4/delta.js

Requirement-to-file map:
- repeated local runs stay stable -> multiple JavaScript and Rust roots
- deferred work is credited correctly -> scheduler plus row assembly
- descriptor changes are isolated -> descriptor helper plus summary
- old numeric records are normalized -> Rust helper plus fold layer

Oracle estimated complexity: 100+ lines of non-boilerplate logic

Red flags:
- none

Residual hardness:
The visible tree still requires dynamic experimentation because the instruction does not reveal which local boundaries are wrong or how the Node/Rust pieces interact.

Collapse verdict: PASS

### Naming-pass record

**Instruction nouns extracted:**
runtime, state, reload, migrations, hooks, dependencies, report, records, scenario, counter, plugin, runs, sequence, work, output

**Renames during drafting:**
- `stateFold` → `f_a`: state is an instruction noun
- `hookQueue` → `q_b`: hook is an instruction noun
- `dependencyFactor` → `k_c`: dependency is an instruction noun

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
  - A (`src/core/a1/alpha.js`): 3/10 = 0.3
  - B (`src/core/b2/beta.js`): 2/10 = 0.2
  - C (`src/core/c3/gamma.js`): 2/10 = 0.2
  - D (`src/native/src/lib.rs`): 2/10 = 0.2
  - E (`src/core/d4/delta.js`): 2/10 = 0.2
- Cap: 0.5. Max ratio observed: 0.3. Status: PASS

### Per-test feasibility pre-check
- Test: test_alpha_path
- Checks: one independent behavior row.
- Valid approaches: 2+
- Chain-dependent: no.
- Feasibility risk: LOW
- Test: test_beta_path
- Checks: one independent behavior row.
- Valid approaches: 2+
- Chain-dependent: no.
- Feasibility risk: LOW
- Test: test_gamma_path
- Checks: one independent behavior row.
- Valid approaches: 2+
- Chain-dependent: no.
- Feasibility risk: LOW
- Test: test_delta_path
- Checks: one independent behavior row.
- Valid approaches: 2+
- Chain-dependent: no.
- Feasibility risk: LOW
- Test: test_epsilon_path
- Checks: one independent behavior row.
- Valid approaches: 2+
- Chain-dependent: no.
- Feasibility risk: LOW
- Test: test_zeta_path
- Checks: one independent behavior row.
- Valid approaches: 2+
- Chain-dependent: no.
- Feasibility risk: LOW
- Test: test_eta_path
- Checks: one independent behavior row.
- Valid approaches: 2+
- Chain-dependent: no.
- Feasibility risk: LOW
- Test: test_theta_path
- Checks: one independent behavior row.
- Valid approaches: 2+
- Chain-dependent: no.
- Feasibility risk: LOW
- Test: test_iota_path
- Checks: one independent behavior row.
- Valid approaches: 2+
- Chain-dependent: no.
- Feasibility risk: LOW
- Test: test_kappa_path
- Checks: one independent behavior row.
- Valid approaches: 2+
- Chain-dependent: no.
- Feasibility risk: LOW
