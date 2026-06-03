# async-executor-liveness — Revision 1 feedback snapshot

Point-in-time archive of platform feedback for `async-executor-liveness`, captured while the active submission was in **NEEDS_REVISION**.

## Submission identity

| Field | Value |
| --- | --- |
| Folder name | `async-executor-liveness` |
| Submission ID | `7243aade-daa1-4513-96d0-7366734d930d` |
| Assignment ID | `3a746d5a-6e17-45ab-91cf-87440414d3d1` |
| Project | Terminus-2nd-Edition (`bfe79c33-8ab0-4061-9849-08d3207c9927`) |
| Platform state at capture | **NEEDS_REVISION** |
| Created | 2026-05-18 23:44 |
| Feedback bundle | `/tmp/feedback_7243aade-daa1-4513-96d0-7366734d930d_20260531T230027Z` |

This is the first archive for this task.

## Revision notes (verbatim)

> This is much closer than the earlier review. I built the image locally and the oracle plus mounted verifier pass offline with 12/12 tests, reward 1, and CTRF present. Cargo is on PATH in the normal container shell, the test names are now descriptive, the rubric panel is fully green, and the prompt now clearly says child rows are scheduled by their own arrival turn rather than waiting for the parent to be accepted. I would not hold the Dockerfile-baked pytest warning against this under the current no-internet verifier setup.
>
> I would still send it back for one small spec fix. The tests require root trace rows to use the literal string "-" for parent, but instruction.md only says every record has a parent field; it never says what root rows should emit. null is a reasonable interpretation, and the failed-agent analysis shows both agents made exactly that choice.
>
> Please add one explicit sentence, for example: Root records must emit parent as the string "-" in JSON, ledger JSONL, and journal output. Just get those fixes in and resubmit!

## Headline signals

| Signal | Value |
| --- | --- |
| Difficulty | ✅ MEDIUM |
| Solvability | ✅ all tests passed by at least one agent run |
| Frontier performance | Claude Opus 4.6: 5/5; GPT-5.2: 3/5 |
| NOP / Oracle | NOP 0/1; oracle 3/3 |
| Instruction sufficiency | ❌ FAIL — root `parent` sentinel unspecified |
| Quality check | ✅ 10/10 pass |
| Agent review | ⚠️ warning for Dockerfile-baked pytest, but human note says not to hold it against the task |
| Main platform blocker | Add one sentence specifying root `parent` must be the string `"-"` in JSON, ledger JSONL, and journal output |

## Agent failure pattern

Both failed trials chose `null`/`None` for root parents because the instruction only required a parent field. This produced a broad 3/12 plateau despite otherwise legitimate implementations. The platform explicitly characterizes the revision as a small spec fix.

## Directory layout

```
revision_1/
├── README.md
├── revision-priorities.md
├── feedback/
│   ├── notes.txt
│   ├── agent_review.txt
│   └── agent_logs/
├── submitted-task/
└── metadata/
    ├── submission_7243aade.json
    └── submission_7243aade_summary.json
```

Live workspace: `tasks/async-executor-liveness/`.

## Refresh commands

```bash
stb submissions feedback 7243aade-daa1-4513-96d0-7366734d930d
stb submissions download 7243aade-daa1-4513-96d0-7366734d930d -o personal_docs/feedback/async-executor-liveness/revision_1/submitted-task
stb submissions fetch-task 7243aade-daa1-4513-96d0-7366734d930d -o personal_docs/feedback/async-executor-liveness/revision_1/metadata
stb submissions view 7243aade-daa1-4513-96d0-7366734d930d
```
