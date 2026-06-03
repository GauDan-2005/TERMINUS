# quantized-beam-alignment — revision_2 feedback snapshot

Point-in-time archive of the platform feedback for submission `4e774a51`,
captured **2026-05-29**. **Do not edit anything under `submitted-task/`** — that
directory is the exact zip captured from the platform at fetch time.

> **TL;DR — ONE real blocker, and it's a regression:**
> The single blocker is **difficulty COLLAPSED to ❌ TRIVIAL** (it was ✅ HARD at
> revision_1). The revision note still says *"AutoEval execution failed. Build
> status: FAILED"* (new build id `b8b8d385-…`), **but that is NOT a Docker build
> failure** — the image demonstrably builds: oracle ran 3/3 and all 14 agent
> trials executed with every test 10/10. Per the standing memo *"AutoEval 'Build
> FAILED' usually means UNSOLVABLE / failed eval gate, not a broken image"*, the
> "Build FAILED" string is the platform's generic wrapper for a **failed
> difficulty/eval gate** — this round driven by TRIVIAL difficulty.
>
> The submitter revised the zip and fixed **every** revision_1 instruction-gap
> (bare case names, per-column constants, cargo-on-PATH, uv-based pytest) — but
> **over-disclosed** the packed-path constants `[2,3,5]`/`[1,-1,2]` directly in
> `instruction.md` *and* `docs/operations.md`, which removed the difficulty
> cliff. Net result: revision_1's *unsolvable* problem is fixed, but the task
> swung past the target into *trivial*. There is no separate Docker build to fix.

## Submission identity

| Field            | Value |
| ---------------- | ----- |
| Task folder      | `quantized-beam-alignment` (platform name `tbench-task`) |
| Project          | Terminus-2nd-Edition |
| Project ID       | `bfe79c33-8ab0-4061-9849-08d3207c9927` |
| Submission ID    | `4e774a51-688e-46e0-b7bc-c56194572f8c` (same id as revision_1; zip updated) |
| Assignment ID    | `49c16ae8-40f5-41eb-a9ba-0d83914655b6` |
| Submission state | **NEEDS_REVISION** |
| Payment status   | PENDING |
| Submitted (listing) | 2026-05-25 14:09 |
| Captured         | 2026-05-29 (this revision folder) |
| `.snorkel_config` | points to `4e774a51` (matches archive) |
| Metadata `difficulty` | `trivial` |

This is **submission #3** in `stb submissions list` (folder
`quantized-beam-alignment`). It is the only submission bound to this folder; the
older `5586b05b` submission noted in revision_1 remains superseded.

## What changed since revision_1

The submitter pushed a revised zip (same submission id, via
`stb submissions update`). `submitted-task/` content genuinely differs from
revision_1:

| File | Change |
| ---- | ------ |
| `environment/config/sets.txt` | `alpha:baseline` … → bare `alpha`, `beta`, `gamma`, `delta`, `epsilon`, `zeta` (fixes revision_1 **P1.1** case-name ambiguity) |
| `instruction.md` | + "The Rust release binary is required for raw output; cargo is on PATH in the runtime." (revision_1 **P1.3**) and + a sentence giving packed-path **per-column scales `[2,3,5]`, biases `[1,-1,2]`** (revision_1 **P1.2**) |
| `environment/docs/operations.md` | + "Packed integer rows expand with per-column scales `[2,3,5]` and biases `[1,-1,2]` … Each column index picks its own scale and bias pair." (revision_1 **P1.2**) |
| `environment/tools/run_local.sh` | + `cargo --version` echo before build (revision_1 **P1.3** discoverability) |
| `environment/Dockerfile` | pytest install moved from `pip --break-system-packages` to a **uv venv** (`uv venv /opt/tbench-testing` + `uv pip install pytest==8.4.1 pytest-json-ctrf==0.3.5`); adds `ca-certificates`, `curl`, fetches uv over network from `astral.sh` at build time (partial revision_1 **P0.2** — but still in the image, not `test.sh`) |
| `.step2b-checksum`, `.step2b-metrics.jsonl` | regenerated for the new content |

`instruction.md` sha256: `0bb38…` (r1) → `a518b…` (r2).

| Pipeline | revision_1 (2026-05-27) | revision_2 (2026-05-29) |
| -------- | ----------------------- | ----------------------- |
| AutoEval gate ("Build FAILED") | FAILED `f9009f4a-…` (gate: unsolvable) | **FAILED** `b8b8d385-…` (gate: TRIVIAL) — *not* a Docker build error |
| Image actually builds? | yes (oracle 3/3) | yes (oracle 3/3 + 14 trials ran) |
| Difficulty | ✅ HARD | **❌ TRIVIAL** (needs ≥ MEDIUM) |
| Solvable | ❌ some tests unsolved by any agent | ✅ all tests solved |
| opus / gpt5 | 0/5 / 0/5 | **5/5 / 5/5** |
| Tests at 0/10 | beta,gamma,delta,epsilon,rust_stage | **none — all 14 at 10/10** |
| Quality checks | 10/10 pass | 10/10 pass |
| Agent review | WARNING (pytest in Dockerfile) | **WARNING** (pytest still in Dockerfile via uv venv; test.sh not self-contained) |

## Headline signals (this round)

| Signal | Verdict |
| ------ | ------- |
| Platform revision note | **AutoEval execution failed. Build status: FAILED.** (Build ID `CodeExecutionEnvironment:b8b8d385-edf2-48dc-9398-5bf767b6f5e5`) — generic eval-gate-failed wrapper, **not** a Docker build error (image builds; oracle 3/3, 14 trials ran) |
| Difficulty check | **❌ TRIVIAL — requires at least MEDIUM** (the actual reason the gate failed) |
| Solvable | ✅ True (all tests passed by at least one agent run) |
| Task category | debugging |
| Quality check summary | ✅ 10/10 axes pass |
| Agent review | ⚠️ WARNING — pytest installed in Dockerfile, not `test.sh`; `test.sh` not self-contained; + suggestion to add an orientation sentence to `instruction.md` |
| Metadata `difficulty` | `trivial` |
| Formal evaluations | 3 × COMPLETED → NEEDS_REVISION (2× 2026-05-25, 1× 2026-05-28 against the revised zip, job `593809e1`) |

## Agent performance (difficulty check, 10 model trials + references)

| Agent | Runs | Successes | Accuracy |
| ----- | ---- | --------- | -------- |
| oracle | 3 | 3 | 100% |
| nop | 1 | 0 | 0% |
| terminus-claude-opus-4-6 | 5 | 5 | **100%** |
| terminus-gpt5-2 | 5 | 5 | **100%** |

### Per-test pass rates (10 trials) — every test 10/10

```
test_alpha_path  10/10   test_eta_path    10/10   test_lambda_path 10/10
test_beta_path   10/10   test_theta_path  10/10   test_nu_path     10/10
test_gamma_path  10/10   test_iota_path   10/10   test_mu_path     10/10
test_delta_path  10/10   test_kappa_path  10/10   test_rust_stage_produces_raw 10/10
test_epsilon_path 10/10  test_zeta_path   10/10
```

The five tests that were **0/10** at revision_1 (`test_beta_path`,
`test_gamma_path`, `test_delta_path`, `test_epsilon_path`,
`test_rust_stage_produces_raw`) are now all **10/10** — direct evidence the
`ax → ax_ref` reasoning step is no longer required because the constants are
disclosed in the spec/docs.

## Why the difficulty collapsed (root cause)

revision_1's plan (P1.2) suggested making per-column behavior explicit "while
keeping the buggy `ax()` unchanged" and adding a SCALES/BIASES example **to a
docs file** so the Rust-replacement cohort could derive constants. The submitted
revision went further than intended:

- `instruction.md` now states the exact constants `[2,3,5]`/`[1,-1,2]` **and**
  the per-column requirement, in the primary task text.
- `docs/operations.md` repeats the exact constants and the "each column index
  picks its own scale and bias pair" rule.

With the answer to the single hard reasoning step printed in two places, the
`ax → ax_ref` cliff disappears and the task is now trivial for both models.

## Directory layout

```
revision_2/
├── README.md                         # this file
├── revision-priorities.md            # P0/P1/P2/P3 plan for the next submission
├── rubric.txt                        # local rubric (no platform rubric emitted this round)
├── feedback/                         # copy of /tmp/claude-1000/feedback_4e774a51_20260529T000609Z/
│   ├── notes.txt                     # revision note + difficulty(TRIVIAL) + quality(10/10)
│   ├── agent_review.txt              # harness static review (WARNING — pytest in Dockerfile)
│   └── agent_logs/
│       ├── summary-of-runs-comment.md
│       └── jobs/                     # 14 trial dirs (nop, oracle×3, opus×5, gpt5×5)
├── submitted-task/                   # exact extracted upload (revised content)
│   ├── instruction.md
│   ├── task.toml
│   ├── output_contract.toml
│   ├── construction_manifest.json
│   ├── environment/
│   ├── solution/
│   └── tests/
└── metadata/
    ├── submission_4e774a51.json          # full fetch-task payload (~1.28 MB)
    └── submission_4e774a51_summary.json  # trimmed top-level summary
```

> **Capture note:** stb 2.2.2 writes the feedback bundle to
> `/tmp/claude-1000/feedback_<id>_<ISO8601>Z/`, **not** `/tmp/feedback_<id>_*/`
> as `personal_docs/feedback.md` step 3 documents. Worth fixing in the workflow
> doc. Unlike revision_1, the difficulty check **did** run, so `agent_logs/` is
> present (oracle×3, nop×1, opus×5, gpt5×5).

## Revision notes (verbatim)

```
AutoEval Execution Summary: AutoEval execution failed. Build status: FAILED. Build ID: CodeExecutionEnvironment:b8b8d385-edf2-48dc-9398-5bf767b6f5e5.
```

## Refresh commands

```bash
cd "/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS"

# Re-fetch feedback bundle (writes to /tmp/claude-1000/feedback_<id>_<ISO8601>Z/)
stb submissions feedback 4e774a51-688e-46e0-b7bc-c56194572f8c

# Re-download submitted zip
stb submissions download 4e774a51-688e-46e0-b7bc-c56194572f8c \
  -o personal_docs/feedback/quantized-beam-alignment/revision_3/submitted-task

# Re-fetch metadata
stb submissions fetch-task 4e774a51-688e-46e0-b7bc-c56194572f8c \
  -o personal_docs/feedback/quantized-beam-alignment/revision_3/metadata

# View on platform
stb submissions view 4e774a51-688e-46e0-b7bc-c56194572f8c

# Push the next revision (after fixing build + restoring difficulty in the live workspace)
stb submissions update 4e774a51-688e-46e0-b7bc-c56194572f8c
```

After the next platform round-trip, run the full workflow in
`personal_docs/feedback.md` again to produce `revision_3/` — never overwrite this
folder.

## Live workspace pointer

The active editable workspace for this task is:

`tasks/quantized-beam-alignment/`

As of this capture the live workspace **equals the submitted (trivial) zip** —
live `instruction.md` is byte-identical to `submitted-task/instruction.md` (the
one with the `[2,3,5]`/`[1,-1,2]` constants). So the over-disclosure that caused
the collapse is present in the live workspace and must be edited there.

Note: the live `tasks/quantized-beam-alignment/task.toml` still declares
`difficulty = "hard"`, which now contradicts the platform's measured `trivial`.
Restore real difficulty (remove the disclosed constants — see
revision-priorities.md), re-run the difficulty check, set `task.toml` to the
certified level, then `stb submissions update 4e774a51-688e-46e0-b7bc-c56194572f8c`
to push. There is **no Docker build to repair** — the image builds fine.
