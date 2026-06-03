### Decision
GO — Attempt 1. The design keeps the prompt symptoms-only while distributing the Rust repair across admission, queue draining, branch filtering, recovery, and artifact emission roots.

### Metadata
- version: 2
- Task name: async-executor-liveness
- Title: Executor Audit Liveness
- Category: debugging
- Languages: ["Rust", "shell"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["rust", "async", "executor", "debugging", "cancellation"]
- Milestones: 0

## Authoring Brief
This file is the only drafting input for Step 2b. Do not use the reviewer appendix until the discovery-budget confirmation after the task files exist.

### Public contract
The task is a standard single-step Rust debugging task. The agent-facing instruction should say that the Rust workload runner under `/app` sometimes leaves its audit stalled or inconsistent when bounded queues, cancelled branches, and child work are mixed. The requested end state is that `bash /app/scripts/run-matrix.sh` completes and writes `/app/output/executor-audit.json` from the current shipped case inputs rather than a canned report.

The output is a JSON object with a top-level cases array for amber, cobalt, drake, ember, flint, and graphite. Each case reports name, ok, finished, pending, trace, ledger, and journal. Trace is the ordered list of accepted work records; every record carries case, task, parent, depth, lane, and turn. Ledger points to a JSONL file with the same records in the same order. Journal points to a whitespace-delimited text file with the same rows in the order case task parent depth lane turn. The audit is clean when every case finishes, has no pending records, has ok true, preserves parent/depth relationships for child work, keeps cancelled branches out of the accepted trace, and the JSON, ledger, and journal agree.

### Failure topology
The built environment should model a small local async-style executor rather than depend on external crates. The visible symptom is liveness and consistency drift: some runs drop overflow work, let cancelled descendants leak, misreport child depth, or emit side-channel rows that do not match the JSON trace. These symptoms must arise from interacting state transitions rather than a single malformed table.

The hard part should be reconstructing the runner's state model from code and runtime output. Admission, queue draining, branch exclusion, recovered accepted-state handling, and artifact emission should each be plausible local suspects, and fixing only one should leave separate tests failing.

### Environment shape
Create a Rust project under `/app` with no external Rust crates. Use opaque module roots such as `core_a/`, `book_b/`, `gate_c/`, `host_d/`, `flow_e/`, `drive_g/`, `read_h/`, plus normal `src/`, `scripts/`, and `data/cases/` directories. The root `src/lib.rs` may include modules from those roots via `#[path = ...]` so the fix-path files live in distinct top-level directories.

Case plans under `data/cases/` should define root rows, child rows, lane assignments, turn arrivals, capacity, and branch removals. Helper and documentation files should look like normal repository context, not hints. Add at least two decoy helper modules that rhyme structurally with fix-path modules but do non-fix work.

### Required artifacts
- `instruction.md` with a concise symptoms-only public contract and absolute paths.
- `task.toml` with `version = "2.0"`, anonymous author fields, `difficulty = "hard"`, `category = "debugging"`, `codebase_size = "small"`, `number_of_milestones = 0`, 3-6 descriptive tags, integer resource/time fields, and `[environment].allow_internet = false`.
- `output_contract.toml` at task root declaring `/app/output/executor-audit.json` as user-visible and the tests/scripts as internal harness files.
- `construction_manifest.json` mirroring the manifest below verbatim.
- `environment/Dockerfile` pinned by digest, with verifier dependencies installed in the image and no runtime dependency install in `tests/test.sh`.
- A 20+ file Rust environment with case plans, scripts, source modules, decoys, and documentation.
- `tests/test.sh` using the offline standard skeleton: create `/logs/verifier`, guard `$PWD = "/"`, run preinstalled pytest with CTRF output, write reward.txt, and exit with the pytest status.
- `tests/test_outputs.py` with 12 deterministic pytest tests named opaquely (`test_a0` through `test_l1`) and informative docstrings. Expected traces must be re-derived in Python from the plan files, not read from golden artifacts.
- `solution/solve.sh` with `set -euo pipefail` that performs a substantive deterministic Rust repair across at least four fix roots and clears the full verifier.

### Test plan
- `test_a0`: run the matrix command and verify the combined object has all six cases in order, each with clean status fields and a nonempty trace.
- `test_b1`: run one direct case through the release binary and confirm it agrees with the same case inside the matrix output.
- `test_c2`: verify amber's expected accepted rows and parent/depth relationships.
- `test_d3`: verify cobalt's bounded pressure preserves overflow work instead of dropping it.
- `test_e4`: verify drake excludes removed branches and descendants.
- `test_f5`: verify ember combines branch exclusion with nested child rows.
- `test_g6`: verify flint accepts duplicate logical rows only once.
- `test_h7`: verify graphite covers mixed pressure, descendants, and late arrivals.
- `test_i8`: verify every ledger JSONL file exactly matches the JSON trace.
- `test_j9`: verify every text journal exactly matches the JSON trace.
- `test_k0`: run the matrix twice and verify deterministic trace/side-channel agreement.
- `test_l1`: directly inspect at least one pressure case for delayed accepted turns derived from capacity limits.

Each test accepts any implementation that produces the correct observable records and artifacts; none requires a specific source layout beyond the committed local project interface.

### Drafting guardrails
Keep the instruction honest and readable, but do not name the internal module roots, function names, algorithms, or exact defect causes. Do not use instruction nouns as fix-path symbols or path tokens. Do not place expected output files or golden traces under `environment/`; tests must compute expectations from plan inputs. Avoid comments near fix-path code that say bug, fix, wrong, expected, or similar correctional vocabulary.

### Triviality Ledger
- A canned `/app/output/executor-audit.json` is blocked because the verifier deletes and regenerates outputs through both the matrix script and direct binary runs, then recomputes expected rows from `data/cases/`.
- A one-file queue loop patch is blocked because branch exclusion, parent/depth propagation, and side-channel emitters are tested independently.
- A branch-only patch is blocked because bounded pressure cases require delayed accepted turns, and duplicate rows are checked separately.
- A side-channel-only patch is blocked because the JSON trace itself must match expected records before ledger and journal agreement is evaluated.
- A prompt-grep patch is blocked by opaque fix-path roots and symbols plus decoy modules that have similar shapes but do non-fix work.

### Per-gate Pitfall Inventory
- RC1/RC7: avoid a tiny revert or table edit; `solve.sh` must add substantive logic across admission, scheduling, filtering, state transfer, and emission with at least 80 semantic-diff lines.
- RC2/CR7: keep file roots and symbols opaque (`core_a`, `book_b`, `op_a`, `fold_b`, etc.) and avoid instruction nouns on the fix path.
- RC3/RC4/RC5: tests must assert computed records and artifact equality; do not read expected values from environment golden files.
- RC6/GX6/GX9/GX10: instruction must describe symptoms and output contract without causal chains, algorithm names, per-case answer values, or polarity contradictions.
- GX1/GX3: environment comments near changed lines should be mechanical or absent; oracle changes must be substantive rather than comment/whitespace padding.
- CR1/CR2/CR8: mirror the construction manifest exactly, declare at least four distinct fix locations across top-level roots, and avoid any non-fix visible file referencing more than two manifest symbols.
- Static checks: use the offline test skeleton, digest-pinned Dockerfile, integer timeouts/resources, `allow_internet = false`, 20+ real environment files, and no runtime installs in `tests/test.sh`.
- NOP/oracle: NOP must fail on missing or incorrect generated artifacts while the oracle must rebuild and pass deterministically without network, randomness, or sleeps.

### Initial Draft Commitments
- `tasks/async-executor-liveness/instruction.md` — symptoms-only task prompt.
- `tasks/async-executor-liveness/task.toml` — Edition 2 metadata with offline runtime.
- `tasks/async-executor-liveness/output_contract.toml` — local output declaration.
- `tasks/async-executor-liveness/construction_manifest.json` — manifest copied from this spec.
- `tasks/async-executor-liveness/environment/Dockerfile` — pinned Rust/Python verifier image.
- `tasks/async-executor-liveness/environment/Cargo.toml` — local Rust project manifest.
- `tasks/async-executor-liveness/environment/src/main.rs` — binary entrypoint.
- `tasks/async-executor-liveness/environment/src/lib.rs` — module wiring.
- `tasks/async-executor-liveness/environment/core_a/core.rs` — admission and row state.
- `tasks/async-executor-liveness/environment/book_b/book.rs` — bounded ordering root.
- `tasks/async-executor-liveness/environment/gate_c/gate.rs` — exclusion decision root.
- `tasks/async-executor-liveness/environment/host_d/host.rs` — transferred state root.
- `tasks/async-executor-liveness/environment/flow_e/flow.rs` — line-oriented emission root.
- `tasks/async-executor-liveness/environment/types_f/types.rs` — shared structs.
- `tasks/async-executor-liveness/environment/types_f/serde.rs` — hand-written JSON serialization.
- `tasks/async-executor-liveness/environment/drive_g/drive.rs` — one-case coordination.
- `tasks/async-executor-liveness/environment/read_h/parse.rs` — case-plan parser.
- `tasks/async-executor-liveness/environment/spill_i/spill.rs` — decoy helper.
- `tasks/async-executor-liveness/environment/mirror_j/mirror.rs` — decoy helper.
- `tasks/async-executor-liveness/environment/note_k/note.rs` — neutral helper.
- `tasks/async-executor-liveness/environment/scripts/run-matrix.sh` — documented matrix command.
- `tasks/async-executor-liveness/environment/scripts/run-one.sh` — direct case helper.
- `tasks/async-executor-liveness/environment/scripts/clean-room.sh` — output cleanup helper.
- `tasks/async-executor-liveness/environment/data/cases/amber.plan` — scenario input.
- `tasks/async-executor-liveness/environment/data/cases/cobalt.plan` — scenario input.
- `tasks/async-executor-liveness/environment/data/cases/drake.plan` — scenario input.
- `tasks/async-executor-liveness/environment/data/cases/ember.plan` — scenario input.
- `tasks/async-executor-liveness/environment/data/cases/flint.plan` — scenario input.
- `tasks/async-executor-liveness/environment/data/cases/graphite.plan` — scenario input.
- `tasks/async-executor-liveness/environment/docs/ARCHITECTURE.md` — neutral project context.
- `tasks/async-executor-liveness/environment/docs/OPERATIONS.md` — neutral run context.
- `tasks/async-executor-liveness/tests/test.sh` — offline verifier runner.
- `tasks/async-executor-liveness/tests/test_outputs.py` — pytest verifier.
- `tasks/async-executor-liveness/solution/solve.sh` — oracle repair.

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: core_a/core.rs
  symbol: op_a
  kind: function
  signature: pub fn op_a(a: &mut S0, b: R0) -> Result<(), E0>
  purpose: Adds one generated row to mutable state after local checks.
- path: book_b/book.rs
  symbol: fold_b
  kind: function
  signature: pub fn fold_b(a: &[R0], b: usize) -> Vec<R0>
  purpose: Orders and drains rows through capacity-limited groups.
- path: gate_c/gate.rs
  symbol: mark_c
  kind: function
  signature: pub fn mark_c(a: &S1, b: &R0) -> bool
  purpose: Decides whether a row survives local exclusion state.
- path: host_d/host.rs
  symbol: bind_d
  kind: function
  signature: pub fn bind_d(a: &mut S2, b: R1) -> Result<R2, E0>
  purpose: Transfers a row through persisted mutable state.
- path: flow_e/flow.rs
  symbol: emit_e
  kind: function
  signature: pub fn emit_e(a: &Path, b: &[Record]) -> io::Result<()>
  purpose: Writes structured rows to a durable line-oriented surface.
- path: drive_g/drive.rs
  symbol: drive_g
  kind: function
  signature: pub fn drive_g(a: &Plan, b: &Path) -> io::Result<CaseReport>
  purpose: Coordinates one scenario from parsed input to generated report.
```

#### flipping_point_contract

```
locations:
  - id: A
    path: core_a/core.rs
    controls_tests: [test_a0, test_c2, test_k0]
  - id: B
    path: book_b/book.rs
    controls_tests: [test_d3, test_h7, test_l1]
  - id: C
    path: gate_c/gate.rs
    controls_tests: [test_e4, test_f5, test_g6]
  - id: D
    path: flow_e/flow.rs
    controls_tests: [test_b1, test_i8, test_j9]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: spill_i/spill.rs
  kind: helper
  rhymes_with: fold_b
  non_fix_purpose: Normalizes small integer buckets for documentation examples.
- path: mirror_j/mirror.rs
  kind: helper
  rhymes_with: emit_e
  non_fix_purpose: Formats diagnostic summaries that are not part of the report path.
```

#### code_forbidden_tokens

```
code_forbidden_tokens: [Rust, workload, runner, audit, queues, branches, child, work, matrix, output, JSON, cases, inputs, array, amber, cobalt, drake, ember, flint, graphite, name, ok, finished, pending, trace, ledger, journal, records, record, case, task, parent, depth, lane, turn, JSONL, file, text, rows, relationships]
```
