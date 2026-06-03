### Decision

GO — Attempt 1.

- Turn-based grid simulator with mid-run persistence and perception-driven hostile turns fits the games category as a hard debugging task.
- Fix surface spans snapshot packing, cache merge on restore, timed modifier epochs, and planner inputs so no single module satisfies the verifier.
- Public contract stays behavioral: resumed hostile turns must stay legal under the bundled tables; the instruction does not name serialization order, cache keys, or planner hooks.

### Metadata

- version: 2
- Task name: fog-state-resume
- Title: Fog Resume Desync
- Category: games
- Languages: ["Go", "shell"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["roguelike", "save-load", "fog-of-war", "ai", "go"]
- Milestones: 0

## Authoring Brief

### Public contract

Repair the local turn-based grid simulator under `/app`. Running `bash /app/scripts/run-matrix.sh` must write `/app/output/resume-audit.json` where every matrix row for rook, bishop, knight, lancer, sentinel, and warden has `ok` true. The bundled layout and script tables under `/app/data` and `/app/config` are authoritative inputs; fix the simulator rather than editing those tables or hardcoding row totals. Uninterrupted fresh runs and resumed runs after a checkpoint must agree on resolved move history and signatures where the instruction describes agreement; resumed hostile turns must not step through blocked tiles or strike from tiles the player cannot see under the sight and legality tables.

### Failure topology

Illegal hostile steps appear only after restoring a checkpoint taken while hidden tiles, timed modifiers, and perception state interact. Each condition looks ordinary alone; the bad moves emerge when restore reuses stale observation data or misaligned modifier epochs.

### Environment shape

Single Docker image with Go command `rogctl`, opaque internal packages, small C legality helper, shell drivers, config tables, layout files, and subsystem docs. At least 20 files under `environment/` excluding Dockerfile.

### Test plan

- `test_rook_row` through `test_warden_row`: each asserts one case `ok` true plus cross-checks on move legality, visibility consistency, effect flags, uninterrupted versus restored path agreement, and sidecar ordering. Values re-derived in verifier code from layouts and config, not env golden JSON.

### Triviality Ledger

- Snapshot-only trap: blocked because perception cache and planner inputs are tested separately.
- Cache-only trap: blocked because effect epochs and wall legality are independently verified.
- Table-edit trap: blocked because tests recompute expectations from bundled inputs.
- Harness-replacement trap: blocked because tests parse move logs and independently check tile legality.
- One-case patch trap: six profiles combine fog timing, modifiers, and multi-hostile layouts.

### Per-gate Pitfall Inventory

- RC1–RC7, GX1, GX3, GX9, GX10: standard Edition 2 guardrails for games debugging task.
- Static: digest-pinned Dockerfile, tmux/asciinema, canonical test.sh footer, output_contract.toml.

### Initial Draft Commitments

- Standard layout under `tasks/fog-state-resume/` with files listed in construction manifest below.

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: internal/a0/pack.go
  symbol: phase_a
  kind: function
  signature: func phase_a(a *stateX, b itemY) error
  purpose: merges world tiles and observation masks into a persisted blob
- path: internal/b1/cache.go
  symbol: fold_b
  kind: function
  signature: func fold_b(a *cacheX, b itemY) error
  purpose: applies a restored blob onto the live perception cache
- path: internal/c2/effect.go
  symbol: mark_c
  kind: function
  signature: func mark_c(a *mapX, b uint64, c []entryX) error
  purpose: rebases timed modifier epochs after a checkpoint boundary
- path: internal/d3/plan.go
  symbol: bind_d
  kind: function
  signature: func bind_d(a *nodeX, b tokenX, c []int) (int, int, bool)
  purpose: chooses the next hostile step from planner inputs
- path: probe/legality.c
  symbol: walk_e
  kind: function
  signature: int walk_e(struct qx *a, int x0, int y0, int x1, int y1)
  purpose: validates a step against wall tiles for the Go caller
```

#### flipping_point_contract

```
locations:
  - id: A
    path: internal/a0/pack.go
    controls_tests: [test_rook_row, test_knight_row]
  - id: B
    path: internal/b1/cache.go
    controls_tests: [test_bishop_row, test_warden_row]
  - id: C
    path: internal/c2/effect.go
    controls_tests: [test_sentinel_row, test_warden_row]
  - id: D
    path: internal/d3/plan.go
    controls_tests: [test_knight_row, test_warden_row]
  - id: E
    path: probe/legality.c
    controls_tests: [test_lancer_row, test_warden_row]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: internal/g6/render.go
  kind: helper
  rhymes_with: phase_a
  non_fix_purpose: formats ASCII map previews for dry-run CLI output
- path: internal/h7/stats.go
  kind: helper
  rhymes_with: mark_c
  non_fix_purpose: aggregates profile counters for documentation only
- path: probe/list.c
  kind: helper
  rhymes_with: walk_e
  non_fix_purpose: shallow tile listing for diagnostics outside the audit path
```

#### code_forbidden_tokens

```
code_forbidden_tokens: [roguelike, simulator, checkpoint, hostile, player, blocked, tiles, strike, sight, legality, tables, matrix, audit, cases, fresh, resume, moves, visibility, effects, records, log, signatures, agreement, scripts, config, layouts, scenarios, runner, completion]
```
