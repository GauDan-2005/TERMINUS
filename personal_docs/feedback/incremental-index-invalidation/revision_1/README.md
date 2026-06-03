# incremental-index-invalidation — Revision 1 feedback snapshot

Point-in-time archive of platform feedback for `incremental-index-invalidation`, captured while the active submission was in **NEEDS_REVISION**.

## Submission identity

| Field | Value |
| --- | --- |
| Folder name | `incremental-index-invalidation` |
| Submission ID | `f0ec5d42-9e1a-4709-9852-acfa502041c5` |
| Assignment ID | `d6742dfc-176e-40c1-ad67-5dbdc7c3afd3` |
| Project | Terminus-2nd-Edition (`bfe79c33-8ab0-4061-9849-08d3207c9927`) |
| Platform state at capture | **NEEDS_REVISION** |
| Created | 2026-05-19 06:38 |
| Feedback bundle | `/tmp/feedback_f0ec5d42-9e1a-4709-9852-acfa502041c5_20260531T225937Z` |

This is the first archive for this task.

## Revision notes (verbatim)

> Needs revision before acceptance. The verifier issue remains unresolved because tests/test.sh does not propagate the pytest exit code. Capture PYTEST_RC=$?, write reward.txt from that result, and exit "$PYTEST_RC". This is a blocking test-harness issue despite otherwise strong task quality.

## Headline signals

| Signal | Value |
| --- | --- |
| Difficulty | ✅ MEDIUM |
| Solvability | ✅ all tests passed by at least one agent run |
| Frontier performance | Claude Opus 4.6: 2/5; GPT-5.2: 4/5 |
| NOP / Oracle | NOP 0/1; oracle 3/3 |
| Instruction sufficiency | ✅ PASS |
| Quality check | ✅ 10/10 pass |
| Agent review | ✅ READY TO USE; only warns about visible offline wheels |
| Main platform blocker | `tests/test.sh` does not propagate pytest's exit code |

## Agent failure pattern

Three failed trials reached 11/12 and all missed the same epoch-source bug in `r4/e.rs`; one trial took a broad wrong path and reached 6/12. The task quality was otherwise assessed as strong. The revision is a harness fix, not a concept rewrite.

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
    ├── submission_f0ec5d42.json
    └── submission_f0ec5d42_summary.json
```

Live workspace: `tasks/incremental-index-invalidation/`.

## Refresh commands

```bash
stb submissions feedback f0ec5d42-9e1a-4709-9852-acfa502041c5
stb submissions download f0ec5d42-9e1a-4709-9852-acfa502041c5 -o personal_docs/feedback/incremental-index-invalidation/revision_1/submitted-task
stb submissions fetch-task f0ec5d42-9e1a-4709-9852-acfa502041c5 -o personal_docs/feedback/incremental-index-invalidation/revision_1/metadata
stb submissions view f0ec5d42-9e1a-4709-9852-acfa502041c5
```
