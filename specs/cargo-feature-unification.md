### Decision
GO - Attempt 1.

- First `build_dependency_toolchain` task in the bank and the first Cargo/Rust resolver-semantics challenge: the solver must implement a feature resolver that reproduces Cargo's resolver-v2 unification across a multi-crate workspace and emits the resolved feature set per crate per resolution lane.
- Hardness survives full disclosure: even with the input format, the query interface, the output schema, and the match-resolver-v2 target stated, the host/build/dev lanes must stay un-unified, weak `pkg?/feat` edges must reach a least fixpoint, `dep:` must suppress implicit features, and default-features must drop/re-enable/expand — coordinated across the whole graph. A naive transitive feature union is exactly the wrong model and is what the bundled samples reward.
- The verifier is an independent Python reimplementation of resolver-v2, runs the solver's program on verify-time held-out workspaces (no hardcoding), and accepts any program that matches resolver-v2 (outcome-verified, many implementations pass).

### Metadata

- version: 2
- Task name: cargo-feature-unification
- Title: Cargo Feature Unification
- Category: software-engineering
- Task shape: reverse_engineering
- Languages: ["Rust", "shell"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["rust", "cargo", "feature-resolution", "build-systems", "reverse-engineering"]
- Milestones: 0

## Authoring Brief
This file is the drafting source for the live task under `tasks/cargo-feature-unification/`.

### Public contract
Implement the feature resolver under `/app/environment` (also reachable through `/app`) so the bundled engine reproduces Cargo's resolver-v2 feature unification. The run interface is `bash /app/environment/scripts/run.sh <workspace-dir> <root-crate> <target-triple> <lane>`, which reads one Cargo workspace, resolves features for the requested context, and writes one JSON object on stdout mapping every reachable crate name to its sorted list of enabled features. `bash /app/environment/scripts/run-suite.sh` runs the engine over every bundled workspace under `/app/environment/data/` and writes a per-workspace report. The shipped engine compiles but emits a naive transitive feature union, which agrees with the bundled samples yet is wrong on the cases resolver-v2 was designed to handle.

A workspace is a set of `Cargo.toml` manifests with `resolver = "2"`. Manifests declare `[features]` (including `default`), `[dependencies]`, `[build-dependencies]`, `[dev-dependencies]`, and `[target.'cfg(...)'.dependencies]`; dependency edges may set `default-features = false`, `optional = true`, and a list of requested features; feature expressions may use plain `pkg`, `pkg/feat`, namespaced `dep:pkg`, and weak `pkg?/feat`. The `<lane>` argument selects the resolution context — the normal/target lane, the host/build lane (build-dependencies, proc-macros, and their transitive deps), or the dev lane — and `<target-triple>` selects the platform the `cfg(...)` predicates are evaluated against. The output is a JSON object `{ "<crate>": ["<feature>", ...], ... }` with feature lists sorted and de-duplicated; the engine must produce the same resolution Cargo's resolver v2 would for that workspace, root, triple, and lane.

`/app/environment/docs/model.md` describes the resolver-v2 unification model conceptually and `/app/environment/evidence/observed.json` shows a few illustrative resolved outputs for lane-agreeing cases so the schema and the easy cases are anchored. The illustrative samples are evidence, not the full contract. Static or hand-written output files are insufficient: the verifier regenerates output by running the solver's program, including on workspaces not present under `/app/environment/data`.

### platform_files

- path: task.toml
- role: Edition 2 metadata and runtime limits for a hard software-engineering Rust task; sets `[environment] allow_internet = false`.
- path: instruction.md
- role: behavioral-target public contract for the manifest input format, the run/query interface, the per-lane output schema, and the match-resolver-v2 target.
- path: output_contract.toml
- role: local authoring metadata declaring the per-lane resolved-feature JSON and schema homes.
- path: construction_manifest.json
- role: authoring metadata for the fix frontier, base image, decoys, and flipping-point contract.
- path: environment/Dockerfile
- role: digest-pinned offline Rust image with cargo, pytest, tmux, and asciinema.
- path: tests/test.sh
- role: canonical offline verifier entrypoint that runs pytest and writes reward.
- path: tests/test_outputs.py
- role: independent Python resolver-v2 reimplementation that checks the engine over bundled and held-out workspaces.
- path: solution/solve.sh
- role: oracle that writes the five engine stage bodies and rebuilds; used only for validation.

### task_files

- path: environment/
- role: the engine workspace (shared core, cli entrypoint, five opaque stage packages, helper packages), bundled data workspaces, the model doc, illustrative samples, and shell runners visible to the solver.
- path: environment/data/
- role: bundled Cargo workspaces analyzed by the engine; development inputs, not answer keys.
- path: solution/solve.sh
- role: oracle implementation used only by Harbor validation.

### fix_frontier

- count: five engine stages.
- distribution: edge/default expansion, lane partition across target/host/dev, cfg/target gating, namespaced/optional handling, and weak-edge least fixpoint, one stage per opaque package.
- naming_policy: opaque package dirs `m1` through `m5`, each exposing a single `run` entry over shared types in a non-fix `core` package; the instruction names neither the packages nor the entry symbols.
- forbidden_stems: instruction nouns such as feature, unification, resolver, dependency, weak, optional, default, namespaced, host, graph, and cfg stay off fix-path symbol, parameter, path, and constant names.
- helpers_policy: sibling helper packages `r6` through `r8` do diagnostic and formatting work that never touches the resolved sets.
- symbol_thin_preferred: yes; each stage stays in its own package with one entry function.

### contract_surface

- boolean_fields_max: 0; the output is per-crate feature-name lists, not status booleans.
- direct_boolean_assertions_max: 0; checks compare resolved feature sets, lane separation, and derived membership rather than boolean verdict fields.
- preferred_assertion_styles: recompute per-crate per-lane sets with an independent resolver and compare sorted sets, run the solver's program on freshly generated held-out workspaces, compare the same crate across lanes to assert non-unification, and assert weak-edge activation and `dep:` suppression via set membership.
- forbidden_assertion_styles: golden resolved-output files shipped under environment, static or hardcoded per-crate answers, schema-only or existence-only checks, scenario→field→expected boolean tables, and copying the illustrative samples into expected outputs.

### task_shape

- type: reverse_engineering
- instruction_framing: behavioral-target with the manifest input format, run/query interface, output schema, match-resolver-v2 target, and illustrative samples disclosed while the unification algorithm is withheld.
- hardness_source: semantic inference of the exact unification function from the manifests, the model doc, and the deceptive samples, plus generalization to held-out workspaces.
- collapse_risk: medium; mitigated by an independent resolver, verify-time held-out workspaces, deceptive lane-agreeing samples, a non-textbook unification model, and a five-stage fix frontier with no single location controlling a test majority.

### category_profile

- challenge_family: reverse-engineering build-toolchain feature resolution under resolver-v2 unification semantics.
- profile_name: build_dependency_toolchain
- allowed_instruction_disclosures: the manifest input format, the per-lane query interface and run command, the resolved-feature JSON schema, the platform/target matrix, the match-resolver-v2 target, offline expectations, and illustrative observed samples.
- forbidden_instruction_leaks: the lane non-unification rule, the weak-feature fixpoint, the `dep:` implicit-feature suppression rule, the default re-enable/expand ordering, the engine-stage identifiers, and per-crate expected feature sets.
- category_specific_hardness_bar: the resolved set derives across lanes, cfg-gated edges, namespaced/optional links, default expansion, and a weak-edge fixpoint; no single edge or manifest suffices and a local choice changes distant crates' sets.
- category_specific_verifier_risks: pin-one-dep shortcuts, trusting a tamperable bundled output, clean-only single-platform tests, hidden generated-file expectations, and sample-overfit acceptance.
- coverage_role: adds the first build_dependency_toolchain task and the first Cargo/Rust resolver-semantics reverse-engineering challenge, distinct from the existing cgroup allocation and udev precedence tasks.

### difficulty_mechanism_plan

- mechanisms: deceptive_but_valid_local_evidence, buried_local_constraints, stateful_multi_step_dependencies, false_green_intermediate_states, cross_file_cross_format_invariants.
- adversarial_layers_count: five.
- fairness_guardrails: every externally tested input format, query argument, output field, lane name, run command, and the match-resolver-v2 target is visible; only the unification algorithm is withheld.
- mechanism: deceptive_but_valid_local_evidence
  placement: the bundled `observed.json` samples cover only cases where the lanes happen to agree, so a naive transitive-union resolver reproduces them exactly.
  why_model_misses_it: a solver validates against the visible samples, sees green, and ships a union resolver that is wrong on the held-out lane-separation and weak cases.
  fairness_guardrail: the instruction states the samples are illustrative evidence, not the full contract, and the schema and match-resolver-v2 target are explicit.
- mechanism: buried_local_constraints
  placement: the lane non-unification rule and the weak-edge activation condition live in the model doc and the manifest structure, not as a recipe in the instruction.
  why_model_misses_it: a solver that treats features as a single global union never separates the host/dev lanes or defers weak edges.
  fairness_guardrail: the conceptual model is documented in a readable doc the solver may study and the manifests are small enough to inspect fully.
- mechanism: stateful_multi_step_dependencies
  placement: weak `pkg?/feat` activation depends on whether `pkg` is enabled elsewhere, which depends on namespaced/optional handling, default expansion, lane scope, and cfg gating.
  why_model_misses_it: computing weak activation in a single pass, before later stages enable the link, misses retroactive activation.
  fairness_guardrail: the dependency between stages is observable by running the engine on the bundled workspaces and comparing lanes.
- mechanism: false_green_intermediate_states
  placement: an engine implementing four of five stages emits feature sets that round-trip through the schema and pass the bundled samples while still failing held-out weak-fixpoint or lane cases.
  why_model_misses_it: schema-valid, sample-passing output reads as success; the shortfall only surfaces against the independent resolver on fresh workspaces.
  fairness_guardrail: the instruction states results are checked against resolver-v2 on workspaces beyond the bundled data.
- mechanism: cross_file_cross_format_invariants
  placement: the TOML manifests, the per-lane query interface, the JSON output, the Rust engine, and the independent Python resolver must agree on the same feature semantics.
  why_model_misses_it: a partial implementation handling one lane emits output that parses and round-trips but disagrees with recomputation under the independent resolver.
  fairness_guardrail: every schema field, the lane vocabulary, and the input format are visible in the instruction or the model doc.

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: an engineer who knows the Cargo features model can solve it by reading the model doc, expanding edges with default handling, separating the three lanes, gating cfg edges against the triple, resolving namespaced/optional links, and iterating the weak edges to a fixpoint, self-checking against the illustrative samples.
- shortcut_audit: tests regenerate output by running the solver's program, build fresh held-out workspaces at verify time, reject static or hardcoded outputs, recompute expected sets with an independent Python resolver rather than trusting any bundled file, and include a contradictory deceptive sample so sample-copying fails.
- ablation_plan: stub each of the five engine stages independently and confirm at least one held-out verifier test fails for that stage only.
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=stronger target agent aligned with Part E worst/best-model thresholds; the verifier is offline (pytest baked into the Dockerfile, no runtime installs under `allow_internet = false`) and post-upload difficulty is classified by Part E after platform agent runs.

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05.
- functional_correctness: per-crate per-lane feature sets match resolver v2 on the bundled and held-out workspaces across the platform matrix.
- hidden_invariants: host/dev lanes do not unify with the target lane, weak `?` edges activate only when their link is otherwise live, and `dep:` suppresses implicit features.
- state_hygiene: re-running the solver on the same workspace and query yields identical sorted sets and the suite leaves the binary and bundled data in place.
- interface_correctness: the documented run command and suite script read the documented inputs and emit the documented per-lane JSON shape.
- deliverable_completeness: every crate reachable in the queried lane appears in the output with its resolved set and every bundled workspace is covered by the suite.
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward is 1 only on pytest exit 0; otherwise reward is 0.

### subtype_milestone_plan

- subcategories: []
- milestone_count: 0
- sequential_dependency: not applicable; standard single-step task.
- local_only_data: true
- sidecar_or_protocol_notes: bundled data workspaces and the observed-sample JSON are local development evidence; the verifier loads authored held-out workspaces and seed-generates additional ones at verify time, all offline.

### satisfiability_risk

- rc2_planned_name_risk: low; engine stages are opaque `m1`-`m5`, helpers are `r6`-`r8`, and data/doc paths use neutral vocabulary while instruction nouns stay off the fix path.
- gx9_contract_risk: low; the instruction states the schema and a few illustrative samples but no per-crate answer key, and expectations are recomputed by the independent resolver on held-out workspaces.
- cr1_symbol_frontier_risk: low; the construction manifest fixes the five `run` symbols and the oracle modifies only those packages.
- hidden_contract_risk: low; every tested input format, query argument, schema field, and run command is in instruction.md or the model doc.

### actionability_plan

- verifier_command_visible: instruction.md names the run command `bash /app/environment/scripts/run.sh <workspace> <root> <triple> <lane>`, the suite script, and the pytest verifier command.
- source_fix_intent_visible: instruction.md says the engine sources under `/app/environment` (core, cli, m1-m5), also reachable through `/app`, must be implemented and that static output writes are insufficient.
- generated_output_rule_visible: instruction.md identifies the per-lane JSON emitted on stdout and the suite report and states workspaces beyond `/app/environment/data` are also resolved at verify time.
- exact_formula_home: the conceptual unification model lives in `/app/environment/docs/model.md` and the instruction; the precise per-edge rules are inferable from the manifests and observed samples and enforced by held-out tests, not stated as a recipe.
- schema_home: instruction.md names every output JSON field and `observed.json` shows one concrete example of the per-lane shape.

### waiver_plan

- waivers_expected: false
- waiver_rationale: no waiver is planned; any checker warning should be resolved or documented before packaging.

### reference_pattern

- justification_if_none: Original task built from the real Cargo resolver-v2 feature-unification model (Cargo Book Features/Resolver chapters and RFC 2957 weak dependency features); not derived from a website task-inspiration, a prior public task, or a reskin of the existing cgroup-budget-solver or udev-rule-precedence-reconstruct tasks. The reference library currently has no promoted entries, so no reference_task_id applies.

### realism_source

- source_type: real_system
- evidence_basis: Cargo's feature resolver v2 (`resolver = "2"`) — default-features handling, optional dependencies and the `dep:` namespaced syntax, weak dependency features `pkg?/feat` from RFC 2957, and the host/build/dev/target dependency-kind boundaries that do not unify, as documented in the Cargo Book Features and Resolver chapters.
- upstream_or_synthetic_rationale: the unification semantics come directly from a real, widely-used toolchain; only the specific workspaces and the opaque engine scaffold are authored to keep the task local, offline, and deterministic.
- minimization_preserves: lane non-unification across target/host/dev, the weak-feature least fixpoint, `dep:` implicit-feature suppression, default-features drop/re-enable/expand, and cfg-gated target edges.
- synthetic_exception_review: not a synthetic exception; the model and rules are drawn from a real build toolchain and only the instances are authored.

### Failure topology
The shipped engine parses the manifests and emits a plain transitive feature union: it walks every dependency edge regardless of kind, unions every requested and default feature, treats every optional dependency as an implicit feature, and ignores weak `?` qualifiers, `cfg(...)` predicates, and the host/dev boundaries. That output compiles, round-trips through the schema, and matches the bundled `observed.json` samples — which were chosen to be lane-agreeing — so it reads as correct. The five resolution concerns are genuinely coupled. Whether a weak `pkg?/feat` edge activates depends on whether `pkg` is enabled by some non-weak path, which depends on namespaced/optional resolution, default expansion, the lane the query selected, and which cfg edges survive for the requested triple. Separating the host/build and dev lanes changes which edges propagate, which changes which optional links are live, which changes which weak edges activate. Default-features dropped on one edge can be re-enabled by a sibling edge, and `default` must be expanded into its member features before further propagation. Any partial implementation that handles some concerns but not all stays green on the samples while diverging from resolver-v2 on the held-out workspaces, where the verifier recomputes the expected sets independently.

### Environment shape
One digest-pinned Rust image with the cargo toolchain, pytest, tmux, and asciinema. The engine is itself a small Cargo workspace: a shared `core` package with the graph/query types and a working TOML manifest reader; a `cli` package with the entrypoint and a thin pipeline that runs the stages in order; five opaque stage packages that the shipped build leaves as naive pass-through stubs; and two or three sibling helper packages that do diagnostic and formatting work off the resolution path. Alongside the engine, `data/` holds several bundled multi-crate Cargo workspaces exercising the full feature zoo, `docs/` describes the resolver-v2 model and the run interface, `evidence/observed.json` carries the illustrative lane-agreeing samples, and `scripts/` holds the run and suite runners. The verifier is offline and invokes the engine's run command on bundled and held-out workspaces.

### Required artifacts
Step 2b creates `instruction.md`, `task.toml` (`version = "2.0"`, `[environment] allow_internet = false`), `output_contract.toml`, `construction_manifest.json`, `environment/Dockerfile`, the engine workspace source, the bundled data workspaces, the model/interface docs, the illustrative samples, the shell runners, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. The task is single-step, single-container, non-UI, not long-context, with at least 20 non-Docker files under `environment/`. The verifier deps (pytest) are baked into the Dockerfile; `tests/test.sh` runs offline with no apt/pip/curl/uv at runtime.

### Test plan
At least twelve held-out checks (plus a deterministic re-run), each recomputed by the independent Python resolver against fresh workspaces, none reading a golden file:
- t01: end-to-end resolution on a bundled workspace across all lanes and a platform — exercises every stage. Multiple approaches: yes. Chain-dependent: yes.
- t02, t03: default-features drop, sibling re-enable, and transitive `default` expansion on held-out manifests. Multiple approaches: yes. Chain-dependent: yes.
- t04, t05: host/build and dev lanes do not unify with the target lane for a crate present in two lanes. Multiple approaches: yes. Chain-dependent: yes.
- t06, t07: cfg/target gating includes a target edge for one triple and excludes it for another. Multiple approaches: yes. Chain-dependent: yes.
- t08, t09: `dep:` suppresses the implicit same-name feature and an explicit `pkg/feat` activates a dormant optional link. Multiple approaches: yes. Chain-dependent: yes.
- t10, t11, t12: weak `pkg?/feat` stays dormant until `pkg` is enabled elsewhere, then activates via the least fixpoint, including a retroactive-activation case. Multiple approaches: yes. Chain-dependent: yes.
- t13: re-running the engine on the same workspace and query yields byte-identical sorted output. Multiple approaches: yes. Chain-dependent: no.

### Drafting guardrails
The instruction must read as a behavioral reverse-engineering task, not a recipe. It must disclose the manifest input format, the run/query interface, the lane vocabulary, the output schema, and the match-resolver-v2 target, but must not state the lane non-unification rule, the weak-feature fixpoint, the `dep:` suppression rule, or the default re-enable/expand ordering, and must not name the engine stages or any per-crate expected set. Tests must generate fresh held-out workspaces and recompute expected sets independently, never compare a shipped golden output. Keep instruction nouns off fix-path symbol, parameter, path, and constant names; helper and decoy packages must do genuine non-fix work.

### Triviality (Avoidance) Ledger

- Naive transitive-union resolver: passes the lane-agreeing `observed.json` samples but fails held-out lane-separation, weak-fixpoint, and `dep:` cases because the verifier recomputes against resolver-v2 on fresh workspaces.
- Sample-copy shortcut: blocked by held-out workspaces the samples never cover and a contradictory deceptive sample.
- Single-pass weak handling: blocked because retroactive weak activation only appears once a later stage enables the link, so a non-fixpoint pass diverges on t10-t12.
- Lane-merge shortcut: blocked by tests that compare the same crate across the host/dev and target lanes and require different sets.
- One-stage fix: blocked by the flipping-point contract — each of the five packages controls a distinct held-out subset and no single package controls a test majority.
- Static-output trap: blocked because the verifier regenerates output by running the solver's program on workspaces outside `/app/environment/data`.

### Per-gate Pitfall Inventory

- RC1: the oracle must implement five substantive stage bodies and a fixpoint loop, not remove code or overwrite one short helper.
- RC2: fix-path packages and symbols are opaque (`m1`-`m5`/`run`) and the instruction avoids them, so visible nouns do not grep to the frontier.
- RC3: the verifier compares domain-correct resolved feature sets and lane separation, not schema or existence.
- RC4: expected held-out sets live in the Python verifier; bundled `observed.json` is deceptive evidence only and tampering it cannot pass held-out tests.
- RC5: no golden resolved output is shipped under `environment/`; only lane-agreeing illustrative samples and input manifests.
- RC6: the instruction is complete about the input format, interface, and schema but not the unification algorithm.
- RC7/GX3: the oracle changes five Rust packages with substantive propagation logic and a fixpoint, well above the LOC floor.
- CR1/CR7: the construction manifest records every oracle-touched symbol and the instruction avoids those symbols.
- CR2: five distinct package roots each control a separate held-out subset.
- GX1: no correctional comments near oracle-changed lines.
- GX9/GX10: the instruction enumerates no per-crate answer rows and no contradictory polarity for any field.
- Static/Docker checks: digest-pinned Rust base, pinned apt packages, tmux and asciinema, offline `tests/test.sh`, and pytest baked into the image.

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
- environment/core/Cargo.toml
- environment/core/src/lib.rs
- environment/core/src/intake.rs
- environment/cli/Cargo.toml
- environment/cli/src/main.rs
- environment/cli/src/pipeline.rs
- environment/m1/Cargo.toml
- environment/m1/src/lib.rs
- environment/m2/Cargo.toml
- environment/m2/src/lib.rs
- environment/m3/Cargo.toml
- environment/m3/src/lib.rs
- environment/m4/Cargo.toml
- environment/m4/src/lib.rs
- environment/m5/Cargo.toml
- environment/m5/src/lib.rs
- environment/r6/Cargo.toml
- environment/r6/src/lib.rs
- environment/r7/Cargo.toml
- environment/r7/src/lib.rs
- environment/r8/Cargo.toml
- environment/r8/src/lib.rs
- environment/data/alpha/ (multi-crate workspace: root plus member manifests)
- environment/data/beta/ (multi-crate workspace exercising weak and dep: edges)
- environment/data/gamma/ (multi-crate workspace exercising cfg and lane splits)
- environment/evidence/observed.json
- environment/scripts/run.sh
- environment/scripts/run-suite.sh
- solution/solve.sh
- tests/test.sh
- tests/test_outputs.py
