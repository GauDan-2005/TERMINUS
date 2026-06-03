# sparse-block-preconditioner — Revision 2 priorities

Captured 2026-05-28. Platform state: **NEEDS_REVISION**. Single blocking driver:
**difficulty collapsed to TRIVIAL**. All other automated checks pass. The
revision_1 fixes worked but the instruction edit over-corrected.

## P0 — platform blocker (must fix to clear NEEDS_REVISION)

- **Difficulty = TRIVIAL (requires ≥ MEDIUM).** `terminus-gpt5-2` went 0/5 →
  5/5 and `terminus-claude-opus-4-6` stayed 5/5; all 13 tests 10/10. The task no
  longer discriminates capability.
  - **Cause:** the new final paragraph in `instruction.md` —
    *"Repair the shipped solver for reordered layouts, not only the audit
    scripts. Every row needs `ok` true and matching residual columns; equivalent
    JSON between reruns is necessary but not sufficient."* — telegraphs the exact
    diagnosis that weaker agents previously failed to reach on their own.
  - **Recommended fix:** re-difficulty the task. Walk the instruction back toward
    symptom-only language so the agent must *discover* that the C++ solver (not
    just the script paths) is broken, **without** reintroducing the revision_1
    problems. Concretely:
    - Drop or soften the explicit "repair the shipped solver, not only the audit
      scripts" directive — keep it as a subtle symptom ("residual columns
      disagree with independent measurement", "rows stay dirty"), not an
      instruction.
    - **Keep** the independent Python reference in `tests/test_outputs.py`
      (test-quality fix) — it does not affect difficulty and is what made the
      suite ROBUST.
    - **Keep** the documented JSON schema / field names (quality-axis fix).
  - The note `"AutoEval execution failed / Build status: FAILED"` is the
    difficulty_check verdict, **not** an infra build error — the build ran to
    completion. Do not chase a phantom Docker failure.
  - **Re-validate locally before resubmitting:** run the difficulty/collapse
    calibration loop (`.cursor/rules/difficulty-calibration.mdc`) and confirm a
    weak agent (gpt5-class) does **not** trivially pass before pushing the next
    `stb submissions update`.

## P1 — instruction / difficulty design (the balancing act)

- The tension to manage: revision_1 failed on *instruction sufficiency* (agents
  read symptoms as observations, not bugs) **and** test-quality; revision_2 fixed
  both but went too far. Aim for: instruction sufficient enough that a capable
  agent can succeed and the oracle is unambiguous, yet not so explicit that it
  hands over the diagnosis. The four C++ defects (bsr_n layout indexing, perm_p
  vector reorder, prec_r preconditioner shift, scale_q +1e-4 norm bias) should
  remain something the agent *infers* from failing audit output.

## P2 — agent-review convention nits (non-blocking)

- **pytest in Dockerfile** — move `pytest==8.4.1` and `pytest-json-ctrf==0.3.5`
  from `environment/Dockerfile` (lines 21–23) into `tests/test.sh`. Still present
  in the rev2 submission. Carried over from revision_1; not blocking but worth
  clearing while re-difficulting.
- **(Optional)** adopt the standard uv-based self-contained `test.sh` runner the
  reviewer suggested.
- **Author rubric** (`rubric.txt`) is unchanged and valid (positive sum +27,
  within 10–40). The reviewer's auto-generated rubric (+41) is informational only
  — do not adopt it wholesale; it exceeds the 40 ceiling.

## P3 — passed, no change needed

- test_quality_judge: **ROBUST / ACCEPT** (anti-cheating gap closed).
- Quality check: **all 10 axes pass** (`behavior_in_task_description` fixed).
- codebase_applicability: real C++/CMake codebase.
- long_context_check: skipped (not a long_context task); static checks pass.
- plagiarism / deduplication: clean.
- Canary string removed from `solution/solve.sh`.
- oracle 3/3; nop 0/1 (correctly fails).

## Tests agents never pass

None this round — all 13 tests pass 10/10. (Contrast revision_1, where gpt5 never
passed `test_h7`, `test_i8`, `test_z9`.)
