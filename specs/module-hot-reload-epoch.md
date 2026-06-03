### Decision
GO — Attempt 1. The design distributes the hot-runtime lifecycle invariant across Node and Rust boundaries with opaque fix-path names and ten behavior tests.

### Metadata
- version: 2
- Task name: module-hot-reload-epoch
- Title: Reload Epoch Drift
- Category: software-engineering
- Languages: ["Node.js", "Rust"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["nodejs", "rust", "hot-reload", "state", "debugging"]
- Milestones: 0

## Authoring Brief

### Public contract
Create a standard single-step task. The agent-facing instruction should say that a local mixed Node.js/Rust project under `/app` produces inconsistent results across repeated local hot-runtime runs and must be repaired so the normal scenario runner writes `/app/outcome/report.json`. The report contains per-scenario records plus aggregate status; the instruction should describe the observable report contract without naming the fix files, lifecycle internals, or numeric answer key.

### Failure topology
The defect is a cross-boundary lifecycle drift: JavaScript constructs rows for local runs, a JavaScript scheduler holds deferred work, another JavaScript layer selects versioned descriptors, a Rust helper normalizes persisted numeric values, and a summary layer folds the rows. Each layer can look plausible in isolation. The failure emerges when repeated local runs combine carried numeric values, deferred items, and descriptor changes.

### Environment shape
Use a small mixed-language repository under `environment/` with an npm runner, a Rust crate invoked from Node, fixtures describing scenarios, neutral documentation, and decoy helpers. Major roots should include `src/core/a1`, `src/core/b2`, `src/core/c3`, `src/core/d4`, `src/core/e5`, `src/core/f6`, `src/native`, `tools`, `fixtures`, `docs`, and `scripts`. Keep file names realistic but opaque on the fix path.

### Required artifacts
Create `instruction.md`, `task.toml`, `output_contract.toml`, `construction_manifest.json`, `environment/Dockerfile`, `environment/.dockerignore`, at least 20 substantive environment files, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. Docker must be offline-complete, digest-pinned, include tmux and asciinema, pin package versions, include lockfiles, use narrow COPY, and set OpenContainers labels. The task is not long_context, not UI, and not multi-container.

### Test plan
- test_alpha_path: checks a simple repeated run keeps carried values consistent.
- test_beta_path: checks aggregate totals match per-record values.
- test_gamma_path: checks the row count and labels for a three-cycle local run.
- test_delta_path: checks deferred work is credited to the correct row.
- test_epsilon_path: checks late deferred work survives a descriptor change.
- test_zeta_path: checks descriptor factors are row-local across changes.
- test_eta_path: checks independent scenarios do not share descriptor values.
- test_theta_path: checks older native rows are normalized before folding.
- test_iota_path: checks mixed native revisions give stable numeric totals.
- test_kappa_path: checks final report status is derived from all scenario invariants.

### Drafting guardrails
Keep the instruction symptoms-only and avoid names such as cache, migration, hook queue, or exact helper locations. Fix-path symbols and path tokens must stay opaque. Tests should derive expected values in Python from embedded scenario definitions, not from environment files. No answer-shaped fixture or golden output may be visible in `environment/`.

### Triviality Ledger
- Naive reset of all memory is blocked because carried numeric values and deferred rows must survive local run boundaries.
- Patching only the Node runner is blocked because native revision rows still produce wrong totals.
- Patching only the Rust helper is blocked because descriptor-local and deferred-row tests still fail.
- Hardcoding scenario answers is discouraged by ten independent scenarios and aggregate cross-checks derived in test code.

### Per-gate Pitfall Inventory
- RC1/RC7/GX3: oracle must add substantive logic across five files, not delete code or rewrite one table.
- RC2/CR7: fix-path file names and symbols use opaque tokens that do not mirror instruction nouns.
- RC3/RC4/RC5: tests assert computed behavior and do not read expected values from mutable environment files.
- RC6/GX6/GX9/GX10: instruction must describe symptoms and output, not causes, exact values, or contradictory polarities.
- GX1: environment comments must avoid bug/fix/correction vocabulary near changed lines.
- CR2: flipping-point locations cover ten tests with no location above the 0.5 cap.
- CR8: no visible orchestrator should name more than two manifest symbols.
- Static Docker checks: Dockerfile must use digest-pinned FROM, pinned apt packages, narrow COPY, .dockerignore, no runtime installs, and the standard offline test.sh template.

### Initial Draft Commitments
- tasks/module-hot-reload-epoch/instruction.md
- tasks/module-hot-reload-epoch/task.toml
- tasks/module-hot-reload-epoch/output_contract.toml
- tasks/module-hot-reload-epoch/construction_manifest.json
- tasks/module-hot-reload-epoch/environment/Dockerfile
- tasks/module-hot-reload-epoch/environment/.dockerignore
- tasks/module-hot-reload-epoch/environment/package.json
- tasks/module-hot-reload-epoch/environment/package-lock.json
- tasks/module-hot-reload-epoch/environment/Cargo.toml
- tasks/module-hot-reload-epoch/environment/Cargo.lock
- tasks/module-hot-reload-epoch/environment/README.md
- tasks/module-hot-reload-epoch/environment/docs/architecture.md
- tasks/module-hot-reload-epoch/environment/docs/operations.md
- tasks/module-hot-reload-epoch/environment/docs/scenario-format.md
- tasks/module-hot-reload-epoch/environment/fixtures/scenarios.json
- tasks/module-hot-reload-epoch/environment/tools/run_matrix.js
- tasks/module-hot-reload-epoch/environment/scripts/clean-local.sh
- tasks/module-hot-reload-epoch/environment/src/core/a1/alpha.js
- tasks/module-hot-reload-epoch/environment/src/core/b2/beta.js
- tasks/module-hot-reload-epoch/environment/src/core/c3/gamma.js
- tasks/module-hot-reload-epoch/environment/src/core/d4/delta.js
- tasks/module-hot-reload-epoch/environment/src/core/e5/epsilon.js
- tasks/module-hot-reload-epoch/environment/src/core/f6/zeta.js
- tasks/module-hot-reload-epoch/environment/src/core/g7/theta.js
- tasks/module-hot-reload-epoch/environment/src/core/h8/iota.js
- tasks/module-hot-reload-epoch/environment/src/native/src/main.rs
- tasks/module-hot-reload-epoch/environment/src/native/src/lib.rs
- tasks/module-hot-reload-epoch/environment/src/native/src/view.rs
- tasks/module-hot-reload-epoch/environment/src/native/README.md
- tasks/module-hot-reload-epoch/solution/solve.sh
- tasks/module-hot-reload-epoch/tests/test.sh
- tasks/module-hot-reload-epoch/tests/test_outputs.py

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table
```json
[
  {
    "path": "src/core/a1/alpha.js",
    "symbol": "f_a",
    "kind": "function",
    "signature": "function f_a(a, b, c)",
    "purpose": "assembles run rows from per-cycle inputs and prior rows"
  },
  {
    "path": "src/core/b2/beta.js",
    "symbol": "q_b",
    "kind": "function",
    "signature": "function q_b(a, b, c)",
    "purpose": "orders deferred items with the current cycle"
  },
  {
    "path": "src/core/c3/gamma.js",
    "symbol": "k_c",
    "kind": "function",
    "signature": "function k_c(a, b, c)",
    "purpose": "derives numeric factors from versioned module descriptors"
  },
  {
    "path": "src/native/src/lib.rs",
    "symbol": "r_d",
    "kind": "function",
    "signature": "pub fn r_d(a: &str, b: i64, c: i64) -> i64",
    "purpose": "normalizes persisted numeric records for the next caller"
  },
  {
    "path": "src/core/d4/delta.js",
    "symbol": "m_e",
    "kind": "function",
    "signature": "function m_e(a, b)",
    "purpose": "folds worker rows into the exported summary"
  }
]
```

#### flipping_point_contract
```json
{
  "locations": [
    {
      "id": "A",
      "path": "src/core/a1/alpha.js",
      "controls_tests": [
        "test_alpha_path",
        "test_beta_path",
        "test_gamma_path"
      ]
    },
    {
      "id": "B",
      "path": "src/core/b2/beta.js",
      "controls_tests": [
        "test_delta_path",
        "test_epsilon_path"
      ]
    },
    {
      "id": "C",
      "path": "src/core/c3/gamma.js",
      "controls_tests": [
        "test_zeta_path",
        "test_eta_path"
      ]
    },
    {
      "id": "D",
      "path": "src/native/src/lib.rs",
      "controls_tests": [
        "test_theta_path",
        "test_iota_path"
      ]
    },
    {
      "id": "E",
      "path": "src/core/d4/delta.js",
      "controls_tests": [
        "test_kappa_path",
        "test_beta_path"
      ]
    }
  ],
  "no_single_location_flips_majority": true,
  "concentration_cap": 0.5
}
```

#### decoy_manifest
```json
[
  {
    "path": "src/core/e5/epsilon.js",
    "kind": "helper",
    "rhymes_with": "f_a",
    "non_fix_purpose": "formats command display data for diagnostics"
  },
  {
    "path": "src/core/f6/zeta.js",
    "kind": "helper",
    "rhymes_with": "q_b",
    "non_fix_purpose": "sorts documentation examples for the local manual"
  },
  {
    "path": "src/native/src/view.rs",
    "kind": "helper",
    "rhymes_with": "r_d",
    "non_fix_purpose": "renders standalone numeric traces for development notes"
  }
]
```

#### code_forbidden_tokens
```json
["runtime", "state", "reload", "migrations", "hooks", "dependencies", "report", "records", "scenario", "counter", "plugin", "runs", "sequence", "work", "output"]
```
