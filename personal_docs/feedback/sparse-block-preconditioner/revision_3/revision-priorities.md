# sparse-block-preconditioner — Revision 3 priorities

Captured 2026-05-30. Platform state: **NEEDS_REVISION**. Single blocking driver:
**difficulty is still TRIVIAL** (requires ≥ MEDIUM). All other automated checks
pass. This repeats the revision_2 finding — the collapse was not fixed.

## P0 — platform blocker (must fix to clear NEEDS_REVISION)

- **Difficulty = TRIVIAL.** `terminus-claude-opus-4-6` and `terminus-gpt5-2` both
  go 5/5; all 13 tests pass 10/10. The task no longer discriminates capability.
  - **Likely cause (carried from revision_2):** the instruction telegraphs the
    diagnosis (the "repair the shipped solver, not only the audit scripts /
    rerun-equivalence is necessary but not sufficient" language). Weak agents no
    longer have to *discover* that the four C++ modules are broken.
  - **Recommended fix:** re-difficulty toward symptom-only language so the agent
    must infer that the C++ solver (not the scripts) is wrong, **without**
    reintroducing the revision_1 issues:
    - Soften/remove the explicit "repair the solver" directive; keep it as a
      subtle symptom ("residual columns disagree with independent measurement").
    - **Keep** the independent Python reference in `tests/test_outputs.py`
      (test-quality fix; does not affect difficulty).
    - **Keep** the documented JSON schema / field names (quality-axis fix).
  - The four defects to keep inference-only: bsr_n layout indexing, perm_p
    vector reorder, prec_r preconditioner block index, scale_q `+1e-4` norm bias.
  - **Re-validate locally** with the difficulty/collapse loop
    (`.cursor/rules/difficulty-calibration.mdc`) and confirm a gpt5-class agent
    does **not** trivially pass before the next `stb submissions update`.

## P1 — difficulty design balance

- The tension: revision_1 failed on instruction sufficiency + test-quality;
  revision_2/3 fixed both but over-corrected into TRIVIAL. Target: capable agent
  can succeed and the oracle is unambiguous, yet the diagnosis is not handed over.

## P2 — agent-review nits (non-blocking)

- Vendored wheels visible to agent (`/opt/verifier-wheels/`) — accepted offline
  trade-off; no action required unless tightening.
- Optional: add one "multiple modules are affected" sentence to the instruction
  (reviewer suggestion) — but weigh against P0 (do not over-hint).

## P3 — passed, no change needed

- Quality check: **all 10 axes pass**.
- claude_code_reviewer: **PASS — READY TO USE**.
- Solvable; oracle 3/3; nop 0/1 (correctly fails).

## Tests agents never pass

None — all 13 tests pass 10/10 (the symptom of the TRIVIAL collapse).
