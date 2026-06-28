### Decision
GO - Attempt 1.

- First filesystem_state_reconstruction profile and first repair_existing_system shape in the bank: a working userspace OCI image-layer flattener produces a flattened tree that diverges from a kernel overlay mount on specific layer stacks, and the solver must diagnose and repair the divergences. The two prior tasks are a Go constrained-optimization and a Rust reverse-engineering; this is the first repair.
- Hardness survives full disclosure: even with the overlay union rules and whiteout conventions documented, the residual work is locating four coupled defects across four pipeline stages (opaque masking scope, directory-whiteout subtree removal and precedence, topmost metadata copy-up, and hardlink-group preservation) in code that compiles and produces plausible output on easy stacks.
- The verifier builds layer stacks with ground truth known by construction, runs the solver, and walks the produced output tree (presence, ownership, permissions, shared inodes) on bundled and verify-time-generated stacks; no golden tree is shipped and the tamperable run report is never trusted.

### Metadata

- version: 2
- Task name: overlayfs-whiteout-flatten
- Title: Overlay Layer Flattener
- Category: system-administration
- Task shape: repair_existing_system
- Languages: ["Go", "shell"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["containers", "overlayfs", "oci-image", "filesystem", "go"]
- Milestones: 0

## Authoring Brief
This file is the drafting source for the live task under `tasks/overlayfs-whiteout-flatten/`.

### Public contract
Repair the image-layer flattener under `/app` (also reachable through the `/app/environment` alias). The flatten binary reads an ordered set of layer archives (the lexicographically-sorted `*.tar` files in a stack directory, lowest layer first) and writes a single flattened directory tree that equals what the kernel overlay filesystem would present if those layers were stacked as lower-to-upper. `bash /app/scripts/flatten-one.sh <stack-dir> <out-dir>` builds then runs the flattener on one stack; `bash /app/scripts/run-suite.sh` flattens every bundled stack under `/app/environment/testdata/stacks/` and writes `/app/output/flatten-report.json`. The shipped flattener compiles and produces a correct tree for simple stacks, but for stacks that use opaque-directory markers, directory whiteouts, the same path in several layers, or hardlinked files, the flattened tree diverges from a kernel overlay mount.

A layer archive is a tar holding regular files, directories, symlinks, the OCI per-name whiteout convention (a `.wh.<name>` entry that deletes `<name>` and its subtree as contributed by lower layers), the opaque-directory convention (a `.wh..wh..opq` entry inside a directory that hides the lower-layer contributions to that directory), and tar hardlink entries that bind two paths to one storage object within a layer. The flattened tree must: hide exactly the lower-layer contributions an opaque marker covers while keeping the marking layer's own entries and any higher-layer additions to that directory; remove a whitened path and its whole lower subtree while letting a higher layer re-create it; take each surviving path's permissions and ownership from the topmost layer that contributes it, including for directories; and materialize hardlinked files as shared inodes, excluding members that an upper layer removed or replaced. Re-running the flattener on the same stack must produce an identical tree.

The overlay union rules and whiteout conventions are documented under `/app/environment/docs`; the marker-detection helpers are implemented in a readable package the solver can study. Static or hand-written output trees are insufficient: the verifier regenerates the tree by running the solver, including on stacks not present under `/app/environment/testdata`.

### Failure topology
The shipped flattener runs a four-stage pipeline over an index it accumulates bottom-up from the layers, and each stage carries one defect that only manifests when the corresponding feature is exercised, so easy stacks look correct (a false-green that invites an early stop). The opaque stage treats a directory marker as a sticky property of the merged directory, so it suppresses not only the lower-layer contributions the marker covers but also entries the marking layer and higher layers add to that directory. The per-name whiteout stage deletes only the exact whitened path from the accumulated set, leaving its descendants orphaned in the tree, and applies whiteouts without respecting layer order so a higher re-creation is dropped. The attribute-resolution stage selects the permissions and ownership contributed by the lowest layer that provides a path rather than the topmost, so paths present in several layers (directories especially) carry stale metadata. The materialization stage dereferences hardlink groups into independent copies and, when it does link, can reference a member a higher layer removed. The four concerns are coupled: the opaque scope interacts with higher additions, subtree removal interacts with link-group membership, and copy-up interacts with re-creation, so a partial repair that fixes the obvious whiteout case still fails opaque scope, copy-up direction, and link preservation. The discriminating insight is that the canonical flattened state is determined across stages — surviving entries in the union stages, the metadata winner in attribute resolution, and shared storage in materialization — so no single stage's output is the answer, and the parity tests exercise every concern at once.

### Environment shape
One digest-pinned Go image with the Go toolchain, pytest, tmux, and asciinema. The environment contains a shared accumulated-index/node/group/stat types package; a readable whiteout-convention detector; a tar intake package that reads and classifies layer entries; a pipeline orchestrator that chains the stages; four neutral stage packages (opaque scope, per-name whiteout, attribute resolution, materialization) that the shipped build leaves defective; two or three sibling helper packages that render diagnostics, aggregate counters, and format log lines off the merge path; bundled ordered layer archives under `testdata/stacks/` that exercise every concern; shell runners; and docs describing the overlay union and whiteout conventions and the run interface. The verifier is offline, rebuilds the binary, and walks the produced tree.

### Required artifacts
Step 2b maintains `instruction.md`, `task.toml`, `construction_manifest.json`, `output_contract.toml`, `environment/Dockerfile`, environment source/archives/docs/scripts, `solution/solve.sh`, `tests/test.sh`, and `tests/test_outputs.py`. The task is single-step, single-container, non-UI, not long-context, `version = "2.0"`, and `[environment].allow_internet = false`.

### task_shape

- type: repair_existing_system
- instruction_framing: symptoms-only
- hardness_source: diagnosis
- collapse_risk: medium; mitigated by verify-time-generated stacks that defeat hardcoding, an output-tree walk that ignores the tamperable run report, a non-textbook overlay-semantics fix, and a fix frontier split across four coupled stages.

### platform_files

- path: task.toml
- role: Edition 2 metadata and runtime limits for a hard system-administration repair task; sets `[environment] allow_internet = false`.
- path: instruction.md
- role: symptoms-only public contract for the run interface, the ordered-layer input format, and overlay-mount equivalence.
- path: tests/test_outputs.py
- role: independent verifier that builds layer stacks with known ground truth, rebuilds and runs the flattener, and walks the produced output tree.
- path: tests/test.sh
- role: canonical verifier entrypoint that runs pytest and writes reward.
- path: solution/solve.sh
- role: oracle that repairs the four stage helpers and rebuilds.
- path: environment/Dockerfile
- role: digest-pinned offline Go runtime image with pytest, tmux, and asciinema.
- path: construction_manifest.json
- role: authoring metadata for fix frontier, base image, decoys, and the flipping-point contract.
- path: output_contract.toml
- role: local authoring metadata for the generated report output and schema homes.

### task_files

- path: environment/
- role: shipped Go flattener, readable marker detector, shared types, bundled layer archives, docs, and shell runners visible to the solver.
- path: solution/solve.sh
- role: oracle repair implementation used only by Harbor validation.
- path: construction_manifest.json
- role: source-of-truth metadata for collapse and approval gates.

### fix_frontier

- count: four stage helpers (one per overlay concern) plus their private callers.
- distribution: opaque masking scope, per-name whiteout precedence and subtree removal, topmost attribute copy-up, and hardlink-group materialization, each in a separate neutral package.
- naming_policy: neutral internal package directories each exposing a stable entry wrapper, with the defect localized to one opaquely named unexported helper per package; shared domain types live in a non-fix package and the whiteout-convention detector is a non-fix decoy.
- forbidden_stems: flatten, layer, whiteout, opaque, overlay, merge, metadata, ownership, permission, hardlink, link, inode, tar, stack, marker, subtree, attribute, group.
- helpers_policy: sibling helper packages render diagnostics, aggregate counters, and format log lines that rhyme with the stage helpers but never change the accumulated set or the output tree.
- symbol_thin_preferred: yes; each stage helper is one unexported function referenced only inside its own package, so no visible file references more than two fix-path symbols.

### contract_surface

- boolean_fields_max: one (`overlay_equivalent`) per report row, justified because the per-row data (entry counts, the deterministic tree digest, detected markers) carries the real evidence and the tests derive verdicts from the walked output tree, not the flag.
- direct_boolean_assertions_max: one; equivalence is checked by walking the produced tree, not by reading the report flag.
- preferred_assertion_styles: walk the flattened output tree and check entry presence and absence, stat output paths and compare permission and ownership bits to the topmost contributor, compare inode numbers and link counts to confirm shared storage, rebuild and rerun the solver on freshly generated stacks.
- forbidden_assertion_styles: golden flattened trees, static output writes, hardcoded per-stack expected digests, schema/existence-only checks, stack->path->expected boolean tables.

### category_profile

- challenge_family: union-merge reconstruction of a flattened filesystem from stacked OCI layers under overlay semantics.
- profile_name: filesystem_state_reconstruction
- allowed_instruction_disclosures: the run interface and commands, the ordered-layer input format, the OCI whiteout conventions, the requirement to match a kernel overlay mount, the preservation constraints for ownership/permissions and shared storage, and the deterministic re-run expectation.
- forbidden_instruction_leaks: the diverging stage identifiers, the cause of each divergence, the merge algorithm, per-stack expected values, and any statement of which stage controls which test.
- category_specific_hardness_bar: the canonical flattened state must be inferred from conflicting contributions across multiple layers (opaque scope, whiteout precedence, topmost copy-up, shared storage); no single stage's output is canonical because the concerns are decided in different stages that consume each other's state.
- category_specific_verifier_risks: leaking a golden flattened tree, trusting the tamperable run report instead of the output tree, coupling tests to directory iteration order, or a hidden-instance puzzle over one bundled stack.
- coverage_role: adds the first filesystem_state_reconstruction profile, the first repair_existing_system shape, and the first system-administration category task to a bank that otherwise holds a Go optimization task and a Rust reverse-engineering task.

### difficulty_mechanism_plan

- mechanisms: false_green_intermediate_states, stateful_multi_step_dependencies, deceptive_but_valid_local_evidence, cross_file_cross_format_invariants, rare_local_vocabulary.
- mechanism: false_green_intermediate_states
  placement: simple single-layer or non-conflicting stacks flatten correctly, so the tool looks finished while the defects only surface on opaque, multi-layer, or linked stacks.
  why_model_misses_it: a solver that validates on an easy stack sees a passing run and stops before exercising the multi-component interactions that fail.
  fairness_guardrail: the overlay contract and the run interface are fully documented so the solver can construct the revealing stacks itself.
- mechanism: stateful_multi_step_dependencies
  placement: the bottom-up accumulation carries opaque scope, surviving entries, the topmost contributor, and link-group membership that later stages consume.
  why_model_misses_it: repairing one stage in isolation corrupts the state a downstream stage depends on, for example fixing subtree removal without updating link-group membership, which is a multi-component state-reconstruction failure.
  fairness_guardrail: the accumulated index types and the per-stage responsibilities are visible in the codebase and docs.
- mechanism: deceptive_but_valid_local_evidence
  placement: each buggy stage emits locally plausible output: an opaque directory looks masked, attributes look set, and files look written, so per-stage inspection reads as correct.
  why_model_misses_it: a locally plausible stage passes a spot check yet violates overlay equivalence only when composed with the other stages on a tricky stack.
  fairness_guardrail: the expected composed behaviour is stated as overlay-mount equivalence, which the solver can check end to end.
- mechanism: cross_file_cross_format_invariants
  placement: the tar layer format, the in-memory accumulated index, the materialized output tree, and the run report must all agree on the same overlay semantics.
  why_model_misses_it: a partial implementation that handles one representation emits a report that round-trips but fails an output-tree walk under the independent verifier.
  fairness_guardrail: every input format detail and output expectation is documented in the instruction and environment docs.
- mechanism: rare_local_vocabulary
  placement: the OCI whiteout conventions (a per-name prefix marker and a directory opaque marker) and copy-up precedence are domain-specific conventions the solver must apply precisely.
  why_model_misses_it: a solver unfamiliar with the exact conventions mishandles the opaque marker scope or the directory-versus-file whiteout distinction.
  fairness_guardrail: the conventions are named and defined in `environment/docs/overlay-semantics.md` so they are discoverable rather than secret.
- adversarial_layers_count: five.
- fairness_guardrails: every externally checked behaviour (presence, ownership, permissions, shared inodes, determinism) is a consequence of the overlay contract stated in the instruction and docs; only the diverging stage locations and the merge algorithm are withheld.

### calibration_plan

- oracle_runs: 10
- no_op_runs: 3
- target_agent_runs: 5
- comparator_agent_runs: 5
- human_sanity: a container-tooling engineer can solve by reading the overlay-semantics doc, flattening the bundled stacks, diffing against expected overlay behaviour, and repairing opaque scope, whiteout subtree and precedence, topmost copy-up, and link-group preservation.
- shortcut_audit: tests rebuild and rerun the solver, generate fresh stacks at verify time, reject static output trees, walk the produced tree rather than trusting the run report, and reject a solver that special-cases the bundled fixtures.
- ablation_plan: revert each of the four stage helpers independently and confirm only that stage's dedicated tests plus the two parity tests fail, while the other stages' tests still pass.
- pass_rate_target: hard_max_pct=20, too_easy_threshold_pct=80, basis=stronger target agent; aligns with Part E Hard/Medium/Easy thresholds on worst/best model accuracy. The verifier is offline (pytest baked into the Dockerfile, no runtime installs under allow_internet = false) and post-upload difficulty is classified by Part E after platform agent runs.

### verifier_scoring_plan

- metrics: functional_correctness, hidden_invariants, state_hygiene, interface_correctness, deliverable_completeness.
- functional_correctness: presence and absence of entries, ownership, and permissions in the flattened tree match a kernel overlay mount on bundled and generated stacks.
- hidden_invariants: opaque masking is confined to strictly-lower layers, a directory whiteout removes the whole lower subtree, copy-up takes the topmost contributor, and storage-sharing sets become shared inodes minus removed members.
- state_hygiene: re-flattening the same stack yields an identical deterministic tree digest and the suite leaves the binary and report in place.
- interface_correctness: the flatten command and the shell runners read the documented inputs and write the documented output tree and report shape.
- deliverable_completeness: every bundled stack appears in the report with its observation fields and the output tree is fully materialized.
- overall_threshold: binary reward requires all pytest assertions to pass.
- reward_output: /logs/verifier/reward.txt.
- binary_threshold_rule: reward is 1 only on pytest exit 0; otherwise reward is 0.

### subtype_milestone_plan

- subcategories: none.
- milestone_count: 0.
- sequential_dependency: not applicable; standard single-step task.
- local_only_data: all source, archives, scripts, and docs are bundled under `/app`.
- sidecar_or_protocol_notes: `run-suite.sh` flattens the bundled stacks and writes one JSON report; verifier tests invoke the flatten binary on temporary generated stacks.

### satisfiability_risk

- rc2_planned_name_risk: low; the four stage helpers carry neutral opaque names in neutral packages and the only domain-named package is the non-fix marker-detector decoy.
- gx9_contract_risk: low; the instruction states the overlay contract and preservation rules but no per-stack expected values; expectations are recomputed from the constructed stacks.
- cr1_symbol_frontier_risk: low; the manifest fixes the four helper symbols and the oracle edits them verbatim within their own packages.
- hidden_contract_risk: low; every tested behaviour is a consequence of the overlay contract stated in the instruction and docs.

### actionability_plan

- verifier_command_visible: instruction.md names the flatten command, `bash /app/scripts/flatten-one.sh <stack-dir> <out-dir>`, `bash /app/scripts/run-suite.sh`, and the pytest verifier command.
- source_fix_intent_visible: instruction.md says the solver sources live under `/app/environment` and that writing a static output tree is insufficient because the verifier re-runs the solver on new stacks.
- generated_output_rule_visible: instruction.md identifies `/app/output/flatten-report.json` and the per-call output tree and states that stacks not under `/app/environment/testdata` are also flattened.
- exact_formula_home: instruction.md and `/app/environment/docs/overlay-semantics.md` state the whiteout conventions, opaque scope, copy-up precedence, and shared-storage preservation rule.
- schema_home: instruction.md names the input layer format and the report fields; the overlay-semantics doc carries the worked union rules.

### waiver_plan

- waivers_expected: false.
- waiver_rationale: no waiver is planned; any checker warning should be resolved or documented before packaging.

### reference_pattern

- justification_if_none: original task built from real Linux overlayfs union semantics and the OCI image-spec whiteout conventions (the per-name `.wh.` prefix and the `.wh..wh..opq` opaque marker) as implemented by userspace flatteners such as umoci and containers/storage; not derived from a website inspiration, a prior public task, or a template reskin. The reference library currently has no promoted entries.

### realism_source

- source_type: real_system
- evidence_basis: Linux overlayfs union and copy-up semantics and the OCI image-spec whiteout conventions (the per-name `.wh.` prefix whiteout and the `.wh..wh..opq` opaque-directory marker), as implemented by userspace image flatteners such as umoci and containers/storage.
- upstream_or_synthetic_rationale: the overlay union rules, whiteout conventions, copy-up precedence, and hardlink preservation are taken from the kernel overlayfs documentation and the OCI image-spec; the specific layer stacks are synthetic to keep all data local and deterministic.
- minimization_preserves: opaque masking confined to strictly-lower layers, directory-whiteout subtree removal and layer-confined precedence, topmost-contributor metadata copy-up including for directories, and tar hardlink-group preservation as shared inodes.
- synthetic_exception_review: not a synthetic exception; the semantics are drawn from real subsystems and a real image-format spec, and only the layer stacks and thresholds are generated.

### Test plan
- `test_t01`: an opaque marker hides the lower-layer contributions to its directory. Multiple approaches: yes. Chain-dependent: no.
- `test_t02`: an opaque marker keeps the entries the marking layer itself provides in that directory. Multiple approaches: yes. Chain-dependent: no.
- `test_t03`: an opaque marker does not suppress entries that higher layers add to that directory. Multiple approaches: yes. Chain-dependent: no.
- `test_t04`: a per-name whiteout removes the whitened path and its whole lower subtree, leaving no orphaned descendants. Multiple approaches: yes. Chain-dependent: no.
- `test_t05`: a path whitened in one layer and re-created in a higher layer is present with the higher layer's content. Multiple approaches: yes. Chain-dependent: no.
- `test_t06`: a whiteout only affects layers below its origin, so a lower whiteout does not remove a higher contribution. Multiple approaches: yes. Chain-dependent: no.
- `test_t07`: a file present in several layers takes the topmost layer's permission and ownership bits. Multiple approaches: yes. Chain-dependent: no.
- `test_t08`: a directory present in several layers takes the topmost layer's permission and ownership bits. Multiple approaches: yes. Chain-dependent: no.
- `test_t09`: a path re-created in a higher layer after a whiteout takes the re-creating layer's permission bits, not a stale lower layer's. Multiple approaches: yes. Chain-dependent: no.
- `test_t10`: two paths bound to one storage object within a layer materialize as shared inodes with a link count of at least two. Multiple approaches: yes. Chain-dependent: no.
- `test_t11`: when a higher layer removes one member of a storage-sharing set, the surviving members remain shared and the removed member is absent. Multiple approaches: yes. Chain-dependent: no.
- `test_t12`: when a higher layer replaces one member of a storage-sharing set with new content, that path is an independent object and the untouched members stay shared. Multiple approaches: yes. Chain-dependent: no.
- `test_t13`: every bundled stack flattened through `run-suite.sh` matches expected overlay behaviour on presence, ownership, permissions, and shared inodes. Multiple approaches: yes. Chain-dependent: yes (whole pipeline).
- `test_t14`: a seeded batch of freshly generated stacks each flatten to an overlay-equivalent tree and re-flatten to an identical digest (generalization and determinism). Multiple approaches: yes. Chain-dependent: yes (whole pipeline).

### Drafting guardrails
The instruction should read like a bug report to a container-tooling engineer, not a recipe. State the run interface, the ordered-layer input format, the whiteout conventions, the requirement to match a kernel overlay mount, the preservation constraints, and the deterministic re-run rule. Describe the observable divergences (entries that should be hidden remain, entries that should remain are missing, some paths carry the wrong ownership or permissions, and some files that share storage are emitted as independent copies) without naming the diverging stages, the cause of each divergence, the merge algorithm, per-stack numbers, or which stage controls which test. Tests construct their own stacks and recompute every expectation by walking the produced tree; no golden tree or report is shipped.

### Triviality Ledger
- Sticky-opaque trap: keeping the opaque flag on the merged directory drops higher-layer additions; blocked by `test_t03` and the parity tests checking upper additions survive.
- Exact-path whiteout trap: deleting only the whitened path leaves orphaned descendants; blocked by `test_t04` walking the subtree.
- Order-insensitive whiteout trap: applying whiteouts globally drops a higher re-creation; blocked by `test_t05`/`test_t06`.
- Bottom-layer metadata trap: taking the lowest contributor's attributes leaves stale ownership/permissions; blocked by `test_t07`/`test_t08`/`test_t09` statting the output against the topmost layer.
- Dereferenced-link trap: writing independent copies breaks shared storage; blocked by `test_t10`/`test_t11`/`test_t12` comparing inode numbers.
- Hardcoding trap: memorizing the bundled stacks fails on verify-time-generated stacks; blocked by `test_t14`.
- Tamper trap: faking the run report does not help; blocked because the verifier walks the produced output tree, not the report.

### Per-gate Pitfall Inventory
- RC1: the oracle rewrites four substantive stage-helper bodies (adds merge logic), it does not delete or revert flags.
- RC2: stage packages and files are neutral (`sift`/`cull`/`vouch`/`braid`); no broken/golden/expected tokens on visible surfaces.
- RC3: tests assert walked-tree presence, ownership, permissions, and shared inodes, not schema/existence alone.
- RC4: the verifier walks the produced output tree and never trusts the run report the agent could rewrite.
- RC5: no golden flattened tree or report fixtures; expected values are computed in test code from the constructed stacks.
- RC6: instruction is symptoms-only; it withholds the cause, the stage locations, and the merge algorithm.
- RC7/A16: the oracle is four real stage-helper repairs, above the LOC floor.
- CR1/CR7: the manifest fixes the four helper symbols; instruction nouns are kept off the fix-path symbols and the only domain-named package is the non-fix marker detector.
- CR2: four locations, each controlling a minority test subset (5/14); no single stage flips a majority.
- CR8: stage helpers are referenced only inside their own packages, so no visible file references more than two fix-path symbols.
- GX1: no intent/correctional comments near oracle-edited lines.
- GX9/GX10: no per-stack answer table and no polarity contradiction; the one report boolean is described once with numeric evidence beside it.
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
- `environment/cmd/flatten/main.go`
- `environment/internal/model/types.go`
- `environment/internal/oci/markers.go`
- `environment/internal/intake/read.go`
- `environment/internal/intake/classify.go`
- `environment/internal/pipeline/run.go`
- `environment/sift/sift.go`
- `environment/cull/cull.go`
- `environment/vouch/vouch.go`
- `environment/braid/braid.go`
- `environment/internal/tarx/archive.go`
- `environment/internal/tally/tally.go`
- `environment/internal/sketch/sketch.go`
- `environment/internal/scribe/scribe.go`
- `environment/docs/architecture.md`
- `environment/docs/overlay-semantics.md`
- `environment/docs/operations.md`
- `environment/scripts/build.sh`
- `environment/scripts/flatten-one.sh`
- `environment/scripts/run-suite.sh`
- `environment/scripts/clean.sh`
- `environment/testdata/stacks/alpha/00.tar`
- `environment/testdata/stacks/alpha/01.tar`
- `environment/testdata/stacks/alpha/02.tar`
- `environment/testdata/stacks/beta/00.tar`
- `environment/testdata/stacks/beta/01.tar`
- `environment/testdata/stacks/beta/02.tar`
- `environment/testdata/stacks/gamma/00.tar`
- `environment/testdata/stacks/gamma/01.tar`
- `environment/testdata/stacks/gamma/02.tar`
- `environment/testdata/stacks/delta/00.tar`
- `environment/testdata/stacks/delta/01.tar`
- `environment/testdata/stacks/epsilon/00.tar`
- `environment/testdata/stacks/epsilon/01.tar`
- `environment/testdata/stacks/epsilon/02.tar`
- `solution/solve.sh`
- `tests/test.sh`
- `tests/test_outputs.py`

### Construction manifest (BLOCKING - Step 2b must follow this verbatim)

#### symbol_table
```
- path: sift/sift.go
  symbol: narrow
  kind: function
  signature: func narrow(a *model.Index, lv int)
  purpose: restricts a directory marker so it suppresses only contributions from levels below the one that declared it
- path: cull/cull.go
  symbol: reap
  kind: function
  signature: func reap(a *model.Index, lv int, p string)
  purpose: removes a path and its whole descendant range from the accumulated set when a lower level is suppressed at the given level
- path: vouch/vouch.go
  symbol: settle
  kind: function
  signature: func settle(n *model.Node) model.Stat
  purpose: selects the attribute record contributed by the highest level that provides the node
- path: braid/braid.go
  symbol: knit
  kind: function
  signature: func knit(g *model.Bundle, dst string) error
  purpose: materializes a storage-sharing set as one backing object plus additional references for the surviving members
```

#### flipping_point_contract
```
locations:
  - id: A
    path: sift/sift.go
    controls_tests: [test_t01, test_t02, test_t03, test_t13, test_t14]
  - id: B
    path: cull/cull.go
    controls_tests: [test_t04, test_t05, test_t06, test_t13, test_t14]
  - id: C
    path: vouch/vouch.go
    controls_tests: [test_t07, test_t08, test_t09, test_t13, test_t14]
  - id: D
    path: braid/braid.go
    controls_tests: [test_t10, test_t11, test_t12, test_t13, test_t14]
no_single_location_flips_majority: true
concentration_cap: 0.5
```

#### decoy_manifest
```
- path: internal/tally/tally.go
  kind: helper
  rhymes_with: narrow
  non_fix_purpose: aggregates per-level entry counters for the run report only and never changes the accumulated set
- path: internal/sketch/sketch.go
  kind: helper
  rhymes_with: settle
  non_fix_purpose: renders an ASCII view of the accumulated index for dry-run console output
- path: internal/scribe/scribe.go
  kind: helper
  rhymes_with: knit
  non_fix_purpose: formats diagnostic log lines for the suite runner off the materialization path
```
