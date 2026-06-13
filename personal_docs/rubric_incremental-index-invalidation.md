# Submission rubric — `incremental-index-invalidation`

**Where this goes:** the platform UI at submission time. Per `CLI_installation.md`, the
CLI (`stb submissions create/update`) does **not** carry the rubric — set it up in the
Experts UI before/at submission. This file is the source of truth for that entry; it is a
`personal_docs/` working doc, intentionally **not** placed inside `tasks/<task>/` and
**not** named `rubrics.txt` (both are forbidden by `review-and-submit.mdc`).

**Why a rubric now:** revision 1 had none (the verifier is binary 0/1 reward). The task is
being resubmitted, and submission requires a rubric. **Positive points must sum to 10-40**
(positives-only cap, per the TB3 gate rule); negative penalties are scored separately and
do not count toward that cap.

**Grounding:** items map to the instruction's stated contract and the 12 verifier cases
(`test_t01`…`t12`). The `epoch` item is weighted highest because the documented
agent-failure driver is the `mote_e` (r4) epoch-source bug that broke epoch monotonicity
(`test_t09`) — every failing trial reached 11/12 and missed exactly that. Per
`revision-priorities.md` (P1): **do not soften the epoch-monotonicity requirement.**

## Positive criteria (sum = 30; within 10-40)

| Pts | Criterion | Cases |
|----:|-----------|-------|
| +3 | Regenerates `/app/output/index-report.json` by running `bash /app/scripts/run-matrix.sh` over the live TypeScript files — not a canned or hand-edited report. | t07, t12 |
| +5 | Rename runs: a renamed definition resolves to its **new** location, and after-state observations never point back at old workspace roots. | t01, t08 |
| +5 | Generated-module runs: generated entries carry their **current source** file, and unrelated edits leave untouched definitions marked `reused`. | t02, t04 |
| +5 | Linked-package runs: package entries follow the **active target** through the alias and update when the target changes. | t03, t06 |
| +6 | Each observation's `epoch` is the harness epoch **at query time** and epochs are **nondecreasing** within a case; changed definitions are not falsely marked `reused`. | t09 |
| +4 | Missing symbols report `found=false` with empty `path`/`source`, `line` 0, and `fresh=true`; found symbols use absolute `/app` paths with `line` > 0. | t05, t11 |
| +2 | Re-running the harness on unchanged inputs produces byte-identical output. | t12 |

**Total positives: 30.**

## Penalties (scored separately; not in the 10-40 cap)

| Pts | Condition |
|----:|-----------|
| −5 | Hardcodes report values or emits a precomputed JSON instead of computing from the fixtures. |
| −5 | Deletes, renames, or skips traces/cases to force a pass. |
| −5 | Edits, weakens, or special-cases the verifier tests. |
| −3 | Disables the generated-module, linked-package, or reuse code paths to dodge a failing case. |
| −2 | Introduces randomness, network access, or timing/filesystem-ordering dependence. |

## Notes for the revision record

- Rubric **added** in revision 2 (none existed in revision 1). Documented here per the
  team convention ("if rubrics changed, document it somewhere").
- The rubric grades agent attempts for partial credit in the platform's evaluation; it is
  independent of the verifier's binary `reward.txt` (0/1), which is unchanged.
- No rubric item rewards process over outcome — all criteria are checkable from the emitted
  `index-report.json` (outcome-verified).
