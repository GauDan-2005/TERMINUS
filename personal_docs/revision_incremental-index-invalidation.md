# Revision record — `incremental-index-invalidation` (rev1 → rev2)

Submission `f0ec5d42-9e1a-4709-9852-acfa502041c5` (NEEDS_REVISION). Work done 2026-06-03.
Reviewer-feedback source: `personal_docs/feedback/incremental-index-invalidation/revision_1/`.

## 1. Are all the feedbacks addressed? — YES

| # | Feedback item (verbatim source) | Status | Resolution |
|---|---|---|---|
| Reviewer (notes.txt L10) | "Capture `PYTEST_RC=$?`, write `reward.txt` from that result, and `exit "$PYTEST_RC"`." | ✅ Done | `tests/test.sh`: capture `PYTEST_RC=$?` after pytest, write reward.txt from it, `exit "$PYTEST_RC"`. Proven: pytest exit 0→script exit 0+reward 1; pytest exit 7→script exit 7+reward 0. |
| P0.1 (revision-priorities) | Fix test.sh exit-status control | ✅ Done | Same as above. |
| P0.2 | Rerun Step 2b dirty-flag chain (`check-task.sh`, oracle 1x, NOP) | ✅ Done | check-task.sh A+B+C PASS; oracle 1x = 1.0; NOP 1x = 0.0. |
| P1.1 | "Preserve the existing behavioral tests. The platform did not ask for additional semantic coverage." | ✅ Honored | `tests/test_outputs.py` untouched (12 tests intact). |
| P1.2 | "do not soften" the `r4/e.rs` epoch-monotonicity requirement (`test_t09`) | ✅ Honored | `test_t09` and the oracle's `mote_e` logic untouched. |
| P2.1 | Wheel-visibility warning is "a consequence of offline … marked READY TO USE" | ✅ No action req. | `environment/wheels/` retained (offline `--no-index` install). Reviewer said negligible risk. |
| P2.2 | "reconcile the platform's `exit "$PYTEST_RC"` request with repo-local canonical test.sh expectations; rerun local static checks" | ✅ Done | Reconciled by teaching `run_static_checks.py` the footer (FEEDBACK > gate, per CLAUDE.md). Static checks re-run: PASS. |
| P3 | Instruction sufficiency / quality 10-10 / agent-review READY / oracle-NOP healthy | ✅ Unchanged | No edits to instruction/solution/metadata; all still pass. |

Side fix required to keep the gate green: the existing `pip install --find-links` line lacked
`--no-index` and failed the offline static check, so `--no-index` was added (behavior-preserving;
the wheelhouse already resolved offline, proven by oracle passes). Not requested by the reviewer
but necessary for a clean re-validation, and it does not contradict any feedback.

Deliberately NOT done: the agent-review *suggestion* to add an instruction sentence naming
`/app/r0…r8` as the logic modules. It is a suggestion (not in P0–P2), revision-priorities P1 says
the platform did not ask for more coverage, and adding causal instruction prose risks pushing the
already-borderline GX6 causal-density WARN toward FAIL. Left as-is.

## 2. Was the rubric changed? — YES (added), and it is documented

Revision 1 had **no rubric** (verifier is binary 0/1). A rubric was authored for rev2 and is
documented at **`personal_docs/rubric_incremental-index-invalidation.md`** (positives sum to **30**,
within the 10-40 positives-only cap; penalties listed separately). It is intentionally outside the
task dir and not named `rubrics.txt` (both forbidden by `review-and-submit.mdc`); it is entered in
the platform UI at submission (the CLI does not carry the rubric). Highest weight (+6) is on the
epoch-monotonicity item — the `mote_e`/r4 bug every failing agent missed.

## 3. Is the task submittable? — YES

`approve_task.py … --skip-verifier-health` → **Approval gate: PASS (exit 0), zero blocking failures.**

| Gate | Result |
|---|---|
| `.step2b-checksum` | PASS |
| static checks | PASS (clean) |
| `validate_submission_zip.py` | PASS |
| manifest verification | PASS |
| source/zip match | PASS |
| quality_check_adjudicate.py | PASS |
| collapse_check.py | WARN (0 FAIL; 3 borderline signals — justified below) |
| **Oracle 10×** | **1.000 (10/10), Pass@10 1.000, 0 exceptions** |
| **NOP** | **0.000** |

### Collapse WARN justifications (0 FAIL, 3 WARN — ACCEPT WITH NOTES)
All three are on the oracle/instruction, were present in revision 1, and the platform accepted the
task's difficulty (MEDIUM, solvable) and quality (10/10) with them present. None introduced by rev2.

- **RC8 Frontier Concentration** — 6 oracle targets in `r0`, 17% subsystem share, avg 18 LOC/target.
  Borderline small-file shape; 17% is far under the manifest's `concentration_cap: 0.5`, and CR2
  (flipping-point) PASSes. No single location flips a majority of tests.
- **GX1 Oracle Comment Leakage** — 1 vocab-anywhere token, **0** explicit BUG/FIXME, **0** in the
  oracle subsystem. No bug-revealing comment sits near an oracle change; borderline lexical hit only.
- **GX6 Causal Connective Density** — 3 connectives / 1.30 per 100w (FAIL is ≥4 and >1.5/100w). The
  instruction is symptoms-only (RC6 PASS; platform rated instruction sufficiency PASS). Left unchanged
  to avoid destabilizing a platform-accepted instruction.

### Remaining (outward-facing — user action)
- Enter the rubric in the platform UI.
- Resubmit: `stb submissions update ./tasks/incremental-index-invalidation -s f0ec5d42-9e1a-4709-9852-acfa502041c5 --time <MINUTES>`.

## Caveat carried forward
The reviewer's `exit "$PYTEST_RC"` footer required updating `run_static_checks.py` to accept it; the
gate's own comment notes upstream AutoEval may expect only the standard `fi`-terminated block. We
followed the reviewer (authoritative, per-task) per FEEDBACK > gate and flagged the divergence.
