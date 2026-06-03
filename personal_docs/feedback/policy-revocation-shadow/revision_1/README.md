# policy-revocation-shadow — Revision 1 feedback snapshot

Point-in-time archive of platform feedback for `policy-revocation-shadow`, captured while the active submission was in **NEEDS_REVISION**.

## Submission identity

| Field | Value |
| --- | --- |
| Folder name | `policy-revocation-shadow` |
| Submission ID | `52218157-dee7-483f-a7f5-5653ee5e1d01` |
| Assignment ID | `07211270-9aa6-4e4f-bf8b-91bd33c6d019` |
| Project | Terminus-2nd-Edition (`bfe79c33-8ab0-4061-9849-08d3207c9927`) |
| Platform state at capture | **NEEDS_REVISION** |
| Created | 2026-05-23 21:25 |
| Feedback bundle | `/tmp/feedback_52218157-dee7-483f-a7f5-5653ee5e1d01_20260531T225853Z` |

This is the first archive for this task.

## Revision notes (verbatim)

> The delegation chain clarification is now present, but the verifier still never checks required decision metadata fields like principal, resource, and action. More importantly, all traces are static and there is no dynamic trace or source level guard, so a canned policy audit.json path could satisfy the suite without proving the engine processes current inputs. Add coverage for those required fields and at least one dynamic trace/generalization check before acceptance .

## Headline signals

| Signal | Value |
| --- | --- |
| Difficulty | ✅ HARD |
| Solvability | ✅ all tests passed by at least one agent run |
| Frontier performance | Claude Opus 4.6: 5/5; GPT-5.2: 0/5 |
| NOP / Oracle | NOP 0/1; oracle 3/3 |
| Instruction sufficiency | ✅ PASS |
| Quality check | ✅ 10/10 pass |
| Agent review | ⚠️ NEEDS REVISION only for pytest placement / self-contained test.sh convention |
| Main platform blocker | Verifier does not prove dynamic processing or required metadata fields, so a canned audit path could pass |

## Agent failure pattern

Two failed trials reached 11/12; three reached 8/12. Common implementation misses were stale cache invalidation after grant/revoke, `group_slot` isolation, and per-subject epoch/reuse semantics. The platform's revision note is not about model failure; it is about verifier coverage and anti-hardcoding strength.

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
    ├── submission_52218157.json
    └── submission_52218157_summary.json
```

Live workspace: `tasks/policy-revocation-shadow/`.

## Refresh commands

```bash
stb submissions feedback 52218157-dee7-483f-a7f5-5653ee5e1d01
stb submissions download 52218157-dee7-483f-a7f5-5653ee5e1d01 -o personal_docs/feedback/policy-revocation-shadow/revision_1/submitted-task
stb submissions fetch-task 52218157-dee7-483f-a7f5-5653ee5e1d01 -o personal_docs/feedback/policy-revocation-shadow/revision_1/metadata
stb submissions view 52218157-dee7-483f-a7f5-5653ee5e1d01
```
