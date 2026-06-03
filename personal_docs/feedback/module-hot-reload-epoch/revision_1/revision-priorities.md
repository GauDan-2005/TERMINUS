# module-hot-reload-epoch — Revision priorities (revision 1)

Source: `feedback/notes.txt` revision notes, `feedback/agent_review.txt`, `metadata/submission_ea9c5aae.json` → `submission_document.test_quality_judge_report` and `text_summary`. Submission state at capture: **NEEDS_REVISION**, captured 2026-05-27.

The autoeval suite (instruction-sufficiency, reward-hacking, 10-axis quality, AutoEval build) all PASSED. The revision is being requested by **reviewer policy** (prompt-style leak + inaccurate tag) and **test-quality judge** (Rust-runtime bypass).

---

## P0 — Reviewer blockers (must fix before resubmit)

1. **De-leak `instruction.md` per prompt-styling guide.**
   Reviewer note (verbatim): *"Instruction.md leaks bug-level implementation hints. The described invariants map almost directly to specific seeded fixes."*
   Today every clause in `instruction.md` maps to one seeded bug:
   - "carried state stays consistent" → carry through `nativeValue` (a1/p.js)
   - "reloads do not lose pending work" → deferred ownership (b2/q.js)
   - "dependency changes stay isolated to the records that use them" → per-row factor recomputation (c3/r.js)
   - "older records remain readable" → Rust `r_d` carry for "old" revisions (lib.rs)
   - "Aggregate status reads healthy when every scenario is healthy" → d4/s.js hardcoded `status:'stale'`
   Action: rewrite as user-observable symptoms ("running `npm run matrix` twice in a row produces different `report.json` outputs", "older scenarios are mis-reported as stale", "totals do not match input bases"), and remove the enumerated invariant list. Pattern reference: https://snorkel-ai.github.io/Terminus-EC-Training-stateful/portal/docs/understanding-tasks/prompt-styling.

2. **Fix the misleading `hot-reload` tag.**
   Reviewer note: *"The hot-reload tag appears inaccurate for the actual task behavior."*
   The task is not about hot module reloading — it is about state propagation across a matrix run of plugin modules and a Rust native helper. Replace in `task.toml`:
   - Current: `tags = ["nodejs", "rust", "hot-reload", "state", "debugging"]`
   - Suggested: `tags = ["nodejs", "rust", "state-propagation", "native-bindings", "debugging"]`
   Re-check task `name` and description framing for the same drift; consider renaming the folder/slug only if the platform allows (otherwise leave the slug and document the mismatch in the instruction's intro line).

## P1 — Test quality vulnerability (judge severity: Critical)

3. **Strengthen the Rust-invocation guard.**
   `test_quality_judge_report` flags `test_rust_build_artifact_present` as vacuous because `environment/Dockerfile` runs `cargo build --locked --bin mhre_native` at image-build time. Required pattern (from judge):
   - Delete `target/` (or just the `mhre_native` binary) at test start and assert it is rebuilt; OR
   - Capture `os.path.getmtime()` of the binary and assert it post-dates the matrix run; OR
   - Verify via process inspection that `mhre_native` was spawned during `npm run matrix`.

4. **Lock the modular layout.**
   Same judge report recommends a structural assertion that `a1/p.js`, `b2/q.js`, `c3/r.js`, `d4/s.js`, and `src/native/src/lib.rs` still exist and are imported by `tools/run_matrix.js` after the agent edits. Without it, an agent can inline everything into one file and pass.

## P2 — Smaller cleanups

5. **Reconcile declared difficulty.**
   `task.toml` declares `difficulty = "hard"`, but autoeval landed on MEDIUM. After de-leaking the instruction, re-run the difficulty check; if it stays MEDIUM, update `task.toml` to match. The accompanying `expert_time_estimate_min = 120` and `junior_time_estimate_min = 300` look high for the MEDIUM result and should be reviewed alongside.

6. **(Optional) Replace inline schema prose with a JSON example.**
   Harness agent-review suggestion (non-blocking): the `record`/`row`/`aggregate` schema is described in prose; a fenced JSON example block would reduce ambiguity for unfamiliar agents. Address only if it does not re-introduce leak risk (P0).

## P3 — Already healthy, no change needed

- Reward-hacking gating (both trials PASS).
- Instruction sufficiency PASS (autoeval).
- 10/10 axes of the quality check PASS (behavior_in_task_description, behavior_in_tests, informative_test_structure, anti_cheating_measures, structured_data_schema, pinned_dependencies, typos, tests_or_solution_in_image, hardcoded_solution, file_reference_mentioned).
- Pinned dependencies (Rust image tag+digest, all apt + pip + npm versions pinned).
- `pytest` install location in `Dockerfile` flagged as a WARNING but documented as intentional via the `/opt/pytest` venv (acceptable, leave as-is).
- Determinism is verified by `test_report_stable_across_consecutive_runs` (10/10).

## Tests that agents never pass

None. Every test has at least 8/10 pass-rate across the 10 solver runs; both failing trials were the same `terminus-gpt5-2` regressions on `test_case_one`. No test is structurally unsolvable.

---

## Suggested revision sequence

1. Rewrite `instruction.md` first (P0 #1) — it is the headline reviewer ask.
2. Update `task.toml` tags + difficulty (P0 #2, P2 #5).
3. Edit `tests/test_outputs.py` to add the Rust-invocation and modular-layout guards (P1 #3, P1 #4).
4. Re-run `solution/solve.sh` and the local test harness to confirm the oracle still passes with the strengthened guards.
5. `stb submissions update ea9c5aae-7199-46c6-bf5b-236691b01936 -p <new.zip>` to revise in place.
