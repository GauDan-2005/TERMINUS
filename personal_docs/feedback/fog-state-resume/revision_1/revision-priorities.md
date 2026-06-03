# fog-state-resume — revision_1 priorities

Action list derived from `feedback/notes.txt`, `feedback/agent_review.txt`, and the
difficulty/quality summaries. Order is execution priority for the next revision.

---

## P0 — Platform blockers (must clear before resubmit)

1. **AutoEval build failure on latest evaluation.** Revision note: `AutoEval execution
   failed. Build status: FAILED. Build ID: CodeExecutionEnvironment:fdc24a2b-...`. An
   earlier build (`a8f6e8dc-...`) succeeded, so the failure is intermittent or was
   triggered by a re-run after a change. Reproduce locally via `scripts/check-task.sh`
   plus `verifier_health.py` / `run_static_checks.py`, fix the build cause, and confirm
   it is repeatable before resubmitting.

2. **Difficulty calibrated TRIVIAL — requires at least MEDIUM.** Both production agents
   solve 5/5 with no timeouts; declared `difficulty = "hard"` in `task.toml`. Either
   (a) increase real difficulty (deepen the bug surface, remove obvious tells in source
   layout/comments, add a subtler interaction between phase_a/fold_b/mark_c bugs) or
   (b) downgrade `task.toml` `difficulty` — but the platform requires at least MEDIUM, so
   raising difficulty is the productive path.

---

## P1 — Instruction / coverage drivers

3. **Quality check `behavior_in_tests` FAILS — `one-case.sh` is unverified.**
   Instruction L7 specifies `bash /app/scripts/one-case.sh <case>` writes
   `/app/output/single-<case>.json` matching the matrix row, but no test invokes it.
   Either add a test (template in `agent_review.txt`, suggested name
   `test_one_case_matches_matrix`) **or** remove the sentence from `instruction.md`. A
   test is preferred because it tightens the contract.

4. **Quality check `structured_data_schema` FAILS — schema is prose only.** Document
   exact JSON keys used by tests:
   - move row: `actor`, `from_x`, `from_y`, `to_x`, `to_y`, `kind`, `legal`, `turn`
   - effects row: `id`, `active`, `epoch`
   - log/trace column layout: `case_name \t turn \t actor \t from_x \t from_y \t to_x \t to_y \t legal`
   Add a schema block (table or fenced JSON sample) to `instruction.md` so the agent
   does not have to read tests to learn key names.

5. **Make the bug premise explicit (agent_review suggestion).** Add one sentence such
   as "The current codebase produces an incorrect audit; identify and fix the issues so
   the matrix run is clean." This does not reduce difficulty (locating the bugs is the
   work) but removes ambiguity about whether the agent is implementing vs. debugging.

---

## P2 — Convention / harness hygiene

6. **Move pytest install out of Dockerfile.** `environment/Dockerfile` lines 21–23
   install `pytest==8.4.1` and `pytest-json-ctrf==0.3.5` into the agent image. Per
   convention, install them inside `tests/test.sh` (the suggested snippet using `uv pip`
   is in `agent_review.txt`). Remove the RUN block from the Dockerfile.

7. **Minor instruction/JSON terminology drift.** Instruction calls the actor field
   "side id"; JSON uses `actor`. Either rename the JSON key or align the prose. Fix
   when P1#4 is being addressed.

---

## P3 — Items already passing (no change needed)

- `behavior_in_task_description` — pass.
- `informative_test_structure` — pass.
- `anti_cheating_measures` — pass; tests/ and solution/ excluded from image; tests run
  the real engine binary.
- `pinned_dependencies` — pass; base image pinned by SHA-256, apt packages and python
  packages all version-pinned.
- `typos` — pass.
- `tests_or_solution_in_image` — pass; only required source dirs copied in.
- `hardcoded_solution` — pass; solution patches source + rebuilds + runs real engine.
- `file_reference_mentioned` — pass; both `/app/output/resume-audit.json` and
  `/app/output/single-<case>.json` are explicitly named.

Keep these stable — do not regress while addressing P0/P1.

---

## Tests agents never pass

**None.** Every test passes 10 / 10 across the 14 enumerated tests in `notes.txt`. The
problem is the inverse: all tests pass too easily, which is why difficulty calibrates
TRIVIAL. No tests-never-pass mitigation is required this revision.
