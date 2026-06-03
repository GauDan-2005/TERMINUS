# sparse-block-preconditioner — Revision priorities (revision_1)

Action list derived from the platform feedback bundle for submission
`64f78238-acf5-4cce-ba2a-100ea9b5a20f` (NEEDS_REVISION). Items are ranked by
severity. Anything not listed under P0/P1/P2 is in P3 and needs no change.

---

## P0 — Platform blockers (must fix before resubmit)

### P0.1  Independent correctness verification in `tests/test_outputs.py`
- **Source:** Revision Notes (lines 1–2 of notes.txt) + Test Quality Judge ("VULNERABLE — Critical / STRENGTHEN").
- **Current state:** Every assertion in `tests/test_outputs.py` reads values from `solver-audit.json` (produced by the solver binary itself) — `iterations`, `final_residual`, `reported_residual`, `ok`. No test independently loads case data and computes the expected residual or solution.
- **Risk:** An agent can hardcode trivially satisfying values in `drive_u/run.cpp` (e.g. `iterations=1, residuals=0.0, ok=true`) and pass all 13 tests without touching the four buggy modules. This violates the anti-cheating requirement and the verifier-must-check-real-correctness rule.
- **Required fix:** For each case, load `/app/data/<case>/{A,b,reorder}` from the harness, run an independent reference computation (e.g. SciPy CG on the BSR matrix with the documented reorder), and assert that the solver's `final_residual` agrees with `||b - A x||` from the harness's own `x` reconstruction (or compare against tolerances anchored to the independent number). Replace every `assert row["final_residual"] < 1e-8` style check with `assert abs(reported - independent) < eps`.

### P0.2  Strict numeric thresholds not documented in `instruction.md`
- **Source:** Revision Notes + Quality Check FAIL on `behavior_in_task_description`.
- **Current state:** Tests enforce `final_residual < 1e-8` (basalt/flint/garnet), `< 1e-7` (shale/mica/opal), basalt `iterations ≤ 20`, `ok=True` for every row, and `iterations < 200` for all convergent cases. `instruction.md` says only "drifts", "stall", "disagree", "rows stay dirty".
- **Required fix:** Either (a) move the thresholds into `instruction.md` as explicit acceptance criteria, or (b) rewrite the tests so they don't depend on absolute thresholds and instead compare against the independently computed reference (P0.1). The reviewer's preference is (b): "the verifier should calculate correctness independently from the case data so results cannot be spoofed".

### P0.3  Drop the legacy canary string from `solution/solve.sh`
- **Source:** Revision Notes (final paragraph of notes.txt).
- **Current state:** `solution/solve.sh` still contains `# Terminal-Bench Canary, do not remove`.
- **Required fix:** Delete the comment. Edition-2 tasks must not contain the canary string.

---

## P1 — Instruction sufficiency / agent failure drivers

### P1.1  Make the source-bug scope explicit in `instruction.md`
- **Source:** Agent review (Suggestion 1) + autoeval analysis of agent failures.
- **Current state:** Instruction uses symptom-only language ("drifts", "stall", "rows stay dirty"). The autoeval analyze step found all 5 gpt5 trials interpret these as symptoms to observe, not bugs to fix. After fixing the script-path issue, agents stop. Zero of 5 ever touched `scale_q/metric.cpp`, `perm_p/order.cpp`, `bsr_n/layout.cpp`, or `prec_r/apply.cpp`.
- **Required fix:** Add one sentence such as "Identify and fix the source-level defects in the solver modules causing incorrect behaviour under reordered layouts. Rebuild after each change." This keeps the task "hard" (the four bugs are still non-trivial to locate) while breaking the systematic stop-at-script-fix loop. Confirms the rubric line `bsr_n/perm_p/prec_r/scale_q` modules are in scope.

### P1.2  Neutralise the determinism false-positive gate
- **Source:** notes.txt analysis section "Key Differences Between Agents".
- **Current state:** Two consecutive matrix runs producing identical JSON is interpreted by agents as proof of correctness even when both runs report `ok: false` and disagreeing residuals.
- **Required fix:** This resolves itself once P0.1 is done (an independent residual check would have flagged the stall), but worth verifying after the rewrite. Optionally, the instruction can warn that "deterministic output is necessary but not sufficient — the audit must also report `ok=True` with residuals that agree with independent measurement."

### P1.3  Tests agents never pass (track until P0.1 fix is in)
- `test_h7_opal_mixed_reordered_residuals` (5/10)
- `test_i8_reported_matches_true_residual` (5/10)
- `test_z9_row_status_flags` (5/10)

All three failures correlate 1:1 with the four untouched C++ bugs. After fixing P0.1 / P1.1 they should still fail until the bugs are patched, but the rubric will then reward partial credit accurately rather than a binary 0/1.

---

## P2 — Agent-review convention nits

### P2.1  Move pytest installs out of `environment/Dockerfile`
- **Source:** agent_review.txt Warning 1.
- **Current state:** `environment/Dockerfile` lines 21–23 install `pytest==8.4.1` and `pytest-json-ctrf==0.3.5` into the image. The agent workspace will never use these.
- **Required fix:** Delete the `RUN python -m pip install … pytest …` block from `environment/Dockerfile`. Add `pip install pytest==8.4.1 pytest-json-ctrf==0.3.5` to `tests/test.sh` before the pytest invocation. Aligns with the standard Terminal-Bench-2 runner pattern.

---

## P3 — Items that passed (no change needed)

- `behavior_in_tests` — every behaviour in `instruction.md` is exercised by a test.
- `informative_test_structure` — descriptive docstrings, alphabetical prefix scheme, helpers separated from assertions, module-scoped fixture.
- `anti_cheating_measures` — Dockerfile copies only the environment tree; tests/ and solution/ are not in the image. (Effective for file-copy attacks; the *correctness* gap is P0.1.)
- `structured_data_schema` — `/app/docs/layout.md` is normative and lists all seven fields.
- `pinned_dependencies` — base image pinned by SHA-256 digest; apt and pip versions pinned exactly.
- `typos` — none found in filenames, paths, variables.
- `tests_or_solution_in_image` — no COPY for tests/ or solution/; tests bind-mounted at runtime.
- `hardcoded_solution` — `solution/solve.sh` patches the four .cpp modules and rebuilds with CMake (no echoed JSON answer).
- `file_reference_mentioned` — `/app/output/solver-audit.json` and `/app/output/<name>-audit.json` named explicitly in instruction.
- Difficulty/solvability — confirmed HARD and solvable (opus 5/5, oracle 3/3).
- Anti-cheating audit (reward_hacking) — clean across all 5 gpt5 trials.

---

## Resubmit checklist

1. Rewrite `tests/test_outputs.py` to compute expected residuals independently from `data/<case>/` and assert agreement (P0.1).
2. Either move numeric thresholds into `instruction.md` or replace them with reference-comparison tolerances (P0.2).
3. Delete the canary comment from `solution/solve.sh` (P0.3).
4. Add the explicit "fix source-level defects" sentence to `instruction.md` (P1.1).
5. Move pytest pip install from `environment/Dockerfile` to `tests/test.sh` (P2.1).
6. Re-run local checks: `run_static_checks.py`, `check-task.sh`, `validate_submission_zip.py`, `verifier_health.py`.
7. Rebuild zip → `stb submissions update 64f78238-acf5-4cce-ba2a-100ea9b5a20f -p <new.zip>` (do NOT `create`).
8. Once platform state changes, fetch a fresh snapshot into `revision_2/` using the workflow in `personal_docs/feedback.md`.
