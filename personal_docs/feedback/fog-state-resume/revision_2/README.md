# fog-state-resume — Revision 2 feedback snapshot

Point-in-time archive of platform feedback for `fog-state-resume`, captured while the active submission was in **NEEDS_REVISION**.

## Submission identity

| Field | Value |
| --- | --- |
| Folder name | `fog-state-resume` |
| Submission ID | `ec8bf6df-d0d2-40bf-ba64-67ea0f67e002` |
| Assignment ID | `51f38673-072f-40dd-9f32-4f1bb491ff94` |
| Project | Terminus-2nd-Edition (`bfe79c33-8ab0-4061-9849-08d3207c9927`) |
| Platform state at capture | **NEEDS_REVISION** |
| Created | 2026-05-25 13:05 |
| Feedback bundle | `/tmp/feedback_ec8bf6df-d0d2-40bf-ba64-67ea0f67e002_20260531T225800Z` |

This is `revision_2`; `revision_1/` remains untouched.

## Revision notes (verbatim)

> `instruction.md:4` lists move/signature/sidecar criteria for a clean row but never states ward `active` must survive restore, while `tests/test_outputs.py:198–203` hard-requires `ward[0]["active"] is True`. The audit `ok` field in `environment/internal/exec/run.go:284` mirrors the instruction gap, so agents can believe the task is finished while still failing the ward assertion.
>
> All the caching files and folders must be removed.

## Headline signals

| Signal | Value |
| --- | --- |
| Difficulty | ✅ HARD |
| Solvability | ✅ all tests passed by at least one agent run |
| Frontier performance | Claude Opus 4.6: 5/5; GPT-5.2: 1/5 |
| NOP / Oracle | NOP 0/1; oracle 3/3 |
| Instruction sufficiency | ❌ FAIL — `test_modifier_active_05` checks an active-state invariant absent from the prompt/audit `ok` criteria |
| Quality check | ✅ 10/10 pass in the automated quality panel |
| Agent review | ⚠️ NEEDS REVISION; flags Dockerfile-baked pytest and terse instructions |
| Test most tied to failures | `test_modifier_active_05` passed 6/10; all other tests passed 10/10 |

## Agent failure pattern

The failed GPT-5.2 trials all reached 15/16 tests and missed the same resume-path timed-modifier issue. Three trials stopped after `ok=True` across the seven cases, which is reasonable because the prompt did not say that ward `active` state is part of the clean-row contract. One trial fixed several real source bugs and still missed `mod/effect.go`.

## Directory layout

```
revision_2/
├── README.md
├── revision-priorities.md
├── rubric.txt
├── feedback/
│   ├── notes.txt
│   ├── agent_review.txt
│   └── agent_logs/
├── submitted-task/
└── metadata/
    ├── submission_ec8bf6df.json
    └── submission_ec8bf6df_summary.json
```

Live workspace: `tasks/fog-state-resume/`.

## Refresh commands

```bash
stb submissions feedback ec8bf6df-d0d2-40bf-ba64-67ea0f67e002
stb submissions download ec8bf6df-d0d2-40bf-ba64-67ea0f67e002 -o personal_docs/feedback/fog-state-resume/revision_2/submitted-task
stb submissions fetch-task ec8bf6df-d0d2-40bf-ba64-67ea0f67e002 -o personal_docs/feedback/fog-state-resume/revision_2/metadata
stb submissions view ec8bf6df-d0d2-40bf-ba64-67ea0f67e002
```
