# TERMINUS - Submission Status

> ⚠️ **Historical snapshot (2026-06-22).** This page reflects the submission state on that date. The per-task feedback archives (`personal_docs/feedback/<task>/revision_1/`), the `personal_docs/reports/revision-progress-2026-06-22.md` report, and the task zips referenced below have since been pruned from the working tree, so those links are historical. The current active tasks are the three under `specs/` / `tasks/` (`cargo-feature-unification`, `cgroup-budget-solver`, `overlayfs-whiteout-flatten`); run `stb submissions list` for live status.

**Project:** Terminus-2nd-Edition (`bfe79c33-8ab0-4061-9849-08d3207c9927`)
**Last updated:** 2026-06-22
**Status source:** user-provided `stb submissions list --show-folder-names` table for assignment states; direct `stb submissions feedback/download/fetch-task` pulls on 2026-06-22 for every `NEEDS_REVISION` row.

Active workspace buckets after pruning accepted rows: **5 needs-revision / 1 offered**. Payment status is `PENDING` for every retained row in the pasted table.

The live `stb submissions list --project-id bfe79c33-8ab0-4061-9849-08d3207c9927 --show-folder-names` call hung during this update, so the active-row table below preserves the user's pasted snapshot with accepted rows removed. The five active revision rows were independently confirmed by feedback metadata: each has `blocking_check_enums` containing `NEEDS_REVISION` and `FAIL`.

## Current status

| # | Submission ID | Created | Folder / task | Assignment State | Payment | New feedback archive |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | `286b5bea-fc9b-4ecf-906f-10bb68c68582` | 05/25 15:56 | _(unnamed offer)_ | OFFERED | PENDING | - |
| 2 | `64f78238-acf5-4cce-ba2a-100ea9b5a20f` | 05/25 15:49 | `sparse-block-preconditioner` | NEEDS_REVISION | PENDING | `personal_docs/feedback/sparse-block-preconditioner/revision_1/` |
| 3 | `4e774a51-688e-46e0-b7bc-c56194572f8c` | 05/25 14:09 | `quantized-beam-alignment` | NEEDS_REVISION | PENDING | `personal_docs/feedback/quantized-beam-alignment/revision_1/` |
| 4 | `ec8bf6df-d0d2-40bf-ba64-67ea0f67e002` | 05/25 13:05 | `fog-state-resume` | NEEDS_REVISION | PENDING | `personal_docs/feedback/fog-state-resume/revision_1/` |
| 8 | `52218157-dee7-483f-a7f5-5653ee5e1d01` | 05/23 21:25 | `policy-revocation-shadow` | NEEDS_REVISION | PENDING | `personal_docs/feedback/policy-revocation-shadow/revision_1/` |
| 12 | `7243aade-daa1-4513-96d0-7366734d930d` | 05/18 23:44 | `async-executor-liveness` _(mapped from prior status/submission archive)_ | NEEDS_REVISION | PENDING | `personal_docs/feedback/async-executor-liveness/revision_1/` |

## Needs-revision summary from feedback pulled 2026-06-22

| Task | Assignment ID | Platform signal | Agent performance | Main revision driver |
| --- | --- | --- | --- | --- |
| `sparse-block-preconditioner` | `961990f5-3736-4942-bc08-2fd732041f9b` | EASY; requires at least MEDIUM; solvable | opus 4/5, gpt5 4/5, oracle 3/3, nop 0/1 | Difficulty below floor plus instruction-sufficiency failure around strict iteration-count equality. |
| `quantized-beam-alignment` | `49c16ae8-40f5-41eb-a9ba-0d83914655b6` | TRIVIAL; requires at least MEDIUM; solvable | opus 5/5, gpt5 5/5, oracle 3/3, nop 0/1 | Every real-agent run passes; needs a genuinely discriminating difficulty raise. |
| `fog-state-resume` | `51f38673-072f-40dd-9f32-4f1bb491ff94` | EASY; requires at least MEDIUM; solvable | opus 4/5, gpt5 5/5, oracle 3/3, nop 0/1 | Near-miss on ward active boundary tests; measured difficulty still below floor. |
| `policy-revocation-shadow` | `07211270-9aa6-4e4f-bf8b-91bd33c6d019` | EASY; requires at least MEDIUM; solvable | opus 4/5, gpt5 5/5, oracle 3/3, nop 0/1 | Measured difficulty below floor; one failed run timed out before implementation. |
| `async-executor-liveness` | `3a746d5a-6e17-45ab-91cf-87440414d3d1` | EASY; requires at least MEDIUM; solvable | opus 4/5, gpt5 5/5, oracle 3/3, nop 0/1 | Measured difficulty below floor; one failed run missed multi-constraint scheduler logic. |

Each archive contains:

- `feedback/notes.txt`
- `feedback/agent_review.txt`
- `feedback/agent_logs/` when provided by the platform
- `submitted-task/` extracted from the submitted zip
- `metadata/submission_<short_id>.json`
- `metadata/submission_<short_id>_summary.json`
- `README.md`
- `revision-priorities.md`
- `rubric.txt`

See `personal_docs/feedback/README.md` for the archive map and refresh commands.

## Local revision progress

Platform assignment states above remain the source of truth until resubmission is uploaded and re-reviewed. Local readiness reflects command-backed repo gates run on 2026-06-22.

| Task | Local revision state | Refreshed zip | Evidence |
| --- | --- | --- | --- |
| `sparse-block-preconditioner` | Feedback addressed; local strict approval gate PASS with no blocking failures. | `Task_Ready_To_Submit/sparse-block-preconditioner.zip` | `personal_docs/reports/revision-progress-2026-06-22.md` |
| `quantized-beam-alignment` | Feedback addressed; local strict approval gate PASS with no blocking failures. | `Task_Ready_To_Submit/quantized-beam-alignment.zip` | `personal_docs/reports/revision-progress-2026-06-22.md` |
| `fog-state-resume` | Feedback addressed; local strict approval gate PASS with no blocking failures. | `Task_Ready_To_Submit/fog-state-resume.zip` | `personal_docs/reports/revision-progress-2026-06-22.md` |
| `policy-revocation-shadow` | Feedback addressed; local strict approval gate PASS with no blocking failures. | `Task_Ready_To_Submit/policy-revocation-shadow.zip` | `personal_docs/reports/revision-progress-2026-06-22.md` |
| `async-executor-liveness` | Feedback addressed; local strict approval gate PASS with no blocking failures. | `Task_Ready_To_Submit/async-executor-liveness.zip` | `personal_docs/reports/revision-progress-2026-06-22.md` |
