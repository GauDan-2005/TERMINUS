# Task feedback archives

Each task gets its own subdirectory. Every platform feedback fetch creates a new `revision_N/` folder; do not overwrite prior snapshots.

Workflow prompt: [`../feedback.md`](../feedback.md)

## Current archive map (on disk, 2026-06-22)

These are the active `NEEDS_REVISION` rows from the current submission table. The old archive tree had been wiped locally, so each task was re-materialized as `revision_1/` based on the on-disk revision-numbering rule in `personal_docs/feedback.md`.

| Task archive folder | Revision present | Submission | Assignment | Platform signal |
| --- | --- | --- | --- | --- |
| `sparse-block-preconditioner/` | `revision_1/` | `64f78238-acf5-4cce-ba2a-100ea9b5a20f` | `961990f5-3736-4942-bc08-2fd732041f9b` | EASY, solvable, needs MEDIUM+ |
| `quantized-beam-alignment/` | `revision_1/` | `4e774a51-688e-46e0-b7bc-c56194572f8c` | `49c16ae8-40f5-41eb-a9ba-0d83914655b6` | TRIVIAL, solvable, needs MEDIUM+ |
| `fog-state-resume/` | `revision_1/` | `ec8bf6df-d0d2-40bf-ba64-67ea0f67e002` | `51f38673-072f-40dd-9f32-4f1bb491ff94` | EASY, solvable, needs MEDIUM+ |
| `policy-revocation-shadow/` | `revision_1/` | `52218157-dee7-483f-a7f5-5653ee5e1d01` | `07211270-9aa6-4e4f-bf8b-91bd33c6d019` | EASY, solvable, needs MEDIUM+ |
| `async-executor-liveness/` | `revision_1/` | `7243aade-daa1-4513-96d0-7366734d930d` | `3a746d5a-6e17-45ab-91cf-87440414d3d1` | EASY, solvable, needs MEDIUM+ |

Each `revision_1/` holds:

- `feedback/` with `notes.txt`, `agent_review.txt`, and `agent_logs/` when the platform included logs.
- `submitted-task/`, the exact submitted zip extracted by `stb submissions download`.
- `metadata/`, including the full `submission_<short_id>.json` from `stb submissions fetch-task` and a trimmed `submission_<short_id>_summary.json`.
- `README.md`, `revision-priorities.md`, and `rubric.txt`.

## Agent-log availability

| Task | `agent_logs/summary-of-runs-comment.md` | `agent_logs/analyze-output-tbench-task.json` |
| --- | --- | --- |
| `sparse-block-preconditioner` | present | present |
| `quantized-beam-alignment` | present | missing |
| `fog-state-resume` | missing | missing |
| `policy-revocation-shadow` | present | present |
| `async-executor-liveness` | present | present |

When `agent_logs/` is missing, use `feedback/notes.txt`; the platform embedded the failure analysis there.

## Refresh commands

```bash
cd "/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS"

stb submissions feedback <SUBMISSION_ID>
stb submissions download <SUBMISSION_ID> -o personal_docs/feedback/<task>/revision_<N>/submitted-task
stb submissions fetch-task <SUBMISSION_ID> -o personal_docs/feedback/<task>/revision_<N>/metadata
stb submissions view <SUBMISSION_ID>
```

See [`../STATUS.md`](../STATUS.md) for the current assignment-state table.
