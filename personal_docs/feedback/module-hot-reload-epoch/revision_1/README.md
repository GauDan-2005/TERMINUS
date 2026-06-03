# module-hot-reload-epoch — Revision 1 (platform feedback snapshot)

Point-in-time archive of TERMINUS platform feedback for the `module-hot-reload-epoch` task. Do **not** edit anything under `submitted-task/` — that mirrors the exact zip the platform evaluated.

## Submission identity

| Field             | Value                                                                                  |
| ----------------- | -------------------------------------------------------------------------------------- |
| Task name         | module-hot-reload-epoch                                                                |
| Submission ID     | `ea9c5aae-7199-46c6-bf5b-236691b01936`                                                 |
| Assignment ID     | `01f44181-3cfe-4141-a1bd-37a85e974a83`                                                 |
| Project ID        | `bfe79c33-8ab0-4061-9849-08d3207c9927`                                                 |
| Project           | Terminus-2nd-Edition                                                                   |
| Platform state    | **NEEDS_REVISION** (overall outcome) — automated quality-check evaluation outcome PASS |
| Submission date   | 2026-05-23 18:58                                                                       |
| Captured on       | 2026-05-27                                                                             |
| Folder name       | module-hot-reload-epoch                                                                |
| Live workspace    | `tasks/module-hot-reload-epoch/`                                                       |
| Revision folder   | `personal_docs/feedback/module-hot-reload-epoch/revision_1/`                           |
| Further revisions | allowed                                                                                |

## Revision notes (verbatim from platform)

> Instruction.md leaks bug-level implementation hints. The described invariants map almost directly to specific seeded fixes. Please refer to https://snorkel-ai.github.io/Terminus-EC-Training-stateful/portal/docs/understanding-tasks/prompt-styling.
>
> The hot-reload tag appears inaccurate for the actual task behavior.

## Headline signals

| Signal                       | Value                                                                |
| ---------------------------- | -------------------------------------------------------------------- |
| Difficulty (autoeval)        | MEDIUM (declared `hard` in task.toml — mismatch worth re-checking)   |
| Solvable                     | Yes — at least one agent passed every test                           |
| Instruction sufficiency      | PASS                                                                 |
| Reward-hacking check         | PASS (both trials clean)                                             |
| Quality check (10-axis)      | PASS on all 10 axes                                                  |
| AutoEval build               | Completed (no build timeout, no AutoEval fail)                       |
| Test quality judge           | **VULNERABLE — severity Critical** (test suite admits Rust bypass)   |
| Harness agent review         | PASS with 1 WARNING (pytest in Dockerfile) + 1 SUGGESTION (schema)   |
| Rubric                       | Present, sum +27 / −12 (see `rubric.txt`)                            |

## Agent performance

| Agent                        | Runs | Successes | Failures (timeout) | Failures (other) | Accuracy |
| ---------------------------- | ---: | --------: | -----------------: | ---------------: | -------: |
| nop (reference)              |    1 |         0 |                  0 |                1 |     0.00 |
| oracle (reference)           |    3 |         3 |                  0 |                0 |     1.00 |
| terminus-claude-opus-4-6     |    5 |         5 |                  0 |                0 |     1.00 |
| terminus-gpt5-2              |    5 |         3 |                  0 |                2 |     0.60 |

Overall solver agents: 8/10 successful runs (80% pass rate across solver trials).

## Per-test pass rates

| Test                                          | Pass / Total |
| --------------------------------------------- | -----------: |
| test_case_one                                 |       8 / 10 |
| test_case_two                                 |      10 / 10 |
| test_case_three                               |      10 / 10 |
| test_case_four                                |      10 / 10 |
| test_case_five                                |      10 / 10 |
| test_case_six                                 |      10 / 10 |
| test_case_seven                               |      10 / 10 |
| test_case_eight                               |      10 / 10 |
| test_case_nine                                |      10 / 10 |
| test_case_ten                                 |      10 / 10 |
| test_rust_build_artifact_present              |      10 / 10 |
| test_report_stable_across_consecutive_runs    |      10 / 10 |

Only `test_case_one` ever flaked, and only on the 2 failing `terminus-gpt5-2` trials.

## Common failure patterns (from notes.txt + analyze-output)

- Both failing trials (`tbench-task__cChGQmt`, `tbench-task__DxJiAFs`) fixed all five seeded bugs (b2/q.js cross-cycle deferred, c3/r.js global factor cache, a1/p.js carry via `nativeValue`, src/native/src/lib.rs `r_d` carry for "old", d4/s.js hardcoded `status:'stale'`).
- Sole failure was a self-introduced regression: the agent added an extra `scenario: a.name` field to record objects in `a1/p.js`, breaking `test_case_one`'s strict dict equality. Classified as **agent over-engineering**, not an instruction gap.
- Both failing trials also encountered a missing `cargo` PATH issue and worked around it (absolute path vs. symlinks).

## Reviewer-flagged issues (the real revision drivers)

1. **Prompt-style leak (P0)** — reviewer claims `instruction.md` maps too directly onto the seeded bug list. Each instruction sentence is a near-1:1 hint to one of the five fixes. The autoeval `task_specification` check passed, but a human reviewer rejected on prompt-styling grounds. Rewrite per Snorkel prompt-styling docs: describe the **observable failure** ("report drifts depending on run sequence", "older records read as stale"), not the **fix recipe**.
2. **Misleading tag (P1)** — `task.toml` tags include `"hot-reload"`, but the task has no module hot-reload behavior; the actual surface is matrix-runner orchestration + Rust native helper. Replace `hot-reload` with something like `state-propagation`, `native-bindings`, or drop it.
3. **Test-quality vulnerability (P1)** — `test_rust_build_artifact_present` is vacuous because the Dockerfile already runs `cargo build` at image-build time; an agent could rewrite `tools/run_matrix.js` to skip the Rust binary entirely and still pass. The judge report recommends asserting either rebuild-after-cleanup or invocation evidence. (Note: in practice no agent did this, but the safeguard is missing.)
4. **Difficulty mislabel (P2)** — `task.toml` says `difficulty = "hard"`, autoeval says MEDIUM. Reconcile after the instruction is de-leaked (de-leaking may bring difficulty back up).
5. **Test deps in Dockerfile (P3)** — harness agent review warns that `pytest` is installed in the image rather than in `test.sh`. Documented as intentional via the venv at `/opt/pytest`; not blocking.

## Directory layout

```
personal_docs/feedback/module-hot-reload-epoch/revision_1/
├── README.md                       # this file
├── revision-priorities.md          # P0/P1/P2/P3 plan
├── rubric.txt                      # 10-line rubric (sum +27 / −12)
├── feedback/                       # full /tmp/feedback_*/ bundle
│   ├── notes.txt                   # revision notes + difficulty + analysis + 10-axis quality
│   ├── agent_review.txt            # harness review (PASS, 1 WARN, 1 SUGGESTION)
│   └── agent_logs/
│       ├── summary-of-runs-comment.md
│       ├── analyze-output-tbench-task.json
│       └── jobs/                   # per-trial CI outputs (nop, oracle x3, opus x5, gpt5 x5)
├── submitted-task/                 # exact zip uploaded to platform — DO NOT EDIT
│   ├── instruction.md
│   ├── task.toml
│   ├── environment/                # Dockerfile + a1..d4 + src/native + tools + fixtures + docs
│   ├── solution/solve.sh
│   ├── tests/test.sh + test_outputs.py
│   └── .snorkel_config
└── metadata/
    └── submission_ea9c5aae.json    # full fetch-task payload (~955 KB; rubric/quality/text_summary inside)
```

## Refresh commands

```bash
cd "/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS"

# Re-pull feedback bundle (writes /tmp/feedback_<sub>_<ts>/)
stb submissions feedback ea9c5aae-7199-46c6-bf5b-236691b01936

# Re-download submitted zip
stb submissions download ea9c5aae-7199-46c6-bf5b-236691b01936 \
    -o personal_docs/feedback/module-hot-reload-epoch/revision_<N+1>/submitted-task

# Re-fetch assignment metadata
stb submissions fetch-task ea9c5aae-7199-46c6-bf5b-236691b01936 \
    -o personal_docs/feedback/module-hot-reload-epoch/revision_<N+1>/metadata

# Open in browser
stb submissions view ea9c5aae-7199-46c6-bf5b-236691b01936
```

When revising, use `stb submissions update` (not `create`) so the assignment ID is preserved.

## Pointer to live workspace

Active editing for the next revision happens in:

```
tasks/module-hot-reload-epoch/
```

Notes already exist under `tasks/module-hot-reload-epoch/.step2b-metrics.jsonl` and `construction_manifest.json` from the original build.
