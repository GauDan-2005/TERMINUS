### Decision
GO - Attempt 1.

- First optimization/search task in the bank: the solver must emit a cgroup-v2 limit assignment over a delegated service tree that satisfies five interacting hard-constraint families and reaches a fairness optimum the verifier computes independently. All 16 prior tasks are repairs; this is a constrained search.
- Hardness survives full disclosure: every constraint and the objective are stated, yet the cgroup-v2 effective-protection down-scaling, the cpu.weight path-product, and the tree max-min `low` allocation must be coordinated across every node. Naive per-leaf or even-split assignments violate a distant constraint or fall under the optimum.
- Verifier is an independent Python reimplementation of the kernel semantics, runs on verify-time-generated trees (no hardcoding), and accepts any assignment that is feasible and within tolerance of the optimum (outcome-verified, many solutions pass).

### Metadata

- version: 2
- Task name: cgroup-budget-solver
- Title: Cgroup Budget Solver
- Category: system-administration
- Task shape: optimization_under_constraints
- Languages: ["Go", "shell"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["cgroups", "systemd", "resource-control", "optimization", "go"]
- Milestones: 0

## Authoring Brief
This file is the drafting source for the live task under `tasks/cgroup-budget-solver/`.

### Public contract
Implement the resource-budget solver under `/app` (also reachable through the `/app/environment` alias). `/app/bin/cgsolve <scenario-in.json> <assignment-out.json>` reads one delegated cgroup-v2 service tree and writes one limit assignment; `bash /app/scripts/solve-one.sh <in> <out>` builds then runs it; `bash /app/scripts/run-suite.sh` runs the solver over every bundled tree under `/app/data/scenarios/` and writes `/app/output/plan-report.json`. The shipped solver compiles but emits an unusable assignment; the work is to make it produce assignments the kernel-v2 protection model accepts.

A scenario is a rooted tree. The root carries the machine memory capacity and the per-device IO capacities. Internal nodes are delegated slices, each with a delegated memory budget. Leaves are services, each with: a guaranteed memory floor, a working-set size, a burst-headroom requirement, a target global CPU share, and a per-device IO floor. The assignment sets, for every node, `mem_min`, `mem_low`, `mem_high`, `mem_max`, `cpu_weight`, and `io_max`.

The assignment must satisfy, on every bundled tree and on freshly generated trees: (1) each leaf's effective memory.min — computed under cgroup-v2 proportional down-scaling from the root through every ancestor — is at least its floor; (2) `mem_max` is non-increasing from root to leaf, never exceeds the machine capacity, and each leaf's `mem_max` is at least its working set, with `mem_min <= mem_high < mem_max`; (3) each leaf's `mem_max - mem_high` is at least its burst headroom; (4) each leaf's path-product CPU share (the product of `cpu_weight` divided by sibling-weight-sum along its root path) is within tolerance of its target share, with every `cpu_weight` an integer in [1, 10000]; (5) on every device, the leaf `io_max` values are each at least the floor and sum to at most the device capacity. Subject to those, the assignment maximizes the worst-off leaf's `mem_low` satisfaction — the minimum over leaves of effective-`mem_low` divided by the leaf's reclaimable desire — where each node's children may be assigned `mem_low` summing to at most that node's reclaimable budget (its delegated budget minus the `mem_min` it reserves). The report records, per scenario, the emitted assignment, the effective protections, the worst-leaf ratio achieved, and whether all hard constraints held.

The cgroup-v2 effective-protection semantics (down-scaling of `memory.min`/`memory.low` when a node's children oversubscribe the protection passed down) are documented in `/app/docs` and implemented in a readable reference evaluator under `/app/internal`; the solver is free to call that evaluator to self-check. Static or hand-written assignment files are insufficient: the verifier regenerates assignments by running the solver, including on trees not present under `/app/data`.

### Failure topology
The shipped solver returns an all-zero assignment: it parses the scenario and emits one entry per node with every field zero, which compiles and round-trips through the report but fails every hard constraint (a zero `mem_max` is below any working set, a zero effective floor is below any guarantee, a unit-less weight misses every share target). The five constraint families are genuinely coupled. Memory floors cannot be satisfied per-leaf: a leaf's effective `mem_min` is bounded by every ancestor's effective `mem_min` and is down-scaled proportionally whenever siblings oversubscribe, so floors must be reserved at every level without oversubscribing any delegated budget. The `mem_low` objective shares each node's *reclaimable* budget, which is whatever that node did not reserve for `mem_min`, so the fairness allocation is entangled with the floor reservation and with the per-node delegated caps. The CPU shares are path-products, so a leaf's global share depends on weights chosen at every level, and a per-leaf weight set to the global target ignores sibling normalization. The IO and max-hierarchy constraints further restrict the feasible region the fairness step optimizes over.

The discriminating insight is that the worst-leaf `mem_low` ratio is capped by the most-constrained subtree, not by any single leaf: the optimum is the largest ratio such that every node can supply that ratio times the total reclaimable desire of its subtree out of its reclaimable budget. A solver that splits each node's reclaimable budget evenly among children, or that gives each leaf its full desire, either falls below that optimum or oversubscribes a node and becomes infeasible. The verifier computes the optimum independently and accepts any feasible assignment within tolerance of it.

### Environment shape
One digest-pinned Go image with the Go toolchain, pytest, tmux, and asciinema. The environment contains a shared types package; a readable reference evaluator that computes effective protections, checks the hard constraints, scores the worst-leaf ratio, and computes the independent optimum; an entrypoint command; five opaque solver-stage packages that the shipped build leaves as pass-through stubs; two or three sibling helper packages that do diagnostic/formatting work off the solver path; bundled scenario trees under `data/`; shell runners; and docs describing the cgroup-v2 protection model and the run interface. The verifier is offline and invokes the shipped binary.

### Required artifacts
Step 2b maintains `instruction.md`, `task.toml`, `construction_manifest.json`, `output_contract.toml`, `environment/Dockerfile`, environment source/scenarios/docs/scripts, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. The task is single-step, single-container, non-UI, not long-context, `version = "2.0"`, and `[environment].allow_internet = false`.

### task_shape

- type: optimization_under_constraints
- instruction_framing: constraint-complete
- hardness_source: constrained optimization
- collapse_risk: medium; mitigated by an independent verifier evaluator, verify-time-generated trees that defeat hardcoding, a non-textbook protection-redistribution model, and a fix frontier split across five solver stages.

### platform_files

- path: task.toml
- role: Edition 2 metadata and runtime limits for a hard system-administration optimization task.
- path: instruction.md
- role: solver-facing public contract for the run interface, scenario/assignment schema, the five hard constraints, and the fairness objective.
- path: tests/test_outputs.py
- role: independent Python verifier that reimplements the cgroup-v2 effective-protection model, checks all constraints, scores the worst-leaf ratio, computes the optimum, and runs the solver on bundled and generated trees.
- path: tests/test.sh
- role: canonical verifier entrypoint that runs pytest and writes reward.
- path: solution/solve.sh
- role: oracle that writes the five solver-stage bodies and rebuilds.
- path: environment/Dockerfile
- role: digest-pinned offline Go runtime image with pytest, tmux, and asciinema.
- path: construction_manifest.json
- role: authoring metadata for fix frontier, base image, decoys, and the flipping-point contract.
- path: output_contract.toml
- role: local authoring metadata for the generated report output and schema homes.

### task_files

- path: environment/
- role: stub Go solver, reference evaluator, shared types, scenario trees, docs, and shell runners visible to the solver.
- path: solution/solve.sh
- role: oracle solver implementation used only by Harbor validation.
- path: construction_manifest.json
- role: source-of-truth metadata for collapse and approval gates.

### fix_frontier

- count: five solver-stage functions (one per constraint/objective family) plus their private helpers.
- distribution: memory-floor reservation, max-hierarchy and headroom limits, cpu path-product weights, io device allocation, and reclaimable max-min `mem_low` fairness, each in a separate opaque package.
- naming_policy: opaque short package directories (`qa` through `qe`) and an opaque stage function name reused per package; shared domain types live in a non-fix package.
- forbidden_stems: cgroup, memory, weight, protection, guarantee, headroom, limit, budget, delegation, device, bandwidth, share, fairness, objective, node, leaf, slice, service, scenario, assignment, solver, suite, report, plan, threshold, tier, reclaimable, working-set, root, parent, child, sibling.
- helpers_policy: sibling helper packages with diagnostic/formatting bodies that rhyme with stage functions but never touch the assignment.
- symbol_thin_preferred: yes; each solver stage is one function in its own package, chained so no file references more than two fix-path symbols.

### contract_surface

- boolean_fields_max: one (`feasible`) per report row, justified because the per-row metadata (effective protections, ratios, per-constraint margins) carries the real evidence and tests derive verdicts from numeric records, not the flag.
- direct_boolean_assertions_max: feasibility is checked alongside recomputed effective protections, ratio-vs-optimum comparisons, weight path-products, and device sums.
- preferred_assertion_styles: recompute effective protections with an independent evaluator, recompute the optimum, compare achieved ratio within tolerance, verify per-constraint numeric margins, run the binary on freshly generated trees.
- forbidden_assertion_styles: golden assignment files, static report writes, hardcoded per-scenario answer values, schema/existence-only checks, scenario->field->expected boolean tables.

### category_profile

- challenge_family: constrained resource-budget allocation over a delegated cgroup hierarchy.
- profile_name: config_policy_precedence
- allowed_instruction_disclosures: the run interface, the scenario and assignment JSON schema, the five hard constraints, the cgroup-v2 effective-protection down-scaling rule, the path-product CPU rule, the reclaimable-budget definition, the fairness objective, and the within-tolerance acceptance rule.
- forbidden_instruction_leaks: the solver-stage package/function identifiers, the constructive allocation algorithm, the optimum formula expressed as a recipe, per-scenario expected numbers, and any statement of which stage controls which test.
- category_specific_hardness_bar: the effective resource policy derives across the whole tree (delegated budgets, ancestor protection propagation, sibling weight normalization, device pools); no single node or leaf assignment is sufficient and local choices break distant feasibility and the objective.
- category_specific_verifier_risks: relying on the environment's Go evaluator (tamperable), accepting overcommitting assignments, brittle exact-value thresholds, or scenarios that allow a per-leaf shortcut.
- coverage_role: adds the first Go optimization/search task and the first constrained-allocation challenge to a bank that is otherwise all repairs.

### difficulty_mechanism_plan

- mechanisms: buried_local_constraints, stateful_multi_step_dependencies, deceptive_but_valid_local_evidence, cross_file_cross_format_invariants, false_green_intermediate_states.
- mechanism: buried_local_constraints
  placement: the effective-protection down-scaling and reclaimable-budget definitions live in the reference evaluator and docs, not as a recipe in the instruction.
  why_model_misses_it: a solver can satisfy a leaf's configured floor while its effective floor is down-scaled to zero by an unfunded ancestor.
  fairness_guardrail: the down-scaling rule is documented and implemented in a readable evaluator the solver may call.
- mechanism: stateful_multi_step_dependencies
  placement: the `mem_low` fairness budget at each node depends on how much `mem_min` that node reserved, which depends on subtree floors.
  why_model_misses_it: optimizing fairness independently of the floor reservation overcommits a node or leaves budget unused, missing the optimum.
  fairness_guardrail: the reclaimable-budget definition (delegated minus reserved min) is stated in the instruction and docs.
- mechanism: deceptive_but_valid_local_evidence
  placement: per-leaf weights set to the global target look locally correct but miss the path-product after sibling normalization.
  why_model_misses_it: a locally plausible weight assignment passes a single-node sanity check yet fails the global share tolerance.
  fairness_guardrail: the path-product rule and the [1,10000] integer range are stated in the instruction.
- mechanism: cross_file_cross_format_invariants
  placement: scenario JSON in, assignment JSON out, report JSON, the Go evaluator, and the Python verifier must all agree on the same numeric semantics.
  why_model_misses_it: a partial implementation that only handles one resource emits a report that round-trips but fails recomputation under the independent evaluator.
  fairness_guardrail: every schema field, formula, and tolerance is visible in the instruction or docs.
- mechanism: false_green_intermediate_states
  placement: an assignment that meets the four feasibility families but splits reclaimable budget evenly produces a feasible-looking report whose worst-leaf ratio is below the optimum.
  why_model_misses_it: feasibility alone reads as success; the objective shortfall is only caught by comparing to the independently computed optimum.
  fairness_guardrail: the objective and the within-tolerance acceptance against the optimum are stated in the instruction.
- adversarial_layers_count: five.
- fairness_guardrails: every externally checked interface, schema field, constraint, formula, tolerance, and the objective is visible in instruction.md or normal environment docs; only the solver-stage locations and the constructive algorithm are withheld.

### calibration_plan

- oracle_runs: 10
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: a systems engineer can solve by reading the cgroup-v2 model docs, reserving floors bottom-up, setting decreasing max with headroom, solving weights level by level, allocating io within device pools, and water-filling reclaimable budget to the binding subtree.
- shortcut_audit: tests regenerate assignments by running the binary, generate fresh trees at verify time, reject static report writes, reject reliance on the environment evaluator by recomputing in Python, and reject overcommitting assignments.
- ablation_plan: stub each of the five solver stages independently and confirm at least one verifier test fails for that stage only.
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=stronger target agent; aligns with Part E Hard/Medium/Easy thresholds on worst/best model accuracy.

### verifier_scoring_plan

- metrics: functional_correctness, hidden_invariants, state_hygiene, interface_correctness, deliverable_completeness.
- functional_correctness: effective floors, max hierarchy, headroom, path-product shares, and device sums hold on bundled and generated trees.
- hidden_invariants: the worst-leaf `mem_low` ratio reaches the independently computed optimum within tolerance and no node oversubscribes its reclaimable budget.
- state_hygiene: re-running the solver on the same tree yields an assignment with identical feasibility and objective, and the suite leaves the binary and report in place.
- interface_correctness: `cgsolve`, `solve-one.sh`, and `run-suite.sh` read the documented inputs and write the documented assignment/report shape.
- deliverable_completeness: every node appears in the assignment with all six fields and every bundled scenario appears in the report.
- overall_threshold: binary reward requires all pytest assertions to pass.
- reward_output: /logs/verifier/reward.txt.
- binary_threshold_rule: reward is 1 only on pytest exit 0; otherwise reward is 0.

### subtype_milestone_plan

- subcategories: none.
- milestone_count: 0.
- sequential_dependency: not applicable; standard single-step task.
- local_only_data: all source, scenarios, scripts, and docs are bundled under `/app`.
- sidecar_or_protocol_notes: `run-suite.sh` regenerates one JSON report from bundled trees; verifier tests invoke `cgsolve` on temporary generated trees.

### satisfiability_risk

- rc2_planned_name_risk: low; solver-stage packages are opaque (`qa`-`qe`) and domain types live in a non-fix package.
- gx9_contract_risk: low; the instruction states constraints and the objective but no per-scenario expected values; expectations are recomputed by the verifier.
- cr1_symbol_frontier_risk: low; the manifest fixes the five stage symbols and the oracle uses them verbatim.
- hidden_contract_risk: low; every tested interface, schema field, formula, and tolerance is in instruction.md or docs.

### actionability_plan

- verifier_command_visible: instruction.md names `/app/bin/cgsolve <in> <out>`, `bash /app/scripts/solve-one.sh <in> <out>`, `bash /app/scripts/run-suite.sh`, and the pytest verifier command with `--ctrf`.
- source_fix_intent_visible: instruction.md says the solver sources live under `/app/internal` and `/app/cmd` (also via `/app/environment`) and that static assignment writes are insufficient.
- generated_output_rule_visible: instruction.md identifies `/app/output/plan-report.json` and per-call assignment outputs and that trees not under `/app/data` are also solved.
- exact_formula_home: instruction.md and `/app/docs` state the down-scaling rule, path-product rule, reclaimable-budget definition, objective, and tolerance.
- schema_home: instruction.md names every scenario, assignment, and report field; docs carry the worked semantics.

### waiver_plan

- waivers_expected: false.
- waiver_rationale: no waiver is planned; any checker warning should be resolved or documented before packaging.

### reference_pattern

- justification_if_none: original synthetic task built from the cgroup-v2 memory-protection model and systemd resource-control delegation; not derived from a website, prior public task, or template reskin. The reference library currently has no promoted entries.

### realism_source

- source_type: real_system
- evidence_basis: the Linux cgroup-v2 memory controller protection model (`memory.min`/`memory.low` proportional distribution and down-scaling, `memory.high`/`memory.max`), `cpu.weight` relative sibling distribution, `io.max`, and systemd delegated-slice budgeting.
- upstream_or_synthetic_rationale: the protection-redistribution and delegation semantics are taken from the kernel cgroup-v2 documentation and systemd resource control; the trees and the fairness objective are synthetic to keep all data local and deterministic.
- minimization_preserves: ancestor protection propagation with proportional down-scaling, no-overcommit of delegated budgets, max-hierarchy inheritance, relative cpu weights as path-products, device IO pools, and reclaimable best-effort distribution.
- synthetic_exception_review: not a synthetic exception; the model and constraints are drawn from a real subsystem, only the instances and objective threshold are generated.

### Test plan
- `test_t01`: every bundled tree solved through `run-suite.sh` is feasible on all five families and reaches the optimum within tolerance. Multiple approaches: yes. Chain-dependent: yes (whole solver).
- `test_t02`: every leaf effective `mem_min` (recomputed under down-scaling) is at least its floor on bundled trees. Multiple approaches: yes. Chain-dependent: no.
- `test_t03`: on a generated tree where leaf-only or unfunded-ancestor floors would down-scale to zero, effective floors still hold. Multiple approaches: yes. Chain-dependent: no.
- `test_t04`: `mem_max` is non-increasing root-to-leaf, within machine capacity, at least the working set, with `mem_min <= mem_high < mem_max`, on bundled trees. Multiple approaches: yes. Chain-dependent: no.
- `test_t05`: every leaf `mem_max - mem_high` is at least its burst headroom on bundled and generated trees. Multiple approaches: yes. Chain-dependent: no.
- `test_t06`: every leaf path-product CPU share is within tolerance of its target on bundled trees, weights integer in [1,10000]. Multiple approaches: yes. Chain-dependent: no.
- `test_t07`: on a generated multi-level tree, path-product shares hold and sibling weights normalize. Multiple approaches: yes. Chain-dependent: no.
- `test_t08`: per-device leaf `io_max` are each at least the floor and sum to at most capacity on bundled trees. Multiple approaches: yes. Chain-dependent: no.
- `test_t09`: on a generated multi-device tree, io allocation is feasible. Multiple approaches: yes. Chain-dependent: no.
- `test_t10`: worst-leaf `mem_low` ratio reaches the independently computed optimum within tolerance on bundled trees. Multiple approaches: yes. Chain-dependent: no.
- `test_t11`: on a generated tree with a binding subtree, the objective reaches the optimum (an even split falls short). Multiple approaches: yes. Chain-dependent: no.
- `test_t12`: no node's children `mem_low` sum exceeds that node's reclaimable budget. Multiple approaches: yes. Chain-dependent: no.
- `test_t13`: a seeded batch of freshly generated trees are each fully feasible and reach the optimum within tolerance (generalization). Multiple approaches: yes. Chain-dependent: yes (whole solver).

### Drafting guardrails
The instruction should read like an engineering brief for a solver, not a recipe. State the interface, schema, the five constraints, the down-scaling and path-product rules, the reclaimable-budget definition, the objective, and the tolerance. Do not name the solver-stage packages/functions, the constructive algorithm, the optimum as a step list, per-scenario numbers, or which stage controls which test. Tests recompute every expectation from the scenario with an independent evaluator; no golden assignment or report is shipped.

### Triviality Ledger
- Per-leaf floor trap: setting only leaf `mem_min` leaves effective floors down-scaled by unfunded ancestors; blocked by `test_t02`/`test_t03` recomputing effective protection.
- Full-desire `mem_low` trap: giving each leaf its full reclaimable desire overcommits a node; blocked by `test_t12` and by infeasibility under the independent evaluator.
- Even-split fairness trap: splitting reclaimable budget evenly misses the binding-subtree optimum; blocked by `test_t10`/`test_t11` comparing to the independently computed optimum.
- Per-leaf weight trap: setting each `cpu_weight` to the global target ignores sibling normalization; blocked by `test_t06`/`test_t07` checking path-products.
- Hardcoding trap: memorizing bundled-tree answers fails on verify-time-generated trees; blocked by `test_t03`/`test_t07`/`test_t09`/`test_t11`/`test_t13`.
- Tamper trap: rewriting the environment Go evaluator does not help; blocked because the verifier recomputes everything in Python.

### Per-gate Pitfall Inventory
- RC1: oracle writes five substantive solver-stage bodies (adds logic), it does not delete or revert.
- RC2: solver-stage packages/files are opaque (`qa`-`qe`/`a.go`); no broken/golden/expected tokens on visible surfaces.
- RC3: tests assert recomputed effective protections, ratios, path-products, and device sums, not schema/existence alone.
- RC4: the verifier recomputes in Python and never trusts the environment Go evaluator the agent could rewrite.
- RC5: no golden assignment/report fixtures; expected values are computed in test code from the generated scenario.
- RC6: instruction is constraint-complete, not solution-complete; it withholds the algorithm and stage locations.
- RC7/A16: oracle is five real solver bodies, well above the LOC floor.
- CR1/CR7: manifest fixes the stage symbols; instruction nouns are kept off the fix-path symbols.
- CR2: five locations, each controlling a minority test subset; no single stage flips a majority.
- CR8: stages are chained so no file references more than two fix-path symbols.
- GX1: no intent/correctional comments near oracle-written lines.
- GX9/GX10: no per-scenario answer table and no polarity contradiction; the one boolean (`feasible`) is described once with numeric evidence beside it.
- Static checks: digest-pinned Go base, pinned apt, tmux/asciinema, offline verifier, zip exclusions.

### Initial Draft Commitments
- `instruction.md`
- `task.toml`
- `construction_manifest.json`
- `output_contract.toml`
- `environment/Dockerfile`
- `environment/.dockerignore`
- `environment/go.mod`
- `environment/Makefile`
- `environment/README.md`
- `environment/cmd/cgsolve/main.go`
- `environment/internal/types/types.go`
- `environment/internal/refeval/protect.go`
- `environment/internal/refeval/checks.go`
- `environment/internal/refeval/objective.go`
- `environment/qa/a.go`
- `environment/qb/b.go`
- `environment/qc/c.go`
- `environment/qd/d.go`
- `environment/qe/e.go`
- `environment/internal/r6/r.go`
- `environment/internal/r7/s.go`
- `environment/internal/r8/t.go`
- `environment/scripts/build.sh`
- `environment/scripts/run-suite.sh`
- `environment/scripts/solve-one.sh`
- `environment/scripts/clean.sh`
- `environment/docs/architecture.md`
- `environment/docs/cgroup-model.md`
- `environment/docs/operations.md`
- `environment/data/scenarios/aspen.json`
- `environment/data/scenarios/birch.json`
- `environment/data/scenarios/cedar.json`
- `environment/data/scenarios/dahlia.json`
- `environment/data/scenarios/elm.json`
- `environment/data/scenarios/fir.json`
- `solution/solve.sh`
- `tests/test.sh`
- `tests/test_outputs.py`

### Construction manifest (BLOCKING - Step 2b must follow this verbatim)

#### symbol_table
```
- path: qa/a.go
  symbol: Apply
  kind: function
  signature: func Apply(s *types.Scenario, a *types.Assignment) error
  purpose: reserves the protected memory floor at every node so effective floors survive down-scaling
- path: qb/b.go
  symbol: Apply
  kind: function
  signature: func Apply(s *types.Scenario, a *types.Assignment) error
  purpose: sets the non-increasing upper limits and the throttle gap for each node
- path: qc/c.go
  symbol: Apply
  kind: function
  signature: func Apply(s *types.Scenario, a *types.Assignment) error
  purpose: chooses integer relative weights per level so each leaf path-product meets its target
- path: qd/d.go
  symbol: Apply
  kind: function
  signature: func Apply(s *types.Scenario, a *types.Assignment) error
  purpose: allocates per-device throughput caps within each pool above each leaf floor
- path: qe/e.go
  symbol: Apply
  kind: function
  signature: func Apply(s *types.Scenario, a *types.Assignment) error
  purpose: distributes the best-effort reclaimable tier to maximize the worst-off subtree ratio
```

#### flipping_point_contract
```
locations:
  - id: A
    path: qa/a.go
    controls_tests: [test_t01, test_t02, test_t03, test_t13]
  - id: B
    path: qb/b.go
    controls_tests: [test_t01, test_t04, test_t05, test_t13]
  - id: C
    path: qc/c.go
    controls_tests: [test_t01, test_t06, test_t07, test_t13]
  - id: D
    path: qd/d.go
    controls_tests: [test_t01, test_t08, test_t09, test_t13]
  - id: E
    path: qe/e.go
    controls_tests: [test_t01, test_t10, test_t11, test_t12, test_t13]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest
```
- path: internal/r6/r.go
  kind: helper
  rhymes_with: Apply
  non_fix_purpose: renders an ASCII summary of a tree for dry-run console output
- path: internal/r7/s.go
  kind: helper
  rhymes_with: Apply
  non_fix_purpose: aggregates per-node counters for the documentation report only
- path: internal/r8/t.go
  kind: helper
  rhymes_with: Apply
  non_fix_purpose: formats device pool labels for diagnostic listings off the assignment path
```
