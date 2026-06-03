# Feedback Snapshot — allocator-free-list-drift / revision_1

Point-in-time capture of Snorkel platform feedback for the TERMINUS task
`allocator-free-list-drift`. Live workspace: `tasks/allocator-free-list-drift/`.

## Submission Identity

| Field | Value |
| --- | --- |
| Task name | allocator-free-list-drift |
| Submission ID | 74fd6fa2-2ca6-46dd-97f1-c88fe2367919 |
| Assignment ID | 8119c063-6ad8-42db-bfd6-c87cf4b40d58 |
| Project | Terminus-2nd-Edition (bfe79c33-8ab0-4061-9849-08d3207c9927) |
| Submission created | 2026-05-25 13:00 UTC |
| Platform state at capture | NEEDS_REVISION |
| Capture date | 2026-05-27 |
| Revision folder | personal_docs/feedback/allocator-free-list-drift/revision_1/ |

## Revision Notes (verbatim from platform)

> Platform feedback summary:
> The platform shows HARD difficulty and solvable status with oracle 3/3, but
> instruction sufficiency fails and the quality check fails
> behavior_in_task_description plus structured_data_schema. The main platform
> issue is that several output details tested by the verifier are not specified
> in instruction.md.
>
> Local verification summary:
> I inspected task.toml, instruction.md, Dockerfile, Makefile, tests, shipped
> files, and platform feedback. Runtime test.sh does not fetch dependencies,
> which is correct for allow_internet=false. My local oracle could not complete
> because the Docker build failed while linking shipped object files: the
> archive includes x86-64 .o files and make links those stale objects on this
> ARM reviewer machine, producing file in wrong format.
>
> Blocking instruction/schema issues:
> instruction.md lists case-level fields but does not fully specify the nested
> step and ledger schemas. Tests require step fields such as seq, op, index,
> size, result_index, heap_sig, fl_count, fl_sig, and byte_total, and ledger
> JSONL rows mirroring those values. The tests also require the cases array to
> be ordered exactly as cedar, jade, slate, coral, onyx, pearl. Please document
> these schema and ordering requirements explicitly, or soften the tests.
>
> Blocking packaging/build issue:
> Remove precompiled .o files from the task zip and make sure Docker builds
> objects from source, for example by running make clean before make or not
> shipping object files at all. The current package is architecture-sensitive
> and fails local build on ARM because Make sees the stale .o files and links
> them instead of recompiling.
>
> Decision:
> Needs Revision until the output schema/order is fully specified and the
> shipped binary/object artifacts are removed or rebuilt from source in a
> portable way.

## Headline Signals

| Signal | Result |
| --- | --- |
| Difficulty | HARD (confirmed) |
| Solvable status | Solvable (oracle 3/3, terminus-claude-opus-4-6 5/5) |
| Task Instruction Sufficiency | FAIL |
| AutoEval build | FAIL on reviewer ARM machine (stale x86-64 .o files linked) |
| Quality check — behavior_in_task_description | FAIL |
| Quality check — structured_data_schema | FAIL |
| Quality check — behavior_in_tests | PASS |
| Quality check — informative_test_structure | PASS |
| Quality check — anti_cheating_measures | PASS |
| Quality check — pinned_dependencies | PASS |
| Quality check — typos | PASS |
| Quality check — tests_or_solution_in_image | PASS |
| Quality check — hardcoded_solution | PASS |
| Quality check — file_reference_mentioned | PASS |
| Harness review | WARNING (pytest in Dockerfile; terse JSON schema) |

## Agent Performance

| Agent | Runs | Pass | Pass rate |
| --- | --- | --- | --- |
| terminus-claude-opus-4-6 | 5 | 5 | 100.0% |
| terminus-gpt5-2 | 5 | 0 | 0.0% |
| oracle (reference) | 3 | 3 | 100.0% |
| nop (reference) | 1 | 0 | 0.0% |

Note: revision-notes table says oracle 3/3 + claude 5/5 succeed, gpt5 0/5 — task
is solvable but unevenly. Per-trial difficulty analysis still flagged
instruction sufficiency as FAIL (2/5 trials flagged `task_specification: fail`).

## Per-Test Pass Rates (10 runs each)

| Test | Pass / 10 |
| --- | --- |
| test_a0 | 5 |
| test_b1 | 8 |
| test_c2 | 5 |
| test_d3 | 9 |
| test_e4 | 5 |
| test_f5 | 9 |
| test_g6 | 5 |
| test_h7 | 5 |
| test_i8 | 10 |
| test_j9 | 10 |
| test_k0 | 5 |
| test_l1 | 9 |

The weakest tests (5/10) are the cases tied to numerical correctness of the
allocator (a0, c2, e4, g6, h7, k0); the high-passing ones (i8, j9) are the
ledger-order and determinism checks.

## Common Failure Patterns (from notes.txt)

1. **Surface validation mistaken for correctness.** Agents ran the scripts, saw
   exit code 0, valid JSON, two identical runs → declared victory. None
   consulted `/tests/test_outputs.py` where `ModelArena` defines expected
   values.
2. **Unfixed C bugs across 5/5 trials:**
   - Off-by-8 byte accounting in `acct_e/acct.c` (`byte_total` inflated, e.g.
     264 vs 240 for cedar).
   - Broken bidirectional coalescing in `list_b/list.c` (`fl_count` too high:
     slate 2 vs 1, pearl 3 vs 2).
   - Wrong footer position in `pool_a/tag.c` (downstream accounting errors).
   - Buggy memory copy in `move_d/move.c` (wrong `byte_total` for realloc,
     onyx: 1504 vs 1464).
3. **Self-inflicted regressions.** `QJ7BGKG` and `5e4xtC2` rewrote
   `flow_g/report.c` to drop the `{"cases": [...]}` wrapper in `run-one.sh`
   output, breaking `test_b1`. Both misread "same rules" as a bug.
4. **Worst-case misdiagnosis.** `WpMWU7F` interpreted "drift" as
   non-determinism and replaced `sig += total * 17` with a MurmurHash-XOR
   accumulator — produced massive integers and failed 9/12 tests.

## Instruction Gaps Identified

- Step-record fields (`seq`, `op`, `index`, `size`, `result_index`, `heap_sig`,
  `fl_count`, `fl_sig`, `byte_total`) are never named in `instruction.md`.
- Ledger JSONL row fields are not documented.
- `cases` array must be ordered exactly `cedar, jade, slate, coral, onyx, pearl`
  — order requirement is not stated.
- `heap_sig` formula (sum over *allocated* blocks, not free blocks),
  `fl_sig`, and `byte_total` formulas are only encoded in `ModelArena`.
- "Same rules" for `run-one.sh` output is ambiguous about the `{"cases": [...]}`
  wrapper.

## Packaging / Build Issues

- Stale precompiled `.o` files shipped under `environment/` (acct_e, drive_h,
  flow_g, list_b, mirror_j, move_d, pool_a, read_f, spill_i, split_c, and 8
  more under `src/`). Linker pulls these in on ARM hosts → "file in wrong
  format" build failure.
- Need to either drop the `.o` artifacts, add a `make clean` in the Dockerfile
  before `make`, or only ship sources.

## Harness Review (agent_review.txt) — WARNING

1. pytest + pytest-json-ctrf installed in Dockerfile; should move to
   `tests/test.sh` so the agent container is not polluted with test tooling.
2. Instruction JSON schema is too terse — recommend adding a short JSON example
   with field types.

## Directory Layout

```
revision_1/
├── README.md                        (this file)
├── revision-priorities.md
├── rubric.txt                       (copied from personal_docs/rubrics/)
├── feedback/                        (from `stb submissions feedback`)
│   ├── notes.txt
│   ├── agent_review.txt
│   └── agent_logs/
│       ├── analyze-output-tbench-task.json
│       ├── summary-of-runs-comment.md
│       └── jobs/                    (15 per-trial trajectories)
├── submitted-task/                  (exact uploaded zip — DO NOT EDIT)
│   ├── instruction.md
│   ├── task.toml
│   ├── environment/                 (contains stale .o files — issue #2)
│   ├── solution/
│   └── tests/
└── metadata/
    ├── submission_74fd6fa2.json
    └── submission_74fd6fa2_summary.json
```

## Refresh Commands

```bash
cd "/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS"

# Refresh feedback bundle (writes new /tmp/feedback_<id>_<ts>/)
stb submissions feedback 74fd6fa2-2ca6-46dd-97f1-c88fe2367919

# Re-download submitted zip
stb submissions download 74fd6fa2-2ca6-46dd-97f1-c88fe2367919 \
    -o personal_docs/feedback/allocator-free-list-drift/revision_<N>/submitted-task

# Re-fetch full assignment metadata
stb submissions fetch-task 74fd6fa2-2ca6-46dd-97f1-c88fe2367919 \
    -o personal_docs/feedback/allocator-free-list-drift/revision_<N>/metadata

# Browser view
stb submissions view 74fd6fa2-2ca6-46dd-97f1-c88fe2367919
```

## Live Workspace

Edit the task at `tasks/allocator-free-list-drift/` and then run
`stb submissions update 74fd6fa2-2ca6-46dd-97f1-c88fe2367919` from the repo
root once revisions are ready. Capture a new revision_N folder after each
update.
