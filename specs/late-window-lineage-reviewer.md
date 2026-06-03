### Decision
GO — Attempt 1. The Rust data-processing seed has enough distributed topology, a symptoms-only prompt path, and a committed opaque construction manifest.

### Metadata
- Task name: late-window-lineage
- Title: Late Window Lineage
- Category: data-processing
- Languages: [Rust, shell]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: [rust, streaming, replay, aggregation, checkpoints]
- Milestones: 0

### Discovery budget
- Discovery: The restarted path reconstructs part of its state from persisted rows while the uninterrupted path keeps in-memory markers, and the two authorities are not equivalent.
  Planned location: `environment/src/d3/host.rs` and runtime state files under `/app/state`.
  Why instruction must not reveal it: It would point directly at the recovery state repair.
- Discovery: Rows that arrive after a case has already emitted a value need stable correction identity tied to ordered input ids, not incidental processing order.
  Planned location: `environment/src/c2/gate.rs` and `environment/src/f5/types.rs`.
  Why instruction must not reveal it: It would turn diagnosis into implementing a named identity recipe.
- Discovery: The retained-row combination pass reorders rows differently from the direct pass, so lineage order has to come from row semantics rather than file order.
  Planned location: `environment/src/b1/book.rs` and runtime traces.
  Why instruction must not reveal it: Naming the ordering authority would make the edit frontier obvious.
- Discovery: Partition-local progress must not suppress a late update from a different partition that shares the same key/window surface.
  Planned location: `environment/src/a0/core.rs` and mixed partition scenario inputs.
  Why instruction must not reveal it: It is a core diagnosis step that must come from code and case comparison.

### Anti-trivialization verdict
- Disclosure-collapse: PASS — honest output agreement does not disclose the internal state authorities.
- Hidden-instance: PASS — several cases exercise one general implementation.
- Single-artifact repair: PASS — no report, manifest, or fixture replacement can satisfy derived tests.
- Generalization: PASS — duplicate replay, late rows, retained state, ordering, and partition isolation all matter.
- Prompt-honesty: PASS — the prompt can state the audit contract without cause-level internals.
- Cheating-vs-difficulty: PASS — anti-cheating is support, not the hard part.
- Mechanical-fix filter: PASS — the core is Rust state behavior, not CI setup.
- Localized-fix: PASS — manifest distributes the frontier across five roots.
- Oracle-locality: PASS — planned oracle is multi-file substantive code.
- Small declarative-cluster: PASS — not a table or policy knob.
- Grep-collapse: PASS — public nouns are banned from fix-path symbols and tests use opaque names.
- Pre-factored-helper: PASS — helper names are opaque, not contract-shaped.
- Recipe-discount: PASS — the recovery invariant is bespoke.
- Security-aura discount: PASS — not a security-flavored task.
- Orthogonal-checklist: PASS — local repairs interact and can regress each other.
- Harness-discount: PASS — Docker and shell are not counted as hardness.
- One-pass solvability: PASS — reading the shell entrypoint will not identify the root cause.
- Hard-only gate: PASS — residual work is professional stateful debugging.
- Discovery budget test: PASS — four concrete discoveries listed.
- Instruction specificity test: PASS — planned instruction is symptoms-only.
- Topology distribution test: PASS — three distributed topologies listed below.

### Topology enumeration (3 candidate fix topologies)
- T1: Repair around canonical folded rows before emission.
  Locations: `src/a0/core.rs::fold_a`, `src/b1/book.rs::merge_b`, `src/c2/gate.rs::mark_c`, `src/e4/flow.rs::push_e`.
  Why no single location suffices: canonical folding alone does not restore markers or stabilize serialized identity.
- T2: Repair around restart-state reconstruction plus stable emission.
  Locations: `src/d3/host.rs::load_d`, `src/c2/gate.rs::mark_c`, `src/e4/flow.rs::push_e`.
  Why no single location suffices: state loading cannot repair direct-path ordering or output identity by itself.
- T3: Repair by enforcing a shared row-normalization boundary.
  Locations: `src/b1/book.rs::merge_b`, `src/a0/core.rs::fold_a`, `src/d3/host.rs::load_d`, `src/f5/types.rs::R2`.
  Why no single location suffices: consumers still need to respect canonical order and duplicate markers.

### Rubric axes
- Verifiable: PASS — deterministic pytest over JSON output.
- Well-specified: PASS — command, path, schema, and agreement properties can be stated succinctly.
- Solvable: PASS — an expert can trace and repair the Rust engine in a few hours.
- Difficult: PASS — requires stateful diagnosis, not transcription.
- Interesting: PASS — replay-correct late-event output is a real streaming-system concern.
- Outcome-verified: PASS — tests judge output behavior, not the exact patch.

### Hardness axes
- Discover: PASS — the solver must find hidden state, ordering, and identity authorities in code/runtime behavior.
- Synthesize: PASS — parsing, folding, retained state, gating, and emission must coordinate.
- Diagnose: PASS — the public prompt states symptoms, not causes.
- Navigate coupling: PASS — duplicate suppression, late corrections, and lineage identity affect each other.
- Reason beyond training: PASS — the task is a bespoke replay invariant rather than a stock window implementation.

### Instruction completeness test
Can the agent solve this by reading ONLY instruction.md without deeply engaging with the codebase? No. The instruction describes the output contract and observed drift but not which of the direct, replay, retained-state, ordering, or emission surfaces is wrong.

## Reviewer Appendix
Human review only during authoring. Do not use this appendix for Step 2b drafting until discovery-budget confirmation after the task files exist.

### Implementation plan
The environment will be a small Rust project that reads six input cases and emits an audit comparing direct and restarted processing. The broken draft should look plausible: it can group rows and write JSON, but restart-sensitive cases diverge because retained state, duplicate markers, row ordering, and correction identity are not reconciled. The oracle will repair the shared state path rather than hardcoding outputs.

### Proposed file inventory
- `instruction.md` — public prompt.
- `task.toml` — metadata.
- `output_contract.toml` — declared output.
- `construction_manifest.json` — manifest mirror.
- `environment/Dockerfile` — image.
- `environment/Cargo.toml` — Rust manifest.
- `environment/README.md`, `environment/docs/architecture.md`, `environment/docs/operations.md` — neutral context.
- `environment/scripts/run-matrix.sh` — audit command.
- `environment/src/main.rs`, `environment/src/lib.rs` — entry and module root.
- `environment/src/{a0,b1,c2,d3,e4}/...` — fix-path modules.
- `environment/src/{f5,g6,h7,i8,j9,k1,l2,m3}/...` — shared, decoy, loader, runner, and helper modules.
- `environment/data/cases/{aurora,boreal,cirrus,drift,ember,flux}.csv` — input cases.
- `solution/solve.sh` — oracle.
- `tests/test.sh`, `tests/test_outputs.py` — verifier.

### Oracle notes
The oracle should rewrite the fix-path Rust modules with generalized logic: canonical row grouping, deterministic retained-row merging, replay-aware emission markers, state loading from persisted rows, and stable JSON output. It must not write a precomputed report or edit decoys.

### Collapse audit
Stage: implementation-plan

Smallest plausible successful patch:
The smallest patch updates row folding, retained-row combination, emission gating, state loading, and output writing across several modules.

Likely editable frontier:
- `src/a0/core.rs`
- `src/b1/book.rs`
- `src/c2/gate.rs`
- `src/d3/host.rs`
- `src/e4/flow.rs`

Requirement-to-file map:
- direct and replay totals agree -> `a0/core.rs`, `b1/book.rs`
- duplicate replay is suppressed -> `c2/gate.rs`, `d3/host.rs`
- correction identity is stable -> `c2/gate.rs`, `e4/flow.rs`, `f5/types.rs`
- lineage order is stable -> `b1/book.rs`, `c2/gate.rs`
- repeated restarted runs are identical -> `d3/host.rs`, `e4/flow.rs`

Oracle estimated complexity: 120-180 non-boilerplate lines.

Red flags:
- Schema prose in the instruction must stay compact enough not to trip RC6 as spec-complete.
- Central orchestration must avoid referencing every manifest symbol in one file.

Residual hardness:
After the file tree is visible, the solver still has to determine which state surface defines correction identity and how to preserve legitimate late changes while suppressing replay duplicates.

Collapse verdict: PASS

### Naming-pass record

**Instruction nouns extracted:**
engine, app, audit, output, scenarios, script, json, cases, aurora, boreal, cirrus, drift, ember, flux, case, name, ok, direct, replay, totals, corrections, repeat, entries, input, run, paths, partition, window, key, value, fields, id, lineage, array, ids, order, records

**Renames during drafting:**
- `resolve_lineage` -> `mark_c`: collided with instruction noun `lineage`.
- `checkpoint_state` -> `load_d`: revealed an internal state surface.
- `test_replay_totals` -> `test_r01`: collided with instruction nouns.

**Test names audited:**
- `test_r01`
- `test_r02`
- `test_r03`
- `test_r04`
- `test_r05`
- `test_r06`
- `test_r07`
- `test_r08`
- `test_r09`
- `test_r10`
- `test_r11`
- `test_r12`

**Concentration math:**
- Total tests across `flipping_point_contract`: 12
- Per location:
  - A (`src/a0/core.rs`): 3/12 = 0.25
  - B (`src/b1/book.rs`): 3/12 = 0.25
  - C (`src/c2/gate.rs`): 3/12 = 0.25
  - D (`src/d3/host.rs`): 3/12 = 0.25
  - E (`e4/flow.rs`): 3/12 = 0.25
- Cap: 0.5. Max ratio observed: 0.25. Status: PASS

### Per-test feasibility pre-check
- Test: `test_r01`; Checks: command and top-level case coverage; Valid approaches: 2+; Chain-dependent: no; Feasibility risk: LOW.
- Test: `test_r02`; Checks: clean case status and required surfaces; Valid approaches: 2+; Chain-dependent: no; Feasibility risk: LOW.
- Test: `test_r03`; Checks: direct totals from input rows; Valid approaches: 2+; Chain-dependent: no; Feasibility risk: LOW.
- Test: `test_r04`; Checks: replay totals match direct totals; Valid approaches: 2+; Chain-dependent: no; Feasibility risk: LOW.
- Test: `test_r05`; Checks: repeated restarted correction IDs; Valid approaches: 2+; Chain-dependent: no; Feasibility risk: LOW.
- Test: `test_r06`; Checks: duplicate suppression without loss; Valid approaches: 2+; Chain-dependent: no; Feasibility risk: LOW.
- Test: `test_r07`; Checks: lineage order from row semantics; Valid approaches: 2+; Chain-dependent: no; Feasibility risk: LOW.
- Test: `test_r08`; Checks: partition-local independence; Valid approaches: 2+; Chain-dependent: no; Feasibility risk: LOW.
- Test: `test_r09`; Checks: compaction-shaped case stability; Valid approaches: 2+; Chain-dependent: no; Feasibility risk: LOW.
- Test: `test_r10`; Checks: persisted state does not duplicate old records; Valid approaches: 2+; Chain-dependent: no; Feasibility risk: LOW.
- Test: `test_r11`; Checks: correction ID binding; Valid approaches: 2+; Chain-dependent: no; Feasibility risk: LOW.
- Test: `test_r12`; Checks: deterministic ordering across invocations; Valid approaches: 2+; Chain-dependent: no; Feasibility risk: LOW.
