### Decision

GO — Attempt 1. The design keeps the prompt symptoms-only, distributes the fix across six neutral Rust modules, and blocks the naive full-cache-flush path with reuse checks.

### Metadata

- version: 2
- Task name: incremental-index-invalidation
- Title: Index Invalidation Drift
- Category: software-engineering
- Languages: ["Rust", "TypeScript"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["rust", "typescript", "indexing", "cache-invalidation", "tooling"]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do not open the reviewer appendix until the post-build discovery-budget confirmation.

### Public contract

The task is a local code-indexing harness under `/app`. The user sees that running `bash /app/scripts/run-matrix.sh` should write `/app/output/index-report.json` from the current TypeScript fixtures rather than from a canned table. The report has a top-level `cases` array for alpha, beta, gamma, delta, epsilon, and zeta. Each case reports `name`, `ok`, `observations`, and `stale`. Each observation reports `label`, `symbol`, `found`, `path`, `source`, `line`, `epoch`, `reused`, and `fresh`. Paths and sources use absolute `/app` paths, and epochs are nondecreasing inside each case. Found symbols must point to the live definition for that case after its preceding edits. Missing symbols report `found` false with empty `path` and `source`. Definitions unaffected by an edit should keep `reused` true when queried again.

### Failure topology

The broken harness simulates editor-like updates against TypeScript workspaces. Some case rows keep old definition locations when a workspace root is switched, a generated tree is refreshed, or a linked package target changes. Other rows fail in the opposite direction: a broad rebuild can hide stale paths but loses stable handles for definitions that did not move. Generated files also carry provenance to source files, so a row can have the right symbol but the wrong source path.

The repair should force the solver to reconstruct how trace events become index entries, how active roots are represented, how package targets are resolved, and how observations are classified. File and symbol names on the fix path must stay opaque; the public prompt should not mention invalidation algorithms, specific Rust modules, or the cause of any stale row.

### Environment shape

Create a standard single-step task. The environment is a Rust command-line project with TypeScript fixture trees and trace files. The Rust project has neutral module roots under `r0` through `r8`, plus shared model, parsing, runner, and JSON report modules. Traces under `traces/` drive six cases. Fixture directories under `fixtures/` contain workspace versions, generated TypeScript files with source provenance, and package target manifests. A shell script under `scripts/` runs the matrix and writes the report.

### Required artifacts

Create the standard task files: root `instruction.md`, `task.toml`, `output_contract.toml`, `construction_manifest.json`, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. The Docker image must be offline at verifier/runtime, with Rust, Python, pytest, and pytest-json-ctrf installed in `environment/Dockerfile`; `tests/test.sh` must not download or install anything. The environment must have more than 20 substantive files excluding Dockerfile.

### Test plan

- `test_t01_flow`: verifies the alpha case no longer reports the old workspace path after a root switch; multiple valid approaches exist if they preserve live definitions.
- `test_t02_flow`: verifies the beta generated row points to the refreshed generated file and current source; multiple valid approaches exist.
- `test_t03_flow`: verifies the gamma package row follows the active target rather than the previous target; multiple valid approaches exist.
- `test_t04_flow`: verifies a generated row in the mixed delta case is reused across an unrelated workspace edit; chain-dependent risk is low because the trace supplies its own setup.
- `test_t05_flow`: verifies the epsilon case reports a removed symbol as missing rather than resolving an old row; multiple valid approaches exist.
- `test_t06_flow`: verifies the zeta case handles package and workspace changes in one trace; chain-dependent risk is low because all prerequisites are in the trace.
- `test_t07_flow`: verifies every case has `ok` true and an empty `stale` list.
- `test_t08_flow`: verifies no after-state observation path remains under an earlier workspace root.
- `test_t09_flow`: verifies epochs are monotonic and changed definitions do not claim reuse.
- `test_t10_flow`: verifies stable definitions keep reuse when a different slot changes.
- `test_t11_flow`: verifies path/source fields are absolute and found/missing rows use the documented empty-field convention.
- `test_t12_flow`: verifies two consecutive matrix runs produce the same report from current fixtures.

### Drafting guardrails

Keep the instruction readable but symptoms-only. Do not name the Rust modules, functions, stale-cache cause, epoch algorithm, source-comment convention, or package-target manifest format. Do not put answer rows, old/new path pairs, hashes, or a golden report in environment files. Fix-path paths and symbols must use the manifest names verbatim and must not contain instruction nouns. Tests should assert behavior and compute helper expectations inside test code, not by reading expected output files from the environment.

### Triviality Ledger

- Naive full rebuild: blocked because delta and zeta include stable definitions that must keep `reused` true across unrelated edits.
- First-match lookup patch: blocked because epsilon expects a removed symbol to be missing, and beta/gamma require current provenance rather than any matching symbol.
- Hardcoded report table: blocked because tests rerun the matrix, check deterministic output shape, and assert values across six independent traces rather than accepting file existence.
- One-root cache edit: blocked because workspace, generated, and package traces exercise distinct roots with separate stale-row symptoms.
- Prompt-grep path: blocked by opaque fix-path directories (`r0` through `r5`) and symbols (`phase_a`, `fold_b`, `emit_c`, `lift_d`, `mote_e`, `cast_f`).

### Per-gate Pitfall Inventory

- RC1 oracle simplification: avoid deletions or flag flips; `solve.sh` must write substantive replacement logic across six Rust modules.
- RC2 oracle predictability: no file or test name should use `stale`, `rename`, `generated`, `symlink`, `cache`, `fix`, `bug`, `golden`, or `expected`.
- RC3 verifier shallowness: tests must inspect domain rows: paths, sources, found state, reuse, epochs, and case cleanliness.
- RC4 tamper surface: tests must not read a golden report or expected file from `environment/`; expected values live in Python literals and helper functions.
- RC5 reference artifacts: do not ship answer-shaped fixtures, reference reports, or hidden output snapshots.
- RC6 instruction specificity: no algorithms, internal module names, cause statements, or exact old/new row pairs in `instruction.md`.
- RC7/GX3 oracle triviality: keep the oracle's semantic edit distance above the 80-line comfortable floor through real logic changes only.
- GX1 comment leakage: no correctional comments near changed Rust lines; prefer no comments in fix-path files.
- GX9/GX10 instruction cheating: do not enumerate the answer rows or use ambiguous binary-status prose.
- Static checks: use `version = "2.0"`, anonymous author fields, 3-6 tags, `codebase_size = "small"`, integer timeouts/resources, and `[environment].allow_internet = false`.

### Initial Draft Commitments

- `instruction.md` — symptoms-only user prompt with the command and report contract.
- `task.toml` — Edition 2 metadata for a hard software-engineering task with offline runtime.
- `output_contract.toml` — root authoring contract for `/app/output/index-report.json`.
- `construction_manifest.json` — exact manifest mirrored from this spec.
- `solution/solve.sh` — deterministic oracle that writes the six corrected Rust modules.
- `tests/test.sh` — offline pytest runner using preinstalled dependencies and the reward footer.
- `tests/test_outputs.py` — twelve pytest checks named `test_t01_flow` through `test_t12_flow`.
- `environment/Dockerfile` — digest-pinned Python base with pinned Rust and pytest dependencies.
- `environment/Cargo.toml` — no-network Rust package manifest.
- `environment/README.md` — concise project context without solution instructions.
- `environment/src/main.rs` — CLI entry point.
- `environment/src/lib.rs` — Rust module declarations.
- `environment/src/model.rs` — shared data structures.
- `environment/src/io.rs` — trace and fixture scanning helpers.
- `environment/src/runner.rs` — case runner that calls the first neutral fix-path symbol.
- `environment/src/report.rs` — JSON serialization.
- `environment/r0/a.rs` — fix-path event routing symbol `phase_a`.
- `environment/r1/b.rs` — fix-path normal tree loading symbol `fold_b`.
- `environment/r2/c.rs` — fix-path generated tree loading symbol `emit_c`.
- `environment/r3/d.rs` — fix-path linked target loading symbol `lift_d`.
- `environment/r4/e.rs` — fix-path lookup symbol `mote_e`.
- `environment/r5/f.rs` — fix-path audit classification symbol `cast_f`.
- `environment/r6/g.rs` — decoy helper rhyming with event routing.
- `environment/r7/h.rs` — decoy helper rhyming with linked target loading.
- `environment/r8/i.rs` — decoy helper rhyming with lookup selection.
- `environment/scripts/run-matrix.sh` — command named in the instruction.
- `environment/traces/alpha.trace` — workspace-switch case.
- `environment/traces/beta.trace` — generated refresh case.
- `environment/traces/gamma.trace` — package target case.
- `environment/traces/delta.trace` — mixed workspace/generated reuse case.
- `environment/traces/epsilon.trace` — removed generated symbol case.
- `environment/traces/zeta.trace` — mixed package/workspace case.
- `environment/fixtures/alpha/ws-old/src/widget.ts` — old workspace fixture.
- `environment/fixtures/alpha/ws-new/src/widget.ts` — current workspace fixture.
- `environment/fixtures/beta/gen-v1/generated/api.ts` — old generated fixture.
- `environment/fixtures/beta/gen-v2/generated/api.ts` — current generated fixture.
- `environment/fixtures/beta/schemas/v1/api.schema` — old generated provenance file.
- `environment/fixtures/beta/schemas/v2/api.schema` — current generated provenance file.
- `environment/fixtures/gamma/alias-a/link.target` — first package target manifest.
- `environment/fixtures/gamma/alias-b/link.target` — second package target manifest.
- `environment/fixtures/gamma/pkg-a/src/bridge.ts` — first package fixture.
- `environment/fixtures/gamma/pkg-b/src/bridge.ts` — second package fixture.
- `environment/fixtures/delta/app-old/src/widget.ts` — old mixed workspace fixture.
- `environment/fixtures/delta/app-new/src/widget.ts` — current mixed workspace fixture.
- `environment/fixtures/delta/gen-v1/generated/client.ts` — first mixed generated fixture.
- `environment/fixtures/delta/gen-v2/generated/client.ts` — second mixed generated fixture.
- `environment/fixtures/delta/schemas/v1/client.schema` — first mixed generated provenance file.
- `environment/fixtures/delta/schemas/v2/client.schema` — second mixed generated provenance file.
- `environment/fixtures/epsilon/gen-v1/generated/legacy.ts` — old generated fixture with removable symbol.
- `environment/fixtures/epsilon/gen-v2/generated/client.ts` — current generated fixture without the removed symbol.
- `environment/fixtures/epsilon/schemas/v1/legacy.schema` — old removable-symbol provenance file.
- `environment/fixtures/epsilon/schemas/v2/client.schema` — current generated provenance file.
- `environment/fixtures/zeta/app-old/src/widget.ts` — old combined workspace fixture.
- `environment/fixtures/zeta/app-new/src/widget.ts` — current combined workspace fixture.
- `environment/fixtures/zeta/alias-a/link.target` — first combined package target manifest.
- `environment/fixtures/zeta/alias-b/link.target` — second combined package target manifest.
- `environment/fixtures/zeta/pkg-a/src/bridge.ts` — first combined package fixture.
- `environment/fixtures/zeta/pkg-b/src/bridge.ts` — second combined package fixture.

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: r0/a.rs
  symbol: phase_a
  kind: function
  signature: pub fn phase_a(a: &mut State, b: &Event, c: &mut CaseReport) -> Result<(), String>
  purpose: routes one parsed trace entry through the state mutation and observation layers
- path: r1/b.rs
  symbol: fold_b
  kind: function
  signature: pub fn fold_b(a: &mut State, b: &str, c: &str) -> Result<(), String>
  purpose: loads a normal tree into the in-memory table for a named slot
- path: r2/c.rs
  symbol: emit_c
  kind: function
  signature: pub fn emit_c(a: &mut State, b: &str, c: &str) -> Result<(), String>
  purpose: loads a generated tree and carries file provenance into emitted rows
- path: r3/d.rs
  symbol: lift_d
  kind: function
  signature: pub fn lift_d(a: &mut State, b: &str, c: &str) -> Result<(), String>
  purpose: loads a target selected through an alias directory into the table
- path: r4/e.rs
  symbol: mote_e
  kind: function
  signature: pub fn mote_e(a: &mut State, b: &str, c: bool) -> Observation
  purpose: selects the table row used by one observation and computes reuse state
- path: r5/f.rs
  symbol: cast_f
  kind: function
  signature: pub fn cast_f(a: &State, b: Observation, c: bool) -> (Observation, Option<String>)
  purpose: classifies one observation for the case-level audit status
```

#### flipping_point_contract

```
locations:
  - id: A
    path: r0/a.rs
    controls_tests: [test_t07_flow, test_t12_flow]
  - id: B
    path: r1/b.rs
    controls_tests: [test_t01_flow, test_t08_flow]
  - id: C
    path: r2/c.rs
    controls_tests: [test_t02_flow, test_t04_flow]
  - id: D
    path: r3/d.rs
    controls_tests: [test_t03_flow, test_t06_flow]
  - id: E
    path: r4/e.rs
    controls_tests: [test_t05_flow, test_t09_flow]
  - id: F
    path: r5/f.rs
    controls_tests: [test_t10_flow, test_t11_flow]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: r6/g.rs
  kind: helper
  rhymes_with: phase_a
  non_fix_purpose: formats diagnostic counters for local developer summaries
- path: r7/h.rs
  kind: helper
  rhymes_with: lift_d
  non_fix_purpose: reads optional display aliases for non-audit listings
- path: r8/i.rs
  kind: helper
  rhymes_with: mote_e
  non_fix_purpose: chooses display ordering for interactive dumps
```

#### code_forbidden_tokens

```
code_forbidden_tokens: [index, harness, definition, locations, rename, module, package, sequences, bash, scripts, output, report, fixtures, JSON, cases, name, observations, label, symbol, path, source, line, epoch, target, audit]
```
