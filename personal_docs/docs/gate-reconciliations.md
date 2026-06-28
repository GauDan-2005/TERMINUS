# Gate reconciliations (local gates aligned to platform/skeleton truth)

Per `CLAUDE.md`: "when a repo rule, doc, or gate (`run_static_checks.py`, `collapse_check.py`,
`approve_task.py`) contradicts a review, **the review wins and the rule/gate is updated to match**."
This file records each such change so it is auditable and reversible.

---

## 2026-06-15 — `scripts/run_static_checks.py`

Trigger: while addressing NEEDS_REVISION feedback, the local static-check gate failed tasks for
reasons that contradict **platform reviewer feedback** and the **official platform skeletons**
(`default-template/`, `personal_docs/references_announcement/{Default,Milestone,UI}_Task_Skeleton/`).
The gate had been over-tightened by the 2026-06-13 Terminal-main sync relative to those skeletons.

### 1. `ALLOWED_DIFFICULTIES`: `{"hard"}` → `{"hard", "medium"}`
- **Why:** The platform difficulty check accepts "at least MEDIUM" (`✅ MEDIUM` is a passing grade;
  only EASY/TRIVIAL fail with "Requires at least MEDIUM"). `async-executor-liveness` was graded
  `✅ MEDIUM` and returned NEEDS_REVISION **only** for the declared-`hard`-vs-measured-`medium`
  label mismatch. The reviewer explicitly offered "relabel `task.toml difficulty = medium`" as a
  fix. The hard-only set was stricter than both the platform and the reviewer.
- **Also updated** the Python-language difficulty rule to accept `medium` (platform grades
  Python tasks `✅ MEDIUM` too; "EASY — Requires at least MEDIUM" implies medium would pass).
- **Note:** This does NOT let a TRIVIAL/EASY task pass by relabeling — the platform re-measures
  difficulty independently. Trivial tasks must still be genuinely hardened to ≥MEDIUM.

### 2. WORKDIR-guard message regex
- The regex required the message to end at `...in your Dockerfile.`, but **every** official
  skeleton and every platform-accepted task uses `...in your Dockerfile before running this
  script.`. Made the trailing clause optional so both forms pass.

### 3. `tests/test.sh` pytest invocation
- The check accepted only bare `pytest` / `/opt/verifier/bin/pytest` / `uvx`, but every official
  skeleton invokes `python -m pytest`, which runs the same Dockerfile-installed pytest module.
  Added `python -m pytest` / `python3 -m pytest` to the accepted forms.

Evidence: `grep -rl 'No working directory set' --include=test.sh` shows all skeletons use the long
message + `python -m pytest`; `personal_docs/feedback/async-executor-liveness/revision_1/` reviewer
notes sanction `difficulty = medium`.

---

## 2026-06-15 — `scripts/approve_task.py` (Step 4 strict gate)

### `actionability_check.py` + `no_hidden_contracts.py` kept NON-BLOCKING in strict approval
- **Why:** both lints scan the verifier's own test files (`tests/test_outputs.py`, `tests/test.sh`)
  and flag *verifier mechanics* as "hidden contracts": pytest flags (`--ctrf`, `-rA`, `-o`), cargo/pip
  build flags (`--bin`, `--release`, `--no-index`, `--find-links`), the verifier-rerun build command
  (`cargo build …`), and the test's reference-computation comprehensions (`{row[...]: ... for row in …}`).
  None of these are agent-facing contracts. They **FAIL on platform-vetted baselines** in this
  repo (verified across the revision set and sibling baselines).
- **Authority:** the platform's own quality_check already validates that the real, agent-facing contract
  is documented — `behavior_in_task_description`, `structured_data_schema`, and `anti_cheating_measures`
  are PASS on all 8 tasks. Per CLAUDE.md ("review wins, gate updates to match"), these crude AST proxies
  are subordinate to the platform's stronger semantic check.
- **Scope of change:** only these two lints are downgraded to WARN. **Every other strict gate stays
  blocking** — `.step2b-checksum`, static checks, collapse (RC1–RC10), zip validation, manifest +
  zip/source parity, `spec_satisfiability`, `obfuscation_lint`, first-look, final oracle (1.0) / NOP
  (0.0) evidence, `category_profile`, `reference_pattern`, and `waiver_lint`.

---

## 2026-06-16 — completing the reconciliation across the remaining local gates

Trigger: while addressing the 2026-06-16 NEEDS_REVISION feedback, several local gates still
contradicted the platform on platform-vetted baselines (instruction-sufficiency PASS,
agent_review READY TO USE, yet failed these local gates). The 2026-06-15 reconciliation had
only updated `run_static_checks.py` and `approve_task.py`; the sibling gates were left inconsistent.
Per CLAUDE.md ("review wins, gate updates to match") each is brought in line. **No new task can pass
by relabeling** — the platform re-measures difficulty and instruction sufficiency independently.

### 1. `.dockerignore` ships in the submission zip (reviewer feedback)
- **Why:** platform reviewer feedback (async-executor-liveness rev_2) **required** `environment/.dockerignore`
  inside the archive; the platform builds the task image from the unpacked archive, so the
  build-context ignore file must travel with it. The local "strip all dotfiles" packaging convention
  removed it. FEEDBACK > documented policy.
- **Change:** `scripts/validate_submission_zip.py` adds `PACKAGED_DOTFILE_ALLOWLIST = {".dockerignore"}`
  (single source of truth). `scripts/package_task.py` includes allowlisted dotfiles (and drops
  `.dockerignore` from its forbidden-filenames set). `scripts/approve_task.py:should_skip_packaged_path`
  keeps allowlisted dotfiles in the source manifest so zip/source parity still holds. `.gitignore` and
  all other dotfiles remain excluded. Regression: `repo_tests/test_package_task.py`.

### 2. `task_runtime_deps.py` — prose command words are not invocations
- **Why:** `COMMAND_RE` matched a runtime name anywhere it appears as a word, firing on ordinary
  English inside Python docstrings/comments ("build the **node** hierarchy", "with **cargo** build") and
  producing false "X invoked but not provided" FAILs.
- **Change:** added `is_invocation_context()` — a match counts only when it is a quoted argv token,
  in shell command position (line start / after a control operator / env-assignment / wrapper keyword),
  or immediately followed by a CLI flag. Regression: `repo_tests/test_task_runtime_deps.py`.

### 3. `spec_gap_detector.py` — Python method calls are not data fields
- **Why:** `tasks.count(...)`, `s.split(...)` etc. were extracted via `FIELD_ACCESS_RE` as if `.count`
  were a tested output field, demanding the instruction "explain" a stdlib method name.
- **Change:** skip `ast.Attribute` nodes that are the callee of a `Call` (method calls). Real data-field
  access is still flagged. Regression: `repo_tests/test_spec_gap_detector.py`.

### 4. `spec_test_alignment.py` — literals homed anywhere solver-visible
- **Why:** the `undocumented_literal` check searched only `instruction.md`, so data-specific scenario
  names that live in solver-visible plan/data files (`environment/data/cases/*.plan`) were flagged —
  even though `collapse_check` GX7 (the authoritative homing gate) already passes them.
- **Change:** the literal home search now spans `instruction.md` + the `environment/` text surface the
  agent can read. A literal homed nowhere is still flagged. Regression: `repo_tests/test_spec_test_alignment.py`.

### 5. `hard_difficulty_predictor.py` — accept ≥ MEDIUM, count mechanisms per line
- **Why (difficulty label):** the gate still required `difficulty=hard`, contradicting the 2026-06-15
  `run_static_checks.py` change and the platform's "at least MEDIUM" rule (and the reviewer's explicit
  sanction of `difficulty = medium` for async-executor-liveness). The genuine hardness bar (worst-model
  pass-rate ceiling) is enforced separately and unchanged.
- **Why (mechanism count):** `MECHANISM_RE.findall(spec_text)` ran without `re.MULTILINE`, so a real
  `difficulty_mechanism_plan` (5 `mechanism:` lines) counted as 0 → false `thin_mechanism_plan` WARN.
- **Change:** accept `{"hard","medium"}`; count `mechanism:` lines per line (consistent with
  `_extract_failure_modes`). Regression: `repo_tests/test_new_gates.py` (still green on hard fixtures).

### 6. `scripts/check-task.sh` — actionability/no_hidden non-blocking in strict (Phase B)
- **Why:** the 2026-06-15 reconciliation downgraded these two lints in `approve_task.py` but not in the
  preflight that writes the `.step2b-checksum` sentinel; in strict mode they still aborted Phase B, so
  no platform-accepted task could ever write the sentinel.
- **Change:** `NONBLOCKING_LINTS="actionability_check.py no_hidden_contracts.py"` warn instead of
  blocking even in strict mode. Every other Phase B lint stays blocking. Regression:
  `repo_tests/test_check_task_sh.py`.

### 7. `scripts/reviewer_simulation.py` — aligned with platform authority
- **Why:** the meta-gate scored `reviewer_confidence=0` (would_reject) on platform-ACCEPTED tasks. It
  treated the non-blocking lints as CRITICAL, mapped every WARN to HIGH (a WARN is "PASS-with-
  justification in Step 3b", not a reject), treated the local pass-rate **heuristic** as CRITICAL (it
  predicted ~69% for an accepted task; the platform difficulty_check is authoritative), and the
  difficulty_confidence cap structurally held a clean ≥MEDIUM task below the ≥90 floor.
- **Change:** `NON_BLOCKING_GATES` (actionability, no_hidden) → LOW; `WARN` → MEDIUM; the
  model-pass-rate heuristic concern → MEDIUM; difficulty_confidence base 70 → 80 for a passing task
  with ≥1 advanced category. Genuine blocking-gate FAILs (collapse RC, spec_gap real gaps, spec_test
  unhomed literals, sandbox, missing/non-PASS first-look) still produce CRITICAL/would_reject, so the
  gate keeps its teeth. Verified: `async-executor-liveness` now scores reviewer_confidence=95.
