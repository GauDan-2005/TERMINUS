### Decision

GO — Attempt 1. The design keeps the prompt symptoms-only, distributes the fix across six neutral Rust modules, and blocks the naive full-cache-flush path with reuse checks.

### Metadata

- Task name: incremental-index-invalidation
- Title: Index Invalidation Drift
- Category: software-engineering
- Languages: ["Rust", "TypeScript"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["rust", "typescript", "indexing", "cache-invalidation", "tooling"]
- Milestones: 0

### Discovery budget

- Discovery: Slot entries must be replaced per active root, not globally flushed or blindly appended.
  Planned location: `environment/r1/b.rs` with state shapes in `environment/src/model.rs` and traces under `environment/traces/`.
  Why instruction must not reveal it: Naming slot-level replacement would point directly to the core invalidation defect and reduce the task to a targeted cache edit.
- Discovery: Generated TypeScript rows carry source provenance that changes when a generated root is refreshed.
  Planned location: `environment/r2/c.rs` plus fixture files under `environment/fixtures/*/gen-*/`.
  Why instruction must not reveal it: The prompt can require current sources but should not disclose the generated file comment convention or the propagation site.
- Discovery: Linked package roots resolve through a target manifest, and the report must use the active target rather than the stable alias.
  Planned location: `environment/r3/d.rs` and package fixture directories with target manifests.
  Why instruction must not reveal it: Explaining the target manifest would collapse the symlinked-package portion to a path-normalization recipe.
- Discovery: Reuse is handle-based across unrelated edits, so a full rebuild fixes stale paths but breaks stable-definition observations.
  Planned location: `environment/r4/e.rs` and `environment/r5/f.rs`.
  Why instruction must not reveal it: The instruction should state the reuse outcome, not the handle allocation and epoch rules that make the task hard.

### Anti-trivialization verdict

| Check | Verdict | Reasoning |
|---|---|---|
| Disclosure-collapse | PASS | Honest behavior still leaves the solver to reconstruct slot lifetimes, source provenance, linked targets, and reuse state. |
| Hidden-instance | PASS | Six traces cover different stale-row families, not one hidden bad file. |
| Single-artifact repair | PASS | The verifier rebuilds the engine; editing one manifest or table cannot satisfy the runtime matrix. |
| Generalization | PASS | The repair must work across workspace, generated, package, missing-symbol, reuse, and mixed traces. |
| Prompt-honesty | PASS | The prompt can describe clean audit output without naming the failing modules or causes. |
| Cheating-vs-difficulty | PASS | Hardness comes from the state model, not from anti-cheating measures. |
| Mechanical-fix filter | PASS | Failures are semantic, not dependency or reward-footer issues. |
| Localized-fix | PASS | A successful patch needs coordinated changes in at least six Rust functions. |
| Oracle-locality | PASS | Oracle work is distributed across six neutral roots with a capped flipping-point contract. |
| Small declarative-cluster | PASS | There is no small table or config block that mirrors the prompt. |
| Grep-collapse | PASS | Fix-path names are opaque and avoid instruction nouns. |
| Pre-factored-helper | PASS | Helper names do not mirror prompt concepts, and decoys perform real non-fix work. |
| Recipe-discount | PASS | A broad cache flush is insufficient because reuse checks must survive. |
| Security-aura discount | PASS | The idea is not borrowing difficulty from security language. |
| Orthogonal-checklist | PASS | Requirements interact: invalidation, provenance, and handle reuse constrain each other. |
| Harness-discount | PASS | Docker and pytest are ordinary; the code-level repair is the hard part. |
| One-pass solvability | PASS | The first dispatch layer is not enough to identify every stale source. |
| Hard-only gate | PASS | The design requires professional-level debugging of a stateful code-indexer. |
| Discovery budget test | PASS | Four non-trivial discoveries are planned and not disclosed in instruction.md. |
| Instruction specificity test | PASS | The instruction is symptoms-only and avoids fix locations or algorithms. |
| Topology distribution test | PASS | Three topologies each require at least three coordinated locations. |

### Topology enumeration (3 candidate fix topologies)

- T1: Slot-replacement topology with downstream lookup and report changes.
  Locations: `environment/r1/b.rs::fold_b`, `environment/r4/e.rs::mote_e`, `environment/r5/f.rs::cast_f`.
  No single location suffices because replacing entries without lookup filtering still allows stale generated and linked rows, while lookup changes without report status can hide stale rows behind `ok` flags.
- T2: Provenance topology for generated roots and linked packages.
  Locations: `environment/r2/c.rs::emit_c`, `environment/r3/d.rs::lift_d`, `environment/r5/f.rs::cast_f`.
  No single location suffices because generated source and linked target provenance enter through different roots, and final stale classification must validate both.
- T3: Epoch and reuse topology preserving stable handles through unrelated edits.
  Locations: `environment/r0/a.rs::phase_a`, `environment/r1/b.rs::fold_b`, `environment/r4/e.rs::mote_e`.
  No single location suffices because event routing, entry replacement, and observation reuse each own one part of the invariant.

### Rubric axes

- Verifiable: PASS — pytest deterministically checks concrete JSON rows from the local Rust engine.
- Well-specified: PASS — one command, one output path, and report fields are public while cause and fix path stay hidden.
- Solvable: PASS — an expert can inspect traces and Rust modules and patch the system in a few hours.
- Difficult: PASS — the task requires stateful index invalidation, provenance, package-target, and reuse reasoning.
- Interesting: PASS — stale code-index results are a real IDE and monorepo productivity problem.
- Outcome-verified: PASS — tests grade report behavior rather than implementation style.

### Hardness axes

- Discover: The solver must inspect the Rust runner, traces, TypeScript fixtures, generated provenance, and package target manifests. Instruction.md alone does not reveal these mechanics.
- Synthesize: The fix spans event routing, entry replacement, generated provenance, package target resolution, lookup, and report classification.
- Diagnose: The prompt describes stale definition symptoms without naming slot removal, source maps, target manifests, or epoch bugs.
- Navigate coupling: A local full-flush fix conflicts with reuse, and a newest-entry-only fix conflicts with missing-symbol and provenance cases.
- Reason beyond training: The task is a project-specific editor-indexing failure, not a standard implementation recipe.

### Instruction completeness test

Can the agent solve this by reading only instruction.md without deeply engaging with the codebase? No. The prompt states what a clean audit means, but the solver must recover the trace DSL, fixture conventions, package target representation, and handle reuse semantics from the code and runtime behavior.

## Reviewer Appendix

### Implementation plan

Build a Rust CLI that reads six trace files and scans TypeScript fixture trees. The baseline appends new rows on root changes and lets stale entries remain selectable; it also mishandles provenance and reuse classification. The oracle will rewrite six neutral Rust modules so active roots replace only their own slot entries, generated rows carry current source paths, package aliases resolve to the active target, lookup rejects inactive rows, and report finalization marks stale observations.

The output is a JSON report at `/app/output/index-report.json`. Tests run the same script agents are asked to use, then inspect the report. A no-op baseline produces old paths and failed clean-status checks. A naive global rebuild fixes old paths but fails reuse checks in mixed traces.

### Proposed file inventory

- Root task files: `instruction.md`, `task.toml`, `output_contract.toml`, `construction_manifest.json`, `solution/solve.sh`, `tests/test.sh`, `tests/test_outputs.py`.
- Environment project files: `Dockerfile`, `Cargo.toml`, `README.md`, `src/main.rs`, `src/lib.rs`, `src/model.rs`, `src/io.rs`, `src/runner.rs`, `src/report.rs`.
- Fix-path modules: `r0/a.rs`, `r1/b.rs`, `r2/c.rs`, `r3/d.rs`, `r4/e.rs`, `r5/f.rs`.
- Decoys: `r6/g.rs`, `r7/h.rs`, `r8/i.rs`.
- Runner and traces: `scripts/run-matrix.sh`, `traces/alpha.trace`, `traces/beta.trace`, `traces/gamma.trace`, `traces/delta.trace`, `traces/epsilon.trace`, `traces/zeta.trace`.
- Fixtures: workspace, generated, schema, alias, and package files under `fixtures/alpha`, `fixtures/beta`, `fixtures/gamma`, `fixtures/delta`, `fixtures/epsilon`, and `fixtures/zeta`; total environment files exceed 50 excluding Dockerfile.

### Oracle notes

`solve.sh` should use deterministic literal rewrites for the six fix-path Rust modules. It should not touch decoy files. The replacement modules should add real logic for per-slot removal, active-root tracking, generated provenance, package target resolution, lookup filtering, reuse calculation, and stale classification. The oracle must not write a report or alter tests.

### Collapse audit

Stage: implementation-plan

Smallest plausible successful patch:
The smallest successful patch rewrites six Rust functions across neutral roots so the state table removes obsolete entries by slot, records current roots, resolves generated and linked provenance, selects only active entries, preserves handles for unchanged definitions, and marks unexpected found/missing rows as stale.

Likely editable frontier:
- `environment/r0/a.rs`
- `environment/r1/b.rs`
- `environment/r2/c.rs`
- `environment/r3/d.rs`
- `environment/r4/e.rs`
- `environment/r5/f.rs`

Requirement-to-file map:
- Clean report command -> `scripts/run-matrix.sh`, `src/main.rs`, `src/runner.rs`
- Live workspace definition rows -> `r1/b.rs`, `r4/e.rs`
- Current generated source rows -> `r2/c.rs`, `r5/f.rs`
- Active linked package target rows -> `r3/d.rs`, `r4/e.rs`
- Missing symbol behavior -> `r4/e.rs`, `r5/f.rs`
- Reuse across unrelated edits -> `r1/b.rs`, `r4/e.rs`

Oracle estimated complexity: 120-180 lines of non-boilerplate logic.

Red flags:
- Avoid a report-writing oracle.
- Avoid instruction wording that says "invalidate by slot" or names target manifests.
- Avoid comments in fix-path files that use correctional vocabulary.

Residual hardness:
After the file tree is visible, the solver still has to understand how trace events compose, why stale rows remain selectable, why a broad clear breaks reuse, and how generated and linked provenance flow into observations. The neutral module names prevent obvious grep-based localization.

Collapse verdict: PASS

### Naming-pass record

**Instruction nouns extracted:**
index, harness, definition, locations, rename, module, package, sequences, bash, scripts, output, report, fixtures, JSON, cases, name, observations, label, symbol, path, source, line, epoch, target, audit

**Renames during drafting:**
- `replace_workspace_slot` -> `fold_b`: The original symbol reused instruction nouns about workspace and replacement, so it was replaced with an opaque name.
- `resolve_generated_source` -> `emit_c`: The original symbol collided with instruction nouns about generated modules and source paths.
- `refresh_package_link` -> `lift_d`: The original symbol exposed the linked-package repair path.

**Test names audited:**
- `test_t01_flow`
- `test_t02_flow`
- `test_t03_flow`
- `test_t04_flow`
- `test_t05_flow`
- `test_t06_flow`
- `test_t07_flow`
- `test_t08_flow`
- `test_t09_flow`
- `test_t10_flow`
- `test_t11_flow`
- `test_t12_flow`

**Concentration math:**
- Total tests across `flipping_point_contract`: 12
- Per location:
  - A (`r0/a.rs`): 2/12 = 0.16666666666666666
  - B (`r1/b.rs`): 2/12 = 0.16666666666666666
  - C (`r2/c.rs`): 2/12 = 0.16666666666666666
  - D (`r3/d.rs`): 2/12 = 0.16666666666666666
  - E (`r4/e.rs`): 2/12 = 0.16666666666666666
  - F (`r5/f.rs`): 2/12 = 0.16666666666666666
- Cap: 0.5. Max ratio observed: 0.16666666666666666. Status: PASS

### Per-test feasibility pre-check

- Test: `test_t01_flow`
  Checks: Alpha after-state path uses the current workspace tree.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW.
- Test: `test_t02_flow`
  Checks: Beta generated observation uses current generated file and source.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW.
- Test: `test_t03_flow`
  Checks: Gamma package observation follows active target.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW.
- Test: `test_t04_flow`
  Checks: Delta generated observation keeps reuse through unrelated workspace edit.
  Valid approaches: 2+.
  Chain-dependent: no; the trace sets preconditions.
  Feasibility risk: LOW.
- Test: `test_t05_flow`
  Checks: Epsilon removed symbol is missing.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW.
- Test: `test_t06_flow`
  Checks: Zeta mixed trace keeps both package and workspace after-states live.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW.
- Test: `test_t07_flow`
  Checks: All cases are clean.
  Valid approaches: 2+.
  Chain-dependent: no; summarizes independent cases.
  Feasibility risk: LOW.
- Test: `test_t08_flow`
  Checks: No after-state path remains under earlier workspace roots.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW.
- Test: `test_t09_flow`
  Checks: Epochs are monotonic and changed rows do not claim reuse.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW.
- Test: `test_t10_flow`
  Checks: Stable rows keep reuse when other slots change.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW.
- Test: `test_t11_flow`
  Checks: Path/source conventions match the public contract.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW.
- Test: `test_t12_flow`
  Checks: Two consecutive matrix runs are deterministic.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW.
