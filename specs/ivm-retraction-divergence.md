### Decision
GO - Attempt 1.

- First `distributed_reconciliation` task built around incremental-view-maintenance arithmetic: the solver must reconcile an incrementally maintained materialized view against a from-scratch recomputation of the same query, where the two truth surfaces diverge only on operation streams that include retractions crossing the join -> group-by -> aggregate boundary.
- Hardness survives full disclosure: even with the view schema, the runner interface, the aggregate semantics, and the match-the-recompute target stated, the agent must diagnose three coupled retraction defects (z-set multiplicity on the join, zero-crossing presence in the grouped count/total, and extreme recomputation in min/max) spread across three packages, where no single edit makes a test majority pass.
- The verifier is metamorphic: an independent Python recomputation of the same query over freshly generated random insert/delete streams (no golden file), plus targeted held-out scenarios that isolate each defect. Any engine that matches the recompute on every checkpoint passes, so multiple valid implementations are accepted.

### Metadata

- version: 2
- Task name: ivm-retraction-divergence
- Title: Incremental View Retraction
- Category: data-processing
- Task shape: repair_existing_system
- Languages: ["Rust", "shell"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["rust", "incremental-view-maintenance", "streaming", "retraction", "dataflow"]
- Milestones: 0

## Authoring Brief
This file is the drafting source for the live task under `tasks/ivm-retraction-divergence/`.

### Public contract
Fix the incremental view-maintenance engine under `/app/environment` (a small Rust workspace) so the materialized view it maintains always equals a direct recomputation of the same query over the current relations, for any sequence of inserts and deletes. The maintained view is a grouped aggregate over the join of two base relations: for each group key it reports the number of joined rows, their total, and the smallest and largest joined value. The run interface is `bash /app/environment/scripts/run.sh <scenario-file>` (and `run-suite.sh` over the bundled scenarios), which reads a scenario — a starting pair of relations plus an ordered sequence of insert/delete operations on either relation — applies the operations incrementally, and prints the view after each operation as a sequence of view snapshots. The shipped engine builds and runs and is correct for insert-only runs, but once a run includes deletions it drifts from a direct recompute on the cases incremental maintenance under retraction is hard: stale group rows linger, counts and totals on some groups are wrong, and reported minimums or maximums no longer reflect the rows that remain.

Relations are bags (rows carry an integer multiplicity); the join, count, total, and min/max aggregates follow the z-set / incremental-view-maintenance semantics described in `/app/environment/docs/model.md`, and the runner interface and view schema are in `/app/environment/docs/interface.md`. The bundled scenarios under `/app/environment/scenarios/` and the illustrative snapshots in `/app/environment/evidence/observed.json` anchor the schema and the easy (insert-only / lane-agreeing) cases; they are development evidence, not the full contract. Static or hand-written output is insufficient: the verifier regenerates output by running the engine, including on insert/delete streams generated at verify time.

### platform_files

- path: task.toml
- role: Edition 2 metadata and runtime limits for a hard data-processing Rust task; sets `[environment] allow_internet = false`.
- path: instruction.md
- role: symptoms-only public prompt describing the maintained-view-vs-recompute drift, the run interface, the view schema, and the source-fix target.
- path: output_contract.toml
- role: local authoring metadata declaring the per-snapshot view JSON and schema homes.
- path: construction_manifest.json
- role: authoring metadata for the fix frontier, base image, decoys, flipping-point contract, and forbidden tokens.
- path: environment/Dockerfile
- role: digest-pinned offline Rust image with cargo, pytest, tmux, and asciinema.
- path: tests/test.sh
- role: canonical offline verifier entrypoint that runs pytest and writes reward.
- path: tests/test_outputs.py
- role: independent Python recomputation of the query (the metamorphic oracle) that checks the engine over targeted held-out scenarios and freshly generated random insert/delete streams.
- path: solution/solve.sh
- role: oracle that rewrites the three operator-step bodies and rebuilds; used only for validation.

### task_files

- path: environment/
- role: the engine workspace (a shared z-set kernel, three opaque operator packages on the fix path, a distinct-normalization operator and a diagnostic helper off the fix path, a pipeline package, and a runner binary), bundled scenarios, the model/interface docs, illustrative snapshots, and shell runners visible to the solver.
- path: environment/scenarios/
- role: bundled insert/delete scenarios driven by the engine; development inputs, not answer keys.
- path: solution/solve.sh
- role: oracle implementation used only by Harbor validation.

### fix_frontier

- count: three operator steps.
- distribution: join multiplicity (z-set weight propagation under retraction), grouped count/total with zero-crossing presence, and grouped min/max with extreme recomputation — one defect per opaque package, across three distinct package roots.
- naming_policy: opaque package dirs with single-word neutral names that do not describe the specific aggregate; each exposes a public `push` entry over shared kernel types and delegates the defect-bearing arithmetic to a private per-package step symbol; the instruction names neither the packages nor the step symbols.
- forbidden_stems: instruction nouns such as view, join, group, aggregate, count, total, sum, minimum, maximum, relation, insert, delete, recompute, and drift stay off fix-path symbol, parameter, path, and constant names.
- helpers_policy: the distinct-normalization operator and the diagnostic renderer do genuine non-fix work over the maintained view and never alter the aggregates.
- symbol_thin_preferred: yes; each operator stays in its own package with one public entry and one private step.

### contract_surface

- boolean_fields_max: 0; the view is per-group numeric records (count, total, min, max), not status booleans.
- direct_boolean_assertions_max: 0; checks compare recomputed per-group records, group presence, and derived membership rather than boolean verdict fields.
- preferred_assertion_styles: recompute the per-group view with an independent Python evaluator and compare to the engine snapshot at every checkpoint, run the engine on freshly generated random insert/delete streams, isolate each defect with a targeted held-out scenario, and assert group disappearance, multiplicity-aware counts, and extreme recomputation via record comparison and set membership.
- forbidden_assertion_styles: golden view files shipped under environment, static or hardcoded per-group answers, schema-only or existence-only checks, scenario->field->expected boolean tables, and copying the illustrative snapshots into expected outputs.

### task_shape

- type: repair_existing_system
- instruction_framing: symptoms-only — the maintained-view-vs-recompute drift is described as an observable symptom (stale groups, wrong counts/totals, stale min/max after deletes) while the defect locations, the z-set multiplicity rule, the zero-crossing rule, and the extreme-recompute rule are withheld.
- hardness_source: diagnosis of three coupled retraction defects from runtime divergence, the model doc, and the engine source, plus generalization to verify-time random streams.
- collapse_risk: medium; mitigated by an independent recompute oracle, verify-time random streams, deceptive insert-only-agreeing samples, non-textbook z-set retraction semantics, and a three-package fix frontier with no single location controlling a test majority.

### category_profile

- challenge_family: incremental-view-maintenance reconciliation between incremental maintenance and batch recomputation under retraction across the join/group-by/aggregate boundary.
- bug_family: incremental view maintenance diverges from batch recompute under deletion (multiplicity arithmetic, zero-crossing aggregate retraction, non-self-maintainable extreme recomputation).
- profile_name: distributed_reconciliation
- allowed_instruction_disclosures: the bag/relation input format, the insert/delete scenario format, the runner command and per-snapshot view schema, the aggregate vocabulary (count, total, min, max per group), the match-the-recompute target, offline expectations, and illustrative observed snapshots.
- forbidden_instruction_leaks: the z-set multiplicity rule for the join under retraction, the zero-crossing presence rule for the grouped count/total, the extreme-recomputation rule for min/max, the operator-package identifiers, and per-group expected records.
- category_specific_hardness_bar: the view derives across two truth surfaces (incremental vs recompute) that must agree under retraction; the join multiplicity, the grouped presence/totals, and the min/max recomputation are coupled, no single operator suffices, and a local choice in one operator leaves the other two diverging.
- category_specific_verifier_risks: count-only checks, a last-write-wins or recompute-from-scratch shortcut passing trivially, golden merged fixtures, and scenario-to-answer tables.
- coverage_role: adds the first distributed_reconciliation task and the first incremental-view-maintenance / z-set retraction challenge, distinct from the existing streaming-window and index-invalidation tasks (those are streaming reconciliation; this is incremental-view-maintenance arithmetic), and distinct from the cargo resolver, cgroup allocation, and overlay-flatten tasks.

### difficulty_mechanism_plan

- mechanisms: deceptive_but_valid_local_evidence, buried_local_constraints, stateful_multi_step_dependencies, false_green_intermediate_states, cross_file_cross_format_invariants, rollback_recovery_requirements.
- adversarial_layers_count: six.
- fairness_guardrails: every externally tested input format, scenario operation, view field, aggregate meaning, runner command, and the match-the-recompute target is visible in the instruction or the model doc; only the retraction-handling algorithm is withheld.
- mechanism: deceptive_but_valid_local_evidence
  placement: the bundled scenarios and `observed.json` snapshots are dominated by insert-only and lane-agreeing runs, which the shipped engine reproduces exactly.
  why_model_misses_it: a solver validates against the visible snapshots, sees green, and ships an engine that is still wrong on the held-out retraction streams.
  fairness_guardrail: the instruction states the snapshots are illustrative evidence, not the full contract, and that deletes are where the drift appears.
- mechanism: buried_local_constraints
  placement: the z-set multiplicity rule, the zero-crossing presence rule, and the not-self-maintainable min/max rule live in the model doc and the engine structure, not as a recipe in the instruction.
  why_model_misses_it: a solver that treats the join weight as a set indicator, the group count as a row tally, or min/max as a running scalar never handles retraction correctly.
  fairness_guardrail: the conceptual z-set / IVM model is documented in a readable doc the solver may study, and the scenarios are small enough to trace fully.
- mechanism: stateful_multi_step_dependencies
  placement: a value's presence in a group depends on the net multiplicity threaded from the join through the grouped accumulator, and the reported min/max depends on the surviving value multiset after retractions.
  why_model_misses_it: fixing one operator (for example the join weight) while leaving the grouped presence or the extreme recomputation wrong still diverges on streams that exercise the other operators.
  fairness_guardrail: the coupling is observable by running the engine on the bundled scenarios and diffing against a recompute.
- mechanism: false_green_intermediate_states
  placement: an engine that fixes two of the three operators emits view snapshots that round-trip through the schema and pass the insert-only and single-defect scenarios while still failing the held-out streams that exercise the third.
  why_model_misses_it: schema-valid, sample-passing output reads as success; the shortfall only surfaces against the independent recompute on fresh streams.
  fairness_guardrail: the instruction states results are checked against a recompute on streams beyond the bundled data.
- mechanism: cross_file_cross_format_invariants
  placement: the scenario text format, the per-snapshot JSON view, the Rust engine, and the independent Python recompute must agree on the same bag/z-set query semantics.
  why_model_misses_it: a partial fix handling one aggregate emits output that parses and round-trips but disagrees with the recompute.
  fairness_guardrail: every schema field, the operation vocabulary, and the input format are visible in the instruction or the model doc.
- mechanism: rollback_recovery_requirements
  placement: deletions are retractions that must roll the view back exactly — emptied groups must disappear, multiplicities must net to zero, and extremes must fall back to the surviving rows.
  why_model_misses_it: an engine that only accumulates forward leaves phantom groups, stale totals, and stale extremes after the matching deletes.
  fairness_guardrail: the rollback target is simply "equal the recompute over the current relations," fully stated and checkable.

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: an engineer who knows incremental view maintenance can solve it by reading the model doc, threading z-set multiplicities through the join, retracting grouped output when a group's net count returns to zero, retaining the per-group value multiset so min/max are recomputed when the current extreme is retracted, and self-checking against the insert-only snapshots and a manual recompute.
- shortcut_audit: tests regenerate output by running the engine, build fresh held-out insert/delete streams at verify time, reject static or hardcoded outputs, recompute expected views with an independent Python evaluator rather than trusting any bundled file, and include retraction streams the insert-only snapshots never cover so sample-copying fails.
- ablation_plan: revert each of the three operator steps independently and confirm its declared held-out subset (and the metamorphic streams) fails for that operator only, while the other two operators' isolated scenarios still pass.
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=stronger target agent aligned with Part E worst/best-model thresholds; the verifier is offline (pytest baked into the Dockerfile, no runtime installs under `allow_internet = false`) and post-upload difficulty is classified by Part E after platform agent runs.

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05.
- functional_correctness: the per-group per-snapshot view matches the independent recompute on the bundled scenarios and on freshly generated random insert/delete streams.
- hidden_invariants: emptied groups disappear (no phantom rows), joined-row counts and totals are multiplicity-correct under retraction, and reported min/max reflect only the surviving rows.
- state_hygiene: re-running the engine on the same scenario yields identical snapshots, the view at every checkpoint equals the recompute (not just the final state), and the suite leaves the binary and bundled data in place.
- interface_correctness: the documented runner command reads the documented scenario format and emits the documented per-snapshot JSON view.
- deliverable_completeness: every group present in the queried relations appears in the snapshot with its resolved record, and every bundled scenario is covered by the suite.
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward is 1 only on pytest exit 0; otherwise reward is 0.

### subtype_milestone_plan

- subcategories: []
- milestone_count: 0
- sequential_dependency: not applicable; standard single-step task.
- local_only_data: true
- sidecar_or_protocol_notes: bundled scenarios and the observed-snapshot JSON are local development evidence; the verifier loads authored held-out scenarios and seed-generates additional random insert/delete streams at verify time, all offline.

### satisfiability_risk

- rc2_planned_name_risk: low; operator packages use opaque single-word neutral names, helpers are off the fix path, and data/doc paths use neutral vocabulary while instruction nouns stay off the fix path.
- gx9_contract_risk: low; the instruction states the schema and a few illustrative snapshots but no per-group answer key, and expectations are recomputed by the independent evaluator on held-out streams.
- cr1_symbol_frontier_risk: low; the construction manifest fixes the three private step symbols and the oracle modifies only those packages.
- hidden_contract_risk: low; every tested input format, scenario operation, schema field, aggregate meaning, and run command is in instruction.md or the model doc.

### actionability_plan

- verifier_command_visible: instruction.md names the run command `bash /app/environment/scripts/run.sh <scenario-file>`, the suite script, and that a pytest verifier recomputes and compares the view.
- source_fix_intent_visible: instruction.md says the engine source under `/app/environment` must be fixed and that static output writes are insufficient.
- generated_output_rule_visible: instruction.md identifies the per-snapshot JSON view emitted on stdout and states streams beyond `/app/environment/scenarios` are also evaluated at verify time.
- exact_formula_home: the bag/z-set aggregate semantics (count = sum of multiplicities, total = multiplicity-weighted sum, min/max over the surviving value multiset) live in `/app/environment/docs/model.md`; the precise retraction-handling rules are inferable from the model and the engine and enforced by held-out tests, not stated as a recipe.
- schema_home: instruction.md names the view fields (group key, count, total, min, max) and `observed.json` shows one concrete example of the per-snapshot shape; `docs/interface.md` documents the JSON keys.

### waiver_plan

- waivers_expected: false
- waiver_rationale: no waiver is planned; any checker warning should be resolved or documented before packaging.

### reference_pattern

- justification_if_none: Original task built from the real incremental-view-maintenance / z-set retraction model (the self-maintainability problem of Gupta & Mumick; the z-set multiplicity semantics of DBSP; and differential-dataflow's reduce operator, which retains per-key inputs precisely because count/min/max are not self-maintainable under deletion), minimized into a local deterministic engine with bundled scenarios and verify-time random streams. Not derived from a website task-inspiration, a prior public task, or a reskin of the existing late-window-lineage, incremental-index-invalidation, cargo-feature-unification, cgroup-budget-solver, or overlayfs-whiteout-flatten tasks. The reference library currently has no promoted entries, so no reference_task_id applies.

### realism_source

- source_type: real_system
- evidence_basis: the incremental-view-maintenance self-maintainability problem (Gupta & Mumick, "Maintenance of Materialized Views"), the z-set multiplicity arithmetic of DBSP (Budiu et al.), and differential-dataflow's reduce/consolidate operators — which retain the full per-key input multiset because count/sum are maintained by multiplicity summation while min/max and distinct are not self-maintainable and must be recomputed from the surviving multiset when the current extreme is retracted.
- upstream_or_synthetic_rationale: the retraction semantics come directly from a real, widely-used dataflow model; only the specific engine scaffold and scenarios are authored to keep the task local, offline, and deterministic.
- minimization_preserves: z-set multiplicity propagation through the join under retraction, zero-crossing retraction of grouped aggregate output, the non-self-maintainability of min/max under deletion, and the incremental-equals-recompute invariant at every checkpoint.
- synthetic_exception_review: not a synthetic exception; the model and rules are drawn from a real dataflow system and only the instances are authored.

### Failure topology
The shipped engine processes a stream of insert/delete deltas and maintains the view through three stateful operators: a join that indexes each relation and emits combined-row deltas, a grouped accumulator that maintains each group's count and total, and a grouped extreme operator that reports min and max. It is correct for insert-only runs, so the bundled insert-only snapshots match. Three retraction defects are coupled. The join propagates combined-row deltas with the wrong multiplicity on the retraction branch, so deleting a row that participated in the join with multiplicity greater than one under-retracts the downstream count and total. The grouped accumulator never retracts a group's output row when the group's net count returns to zero, so fully deleted groups linger as phantom rows. The grouped extreme operator maintains min and max as running scalars updated on insertion but not recomputed on retraction, so deleting the current minimum or maximum leaves a stale extreme. Each defect surfaces a distinct observable: wrong counts/totals on multiplicity-bearing groups, lingering emptied groups, and stale extremes after the current extreme is deleted. Because the three observables are disjoint on carefully isolated scenarios but all appear together on random streams, fixing any one operator leaves the maintained view diverging from a direct recompute on the streams that exercise the others; only a coordinated fix across all three operators makes incremental equal recompute at every checkpoint.

### Environment shape
One digest-pinned Rust image with the cargo toolchain, pytest, tmux, and asciinema. The engine is a small Cargo workspace: a shared kernel package with the bag/z-set collection type, the indexed-state types, and a working consolidation routine and scenario reader; three opaque operator packages (a join, a grouped count/total accumulator, and a grouped min/max operator) whose shipped step bodies mishandle retraction; a distinct-normalization operator and a diagnostic renderer that do genuine work off the fix path; a pipeline package that wires the operators in order through their public entries; and a runner binary that reads a scenario and prints the per-snapshot view. Alongside the engine, `scenarios/` holds several bundled insert/delete scenarios, `docs/` describes the z-set / IVM model and the runner interface, `evidence/observed.json` carries illustrative insert-only snapshots, and `scripts/` holds the run and suite runners. The verifier is offline and drives the runner on bundled and held-out scenarios and on verify-time random streams.

### Required artifacts
Step 2b creates `instruction.md`, `task.toml` (`version = "2.0"`, `[environment] allow_internet = false`), `output_contract.toml`, `construction_manifest.json`, `environment/Dockerfile`, `environment/.dockerignore`, the engine workspace source, the bundled scenarios, the model/interface docs, the illustrative snapshots, the shell runners, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. The task is single-step, single-container, non-UI, not long-context, with at least 20 non-Docker files under `environment/`. The verifier deps (pytest, pytest-json-ctrf) are baked into the Dockerfile; `tests/test.sh` runs offline with no apt/pip/curl/uv at runtime, and the verifier rebuilds the engine with `cargo build --release` (offline, no external crates) before checking it.

### Test plan
At least eleven held-out checks, each recomputed by the independent Python evaluator against bundled, authored held-out, or freshly generated scenarios, none reading a golden file:
- t01, t02, t03: z-set multiplicity on the join under retraction — a row that joined with multiplicity > 1 is deleted; the affected group's count and total drop by the full multiplicity while its min/max (an interior value) are unchanged, so the defect is isolated to the join. Multiple approaches: yes. Chain-dependent: yes.
- t04, t05, t06: zero-crossing presence in the grouped count/total — a group is fully deleted (and a re-insert case), so it must disappear with no phantom row; 1:1 joins and single-extreme groups keep the other two operators inert. Multiple approaches: yes. Chain-dependent: yes.
- t07, t08, t09: extreme recomputation in min/max — the current minimum (and maximum, and a churn case) is deleted while the group stays non-empty, so the reported extreme must fall back to the surviving rows; counts/totals stay correct so the defect is isolated to the extreme operator. Multiple approaches: yes. Chain-dependent: yes.
- t10, t11: metamorphic — many seeded random insert/delete streams over the full query; the engine snapshot must equal the independent recompute at every checkpoint. These exercise all three operators and fail if any defect remains. Multiple approaches: yes. Chain-dependent: yes.

### Drafting guardrails
The instruction must read as a symptoms-only repair task. It must disclose the bag/relation input format, the insert/delete scenario format, the runner command, the per-snapshot view schema, the aggregate vocabulary, and the match-the-recompute target, but must not state the z-set multiplicity rule, the zero-crossing rule, or the extreme-recompute rule, and must not name the operator packages or any per-group expected record. Tests must generate fresh held-out streams and recompute expected views independently, never compare a shipped golden output. Keep instruction nouns off fix-path symbol, parameter, path, and constant names; helper and decoy packages must do genuine non-fix work.

### Triviality (Avoidance) Ledger

- Recompute-from-scratch shortcut: an agent that rebuilds the whole view from the base relations each step would pass, but that is a legitimate (multi-approach) outcome and is more work than the three-operator fix; the engine's streaming structure and the per-checkpoint comparison make fixing the operators the natural path, and the metamorphic verifier never rewards hardcoding.
- Naive forward-only engine: passes the insert-only `observed.json` snapshots but fails held-out retraction streams because the verifier recomputes against the current relations at every checkpoint.
- Sample-copy shortcut: blocked by verify-time random streams the snapshots never cover and by retraction scenarios that contradict the insert-only samples.
- Single-operator fix: blocked by the flipping-point contract — each of the three packages controls a distinct held-out subset and no single package controls a test majority; the metamorphic streams require all three.
- Count-as-row-tally shortcut: blocked because z-set multiplicity scenarios make a duplicate-row group's count exceed its distinct-row tally, caught by the join-isolation tests.
- Running-extreme shortcut: blocked because the min/max isolation tests delete the current extreme while the group stays non-empty, so a non-recomputing engine reports a stale extreme.
- Static-output trap: blocked because the verifier regenerates output by running the engine on streams outside `/app/environment/scenarios`.

### Per-gate Pitfall Inventory

- RC1: the oracle must rewrite three substantive operator-step bodies (multiplicity threading, zero-crossing retraction with presence, and per-group multiset retention with extreme recomputation), not remove code or overwrite one short helper.
- RC2: fix-path packages and step symbols are opaque and neutral, and the instruction avoids them, so visible nouns do not grep to the frontier.
- RC3: the verifier compares domain-correct per-group records and group presence against an independent recompute, not schema or existence.
- RC4: expected held-out views live in the Python verifier; bundled `observed.json` is deceptive evidence only and tampering it cannot pass held-out streams.
- RC5: no golden view is shipped under `environment/`; only insert-only illustrative snapshots and input scenarios.
- RC6: the instruction is symptoms-only — it describes the maintained-view-vs-recompute drift and the schema but not the retraction-handling algorithm or the defect locations.
- RC7/GX3: the oracle changes three Rust packages with substantive retraction logic, well above the LOC floor.
- CR1/CR7: the construction manifest records every oracle-touched symbol and the instruction avoids those symbols.
- CR2: three distinct package roots each control a separate held-out subset at concentration <= 0.5.
- CR8: the pipeline references each operator only through its public `push` entry, not the private step symbols, so no visible file names more than two fix-path symbols.
- GX1: no correctional comments near oracle-changed lines.
- GX6: the instruction describes observed symptoms without chaining patch-causation clauses.
- GX9/GX10: the instruction enumerates no per-group answer rows and no contradictory polarity for any field.
- Static/Docker checks: digest-pinned Rust base, pinned apt packages, tmux and asciinema, offline `tests/test.sh`, pytest baked into the image, and a dependency-free Rust workspace so the verifier rebuild is fully offline.

### Initial Draft Commitments

- instruction.md
- task.toml
- output_contract.toml
- construction_manifest.json
- environment/Dockerfile
- environment/.dockerignore
- environment/README.md
- environment/Cargo.toml
- environment/Cargo.lock
- environment/docs/model.md
- environment/docs/interface.md
- environment/kernel/Cargo.toml
- environment/kernel/src/lib.rs
- environment/kernel/src/bag.rs
- environment/kernel/src/scenario.rs
- environment/cog/Cargo.toml
- environment/cog/src/lib.rs
- environment/dot/Cargo.toml
- environment/dot/src/lib.rs
- environment/orb/Cargo.toml
- environment/orb/src/lib.rs
- environment/pad/Cargo.toml
- environment/pad/src/lib.rs
- environment/rib/Cargo.toml
- environment/rib/src/lib.rs
- environment/plan/Cargo.toml
- environment/plan/src/lib.rs
- environment/runner/Cargo.toml
- environment/runner/src/main.rs
- environment/scenarios/insert_only_small.scn
- environment/scenarios/insert_only_lanes.scn
- environment/scenarios/mixed_churn.scn
- environment/scenarios/multiplicity.scn
- environment/scenarios/group_drop.scn
- environment/scenarios/extreme_churn.scn
- environment/evidence/observed.json
- environment/scripts/run.sh
- environment/scripts/run-suite.sh
- solution/solve.sh
- tests/test.sh
- tests/test_outputs.py
