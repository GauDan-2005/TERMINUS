# Validation Log: allocator-free-list-drift

## Attempt 1
- Derived score: 12 FAILs, 0 WARNs
- Evidence: allocator-free-list-drift-attempt-1-evidence.json
- Evidence errors:
  - Schema validation failed at $.topology_enumeration[0]: 'id' is a required property
  - Schema validation failed at $.topology_enumeration[0]: 'summary' is a required property
  - Schema validation failed at $.topology_enumeration[0]: 'why_no_single_location_suffices' is a required property
  - Schema validation failed at $.topology_enumeration[0]: Additional properties are not allowed ('description', 'topology_id', 'why_not_single_locus' were unexpected)
  - Schema validation failed at $.topology_enumeration[1]: 'id' is a required property
  - Schema validation failed at $.topology_enumeration[1]: 'summary' is a required property
  - Schema validation failed at $.topology_enumeration[1]: 'why_no_single_location_suffices' is a required property
  - Schema validation failed at $.topology_enumeration[1]: Additional properties are not allowed ('description', 'topology_id', 'why_not_single_locus' were unexpected)
  - Schema validation failed at $.topology_enumeration[2]: 'id' is a required property
  - Schema validation failed at $.topology_enumeration[2]: 'summary' is a required property
  - Schema validation failed at $.topology_enumeration[2]: 'why_no_single_location_suffices' is a required property
  - Schema validation failed at $.topology_enumeration[2]: Additional properties are not allowed ('description', 'topology_id', 'why_not_single_locus' were unexpected)
- Blocking evidence failures:
  - Schema validation failed at $.topology_enumeration[0]: 'id' is a required property
  - Schema validation failed at $.topology_enumeration[0]: 'summary' is a required property
  - Schema validation failed at $.topology_enumeration[0]: 'why_no_single_location_suffices' is a required property
  - Schema validation failed at $.topology_enumeration[0]: Additional properties are not allowed ('description', 'topology_id', 'why_not_single_locus' were unexpected)
  - Schema validation failed at $.topology_enumeration[1]: 'id' is a required property
  - Schema validation failed at $.topology_enumeration[1]: 'summary' is a required property
  - Schema validation failed at $.topology_enumeration[1]: 'why_no_single_location_suffices' is a required property
  - Schema validation failed at $.topology_enumeration[1]: Additional properties are not allowed ('description', 'topology_id', 'why_not_single_locus' were unexpected)
  - Schema validation failed at $.topology_enumeration[2]: 'id' is a required property
  - Schema validation failed at $.topology_enumeration[2]: 'summary' is a required property
  - Schema validation failed at $.topology_enumeration[2]: 'why_no_single_location_suffices' is a required property
  - Schema validation failed at $.topology_enumeration[2]: Additional properties are not allowed ('description', 'topology_id', 'why_not_single_locus' were unexpected)

## Attempt 2
- Derived score: 12 FAILs, 0 WARNs
- Evidence: allocator-free-list-drift-attempt-2-evidence.json
- Evidence errors:
  - Schema validation failed at $: 'anti_trivialization_checks' is a required property
  - Schema validation failed at $: 'attack_path' is a required property
  - Schema validation failed at $: 'collapse_audit' is a required property
  - Schema validation failed at $: 'construction_manifest' is a required property
  - Schema validation failed at $: 'discovery_budget' is a required property
  - Schema validation failed at $: 'hardness_axes' is a required property
  - Schema validation failed at $: 'instruction_completeness_test' is a required property
  - Schema validation failed at $: 'instruction_specificity' is a required property
  - Schema validation failed at $: 'naming_pass' is a required property
  - Schema validation failed at $: 'rubric_axes' is a required property
  - Schema validation failed at $: 'smallest_plausible_patch' is a required property
  - Schema validation failed at $: 'topology_enumeration' is a required property
- Blocking evidence failures:
  - Schema validation failed at $: 'anti_trivialization_checks' is a required property
  - Schema validation failed at $: 'attack_path' is a required property
  - Schema validation failed at $: 'collapse_audit' is a required property
  - Schema validation failed at $: 'construction_manifest' is a required property
  - Schema validation failed at $: 'discovery_budget' is a required property
  - Schema validation failed at $: 'hardness_axes' is a required property
  - Schema validation failed at $: 'instruction_completeness_test' is a required property
  - Schema validation failed at $: 'instruction_specificity' is a required property
  - Schema validation failed at $: 'naming_pass' is a required property
  - Schema validation failed at $: 'rubric_axes' is a required property
  - Schema validation failed at $: 'smallest_plausible_patch' is a required property
  - Schema validation failed at $: 'topology_enumeration' is a required property

## Attempt 3
- Derived score: 0 FAILs, 0 WARNs
- Evidence: allocator-free-list-drift-attempt-3-evidence.json

## Per-task authoring metrics

- count of run_static_checks.py FAIL exits before first PASS: 4
- count of run_static_checks.py WARN-only exits before approval: 0
- count of collapse_check.py FAIL exits before first PASS: 15
- count of dirty-flag triggers (approve_task.py refused due to checksum mismatch): 0
- wall-clock time from first preflight to first preflight PASS: 444.30s
- wall-clock time from first Step 2b PASS to approve_task.py exit 0: 1625.59s
- list of CNI references that fired during the authoring: []
- whether the spec's Initial Draft Commitments matched the final file set (draft_commitments_diff): null

## Per-task authoring metrics

- count of run_static_checks.py FAIL exits before first PASS: 4
- count of run_static_checks.py WARN-only exits before approval: 1
- count of collapse_check.py FAIL exits before first PASS: 16
- count of dirty-flag triggers (approve_task.py refused due to checksum mismatch): 0
- wall-clock time from first preflight to first preflight PASS: 444.30s
- wall-clock time from first Step 2b PASS to approve_task.py exit 0: 191605.88s
- list of CNI references that fired during the authoring: []
- whether the spec's Initial Draft Commitments matched the final file set (draft_commitments_diff): null

## Per-task authoring metrics

- count of run_static_checks.py FAIL exits before first PASS: 4
- count of run_static_checks.py WARN-only exits before approval: 1
- count of collapse_check.py FAIL exits before first PASS: 16
- count of dirty-flag triggers (approve_task.py refused due to checksum mismatch): 0
- wall-clock time from first preflight to first preflight PASS: 444.30s
- wall-clock time from first Step 2b PASS to approve_task.py exit 0: 253106.96s
- list of CNI references that fired during the authoring: []
- whether the spec's Initial Draft Commitments matched the final file set (draft_commitments_diff): null

## Per-task authoring metrics

- count of run_static_checks.py FAIL exits before first PASS: 4
- count of run_static_checks.py WARN-only exits before approval: 1
- count of collapse_check.py FAIL exits before first PASS: 17
- count of dirty-flag triggers (approve_task.py refused due to checksum mismatch): 0
- wall-clock time from first preflight to first preflight PASS: 444.30s
- wall-clock time from first Step 2b PASS to approve_task.py exit 0: 301868.26s
- list of CNI references that fired during the authoring: []
- whether the spec's Initial Draft Commitments matched the final file set (draft_commitments_diff): null

## Per-task authoring metrics

- count of run_static_checks.py FAIL exits before first PASS: 4
- count of run_static_checks.py WARN-only exits before approval: 1
- count of collapse_check.py FAIL exits before first PASS: 17
- count of dirty-flag triggers (approve_task.py refused due to checksum mismatch): 0
- wall-clock time from first preflight to first preflight PASS: 444.30s
- wall-clock time from first Step 2b PASS to approve_task.py exit 0: 302472.09s
- list of CNI references that fired during the authoring: []
- whether the spec's Initial Draft Commitments matched the final file set (draft_commitments_diff): null
