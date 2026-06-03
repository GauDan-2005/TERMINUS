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
