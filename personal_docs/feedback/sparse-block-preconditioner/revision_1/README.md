# sparse-block-preconditioner — Revision 1 feedback snapshot

Point-in-time archive of platform feedback for the `sparse-block-preconditioner`
task. The submission was returned in state **NEEDS_REVISION**. This is the
first archived revision (no prior `revision_*` folders existed).

## Submission identity

| Field                | Value                                                  |
| -------------------- | ------------------------------------------------------ |
| Folder name          | `sparse-block-preconditioner`                          |
| Submission ID        | `64f78238-acf5-4cce-ba2a-100ea9b5a20f`                 |
| Assignment ID        | `961990f5-3736-4942-bc08-2fd732041f9b`                 |
| Project              | Terminus-2nd-Edition (`bfe79c33-8ab0-4061-9849-08d3207c9927`) |
| Submission task type | `submission-941bede0-d9c6-42f0-874d-cd3d25582c72`      |
| Created (evaluation) | 2026-05-25 15:56:41 UTC                                |
| Updated (evaluation) | 2026-05-25 17:59:05 UTC                                |
| Submission state     | **NEEDS_REVISION** (created 2026-05-25 15:49)          |
| Captured at          | 2026-05-27                                             |
| Further revisions    | allowed                                                |
| Submission AHT       | (see metadata summary)                                 |

Submitted zip used at capture: `submitted-task/sparse-block-preconditioner.zip`
(extracted into `submitted-task/`). Do not edit anything under that folder —
it is the exact uploaded artifact reviewers evaluated.

## Revision notes (verbatim from platform)

> the verifier has a high severity correctness and anti cheating gap.
> tests/test_outputs.py only checks json values reported by the solver binary
> like iterations, final_residual, reported_residual and the ok flag instead
> of independently verifying the actual numerical results. an agent could skip
> the intended c++ debugging work by hardcoding successful audit values in
> drive_u/run.cpp and still pass the current assertions without fixing the
> real bugs in the bsr layout permutation preconditioner or residual metric
> modules. this breaks the anti cheating requirement that hardcoded values
> should not pass and also breaks the verifier requirement that tests must
> check real correctness.
>
> the tests also enforce strict convergence thresholds like residuals < 1e-8
> even though the instructions never clearly define them. the prompt only
> mentions symptoms like "drifts" and "stall". the verifier should calculate
> correctness independently from the case data so results cannot be spoofed
> and any strict convergence behavior being tested should be clearly explained
> in the instructions. also the old "# Terminal-Bench Canary, do not remove"
> comment should be removed from solution/solve.sh because canary strings are
> no longer expected in edition 2.

## Headline signals

| Signal                          | Result                                                              |
| ------------------------------- | ------------------------------------------------------------------- |
| Difficulty check                | **HARD**, solvable (all tests passed by at least one agent run)     |
| AutoEval build                  | Build/static checks completed; evaluation outcome PASS              |
| Task Instruction Sufficiency    | PASS (with systematic comprehension gap noted by autoeval analysis) |
| Quality check (10-axis)         | **1 fail** / 9 pass — `behavior_in_task_description` FAILED         |
| Test quality judge              | **VULNERABLE — Critical / STRENGTHEN** (anti-cheating gap)          |
| Agent review (harness lint)     | WARNING — pytest installed in Dockerfile instead of test.sh         |
| Final platform decision         | NEEDS_REVISION                                                      |

### Quality check breakdown (10 axes)
- FAIL `behavior_in_task_description` — tests enforce thresholds (residual `< 1e-8`, max iter ≤ 20, `ok` True for all rows, all cases below 200-iter cap) that the instruction never spells out.
- PASS the remaining nine axes: behavior_in_tests, informative_test_structure, anti_cheating_measures, structured_data_schema, pinned_dependencies, typos, tests_or_solution_in_image, hardcoded_solution, file_reference_mentioned.

## Agent performance

| Agent                       | Runs | Successes | Failures (timeout) | Failures (other) | Accuracy |
| --------------------------- | ---- | --------- | ------------------ | ---------------- | -------- |
| nop                         | 1    | 0         | 0                  | 1                | 0.0      |
| oracle                      | 3    | 3         | 0                  | 0                | 1.0      |
| terminus-claude-opus-4-6    | 5    | 5         | 0                  | 0                | 1.0      |
| terminus-gpt5-2             | 5    | 0         | 0                  | 5                | 0.0      |

### Per-test pass rate (10 trials = 5 opus + 5 gpt5)

| Test                                       | Pass / Total | Notes                                      |
| ------------------------------------------ | ------------ | ------------------------------------------ |
| test_a0_matrix_cases_present               | 10 / 10      |                                            |
| test_b1_run_one_basalt_matches_matrix      | 10 / 10      |                                            |
| test_c2_basalt_converges_quickly           | 10 / 10      |                                            |
| test_d3_flint_off_diagonal_converges       | 10 / 10      |                                            |
| test_e4_shale_reordered_converges          | 10 / 10      |                                            |
| test_f5_garnet_reordered_converges         | 10 / 10      |                                            |
| test_g6_mica_low_final_residual            | 10 / 10      |                                            |
| **test_h7_opal_mixed_reordered_residuals** | 5 / 10       | gpt5 never passes (reported≠measured)      |
| **test_i8_reported_matches_true_residual** | 5 / 10       | gpt5 never passes                          |
| test_j9_two_matrix_runs_equivalent         | 10 / 10      |                                            |
| test_k0_convergent_cases_below_cap         | 10 / 10      |                                            |
| test_l1_run_one_shale_matches_matrix       | 10 / 10      |                                            |
| **test_z9_row_status_flags**               | 5 / 10       | gpt5 never passes (`ok` flag)              |

## Common failure pattern (from notes.txt analyze step)

All 5 gpt5 trials followed an **identical trajectory** and stalled at 10/13:

1. PASS — correctly identified script-path mismatch (`/app/bin/solverctl` → `/app/build/bin/solverctl`).
2. PASS — fixed both `run-matrix.sh` and `run-one.sh` to call the build-tree binary.
3. PASS — verified structural correctness (per-case JSON matches matrix slices, two runs deterministic).
4. FAIL — stopped here, never investigated the underlying C++ source bugs.

Agents observed `ok: false` and `reported_residual: 0.0001` vs `final_residual: 0.0` in the JSON they generated, then treated that as expected. The determinism check (run A = run B) acted as a **false-positive gate** giving them unwarranted confidence.

**Unresolved C++ bugs (zero agents touched):**
- `scale_q/metric.cpp` — hardcoded `norm_q = 0.0001` instead of computing L2 norm
- `perm_p/order.cpp` — incorrect RHS vector permutation
- `bsr_n/layout.cpp` — incorrect block-row reordering
- `prec_r/apply.cpp` — preconditioner bug under reordered layouts

Hack check: clean — no reward hacking, no `solution/` access, no test-file edits.

## Instruction gaps highlighted by reviewers

- Cryptic symptom-only language ("drifts", "stall", "residual columns disagree", "rows stay dirty") never says **"fix C++ source defects"** — agents read these as observations, not bugs.
- No quantitative convergence criteria. Tests enforce `< 1e-8` (basalt/flint/garnet) and `< 1e-7` (shale/mica/opal) plus a `≤ 20` iteration bound for basalt and an all-rows `ok=True` invariant; none of those are stated in `instruction.md`.
- The verifier checks self-reported solver values without independent computation, so the convergence claims cannot anchor the rubric.

## Agent-review (harness) warnings & suggestions

WARNING (1):
- `environment/Dockerfile` lines 21–23 install `pytest==8.4.1` and `pytest-json-ctrf==0.3.5` inside the image. Move these to `tests/test.sh` so the agent workspace stays minimal and matches the Terminal-Bench-2 runner pattern.

Suggestion:
- Add an explicit "Identify and fix the source-level defects causing incorrect behavior under reordered layouts" sentence to `instruction.md` to reduce the unproductive exploration loop noted above.

Overall agent-review recommendation: **READY TO USE** (warning is style/compliance, not correctness).

## Test quality judge — critical findings

Severity: **Critical / VULNERABLE / STRENGTHEN.** `tests/test_outputs.py` checks values self-reported by the solver binary (`solver-audit.json`) without ever independently loading the case data, computing the expected residual / iteration count, or comparing. An agent could append a 6-line patch to `drive_u/run.cpp` that hardcodes `iterations=1`, `residuals=0.0`, `ok=true` and pass all 13 tests without touching `bsr_n`, `perm_p`, `prec_r`, or `scale_q`.

Required fixes (called out by reviewers):
- Compute expected residuals independently from `data/<case>/` inputs inside the test harness.
- Assert measured vs. solver-reported residual agreement using the independent calculation, not the binary's own claim.
- Either remove strict numeric thresholds from tests, or document them in `instruction.md`.

## Auxiliary issues called out in revision notes

- `solution/solve.sh` still contains the legacy `# Terminal-Bench Canary, do not remove` comment. Edition-2 tasks must drop the canary string.

## Directory layout

```
personal_docs/feedback/sparse-block-preconditioner/revision_1/
├── README.md                              # this file
├── revision-priorities.md                 # P0–P3 action list
├── rubric.txt                             # platform rubric (verbatim) + sum
├── feedback/                              # copied from /tmp/feedback_64f78238_*
│   ├── notes.txt                          # revision notes, difficulty summary, quality check, agent failure analysis
│   ├── agent_review.txt                   # harness review (warnings/suggestions)
│   └── agent_logs/
│       ├── analyze-output-tbench-task.json
│       ├── summary-of-runs-comment.md
│       └── jobs/                          # per-trial trajectories / verifier output
├── submitted-task/                        # exact zip the platform evaluated — DO NOT EDIT
│   ├── environment/
│   ├── solution/
│   ├── tests/
│   ├── instruction.md
│   ├── task.toml
│   └── sparse-block-preconditioner.zip
└── metadata/
    ├── submission_64f78238.json           # full fetch-task payload (~510 KB)
    └── submission_64f78238_summary.json   # trimmed top-level summary (~13 KB)
```

Live workspace: `tasks/sparse-block-preconditioner/`. `submitted-task/instruction.md`
is byte-identical to the current `tasks/sparse-block-preconditioner/instruction.md`
at fetch time (2026-05-27).

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

When re-running after an `stb submissions update`, always create a new
`revision_<N+1>/` folder. Never overwrite `revision_1/`.
