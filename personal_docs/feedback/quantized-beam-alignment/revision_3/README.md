# quantized-beam-alignment — Revision 3 feedback snapshot

Point-in-time archive of platform feedback for the `quantized-beam-alignment`
task, captured **2026-05-30** via `stb submissions feedback / download / fetch-task`.

**Headline:** **NEEDS_REVISION**, but the opposite problem to sparse — the task
is **HARD and arguably too hard**. Difficulty = HARD, quality 10/10, instruction
sufficiency PASS, reviewer READY TO USE, **but no frontier agent passes** (opus
0/5, gpt5 0/5) and **5 of 14 tests are never passed by any non-oracle agent**, so
the difficulty gate returns "not clear if solvable or simply super hard."

## Submission identity

| Field                  | Value                                                         |
| ---------------------- | ------------------------------------------------------------- |
| Folder name            | `quantized-beam-alignment`                                    |
| Submission ID          | `4e774a51-688e-46e0-b7bc-c56194572f8c`                        |
| Assignment ID          | `49c16ae8-40f5-41eb-a9ba-0d83914655b6`                        |
| Project                | Terminus-2nd-Edition (`bfe79c33-8ab0-4061-9849-08d3207c9927`) |
| Current platform state | **NEEDS_REVISION**                                            |
| Latest AutoEval build  | `CodeExecutionEnvironment:4029bf13-c0a5-4c75-a81b-6919c406ac5f` |
| Submission created     | 2026-05-25                                                    |
| Captured at            | 2026-05-30                                                    |

`.snorkel_config` submission_id matches. Second prior archive existed
(revision_1, revision_2); this is **revision_3**.

## Revision notes (verbatim from platform)

> AutoEval Execution Summary: AutoEval execution failed. Build status: FAILED.
> Build ID: CodeExecutionEnvironment:4029bf13-c0a5-4c75-a81b-6919c406ac5f.

> [!NOTE]
> "Build FAILED" is the **difficulty_check verdict**, not infra. Agents ran
> (reward.txt: oracle 3×`1`, every terminus run `0`). The gate is unhappy
> because **no non-oracle agent solved all tests** (HARD but possibly too hard).

## Headline signals (latest evaluation)

| Check                        | Result                                                       |
| ---------------------------- | ----------------------------------------------------------- |
| **difficulty_check**         | ✅ HARD, **but** ❌ "some tests not passed by any agent run"  |
| solvable                     | ⚠️ only the **oracle** (author solution) passes all         |
| Quality check (10 axes)      | ✅ **all 10 PASS**                                           |
| Instruction sufficiency      | ✅ **PASS** (codebase provides the spec; clue present)       |
| claude_code_reviewer         | ✅ **PASS — READY TO USE** (1 cosmetic suggestion)           |
| **Final platform decision**  | **NEEDS_REVISION** (driver: 0% frontier success / too hard) |

## Agent performance (difficulty_check)

| Agent                    | Runs | Successes | Accuracy |
| ------------------------ | ---- | --------- | -------- |
| nop                      | 1    | 0         | 0.0      |
| oracle                   | 3    | 3         | 1.0      |
| terminus-claude-opus-4-6 | 5    | **0**     | **0.0**  |
| terminus-gpt5-2          | 5    | **0**     | **0.0**  |

Per-test pass rate: 9/14 pass 10/10; **never passed by any agent (0/10):**
`test_beta_path`, `test_gamma_path`, `test_delta_path`, `test_epsilon_path`,
`test_rust_stage_produces_raw`.

## Common failure pattern (from notes.txt analysis)

All agents fix the "plumbing" (run_local.sh PATH, Go `fold()` dedup, Go `agree`
field-by-field) → 9/14. **None** crack the core Rust computation bugs in
`src/a0/mod.rs`, `src/b1/mod.rs`, `src/c2/mod.rs`:

- `ax()` uses a per-row scale/bias index (`c % len`) instead of per-column
  (`i % len`) → wrong `produced` for packed cases.
- `bx()` returns input indices instead of looking them up through handle vector `a.v`.
- `cx()` accumulates with `+=` instead of replacing with `=`.

The "smoking gun" `ax_ref()` reference function sitting next to buggy `ax()` went
unnoticed in every trial. Plateau is a flat **9/14 (64%)** with zero variance.
No reward hacking; failures attributed to investigation depth, not instructions.

## Agent review (claude_code_reviewer) — READY TO USE

- **SUGGESTION (cosmetic)** — `data/` has alpha/beta/gamma/delta but not
  epsilon/zeta though `config/sets.txt` lists all six; case data is hardcoded in
  `main.rs`. Add `epsilon.txt`/`zeta.txt` or remove unused data files.

## Directory layout

```
revision_3/
├── README.md
├── revision-priorities.md
├── rubric.txt                 # author rubric (copied from personal_docs/rubrics)
├── feedback/
│   ├── notes.txt
│   ├── agent_review.txt        # PASS / READY TO USE
│   └── agent_logs/
│       ├── analyze-output-tbench-task.json
│       ├── summary-of-runs-comment.md
│       └── jobs/               # 14 per-trial dirs
├── submitted-task/             # exact evaluated artifact — DO NOT EDIT (31 files)
└── metadata/
    └── submission_4e774a51.json
```

## Refresh commands

```bash
cd "/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS"
stb submissions feedback   4e774a51-688e-46e0-b7bc-c56194572f8c
stb submissions download   4e774a51-688e-46e0-b7bc-c56194572f8c -o <rev>/submitted-task
stb submissions fetch-task 4e774a51-688e-46e0-b7bc-c56194572f8c -o <rev>/metadata
```

Live workspace: `tasks/quantized-beam-alignment/`.
