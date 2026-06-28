### Decision
GO - Attempt 4.

- First temporal-data task in the bank and the first binary-serialization reverse-engineering challenge: the solver must make a two-axis reference-data engine reproduce SQL:2011/XTDB bitemporal materialization, where a correction to the application-axis past is gated by the revision at which it was recorded, and re-serialize a canonical store across a binary and a text form.
- Hardness survives full disclosure: even with the binary byte layout, the text schema, the offset-index relationship, the query meaning, and the canonical/minimal/idempotent/bijection/no-future-leak properties all stated, the recorded-order supersession key, the derived recorded-axis upper bound, the per-sub-interval split, the coalescing least fixpoint, and the two-axis withdrawal effect stay withheld. A whole-record, file-order, single-pass materializer is exactly the wrong model and is what the bundled samples reward.
- The verifier is anchored on the file-format-serialization family, not a full reimplementation: a thin definitional point oracle plus decomposition-invariant step-function comparison, byte-stable round-trip idempotency, an offset-index integer relationship, binary<->text bijection, and an oracle-free cross-truncation metamorphic invariant, all over verify-time held-out stores (no hardcoding); any program matching the period-table semantics passes (outcome-verified).

### Metadata

- version: 2
- Task name: bitemporal-asof-correction
- Title: Revision-Aware Reference Store
- Category: data-processing
- Task shape: reverse_engineering
- Languages: ["Go", "shell"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["go", "bitemporal", "serialization", "temporal-data", "reverse-engineering"]
- Milestones: 0

## Authoring Brief
This file is the drafting source for the live task under `tasks/bitemporal-asof-correction/`.

### Public contract
Change the reference-data engine under `/app/environment` (also reachable through `/app`) so it correctly materializes and serializes a two-axis reference-data store. The engine is a single Go binary driven by shell wrappers. `bash /app/environment/scripts/run.sh pack <log.rdx> <out.rdx>` reads an append-order binary store (layout 0) and writes the canonical materialized store (layout 1) with a strictly increasing record offset index; `bash /app/environment/scripts/run.sh probe <store.rdx> <key> <point> <rev>` prints the integer value that applies at span coordinate `point` according to what was recorded as of revision `rev`, or `<none>`; `bash /app/environment/scripts/run.sh emit <store.rdx> <out.jsonl>` and `bash /app/environment/scripts/run.sh absorb <in.jsonl> <out.rdx>` convert between the canonical binary and text forms; `bash /app/environment/scripts/run-suite.sh` materializes every bundled store under `/app/environment/inputs/` and writes a per-case JSON report to the engine's generated report path. The shipped engine builds and runs but is wrong: it folds records in file order, supersedes whole records instead of splitting on partial span overlap, makes a single forward pass with no fixpoint, and treats a withdrawal as a whole-record delete, so it agrees with the bundled samples yet diverges from the period-table semantics.

Each record carries a key, a half-open span interval `[spanLo, spanHi)` over which the fact applies, a recorded-revision lower bound, an append tie-break, an op (set or clear), and (for set) an integer value; the recorded-revision upper bound is not stored. The binary byte layout, the offset-index relationship, the text schema, the error behavior, and the canonical/minimal/idempotent/bijection/no-future-leak properties are described in `/app/environment/docs/format.md`, and the conceptual two-axis model in `/app/environment/docs/model.md`. `/app/environment/evidence/observed.rdx`, `observed.jsonl`, and `observed.probe.json` show a few illustrative outputs for easy cases so the schema and the easy cases are anchored; they are evidence, not the full contract. Static or hand-written output files are insufficient: the verifier regenerates output by running the solver's program, including on stores not present under `/app/environment/inputs`.

### platform_files

- path: task.toml
- role: Edition 2 metadata and runtime limits for a hard data-processing Go task; sets `[environment] allow_internet = false`.
- path: instruction.md
- role: behavioral-target public contract for the binary/text byte format, the run interface, the query meaning, and the canonical/idempotent/bijection target.
- path: output_contract.toml
- role: local authoring metadata declaring the materialized store and report outputs and their schema homes.
- path: construction_manifest.json
- role: authoring metadata for the fix frontier, base image, decoys, and flipping-point contract.
- path: environment/Dockerfile
- role: digest-pinned offline Go image with the toolchain, pytest, tmux, and asciinema.
- path: tests/test.sh
- role: canonical offline verifier entrypoint that runs pytest and writes reward.
- path: tests/test_outputs.py
- role: file-format-serialization verifier (thin point oracle plus round-trip, offset-index, cross-format, and cross-truncation invariants) over bundled and held-out stores.
- path: solution/solve.sh
- role: oracle that writes the five engine pass bodies and rebuilds; used only for validation.

### task_files

- path: environment/
- role: the Go engine (shared core codec, cli pipeline, five opaque passes, helper packages), bundled append-order binary stores, the format and model docs, illustrative samples, and shell runners visible to the solver.
- path: environment/inputs/
- role: bundled append-order binary stores materialized by the engine; development inputs, not answer keys.
- path: solution/solve.sh
- role: oracle implementation used only by Harbor validation.

### fix_frontier

- count: five engine passes.
- distribution: boundary algebra (align), recorded-axis upper-bound derivation (reach), recorded-order selection (rank), partial-overlap span splitting (cleave), and coalescing least fixpoint plus withdrawal and canonical encode (knit), one concern per opaque package.
- naming_policy: opaque package dirs `align`, `reach`, `rank`, `cleave`, `knit`, each exposing a single `Step` entry over shared neutral `core` types; the instruction names neither the packages nor the entry symbols.
- forbidden_stems: instruction nouns such as span, revision, recorded, point, materialized, canonical, sentinel, grade, rating, counterparty, and interchange stay off fix-path symbol, parameter, path, and constant names.
- helpers_policy: sibling helper packages `tally`, `digestx`, and `render` do counting, CRC, and formatting work for the stats and report views and never touch the materialized tiles.
- symbol_thin_preferred: yes; each pass stays in its own package with one entry function.

### contract_surface

- boolean_fields_max: 0; the output is per-record interval/value tiles and integer answers, not status booleans.
- direct_boolean_assertions_max: 0; checks compare recomputed integer answers, decomposition-invariant step functions, byte digests, and integer index relationships rather than boolean verdict fields.
- preferred_assertion_styles: recompute point answers with a thin definitional oracle and compare integers; compare the emitted relation as a step-function over the breakpoint grid (decomposition-invariant); assert oracle-free metamorphic invariants (cross-truncation monotonicity, pack idempotency, binary<->text bijection bytes); assert the offset-index integer relationship and contiguous recorded-axis tiling from the decoded store only.
- forbidden_assertion_styles: golden materialized store shipped under environment, static or hardcoded per-key answers, schema-only or existence-only checks, scenario→coordinate→expected boolean tables, copying the illustrative samples into expected outputs, and trusting the engine's own probe output as ground truth.

### task_shape

- type: reverse_engineering
- instruction_framing: behavioral-target with the binary/text byte layout, the offset-index relationship, the run/query interface, the query meaning, the canonical/idempotent/bijection/no-future-leak properties, and illustrative samples disclosed while the materialization algorithm is withheld.
- hardness_source: semantic inference of the exact two-axis materialization function from the byte format, the conceptual model, and the deceptive samples, plus generalization to held-out stores.
- collapse_risk: medium; mitigated by a thin definitional oracle plus decomposition-invariant and oracle-free metamorphic checks, fresh-entropy held-out stores, deceptive full-coverage samples, a non-textbook compound requirement, and a five-pass fix frontier with no single location controlling a test majority.

### category_profile

- challenge_family: reverse-engineering a two-axis reference-data store's serialization-and-materialization semantics.
- profile_name: file_format_serialization
- allowed_instruction_disclosures: the binary and text byte layouts, the offset-index relationship, the run/query interface and commands, the query meaning, the canonical/minimal/idempotent/bijection/no-future-leak properties, error behavior, and a few illustrative observed outputs.
- forbidden_instruction_leaks: the recorded-order supersession key, the derived recorded-axis upper bound, the per-sub-interval splitting rule, the coalescing least fixpoint, the two-axis withdrawal effect, the engine pass identifiers, and any per-key expected value.
- category_specific_hardness_bar: the materialized relation derives across boundary algebra, recorded-order visibility, partial-overlap splitting, and a coalescing fixpoint; no single record or pass suffices and a local choice changes distant lookups and the canonical byte layout.
- category_specific_verifier_risks: spec transcription, a leaked golden store, a one-pass shortcut passing the samples, boolean per-case verdict fields, and sample-overfit acceptance.
- coverage_role: adds the first temporal-data (bitemporal as-of) task and the first binary serialization/round-trip reverse-engineering challenge, distinct from the existing build-toolchain, cgroup-allocation, and overlay-flatten tasks.

### difficulty_mechanism_plan

- mechanisms: deceptive_but_valid_local_evidence, cross_file_cross_format_invariants, stateful_multi_step_dependencies, false_green_intermediate_states, buried_local_constraints.
- adversarial_layers_count: five.
- fairness_guardrails: every externally tested byte field, command, query argument, output shape, and the canonical/idempotent/bijection/no-future-leak target is visible; only the materialization algorithm is withheld.
- mechanism: deceptive_but_valid_local_evidence
  placement: the bundled `inputs/` stores and `evidence/observed.*` contain only changes that fully cover the prior span or are forward-only and are probed as-of-current, plus one lure recorded over a past span whose only sampled lookup is after the change.
  why_model_misses_it: the whole-record shipped engine reproduces every sample byte-for-byte and answer-for-answer, so the solver's natural self-checks are all green and steer toward whole-record supersession.
  fairness_guardrail: the instruction states the samples are illustrative evidence, not the contract, and that held-out stores are checked, so every divergence axis is reachable by inference from the disclosed surface.
- mechanism: cross_file_cross_format_invariants
  placement: the binary store, the text interchange, the offset index, the Go engine, and the independent verifier must agree on the same two-axis semantics and the bijective canonical forms.
  why_model_misses_it: a partial implementation emits a store that parses and round-trips through the schema yet disagrees with the recomputed point answers and the cross-format and offset-index invariants.
  fairness_guardrail: every byte field, the text schema, the offset-index relationship, and the bijection property are disclosed in instruction.md and docs/format.md.
- mechanism: stateful_multi_step_dependencies
  placement: the derived recorded-axis upper bound depends on which later record supersedes over an overlapping span sub-interval, which depends on the split, which depends on recorded order; a change-of-a-change must settle.
  why_model_misses_it: computing the upper bound or the supersession in a single forward pass, before splitting fragments a wide record, mis-nests deep chains.
  fairness_guardrail: the dependency is observable by running the engine on stores with chains and earlier-revision lookups, the canonical/idempotent property is disclosed, and depth>=3 makes the fixpoint genuinely required.
- mechanism: false_green_intermediate_states
  placement: an engine implementing four of five passes emits a store that round-trips through the schema and passes the bundled samples and the forward-only control while still failing held-out splitting, ordering, or fixpoint families.
  why_model_misses_it: schema-valid, sample-passing output reads as success; the shortfall only surfaces against the recomputed answers and metamorphic invariants on fresh stores.
  fairness_guardrail: the instruction states results are checked on stores beyond `inputs/` via recomputed answers and the round-trip, offset-index, cross-format, and cross-truncation invariants.
- mechanism: buried_local_constraints
  placement: the half-open convention on both axes, the open-supremum sentinel, and the no-future-leak property live in docs/format.md and the disclosed properties, not as a recipe in the instruction.
  why_model_misses_it: a solver that ignores the half-open boundary or the recorded-order gate produces off-by-one edges and future-leaking earlier-revision lookups.
  fairness_guardrail: the conventions and properties are documented in readable format and model docs the solver may study and the stores are small enough to inspect fully.

### calibration_plan

- oracle_runs: 3
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: an engineer who knows bitemporal/period-table materialization can solve it by reading docs/format.md and docs/model.md, building the breakpoint grid, deriving recorded-axis bounds by recorded order, splitting on partial overlap, iterating to the coalesced fixpoint, and handling withdrawals, self-checking against the illustrative samples.
- shortcut_audit: tests regenerate output by running the program, build fresh-entropy held-out stores at verify time, reject static or hardcoded outputs, recompute point answers with a thin independent oracle, never trust the engine's own probe for ground truth, and include a lure sample so sample-copying and whole-record supersession both fail.
- ablation_plan: stub each of the five engine passes independently and confirm at least one held-out family fails for that pass only, and that no single pass flips a test majority (concentration_cap 0.5).
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=stronger target agent aligned with Part E worst/best-model thresholds; the verifier is offline (pytest baked into the Dockerfile, no runtime installs under `allow_internet = false`) and post-upload difficulty is classified by Part E after platform agent runs; recall-collapse risk means worst-model<=20% is treated as unconfirmed until the mandatory frontier-agent run.

### verifier_scoring_plan

- metrics: functional_correctness=0.45, hidden_invariants=0.25, state_hygiene=0.15, interface_correctness=0.10, deliverable_completeness=0.05.
- functional_correctness: recomputed point answers match the program over a stratified grid of as-of-current, as-of-at-change, and earlier-revision coordinates on bundled and held-out stores.
- hidden_invariants: cross-truncation monotonicity (earlier-revision answers are invariant under later records), pack idempotency, and binary<->text bijection hold on held-out stores.
- state_hygiene: re-running pack and emit yields byte-identical output and the suite leaves the binary and bundled data in place.
- interface_correctness: the documented run and suite commands read the documented inputs and emit the documented binary, text, and report shapes.
- deliverable_completeness: the materialized store carries a strictly increasing offset index covering every record and every bundled store is materialized by the suite.
- overall_threshold: 0.999
- reward_output: reward.txt
- binary_threshold_rule: reward is 1 only on pytest exit 0; otherwise reward is 0.

### subtype_milestone_plan

- subcategories: []
- milestone_count: 0
- sequential_dependency: not applicable; standard single-step task.
- local_only_data: true
- sidecar_or_protocol_notes: bundled append-order binary stores and the observed-sample files are local development evidence; the verifier emits authored held-out stores and fresh-entropy generated stores at verify time, all offline.

### satisfiability_risk

- rc2_planned_name_risk: low; engine passes are neutral `align`/`reach`/`rank`/`cleave`/`knit`, helpers are `tally`/`digestx`/`render`, and the instruction nouns stay off all fix-path symbols, paths, and constants.
- gx9_contract_risk: low; the instruction states the format and properties and shows a few illustrative outputs but no per-key answer key, and expectations are recomputed on held-out stores.
- cr1_symbol_frontier_risk: low; the construction manifest fixes the five `Step` symbols and the oracle modifies only those packages.
- hidden_contract_risk: low; every tested byte field, command, query argument, and property is disclosed in instruction.md or docs/format.md.

### actionability_plan

- verifier_command_visible: instruction.md names `run.sh pack/probe/emit/absorb`, `run-suite.sh`, and that the harness runs `pytest` over an offline verifier.
- source_fix_intent_visible: instruction.md says the engine source under `/app/environment` must be changed and that static or hand-written outputs are insufficient.
- generated_output_rule_visible: instruction.md states the materialized store and answers are regenerated by running the program, including on stores not present under `/app/environment/inputs`.
- exact_formula_home: the conceptual two-axis model lives in `/app/environment/docs/model.md` and the disclosed properties in instruction.md and `docs/format.md`; the precise derivation is inferable and held-out-enforced, not stated as a recipe.
- schema_home: instruction.md and `docs/format.md` name every binary field and the text schema, and `evidence/observed.*` shows one concrete example of each form.

### waiver_plan

- waivers_expected: false
- waiver_rationale: no waiver is planned; any checker warning should be resolved or documented before packaging.

### reference_pattern

- justification_if_none: Original task built from real bitemporal data semantics (SQL:2011 system-versioned plus application-time period tables with FOR PORTION OF row splitting, and XTDB/Crux document bitemporality with valid-time plus transaction-time and backdated corrections invisible to earlier transaction-time reads), minimized into a local deterministic Go engine with a compact binary store, a text interchange, bundled append-order stores, and verify-time held-out stores. Not derived from a website task-inspiration, a prior public task, or a reskin of the existing cargo-feature-unification, cgroup-budget-solver, or overlayfs-whiteout-flatten tasks; the verifier family (binary round-trip, offset-index, cross-format bijection, cross-truncation metamorphic invariants) and the mechanic (a correction to the application-axis past gated by the revision at which it was recorded) are both distinct from those tasks. The reference library currently has no promoted entries, so no reference_task_id applies.

### realism_source

- source_type: real_system
- evidence_basis: SQL:2011 temporal tables (system-versioned rows with a transaction-time period and application-time period tables whose FOR PORTION OF updates split application-time rows) and XTDB/Crux document bitemporality (valid-time plus transaction-time with as-of queries where backdated corrections are invisible to earlier transaction-time reads).
- upstream_or_synthetic_rationale: the two-axis semantics come directly from a real, widely-used standard and database family; only the specific stores, the compact binary layout, and the opaque engine scaffold are authored to keep the task local, offline, and deterministic.
- minimization_preserves: the recorded-revision-gated correction of the application-axis past, the derived recorded-axis upper bound, per-sub-interval splitting on partial overlap, the coalescing least fixpoint, and the two-axis withdrawal/re-issue behavior.
- synthetic_exception_review: not a synthetic exception; the model and rules are drawn from a real standard and database family and only the instances are authored.

### Failure topology
The shipped engine parses the binary store and emits a materialized store by folding records in physical file order: for each new record it closes the recorded-axis life of every live record whose span overlaps the new one as a whole rectangle, emits the new record, makes a single forward pass with no fixpoint, treats a withdrawal as a whole-record delete for all revisions, and does no equal-value coalescing. That output parses, round-trips through the schema, and matches the bundled `observed.*` samples — which were chosen so that every change fully covers the prior span or is forward-only and every probe is as-of-current — so it reads as correct. The five concerns are genuinely coupled. Whether a record's recorded-axis upper bound is finite or open depends on which later record supersedes it over an overlapping span sub-interval, which depends on the split, which depends on recorded order; separating a partial overlap into the overlapped and surviving sub-intervals changes which earlier-revision lookups see the prior value, which changes where the recorded-slab boundaries fall, which changes coalescing and the canonical byte layout. A change-of-a-change must settle to a least fixpoint that a single forward pass mis-nests. Any partial implementation that handles some concerns but not all stays green on the samples and the forward-only control while diverging from the period-table semantics on the held-out stores, where the verifier recomputes the expected answers independently and checks the round-trip, offset-index, cross-format, and cross-truncation invariants.

### Environment shape
One digest-pinned Go image with the toolchain, pytest, tmux, and asciinema. The engine is a small Go module: a shared `core` package with the neutral two-axis record/tile/interval types, the binary codec (layout 0/1 reader and writer, LEB128 key/value, fixed-width interval fields, the open-supremum sentinel, the offset-index builder), the canonical text codec, and one generic close-and-split interval primitive; a `cli` package with the entrypoint and a thin pipeline that dispatches pack/probe/emit/absorb and run-suite through the five passes in order; five opaque pass packages that the shipped build leaves as naive pass-through stubs; and three sibling helper packages that do counting, CRC, and formatting off the materialization path. Alongside the engine, `inputs/` holds several bundled append-order binary stores, `docs/` describes the byte format and the conceptual model, `evidence/observed.*` carries the illustrative samples, and `scripts/` holds the run and suite runners. The verifier is offline and invokes the engine's run command on bundled and held-out stores.

### Required artifacts
Step 2b creates `instruction.md`, `task.toml` (`version = "2.0"`, `[environment] allow_internet = false`), `output_contract.toml`, `construction_manifest.json`, `environment/Dockerfile`, the Go engine source, the bundled binary stores, the format and model docs, the illustrative samples, the shell runners, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. The task is single-step, single-container, non-UI, not long-context, with at least 20 non-Docker files under `environment/`. The verifier deps (pytest) are baked into the Dockerfile; `tests/test.sh` runs offline with no apt/pip/curl/uv at runtime.

### Test plan
At least sixteen held-out checks (plus a deterministic re-run and an anti-vacuity control), each recomputed by the thin independent oracle or asserted as an oracle-free invariant against fresh stores, none reading a golden file:
- tcase_edge_halfopen_membership: probes exactly at span and recorded-axis edges to force half-open membership. Multiple approaches: yes. Chain-dependent: no.
- tcase_forward_only_baseline: forward, non-overlapping records probed as-of-current; an anti-vacuity control that passes the naive engine too. Multiple approaches: yes. Chain-dependent: no.
- tcase_prior_cut_lookup: single full-cover change probed at a revision before it. Multiple approaches: yes. Chain-dependent: no.
- tcase_log_order_interleaved: physical file order differs from recorded order. Multiple approaches: yes. Chain-dependent: no.
- tcase_partial_overlap_survivor_current, tcase_partial_overlap_survivor_prior: partial span overlap, probe the surrounding surviving region as-of-current and as-of-earlier. Multiple approaches: yes. Chain-dependent: no.
- tcase_chain_depth_two, tcase_chain_depth_three: change-of-a-change over nested spans probed across revision slabs; depth three forces a true least fixpoint. Multiple approaches: yes. Chain-dependent: yes.
- tcase_withdrawal_gap_prior_vs_current, tcase_withdrawal_then_reissue: a withdrawal probed earlier (prior value) vs current (none), and a withdrawal then a later set resurrecting coverage. Multiple approaches: yes. Chain-dependent: yes.
- tcase_pack_idempotent_bytes: pack(pack(store)) is byte-identical. Multiple approaches: yes. Chain-dependent: no.
- tcase_truncation_monotone: probe(store) equals probe(truncate(store, rev)) over the grid, oracle-free. Multiple approaches: yes. Chain-dependent: no.
- tcase_straddle_each_entry: for every injected change, just-before vs just-after probes differ and match the oracle. Multiple approaches: yes. Chain-dependent: partial.
- tcase_offset_index_integrity: index entries equal decoded byte starts, strictly increasing, header consistent. Multiple approaches: no. Chain-dependent: no.
- tcase_text_binary_bijection: absorb(emit(pack(store))) re-packed equals pack(store) bytes; probe agreement across binary and text. Multiple approaches: yes. Chain-dependent: no.
- tcase_structural_tiling: per covered span coordinate the recorded-axis intervals tile contiguously to the sentinel with no overlap, from the decoded store only. Multiple approaches: yes. Chain-dependent: no.
- tcase_comprehensive_all: every mechanism at once; full probe grid plus step-function relation equality plus cross-truncation plus bijection. Multiple approaches: yes. Chain-dependent: yes.
- tcase_determinism_byte_identical: pack and emit run twice are byte-identical. Multiple approaches: yes. Chain-dependent: no.

### Drafting guardrails
The instruction must read as a behavioral reverse-engineering task, not a recipe. It must disclose the binary and text byte layouts, the offset-index relationship, the run/query interface, the query meaning, and the canonical/minimal/idempotent/bijection/no-future-leak properties, but must not state the recorded-order supersession key, the derived recorded-axis upper bound, the per-sub-interval split, the coalescing least fixpoint, or the two-axis withdrawal effect, and must not name the engine passes or any per-key expected value. Tests must generate fresh held-out stores and recompute expected answers independently or assert oracle-free invariants, never compare a shipped golden store. Keep instruction nouns off fix-path symbol, parameter, path, and constant names; helper packages must do genuine non-fix work.

### Triviality (Avoidance) Ledger

- Whole-record, file-order, single-pass materializer: passes the full-coverage, forward-only `observed.*` samples but fails held-out partial-overlap, interleaved-order, chain, and withdrawal families because the verifier recomputes against the period-table semantics on fresh stores.
- Sample-copy shortcut: blocked by fresh-entropy held-out stores the samples never cover and a contradictory lure sample.
- Single-pass fixpoint omission: blocked because a change-of-a-change only nests correctly at depth>=3 once the least fixpoint settles, so a non-fixpoint pass diverges on tcase_chain_depth_three.
- Single-axis collapse shortcut: blocked by tcase_prior_cut_lookup, tcase_truncation_monotone, and tcase_straddle_each_entry, which require earlier-revision answers to be invariant under later records.
- One-pass fix: blocked by the flipping-point contract — each of the five packages controls a distinct held-out subset and no single package controls a test majority.
- Static-output trap: blocked because the verifier regenerates output by running the solver's program on stores outside `/app/environment/inputs`.

### Per-gate Pitfall Inventory

- RC1: the oracle must implement five substantive pass bodies (boundary algebra, recorded-axis derivation, recorded-order selection, splitting, fixpoint/coalesce/encode), not remove code or flip a flag.
- RC2: fix-path packages and symbols are opaque (`align`/`reach`/`rank`/`cleave`/`knit`, `Step`) and the instruction avoids them, so visible nouns do not grep to the frontier.
- RC3: the verifier compares domain-correct recomputed answers and decomposition-invariant step functions, not schema or existence.
- RC4: expected held-out answers are recomputed in the Python verifier; bundled samples are deceptive evidence only and tampering them cannot pass held-out checks.
- RC5: no golden materialized store is shipped under `environment/`; only full-coverage illustrative samples and append-order inputs.
- RC6: the instruction is complete about the byte format, interface, and properties but not the materialization algorithm.
- RC7/GX3: the oracle changes five Go packages with substantive propagation logic and a fixpoint, well above the LOC floor.
- CR1/CR7: the construction manifest records every oracle-touched symbol and the instruction avoids those symbols.
- CR2: five distinct package roots each control a separate held-out subset.
- GX1: no correctional comments near oracle-changed lines; the shipped stub comments are neutral.
- GX9/GX10: the instruction enumerates no per-key answer rows and no contradictory polarity for any field.
- Static/Docker checks: digest-pinned canonical Go base, pinned apt packages, tmux and asciinema, offline `tests/test.sh`, and pytest baked into the image.

### Initial Draft Commitments

- instruction.md
- task.toml
- output_contract.toml
- construction_manifest.json
- environment/Dockerfile
- environment/.dockerignore
- environment/README.md
- environment/go.mod
- environment/docs/format.md
- environment/docs/model.md
- environment/docs/interface.md
- environment/core/types.go
- environment/core/codec.go
- environment/core/text.go
- environment/core/seal.go
- environment/cli/main.go
- environment/cli/pipeline.go
- environment/align/align.go
- environment/reach/reach.go
- environment/rank/rank.go
- environment/cleave/cleave.go
- environment/knit/knit.go
- environment/tally/tally.go
- environment/digestx/digestx.go
- environment/render/render.go
- environment/inputs/forward_a/in.rdx
- environment/inputs/cover_b/in.rdx
- environment/inputs/lure_c/in.rdx
- environment/evidence/observed.rdx
- environment/evidence/observed.jsonl
- environment/evidence/observed.probe.json
- environment/scripts/run.sh
- environment/scripts/run-suite.sh
- environment/scripts/build.sh
- solution/solve.sh
- tests/test.sh
- tests/test_outputs.py
