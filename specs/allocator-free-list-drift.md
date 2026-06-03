### Decision

GO — Attempt 1. The allocator stress-audit idea is shaped into a single-container hard debugging task with symptoms gated on split, coalesce, realloc relocation, and byte accounting under scripted sequences. The planned fix surface is distributed across boundary-tag maintenance, free-list linking, relocation copy sizing, and accounting updates so no one location can satisfy the verifier. The public contract stays behavioral: the heap audit must agree with the scripted sequences, but the instruction must not name tag layouts, list splice rules, or copy bounds as causes.

### Metadata

- version: 2
- Task name: allocator-free-list-drift
- Title: Heap Stress Audit Drift
- Category: debugging
- Languages: ["C", "shell"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["c", "allocator", "heap", "debugging", "memory"]
- Milestones: 0

## Authoring Brief

This file is the only drafting input for Step 2b. Do not include reviewer-only notes, oracle patch recipes, or a full solution walkthrough in solver-visible files.

### Public contract

Create a standard task in which the agent repairs a local heap stress harness under `/app`. The user-facing goal is that the shipped audit command produces `/app/output/alloc-audit.json` showing each scripted scenario reports clean status with heap layout, free-list shape, and byte accounting aligned to the sequence ledger. The instruction should mention the output path, that the JSON report identifies the checked scenarios, and that agreement covers per-step records, heap block layout, free-list nodes, and accounting totals. It must not prescribe tag encodings, list splice algorithms, relocation copy sizes, or exact file names on the fix path.

The verifier should run the repaired harness across six shipped scenarios, then parse the generated report and independently re-derive expectations from the scenario scripts. A valid solution may rework internal block metadata, list wiring, relocation helpers, or tally routines, as long as the observable audit contract is satisfied without replacing the harness or weakening checks.

### Failure topology

The visible symptom is audit drift that only appears under scripted stress: block splitting leaves inconsistent boundary metadata, freeing adjacent regions fails to merge the full span, growing reallocations copy the wrong span when relocation is required, and byte tallies diverge from the live heap. Smoke-length sequences can look healthy while the matrix scenarios fail. The hard part is reconstructing how tag maintenance, list linking, relocation, and accounting interact across opaque module roots.

### Environment shape

Use a single Docker image with a small C codebase: a control binary, neutral internal module directories, scenario scripts under `data/cases/`, shell orchestration, config and documentation, and at least 20 files under `environment/` excluding Dockerfile. Keep decoy helpers that rhyme structurally with fix-path modules but perform non-fix work.

### Required artifacts

Step 2b must create the standard layout with `instruction.md`, `task.toml`, `output_contract.toml`, `construction_manifest.json`, digest-pinned `environment/Dockerfile`, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. Single-container, non-UI, hard difficulty, `[environment].allow_internet = false`.

### Test plan

- `test_a0`: matrix command; six cases cedar through pearl; each `ok` true.
- `test_b1`: direct-case helper matches matrix slice.
- `test_c2`: cedar basic sequence accounting and heap signature.
- `test_d3`: jade split-heavy layout and free-list shape.
- `test_e4`: slate coalesce free-list node count and sizes.
- `test_f5`: coral in-place realloc stable pointer slot and tags.
- `test_g6`: onyx reloc realloc heap block migration.
- `test_h7`: pearl mixed stress end-state.
- `test_i8`: ledger JSONL order matches steps array.
- `test_j9`: two matrix runs deterministic.
- `test_k0`: accounting bytes match model for all cases.
- `test_l1`: slate free-list signature after middle free.

### Drafting guardrails

Symptoms-only instruction; opaque fix-path symbols; no golden audit under `environment/`; tests re-derive expectations from `.plan` files; oracle substantive across four roots; CR8 limits symbols per visible orchestration file.

### Triviality Ledger

- Canned `/app/output/alloc-audit.json` blocked: verifier deletes output and regenerates via matrix and direct runs.
- One-file list-only patch blocked: split, coalesce, reloc, and accounting tested separately.
- Accounting-only patch blocked: heap signatures and free-list nodes fail independently.
- Tag-only patch blocked: coalesce and realloc cases still fail.
- Prompt-grep patch blocked: opaque module roots and `code_forbidden_tokens`.

### Per-gate Pitfall Inventory

- RC1/RC7: substantive `solve.sh` across tag, list, move, acct modules (≥80 semantic LOC).
- RC6/GX9/GX10: symptoms-only; no per-case answer recital.
- CR1/CR2/CR8: manifest verbatim; four flip locations; ≤2 symbols per orchestration file.
- Docker: tmux, asciinema, digest-pinned FROM, narrow COPY, `.dockerignore`.
- NOP/oracle: broken baseline fails domain assertions; oracle deterministic.

### Initial Draft Commitments

- `tasks/allocator-free-list-drift/instruction.md`
- `tasks/allocator-free-list-drift/task.toml`
- `tasks/allocator-free-list-drift/output_contract.toml`
- `tasks/allocator-free-list-drift/construction_manifest.json`
- `tasks/allocator-free-list-drift/environment/Dockerfile`
- `tasks/allocator-free-list-drift/environment/Makefile`
- `tasks/allocator-free-list-drift/environment/include/arena.h`
- `tasks/allocator-free-list-drift/environment/include/block.h`
- `tasks/allocator-free-list-drift/environment/include/plan.h`
- `tasks/allocator-free-list-drift/environment/include/report.h`
- `tasks/allocator-free-list-drift/environment/pool_a/tag.c`
- `tasks/allocator-free-list-drift/environment/list_b/list.c`
- `tasks/allocator-free-list-drift/environment/split_c/split.c`
- `tasks/allocator-free-list-drift/environment/move_d/move.c`
- `tasks/allocator-free-list-drift/environment/acct_e/acct.c`
- `tasks/allocator-free-list-drift/environment/read_f/parse.c`
- `tasks/allocator-free-list-drift/environment/flow_g/report.c`
- `tasks/allocator-free-list-drift/environment/drive_h/run.c`
- `tasks/allocator-free-list-drift/environment/src/main.c`
- `tasks/allocator-free-list-drift/environment/spill_i/spill.c`
- `tasks/allocator-free-list-drift/environment/mirror_j/mirror.c`
- `tasks/allocator-free-list-drift/environment/config/limits.toml`
- `tasks/allocator-free-list-drift/environment/docs/operations.md`
- `tasks/allocator-free-list-drift/environment/docs/layout.md`
- `tasks/allocator-free-list-drift/environment/data/cases/cedar.plan`
- `tasks/allocator-free-list-drift/environment/data/cases/jade.plan`
- `tasks/allocator-free-list-drift/environment/data/cases/slate.plan`
- `tasks/allocator-free-list-drift/environment/data/cases/coral.plan`
- `tasks/allocator-free-list-drift/environment/data/cases/onyx.plan`
- `tasks/allocator-free-list-drift/environment/data/cases/pearl.plan`
- `tasks/allocator-free-list-drift/environment/scripts/run-matrix.sh`
- `tasks/allocator-free-list-drift/environment/scripts/run-one.sh`
- `tasks/allocator-free-list-drift/environment/scripts/clean-room.sh`
- `tasks/allocator-free-list-drift/tests/test.sh`
- `tasks/allocator-free-list-drift/tests/test_outputs.py`
- `tasks/allocator-free-list-drift/solution/solve.sh`

### Construction manifest (BLOCKING — Step 2b must follow this verbatim)

#### symbol_table

```
- path: pool_a/tag.c
  symbol: op_a
  kind: function
  signature: void op_a(Block *a, size_t b)
  purpose: Writes boundary size words for a block span.
- path: list_b/list.c
  symbol: fold_b
  kind: function
  signature: void fold_b(Arena *a, Block *b)
  purpose: Splices a free block into the intrusive list.
- path: split_c/split.c
  symbol: mark_c
  kind: function
  signature: Block *mark_c(Arena *a, Block *b, size_t c)
  purpose: Splits an allocated block and returns the remainder free piece.
- path: move_d/move.c
  symbol: bind_d
  kind: function
  signature: int bind_d(void *a, void *b, size_t c)
  purpose: Copies payload bytes during relocation.
- path: acct_e/acct.c
  symbol: note_e
  kind: function
  signature: void note_e(Stats *a, ssize_t b)
  purpose: Adjusts live byte tallies after heap mutations.
- path: flow_g/report.c
  symbol: emit_e
  kind: function
  signature: int emit_e(const CaseResult *a, const char *b)
  purpose: Writes JSON audit and companion ledger for one scenario.
```

#### flipping_point_contract

```
locations:
  - id: A
    path: pool_a/tag.c
    controls_tests: [test_a0, test_d3, test_j9]
  - id: B
    path: list_b/list.c
    controls_tests: [test_e4, test_l1, test_h7]
  - id: C
    path: move_d/move.c
    controls_tests: [test_f5, test_g6, test_b1]
  - id: D
    path: acct_e/acct.c
    controls_tests: [test_c2, test_k0, test_i8]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest

```
- path: spill_i/spill.c
  kind: helper
  rhymes_with: fold_b
  non_fix_purpose: Buckets small integers for documentation tables.
- path: mirror_j/mirror.c
  kind: helper
  rhymes_with: emit_e
  non_fix_purpose: Formats stderr diagnostics not used in the audit path.
```

#### code_forbidden_tokens

```
code_forbidden_tokens: [heap, stress, harness, audit, scripted, scenarios, matrix, output, JSON, cases, sequence, ledger, agreement, covers, step, records, layout, free, list, nodes, accounting, totals, clean, status, cedar, jade, slate, coral, onyx, pearl, name, ok, steps, freelist, blocks, bytes, peak, block, pointer, slot, relocation, split, coalesce]
```
