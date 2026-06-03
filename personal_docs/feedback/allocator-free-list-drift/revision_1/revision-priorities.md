# Revision Priorities — allocator-free-list-drift (revision_1)

Submission `74fd6fa2-2ca6-46dd-97f1-c88fe2367919` is in NEEDS_REVISION. Both
the platform reviewer note and the automated quality check converge on two
blockers: an incomplete output schema in `instruction.md`, and stale
architecture-specific object files shipped in the environment.

## P0 — Platform Blockers (must fix to clear NEEDS_REVISION)

1. **Remove shipped `.o` files / force clean build.** Reviewer's local oracle
   build failed because `make` linked stale x86-64 objects on an ARM host.
   - Delete every `.o` under `environment/` (18 files in pool_a, list_b,
     split_c, move_d, acct_e, read_f, flow_g, drive_h, mirror_j, spill_i, src)
     before re-zipping.
   - Add `make clean &&` in front of `make` in the Dockerfile (or drop the
     `.o` files entirely and rely on the build).
   - Verify the package contains no precompiled binaries
     (`find environment -name '*.o' -o -name 'allocctl'`).

2. **Fully specify output schema in `instruction.md`.** Tests assert step and
   ledger row fields that the instruction does not mention.
   - Document the per-step fields: `seq`, `op`, `index`, `size`,
     `result_index`, `heap_sig`, `fl_count`, `fl_sig`, `byte_total`.
   - Document the ledger JSONL row fields (same shape as steps plus the
     ordering invariant).
   - State the required case order: `cedar, jade, slate, coral, onyx, pearl`.
   - Clarify that `run-one.sh` output keeps the top-level `{"cases": [...]}`
     wrapper (single-element array) — this is the "same rules" the current
     prose hints at.
   - Adding a 5–10 line JSON example block (placeholder values) is the lowest
     risk way to address both this and the agent-review schema warning.

3. **Optional but recommended: document the signature formulas at a high
   level.** Specify that `heap_sig` is summed over *allocated* blocks (not
   free), and give the accumulator (`sig += total * 17`) so an agent cannot
   re-invent MurmurHash. This was a concrete failure mode (`WpMWU7F`).

## P1 — Instruction Sufficiency / Agent Failure Drivers

1. **Move pytest from Dockerfile to `tests/test.sh`.** Harness agent review
   flagged this. The agent does not need pytest at runtime — only the
   verifier does. Remove
   `pytest==8.4.1` and `pytest-json-ctrf==0.3.5` from the Dockerfile and add
   them to `tests/test.sh` before `pytest` is invoked.

2. **Add explicit guidance to consult `tests/test_outputs.py`/the reference
   model.** Without this prompt, agents stop at "exit code 0 + JSON valid"
   and never inspect numerical correctness. Either:
   - Add a hint in the instruction ("check that your audit values match a
     reference implementation in `tests/test_outputs.py`"), OR
   - Add a small `docs/` cheatsheet inside the environment that names the
     four buggy modules (pool_a, list_b, move_d, acct_e) without giving the
     fix.

## P2 — Convention Nits / Quality of Life

1. **Pin `make clean` semantics.** Currently the Makefile may have no
   `.PHONY: clean` rule; verify a `make clean && make` cycle is well-formed.
2. **Confirm `tests/test.sh` does not need pytest install when run via
   harness.** If harness runs verifier outside the image, ensure install
   logic is in test.sh and exits cleanly when packages already present.

## P3 — Already Passing (no change needed)

- `behavior_in_tests` — instruction-described behaviors are all tested.
- `informative_test_structure` — docstrings + grouping present.
- `anti_cheating_measures` — expected values computed by ModelArena; no copy
  of tests/solution into image.
- `pinned_dependencies` — base image pinned by SHA256, apt/pip pinned.
- `typos` — none.
- `tests_or_solution_in_image` — Dockerfile only copies environment subdirs.
- `hardcoded_solution` — solution rebuilds from source via Python rewrites.
- `file_reference_mentioned` — `/app/output/...` paths cross-referenced.
- Oracle 3/3 + Claude 5/5 — solvability proven; difficulty rating HARD is
  not under dispute.

## Tests Agents Never Pass — None

Every test passes for at least one agent run (test_i8 and test_j9 reach
10/10). The half-passing tests (a0, c2, e4, g6, h7, k0) are the
ModelArena-correctness checks that gate on the four C bugs being fixed —
they are doing exactly the gating they should.

## Suggested Change Order

1. Delete `.o` files, add `make clean`, re-build locally to confirm portable
   build (P0.1).
2. Expand `instruction.md` with the full step/ledger schema + required order
   + JSON example + signature formula hint (P0.2 + P0.3 + P1.2).
3. Move pytest install to `tests/test.sh` (P1.1).
4. Re-zip, `stb submissions update 74fd6fa2-2ca6-46dd-97f1-c88fe2367919`,
   capture new `revision_2/` snapshot via the feedback workflow.
