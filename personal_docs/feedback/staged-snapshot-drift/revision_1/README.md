# staged-snapshot-drift — revision_1

> **Older submission.** This snapshot captures the state of an older submission that has been in `NEEDS_REVISION` for ~12 days (created 2026-05-15, captured 2026-05-27). The submission's most recent automated check (eval 7, captured 2026-05-25) failed with an `AutoEval execution failed` build error, leaving the platform state as `NEEDS_REVISION` for the active version. Multiple intermediate evaluations in this submission's history have alternated PASS / NEEDS_REVISION as the author iterated on the same submission_id.

## 1. Submission identity

| Field                | Value                                                                                       |
| -------------------- | ------------------------------------------------------------------------------------------- |
| Task folder          | `staged-snapshot-drift`                                                                     |
| Submission ID        | `d6d229bf-537c-414f-a71f-74582b7ee47c`                                                      |
| Assignment ID        | `7f8fe66d-27e0-4efc-9834-3e1913ca5e83`                                                      |
| Project              | Terminus-2nd-Edition (`bfe79c33-8ab0-4061-9849-08d3207c9927`)                               |
| Created at           | 2026-05-15T19:41:28Z                                                                        |
| Captured at          | 2026-05-27T16:30Z                                                                           |
| Platform state       | `NEEDS_REVISION`                                                                            |
| Revision folder      | `personal_docs/feedback/staged-snapshot-drift/revision_1/`                                  |
| Live workspace       | `tasks/staged-snapshot-drift/`                                                              |

## 2. Revision notes (verbatim)

> AutoEval Execution Summary: AutoEval execution failed. Build status: FAILED. Build ID: CodeExecutionEnvironment:16813e8c-25e4-49b6-98c3-53a115ee1258.

## 3. Headline signals

| Signal                                | Value                                                                 |
| ------------------------------------- | --------------------------------------------------------------------- |
| Reported difficulty                   | `easy` (platform marks **EASY — Requires at least MEDIUM**)           |
| Task.toml claimed difficulty          | `hard`                                                                |
| Task category                         | `debugging`                                                           |
| Languages                             | Go, shell, C                                                          |
| Codebase size                         | small                                                                 |
| Solvable                              | Yes — all unit tests pass on at least one agent run                   |
| Quality check (10-axis)               | All 10 axes PASS                                                      |
| Instruction sufficiency               | PASS                                                                  |
| Test quality judge                    | **VULNERABLE (Major) — STRENGTHEN**                                   |
| Agent review                          | WARNING — pytest install in Dockerfile, instruction can be clearer    |
| CI / fast static checks               | All static checks passed                                              |
| AutoEval build (final, eval 7)        | **FAILED** for build `16813e8c-25e4-49b6-98c3-53a115ee1258`            |

## 4. Agent performance

| Agent / model              | Runs | Success | Other failures | Accuracy |
| -------------------------- | ---- | ------- | -------------- | -------- |
| nop                        | 1    | 0       | 1              | 0.0      |
| oracle                     | 3    | 3       | 0              | 1.0      |
| terminus-claude-opus-4-6   | 5    | 5       | 0              | 1.0      |
| terminus-gpt5-2            | 5    | 4       | 1              | 0.8      |

### Per-test pass rates (10 runs each)

| Test                                | Pass | Fail |
| ----------------------------------- | ---- | ---- |
| test_run_matrix_produces_output     | 10   | 0    |
| test_alpha_matrix                   | 10   | 0    |
| test_beta_matrix                    | 10   | 0    |
| test_gamma_matrix                   | 10   | 0    |
| test_delta_matrix                   | 10   | 0    |
| test_epsilon_matrix                 | 9    | 1    |
| test_zeta_matrix                    | 9    | 1    |

## 5. Common failure patterns & gaps

- **Difficulty miscalibration.** Two heavy models (claude-opus-4.6 at 5/5, gpt5-2 at 4/5) put combined accuracy at 90 percent. Platform tags the task EASY and requires at least MEDIUM. `task.toml` claims `hard` — three signals disagree.
- **Last-mile bug missed by failing gpt5 trial.** Both gpt5 failures and the single-trial failure analysis trace to one unfixed bug in `c2/roll.go` `mark_c`: when `Restart` and `Roll` flags are both set the period override flips `p1 -> p0`, so `d/roll.txt` in epsilon and zeta reports `p0` instead of expected `p1`. Same root cause across both failed cases; not an instruction gap.
- **Hack-shortcut surface (test quality judge).** Tests verify on-disk equality but never check that the row-based pipeline is exercised. ~30 lines of Go (`cp -a` materialize + direct filesystem walk for accounting) bypass all 9 intended bugs.
- **fsmeasure C bugs untested directly.** `probe/measure.c` has 3 deliberate bugs (zeros d/ sizes, halves shared, +1 for c/). Tests only check final accounting JSON, so an agent can compute sizes in pure Go and leave C bugs in place.
- **AutoEval flake on final eval.** Eval 7's last build (`16813e8c...`) failed, but the immediately prior build (`3cfb51d5...`) succeeded — suggests infra flake on the deciding run. Earlier evals 0, 1, 5 also had a single failed CodeBuild interleaved with successes.
- **Agent review: pytest in Dockerfile.** `environment/Dockerfile` lines 20-22 install pytest into the image instead of `tests/test.sh`. Deviates from the standard Terminal-Bench pattern.
- **Agent review: instruction wording.** Instruction says "out of agreement" without naming bugs in `/app/internal`. One scoped sentence would shorten wasted hypothesis time without giving the answer away.

## 6. Submission evaluation history (this submission_id only)

| Idx | Created at           | Outcome          | Notes                                                        |
| --- | -------------------- | ---------------- | ------------------------------------------------------------ |
| 0   | 2026-05-15T19:41Z    | NEEDS_REVISION   | 4 build successes, 1 failed                                  |
| 1   | 2026-05-16T05:58Z    | NEEDS_REVISION   | 4 build successes, 1 failed                                  |
| 2   | 2026-05-16T07:53Z    | PASS             | 5 build successes                                            |
| 3   | 2026-05-16T19:18Z    | PASS             | 5 build successes                                            |
| 4   | 2026-05-22T09:56Z    | PASS             | 5 build successes                                            |
| 5   | 2026-05-23T12:33Z    | NEEDS_REVISION   | 5 builds OK, 1 failed                                        |
| 6   | 2026-05-23T19:44Z    | NEEDS_REVISION   | Build completion timeout (s3 marker not written)             |
| 7   | 2026-05-25T11:52Z    | NEEDS_REVISION   | 5 builds OK, 1 failed (current state)                        |

Pattern: AutoEval has been intermittent for this submission. Three previous PASS evaluations indicate the task itself is healthy; the most recent failures look like build-infra noise rather than task regressions, although the difficulty miscalibration and hack-shortcut weaknesses are unresolved.

## 7. Directory layout

```
personal_docs/feedback/staged-snapshot-drift/revision_1/
├── README.md                 (this file)
├── revision-priorities.md
├── rubric.txt
├── feedback/
│   ├── notes.txt
│   ├── agent_review.txt
│   └── agent_logs/
│       ├── analyze-output-tbench-task.json
│       ├── summary-of-runs-comment.md
│       └── jobs/                          (14 agent trial dirs)
├── submitted-task/
│   ├── environment/
│   ├── solution/
│   ├── tests/
│   ├── instruction.md
│   └── task.toml
└── metadata/
    ├── submission_d6d229bf.json
    └── submission_d6d229bf_summary.json
```

## 8. Refresh commands (from repo root)

```bash
cd "/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS"

# Refresh feedback bundle (writes /tmp/feedback_<id>_*/)
stb submissions feedback d6d229bf-537c-414f-a71f-74582b7ee47c

# Re-download submitted zip
stb submissions download d6d229bf-537c-414f-a71f-74582b7ee47c \
    -o "personal_docs/feedback/staged-snapshot-drift/revision_2/submitted-task"

# Re-fetch metadata JSON
stb submissions fetch-task d6d229bf-537c-414f-a71f-74582b7ee47c \
    -o "personal_docs/feedback/staged-snapshot-drift/revision_2/metadata"

# Open in Snorkel Experts UI
stb submissions view d6d229bf-537c-414f-a71f-74582b7ee47c
```

## 9. Pointer to live workspace

Edits and re-uploads happen in: `tasks/staged-snapshot-drift/`. Use `stb submissions update` (not `create`) when revising — this submission_id is already linked.
