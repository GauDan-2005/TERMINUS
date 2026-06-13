# Validation Log: policy-revocation-shadow

## Attempt 1
- Derived score: 1 FAILs, 0 WARNs
- Evidence: policy-revocation-shadow-attempt-1-evidence.json
- Evidence errors:
  - naming_pass.concentration_math disagrees with computed values: total_tests supplied=12 computed=11; location 'A' ratio supplied=0.16666666666666666 computed=0.181818; location 'B' ratio supplied=0.16666666666666666 computed=0.181818; location 'C' ratio supplied=0.16666666666666666 computed=0.181818; location 'D' ratio supplied=0.16666666666666666 computed=0.181818; location 'E' ratio supplied=0.16666666666666666 computed=0.181818; location 'F' ratio supplied=0.16666666666666666 computed=0.181818
- Blocking evidence failures:
  - naming_pass.concentration_math disagrees with computed values: total_tests supplied=12 computed=11; location 'A' ratio supplied=0.16666666666666666 computed=0.181818; location 'B' ratio supplied=0.16666666666666666 computed=0.181818; location 'C' ratio supplied=0.16666666666666666 computed=0.181818; location 'D' ratio supplied=0.16666666666666666 computed=0.181818; location 'E' ratio supplied=0.16666666666666666 computed=0.181818; location 'F' ratio supplied=0.16666666666666666 computed=0.181818

## Attempt 2
- Derived score: 0 FAILs, 0 WARNs
- Evidence: policy-revocation-shadow-attempt-2-evidence.json

## Revision 1 — feedback addressed (2026-06-04)

Platform reviewer feedback (submission `52218157`, NEEDS_REVISION): "the verifier still never
checks required decision metadata fields like principal, resource, and action. More importantly,
all traces are static and there is no dynamic trace or source level guard, so a canned policy
audit.json path could satisfy the suite ... Add coverage for those required fields and at least
one dynamic trace/generalization check."

Addressed point-by-point:
- **principal / resource / action coverage** → `tests/test_outputs.py::test_t13_flow` asserts all
  three on six rows spanning direct, delegated, and batched decisions (alpha/before, beta/solo,
  gamma/batch, epsilon/check, zeta/a, zeta/b). `test_t14_flow` also asserts them on its row.
- **dynamic trace / generalization** → `test_t14_flow` writes a NEW trace at runtime and runs the
  engine on isolated `/tmp` paths (`cargo run --offline --manifest-path /app/Cargo.toml`), checking
  the same delegated check flips allow→deny once the grantor is revoked. No canned
  `/app/output/policy-audit.json` can satisfy both variants.
- **source-level guard** → `environment/scripts/run-matrix.sh` and `run-one.sh` now `rm -f` the
  target output before regenerating, so a pre-seeded canned report cannot survive a run.
- `construction_manifest.json` flipping-point contract updated (t13→F/`k0`, t14→D/`k4`).
- `tests/test.sh`: pytest moved out of the Dockerfile into a self-contained **offline wheelhouse**
  (Dockerfile `pip download` → `/opt/test-wheels`; test.sh `pip install --no-index`,
  `allow_internet` stays `false`) — clears the agent_review "self-contained test.sh" warning
  gate-compliantly (the networked version it literally suggested is gate-impossible; see
  run_static_checks.py:1441).

**Rubric (regenerated):** the author rubric is pasted into the platform UI, not shipped in the task
dir (the submission zip excludes `rubric.txt`/`rubrics.txt`). For reference, the revision_1 submitted
author rubric (`task_documents[0].submission_document.test_rubrics`) had **+25** positives, and the
platform's auto-generated rubric was **14 checks / max score 24**. Regenerated for this revision →
[`personal_docs/rubrics/policy-revocation-shadow-rubric.md`](../personal_docs/rubrics/policy-revocation-shadow-rubric.md),
**positives = +28** (within the 10–40 cap): added one criterion for decision-metadata coverage
(principal/resource/action + batch_id/delegated_from/stale, per `test_t13`) and reframed the
anti-canned criterion to credit dynamic-input processing (`test_t14`) plus byte-identical determinism
(`test_t12`). Paste these into the platform UI on resubmission.

Verification (2026-06-04, all from command output):
- run_static_checks.py **PASS**; collapse_check.py **0 FAIL / 22 PASS** (1 WARN = GX9, pre-existing —
  identical verdict at git HEAD); check-task.sh **PASS** (checksum written; `task_integrity verify` ✓).
- Oracle 1× mean **1.0** (14/14; offline install confirmed: `Looking in links: /opt/test-wheels`);
  Oracle 10× **10/10** mean **1.000**, 0 exceptions; NOP mean **0.0**.
- validate_submission_zip.py **PASS**; **approve_task.py exit 0** ("Blocking failures: none").
- Submission zip: `Task_Ready_To_Submit/policy-revocation-shadow.zip`.
- Pending (outward-facing): `stb submissions update ./tasks/policy-revocation-shadow -s 52218157-dee7-483f-a7f5-5653ee5e1d01 --time 90`.

## Per-task authoring metrics

- count of run_static_checks.py FAIL exits before first PASS: 1
- count of run_static_checks.py WARN-only exits before approval: 0
- count of collapse_check.py FAIL exits before first PASS: 2
- count of dirty-flag triggers (approve_task.py refused due to checksum mismatch): 0
- wall-clock time from first preflight to first preflight PASS: 162.70s
- wall-clock time from first Step 2b PASS to approve_task.py exit 0: 255.71s
- list of CNI references that fired during the authoring: []
- whether the spec's Initial Draft Commitments matched the final file set (draft_commitments_diff): null

## Per-task authoring metrics

- count of run_static_checks.py FAIL exits before first PASS: 1
- count of run_static_checks.py WARN-only exits before approval: 0
- count of collapse_check.py FAIL exits before first PASS: 2
- count of dirty-flag triggers (approve_task.py refused due to checksum mismatch): 0
- wall-clock time from first preflight to first preflight PASS: 162.70s
- wall-clock time from first Step 2b PASS to approve_task.py exit 0: 609.15s
- list of CNI references that fired during the authoring: []
- whether the spec's Initial Draft Commitments matched the final file set (draft_commitments_diff): null

## Per-task authoring metrics

- count of run_static_checks.py FAIL exits before first PASS: 1
- count of run_static_checks.py WARN-only exits before approval: 3
- count of collapse_check.py FAIL exits before first PASS: 2
- count of dirty-flag triggers (approve_task.py refused due to checksum mismatch): 0
- wall-clock time from first preflight to first preflight PASS: 162.70s
- wall-clock time from first Step 2b PASS to approve_task.py exit 0: 998359.72s
- list of CNI references that fired during the authoring: []
- whether the spec's Initial Draft Commitments matched the final file set (draft_commitments_diff): null
