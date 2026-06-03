# staged-snapshot-drift — revision priorities (revision_2)

Submission: `d6d229bf-537c-414f-a71f-74582b7ee47c` — state `NEEDS_REVISION` (captured 2026-05-28, ~13 days stale).

> **Status vs revision_1: all priorities still open.** The platform feedback, submitted zip, and metadata are byte-identical to `revision_1`, and the live workspace still matches the submitted content. Nothing has been applied or resubmitted. The list below is carried forward unchanged, with current-state confirmations added.

## P0 — platform blockers

- **P0-1. AutoEval build failure on the latest eval (eval 7, 2026-05-25).** Build `16813e8c-25e4-49b6-98c3-53a115ee1258` failed. The *other* CodeBuild in the same eval — the code-quality/check build embedded in `metadata → task_documents[0].submission_document.code_quality_check_results` — **succeeded at every phase** (DOWNLOAD_SOURCE → BUILD → POST_BUILD → UPLOAD_ARTIFACTS, 2026-05-25 11:58–12:00). So the failure is isolated to the AutoEval/difficulty build, whose full log is **not** in the JSON; it is only referenced via the artifact S3 key `codebuild_uploads/autoeval_artifacts/d6d229bf.../59eddd31/difficulty_check_artifact.zip`.
  - The platform's overall outcome is gated by the latest build, so the surface fix is to resubmit (`stb submissions update`) and let CI re-run.
  - Before resubmitting, sanity-check `environment/Dockerfile` and `tests/test.sh` for infra fragility (network calls during build, base-image SHA churn, daemon/timeout). A prior `dockerd`/`docker info` 30s wait is present in the buildspec — confirm it is not the flake source.
  - To get the actual failure cause, pull the difficulty-check artifact (S3 key above) or open `stb submissions view "$SID"`; the bundled `agent_logs/` here is from the last *successful* difficulty run and will not show the eval-7 build error.

## P1 — difficulty and rubric integrity (these will keep coming back even if AutoEval passes)

- **P1-1. Difficulty miscalibration: EASY, platform requires at least MEDIUM.** Combined agent accuracy ≈ 90% (claude-opus-4-6 5/5, gpt5-2 4/5). `task.toml` claims `difficulty = "hard"` (and `metadata.extra.difficulty_label = "hard"`), contradicting both the platform rating and the measured pass rate. Raise actual difficulty (deeper bug interleavings, a non-debugging step, or remove the affordance that lets a single Claude run pass every time) **and** reconcile the `task.toml` label with reality.
- **P1-2. Test-quality judge: VULNERABLE / Major / STRENGTHEN.** Two structural holes (verbatim from the judge):
  - No assertion that the internal row-processing pipeline (`b1.FoldRows`, `c2.ItemsC`, etc.) is actually exercised. An agent can rewrite ~30 lines in `cmd/ctl/main.go` (swap `Materialize` for `cp -a`, replace accounting with a short filesystem walk) and bypass all ~9 intended bugs. Add a Go unit test that drives the internal packages directly, or hash `internal/*` and whitelist allowable fixes.
  - `probe/measure.c` C bugs are only caught indirectly via the accounting JSON. Add a direct test that runs the `fsmeasure` binary on a known directory and asserts byte-for-byte output.
  - Also: no check that the existing package structure remains intact.
  - **This is likely the root of the PASS→NEEDS_REVISION pattern** — closing the bypass also tends to nudge difficulty up (P1-1).
- **P1-3. Rubric magnitude exceeds the 10–40 cap.** Positive items sum to +28, negative to −18, so `|pos| + |neg| = 46` (cap 40). Trim or merge low-leverage items. (Confirmed unchanged in this revision's `test_rubrics`.)

## P2 — agent-review nits

- **P2-1. Move pytest install out of the Dockerfile.** `environment/Dockerfile` lines ~20–22 install `pytest==8.4.1` and `pytest-json-ctrf==0.3.5` in the image. Standard Terminal-Bench pattern installs them in `tests/test.sh` via `uv pip install`. The suggested `test.sh` is in `feedback/agent_review.txt`.
- **P2-2. One-sentence instruction nudge.** `instruction.md` (verified this revision, 1751 bytes, regular file) says "Restored directories are out of agreement with their sources across all six matrix cases" but, per the agent-review suggestion, "does not explicitly state that there are bugs in the Go source code that need fixing." Suggested addition (verbatim from `agent_review.txt`): *"The source code under /app/internal contains logic errors that cause incorrect staging, replay, grouping, and accounting behavior."* Preserves debugging difficulty, reduces wasted time on wrong hypotheses (missing data / misconfiguration). Note this is a **non-blocking SUGGESTION**, not the WARNING. (Not applied.)

## P3 — passed (no change needed)

- Quality check 10-axis: all 10 PASS (behavior-in-task-description, behavior-in-tests, informative-test-structure, anti-cheating-measures, structured-data-schema, pinned-dependencies, typos, tests-or-solution-in-image, hardcoded-solution, file-reference-mentioned).
- Instruction sufficiency: PASS.
- CI / fast static checks: passed; `long_context_quality/skip` (not a long-context task).
- Hack check on the failing gpt5 trial: clean (no cheating detected).
- Solvability: confirmed (every test passes on at least one run; oracle 3/3).
- Code-quality CodeBuild (eval 7): succeeded at all phases.

## Tests agents never pass

None. Worst per-test pass rate is 9/10 (`test_epsilon_matrix`, `test_zeta_matrix`); both failed on the same single gpt5 trial due to the unfixed `mark_c` period-flag bug. Not flaky, not unreachable.

## Recommended order for the next revision

1. **P1-2** (close the `cp -a` / pipeline-bypass shortcut) — highest leverage; also addresses difficulty and likely the regression driver.
2. **P1-1 / P1-3** — re-calibrate difficulty and reconcile the `task.toml` label; trim the rubric under 40.
3. **P2-1 / P2-2** — Dockerfile pytest move and the instruction nudge.
4. **P0-1** — run `stb submissions update` so AutoEval re-runs cleanly, after the above are in place. If the eval-7 build error turns out to be pure infra flake, a resubmit alone may flip it, but resubmitting without P1 fixes will just regress again (the task has already cycled PASS→NEEDS_REVISION three times).
