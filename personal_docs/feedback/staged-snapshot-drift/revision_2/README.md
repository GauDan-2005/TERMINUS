# staged-snapshot-drift — revision_2

> **No-change re-capture.** This snapshot was taken on **2026-05-28** (feedback bundle stamped `20260528T235102Z`). Compared byte-for-byte against `revision_1` (captured 2026-05-27), **nothing on the platform has changed**: `notes.txt`, `agent_review.txt`, the entire `agent_logs/` tree, the submitted zip, and the 3.48 MB metadata JSON are all **identical**. The submission is still `NEEDS_REVISION` on the same submission ID, with the same failed AutoEval build (`16813e8c`). It has now been sitting in `NEEDS_REVISION` for **~13 days** (created 2026-05-15, captured 2026-05-28). No new evaluation has run since **eval 7 on 2026-05-25**, and the author has **not** resubmitted — the live workspace still matches the submitted content, so none of the `revision_1` priorities have been applied yet.

## 1. Submission identity

| Field                | Value                                                                                       |
| -------------------- | ------------------------------------------------------------------------------------------- |
| Task folder          | `staged-snapshot-drift`                                                                     |
| Submission ID        | `d6d229bf-537c-414f-a71f-74582b7ee47c`                                                      |
| Assignment ID        | `7f8fe66d-27e0-4efc-9834-3e1913ca5e83`                                                      |
| Task ID              | `d6d229bf-537c-414f-a71f-74582b7ee47c`                                                      |
| Project              | Terminus-2nd-Edition (`bfe79c33-8ab0-4061-9849-08d3207c9927`)                               |
| Created at           | 2026-05-15T19:41:28Z                                                                        |
| Captured at          | 2026-05-28T23:51Z (bundle `feedback_..._20260528T235102Z`)                                  |
| Platform state       | `NEEDS_REVISION`                                                                            |
| Payment status       | `PENDING`                                                                                   |
| Further revisions    | allowed (`further_revision_requests_allowed = true`)                                        |
| Submission expiry    | 2026-10-22T12:35:55Z                                                                        |
| Revision folder      | `personal_docs/feedback/staged-snapshot-drift/revision_2/`                                  |
| Live workspace       | `tasks/staged-snapshot-drift/`                                                              |

This is the **only** submission for the `staged-snapshot-drift` folder (row #16 of 17 in `stb submissions list`). There is no newer submission ID; the author has iterated in place on this one submission_id.

## 2. Revision notes (verbatim)

> AutoEval Execution Summary: AutoEval execution failed. Build status: FAILED. Build ID: CodeExecutionEnvironment:16813e8c-25e4-49b6-98c3-53a115ee1258.

(Identical to `revision_1`.)

## 3. Evaluation history (from metadata `evaluations[]`)

The submission has **8 evaluations**. It reached PASS three times (evals 2–4) and then regressed to `NEEDS_REVISION` (evals 5–7). The latest eval failed on the AutoEval build, not on agent solvability.

| # | Created (UTC)        | Updated (UTC)        | Outcome          |
| - | -------------------- | -------------------- | ---------------- |
| 0 | 2026-05-15 19:41     | 2026-05-15 22:03     | NEEDS_REVISION   |
| 1 | 2026-05-16 05:58     | 2026-05-16 06:48     | NEEDS_REVISION   |
| 2 | 2026-05-16 07:53     | 2026-05-16 08:36     | **PASS**         |
| 3 | 2026-05-16 19:18     | 2026-05-16 20:43     | **PASS**         |
| 4 | 2026-05-22 09:56     | 2026-05-22 11:28     | **PASS**         |
| 5 | 2026-05-23 12:33     | 2026-05-23 13:25     | NEEDS_REVISION   |
| 6 | 2026-05-23 19:44     | 2026-05-23 22:38     | NEEDS_REVISION   |
| 7 | 2026-05-25 11:52     | 2026-05-25 12:35     | **NEEDS_REVISION** (latest — AutoEval build `16813e8c` FAILED) |

> The regression after eval 4 (last PASS, 2026-05-22) is worth noting: something between 05-22 and 05-23 flipped the task from PASS back to NEEDS_REVISION, and it has stayed there. The eval-7 surface symptom is an AutoEval build failure.

## 4. Headline signals (unchanged from revision_1)

| Signal                                | Value                                                                 |
| ------------------------------------- | --------------------------------------------------------------------- |
| Reported difficulty                   | `easy` (platform marks **EASY — Requires at least MEDIUM**)           |
| `task.toml` claimed difficulty        | `hard` (also `metadata.extra.difficulty_label = "hard"`)              |
| Estimated AHT                         | 85 minutes                                                            |
| Task category                         | `debugging`                                                           |
| Languages                             | Go, shell, C                                                          |
| Codebase size                         | small                                                                 |
| Milestones                            | 0 (single-step task)                                                  |
| Solvable                              | Yes — all unit tests pass on at least one agent run                   |
| Quality check (10-axis)               | All 10 axes PASS                                                      |
| Instruction sufficiency               | PASS                                                                  |
| Test quality judge                    | **VULNERABLE (Major) — STRENGTHEN**                                   |
| Agent review                          | WARNING — pytest install in Dockerfile; suggestion: name buggy subsystem in instruction |
| CI / fast static checks               | All static checks passed (`long_context_quality/skip`)               |
| AutoEval build (final, eval 7)        | **FAILED** for build `16813e8c-25e4-49b6-98c3-53a115ee1258`            |
| Code-quality CodeBuild (eval 7)       | SUCCEEDED (all phases) — this is a *different* build from the AutoEval build |

> **Two builds per eval.** The `code_quality_check_results` log in the metadata is the quality/code-check CodeBuild and it **succeeded at every phase** (DOWNLOAD_SOURCE → BUILD → POST_BUILD → UPLOAD_ARTIFACTS all `SUCCEEDED`, 2026-05-25 11:58–12:00). The build that **failed** is the separate AutoEval build `16813e8c`, whose full logs are not embedded in the JSON (only referenced via the difficulty-check artifact S3 key `codebuild_uploads/autoeval_artifacts/d6d229bf.../59eddd31/difficulty_check_artifact.zip`). This is the same split `revision_1` documented.

## 5. Agent performance (from `agent_logs/summary-of-runs-comment.md`)

| Agent / model              | Runs | Success | Other failures | Accuracy |
| -------------------------- | ---- | ------- | -------------- | -------- |
| nop                        | 1    | 0       | 1              | 0.0      |
| oracle                     | 3    | 3       | 0              | 1.0      |
| terminus-claude-opus-4-6   | 5    | 5       | 0              | 1.0      |
| terminus-gpt5-2            | 5    | 4       | 1              | 0.8      |

Combined non-reference agent accuracy ≈ **90%** (9/10) — the basis for the EASY rating.

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

The single epsilon/zeta failure traces to one unfixed bug in `c2/roll.go`'s `mark_c` (period flag `p1→p0` when both `Restart` and `Roll` are set) — an agent reasoning miss, not a flaky or unreachable test. Hack check on that trial: **clean**.

## 6. Test-quality judge (VULNERABLE / Major / STRENGTHEN)

> The test suite verifies output correctness thoroughly but cannot distinguish between an agent that debugged 9 bugs across 6 files and one that rewrote ~30 lines in `cmd/ctl/main.go` to bypass the entire row-processing pipeline.

- **Strength:** tests independently verify on-disk filesystem state (contents, hardlink inode groups, byte sizes), not just the tool's JSON.
- **Weakness:** no assertion the internal row-processing pipeline is actually used; no direct check that the `fsmeasure` C binary produces correct output; no check the package structure stays intact.

## 7. Rubric

Captured verbatim in `rubric.txt`. Positive total **+28**, negative total **−18**, so `|pos| + |neg| = 46`, which **exceeds the workflow 10–40 cap**. Unchanged from revision_1.

## 8. What changed since revision_1

**Nothing on the platform.** Integrity checks run at capture time:

| Artifact                        | rev1 vs rev2          |
| ------------------------------- | --------------------- |
| `feedback/notes.txt`            | identical             |
| `feedback/agent_review.txt`     | identical             |
| `feedback/agent_logs/` (tree)   | identical             |
| `submitted-task/` (full tree)   | identical             |
| `metadata/submission_*.json`    | identical (3,478,893 bytes) |

The live workspace `tasks/staged-snapshot-drift/` matches the submitted content on every shared file (`instruction.md`, `task.toml`, `environment/internal/*`, `tests/*`, `solution/*` all identical). The only local-only files are build/scaffolding artifacts not in the submission:

- `construction_manifest.json`, `output_contract.toml`, `.step2b-checksum`, `.step2b-metrics.jsonl`
- `environment/.dockerignore` (added locally since the submission; not in the platform zip)

**Implication:** none of the `revision_1` revision priorities have been implemented or resubmitted. They all still apply — see `revision-priorities.md`.

## 9. Directory layout (this revision)

```
personal_docs/feedback/staged-snapshot-drift/revision_2/
├── README.md                  ← this file
├── revision-priorities.md     ← P0–P3, carried forward from revision_1 (all still open)
├── rubric.txt                 ← platform rubric, verbatim (+28 / −18, sum 46 > 40 cap)
├── feedback/
│   ├── notes.txt              ← identical to revision_1
│   ├── agent_review.txt       ← identical to revision_1
│   └── agent_logs/            ← ~35 MB; difficulty-check artifacts (identical to revision_1)
│       ├── summary-of-runs-comment.md
│       ├── analyze-output-tbench-task.json
│       └── jobs/              ← 14 job dirs (1 nop, 3 oracle, 5 opus-4-6, 5 gpt5-2)
├── submitted-task/            ← exact platform zip (27.25 KB), + .snorkel_config
│   ├── instruction.md
│   ├── task.toml
│   ├── environment/ (cmd, config, data, docs, internal, probe, scripts, Dockerfile, go.mod, Makefile, README.md)
│   ├── solution/solve.sh
│   └── tests/ (test.sh, test_outputs.py)
└── metadata/
    ├── submission_d6d229bf.json          ← full fetch-task payload (3.48 MB)
    └── submission_d6d229bf_summary.json  ← trimmed summary (IDs, evals, rubric, headline)
```

## 10. Refresh commands

```bash
cd "/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS"
SID=d6d229bf-537c-414f-a71f-74582b7ee47c

stb submissions list --project-id bfe79c33-8ab0-4061-9849-08d3207c9927 --show-folder-names
stb submissions feedback   "$SID"
stb submissions download   "$SID" -o personal_docs/feedback/staged-snapshot-drift/revision_<N>/submitted-task
stb submissions fetch-task "$SID" -o personal_docs/feedback/staged-snapshot-drift/revision_<N>/metadata
stb submissions view       "$SID"   # browser
```

> Note: on `stb` 2.2.2 the feedback bundle is written under `/tmp/claude-1000/feedback_<SID>_<UTCstamp>/` (not `/tmp/feedback_*`). Copy it into `revision_<N>/feedback/`.

## 11. Capture-time note (filesystem)

During this capture, re-reads of files under the `/media/.../COLLEGE MATERIAL/...` mount intermittently misreported types (e.g. `instruction.md` briefly appearing as a directory, duplicated `tests` entries in `ls`). These were transient mount glitches; a fresh `stat` and `diff -rq` against `revision_1` confirmed every `submitted-task` file is intact and byte-identical (`instruction.md` = regular file, 1751 bytes). The archive content is sound.
