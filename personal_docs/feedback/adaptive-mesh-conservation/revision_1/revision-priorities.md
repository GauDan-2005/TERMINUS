# adaptive-mesh-conservation — Revision 1 priorities

Captured 2026-05-30. Platform state: **NEEDS_REVISION**. Multiple drivers, but
the difficulty is correct (HARD) — **do not increase difficulty.** The blockers
are an instruction/spec gap and a test-runner convention issue.

## P0 — platform blockers (must fix to clear NEEDS_REVISION)

1. **Instruction sufficiency FAIL + quality FAIL (`behavior_in_task_description`).**
   `test_i8_tampered_snapshot_rejected` requires the agent to emit a
   `SIGNATURE_MISMATCH` rejection (fingerprint validation in
   `rsm_k/resume.cpp::load_k`), but neither `instruction.md` nor `layout.md`
   states that tamper/fingerprint checking is required.
   - **Fix (preferred):** add the tamper-detection requirement to
     `instruction.md`/`layout.md` — describe that a tampered vault snapshot must
     be rejected and the `persistence_audit.log` reason for it
     (`SIGNATURE_MISMATCH`). This closes the spec gap without changing tests.
   - **Alternative:** drop/relax `test_i8` if tamper detection is out of scope.

2. **Adjacency not discoverable from symptoms.** The failing adjacency tests
   (`c2`, `d3`, `j9`) need `lnk_n/relate.cpp::step_n` to populate
   `child0`/`child_count`, but a conservation-drift symptom gives no signal.
   - **Fix:** add a symptom-level hint that the audit's `adjacency` column /
     relation counts must agree with the independent recomputation (so a capable
     agent investigates `adjacency = 0`), without naming the module.

## P1 — solvability margin (difficulty stays HARD)

- 0% frontier success; `k0`/`l1` (halo band) never pass. After the P0 spec fix,
  confirm a strong agent can plausibly reach the halo bug (`op_b` `d=1`→`d=0`)
  and adjacency bug. Target ≥1 frontier success while keeping nop at 0. Use
  `.cursor/rules/difficulty-calibration.mdc`. Do **not** over-hint into MEDIUM/TRIVIAL.

## P2 — agent-review convention (NEEDS REVISION driver)

- **Move pytest out of the Dockerfile.** Remove `pytest==8.4.1` +
  `pytest-json-ctrf==0.3.5` from `environment/Dockerfile` (lines 21–23) and make
  `tests/test.sh` self-contained with the standard uv preamble
  (curl → uv → venv → `uv pip install pytest…` → `uv run pytest --ctrf …`).
  - Note: with `allow_internet=false`, prefer the offline-wheels pattern (vendor
    wheels at build, `pip install --no-index --find-links`) so the self-contained
    `test.sh` still installs without network. See repo memory on offline wheels.

## P3 — passed, no change needed

- Difficulty: **HARD** (appropriate).
- Anti-cheating: canary (`tb_amr_noembed_8d7a4c2f`) + independent Python
  `simulate()` + tests/solution not in image — all pass.
- structured_data_schema, pinned_dependencies, typos, hardcoded_solution,
  file_reference_mentioned, behavior_in_tests, informative_test_structure — pass.
- No reward hacking; oracle 3/3; nop 0/1.

## Tests agents never pass

`test_k0_canyon_halo_band`, `test_l1_dune_halo_band` — 0/10 (halo offset bug).
Adjacency tests (`c2` 3/10, `d3` 3/10, `j9` 2/10) and `i8` (6/10) are the next
weakest and tie to the P0 spec gaps.
