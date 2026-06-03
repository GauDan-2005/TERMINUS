# Revision priorities — quantized-beam-alignment (revision_2)

Captured 2026-05-29. Source signals: `feedback/notes.txt`,
`feedback/agent_review.txt`, `feedback/agent_logs/summary-of-runs-comment.md`,
and `metadata/submission_4e774a51.json`.

**There is ONE real blocker this round, and it is a regression from the last
revision: difficulty collapsed from HARD to TRIVIAL.** The revision note still
reads *"AutoEval execution failed. Build status: FAILED"*, but — per the standing
memo *"AutoEval 'Build FAILED' usually means UNSOLVABLE / failed eval gate, not a
broken image"* — that is **not** a Docker build failure. The image builds fine:
oracle solved 3/3 and all 14 agent trials ran with every test 10/10. The
"Build FAILED" string is the generic wrapper for the AutoEval gate failing, and
this round the gate fails because the **difficulty floor (≥ MEDIUM) is not met**.

Goal for revision_3: restore difficulty to at least MEDIUM (ideally HARD)
**without** re-introducing the instruction ambiguities that made revision_1
unsolvable, and clean up the non-blocking pytest-in-Dockerfile WARNING.

> Do NOT chase a Docker build bug. Confirm for yourself first: oracle 3/3 + 14
> trials executing = the image builds. The fix is in the spec/docs (difficulty),
> not the Dockerfile build.

---

## P0 — The blocker: difficulty collapsed to TRIVIAL — restore to ≥ MEDIUM

- Difficulty check this round: **❌ TRIVIAL — requires at least MEDIUM.**
  Metadata `difficulty = trivial`. opus 5/5, gpt5 5/5; all 14 tests 10/10 (the
  five previously-impossible tests — `test_{beta,gamma,delta,epsilon}_path` and
  `test_rust_stage_produces_raw` — now pass every trial).
- **Root cause:** the revised `instruction.md` AND `docs/operations.md` both
  state the exact per-column scales `[2,3,5]` and biases `[1,-1,2]`. That hands
  agents the answer to the one hard reasoning step (`ax → ax_ref` per-column
  reconstruction in `src/a0/mod.rs`), eliminating the difficulty cliff.
- **Action — walk the disclosure back to "specified, not solved":**
  - Remove the literal constants `[2,3,5]`/`[1,-1,2]` from `instruction.md` AND
    from `docs/operations.md`.
  - Keep the *behavioral* requirement (each column position gets its own
    scale/bias on the packed path) so the spec is still sufficient, but make the
    agent **derive** the constants by tracing the Rust code / the `ax_ref`
    dead-code reference, rather than copying them from prose.
  - Keep the two revision_1 fixes that did NOT over-disclose: bare case names in
    `sets.txt` (P-resolved below) and the "cargo is on PATH; Rust binary
    required" note + `cargo --version` echo (these prevent the unsolvable
    Rust-replacement failure mode without trivializing the task).
- **Calibration target — mind the band:** revision_1 was HARD-but-unsolvable
  (0/10 full passes); revision_2 is trivially solvable (10/10). The target is the
  middle: solvable by strong models, but NOT by reading a constant out of the
  instructions. Removing the constants while keeping bare case names + the
  cargo note should land closer to that band. **Iterate on the difficulty check
  until it certifies ≥ MEDIUM with the best models still able to solve it.**
- Sync the live `tasks/quantized-beam-alignment/task.toml`: it still declares
  `difficulty = "hard"`, contradicting the measured `trivial`. Set it to whatever
  the difficulty check certifies after the rework.

---

## P1 — Agent-review WARNING (non-blocking, but fix while you're here)

### P1.1 — Move pytest install out of the Dockerfile into `tests/test.sh`

- Agent review (⚠️ WARNING, 2 items) flags `environment/Dockerfile` lines 31-34
  still installing `pytest==8.4.1 pytest-json-ctrf==0.3.5` (now via a uv venv at
  `/opt/tbench-testing`) **inside the image**, and `tests/test.sh` (lines 1-19)
  calling `python -m pytest` directly without installing its own deps.
- Suggested standard `test.sh` (verbatim from agent_review.txt): install uv →
  `uv venv .tbench-testing` → `source .tbench-testing/bin/activate` → `uv pip
  install pytest==8.4.1 pytest-json-ctrf==0.3.5` → `uv run pytest
  /tests/test_outputs.py -rA --ctrf /logs/verifier/ctrf.json` → write reward.txt.
- This keeps the agent image clean of test tooling and makes `test.sh`
  self-contained/portable. It is **WARNING, not FAIL** — it is not why the gate
  failed (difficulty is) — but it is the only outstanding reviewer item.

> **Doc/CI conflict caveat:** if moving uv install into `test.sh` trips a local
> CI gate (e.g. `run_static_checks.py` docker rules), apply the platform/reviewer
> guidance over the local gate but surface the conflict — see the standing memo
> "Feedback overrides documented policy". Keep the task functional either way.

---

## P2 — Optional clarity suggestion (non-blocking)

### P2.1 — Orientation sentence in `instruction.md`

- Agent review suggests adding one sentence like: "Run `/app/tools/run_local.sh`
  to observe the current incorrect output, then trace the bug through the Rust
  and Go stages." This aids orientation without lowering difficulty.
- Safe to add **only alongside** P0 — i.e. once the literal constants are
  removed. An orientation-to-trace sentence is fine; a constants dump is not.

---

## P3 — Items confirmed passing / resolved this round (no change required)

- Quality check: 10/10 axes pass (behavior_in_task_description, behavior_in_tests,
  informative_test_structure, anti_cheating_measures, structured_data_schema,
  pinned_dependencies, typos, tests_or_solution_in_image, hardcoded_solution,
  file_reference_mentioned).
- Solvable: ✅ (all tests passed by at least one agent run). This was revision_1's
  failure (some tests unsolved by any agent) — now fixed.
- Oracle solve: 3/3; NOP: 0. (Also confirms the image builds and runs.)
- Case-name ambiguity (revision_1 P1.1): **resolved** — `sets.txt` now has bare
  names. Keep this.
- Rust-replacement anti-strategy (revision_1 P1.3): **resolved** — instruction
  states cargo is on PATH and the Rust binary is required; `run_local.sh` echoes
  `cargo --version`. Keep this.

---

## What NOT to do in revision_3

- **Do not edit the Dockerfile to "fix the build."** The image builds; the
  "Build FAILED" note is the difficulty gate, not a compile error. (The earlier
  draft of this file wrongly suspected the build-time `curl … astral.sh` line —
  that suspicion is unfounded; agents ran, so the build succeeded.)
- **Do not re-add the case-name colons** or remove the cargo-on-PATH note — those
  fixes are correct and prevent revision_1's unsolvable failure modes.
- **Do not simply bump `task.toml` `difficulty` down to match `trivial`.** The
  goal is to make the task genuinely harder again, not to relabel it; a TRIVIAL
  task does not meet the project floor regardless of the label.

---

## Sequencing for revision_3

1. **Restore difficulty (P0):** remove the literal `[2,3,5]`/`[1,-1,2]` constants
   from `instruction.md` and `operations.md`; keep the per-column behavioral
   requirement, bare case names, and the cargo note.
2. **Clear the WARNING (P1):** move pytest tooling into a self-contained
   `tests/test.sh`; drop the pytest install from the Dockerfile.
3. Re-run cheap Step 2b gates per CLAUDE.md:
   `./scripts/check-task.sh tasks/quantized-beam-alignment` → oracle 1× → NOP.
4. Re-run the difficulty check; iterate until it certifies ≥ MEDIUM with strong
   models still solving (not trivially, not unsolvable).
5. Set `task.toml` `difficulty` to the certified level.
6. `stb submissions update 4e774a51-688e-46e0-b7bc-c56194572f8c`, then re-run the
   `personal_docs/feedback.md` workflow to capture `revision_3/`.
