# fog-state-resume — revision_1 feedback snapshot

Point-in-time archive of platform feedback for the `fog-state-resume` TERMINUS task.
Captured **2026-05-27**. Submission is in `NEEDS_REVISION`; this is the first revision archive.

---

## Submission identity

| Field             | Value                                            |
| ----------------- | ------------------------------------------------ |
| Folder name       | `fog-state-resume`                               |
| Platform task ID  | `tbench-task` (per agent_review header)          |
| Project           | Terminus-2nd-Edition                             |
| Project ID        | `bfe79c33-8ab0-4061-9849-08d3207c9927`           |
| Submission ID     | `ec8bf6df-d0d2-40bf-ba64-67ea0f67e002`           |
| Assignment ID     | `51f38673-072f-40dd-9f32-4f1bb491ff94`           |
| Submission VID    | `abf2a515-6940-4b7f-af34-e298baa1ad71`           |
| Created           | 2026-05-25 13:05                                 |
| Evaluation ID     | `b84b7436-b9ec-43a8-8eb0-e519fc75891d`           |
| Evaluation status | `COMPLETED`                                      |
| Platform state    | `NEEDS_REVISION` (at snapshot time)              |
| Difficulty (toml) | `hard`                                           |
| Category          | `games`                                          |
| Captured at       | 2026-05-27 (this archive)                        |

Multiple submissions for this folder: only the active submission above was archived.

---

## Revision notes (verbatim from platform)

> AutoEval Execution Summary: AutoEval execution failed. Build status: FAILED. Build ID: CodeExecutionEnvironment:fdc24a2b-8628-42ff-b158-f82b024b2158.

The `evaluations[].overall_evaluation_result.notes` array also shows multiple later
`AutoEval Execution Summary` entries with `passed: true` and `Build status: SUCCEEDED`
(latest succeeded build: `a8f6e8dc-769b-4bcb-8bbb-58fb2eb008ac`). So the final blocking
revision note above reflects the **most recent failed AutoEval build** even though earlier
ones in this submission's history succeeded — treat AutoEval reproducibility as a P0.

---

## Headline signals

| Signal                       | Value                                                                 |
| ---------------------------- | --------------------------------------------------------------------- |
| AutoEval build (latest note) | **FAILED** — build `fdc24a2b-8628-42ff-b158-f82b024b2158`             |
| AutoEval build (earlier)     | SUCCEEDED — build `a8f6e8dc-769b-4bcb-8bbb-58fb2eb008ac`              |
| Difficulty (measured)        | **TRIVIAL** — needs at least MEDIUM (declared `hard` in task.toml)    |
| Solvability                  | Solvable — all unit tests passed at least once                        |
| Instruction sufficiency      | NOT_APPLICABLE (debug output unavailable)                             |
| Quality checks               | 8 / 10 pass; 2 fail (`behavior_in_tests`, `structured_data_schema`)   |
| Agent review                 | WARNING — pytest in Dockerfile, untested `one-case.sh` behavior       |
| Rubric line sum              | **15** (within 10–40 range)                                           |

---

## Agent performance

| Agent / model              | Runs | Successes | Timeouts | Other fail | Accuracy |
| -------------------------- | ---- | --------- | -------- | ---------- | -------- |
| `nop`                      | 1    | 0         | 0        | 1          | 0%       |
| `oracle`                   | 3    | 3         | 0        | 0          | 100%     |
| `terminus-claude-opus-4-6` | 5    | 5         | 0        | 0          | **100%** |
| `terminus-gpt5-2`          | 5    | 5         | 0        | 0          | **100%** |

Both production agents solve every run — this drives the TRIVIAL classification despite
the task being declared HARD. The task currently fails the difficulty calibration gate.

### Per-test pass rates (10 runs each)

| Test                                  | Pass / Total |
| ------------------------------------- | ------------ |
| test_run_harness_produces_output      | 10 / 10      |
| test_rook_row                         | 10 / 10      |
| test_bishop_row                       | 10 / 10      |
| test_knight_row                       | 10 / 10      |
| test_lancer_row                       | 10 / 10      |
| test_sentinel_row                     | 10 / 10      |
| test_warden_row                       | 10 / 10      |
| test_path_parity_rook                 | 10 / 10      |
| test_no_wall_steps_knight             | 10 / 10      |
| test_no_hidden_hit_bishop             | 10 / 10      |
| test_effect_epoch_sentinel            | 10 / 10      |
| test_sidecar_order_lancer             | 10 / 10      |
| test_trace_sidecar_warden             | 10 / 10      |
| test_binary_exists                    | 10 / 10      |

Every test passes for every production-agent run; no test has a partial pass rate.

---

## Common failure patterns / instruction gaps

From the quality-check summary and agent_review:

1. **Instruction describes untested behavior.** `one-case.sh` writes
   `/app/output/single-<case>.json` per instruction.md L7, but no test exercises that
   path. Quality check `behavior_in_tests` fails on this.
2. **Schema not documented.** Instruction uses descriptive prose ("side id", "from
   coordinates") while tests index exact keys (`actor`, `from_x`, `from_y`, `to_x`,
   `to_y`, plus `effects[].id`, `effects[].active`, `effects[].epoch`, and trace columns
   `parts[1..2, -1]`). Quality check `structured_data_schema` fails.
3. **pytest installed in Dockerfile.** `environment/Dockerfile` lines 21–23 install
   `pytest==8.4.1` and `pytest-json-ctrf==0.3.5` into the agent image. Convention
   requires those in `tests/test.sh` to keep test deps out of the agent environment.
4. **Difficulty is TRIVIAL, not HARD.** Both production agents solve 5/5 with no
   timeouts. The bug surface is too easy to locate or the failure signal is too direct;
   the task fails the calibration gate.
5. **No explicit "bugs exist" statement.** Suggestion in agent_review.txt — instruction
   never tells the agent there are bugs; agent must infer from running the matrix.

`notes.txt → Analysis on Agent Failures` is NOT_APPLICABLE because the debug bundle for
failure introspection was not produced (no agent failures to analyze).

---

## Directory layout

```
personal_docs/feedback/fog-state-resume/revision_1/
├── README.md                      # this file
├── revision-priorities.md         # P0/P1/P2/P3 action list
├── rubric.txt                     # copy of personal_docs/rubrics/fog-state-resume-rubric.txt (sum=15)
├── feedback/                      # bundle from `stb submissions feedback`
│   ├── notes.txt                  # revision note + difficulty/quality summaries
│   ├── agent_review.txt           # WARNING report from harness review
│   └── agent_logs/
│       ├── summary-of-runs-comment.md
│       └── jobs/                  # per-trial trajectory dirs (nop, oracle, opus, gpt5)
├── submitted-task/                # exact platform zip (do NOT edit)
│   ├── instruction.md
│   ├── task.toml
│   ├── .snorkel_config
│   ├── environment/
│   ├── solution/
│   └── tests/
└── metadata/
    ├── submission_ec8bf6df.json          # full fetch-task payload (~594 KB)
    └── submission_ec8bf6df_summary.json  # trimmed (evaluation notes only)
```

---

## Refresh commands

Run from repo root (path has a space — keep quotes):

```bash
cd "/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS"

# Re-pull feedback (writes new /tmp/feedback_<id>_<ts>/ bundle)
stb submissions feedback ec8bf6df-d0d2-40bf-ba64-67ea0f67e002

# Re-download exact submitted zip
stb submissions download ec8bf6df-d0d2-40bf-ba64-67ea0f67e002 \
  -o "personal_docs/feedback/fog-state-resume/revision_<N>/submitted-task"

# Re-pull assignment JSON
stb submissions fetch-task ec8bf6df-d0d2-40bf-ba64-67ea0f67e002 \
  -o "personal_docs/feedback/fog-state-resume/revision_<N>/metadata"

# Open Experts UI in browser
stb submissions view ec8bf6df-d0d2-40bf-ba64-67ea0f67e002
```

Always create a new `revision_N+1/` folder — never overwrite this archive.

---

## Pointer to live workspace

Live editable task tree: [`tasks/fog-state-resume/`](../../../../tasks/fog-state-resume/)
(any fixes for the next submission go there; copy the archived `submitted-task/`
contents only if the live tree has drifted from the platform copy).
