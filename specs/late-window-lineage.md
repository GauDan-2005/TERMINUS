### Decision
GO — Attempt 1. The design keeps the public prompt at symptom level, distributes the repair across Rust state, ordering, recovery, and emission paths, and commits opaque fix-path names before drafting.

### Metadata
- version: 2
- Task name: late-window-lineage
- Title: Late Window Lineage
- Category: data-processing
- Languages: [Rust, shell]
- Difficulty: hard
- Codebase size: small (20-200 files under environment/ excluding Docker files)
- Subcategories: []
- Tags: [rust, streaming, replay, aggregation, checkpoints]
- Milestones: 0

## Authoring Brief
This file is the only drafting input for Step 2b. Do not use the reviewer appendix while drafting the task files.

### Public contract
Build a Rust streaming/event-time aggregation repository under `/app`. The public prompt should say the local event engine produces restart-sensitive audit output for late-window scenarios. The documented command is `bash /app/scripts/run-matrix.sh`, and the user-visible output is `/app/output/window-audit.json`. The JSON must contain a top-level cases array for aurora, boreal, cirrus, drift, ember, and flux. Each case reports `name`, `ok`, direct/replay views, totals, corrections, repeat stability, and lineage-bearing correction rows. The clean state is every case `ok == true`, direct and replay totals match, correction identities and lineage are stable across repeated restarted runs, and replayed input does not create duplicate correction records.

### Failure topology
The symptom clusters should involve the same scenario looking healthy when run straight through but drifting under a restart/replay path. The concrete implementation must make the direct path, restarted path, retained rows, and output writer each plausible sources of truth, with no single file revealing the whole invariant.

The hard part is the coupling: suppressing replay duplicates must not suppress legitimate late corrections; sorting emitted rows must not change correction identity; rebuilding retained state must agree with direct in-memory state; compaction cannot change lineage order. A one-file equality hack should fail the tests.

### Environment shape
Create a small Rust project with modules for row types/serialization, parsing, case loading, grouped row construction, retained-row combination, emission gating, restart-state loading, audit orchestration, and non-fix display helpers. Keep the fix path in opaque directories (`a0`, `b1`, `c2`, `d3`, `e4`) and use the committed symbols below. Include six case input files under `environment/data/cases/` and shell tooling under `environment/scripts/`.

### Required artifacts
Create a standard single-step task: `instruction.md`, `task.toml`, `output_contract.toml`, `construction_manifest.json`, `environment/Dockerfile`, 20+ substantive files under `environment/`, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. Do not create milestone, UI, or multi-container structure.

### Test plan
- `test_r01`: the documented command creates the JSON audit and all six case names are present; multiple implementations valid; not chain-dependent.
- `test_r02`: every case reports a clean audit and exposes direct/replay/repeat surfaces; multiple implementations valid; not chain-dependent.
- `test_r03`: direct totals match values independently derived from case input rows; multiple implementations valid; not chain-dependent.
- `test_r04`: replay totals match the direct totals in mixed late-row cases; multiple implementations valid; not chain-dependent.
- `test_r05`: repeated restarted runs produce the same correction identities; multiple implementations valid; not chain-dependent.
- `test_r06`: duplicate input rows are suppressed without losing legitimate corrections; multiple implementations valid; not chain-dependent.
- `test_r07`: correction lineage is ordered by row semantics rather than incidental file order; multiple implementations valid; not chain-dependent.
- `test_r08`: partition-local progress does not suppress another partition's update; multiple implementations valid; not chain-dependent.
- `test_r09`: compaction-style case data yields stable replay records; multiple implementations valid; not chain-dependent.
- `test_r10`: persisted state is reused without duplicating old correction rows; multiple implementations valid; not chain-dependent.
- `test_r11`: correction IDs bind the case, partition, window, key, value, and lineage; multiple implementations valid; not chain-dependent.
- `test_r12`: totals and corrections remain sorted deterministically across two invocations; multiple implementations valid; not chain-dependent.

### Drafting guardrails
Do not name internal causes in `instruction.md`. Avoid code symbols or fix-path directories using public nouns such as replay, window, lineage, checkpoint, watermark, compaction, partition, or correction. Do not ship golden outputs under `environment/`. The case files are inputs only; tests compute expected behavior independently.

### Triviality Ledger
- Global output sorting alone is blocked because tests recompute correction IDs and lineage from input rows.
- Dropping all duplicate-looking rows is blocked because tests include legitimate late updates that share case/key/window surfaces.
- Rebuilding only the restarted path is blocked because direct totals and repeated restarted output are both checked.
- Hardcoding six reports is blocked by tests deriving values from scenario inputs and by NOP-failing domain assertions.
- One-file helper completion is blocked by the flipping-point contract across five source roots.

### Per-gate Pitfall Inventory
- RC1/RC7: the oracle must add substantive Rust logic across multiple files, not delete branches or overwrite one tiny table.
- RC2/CR7: fix-path names and test names must stay opaque; use the symbol table exactly.
- RC3/RC4/RC5: tests assert derived domain values and keep expected values in Python code, not in environment reference outputs.
- RC6/GX6/GX9/GX10: instruction stays symptoms-only, with schema prose but no algorithms, internal file names, numeric thresholds, cause statements, or answer-key triples.
- CR2/CR8: no one location controls a majority of tests, and no visible file should reference more than two manifest symbols.
- GX1/GX3: environment comments must not disclose fixes; solve.sh edits must be substantive, not cosmetic diff padding.
- Static checks: canonical `tests/test.sh`, pinned Dockerfile base and apt packages, environment file count above 20, no AI scaffolding names, no hidden instructions.

### Initial Draft Commitments
- `tasks/late-window-lineage/instruction.md` — symptoms-only public prompt.
- `tasks/late-window-lineage/task.toml` — Edition 2 metadata.
- `tasks/late-window-lineage/output_contract.toml` — repo-local output contract.
- `tasks/late-window-lineage/construction_manifest.json` — mirror of this manifest for collapse checks.
- `tasks/late-window-lineage/environment/Dockerfile` — pinned single-container image with Rust toolchain.
- `tasks/late-window-lineage/environment/Cargo.toml` — Rust package manifest.
- `tasks/late-window-lineage/environment/README.md` — neutral repository context.
- `tasks/late-window-lineage/environment/docs/architecture.md` — neutral component overview.
- `tasks/late-window-lineage/environment/docs/operations.md` — neutral operator notes.
- `tasks/late-window-lineage/environment/scripts/run-matrix.sh` — documented command.
- `tasks/late-window-lineage/environment/src/main.rs` — CLI entry.
- `tasks/late-window-lineage/environment/src/lib.rs` — module root.
- `tasks/late-window-lineage/environment/src/a0/mod.rs` — opaque module declaration.
- `tasks/late-window-lineage/environment/src/a0/core.rs` — manifest fix-path source.
- `tasks/late-window-lineage/environment/src/b1/mod.rs` — opaque module declaration.
- `tasks/late-window-lineage/environment/src/b1/book.rs` — manifest fix-path source.
- `tasks/late-window-lineage/environment/src/c2/mod.rs` — opaque module declaration.
- `tasks/late-window-lineage/environment/src/c2/gate.rs` — manifest fix-path source.
- `tasks/late-window-lineage/environment/src/d3/mod.rs` — opaque module declaration.
- `tasks/late-window-lineage/environment/src/d3/host.rs` — manifest fix-path source.
- `tasks/late-window-lineage/environment/src/e4/mod.rs` — opaque module declaration.
- `tasks/late-window-lineage/environment/src/e4/flow.rs` — manifest fix-path source.
- `tasks/late-window-lineage/environment/src/f5/mod.rs` — shared type/serialization module declaration.
- `tasks/late-window-lineage/environment/src/f5/types.rs` — shared data types.
- `tasks/late-window-lineage/environment/src/f5/serde.rs` — JSON writer helpers.
- `tasks/late-window-lineage/environment/src/g6/mod.rs` — decoy helper declaration.
- `tasks/late-window-lineage/environment/src/g6/cache.rs` — non-fix display state helper.
- `tasks/late-window-lineage/environment/src/h7/mod.rs` — decoy helper declaration.
- `tasks/late-window-lineage/environment/src/h7/view.rs` — non-fix summary helper.
- `tasks/late-window-lineage/environment/src/i8/mod.rs` — parse helper declaration.
- `tasks/late-window-lineage/environment/src/i8/parse.rs` — input row parser.
- `tasks/late-window-lineage/environment/src/j9/mod.rs` — case loader declaration.
- `tasks/late-window-lineage/environment/src/j9/cases.rs` — case loader.
- `tasks/late-window-lineage/environment/src/k1/mod.rs` — run orchestration declaration.
- `tasks/late-window-lineage/environment/src/k1/run.rs` — run orchestration.
- `tasks/late-window-lineage/environment/src/l2/mod.rs` — text helper declaration.
- `tasks/late-window-lineage/environment/src/l2/text.rs` — small text helper.
- `tasks/late-window-lineage/environment/src/m3/mod.rs` — check helper declaration.
- `tasks/late-window-lineage/environment/src/m3/check.rs` — internal audit comparison helper.
- `tasks/late-window-lineage/environment/data/cases/aurora.csv` — input case data.
- `tasks/late-window-lineage/environment/data/cases/boreal.csv` — input case data.
- `tasks/late-window-lineage/environment/data/cases/cirrus.csv` — input case data.
- `tasks/late-window-lineage/environment/data/cases/drift.csv` — input case data.
- `tasks/late-window-lineage/environment/data/cases/ember.csv` — input case data.
- `tasks/late-window-lineage/environment/data/cases/flux.csv` — input case data.
- `tasks/late-window-lineage/solution/solve.sh` — deterministic oracle.
- `tasks/late-window-lineage/tests/test.sh` — canonical pytest runner.
- `tasks/late-window-lineage/tests/test_outputs.py` — verifier tests.

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

```json
{
  "symbol_table": [
    {"path": "src/a0/core.rs", "symbol": "fold_a", "kind": "function", "signature": "pub fn fold_a(a: &[R0], b: &S0) -> Vec<R1>", "purpose": "builds normalized grouped rows from observed input and control state"},
    {"path": "src/b1/book.rs", "symbol": "merge_b", "kind": "function", "signature": "pub fn merge_b(a: &mut S1, b: &[R1]) -> Vec<R1>", "purpose": "combines retained and fresh rows into a deterministic stream"},
    {"path": "src/c2/gate.rs", "symbol": "mark_c", "kind": "function", "signature": "pub fn mark_c(a: &mut S2, b: &R1) -> Option<R2>", "purpose": "decides whether a normalized row should produce an emitted record"},
    {"path": "src/d3/host.rs", "symbol": "load_d", "kind": "function", "signature": "pub fn load_d(a: &std::path::Path) -> std::io::Result<S3>", "purpose": "recreates local state from persisted rows"},
    {"path": "src/e4/flow.rs", "symbol": "push_e", "kind": "function", "signature": "pub fn push_e(a: &std::path::Path, b: &[R2]) -> std::io::Result<()>", "purpose": "writes structured rows consumed by the audit layer"}
  ],
  "flipping_point_contract": {
    "locations": [
      {"id": "A", "path": "a0/core.rs", "controls_tests": ["test_r01", "test_r02", "test_r03"]},
      {"id": "B", "path": "b1/book.rs", "controls_tests": ["test_r04", "test_r05", "test_r06"]},
      {"id": "C", "path": "c2/gate.rs", "controls_tests": ["test_r07", "test_r08", "test_r09"]},
      {"id": "D", "path": "d3/host.rs", "controls_tests": ["test_r10", "test_r11", "test_r12"]},
      {"id": "E", "path": "e4/flow.rs", "controls_tests": ["test_r02", "test_r06", "test_r10"]}
    ],
    "no_single_location_flips_majority": true,
    "concentration_cap": 0.5
  },
  "decoy_manifest": [
    {"path": "src/g6/cache.rs", "kind": "helper", "rhymes_with": "fold_a", "non_fix_purpose": "stores operator display state that does not affect execution"},
    {"path": "src/h7/view.rs", "kind": "helper", "rhymes_with": "push_e", "non_fix_purpose": "formats textual summaries for local inspection"},
    {"path": "src/i8/parse.rs", "kind": "helper", "rhymes_with": "load_d", "non_fix_purpose": "parses simple input rows without owning recovery state"}
  ],
  "code_forbidden_tokens": ["engine", "app", "audit", "output", "scenarios", "script", "json", "cases", "aurora", "boreal", "cirrus", "drift", "ember", "flux", "case", "name", "ok", "direct", "replay", "totals", "corrections", "repeat", "entries", "input", "run", "paths", "partition", "window", "key", "value", "fields", "id", "lineage", "array", "ids", "order", "records"]
}
```
