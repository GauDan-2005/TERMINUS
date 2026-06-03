# Revision priorities — quantized-beam-alignment (revision_1)

Source signals: `feedback/notes.txt`, `feedback/agent_review.txt`,
`feedback/agent_logs/summary-of-runs-comment.md`, and per-trial logs under
`feedback/agent_logs/jobs/`.

Goal: clear the AutoEval build failure, keep the HARD difficulty, and remove
the two spec ambiguities that turned the existing difficulty into noise
instead of intended challenge.

---

## P0 — Platform blockers (must fix before resubmit)

### P0.1 — Resolve AutoEval build failure

- Platform revision note: *"AutoEval execution failed. Build status: FAILED.
  Build ID: CodeExecutionEnvironment:f9009f4a-00b4-43ad-b3f4-abba8e418c15."*
- This is the only blocking signal in the revision note. Until AutoEval
  builds the image, the rest of the rubric cannot run.
- Action: rebuild locally with `scripts/check-task.sh` and inspect the
  `environment/Dockerfile`. The likely culprits flagged by the agent
  reviewer (P2.1) are also build-fragility flags — fixing pytest-out-of-image
  may quietly resolve this. If not, log full Docker build output and trace
  layer failures.

### P0.2 — Move pytest install out of the Dockerfile

- Agent reviewer flags `environment/Dockerfile` lines 21-23 (`pip install
  pytest==8.4.1 pytest-json-ctrf==0.3.5 --break-system-packages`) as
  non-portable; `tests/test.sh` then calls `python -m pytest` directly
  without its own venv.
- Migrate to the standard self-contained `test.sh` pattern (uv install →
  `uv venv .tbench-testing` → `uv pip install pytest==8.4.1
  pytest-json-ctrf==0.3.5` → `uv run pytest ... --ctrf
  /logs/verifier/ctrf.json`) and delete the Dockerfile lines.
- This is officially "WARNING" not "FAIL", but pairing it with P0.1 is
  prudent — the build failure may originate here.

---

## P1 — Instruction sufficiency / agent failure drivers

### P1.1 — Disambiguate case-name format (caused 9/14 failures for one trial)

- `instruction.md` tells agents to read case names from
  `/app/config/sets.txt`, but the file contains entries like
  `alpha:baseline` while every test expects the bare short name
  `alpha`.
- One trial (`uoaPnP9`) used the full strings verbatim and dropped from
  9/14 to 3/14.
- Action: either (a) restate in `instruction.md` that the case name is the
  prefix before the colon (and show an example), or (b) change
  `sets.txt` to contain just the short names. Option (b) is lower risk and
  preserves the difficulty curve elsewhere.

### P1.2 — Decide whether to keep the `ax_ref` hint adjacent to `ax`

- 100% of trials missed the `ax → ax_ref` substitution in
  `src/a0/mod.rs`. The reviewer accepted the dead-code hint as
  sufficient for a hard task, but the 7-trial 9/14 plateau means the
  cliff is currently impassable for both models tested.
- Two ways to keep difficulty HARD while letting the best models break
  through:
  - **Option A (preferred):** add a single sentence to `instruction.md`
    or to a docs file noting that for compressed (packed) requests each
    column receives its own scale/bias, while keeping the buggy `ax()`
    unchanged. The expand-function reference is already partially in
    spec; this just makes the per-column requirement explicit.
  - **Option B:** keep the spec, but ensure `ax_ref` has a docstring
    explicitly stating it is the corrected per-column variant. The bug
    fix then becomes a one-line call-site change rather than a leap.
- Either way, also add a SCALES/BIASES example pair to the docs so the
  "Replace Rust with Go" cohort has a way to derive the constants
  without seeing the test file.

### P1.3 — Discourage Rust-replacement anti-strategy

- 3 of 10 trials wrote a Go binary in place of the Rust stage because they
  doubted `cargo` was on PATH.
- `test_rust_stage_produces_raw` already enforces the Rust path, but the
  signal arrives too late.
- Action: add one sentence to `instruction.md` stating "the Rust binary is
  required; `cargo` is available on PATH in the runtime". `run_local.sh`
  itself can echo a `cargo --version` line before the build to make
  availability discoverable.

---

## P2 — Agent-review convention nits

### P2.1 — `tests/test.sh` should be self-contained

- Covered by P0.2. Adopting the standard uv pattern also removes a future
  source of harness drift.

### P2.2 — Confirm task category and milestone count

- Metadata reports `task_category: debugging`, `number_of_milestones: 0`.
  This matches expectations for a fix-the-bug task; no change needed,
  but verify the `task.toml` `category` matches.

---

## P3 — Items that passed (no change required)

- Quality check: 10/10 axes pass (`behavior_in_task_description`,
  `behavior_in_tests`, `informative_test_structure`,
  `anti_cheating_measures`, `structured_data_schema`,
  `pinned_dependencies`, `typos`, `tests_or_solution_in_image`,
  `hardcoded_solution`, `file_reference_mentioned`).
- Test quality judge: ROBUST → ACCEPT.
- Reward-hack check: clean across all 10 trials.
- Oracle solve: 3/3.
- Difficulty floor: HARD confirmed.
- Static checks: pass.

---

## Tests agents never pass (for engineering focus)

| Test | Root cause (one line) |
| ---- | --------------------- |
| `test_beta_path`, `test_gamma_path`, `test_delta_path`, `test_epsilon_path` | All four pull through `a0/mod.rs::ax()`; cannot pass without the `ax → ax_ref` swap or equivalent per-column scale/bias. |
| `test_rust_stage_produces_raw` | Direct `cargo run` against `/app/target/release/local-infer-sandbox`. Fails for the same reason plus is fatal for any Go-replacement attempt. |

If P1.2 is acted on, every one of these should move off zero.
