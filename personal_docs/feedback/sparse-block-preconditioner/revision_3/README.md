# sparse-block-preconditioner — Revision 3 feedback snapshot

Point-in-time archive of platform feedback for the `sparse-block-preconditioner`
task, captured **2026-05-30** via `stb submissions feedback / download / fetch-task`.

**Headline:** still **NEEDS_REVISION** for the *same* reason as revision_2 — the
task **remains TRIVIAL** (both frontier agents solve it 5/5). Every other
automated check passes (quality 10/10, test-quality robust, reviewer READY TO
USE). The difficulty collapse identified in revision_2 was **not** resolved in
the latest re-evaluation (new build `74b978d6`, verdict still TRIVIAL).

## Submission identity

| Field                  | Value                                                         |
| ---------------------- | ------------------------------------------------------------- |
| Folder name            | `sparse-block-preconditioner`                                 |
| Submission ID          | `64f78238-acf5-4cce-ba2a-100ea9b5a20f`                        |
| Assignment ID          | `961990f5-3736-4942-bc08-2fd732041f9b`                        |
| Project                | Terminus-2nd-Edition (`bfe79c33-8ab0-4061-9849-08d3207c9927`) |
| Current platform state | **NEEDS_REVISION**                                            |
| Latest AutoEval build  | `CodeExecutionEnvironment:74b978d6-2ad6-452f-98de-5b4b38f33330` |
| Submission created     | 2026-05-25                                                    |
| Captured at            | 2026-05-30                                                    |

`.snorkel_config` submission_id matches the active submission. This is the
**third** archived snapshot (revision_1 = original test-quality gap; revision_2 =
first TRIVIAL collapse; revision_3 = collapse persists).

## Revision notes (verbatim from platform)

> AutoEval Execution Summary: AutoEval execution failed. Build status: FAILED.
> Build ID: CodeExecutionEnvironment:74b978d6-2ad6-452f-98de-5b4b38f33330.

> [!NOTE]
> "Build FAILED" here is the **difficulty_check verdict**, not a Docker/infra
> build error. Agents ran to completion (see reward.txt — opus 5×`1`, gpt5
> 5×`1`); the gate fails because the measured difficulty is **TRIVIAL**.

## Headline signals (latest evaluation)

| Check                        | Result                                                       |
| ---------------------------- | ----------------------------------------------------------- |
| **difficulty_check**         | ❌ **TRIVIAL — requires at least MEDIUM** (sole blocker)     |
| solvable                     | ✅ all tests passed by ≥1 agent                              |
| Quality check (10 axes)      | ✅ **all 10 PASS**                                           |
| test_quality_judge           | ✅ (implied robust — no test-quality flag this round)        |
| claude_code_reviewer         | ✅ **PASS — READY TO USE** (1 warning, 1 suggestion, non-blocking) |
| Instruction sufficiency      | ➖ NOT_APPLICABLE (no agent failures to analyze)             |
| **Final platform decision**  | **NEEDS_REVISION** (single driver: difficulty)              |

## Agent performance (difficulty_check)

| Agent                    | Runs | Successes | Accuracy |
| ------------------------ | ---- | --------- | -------- |
| nop                      | 1    | 0         | 0.0      |
| oracle                   | 3    | 3         | 1.0      |
| terminus-claude-opus-4-6 | 5    | **5**     | **1.0**  |
| terminus-gpt5-2          | 5    | **5**     | **1.0**  |

Per-test pass rate: **all 13 tests 10 / 10.** nop correctly fails (0/1).

## Agent review (claude_code_reviewer) — READY TO USE

- **WARNING** — vendored test wheels (`pytest==8.4.1`, `pytest-json-ctrf==0.3.5`)
  downloaded to `/opt/verifier-wheels/` are visible to the agent. Acceptable
  offline workaround; noted only.
- **SUGGESTION** — instruction could add one sentence like "Multiple modules
  under /app contribute to these failures" so the agent investigates broadly.

## Directory layout

```
revision_3/
├── README.md                  # this file
├── revision-priorities.md     # P0–P3 action list
├── rubric.txt                 # author rubric (copied from personal_docs/rubrics)
├── feedback/                  # copied from /tmp/claude-1000/feedback_64f78238_*
│   ├── notes.txt              # revision notes + difficulty + 10-axis quality
│   ├── agent_review.txt       # claude_code_reviewer (PASS / READY TO USE)
│   └── agent_logs/
│       ├── summary-of-runs-comment.md   # difficulty=trivial run table
│       └── jobs/              # 14 per-trial dirs (nop/oracle/opus/gpt5)
├── submitted-task/            # exact evaluated artifact — DO NOT EDIT (39 files)
└── metadata/
    └── submission_64f78238.json
```

## Refresh commands

```bash
cd "/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS"
stb submissions feedback   64f78238-acf5-4cce-ba2a-100ea9b5a20f
stb submissions download   64f78238-acf5-4cce-ba2a-100ea9b5a20f -o <rev>/submitted-task
stb submissions fetch-task 64f78238-acf5-4cce-ba2a-100ea9b5a20f -o <rev>/metadata
```

Live workspace: `tasks/sparse-block-preconditioner/`.
