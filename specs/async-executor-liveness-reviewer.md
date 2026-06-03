### Decision
GO — Attempt 1. The design keeps the prompt symptoms-only while distributing the Rust repair across admission, queue draining, branch filtering, recovery, and artifact emission roots.

### Metadata
- Task name: async-executor-liveness
- Title: Executor Audit Liveness
- Category: debugging
- Languages: ["Rust", "shell"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["rust", "async", "executor", "debugging", "cancellation"]
- Milestones: 0

### Discovery budget
- Discovery: Plan rows create a parent graph whose accepted child depth must be derived from the surviving ancestor chain.
  Planned location: environment/read_h/parse.rs and environment/core_a/core.rs
  Why instruction must not reveal it: Naming the ancestry propagation rule as the cause would point directly at the repair path and collapse diagnosis.
- Discovery: Bounded lane pressure is a spill-forward process, not a drop-on-overflow process, and accepted turns come from the drain cycle.
  Planned location: environment/book_b/book.rs and environment/drive_g/drive.rs
  Why instruction must not reveal it: Stating spill-forward scheduling would give the core algorithm and turn repair away.
- Discovery: Cancelled branch names must exclude descendants as well as the named row, and this interacts with duplicate task admission.
  Planned location: environment/gate_c/gate.rs and environment/host_d/host.rs
  Why instruction must not reveal it: The instruction should say cancelled branches stay out of the trace, not specify the internal descendant walk.
- Discovery: The JSON trace, JSONL ledger, and text journal are generated through different emit paths that must receive the same ordered records.
  Planned location: environment/flow_e/flow.rs and environment/types_f/serde.rs
  Why instruction must not reveal it: If the prompt names the divergent emitter as the issue, the solver can patch outputs without understanding runner state.

### Anti-trivialization verdict
All 21 checks PASS. The task is not a hidden-instance search, one-artifact repair, small table update, prompt-grep patch, or standard recipe. The future solver must recover at least four code/runtime discoveries and coordinate at least three roots in every viable topology. The instruction specificity remains symptoms-only; the final hard classification must be confirmed empirically using the announced Hard -> Medium -> Easy order once platform model results exist.

### Topology enumeration (3 candidate fix topologies)
1. Admission-and-drain topology: environment/core_a/core.rs::op_a, environment/book_b/book.rs::fold_b, environment/drive_g/drive.rs::drive_g. No single location suffices because admission, capacity spill, and orchestration each control different failing observations.
2. Branch-and-depth topology: environment/gate_c/gate.rs::mark_c, environment/host_d/host.rs::bind_d, environment/core_a/core.rs::R0. No single location suffices because exclusion state, transferred rows, and record shape must agree for child relationships.
3. Artifact-consistency topology: environment/flow_e/flow.rs::emit_e, environment/types_f/serde.rs::row_json, environment/drive_g/drive.rs::drive_g. No single location suffices because all generated surfaces must receive the same ordered records.

### Rubric axes
- Verifiable: PASS — deterministic local pytest checks rebuild and run the Rust project, then compare outputs to Python-derived expectations.
- Well-specified: PASS — the instruction gives command, output path, and observable consistency contract without naming internals.
- Solvable: PASS — expert Rust debugging in a few hours; no external service or giant rewrite.
- Difficult: PASS — requires coordinating scheduling, cancellation, hierarchy, and artifact invariants across modules.
- Interesting: PASS — executor liveness under cancellation and bounded pressure is a realistic systems reliability problem.
- Outcome-verified: PASS — tests grade generated behavior and artifacts, not process.

### Hardness axes
- Discover: The solver must inspect plan parsing, state propagation, queue draining, and generated artifacts; the instruction alone is insufficient.
- Synthesize: The answer spans admission, scheduling, filtering, recovery, and output emission.
- Diagnose: The prompt states stalled/inconsistent audit symptoms, not the missing internal operations.
- Navigate coupling: Queue changes affect turns and artifact order; branch changes affect child depth and duplicate filtering.
- Reason beyond training: The system is a bespoke deterministic executor simulator, not a stock async runtime exercise.

### Instruction completeness test
Can the agent solve this by reading ONLY instruction.md without deeply engaging with the codebase? No. The instruction names the desired audit behavior, but the solver must recover the plan grammar, local runner semantics, and output generation paths from code and runtime behavior.

## Reviewer Appendix

### Implementation plan
Build a local Rust project with a binary `executor-ctl` and scripts that run six plan files. The baseline implementation should compile and run but mishandle multiple interacting semantics: drop overflow rows, let some removed descendants through, lose depth across child rows, duplicate repeated logical rows, or generate a side-channel artifact from a differently ordered list. The verifier recomputes expected rows from the plan files and compares every generated surface.

The oracle should rewrite the fix roots with deterministic logic: parse rows into a parent graph, compute removed descendants, drain capacity-limited lane backlogs by turn, suppress duplicates by task id, propagate parent and depth, and emit JSONL/text from the final ordered row list. The patch should be substantive and distributed rather than a one-file replacement.

### Proposed file inventory
- `instruction.md` — public symptoms-only prompt.
- `task.toml` — Edition 2 hard/offline metadata.
- `output_contract.toml` — local output schema declaration.
- `construction_manifest.json` — manifest for collapse checks.
- `environment/Dockerfile` — pinned Rust/Python image with pytest installed.
- `environment/Cargo.toml` — no external crates.
- `environment/src/main.rs` — binary entrypoint.
- `environment/src/lib.rs` — module wiring.
- `environment/core_a/core.rs` — admission state.
- `environment/book_b/book.rs` — bounded ordering.
- `environment/gate_c/gate.rs` — exclusion checks.
- `environment/host_d/host.rs` — transferred state.
- `environment/flow_e/flow.rs` — JSONL/text emission.
- `environment/types_f/types.rs` — shared structs.
- `environment/types_f/serde.rs` — manual JSON serialization.
- `environment/drive_g/drive.rs` — case runner.
- `environment/read_h/parse.rs` — plan parser.
- `environment/spill_i/spill.rs` — decoy ordering helper.
- `environment/mirror_j/mirror.rs` — decoy formatting helper.
- `environment/note_k/note.rs` — neutral helper.
- `environment/scripts/run-matrix.sh` — matrix command.
- `environment/scripts/run-one.sh` — one-case command.
- `environment/scripts/clean-room.sh` — cleanup helper.
- `environment/data/cases/{amber,cobalt,drake,ember,flint,graphite}.plan` — inputs.
- `environment/docs/ARCHITECTURE.md` and `environment/docs/OPERATIONS.md` — neutral context.
- `tests/test.sh` — offline pytest runner.
- `tests/test_outputs.py` — 12 tests.
- `solution/solve.sh` — oracle.

### Oracle notes
The oracle should replace or patch `core_a/core.rs`, `book_b/book.rs`, `gate_c/gate.rs`, `host_d/host.rs`, `flow_e/flow.rs`, and `drive_g/drive.rs`. It should keep symbol names from the manifest. The fix must compute expected behavior from plan inputs at runtime and write generated artifacts; it must not copy test literals or precomputed answers.

### Collapse audit
Stage: implementation-plan

Smallest plausible successful patch:
The smallest successful patch repairs duplicate-aware admission, capacity-limited spill-forward ordering, removed-descendant checks, parent/depth propagation, and side-channel emission agreement across multiple Rust roots.

Likely editable frontier:
- `core_a/core.rs`
- `book_b/book.rs`
- `gate_c/gate.rs`
- `host_d/host.rs`
- `flow_e/flow.rs`
- `drive_g/drive.rs`

Requirement-to-file map:
- Matrix completes and writes the audit -> `drive_g/drive.rs`, `scripts/run-matrix.sh`
- No pending records and clean status -> `drive_g/drive.rs`, `core_a/core.rs`
- Bounded queues preserve work -> `book_b/book.rs`
- Cancelled branches stay out -> `gate_c/gate.rs`, `host_d/host.rs`
- Parent/depth relationships are preserved -> `core_a/core.rs`, `host_d/host.rs`
- Ledger and journal agree with JSON -> `flow_e/flow.rs`, `types_f/serde.rs`

Oracle estimated complexity: 140+ lines of non-boilerplate logic.

Red flags:
- The instruction must not enumerate per-case expected task ids or accepted turns.
- The environment must not contain golden outputs or comments saying which function is wrong.

Residual hardness:
After all visible files exist, the solver still has to run scenarios, infer plan semantics, trace state through distinct modules, and coordinate fixes so that generated JSON and side-channel artifacts all agree. The opaque roots and decoys reduce grep-based targeting.

Collapse verdict: PASS

### Naming-pass record

**Instruction nouns extracted:**
Rust, workload, runner, audit, queues, branches, child, work, matrix, output, JSON, cases, inputs, array, amber, cobalt, drake, ember, flint, graphite, name, ok, finished, pending, trace, ledger, journal, records, record, case, task, parent, depth, lane, turn, JSONL, file, text, rows, relationships

**Renames during drafting:**
- `accept_record` -> `op_a`: the original name contained the instruction noun record.
- `fair_lane_drain` -> `fold_b`: the original name contained the instruction noun lane.
- `branch_gate` -> `mark_c`: the original name contained the instruction noun branches.
- `emit_journal` -> `emit_e`: the original name contained the instruction noun journal.

**Test names audited:**
- test_a0
- test_b1
- test_c2
- test_d3
- test_e4
- test_f5
- test_g6
- test_h7
- test_i8
- test_j9
- test_k0
- test_l1

**Concentration math:**
- Total tests across `flipping_point_contract`: 12
- Per location:
  - A (`core_a/core.rs`): 3/12 = 0.25
  - B (`book_b/book.rs`): 3/12 = 0.25
  - C (`gate_c/gate.rs`): 3/12 = 0.25
  - D (`flow_e/flow.rs`): 3/12 = 0.25
- Cap: 0.5. Max ratio observed: 0.25. Status: PASS

### Per-test feasibility pre-check
- Test: test_a0
  Checks: Matrix command emits all cases with clean status and nonempty traces.
  Valid approaches: 2+.
  Chain-dependent: no — it checks matrix-level generated behavior.
  Feasibility risk: LOW
- Test: test_b1
  Checks: Direct binary output for one case agrees with matrix output.
  Valid approaches: 2+.
  Chain-dependent: no — the direct command creates its own output.
  Feasibility risk: LOW
- Test: test_c2
  Checks: Amber records and parent/depth relationships match plan semantics.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW
- Test: test_d3
  Checks: Cobalt pressure case preserves overflow as delayed turns.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW
- Test: test_e4
  Checks: Drake removed branches and descendants are absent.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW
- Test: test_f5
  Checks: Ember combines nested rows with branch exclusion.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW
- Test: test_g6
  Checks: Flint accepts duplicate logical rows only once.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW
- Test: test_h7
  Checks: Graphite mixed scenario matches expected records.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW
- Test: test_i8
  Checks: Ledger JSONL files match JSON trace.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW
- Test: test_j9
  Checks: Text journal files match JSON trace.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW
- Test: test_k0
  Checks: Repeated matrix runs are deterministic.
  Valid approaches: 2+.
  Chain-dependent: no — each run resets outputs.
  Feasibility risk: LOW
- Test: test_l1
  Checks: At least one pressure case has delayed accepted turns derived from capacity.
  Valid approaches: 2+.
  Chain-dependent: no.
  Feasibility risk: LOW
