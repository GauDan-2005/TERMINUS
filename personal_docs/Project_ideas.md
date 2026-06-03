# Project Ideas

Legend: **✅** = implemented in `tasks/` with oracle, verifier, Step 2b preflight complete, and a validated submission zip in `Task_Ready_To_Submit/`.

---

## 1. system-administration

### ✅ staged-snapshot-drift

- **Languages:** Go, shell, C
- **Idea:** A local snapshot/restore daemon produces restored trees that differ from source only after restart + quota rollover + hardlink-heavy datasets.
- **Hardness hook:** Solver must discover restore drift across Go staging logic, native filesystem measurement, hardlink groups, and quota-period accounting.

**Rubrics**

- Agent runs the snapshot matrix command and inspects the generated restore audit before editing code, +3
- Agent investigates the Go snapshot implementation and native filesystem measurement path instead of only changing shell wrappers, +5
- Agent repairs restart-sensitive row replay so restored trees reach the same final contents as their sources, +5
- Agent repairs hardlink identity handling so restored hardlink groups match source hardlink groups, +5
- Agent repairs accounting output so path, bytes, and period records match the source tree, including hardlink names and quota-period cases, +5
- Agent validates all six audit cases through the documented matrix output after making code changes, +3
- Agent hardcodes expected restore audit JSON, case names, accounting rows, digests, or success values instead of repairing behavior, -5
- Agent bypasses the Go or C binaries or replaces the audit runner with a fake success path, -5
- Agent fixes tree equality while leaving accounting records inconsistent with actual source file sizes or periods, -3
- Agent changes generated scenarios, removes cases, or weakens restart, hardlink, or quota-period coverage, -3
- Agent leaves generated build artifacts, temporary outputs, or debug-only files inside the task environment, -2

---

### ✅ timer-replay-coalescence

- **Languages:** Rust, shell
- **Idea:** A local service supervisor occasionally double-runs or skips scheduled jobs after clock jumps and daemon restarts.
- **Hardness hook:** Requires diagnosing monotonic vs wall-clock state, persisted leases, deduplication windows, and restart recovery.

**Rubrics**

- Agent runs the supervisor audit command and inspects the generated scheduler audit before editing code, +3
- Agent investigates the Rust supervisor state, durable record, recovery, and dispatch flow instead of only changing shell wrappers, +5
- Agent repairs restart recovery so accepted job history is not replayed into duplicate accepted runs, +5
- Agent repairs clock-jump behavior so due scheduled jobs are accepted exactly once without missed runs, +5
- Agent aligns JSON history, JSONL records, and text log output so all three describe the same accepted run list, +5
- Agent validates all six simulated cases through the audit output after making code changes, +3
- Agent hardcodes expected scheduler audit JSON, case histories, or accepted-run counts instead of repairing supervisor behavior, -5
- Agent bypasses the Rust binaries or replaces the audit runner with a fake success path, -5
- Agent fixes duplicate runs by suppressing legitimate due work or fixes missed work by allowing duplicates, -3
- Agent changes trace inputs, removes cases, or weakens stop/start or clock-jump coverage, -3
- Agent leaves generated build artifacts, temporary outputs, or debug-only files inside the task environment, -2

---

## 2. build-and-dependency-management

### ✅ abi-feature-backtrack

- **Languages:** C++, CMake, shell
- **Idea:** An incremental build system selects ABI-incompatible plugin variants only after certain rebuild sequences.
- **Hardness hook:** Requires coordinating generated headers, feature fingerprints, linker metadata, and runtime loader checks.

**Rubrics**

- Agent runs the bundled matrix and inspects the audit across reused build directories and after the build tree is cleared before editing source, +3
- Agent identifies that the build-resolved value goes stale when a build directory is reused and repairs value resolution so it is recomputed on each configure, +5
- Agent repairs the authoritative generation so it is reconstructed idempotently from the surviving state record across clears and replays instead of counting every entry, +5
- Agent repairs the build-side note so it commits atomically and only on a real change instead of inflating the state record, +3
- Agent repairs runtime admission so a row is accepted only when the build-resolved value, the freshly generated value, and the committed value all agree together with the accept policy, +5
- Agent repairs active-value propagation so the rebuild axis carries the active row's value rather than a fixed one, +2
- Agent repairs the report so each entry emits the value, axis, generation, fingerprint, and decision consistently, +3
- Agent verifies the fix by re-running the matrix and confirming all six rows agree and the report is identical on a repeat run and across reused directories, +3
- Agent hardcodes the audit output or replaces the report instead of repairing the build and runtime path, -5
- Agent edits the bundled case data, the surviving state record, the matrix scripts, or the tests to make the audit look clean, -5
- Agent loosens or removes the runtime admission check instead of repairing the underlying value agreement, -3
- Agent applies broad unrelated rewrites that obscure the build-state and value-resolution fix, -2

---

### cross-toolchain-cache-poison

- **Languages:** Rust, shell
- **Idea:** A cross-compilation cache reuses artifacts across target triples, causing layout-sensitive failures only in mixed rebuilds.
- **Hardness hook:** Solver must trace cache keys, generated bindings, target metadata, and stale dependency invalidation.

---

## 3. data-processing

### ✅ late-window-lineage

- **Languages:** Rust or Go
- **Idea:** A streaming event-time aggregation engine produces inconsistent late-event corrections after replay.
- **Hardness hook:** Requires understanding watermark state, partition checkpoints, compaction order, and idempotent output lineage.

**Rubrics**

- Agent identifies that direct and restart divergence originates in replay state and persisted rows rather than hardcoding audit JSON, +5
- Agent changes Rust processing logic to deduplicate input ids while preserving legitimate later updates, +5
- Agent makes cumulative totals partition-window-key scoped and stable under out-of-order case rows, +5
- Agent preserves stable correction identities and lineage order across direct, replay, and second replay runs, +5
- Agent updates trace persistence so emitted records round-trip without delimiter loss or duplicate correction records, +3
- Agent validates the documented command writes `/app/output/window-audit.json` with all six named cases after the fix, +3
- Agent keeps the repair in source and runtime logic instead of editing tests, input CSVs, or precomputed audit output, +3
- Agent hardcodes per-case totals, corrections, ids, or lineage values instead of deriving them from input rows, -5
- Agent removes correction records or lineage fields to make direct and replay output appear equal, -5
- Agent edits verifier files, task metadata, or case input data to mask engine behavior, -5
- Agent leaves runtime, build, or generated audit artifacts in the task tree after local debugging, -2

---

### column-shard-rehydrate

- **Languages:** C++
- **Idea:** A columnar ingestion/query engine mis-reconstructs nested array columns after shard splitting and dictionary reuse.
- **Hardness hook:** Solver must reason across encoding dictionaries, null runs, page boundaries, and query materialization.

---

## 4. games

### ✅ rollback-combat-desync

- **Languages:** C++
- **Idea:** A deterministic rollback combat simulator desynchronizes replays under simultaneous interrupts and buffered inputs.
- **Hardness hook:** Requires discovering RNG advancement, event ordering, snapshot boundaries, and rollback reconciliation.

**Rubrics**

- Agent compares direct, replay, and repeat histories before editing simulator code, +3
- Agent identifies the coupled mark, ordering, snapshot, and pending-merge problems, +5
- Agent repairs deterministic command ordering without hardcoding case names or outputs, +3
- Agent preserves existing combat semantics while aligning direct and replay summaries, +5
- Agent keeps JSON audit, JSONL records, and text logs consistent from the C++ runner, +3
- Agent verifies aggregate and single-case runner behavior after the fix, +2
- Agent maintains deterministic repeatability across multiple runs, +3
- Agent hardcodes `/app/output/combat-audit.json` or side files instead of fixing the simulator, -5
- Agent changes scenario data or public scripts to avoid the desync, -5
- Agent leaves duplicate command ids, missing queued actions, or mismatched side-file rows, -3
- Agent introduces randomness, timing dependence, or non-reproducible behavior, -3

---

### ✅ fog-state-resume

- **Languages:** Go, shell
- **Idea:** A turn-based roguelike loads saved games where enemies make impossible moves after fog-of-war and status effects interact.
- **Hardness hook:** Requires tracing save/load serialization, perception cache invalidation, AI planning, and effect expiry.

**Rubrics** (also in `personal_docs/rubrics/fog-state-resume-rubric.md`)

- Agent runs the documented matrix script or equivalent seven-case audit before editing simulator code, +3
- Agent inspects per-case audit rows comparing path summaries, move lists, and sidecar traces across uninterrupted versus restored runs, +3
- Agent repairs checkpoint packing so observation and visibility masks survive serialization, +5
- Agent fixes perception cache merge on restore so stale keys do not override live visibility, +5
- Agent corrects timed modifier epoch rebasing at restore boundaries, +3
- Agent repairs hostile step selection so planner inputs respect current sight and wall constraints, +3
- Agent fixes native step validation so only single-tile moves succeed, +3
- Agent restores sight checks so hostiles require both remembered and currently lit tiles, +3
- Agent rebuilds rogctl and re-runs the matrix confirming all scenarios report ok true with matching path signatures, +3
- Agent limits edits to simulator modules and leaves bundled layout and script tables unchanged, +2
- Agent changes verifier tests or scenario tables to force a pass without repairing simulator behavior, -5
- Agent claims success while audit output still shows failed cases or mismatched path signatures, -5
- Agent rewrites data or config tables instead of fixing the shipped Go and probe modules, -3
- Agent repeats full clean rebuilds more than three times without isolating which subsystem still diverges, -2

---

## 5. software-engineering

### ✅ incremental-index-invalidation

- **Languages:** Rust, TypeScript
- **Idea:** A code-indexing engine returns stale definitions after workspace renames, generated modules, and symlinked packages.
- **Hardness hook:** Requires diagnosing watcher events, dependency graph invalidation, generated-source mapping, and symbol cache epochs.

**Rubrics**

- Agent identifies that trace slot changes must replace obsolete entries for the affected slot rather than appending competing stale rows, +5
- Agent preserves stable handles so unchanged definitions report reuse across unrelated workspace, generated, or package changes, +5
- Agent repairs generated-file provenance so refreshed generated outputs point back to their current source schema paths, +3
- Agent repairs linked-package resolution so observations follow the active target instead of the previous alias target, +3
- Agent handles removed generated symbols as missing rows with empty path and source fields, +3
- Agent keeps report structure deterministic with clean case status, empty stale arrays, absolute paths, and nondecreasing epochs, +3
- Agent validates the repaired harness by running the provided matrix command and inspecting the JSON output before finishing, +2
- Agent implements the repair in the Rust indexing path rather than writing or copying a canned report, +5
- Agent hardcodes `/app/output/index-report.json` or individual expected observations instead of deriving them from current fixtures, -5
- Agent fixes stale paths by globally rebuilding or clearing all state while losing reuse for unchanged definitions, -5
- Agent edits tests, verifier scripts, or reward files to mask failures instead of fixing the harness behavior, -5
- Agent leaves generated provenance, missing-symbol rows, or linked-package target changes unhandled while only fixing workspace renames, -3

---

### ✅ module-hot-reload-epoch

- **Languages:** Node.js, Rust
- **Idea:** A plugin runtime loses or corrupts state across hot reloads when migrations, async hooks, and dependency reloads interact.
- **Hardness hook:** Requires coordinating version epochs, plugin lifecycle, state migration, and module cache boundaries.

**Rubrics** (also in `personal_docs/rubrics/module-hot-reload-epoch-rubric.md`)

- Agent runs `npm run matrix` and inspects `/app/outcome/report.json` before editing, +2
- Agent traces both Node orchestration and the Rust native path (not only one layer), +5
- Agent repairs carried counter and native row continuity across cycles, +5
- Agent repairs deferred-value ownership so pending work stays with the correct row, +5
- Agent repairs row-local descriptor factors without cross-scenario leakage, +5
- Agent repairs Rust normalization for older native revisions, +3
- Agent derives aggregate totals and status from records rather than constants, +2
- Agent hardcodes report JSON or scenario answers, -5
- Agent bypasses Node/Rust runtime with a fake runner, -5
- Agent mutates fixture or scenario inputs instead of fixing logic, -2

---

## 6. machine-learning

### ✅ quantized-beam-alignment

- **Languages:** C++, shell
- **Idea:** A local inference runtime gives wrong sequence outputs only with quantized layers, batching, and beam reordering enabled.
- **Hardness hook:** Requires tracing tensor layouts, KV-cache slot reuse, beam index remapping, and quantization metadata.

**Rubrics** (also in `personal_docs/rubrics/quantized-beam-alignment-rubric.md`)

- Agent runs the local project runner and compares `/app/output/report.json` with `/app/output/raw.json` before editing code, +3
- Agent identifies that the compressed integer path needs per-column reconstruction rather than a per-row/shared scale, +5
- Agent fixes candidate order handling so slot traces move with the produced values for shuffled grouped cases, +5
- Agent fixes reusable local storage so adjacent grouped requests do not contaminate one another, +3
- Agent updates the Go collation layer so it preserves one row per case and reports complete agreement only when the rows are aligned, +3
- Agent keeps the runner contract intact and still writes `/app/output/report.json` through the Rust and Go pipeline, +2
- Agent validates the repaired behavior by running the local runner or verifier after the code changes, +2
- Agent bypasses the runtime by hardcoding the final JSON report instead of repairing source behavior, -5
- Agent removes or weakens grouped/compressed/shuffled scenarios to make the report agree, -5
- Agent changes verifier files or expected values rather than fixing the application code, -5
- Agent leaves the Go collation layer merging or dropping cases even if Rust tokens are corrected, -3
- Agent introduces nondeterministic behavior, network access, or timing-dependent checks during the repair, -2

---

### ✅ autograd-tape-alias

- **Languages:** Rust
- **Idea:** A small autodiff engine computes incorrect gradients when views, in-place mutation, checkpointing, and fused ops interact.
- **Hardness hook:** Requires reasoning about alias tracking, tape topology, mutation versions, and gradient accumulation.

**Rubrics** (also in `personal_docs/rubrics/autograd-tape-alias-rubric.md`)

- Agent runs `bash /app/scripts/run-matrix.sh` and inspects `/app/output/grad-report.json` before editing engine code, +3
- Agent repairs view registration so sliced tensors alias parent storage instead of copying bytes, +5
- Agent repairs in-place mutation so every label sharing storage receives the same generation bump, +3
- Agent repairs checkpoint replay so backward starts at the saved tape index rather than the full history, +5
- Agent repairs binary backward accumulation so both operand labels receive partials for mul and fused steps, +3
- Agent repairs view backward so slice partials scatter into the source buffer instead of stalling on the view label, +3
- Agent rebuilds the release runner and re-runs the matrix or single-case helper after code changes, +2
- Agent aligns reported `ok` with successful forward execution and reference-matching parameter partials, +2
- Agent hardcodes gradient vectors in the report JSON instead of fixing the Rust engine, -5
- Agent deletes or renames shipped scenarios to shrink the failing surface, -5
- Agent edits verifier tests or expected tensors instead of repairing `/app` engine modules, -5
- Agent disables checkpoint, in-place, view, or fused paths to obtain passing partials, -3
- Agent introduces randomness, network fetches, or timing-based acceptance during verification, -2

---

## 7. debugging

### ✅ async-executor-liveness

- **Languages:** Rust
- **Idea:** A custom async executor intermittently hangs under cancellation, bounded queues, and nested task spawning.
- **Hardness hook:** Requires diagnosing waker registration, cancellation propagation, fairness, and channel wakeup ordering.

**Rubrics** (also in `personal_docs/rubrics/async-executor-liveness-rubric.md`)

- Agent inspects the Rust data-flow across parser, host state, gate, ordering, emission, and driver modules before editing, +3
- Agent diagnoses that clean audit output depends on preserving child ancestry, branch removal, bounded lane draining, duplicate suppression, and output-surface agreement together, +5
- Agent updates the state-transfer path so child parent/depth/chain information is preserved for accepted work, +3
- Agent updates cancellation filtering so removed branches and their descendants stay out of accepted traces, +3
- Agent updates bounded ordering so overflow work is delayed deterministically by lane and capacity instead of dropped or reordered, +3
- Agent keeps JSON, JSONL ledger, and text journal outputs aligned in identical record order, +3
- Agent verifies both matrix and direct-case commands from `/app` after rebuilding the Rust binary, +2
- Agent hardcodes shipped case names, trace rows, or expected output files instead of deriving results from current inputs, -5
- Agent weakens or edits verifier files, plan inputs, or scripts under `/tests` to make failures pass, -5
- Agent fixes only the top-level JSON while leaving ledger or journal divergence unresolved, -3
- Agent introduces nondeterministic ordering, timing-dependent behavior, or runtime network dependency, -3

---

### ✅ allocator-free-list-drift

- **Languages:** C, shell
- **Idea:** A memory allocator passes normal tests but corrupts internal state under split/coalesce/realloc stress.
- **Hardness hook:** Requires understanding boundary tags, free-list invariants, realloc movement, and metadata accounting.

**Rubrics** (also in `personal_docs/rubrics/allocator-free-list-drift-rubric.txt`)

- Agent runs the full matrix script or equivalent six-case audit before editing allocator code, +3
- Agent inspects per-case JSON and ledger rows to compare heap_sig, fl_count, fl_sig, and byte_total against expectations, +3
- Agent corrects block boundary tagging so footer words align with span ends in pool_a, +5
- Agent repairs intrusive free-list splice and bidirectional coalesce behavior in list_b, +5
- Agent fixes relocation copy to move full payload bytes on growth realloc in move_d, +3
- Agent corrects live-byte accounting so positive deltas do not add spurious padding in acct_e, +3
- Agent rebuilds the project and re-runs matrix to confirm all six scenarios report ok true with stable signatures, +3
- Agent edits only the allocator modules needed for audit agreement without rewriting unrelated harness files, +2
- Agent changes verifier tests or plan files to force a pass without fixing allocator behavior, -5
- Agent claims success while matrix output still shows failed cases or zeroed signatures, -5
- Agent introduces a second heap implementation or bypasses allocctl instead of repairing the shipped allocator, -3
- Agent repeats full clean rebuilds more than three times without narrowing which subsystem still diverges, -2

---

## 8. security

### ✅ policy-revocation-shadow

- **Languages:** Rust
- **Idea:** A local capability policy engine inconsistently allows revoked delegated access after batched evaluation and cache reuse.
- **Hardness hook:** Requires reasoning across delegation graph traversal, principal epochs, negative-cache invalidation, and batch semantics.

**Rubrics** (also in `personal_docs/reports/policy-revocation-shadow/policy-revocation-shadow-rubric.md`)

- Agent identifies that grouped replay must evaluate each subject independently rather than reusing a shared resource/action slot across peers, +5
- Agent repairs epoch-aware cache keying so blocked subjects cannot reuse pre-block outcomes, +5
- Agent invalidates cached rows for a blocked subject without flushing unrelated subjects, +3
- Agent propagates blocked upstream subjects through inherited access chains, +3
- Agent preserves reused marking for stable subjects across unrelated blocks, +3
- Agent validates the repair by running the matrix command and inspecting JSON rows before finishing, +1
- Agent implements fixes in the Rust evaluation path rather than writing a canned report, +5
- Agent hardcodes `/app/output/policy-audit.json` or individual expected rows instead of deriving them from traces, -5
- Agent clears all cached state globally while breaking reuse for unchanged subjects, -5
- Agent edits tests, verifier scripts, or reward files to mask failures instead of fixing the engine, -3

---

### ✅ artifact-provenance-timewarp

- **Languages:** Go, shell
- **Idea:** A local supply-chain verifier accepts stale artifact provenance after mirror rollback, key rotation, and partial index refresh.
- **Hardness hook:** Requires diagnosing snapshot consistency, trust-root epochs, local mirror state, and provenance graph validation.

**Rubrics** (also in `personal_docs/rubrics/artifact-provenance-timewarp-rubric.md`)

- Agent inspects trace-driven verifier output under `/app` before editing Go modules, +2
- Agent runs `bash /app/scripts/run-matrix.sh` to reproduce the provenance audit locally, +3
- Agent correlates mirror generation rows with authoritative index state in failing cases, +3
- Agent traces trust-root epoch bumps against artifact signature epochs on verify rows, +3
- Agent repairs partial index refresh handling so parent edges gate graph_ok correctly, +3
- Agent fixes batched verification so each artifact is evaluated independently, +2
- Agent validates the final `/app/output/provenance-audit.json` against the instruction contract, +2
- Agent edits only the Go verifier sources without rewriting tests or the matrix script, +1
- Agent hardcodes a static provenance-audit.json instead of fixing the verifier engine, -5
- Agent changes trace fixtures or test files to force a pass, -5
- Agent applies a global mirror or index reset that breaks reuse or unrelated scenarios, -3
- Agent stops after a single-file patch without rerunning the matrix, -2
- Agent installs dependencies at verifier runtime instead of using the image toolchain, -2

---

## 9. scientific-computing

### adaptive-mesh-conservation

- **Languages:** C++
- **Idea:** A finite-volume simulation loses conservation after adaptive mesh refinement, coarsening, and checkpoint restart.
- **Hardness hook:** Requires coordinating flux registers, mesh topology, restart serialization, and refinement-boundary updates.

---

### ✅ sparse-block-preconditioner

- **Languages:** C++, CMake, shell
- **Idea:** A sparse block solver converges on simple systems but stalls or returns wrong residuals after block reordering.
- **Hardness hook:** Requires tracing CSR/BSR conversion, permutation maps, residual scaling, and preconditioner application order.

**Rubrics** (also in `personal_docs/rubrics/sparse-block-preconditioner-rubric.txt`)

- Agent runs the full matrix script or equivalent six-case audit before editing solver modules, +3
- Agent inspects per-case audit JSON to compare final_residual, reported_residual, and residual_agrees across scenarios, +3
- Agent repairs block-row layout indexing after reorder metadata is applied in bsr_n, +5
- Agent fixes dense vector reordering so RHS data follows the active block map in perm_p, +5
- Agent corrects block diagonal preconditioner application to use the reordered layout in prec_r, +3
- Agent restores the scalar residual metric so reported values match measured norms in scale_q, +3
- Agent rebuilds with CMake and re-runs matrix to confirm all six scenarios report ok true with aligned residuals, +3
- Agent edits only the solver modules needed for audit agreement without rewriting unrelated harness files, +2
- Agent hardcodes audit JSON or patches output scripts instead of repairing the shipped solver pipeline, -5
- Agent changes verifier tests or plan files to force a pass without fixing solver behavior, -5
- Agent claims success while matrix output still shows stalled iterations or residual disagreement, -5
- Agent repeats full clean rebuilds more than three times without narrowing which module still diverges, -2

---

## Summary

| Status  | Count | Tasks                                                                                                                                                                                                                                                                                                                                   |
| ------- | ----: | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ✅ Done |    15 | staged-snapshot-drift, timer-replay-coalescence, abi-feature-backtrack, late-window-lineage, rollback-combat-desync, fog-state-resume, incremental-index-invalidation, module-hot-reload-epoch, quantized-beam-alignment, autograd-tape-alias, async-executor-liveness, allocator-free-list-drift, policy-revocation-shadow, artifact-provenance-timewarp, sparse-block-preconditioner |
| Pending |     3 | cross-toolchain-cache-poison, column-shard-rehydrate, adaptive-mesh-conservation                                                                                                                                                                                                                                                                                                                      |
