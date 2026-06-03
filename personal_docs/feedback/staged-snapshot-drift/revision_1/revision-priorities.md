# staged-snapshot-drift — revision priorities (revision_1)

Submission: `d6d229bf-537c-414f-a71f-74582b7ee47c` — state `NEEDS_REVISION` (captured 2026-05-27, ~12 days stale).

## P0 — platform blockers

- **P0-1. AutoEval build failure on final eval.** Eval 7's last CodeBuild (`16813e8c-25e4-49b6-98c3-53a115ee1258`) failed; the preceding build in the same eval succeeded. The platform's overall outcome is gated by the latest build, so the surface fix is to resubmit and let CI re-run. Prior to resubmission, sanity-check `environment/Dockerfile` and `tests/test.sh` for any infra-fragility (network calls during build, base-image SHA churn). Look at `feedback/agent_logs/jobs/*/job.log` and the full `code_quality_check_results` log under `metadata/submission_d6d229bf.json -> task_documents[0].submission_document.code_quality_check_results` to confirm the failure was infra and not deterministic.

## P1 — difficulty and rubric integrity (these will keep coming back even if AutoEval passes)

- **P1-1. Difficulty miscalibration: EASY instead of required MEDIUM+.** Combined agent accuracy is 90 percent (Claude-opus 5/5, gpt5 4/5). Platform flagged the task EASY and requires at least MEDIUM. `task.toml` claims `hard`, contradicting both signals. Add one or more of: deeper bug interleavings, a non-debugging step, or remove the affordance that lets a single Claude run succeed every time.
- **P1-2. Test-quality judge: VULNERABLE / STRENGTHEN.** Two structural holes:
  - No assertion that the row-based pipeline (`b1.FoldRows`, `c2.ItemsC`, etc.) is exercised. An agent can swap `Materialize` for `cp -a` and replace accounting with a 15-line filesystem walk (~30 lines total) and bypass all 9 intended bugs. Either add a Go unit test that drives the internal packages directly, or hash internal/* files and whitelist allowable fixes.
  - `probe/measure.c` C bugs (`zeroes d/`, halves `shared`, `+1` for `c/`) are only caught indirectly via accounting JSON. Add a direct test that runs the `fsmeasure` binary on a known directory and asserts byte-for-byte output.
- **P1-3. Rubric magnitude exceeds the 10-40 cap.** Positive items sum to +28, negative to -18, so |pos|+|neg| = 46 (workflow cap is 40). Trim or merge a low-leverage item.

## P2 — agent review nits

- **P2-1. Move pytest install out of Dockerfile.** Currently in `environment/Dockerfile` lines 20-22 (`pytest==8.4.1`, `pytest-json-ctrf==0.3.5`). Standard Terminal-Bench pattern is to install in `tests/test.sh` via `uv pip install`. Suggested test.sh shell shown in `feedback/agent_review.txt`.
- **P2-2. One-sentence instruction nudge.** `submitted-task/instruction.md` says "Restored directories are out of agreement with their sources" without naming the buggy subsystem. Add: "The source code under `/app/internal` contains logic errors that cause incorrect staging, replay, grouping, and accounting behavior." Preserves debugging difficulty, cuts wasted hypothesis time.

## P3 — passed (no change needed)

- Quality check 10-axis: all 10 pass (behavior-in-task-description, behavior-in-tests, informative-test-structure, anti-cheating-measures, structured-data-schema, pinned-dependencies, typos, tests-or-solution-in-image, hardcoded-solution, file-reference-mentioned).
- Instruction sufficiency: PASS.
- CI / fast static checks: passed; `long_context_quality/skip` (not a long-context task).
- Uniqueness: no duplication.
- Hack check on failing gpt5 trial: clean (no cheating detected).
- Solvability: confirmed (every test passes on at least one run; oracle passes 3/3).

## Tests agents never pass

None. Worst per-test pass rate is 9/10 (`test_epsilon_matrix`, `test_zeta_matrix`); both failed on the same gpt5 trial due to the unfixed `mark_c` period-flag bug. The failure is a single agent reasoning error, not a flaky or unreachable test.

## Recommended order for the next revision

1. Address P1-2 (test-strength shortcut closure) — fixing this likely also nudges difficulty up because the `cp -a` bypass is no longer available.
2. Re-evaluate difficulty calibration and update `task.toml` metadata if still mismatched (P1-1, P1-3).
3. Apply P2 nits.
4. Run `stb submissions update` so AutoEval re-runs cleanly (P0-1).
