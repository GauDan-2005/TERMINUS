# adaptive-mesh-conservation — Revision 1 feedback snapshot

First point-in-time archive of platform feedback for the
`adaptive-mesh-conservation` task, captured **2026-05-30** via
`stb submissions feedback / download / fetch-task`.

**Headline:** **NEEDS_REVISION** with **two real, actionable blockers** (unlike
sparse/quantized whose only issue is difficulty calibration):
1. **Instruction sufficiency FAIL + quality FAIL** — `test_i8` requires a
   `SIGNATURE_MISMATCH` / fingerprint rejection that is **never described** in
   `instruction.md` or `layout.md` (a genuine spec gap); adjacency is also not
   hinted by the symptoms.
2. **Agent review = NEEDS REVISION** — `pytest` is installed in the Dockerfile
   instead of a self-contained `test.sh`.

Difficulty itself is fine (**HARD**, 0% frontier success), so do not increase it.

## Submission identity

| Field                  | Value                                                         |
| ---------------------- | ------------------------------------------------------------- |
| Folder name            | `adaptive-mesh-conservation`                                  |
| Submission ID          | `5586b05b-0661-46a5-a2a6-1d98344b0ada`                        |
| Assignment ID          | `fa2ae7c4-4f58-4915-ade1-d6885ab18442`                        |
| Project                | Terminus-2nd-Edition (`bfe79c33-8ab0-4061-9849-08d3207c9927`) |
| Current platform state | **NEEDS_REVISION**                                            |
| Latest AutoEval build  | `CodeExecutionEnvironment:bf5d2e32-2cb2-4fba-ac50-2311c41f451a` |
| Submission created     | 2026-05-22                                                    |
| Captured at            | 2026-05-30                                                    |

No `.snorkel_config` in the live task folder; submission ID resolved from the
project submissions list (folder name match). This is the **first** archive
(`revision_1`).

## Revision notes (verbatim from platform)

> AutoEval Execution Summary: AutoEval execution failed. Build status: FAILED.
> Build ID: CodeExecutionEnvironment:bf5d2e32-2cb2-4fba-ac50-2311c41f451a.

> [!NOTE]
> "Build FAILED" is the difficulty/quality gate verdict, not infra. Agents ran
> (reward.txt: oracle 3×`1`, every terminus run `0`).

## Headline signals (latest evaluation)

| Check                        | Result                                                       |
| ---------------------------- | ----------------------------------------------------------- |
| **difficulty_check**         | ✅ HARD, but ❌ "some tests not passed by any agent run"      |
| Quality check (10 axes)      | ❌ **1 FAIL** — `behavior_in_task_description` (others pass) |
| **Instruction sufficiency**  | ❌ **FAIL** (fingerprint requirement undocumented; adjacency unhinted) |
| claude_code_reviewer         | ⚠️ **WARNING → NEEDS REVISION** (pytest in Dockerfile)      |
| solvable                     | ⚠️ only the **oracle** passes all 13                        |
| **Final platform decision**  | **NEEDS_REVISION** (multiple drivers)                       |

## Agent performance (difficulty_check)

| Agent                    | Runs | Successes | Accuracy |
| ------------------------ | ---- | --------- | -------- |
| nop                      | 1    | 0         | 0.0      |
| oracle                   | 3    | 3         | 1.0      |
| terminus-claude-opus-4-6 | 5    | **0**     | **0.0**  |
| terminus-gpt5-2          | 5    | **0**     | **0.0**  |

Per-test pass rate (13 tests, grading is all-or-nothing 13/13):

| Pass band | Tests |
| --------- | ----- |
| 10/10     | a0, b1, e4, f5, no_canary |
| 7/10      | g6, h7 |
| 6/10      | i8 (tampered snapshot) |
| 3/10      | c2, d3 (adjacency) |
| 2/10      | j9 (resumed adjacency) |
| **0/10**  | **k0, l1 (halo band)** |

Avg ~8.1/13; best trial 11/13 (one fix away). No reward hacking detected.

## Failure patterns + spec gaps (from notes.txt analysis)

Agents reliably fix the 3 "obvious" conservation bugs (`fold_q` weighted avg,
`op_m` per-subface flux, vault FluxBank save/restore) and stop. Reliably missed:

- **Adjacency** (`lnk_n/relate.cpp`): `step_n` never populates
  `child0`/`child_count` → `adjacency` always 0. Not hinted by a conservation
  symptom → 3 tests fail.
- **Halo offset** (`sync_b/halo.cpp` / `drv_u/run_blend.cpp`): `op_b` uses `d=1`
  instead of `d=0` → wrong ghost band → 2 tests fail (k0, l1 never pass).
- **Fingerprint/tamper** (`rsm_k/resume.cpp`): `SIGNATURE_MISMATCH` rejection
  required by `test_i8` but **never described** in instruction/layout → **the
  spec gap** (4 trials flagged `task_specification: fail`).

## Agent review (claude_code_reviewer) — NEEDS REVISION

- **WARNING 1** — `pytest==8.4.1` + `pytest-json-ctrf==0.3.5` installed in
  `environment/Dockerfile` (lines 21–23). Move into `tests/test.sh` using the
  standard uv-based self-contained runner.
- **WARNING 2** — `tests/test.sh` is not self-contained (no curl/uv/pytest
  install preamble); relies entirely on the Dockerfile.

## Directory layout

```
revision_1/
├── README.md
├── revision-priorities.md
├── rubric.txt                 # extracted from metadata test_rubrics (if present)
├── feedback/
│   ├── notes.txt              # difficulty + quality FAIL + instruction FAIL
│   ├── agent_review.txt        # WARNING / NEEDS REVISION (pytest in Dockerfile)
│   └── agent_logs/
│       ├── analyze-output-tbench-task.json
│       ├── summary-of-runs-comment.md
│       └── jobs/               # 14 per-trial dirs
├── submitted-task/             # exact evaluated artifact — DO NOT EDIT (46 files)
└── metadata/
    └── submission_5586b05b.json
```

## Refresh commands

```bash
cd "/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS"
stb submissions feedback   5586b05b-0661-46a5-a2a6-1d98344b0ada
stb submissions download   5586b05b-0661-46a5-a2a6-1d98344b0ada -o <rev>/submitted-task
stb submissions fetch-task 5586b05b-0661-46a5-a2a6-1d98344b0ada -o <rev>/metadata
```

Live workspace: `tasks/adaptive-mesh-conservation/`.
