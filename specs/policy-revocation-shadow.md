### Decision

GO — Attempt 1. The design keeps the prompt symptoms-only, distributes the fix across five neutral Rust modules, and blocks naive full-cache-flush and single-table edits with reuse and mixed-batch checks.

### Metadata

- version: 2
- Task name: policy-revocation-shadow
- Title: Policy Revocation Shadow
- Category: security
- Languages: ["Rust", "shell"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["rust", "security", "capability", "delegation", "cache-invalidation"]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do not open the reviewer appendix until the post-build discovery-budget confirmation.

### Public contract

The task is a local capability policy harness under `/app`. The user sees that running `bash /app/scripts/run-matrix.sh` should write `/app/output/policy-audit.json` from the current trace inputs rather than from a canned table. The report has a top-level `cases` array for alpha, beta, gamma, delta, epsilon, and zeta. Each case reports `name`, `ok`, `decisions`, and `stale`. Each decision reports `label`, `principal`, `resource`, `action`, `verdict`, `epoch`, `reused`, `batch_id`, and `delegated_from`. The `verdict` field is `allow` or `deny`. The `batch_id` field is empty outside batched checks. The `delegated_from` field names the grantor when access comes through delegation and is empty for direct grants. Each decision epoch is the principal epoch at evaluation time, and epochs are nondecreasing inside each case. Revoked principals must never receive `allow` on delegated paths. Unchanged decisions are marked as `reused` when the same principal, resource, and action are checked again without an intervening state change that affects that principal.

### Failure topology

The broken harness evaluates access requests from trace files through delegation graph walks, principal epoch bumps, negative-cache reuse, and batched member evaluation. Some cases incorrectly allow delegated access after a revoke when checks run inside a batch that reuses an earlier cached verdict. Other cases keep stale deny rows after a grant is added, or fail to propagate ancestor revokes through multi-hop delegation. Mixed batches can deny a clean principal when a revoked peer shares the same resource and action slot.

The repair should force the solver to reconstruct how trace events mutate grants and delegation edges, how principal epochs participate in cache keys, how batch members are evaluated independently, and how reuse is computed without flushing unrelated principals. File and symbol names on the fix path must stay opaque; the public prompt should not mention internal module names or the cause of any stale row.

### Environment shape

Create a standard single-step task. The environment is a Rust command-line project with trace files and principal fixture manifests. The Rust project has neutral module roots under `k0` through `k8`, plus shared model, parsing, runner, and JSON report modules. Traces under `traces/` drive six cases. Fixture directories under `fixtures/` contain principal registries and delegation notes for realism. A shell script under `scripts/` runs the matrix and writes the report.

### Required artifacts

Create the standard task files: root `instruction.md`, `task.toml`, `output_contract.toml`, `construction_manifest.json`, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. The Docker image must be offline at verifier/runtime, with Rust, Python, pytest, and pytest-json-ctrf installed in `environment/Dockerfile`; `tests/test.sh` must not download or install anything. The environment must have more than 20 substantive files excluding Dockerfile.

### Test plan

- `test_t01_flow`: verifies alpha denies delegated access after revoke inside and outside batches.
- `test_t02_flow`: verifies beta allows access after grant invalidates an earlier deny cache entry.
- `test_t03_flow`: verifies gamma denies multi-hop delegated access when an ancestor is revoked.
- `test_t04_flow`: verifies delta keeps reuse for an unchanged principal across an unrelated revoke.
- `test_t05_flow`: verifies epsilon denies access when a middle delegation node is revoked.
- `test_t06_flow`: verifies zeta mixed batch denies the revoked principal while allowing the clean peer.
- `test_t07_flow`: verifies every case has `ok` true and an empty `stale` list.
- `test_t08_flow`: verifies no decision after a revoke reports `allow` on a delegated path for that principal.
- `test_t09_flow`: verifies epochs are monotonic and changed principals do not claim reuse incorrectly.
- `test_t10_flow`: verifies `delegated_from` names the grantor on delegated allows and stays empty on direct grants.
- `test_t11_flow`: verifies batch_id is populated only inside batch checks and empty otherwise.
- `test_t12_flow`: verifies two consecutive matrix runs produce byte-identical output.

### Drafting guardrails

Keep the instruction readable but symptoms-only. Do not name the Rust modules, functions, cache cause, epoch algorithm, or trace opcode format. Do not put answer rows, verdict tables, hashes, or a golden report in environment files. Fix-path paths and symbols must use the manifest names verbatim and must not contain instruction nouns. Tests should assert behavior and compute helper expectations inside test code, not by reading expected output files from the environment.

### Triviality Ledger

- Naive full cache flush: blocked because delta requires `reused` true for an unchanged principal across an unrelated revoke.
- Single policy table edit: blocked because gamma and epsilon require multi-hop delegation propagation and beta requires negative-cache invalidation after grant.
- Hardcoded report table: blocked because tests rerun the matrix, check deterministic output shape, and assert values across six independent traces.
- One-function epoch patch: blocked because zeta mixed batches require independent member evaluation and alpha requires batch plus post-revoke checks.
- Prompt-grep path: blocked by opaque fix-path directories (`k0` through `k4`) and symbols (`phase_a`, `fold_b`, `emit_c`, `lift_d`, `mote_e`, `cast_f`).

### Per-gate Pitfall Inventory

- RC1 oracle simplification: avoid deletions or flag flips; `solve.sh` must write substantive replacement logic across five Rust modules.
- RC2 oracle predictability: no file or test name should use `revoke`, `delegation`, `cache`, `shadow`, `fix`, `bug`, `golden`, or `expected`.
- RC3 verifier shallowness: tests must inspect domain rows: verdict, epoch, reuse, batch_id, delegated_from, and case cleanliness.
- RC4 tamper surface: tests must not read a golden report from `environment/`; expected values live in Python literals and helper functions.
- RC5 reference artifacts: do not ship answer-shaped fixtures, reference reports, or hidden output snapshots.
- RC6 instruction specificity: no algorithms, internal module names, cause statements, or exact verdict tables in `instruction.md`.
- RC7/GX3 oracle triviality: keep the oracle semantic edit distance above the 80-line comfortable floor through real logic changes only.
- GX1 comment leakage: no correctional comments near changed Rust lines; prefer no comments in fix-path files.
- GX9/GX10 instruction cheating: do not enumerate the answer rows or use ambiguous allow/deny prose for one scenario.
- Static checks: use `version = "2.0"`, anonymous author fields, 3-6 tags, `codebase_size = "small"`, integer timeouts/resources, and `[environment].allow_internet = false`.

### Initial Draft Commitments

- `instruction.md` — symptoms-only user prompt with the command and report contract.
- `task.toml` — Edition 2 metadata for a hard security task with offline runtime.
- `output_contract.toml` — root authoring contract for `/app/output/policy-audit.json`.
- `construction_manifest.json` — exact manifest mirrored from this spec.
- `solution/solve.sh` — deterministic oracle that writes the five corrected Rust modules.
- `tests/test.sh` — offline pytest runner using preinstalled dependencies and the reward footer.
- `tests/test_outputs.py` — twelve pytest checks named `test_t01_flow` through `test_t12_flow`.
- `environment/Dockerfile` — digest-pinned Rust base with pinned apt and pytest dependencies.
- `environment/Cargo.toml` — no-network Rust package manifest.
- `environment/Cargo.lock` — locked dependencies.
- `environment/README.md` — concise project context without solution instructions.
- `environment/docs/architecture.md` — subsystem overview without fix hints.
- `environment/.dockerignore` — build context exclusions.
- `environment/src/main.rs` — CLI entry point.
- `environment/src/lib.rs` — Rust module declarations.
- `environment/src/model.rs` — shared data structures.
- `environment/src/io.rs` — trace parsing helpers.
- `environment/src/runner.rs` — case runner.
- `environment/src/report.rs` — JSON serialization.
- `environment/k0/a.rs` — fix-path event routing symbol `phase_a`.
- `environment/k1/b.rs` — fix-path revoke handling symbol `fold_b`.
- `environment/k2/c.rs` — fix-path cache keying symbol `emit_c`.
- `environment/k3/d.rs` — fix-path batch evaluation symbol `lift_d`.
- `environment/k4/e.rs` — fix-path delegation resolution symbol `mote_e`.
- `environment/k5/f.rs` — fix-path audit classification symbol `cast_f`.
- `environment/k6/g.rs` — decoy helper rhyming with event routing.
- `environment/k7/h.rs` — decoy helper rhyming with batch evaluation.
- `environment/k8/i.rs` — decoy helper rhyming with delegation resolution.
- `environment/scripts/run-matrix.sh` — command named in the instruction.
- `environment/scripts/run-one.sh` — single-case helper.
- `environment/traces/alpha.trace` through `zeta.trace` — six scenario traces.
- `environment/fixtures/` — principal registry files for each case.

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: k0/a.rs
  symbol: phase_a
  kind: function
  signature: pub fn phase_a(a: &mut State, b: &Event, c: &mut CaseReport) -> Result<(), String>
  purpose: routes one parsed trace entry through grant, delegate, revoke, batch, and check layers
- path: k1/b.rs
  symbol: fold_b
  kind: function
  signature: pub fn fold_b(a: &mut State, b: &str) -> Result<(), String>
  purpose: applies a revoke event and updates principal epoch state
- path: k2/c.rs
  symbol: emit_c
  kind: function
  signature: pub fn emit_c(a: &State, b: &str, c: &str, d: &str) -> Option<String>
  purpose: reads a cached verdict for a principal resource action tuple
- path: k3/d.rs
  symbol: lift_d
  kind: function
  signature: pub fn lift_d(a: &mut State, b: &str, c: &str, d: &str) -> Decision
  purpose: evaluates one batched check member and records its verdict
- path: k4/e.rs
  symbol: mote_e
  kind: function
  signature: pub fn mote_e(a: &State, b: &str, c: &str, d: &str) -> (String, String)
  purpose: resolves whether a principal may access a resource action through delegation
- path: k5/f.rs
  symbol: cast_f
  kind: function
  signature: pub fn cast_f(a: &State, b: Decision, c: bool) -> (Decision, Option<String>)
  purpose: classifies one decision for the case-level audit status and reuse marking
```

#### flipping_point_contract

```
locations:
  - id: A
    path: k1/b.rs
    controls_tests: [test_t01_flow, test_t08_flow]
  - id: B
    path: k2/c.rs
    controls_tests: [test_t02_flow, test_t09_flow]
  - id: C
    path: k3/d.rs
    controls_tests: [test_t06_flow, test_t11_flow]
  - id: D
    path: k4/e.rs
    controls_tests: [test_t03_flow, test_t05_flow]
  - id: E
    path: k5/f.rs
    controls_tests: [test_t04_flow, test_t10_flow]
  - id: F
    path: k0/a.rs
    controls_tests: [test_t07_flow, test_t12_flow]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: k6/g.rs
  kind: helper
  rhymes_with: phase_a
  non_fix_purpose: formats diagnostic counters for local developer summaries
- path: k7/h.rs
  kind: helper
  rhymes_with: lift_d
  non_fix_purpose: reads optional display labels for non-audit listings
- path: k8/i.rs
  kind: helper
  rhymes_with: mote_e
  non_fix_purpose: chooses display ordering for interactive dumps
```

#### code_forbidden_tokens

```
code_forbidden_tokens: [capability, harness, delegated, access, revoke, batch, cached, results, Rust, sources, cargo, bash, scripts, output, audit, JSON, cases, name, ok, decisions, stale, label, resource, action, verdict, allow, deny, epoch, reused, batch_id, delegated_from, grants, agreement, trace, principal]
```
