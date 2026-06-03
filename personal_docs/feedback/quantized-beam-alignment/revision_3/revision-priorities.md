# quantized-beam-alignment — Revision 3 priorities

Captured 2026-05-30. Platform state: **NEEDS_REVISION**. Single blocking driver:
**0% frontier-agent success** → the difficulty gate cannot confirm the task is
solvable-but-not-impossible (HARD verdict, but "not clear if solvable or super
hard"). This is the *too-hard* failure mode (contrast sparse, which is trivial).

## P0 — platform blocker (must fix to clear NEEDS_REVISION)

- **No non-oracle agent passes (opus 0/5, gpt5 0/5); 5 tests 0/10.** The oracle
  (author solution) passes 3/3, so the task *is* technically solvable, but the
  gate wants at least a plausible path for a frontier agent.
  - **Root cause:** the core Rust bugs (`ax`/`bx`/`cx` in `a0`/`b1`/`c2`) are too
    obscure. Every agent stops at 9/14 after fixing PATH + the Go stage, then
    mistakes structurally-consistent-but-numerically-wrong output for success.
  - **Recommended fix — nudge solvability without making it trivial:**
    - Make the `ax_ref()` reference function more discoverable (e.g., a comment
      tying it to `ax()`, or a doc note that the packed path has a known-good
      reference), so a capable agent can cross-check `produced` values.
    - Or add a *symptom-level* hint that the numeric token values (not just the
      raw/report agreement) must match an independent reference — without naming
      the modules.
    - Re-run the difficulty loop and target ≥1 frontier success across runs
      while keeping nop at 0 and avoiding a TRIVIAL slide.

## P1 — difficulty calibration

- Aim for HARD-with-a-path: oracle passes, ≥1 frontier agent passes occasionally,
  weak agents plateau. Currently the ceiling is a hard 9/14 with zero variance —
  too flat. See `.cursor/rules/difficulty-calibration.mdc`.

## P2 — agent-review nits (non-blocking)

- Add `data/epsilon.txt` and `data/zeta.txt` (or remove unused `data/` files) so
  the 6-case `config/sets.txt` matches the 4 present data files. Cosmetic; case
  data is hardcoded in `main.rs`.

## P3 — passed, no change needed

- Quality check: **all 10 axes pass**.
- Instruction sufficiency: **PASS** (codebase + `ax_ref()` + tests define the spec).
- claude_code_reviewer: **PASS — READY TO USE**.
- HARD difficulty; oracle 3/3; nop 0/1; no reward hacking.

## Tests agents never pass

`test_beta_path`, `test_gamma_path`, `test_delta_path`, `test_epsilon_path`,
`test_rust_stage_produces_raw` — all 0/10. These gate on the unfixed Rust
computation bugs.
