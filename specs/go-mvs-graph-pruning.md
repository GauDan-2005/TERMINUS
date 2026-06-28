### Decision
GO - Attempt 1.

- First version-selection task in the bank: the shipped tool computes a build list over a pruned requirement graph and is wrong under the combination of require, exclude, replace, and retract; no prior task exercises minimal-version-selection or module-graph pruning, so this adds genuinely new coverage to `build_dependency_toolchain`.
- Hardness survives full disclosure of the symptoms and the verification method: even told that "some graphs select the wrong revisions or load too much", the solver must reconstruct that the pruned graph keeps a folded node's direct requirements but not its deeper ones, that an excluded revision bumps up rather than vanishes, that a replacement contributes the replacement's own requirements, that the selected revision is the maximum of the required minimums, and that a retracted revision stays selected yet is held back only from the upgrade preview — five coupled rules where the obvious mental model is wrong.
- The verifier is an independent Python reimplementation of the planner that runs the solver's program on verify-time held-out graphs (no hardcoding) and accepts any program that produces the correct build list, the held set, and the upgrade preview.

### Metadata

- version: 2
- Task name: go-mvs-graph-pruning
- Title: Go Module Build-List Planner
- Category: build-and-dependency-management
- Task shape: repair_existing_system
- Languages: ["Go", "shell"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["go", "go-modules", "version-selection", "build-systems", "dependency-resolution"]
- Milestones: 0

## Authoring Brief
This file is the drafting source for the live task under `tasks/go-mvs-graph-pruning/`.

### Public contract
Repair the build-list planner under `/app/environment` (also reachable through `/app`) so it computes the correct selection for a bundled, offline graph format. The run interface is `bash /app/environment/scripts/run.sh <catalog-dir>`, which reads one catalog describing a root, a fold threshold, a set of declared node revisions with their requirements and ranks, plus root-level exclude and replace directives and node-level retract directives, then writes one JSON object on stdout with three keys: `picks` (the chosen revision per node in the build list), `held` (the nodes whose chosen revision is retracted), and `fresh` (the per-node upgrade-preview revision). `bash /app/environment/scripts/run-suite.sh` runs the planner over every bundled catalog under `/app/environment/data/` and writes a combined report. The shipped tool builds and runs but is wrong: on catalogs that exercise excludes, replaces, retracts, deeper requirements behind folded nodes, or multiply-required nodes, it produces the wrong `picks`/`held`/`fresh`, while still matching the bundled illustrative catalogs whose graphs are simple enough that every rule coincides with the naive one.

A catalog is a single text file. It names the root node and a fold threshold, declares each node revision with its rank and its list of requirements (a requirement names another node and a minimum revision), and may declare root-level excludes (a node revision the root forbids), root-level replaces (substitute a node — optionally only at a specific revision — with another node revision), and retracts (a node revision its own author has withdrawn). `/app/environment/docs/model.md` describes the selection model conceptually and `/app/environment/docs/interface.md` documents the catalog grammar, the run command, and the output schema. `/app/environment/evidence/observed.json` shows the correct output for the bundled illustrative catalogs only; those catalogs are deliberately simple and do not pin down the rules the held-out graphs exercise. Static or hand-written output files are insufficient: the verifier regenerates output by running the solver's program, including on catalogs not present under `/app/environment/data`.

### platform_files

- path: task.toml
- role: Edition 2 metadata and runtime limits for a hard build-and-dependency-management Go task; sets `[environment] allow_internet = false`.
- path: instruction.md
- role: symptoms-only repair prompt naming the run interface, the catalog input, the output schema, the observable wrong behavior, and the verification method, without naming the cause, the fix locations, or the selection rules.
- path: output_contract.toml
- role: local authoring metadata declaring the combined-report JSON and its schema home.
- path: construction_manifest.json
- role: authoring metadata for the fix frontier, base image, decoys, and flipping-point contract.
- path: environment/Dockerfile
- role: digest-pinned offline Go image with the toolchain, pytest, tmux, and asciinema.
- path: tests/test.sh
- role: canonical offline verifier entrypoint that runs pytest and writes reward.
- path: tests/test_outputs.py
- role: independent Python planner reimplementation that checks the tool over bundled and held-out catalogs.
- path: solution/solve.sh
- role: oracle that rewrites the five planner stage bodies and rebuilds; used only for validation.

### task_files

- path: environment/
- role: the planner module (shared types, a working catalog reader, the entrypoint, a pipeline driver, five opaque stage packages, helper packages), bundled data catalogs, the model and interface docs, illustrative outputs, and shell runners visible to the solver.
- path: environment/data/
- role: bundled catalogs analyzed by the planner; development inputs, not answer keys.
- path: solution/solve.sh
- role: oracle implementation used only by Harbor validation.

### fix_frontier

- count: five planner stages.
- distribution: requirement reading with fold pruning, replace substitution, exclude bumping, maximum-of-minimums selection, and retract reporting — one stage per opaque package, each controlling a distinct held-out subset.
- naming_policy: opaque package dirs `pass1` through `pass5`, each exposing a single `Step` entry over shared types in a non-fix `plan` package; the instruction names neither the packages nor the entry symbol; the pipeline driver references only the one shared `Step` name.
- forbidden_stems: instruction nouns such as module, version, require, exclude, replace, retract, prune, select, build, resolver, dependency, tier, and upgrade stay off fix-path symbol, parameter, path, and constant names.
- helpers_policy: sibling helper packages `render`, `tally`, and `banner` do diagnostic and formatting work that never touches the chosen revisions.
- symbol_thin_preferred: yes; each stage stays in its own package with one `Step` entry function.

### contract_surface

- boolean_fields_max: 0; the output is per-node revision integers and a list of held node names, not status booleans.
- direct_boolean_assertions_max: 0; checks compare the chosen revision map, the held set, and the upgrade-preview map rather than boolean verdict fields.
- preferred_assertion_styles: recompute the build list, the held set, and the upgrade preview with an independent planner and compare; run the solver's program on freshly generated held-out catalogs; assert pruning by checking a deep node is absent behind a folded parent yet present behind an open one; assert selection by requiring a node at two revisions and checking the maximum; assert retract by checking the revision stays chosen yet is held back from the preview.
- forbidden_assertion_styles: golden output files shipped under environment, static or hardcoded per-node answers, schema-only or existence-only checks, scenario-to-field-to-expected boolean tables, and copying the illustrative outputs into expected values.

### task_shape

- type: repair_existing_system
- instruction_framing: symptoms-only; the prompt names the run interface, the catalog input, the output schema, the observable wrong behavior, and the verification method, while withholding the cause, the fix locations, and the selection rules.
- hardness_source: diagnosis and semantic inference — reproducing the symptoms, reconstructing the five coupled selection rules from the model doc and the catalogs, localizing the five wrong stages among decoys, and correcting each so the build list generalizes to held-out catalogs.
- collapse_risk: medium; mitigated by an independent planner, verify-time held-out catalogs, deliberately simple bundled catalogs that hide the rules, a non-textbook selection model, and a five-stage fix frontier with no single location controlling a test majority.

### category_profile

- challenge_family: repairing a minimal-version-selection planner whose pruned-graph traversal interacts with exclude, replace, and retract directives.
- profile_name: build_dependency_toolchain
- allowed_instruction_disclosures: the catalog input format, the run command and suite command, the three-key output schema, the offline expectation, the observable symptoms, and that the bundled outputs are illustrative.
- forbidden_instruction_leaks: the fold-pruning rule (direct-but-not-deeper behind a folded node), the exclude-bump rule, the replace-brings-its-own-requirements rule, the maximum-of-minimums selection rule, the retract-stays-but-held rule, the stage identifiers, and per-node expected revisions.
- category_specific_hardness_bar: the chosen revision of one node derives from pruning decisions, exclude bumps, replace substitutions, and the maximum over every requirement that survives; no single directive or node suffices and a local choice changes distant nodes' revisions.
- category_specific_verifier_risks: trusting a tamperable bundled report, single-catalog tests, clean-only graphs with no excludes/replaces/retracts, hidden generated-file expectations, and accepting a tool that only reproduces the illustrative catalogs.
- coverage_role: adds the first version-selection and module-graph-pruning task, distinct from the existing Cargo feature-resolution, cgroup allocation, and overlay-flatten tasks.

### difficulty_mechanism_plan

- mechanisms: deceptive_but_valid_local_evidence, buried_local_constraints, stateful_multi_step_dependencies, false_green_intermediate_states, cross_file_cross_format_invariants.
- adversarial_layers_count: five.
- fairness_guardrails: every externally tested input keyword, run command, output key, and the match-the-model target is visible in the instruction or the model and interface docs; only the selection rules and the fix locations are withheld.
- mechanism: deceptive_but_valid_local_evidence
  placement: the bundled catalogs are simple — every node is required at one revision, all nodes are open, and there are no excludes, replaces, or retracts — so the naive planner reproduces their outputs exactly.
  why_model_misses_it: a solver validates against the visible outputs, sees them match, and concludes the planner is already correct, missing the held-out cases the simple catalogs never exercise.
  fairness_guardrail: the instruction states the bundled outputs are illustrative and that the verifier runs additional held-out catalogs, and the interface doc states the simple catalogs do not pin down the rules.
- mechanism: buried_local_constraints
  placement: the pruning rule, the exclude-bump rule, and the retract-stays rule live in the model doc and the catalog structure, not as a recipe in the instruction.
  why_model_misses_it: a solver that walks the whole requirement graph and treats "minimal" as the lowest revision never prunes deep requirements behind folded nodes and selects the wrong revision.
  fairness_guardrail: the conceptual model is documented in a readable doc the solver may study and the catalogs are small enough to inspect fully.
- mechanism: stateful_multi_step_dependencies
  placement: a replace can introduce a folded node whose pruning then hides a deeper requirement, an exclude can bump a revision that changes the maximum, and a retract changes the preview but not the selection — the stages feed each other.
  why_model_misses_it: fixing one stage in isolation leaves the others wrong, and the coupling means a partial fix still fails the comprehensive and coupling catalogs.
  fairness_guardrail: the dependency between stages is observable by running the planner on catalogs that combine the directives and comparing.
- mechanism: false_green_intermediate_states
  placement: a planner that fixes four of five stages still produces output that parses and round-trips through the schema and passes the bundled catalogs while failing held-out exclude, replace, or retract cases.
  why_model_misses_it: schema-valid, sample-passing output reads as success; the shortfall only surfaces against the independent planner on fresh catalogs.
  fairness_guardrail: the instruction states results are checked against the model on catalogs beyond the bundled data.
- mechanism: cross_file_cross_format_invariants
  placement: the catalog text format, the run interface, the JSON output, the Go planner, and the independent Python planner must agree on the same selection semantics.
  why_model_misses_it: a partial implementation handling one directive emits output that parses but disagrees with recomputation under the independent planner.
  fairness_guardrail: every output key, the catalog grammar, and the run command are visible in the instruction or the docs.

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: an engineer who knows minimal version selection and Go module-graph pruning can solve it by reading the model doc, reproducing the symptoms, and correcting each stage: read direct-but-not-deeper requirements behind a folded node, substitute replaces with their own requirements, bump excluded revisions to the next available, select the maximum of the required minimums, and keep retracted revisions selected while holding them back from the preview, self-checking against the illustrative outputs.
- shortcut_audit: tests regenerate output by running the solver's program, build fresh held-out catalogs at verify time, reject static or hardcoded outputs, recompute expected values with an independent Python planner rather than trusting any bundled file, and include catalogs whose correct output contradicts the naive planner so sample-matching fails.
- ablation_plan: revert each of the five stage bodies to its shipped form independently and confirm at least one held-out verifier test fails for that stage only.
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=stronger target agent aligned with Part E worst/best-model thresholds; the verifier is offline (pytest baked into the Dockerfile, no runtime installs under `allow_internet = false`) and post-upload difficulty is classified by Part E after platform agent runs.

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05.
- functional_correctness: the build list, held set, and upgrade preview match the independent planner on the bundled and held-out catalogs.
- hidden_invariants: deep requirements behind folded nodes are pruned, excluded revisions bump up, replaces contribute their own requirements, selection is the maximum of the minimums, and retracted revisions stay selected but absent from the preview.
- state_hygiene: re-running the planner on the same catalog yields identical output and the suite leaves the binary and bundled data in place.
- interface_correctness: the documented run command and suite script read the documented inputs and emit the documented three-key JSON shape.
- deliverable_completeness: every node in the build list appears in `picks` and every bundled catalog is covered by the suite report.
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward is 1 only on pytest exit 0; otherwise reward is 0.

### subtype_milestone_plan

- subcategories: []
- milestone_count: 0
- sequential_dependency: not applicable; standard single-step task.
- local_only_data: true
- sidecar_or_protocol_notes: bundled data catalogs and the illustrative-output JSON are local development evidence; the verifier loads authored held-out catalogs and seed-generates additional ones at verify time, all offline.

### satisfiability_risk

- rc2_planned_name_risk: low; planner stages are opaque `pass1`-`pass5`, helpers are `render`/`tally`/`banner`, and data/doc paths use neutral vocabulary while instruction nouns stay off the fix path.
- gx9_contract_risk: low; the instruction states the schema and points at illustrative outputs but no per-node answer key, and expectations are recomputed by the independent planner on held-out catalogs.
- cr1_symbol_frontier_risk: low; the construction manifest fixes the five `Step` symbols and the oracle modifies only those packages.
- hidden_contract_risk: low; every tested input keyword, output key, and run command is in instruction.md or the docs.

### actionability_plan

- verifier_command_visible: instruction.md names the run command `bash /app/environment/scripts/run.sh <catalog-dir>`, the suite script, and the pytest verifier command.
- source_fix_intent_visible: instruction.md says the planner sources under `/app/environment` (also reachable through `/app`) build and run but compute the wrong result and must be repaired, and that static output writes are insufficient.
- generated_output_rule_visible: instruction.md identifies the JSON emitted on stdout and the suite report and states catalogs beyond `/app/environment/data` are also planned at verify time.
- exact_formula_home: the conceptual selection model lives in `/app/environment/docs/model.md`; the precise per-directive rules are inferable from the model, the catalogs, and the symptoms and enforced by held-out tests, not stated as a recipe in instruction.md.
- schema_home: instruction.md names the three output keys and `/app/environment/docs/interface.md` documents the catalog grammar and shows one concrete example of the output shape.

### waiver_plan

- waivers_expected: false
- waiver_rationale: no waiver is planned; any checker warning should be resolved or documented before packaging.

### reference_pattern

- justification_if_none: Original task built from the real Go modules minimal-version-selection and module-graph-pruning model (go.dev/ref/mod minimal-version-selection and graph-pruning sections, plus Russ Cox's MVS writeups), minimized into a local deterministic planner with a bundled offline catalog format; not derived from a website task-inspiration, a prior public task, or a reskin of the existing cargo-feature-unification, cgroup-budget-solver, or overlayfs-whiteout-flatten tasks. The reference library currently has no promoted entries, so no reference_task_id applies.

### realism_source

- source_type: real_system
- evidence_basis: Go modules minimal version selection (the build list is the maximum of the required minimum versions), module graph pruning for `go 1.17+` modules (a pruned graph keeps a module's own requirements but not the deep transitive requirements behind it unless reached through an unpruned module), and the `exclude`, `replace`, and `retract` directive semantics, as documented at go.dev/ref/mod.
- upstream_or_synthetic_rationale: the selection and pruning semantics come directly from a real, widely-used toolchain; only the specific catalogs and the opaque planner scaffold are authored to keep the task local, offline, and deterministic.
- minimization_preserves: maximum-of-minimums selection, pruned-graph direct-but-not-deeper traversal, exclude bumping to the next available revision, replace contributing the replacement's own requirements, and retract keeping a revision selected while withholding it from the upgrade preview.
- synthetic_exception_review: not a synthetic exception; the model and rules are drawn from a real build toolchain and only the instances are authored.

### Failure topology
The shipped planner parses the catalog and runs five stages, but each stage encodes the obvious-yet-wrong mental model. The requirement-reading stage walks the whole graph and reads every node's deeper requirements regardless of the fold threshold, so it loads requirements that a pruned graph would never see. The replace stage rewrites a requirement's selected identity to the replacement but keeps reading the original node's requirements instead of the replacement's. The exclude stage treats an excluded revision as simply usable and never bumps to the next available revision. The selection stage takes the minimum required revision rather than the maximum. The retract stage drops a retracted revision out of the build list rather than keeping it selected and only withholding it from the upgrade preview. On the bundled catalogs — every node required at one revision, all nodes open, no excludes, replaces, or retracts — all five wrong rules coincide with the right answer, so the tool reproduces the illustrative outputs and reads as correct. The five concerns are coupled: a replace can introduce a folded node whose deeper requirement must then be pruned; an exclude bump can raise a revision that becomes the maximum; a retract changes the preview without changing the selection. Any partial repair stays green on the bundled catalogs while diverging from the model on the held-out catalogs, where the verifier recomputes the expected build list independently.

### Environment shape
One digest-pinned Go image with the toolchain, pytest, tmux, and asciinema. The planner is a small Go module: a shared `plan` package with the graph/query types and a working catalog reader; an entrypoint that prints the JSON report; a pipeline driver that runs the five stages to a fixed point and then reports; five opaque stage packages whose shipped bodies encode the wrong rules; and three sibling helper packages that do diagnostic and formatting work off the selection path. Alongside the planner, `data/` holds several bundled catalogs, `docs/` describes the selection model and the run interface, `evidence/observed.json` carries the illustrative correct outputs, and `scripts/` holds the run and suite runners. The verifier is offline and invokes the planner's run command on bundled and held-out catalogs.

### Required artifacts
Step 2b creates `instruction.md`, `task.toml` (`version = "2.0"`, `[environment] allow_internet = false`), `output_contract.toml`, `construction_manifest.json`, `environment/Dockerfile`, the planner module source, the bundled data catalogs, the model and interface docs, the illustrative outputs, the shell runners, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. The task is single-step, single-container, non-UI, not long-context, with at least 20 non-Docker files under `environment/`. The verifier deps (pytest) are baked into the Dockerfile; `tests/test.sh` runs offline with no apt/pip/curl/uv at runtime.

### Test plan
At least thirteen held-out checks (plus a deterministic re-run), each recomputed by the independent Python planner against fresh catalogs, none reading a golden file:
- t01: end-to-end planning on a comprehensive held-out catalog combining all directives — exercises every stage. Multiple approaches: yes. Chain-dependent: yes.
- t02, t03: a deep requirement behind a folded node is pruned, while the same requirement behind an open node is kept. Multiple approaches: yes. Chain-dependent: yes.
- t04, t05: a replace contributes the replacement's own requirements; a revision-qualified replace applies only at the matching revision. Multiple approaches: yes. Chain-dependent: yes.
- t06, t07: an excluded revision bumps to the next available revision; consecutive excludes bump past both. Multiple approaches: yes. Chain-dependent: yes.
- t08, t09: a node required at two revisions selects the maximum; a deeper requirement raises a node above its direct minimum. Multiple approaches: yes. Chain-dependent: yes.
- t10, t11: a retracted selected revision stays in the build list and is reported as held; the upgrade preview skips a retracted top revision. Multiple approaches: yes. Chain-dependent: yes.
- t12: a replace introduces a folded node whose deeper requirement must be pruned and whose revision must win the maximum — passes only when pruning, replace, and selection are all correct. Multiple approaches: yes. Chain-dependent: yes.
- t13: re-running the planner on the same catalog yields byte-identical output. Multiple approaches: yes. Chain-dependent: no.

### Drafting guardrails
The instruction must read as a symptoms-only repair task, not a recipe or a diagnosis. It must disclose the catalog input format, the run/suite interface, the three output keys, and the observable wrong behavior, but must not state the fold-pruning rule, the exclude-bump rule, the replace-requirements rule, the maximum-of-minimums rule, or the retract-stays rule, must not name the cause or the stage packages, and must not show any per-node expected revision. Tests must generate fresh held-out catalogs and recompute expected values independently, never compare a shipped golden output. Keep instruction nouns off fix-path symbol, parameter, path, and constant names; helper and decoy packages must do genuine non-fix work.

### Triviality (Avoidance) Ledger

- Naive whole-graph, lowest-revision planner: reproduces the simple bundled catalogs but fails held-out pruning, exclude, replace, retract, and maximum cases because the verifier recomputes against the model on fresh catalogs.
- Sample-match shortcut: blocked by held-out catalogs the bundled outputs never cover and by catalogs whose correct output contradicts the naive planner.
- Single-pass partial fix: blocked because the directives are coupled, so a comprehensive and a coupling catalog fail unless pruning, replace, exclude, and selection are all correct.
- Retract-as-exclude shortcut: blocked by a catalog where a retracted revision is still the selected maximum and must remain in the build list while being held back from the preview.
- One-stage fix: blocked by the flipping-point contract — each of the five packages controls a distinct held-out subset and no single package controls a test majority.
- Static-output trap: blocked because the verifier regenerates output by running the solver's program on catalogs outside `/app/environment/data`.

### Per-gate Pitfall Inventory

- RC1: the oracle must rewrite five substantive stage bodies with real traversal, substitution, bumping, selection, and reporting logic, not delete code or flip one comparison.
- RC2: fix-path packages and symbols are opaque (`pass1`-`pass5`/`Step`) and the instruction avoids them, so visible nouns do not grep to the frontier.
- RC3: the verifier compares the computed build list, held set, and preview, not schema or existence.
- RC4: expected held-out values live in the Python verifier; bundled outputs are illustrative only and tampering them cannot pass held-out tests.
- RC5: no golden output is shipped under `environment/`; only illustrative outputs for the simple catalogs and the input catalogs.
- RC6: the instruction is complete about the input format, interface, and schema but not the selection rules.
- RC7/GX3: the oracle changes five Go packages with substantive logic, well above the LOC floor.
- CR1/CR7: the construction manifest records every oracle-touched symbol and the instruction avoids those symbols.
- CR2: five distinct package roots each control a separate held-out subset, none a majority.
- CR8: only the pipeline driver runs the stages, and it references a single shared `Step` symbol name.
- GX1: no correctional comments near oracle-changed lines.
- GX9/GX10: the instruction enumerates no per-node answer rows and no contradictory polarity for any field.
- Static/Docker checks: digest-pinned Go base, pinned apt packages, tmux and asciinema, offline `tests/test.sh`, and pytest baked into the image.

### Initial Draft Commitments

- instruction.md
- task.toml
- output_contract.toml
- construction_manifest.json
- environment/Dockerfile
- environment/.dockerignore
- environment/README.md
- environment/go.mod
- environment/Makefile
- environment/docs/model.md
- environment/docs/interface.md
- environment/cmd/resolve/main.go
- environment/internal/plan/state.go
- environment/internal/plan/intake.go
- environment/internal/pipeline/run.go
- environment/pass1/pass1.go
- environment/pass2/pass2.go
- environment/pass3/pass3.go
- environment/pass4/pass4.go
- environment/pass5/pass5.go
- environment/render/render.go
- environment/tally/tally.go
- environment/banner/banner.go
- environment/data/alpha/graph.cat
- environment/data/beta/graph.cat
- environment/data/gamma/graph.cat
- environment/evidence/observed.json
- environment/scripts/run.sh
- environment/scripts/run-suite.sh
- environment/scripts/build.sh
- solution/solve.sh
- tests/test.sh
- tests/test_outputs.py
