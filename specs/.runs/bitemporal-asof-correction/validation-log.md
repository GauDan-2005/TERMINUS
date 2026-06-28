# Validation Log: bitemporal-asof-correction

## Attempt 1
- Derived score: 8 FAILs, 1 WARNs
- Evidence: specs/.runs/bitemporal-asof-correction/attempt-1-evidence.json
- Evidence errors:
  - task_files entries must be under environment/ or steps/: solution/solve.sh
  - hardness_axes is missing required ids: discover, synthesize, diagnose_or_design, navigate_coupling, reason_beyond_training.
  - hardness_axes contains unexpected ids: A1, A2, A3, A4, A5.
  - anti_trivialization_checks is missing required ids: disclosure_collapse, hidden_instance, single_artifact_repair, generalization, prompt_honesty, cheating_vs_difficulty, mechanical_fix_filter, localized_fix, oracle_locality, small_declarative_cluster, grep_collapse, pre_factored_helper, recipe_discount, security_aura_discount, orthogonal_checklist, harness_discount, one_pass_solvability, hard_only_gate, discovery_budget_test, instruction_specificity_test, topology_distribution_test.
  - anti_trivialization_checks contains unexpected ids: C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14, C15, C16, C17, C18, C19, C20, C21.
  - rubric_axes is missing required ids: verifiable, well_specified, solvable, difficult, interesting, outcome_verified.
  - rubric_axes contains unexpected ids: R1, R2, R3, R4, R5, R6.
  - naming_pass.concentration_math disagrees with computed values: location 'align' ratio supplied=0.214 computed=0.214286; location 'reach' ratio supplied=0.286 computed=0.285714; location 'rank' ratio supplied=0.286 computed=0.285714; location 'cleave' ratio supplied=0.286 computed=0.285714; location 'knit' ratio supplied=0.429 computed=0.428571
- Blocking evidence failures:
  - task_files entries must be under environment/ or steps/: solution/solve.sh
  - hardness_axes is missing required ids: discover, synthesize, diagnose_or_design, navigate_coupling, reason_beyond_training.
  - hardness_axes contains unexpected ids: A1, A2, A3, A4, A5.
  - anti_trivialization_checks is missing required ids: disclosure_collapse, hidden_instance, single_artifact_repair, generalization, prompt_honesty, cheating_vs_difficulty, mechanical_fix_filter, localized_fix, oracle_locality, small_declarative_cluster, grep_collapse, pre_factored_helper, recipe_discount, security_aura_discount, orthogonal_checklist, harness_discount, one_pass_solvability, hard_only_gate, discovery_budget_test, instruction_specificity_test, topology_distribution_test.
  - anti_trivialization_checks contains unexpected ids: C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14, C15, C16, C17, C18, C19, C20, C21.
  - rubric_axes is missing required ids: verifiable, well_specified, solvable, difficult, interesting, outcome_verified.
  - rubric_axes contains unexpected ids: R1, R2, R3, R4, R5, R6.
  - naming_pass.concentration_math disagrees with computed values: location 'align' ratio supplied=0.214 computed=0.214286; location 'reach' ratio supplied=0.286 computed=0.285714; location 'rank' ratio supplied=0.286 computed=0.285714; location 'cleave' ratio supplied=0.286 computed=0.285714; location 'knit' ratio supplied=0.429 computed=0.428571

## Attempt 2
- Derived score: 4 FAILs, 1 WARNs
- Evidence: specs/.runs/bitemporal-asof-correction/attempt-2-evidence.json
- Evidence errors:
  - hardness_axes entry 'diagnose_or_design' must use name 'Diagnose or Design/Search', found 'Design/Search/Infer'.
  - anti_trivialization_checks entry 'discovery_budget_test' must use name 'Discovery/design budget test', found 'Discovery/design budget'.
  - anti_trivialization_checks entry 'instruction_specificity_test' must use name 'Instruction specificity test', found 'Instruction specificity'.
  - anti_trivialization_checks entry 'topology_distribution_test' must use name 'Topology distribution test', found 'Topology distribution'.
- Blocking evidence failures:
  - hardness_axes entry 'diagnose_or_design' must use name 'Diagnose or Design/Search', found 'Design/Search/Infer'.
  - anti_trivialization_checks entry 'discovery_budget_test' must use name 'Discovery/design budget test', found 'Discovery/design budget'.
  - anti_trivialization_checks entry 'instruction_specificity_test' must use name 'Instruction specificity test', found 'Instruction specificity'.
  - anti_trivialization_checks entry 'topology_distribution_test' must use name 'Topology distribution test', found 'Topology distribution'.

## Attempt 3
- Derived score: 0 FAILs, 1 WARNs
- Evidence: specs/.runs/bitemporal-asof-correction/attempt-3-evidence.json

## Attempt 4
- Derived score: 0 FAILs, 0 WARNs
- Evidence: specs/.runs/bitemporal-asof-correction/attempt-4-evidence.json

