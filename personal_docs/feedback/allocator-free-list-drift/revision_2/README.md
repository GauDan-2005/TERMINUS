# Feedback Snapshot — allocator-free-list-drift / revision_2

Point-in-time capture of Snorkel platform feedback for the TERMINUS task
`allocator-free-list-drift`. Live workspace: `tasks/allocator-free-list-drift/`.

> **Headline:** Still `NEEDS_REVISION`. The platform's revision note reads
> *"AutoEval execution failed. Build status: FAILED."* — but this is **not** a
> Docker/compile failure. The failed build (`995b70b0`) is the **difficulty-check**
> CodeBuild job; it is marked FAILED only because the harness returned
> `solvable=False` (no candidate agent passed the binary threshold). The image
> builds fine and the oracle passes 3/3. The single root cause is a `byte_total`
> spec ambiguity in `instruction.md` that contradicts the test reference model —
> see [Build "Failure" Decoded](#build-failure-decoded) and
> [The byte_total Regression](#the-byte_total-regression-rev1--rev2).

## Submission Identity

| Field | Value |
| --- | --- |
| Task name | allocator-free-list-drift |
| Submission ID | 74fd6fa2-2ca6-46dd-97f1-c88fe2367919 |
| Assignment ID | 8119c063-6ad8-42db-bfd6-c87cf4b40d58 |
| Project | Terminus-2nd-Edition (bfe79c33-8ab0-4061-9849-08d3207c9927) |
| Folder name (platform) | allocator-free-list-drift |
| Submission created | 2026-05-25 13:00 UTC |
| Latest evaluation captured | Eval #3 of 3 — created 2026-05-28 10:47 UTC, updated 11:39 UTC |
| Feedback bundle timestamp | 20260528T234535Z |
| Platform state at capture | NEEDS_REVISION |
| Capture date | 2026-05-29 |
| Revision folder | personal_docs/feedback/allocator-free-list-drift/revision_2/ |

Single submission for this folder (no duplicates). Submission ID matches
`tasks/allocator-free-list-drift/.snorkel_config`.

### Evaluation history on this submission (3 evals, same submission ID)

The submission has been re-evaluated three times (the author updated it in place
via `stb submissions update`, keeping the same ID):

| Eval | Created (UTC) | Updated (UTC) | Outcome | Final build |
| --- | --- | --- | --- | --- |
| #1 | 2026-05-25 13:01 | 2026-05-25 13:47 | **PASS** | all AutoEval builds SUCCEEDED |
| #2 | 2026-05-27 17:42 | 2026-05-27 19:36 | NEEDS_REVISION | build `d5c53485…` FAILED (≈ revision_1 capture) |
| #3 | 2026-05-28 10:47 | 2026-05-28 11:39 | NEEDS_REVISION | build `995b70b0…` FAILED (**this capture**) |

`further_revision_requests_allowed = true`; `rebuttal_notes`, `accept_notes`,
and `user_reviews` are all null. Submission expiry: 2026-10-25 UTC.

## Revision Notes (verbatim from platform)

> AutoEval Execution Summary: AutoEval execution failed. Build status: FAILED.
> Build ID: CodeExecutionEnvironment:995b70b0-8374-44af-bbe2-916d997798a5.

(That single status line is the entire platform note for this evaluation — there
is no free-text reviewer note this round, unlike revision_1.)

## Headline Signals

| Signal | Result |
| --- | --- |
| Difficulty | HARD (confirmed) |
| Solvable status | **NOT solvable by candidate agents** — `solvable=False` |
| AutoEval / difficulty-check build (`995b70b0`) | **FAILED** — solvability gate, *not* a compile/build error |
| Other AutoEval builds + fast_static_checks (`597c13f2`) | SUCCEEDED |
| Task Instruction Sufficiency | **FAIL** (`byte_total` spec ambiguity) |
| Quality check (10 axes) | **10 / 10 PASS** (up from 8/10 in revision_1) |
| Test-quality judge | ROBUST → **ACCEPT** |
| Harness agent review | WARNING (pytest-in-Dockerfile + test.sh format — both repo-convention false positives) |
| `.o` packaging issue (revision_1 blocker) | **RESOLVED** — 0 `.o` files shipped; `.dockerignore` excludes `**/*.o` |

## Agent Performance

| Agent | Runs | Pass | Pass rate |
| --- | --- | --- | --- |
| oracle (reference) | 3 | 3 | 100.0% |
| nop (reference) | 1 | 0 | 0.0% |
| terminus-claude-opus-4-6 | 5 | 0 | **0.0%** |
| terminus-gpt5-2 | 5 | 0 | **0.0%** |

No agent timeouts (`n_agent_timeouts = 0` for every model). All failures are
value-correctness, not infra. Hack check: **no cheating detected** across all 10
trials — every 0.0 reward is legitimate.

## Per-Test Pass Rates (10 runs each)

| Test | Pass / 10 | What it gates | Driver |
| --- | --- | --- | --- |
| test_a0 | **0** | case order + final heap_sig/fl_count/fl_sig/**byte_total** per case | byte_total |
| test_b1 | 10 | run-one.sh single-case envelope | — |
| test_c2 | **0** | cedar per-step heap_sig + **byte_total** | byte_total |
| test_d3 | 10 | (structural) | — |
| test_e4 | 4 | slate fl_count + fl_sig (bidirectional coalesce) | backward coalesce |
| test_f5 | 8 | result_index correctness | minor |
| test_g6 | **0** | onyx final heap_sig + **byte_total** (growth/realloc) | byte_total (+ realloc-move) |
| test_h7 | 4 | pearl final heap_sig + fl_count | realloc-move slot semantics + coalesce |
| test_i8 | 10 | ledger JSONL mirrors steps | — |
| test_j9 | 10 | determinism across two runs | — |
| test_k0 | **0** | every case final **byte_total** (pure byte_total) | byte_total |
| test_l1 | 10 | (structural) | — |

The four 0/10 tests (a0, c2, g6, k0) all assert `byte_total`. The two 4/10 tests
(e4, h7) are coalesce / realloc-move tests, not byte_total.

## Build "Failure" Decoded

The platform note *"AutoEval execution failed. Build status: FAILED. Build ID:
…995b70b0"* is misleading at face value. Deep read of
`metadata/submission_74fd6fa2.json` (high confidence):

- `995b70b0` **is the `difficulty_check` evaluator's CodeBuild job.** Its
  `output_data` is a complete, valid difficulty report (oracle 3/3, nop 0/1,
  both candidate agents 0/5, full per-test matrix, written failure analysis).
- It is marked `build_status=FAILED` **solely because `solvable=False`** — i.e.
  no non-oracle agent passed the binary threshold, so the evaluator returns
  `passed=False` and the wrapping CodeBuild process exits non-zero, which the
  platform surfaces as "Build status: FAILED."
- **No compile / linker / docker-build / architecture / missing-file /
  wrong-format error exists anywhere** in the logs. Greps for `gcc`, `compil*`,
  `docker build`, `x86`, `aarch64`, `wrong format`, `cannot execute`, `No such`
  all return zero hits in the difficulty `output_data`.
- **Not a timeout:** build ran 2026-05-28 10:49:28→11:21:44 UTC (~32 min) vs a
  7200 s ceiling.
- **The image builds everywhere else:** the oracle ran 3/3, and the other
  AutoEval builds + `fast_static_checks` (`597c13f2`) all report SUCCEEDED on the
  same Dockerfile/Makefile/context. `fast_static_checks` has no solvability gate,
  so it cannot "fail" on this.
- **revision_1's `.o` cause is gone:** 0 `.o` files shipped, and the
  `.dockerignore` excludes `**/*.o` and `bin/allocctl`, so the stale-object
  failure cannot recur. The Dockerfile does `make clean && make` from `.c`.

**Conclusion: this is a solvability problem, not an environment problem. Fixing
the `byte_total` spec so agents can pass is what flips the build back to
SUCCEEDED.** Do not chase a Dockerfile/Makefile fix.

## The byte_total Regression (rev1 → rev2)

Diffing the two archived `submitted-task/instruction.md` files shows exactly how
solvability broke between revisions:

- **revision_1 instruction.md did not define the signature formulas at all.** It
  listed the field names only. The better agent (opus-4-6) inferred `byte_total`
  from the corrected C source and the reference model and passed **5/5**; tests
  a0/c2/g6/k0 each passed 5/10. The quality check, however, **failed**
  `behavior_in_task_description` and `structured_data_schema` for the missing
  schema/formula detail.
- **revision_2 instruction.md added line 5** to satisfy that quality check:
  *"After each step, heap_sig sums block_size times 17 over allocated blocks
  only; fl_sig sums free-block sizes; fl_count counts free blocks; **byte_total
  tracks live allocated payload bytes**."* It also added the `report.h` StepRec
  reference, `seq…byte_total`, `index`/`result_index`, the exact case order, and
  the run-one `{"cases":[…]}` envelope clarification.
- **Result:** the schema additions fixed the quality check (now 10/10), but the
  `byte_total` clause is **semantically wrong**. The reference `ModelArena`
  (`tests/test_outputs.py:274`, `rec["byte_total"] = self.allocated`) accumulates
  **full block sizes including the 16-byte header + 8-byte footer, aligned** —
  `align(req + HDR + FTR)` — never the user-requested payload. An agent that
  follows the new wording ("payload bytes") subtracts the overhead and fails every
  byte_total test. 7 of 10 trials fixed all other bugs and failed **only** on
  byte_total.

So the rev1→rev2 edit traded a quality-check failure for a solvability failure.
The fix is to **keep the schema additions but correct the `byte_total`
definition** to match the model (full block bytes incl. HDR+FTR). See
`revision-priorities.md` P0.

### Secondary ambiguity — realloc-move slot indexing

`ModelArena` (`test_outputs.py:247-270`) assigns a **new** slot index on a
relocating realloc (grow that can't be satisfied in place or by forward-merge):
it appends a fresh slot, frees+coalesces the original block, marks the original
slot dead, and reports the **new** index as `result_index`. The instruction never
states this, so an agent that preserves the original index (a reasonable reading)
fails pearl `heap_sig` (trial `rvNb4GD`). Drives part of test_g6 / test_h7.

## Common Failure Patterns (from notes.txt / agent_logs)

1. **Pattern A — Insufficient investigation (3 trials: eKkYeh7, 9eBT7gZ,
   riwDKdt).** Never opened the C sources; validated structure only; passed 6/12
   format tests, failed all value tests.
2. **Pattern B — `byte_total` misinterpretation (7 trials).** Fixed footer
   offset, spurious `+8`, half-copy, and backward coalesce, but read "payload
   bytes" as the requested size → 4 failing tests each. Best agents (UrJ2btN,
   C46aG3j, fxKPJ4J) reached **8/12** — one spec word from passing.
3. **Pattern C — regressions (2 trials).** `zfpGxQ4` over-coalesced during split;
   `NFyNJ3R` rewrote `slot_split.c` introducing new coalesce errors; `rvNb4GD`
   preserved the realloc slot index and failed pearl heap_sig.

No agent reached 9/12. Binary grading turned 67%-correct trajectories into 0.0
reward.

## Quality Check — 10 / 10 PASS (improved from revision_1)

All ten axes pass: `behavior_in_task_description`, `behavior_in_tests`,
`informative_test_structure`, `anti_cheating_measures`, `structured_data_schema`,
`pinned_dependencies`, `typos`, `tests_or_solution_in_image`,
`hardcoded_solution`, `file_reference_mentioned`. The two that failed in
revision_1 (`behavior_in_task_description`, `structured_data_schema`) now pass —
that is exactly the edit that introduced the byte_total regression above.

> Caveat captured in metadata: the quality check and `fast_static_checks` (PASS,
> build `597c13f2`) come from an **earlier successful build**; the **final**
> revision_2 difficulty build (`995b70b0`) FAILED, which drives the
> NEEDS_REVISION outcome.

## Test-Quality Judge — ROBUST / ACCEPT

Verdict: ROBUST, severity None, recommendation ACCEPT. The 12-test suite uses an
independent `ModelArena` reference computed at runtime from the same `.plan`
files, so it cannot be passed by hardcoding or by reading the model; it runs
`make` and asserts the binary exists so compilation cannot be bypassed. Noted
weakness: per-step intermediate validation exists only for cedar; other cases
check final aggregates only. (The judge is positive even though live agents all
failed — the agent-failure analysis separately flags the byte_total wording as
the decisive blocker.)

## Harness Agent Review (agent_review.txt) — WARNING

Two warnings + one suggestion. **Both warnings are known repo-convention false
positives** (see `REPO_CONVENTIONS.md`):

1. **pytest/pytest-json-ctrf installed in Dockerfile (lines 20-22).** Reviewer
   wants them moved to `tests/test.sh`. **Do not apply.** `task.toml` sets
   `[environment].allow_internet = false`, so a runtime `pip install` in test.sh
   would fail offline; the policy requires verifier deps pinned in the image
   build — which is what lines 20-22 already do. Push back.
2. **test.sh "not standard uv format" (lines 1-19).** Reviewer suggests a
   `curl … uv … uv pip install` rewrite. **Do not apply** — those network fetches
   fail under `allow_internet=false`. The submitted `python -m pytest … ; if
   [ $? -eq 0 ]` offline template *is* this repo's canonical verifier shape.
3. *(suggestion, optional)* Add a one-line symptom sentence to instruction.md
   line 1. Reviewer itself rates this "acceptable as-is" for a hard task. If
   applied, keep the terse voice; do not convert to a Task/Output template.

## Directory Layout

```
revision_2/
├── README.md                        (this file)
├── revision-priorities.md
├── rubric.txt                       (12 lines; +27 positive / -15 negative; net 12)
├── feedback/                        (from `stb submissions feedback`)
│   ├── notes.txt
│   ├── agent_review.txt
│   └── agent_logs/
│       ├── analyze-output-tbench-task.json
│       ├── summary-of-runs-comment.md
│       └── jobs/                    (14 trajectories: nop×1, oracle×3, opus-4-6×5, gpt5-2×5)
├── submitted-task/                  (exact uploaded zip — DO NOT EDIT)
│   ├── instruction.md               (line 5 holds the wrong byte_total wording)
│   ├── task.toml
│   ├── environment/                 (Dockerfile, Makefile, include/report.h, src + module dirs; 0 .o files)
│   ├── solution/solve.sh
│   ├── tests/                       (test_outputs.py ModelArena, test.sh)
│   ├── output_contract.toml
│   ├── construction_manifest.json
│   └── .step2b-checksum / .step2b-metrics.jsonl / .snorkel_config
└── metadata/
    ├── submission_74fd6fa2.json     (1.3 MB full assignment payload — keep as-is)
    └── submission_74fd6fa2_summary.json  (trimmed top-level summary)
```

## Notable Config (task.toml / form)

- `[metadata]` difficulty=hard, category=debugging, codebase_size=small,
  languages=[C, shell], milestones=0, expert_estimate=75 min, junior=180 min.
- `[agent].timeout_sec=1800` (30 min); `[verifier].timeout_sec=900`.
- `[environment]` allow_internet=**false**, build_timeout_sec=600, cpus=2,
  memory_mb=4096, storage_mb=10240, gpus=0.
- `task.toml version='2.0'`; `submission_document.solvable=False`,
  `submission_aht=90`, `checkbox_send_to_reviewer=true`.

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

Edit the task at `tasks/allocator-free-list-drift/`. After applying the
byte_total fix (P0) and re-running the cheap Step 2b gates, push with
`stb submissions update 74fd6fa2-2ca6-46dd-97f1-c88fe2367919` from the repo root,
then capture a new `revision_3/` snapshot via this feedback workflow.
