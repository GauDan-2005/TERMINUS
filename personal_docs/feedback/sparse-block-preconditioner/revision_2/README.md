# sparse-block-preconditioner — Revision 2 feedback snapshot

Point-in-time archive of platform feedback for the `sparse-block-preconditioner`
task, captured **2026-05-28**. This is the snapshot of the **re-evaluation that
ran after an `stb submissions update`** (the revision that addressed the
revision_1 findings).

**Headline:** the revision over-corrected. All of the revision_1 blockers were
fixed (anti-cheating/test-quality gap, instruction sufficiency, canary string),
but the task **collapsed from HARD → TRIVIAL** and is back in **NEEDS_REVISION**
for that reason. Every other automated check now passes.

## Submission identity

| Field                  | Value                                                         |
| ---------------------- | ------------------------------------------------------------- |
| Folder name            | `sparse-block-preconditioner`                                 |
| Submission ID          | `64f78238-acf5-4cce-ba2a-100ea9b5a20f`                        |
| Assignment ID          | `961990f5-3736-4942-bc08-2fd732041f9b`                        |
| Task ID                | `64f78238-acf5-4cce-ba2a-100ea9b5a20f`                        |
| Project                | Terminus-2nd-Edition (`bfe79c33-8ab0-4061-9849-08d3207c9927`) |
| Submission task type   | `submission-941bede0-d9c6-42f0-874d-cd3d25582c72`             |
| Current platform state | **NEEDS_REVISION**                                            |
| Further revisions      | allowed (`further_revision_requests_allowed: true`)           |
| Assignment expiry      | 2026-10-25T16:44:05Z                                          |
| Captured at            | 2026-05-28                                                    |

### Evaluation history (two evaluations on this submission)

| # | Created (UTC)        | Updated (UTC)        | AutoEval outcome | Notes                                            |
| - | -------------------- | -------------------- | ---------------- | ------------------------------------------------ |
| 0 | 2026-05-25 15:56:41  | 2026-05-25 17:59:05  | PASS             | Original eval. Human reviewer → NEEDS_REVISION (test-quality / anti-cheating gap). Captured in **revision_1**. |
| 1 | 2026-05-28 16:00:13  | 2026-05-28 16:44:05  | **NEEDS_REVISION** | Re-eval after `stb submissions update`. Difficulty gate failed (TRIVIAL). **This snapshot.** |

Submitted artifact at capture: `submitted-task/` (extracted from
`sparse-block-preconditioner.zip`, 34.69 KB). The `download` command extracts in
place and does not retain the zip itself. Do not edit anything under
`submitted-task/` — it is the exact uploaded artifact reviewers evaluated.
`submitted-task/instruction.md`, `tests/test_outputs.py`, and the environment are
**byte-identical** to the current `tasks/sparse-block-preconditioner/` workspace
at fetch time.

## Revision notes (verbatim from platform)

> AutoEval Execution Summary: AutoEval execution failed. Build status: FAILED.
> Build ID: CodeExecutionEnvironment:e8ae1615-bd75-49b6-92de-9c8ef2fd41fd.

> [!IMPORTANT]
> **This wording is misleading.** Build `e8ae1615` is the **difficulty_check**
> evaluator, and its `output_data` shows it ran to completion and produced a
> full difficulty report. There was **no Docker/infrastructure build error.**
> The platform marks a check's `build_status` as `FAILED` whenever the check
> returns a non-passing verdict; here the verdict is **difficulty = TRIVIAL**
> (requires at least MEDIUM). The real and only blocker is the difficulty
> collapse, not a broken image. The five other CodeBuild sub-checks all
> SUCCEEDED.

## Headline signals (2026-05-28 evaluation)

| Check (evaluator)            | Build       | Result                                                       |
| ---------------------------- | ----------- | ------------------------------------------------------------ |
| plagiarism (shadow)          | —           | PASS — no plagiarism                                          |
| deduplication                | —           | PASS — no duplication (`min_edit_distance_ratio` 1.0)        |
| long_context_check           | 5b32176c ✅ | PASS — not a long_context task, skipped; all static checks passed |
| codebase_applicability       | 7fd39097 ✅ | PASS — genuine C++/CMake codebase (`is_real_code_base: true`) |
| tb_check (quality, 10-axis)  | bf24d356 ✅ | **PASS — all 10 axes pass** (was 1 FAIL in revision_1)       |
| test_quality_judge           | e723c95b ✅ | **ROBUST / ACCEPT, Severity None** (was VULNERABLE-Critical in revision_1) |
| **difficulty_check**         | e8ae1615 ❌ | **TRIVIAL — requires at least MEDIUM** → NEEDS_REVISION       |
| claude_code_reviewer         | 5076ff18 ✅ | WARNING (pytest in Dockerfile) — **READY TO USE**            |
| **Final platform decision**  |             | **NEEDS_REVISION** (single driver: difficulty)               |

### Quality check (10 axes) — all PASS this round

`behavior_in_task_description` (the lone FAIL in revision_1) now PASSES — the
instruction enumerates the JSON fields and the required behaviors and the
independent-measurement language aligns with the test's `reference_row()`. The
other nine axes pass as before: `behavior_in_tests`, `informative_test_structure`,
`anti_cheating_measures`, `structured_data_schema`, `pinned_dependencies`,
`typos`, `tests_or_solution_in_image`, `hardcoded_solution`,
`file_reference_mentioned`.

## Agent performance (difficulty_check)

**Difficulty: ❌ TRIVIAL — Requires at least MEDIUM. Solvable: ✅**

| Agent                       | Runs | Successes | Timeouts | Other fail | Accuracy |
| --------------------------- | ---- | --------- | -------- | ---------- | -------- |
| nop                         | 1    | 0         | 0        | 1          | 0.0      |
| oracle                      | 3    | 3         | 0        | 0          | 1.0      |
| terminus-claude-opus-4-6    | 5    | 5         | 0        | 0          | 1.0      |
| terminus-gpt5-2             | 5    | **5**     | 0        | 0          | **1.0**  |

Per-test pass rate: **all 13 tests 10 / 10.** The three tests gpt5 never passed
in revision_1 (`test_h7_opal_mixed_reordered_residuals`,
`test_i8_reported_matches_true_residual`, `test_z9_row_status_flags`) now pass
10/10. nop scores 0.0 (1 "other" failure — correct: an empty solution cannot
build/produce output).

`Task Instruction Sufficiency` analysis: **NOT_APPLICABLE** (debug output not
available — the analysis only runs when there are agent failures to explain, and
this round had none).

## Why difficulty collapsed — diff vs revision_1

Three edits between the two captures:

1. **`instruction.md` (+2 lines)** — added a final paragraph:
   > *"Repair the shipped solver for reordered layouts, not only the audit
   > scripts. Every row needs `ok` true and matching residual columns; equivalent
   > JSON between reruns is necessary but not sufficient."*
2. **`tests/test_outputs.py` (168 → 392 lines)** — added a full independent
   Python PCG reference implementation that recomputes expected iterations /
   residuals / flags from the case data (the anti-cheating fix).
3. **`solution/solve.sh`** — removed the legacy
   `# Terminal-Bench Canary, do not remove` line.

Effect map:

| revision_1 finding                                    | revision_2 status |
| ----------------------------------------------------- | ----------------- |
| Test-quality / anti-cheating gap (self-reported vals) | ✅ FIXED — test_quality_judge now ROBUST |
| `behavior_in_task_description` quality FAIL           | ✅ FIXED — all 10 axes pass |
| Legacy canary string in `solve.sh`                    | ✅ FIXED — removed |
| Difficulty (was HARD, gpt5 0/5)                        | ❌ REGRESSED → TRIVIAL (gpt5 5/5) |
| pytest installed in Dockerfile (style warning)        | ⚠️ STILL PRESENT (non-blocking) |

**Root cause of the collapse:** edit #1. In revision_1 the discriminating step
was that weaker agents fixed the script-path mismatch, saw the determinism check
pass, and stopped — never investigating the four C++ source bugs. The new
instruction paragraph explicitly tells the agent to *repair the solver, not just
the scripts*, and that rerun-equivalence is "necessary but not sufficient." That
telegraphs the entire diagnosis, so gpt5 now solves it too. The anti-cheating
test fix (#2) is good and independent of difficulty; it is the **instruction
hint** that removed the challenge, not the test hardening.

## Agent review (claude_code_reviewer) — READY TO USE

Overall: **strong hard-difficulty debugging task; READY TO USE.** One WARNING,
one SUGGESTION — both style/structure, neither blocking:

- **WARNING** — `environment/Dockerfile` lines 21–23 install `pytest==8.4.1`
  and `pytest-json-ctrf==0.3.5` in the image. Move these to `tests/test.sh` so
  the agent image stays minimal (it's a C++/CMake task; the agent never uses
  pytest). **Confirmed still present in the rev2 submitted Dockerfile.**
- **SUGGESTION** — make `test.sh` self-contained using the standard uv-based
  runner pattern (install pytest in test.sh, run in a venv).

Note: the reviewer also auto-generated its own proposed rubric (3 groups,
positive sum **+41**, above the 40 ceiling). That is not the author rubric; it is
archived at `feedback/reviewer_proposed_rubric.txt`. The **author** rubric
(`rubric.txt`) is unchanged from revision_1 (positive sum **+27**).

## Test quality judge — ROBUST

Status **✅ ROBUST**, Severity **None**, Recommendation **ACCEPT**. The suite now
reimplements BSR packing, permutation mapping, and the PCG solve in Python and
compares every output field against the agent's compiled binary across all 6
cases (4 reordered), plus a determinism rerun and a full CMake rebuild from
source — shortcuts are infeasible. Only minor weakness noted: `run-one.sh` is
exercised for 2 of 6 cases (basalt, shale), which the judge calls negligible.

## Directory layout

```
personal_docs/feedback/sparse-block-preconditioner/revision_2/
├── README.md                              # this file
├── revision-priorities.md                 # P0–P3 action list
├── rubric.txt                             # AUTHOR rubric (verbatim) + sum (+27)
├── feedback/                              # copied from /tmp/claude-1000/feedback_64f78238_*
│   ├── notes.txt                          # revision notes, difficulty summary, quality check
│   ├── agent_review.txt                   # claude_code_reviewer (warning + suggestion)
│   ├── reviewer_proposed_rubric.txt       # reviewer-generated rubric (NOT author; +41)
│   └── agent_logs/
│       ├── summary-of-runs-comment.md     # difficulty=trivial run table
│       └── jobs/                          # per-trial trajectories / verifier output (14 jobs)
├── submitted-task/                        # exact evaluated artifact — DO NOT EDIT
│   ├── environment/  solution/  tests/
│   ├── instruction.md  task.toml  output_contract.toml  construction_manifest.json
│   └── .snorkel_config
└── metadata/
    ├── submission_64f78238.json           # full fetch-task payload (~957 KB)
    └── submission_64f78238_summary.json   # trimmed top-level summary (~6 KB)
```

Live workspace: `tasks/sparse-block-preconditioner/` (byte-identical to
`submitted-task/` at fetch time). No `analyze-output-tbench-task.json` this round
— the instruction-sufficiency analysis was NOT_APPLICABLE (no agent failures).

## Refresh commands

```bash
cd "/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS"

stb submissions feedback   64f78238-acf5-4cce-ba2a-100ea9b5a20f
stb submissions download   64f78238-acf5-4cce-ba2a-100ea9b5a20f \
    -o personal_docs/feedback/sparse-block-preconditioner/revision_<N>/submitted-task
stb submissions fetch-task 64f78238-acf5-4cce-ba2a-100ea9b5a20f \
    -o personal_docs/feedback/sparse-block-preconditioner/revision_<N>/metadata
stb submissions view       64f78238-acf5-4cce-ba2a-100ea9b5a20f
```

After the next `stb submissions update`, always create `revision_3/`. Never
overwrite `revision_1/` or `revision_2/`.
