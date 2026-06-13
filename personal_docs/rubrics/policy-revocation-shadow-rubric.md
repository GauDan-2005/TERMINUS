# policy-revocation-shadow — rubric (regenerated for revision_1)

**Status:** REGENERATED 2026-06-04 for the revision_1 changes — added `test_t13` (principal/
resource/action metadata coverage), `test_t14` (runtime dynamic-trace / generalization), and the
`rm -f` source guard in `run-matrix.sh`/`run-one.sh`. The rubric is pasted into the platform UI and
is **NOT shipped in the task dir** (the submission zip excludes `rubric.txt`/`rubrics.txt`).

**Provenance:** derived from the revision_1 submitted rubric
(`personal_docs/feedback/policy-revocation-shadow/revision_1/metadata/submission_52218157.json`
→ `task_documents[0].submission_document.test_rubrics`, positives = **+25**), updated to credit the
decision-metadata coverage and dynamic-input/anti-canned emphasis the reviewer required.

**Weights:** 8 positive criteria summing to **+28** (within the required 10–40 positives cap);
4 negative criteria (−5, −5, −3, −3 = −16; negatives do not count toward the cap).

## Positive criteria (sum = +28)

```
Agent evaluates grouped replay per subject rather than reusing a shared resource/action slot across peers, so one member's block does not deny a peer in the same batch, +5
Agent makes the verdict cache epoch-aware so a granted or revoked subject cannot reuse a pre-change outcome, +5
Agent invalidates only the blocked subject's cached rows on revoke and bumps that subject's epoch, without flushing unrelated subjects, +3
Agent denies inherited access whenever any subject along the delegation chain is blocked or revoked, not only the requesting subject, +3
Agent preserves reused marking for stable same-epoch subjects across an unrelated subject's block, +3
Agent populates each decision row's principal, resource, and action, sets batch_id only inside groups and delegated_from to the grantor (empty on denial), and flags inherited allows from blocked subjects as stale, +3
Agent fixes the Rust evaluation path so the report is computed from the current trace inputs rather than a canned file, and matrix reruns on unchanged inputs are byte-identical, +5
Agent inspects the matrix output before editing and rebuilds with cargo and re-runs the matrix after changes, +1
```

## Negative criteria (sum = −16)

```
Agent hardcodes or pre-seeds /app/output/policy-audit.json or individual expected rows instead of deriving them from the traces, -5
Agent flushes all cached state globally, breaking reuse for unchanged subjects, to force passing verdicts, -5
Agent edits tests, verifier scripts, trace inputs, or reward files to mask failures instead of fixing the engine, -3
Agent grants allow to a blocked or revoked subject on a delegated path, or disables the delegation/revoke/cache/batch paths to obtain passing verdicts, -3
```

## Changed vs the revision_1 submitted rubric (positives 25 → 28)

| Criterion | rev1 | now | why |
|---|---|---|---|
| Grouped replay per-subject isolation | +5 | +5 | unchanged (core; `test_t06`) |
| Epoch-aware cache keying | +5 | +5 | unchanged — hardest bug, agents missed it (`test_t01`/`t02`/`t08`) |
| Per-subject revoke invalidation | +3 | +3 | unchanged (`test_t02`/`t04`) |
| Delegation-chain block propagation | +3 | +3 | unchanged (`test_t01`/`t03`/`t05`/`t08`) |
| Reuse for stable subjects | +3 | +3 | unchanged (`test_t04`) |
| **Decision metadata (principal/resource/action + batch_id/delegated_from/stale)** | — | **+3** | **NEW — reviewer P0: verifier must check these fields (`test_t13`, `test_t10`/`t11`)** |
| Compute from current inputs (no canned report) + byte-identical reruns | +5 | +5 | reworded from "implements fixes in the Rust path rather than a canned report" to credit dynamic-input processing (`test_t14`) + determinism (`test_t12`) |
| Inspect matrix output + rebuild/re-run | +1 | +1 | unchanged |
| **Positives total** | **25** | **28** | within 10–40 |

Negatives: kept the rev1 set (hardcode output −5, global cache flush −5, edit verifier/tests −3)
and added the core-invariant hack (allow on a delegated path for a blocked subject / disabling the
fix paths, −3). Negatives are scored separately and do not count toward the 10–40 positives cap.
