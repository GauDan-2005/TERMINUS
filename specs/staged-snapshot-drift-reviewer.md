### Decision
GO — Attempt 1.

### Metadata
- Task name: staged-snapshot-drift
- Title: Restored Tree Drift
- Category: system-administration
- Languages: ["Go", "shell", "C"]
- Difficulty: hard
- Codebase size: small
- Subcategories: []
- Tags: ["filesystem", "snapshots", "restore", "quotas", "hardlinks"]
- Milestones: 0

### Discovery budget
- Discovery: The persisted operation stream is not safely replayed in the same effective order after a process boundary.
  Planned location: `environment/internal/b1/replay.go` plus scenario traces emitted by `environment/scripts/run-matrix.sh`.
  Why instruction must not reveal it: Naming replay order would point directly to the repair and collapse the diagnosis work.
- Discovery: The code treats names and backing file identity as equivalent in some paths but not others.
  Planned location: `environment/internal/d3/pair.go`, `environment/internal/a0/core.go`, and C observations from `environment/probe/measure.c`.
  Why instruction must not reveal it: Telling the solver to track inode-style identity turns the task into a standard hardlink recipe.
- Discovery: Accounting attributes are produced on a different lifecycle than restored file objects.
  Planned location: `environment/internal/c2/roll.go`, `environment/internal/c2/table.go`, and profile data under `environment/data/profiles/`.
  Why instruction must not reveal it: Naming metadata propagation exposes the cross-subsystem invariant the solver should infer.
- Discovery: The C traversal helper and Go grouping code disagree on what observation is stable across generated cases.
  Planned location: `environment/probe/measure.c`, `environment/internal/e4/walk.go`, and verifier-side independent inspection.
  Why instruction must not reveal it: Directing attention to the helper boundary makes the likely edit frontier too small.

### Anti-trivialization verdict
- Disclosure-collapse: PASS — an honest prompt can state the bad restored output without naming the internal coupling.
- Hidden-instance: PASS — the verifier uses multiple generated profiles, not one secretly corrupted case.
- Single-artifact repair: PASS — planned fix spans Go state, persisted rows, metadata records, and C observations.
- Generalization: PASS — the tests cover clean, interrupted, transition, dense, and mixed scenarios.
- Prompt-honesty: PASS — the output contract can be complete while the diagnosis remains undisclosed.
- Cheating-vs-difficulty: PASS — difficulty comes from cross-component reasoning, not anti-tamper rules.
- Mechanical-fix filter: PASS — the task is semantic, not dependency or timeout tuning.
- Localized-fix: PASS — no single function or tiny cluster controls more than two of six tests.
- Oracle-locality: PASS — oracle is expected to alter several files and add real coordination logic.
- Small declarative-cluster: PASS — not a policy table or manifest repair.
- Grep-collapse: PASS — planned instruction nouns are banned from fix-path symbols and tests use neutral names.
- Pre-factored-helper: PASS — fix-path symbols are opaque and decoys rhyme structurally.
- Recipe-discount: PASS — standard hardlink preservation is insufficient without restart and accounting interactions.
- Security-aura discount: PASS — no security framing is used as a substitute for hardness.
- Orthogonal-checklist: PASS — each local fix interacts with at least one distant invariant.
- Harness-discount: PASS — shell/C/Go realism supports the scenario but is not counted as hardness by itself.
- One-pass solvability: PASS — opening obvious files should not reveal a one-file patch.
- Hard-only gate: PASS — the coupled failure requires professional filesystem/service debugging.
- Discovery budget test: PASS — at least four non-trivial discoveries are planned.
- Instruction specificity test: PASS — planned instruction is symptoms-only.
- Topology distribution test: PASS — three plausible topologies each require at least three locations.

### Topology enumeration (3 candidate fix topologies)
- Topology 1: Coordinated replay/materialization path.
  Locations: `internal/b1/replay.go::fold_b`, `internal/a0/core.go::phase_a`, `internal/d3/pair.go::bind_d`, `probe/measure.c::walk_e`.
  Why no single location suffices: Ordering alone cannot preserve grouped backing objects or emit accounting records, and grouping alone cannot repair persisted replay.
- Topology 2: Capture-side canonical object graph.
  Locations: `internal/a0/scan.go`, `internal/a0/core.go::phase_a`, `internal/c2/roll.go::mark_c`, `internal/f5/encode.go`.
  Why no single location suffices: Captured graph shape, encoded rows, and emitted metadata must agree across process boundaries.
- Topology 3: Inspection-normalized reconciliation.
  Locations: `probe/measure.c::walk_e`, `internal/e4/walk.go`, `internal/d3/map.go`, `internal/c2/table.go`.
  Why no single location suffices: Native observations must be normalized before Go grouping and metadata tables can converge.

### Rubric axes
- Verifiable: PASS — tests can deterministically generate workspaces and compare filesystem/report observations.
- Well-specified: PASS — instruction can state the desired audit outcome in concise prose.
- Solvable: PASS — an expert can debug and repair the small Go/C service in a few hours.
- Difficult: PASS — the failure combines restart semantics, file identity, and metadata lifecycle reasoning.
- Interesting: PASS — local backup/snapshot drift is production-relevant system administration work.
- Outcome-verified: PASS — verifier grades behavior and outputs, not the chosen implementation approach.

### Hardness axes
- Discover: PASS — the solver must inspect code and runtime traces to learn how rows, object identity, and accounting records flow.
- Synthesize: PASS — the answer spans Go service internals, native scanning, shell scenarios, and generated data.
- Diagnose: PASS — the prompt describes drift, not replay-order or identity-tracking causes.
- Navigate coupling: PASS — local fixes can break other scenarios because identity and accounting are propagated through different layers.
- Reason beyond training: PASS — this is not a textbook hardlink or backup script recipe; it requires domain reasoning about restart-sensitive state.

### Instruction completeness test
Can the agent solve this by reading ONLY instruction.md without deeply engaging with the codebase? No. The instruction can say what the audit must prove and where to leave the report, but the solver must find why the existing service diverges under the coupled scenario matrix.

## Reviewer Appendix

### Implementation plan
Build a compact Go service and CLI with neutral package names, a C filesystem observation helper, shell scenario scripts, and profile data. Seed the environment with defects that only compose under process restart plus period transition plus file identity reuse. The agent will run the audit, inspect logs and code, then repair coordinated data flow across the persisted row stream, object graph, metadata emission, and native observation boundary.

The verifier will not trust the report alone. It will run scenarios in isolated temp dirs, inspect actual files and link groups, compare report fields to independent observations, and ensure the original no-op environment fails. The oracle should add real implementation logic across the committed symbol table rather than replacing the runner.

### Proposed file inventory
- `instruction.md` — concise symptoms-only prompt.
- `task.toml` — Edition 2 metadata and timeouts.
- `output_contract.toml` — declares `/app/output/restore-audit.json`.
- `construction_manifest.json` — local copy of the symbol and flipping contract used by collapse checks.
- `environment/Dockerfile` — pinned single-container Go/C build image.
- `environment/go.mod` — local Go module definition for the utility code.
- `environment/Makefile` — build targets for service, CLI, and helper.
- `environment/README.md` — operator overview without repair hints.
- `environment/docs/architecture.md` — subsystem overview.
- `environment/docs/operators.md` — how profiles are run.
- `environment/config/profiles.toml` — scenario profile registry.
- `environment/config/layouts.toml` — layout registry.
- `environment/cmd/apex/main.go` — service entrypoint.
- `environment/cmd/ctl/main.go` — CLI entrypoint.
- `environment/internal/a0/core.go`, `scan.go`, `pack.go` — object graph and capture support.
- `environment/internal/b1/log.go`, `replay.go`, `checkpoint.go` — persisted stream support.
- `environment/internal/c2/table.go`, `roll.go` — accounting table support.
- `environment/internal/d3/map.go`, `pair.go` — grouping support.
- `environment/internal/e4/io.go`, `walk.go` — helper integration and tree walking.
- `environment/internal/f5/types.go`, `encode.go` — shared record types and encoding.
- `environment/internal/g6/cache.go`, `environment/internal/h7/rollup.go` — decoys with real non-fix work.
- `environment/probe/fswalk.c`, `fswalk.h`, `measure.c`, `list.c` — native observation helper.
- `environment/scripts/run-matrix.sh`, `make-case.sh`, `clean-room.sh` — scenario orchestration.
- `environment/data/profiles/*.toml`, `environment/data/layouts/*.manifest` — generated input definitions.
- `solution/solve.sh` — deterministic oracle patch.
- `tests/test.sh`, `tests/test_outputs.py` — pytest verifier and reward writer.

### Oracle notes
The oracle should modify the committed fix-path symbols to make row folding deterministic across process boundaries, keep backing-object grouping stable when multiple names share one underlying file, propagate accounting attributes through the same object graph that emits restored files, and normalize the C observation data consumed by tests. It should also update any necessary call sites and error handling so partial state does not silently produce a clean report.

### Collapse audit
Stage: implementation-plan

Smallest plausible successful patch:
The smallest credible patch coordinates persisted row folding, object grouping, accounting record transfer, and native observation normalization. A one-file change can improve one symptom but should not satisfy all six tests.

Likely editable frontier:
- `environment/internal/a0/core.go`
- `environment/internal/b1/replay.go`
- `environment/internal/c2/roll.go`
- `environment/internal/d3/pair.go`
- `environment/probe/measure.c`
- call sites in adjacent neutral packages

Requirement-to-file map:
- Restored tree equivalence -> `internal/a0`, `internal/d3`, `internal/e4`, `probe`.
- Restart consistency -> `internal/b1`, `internal/a0`.
- Accounting agreement -> `internal/c2`, `internal/f5`, verifier inspection.
- Mixed scenario correctness -> all fix roots plus scripts.

Oracle estimated complexity: 110-150 non-boilerplate lines.

Red flags:
- The instruction must not name replay order, identity tracking, or quota metadata propagation.
- Test names and file paths must stay neutral enough to avoid grep collapse.

Residual hardness:
After the full file tree is visible, the solver still has to connect runtime divergence to the interaction between persisted operation ordering, object identity grouping, metadata lifecycle, and the C/Go observation boundary. That synthesis is the hard work.

Collapse verdict: PASS

### Naming-pass record

**Instruction nouns extracted:**
service, audit, trees, source, restart, problem, quota, period, data, directory, layouts, hardlinks, command, report, scenarios, link, relationships, accounting, records, runner, checks, completion

**Renames during drafting:**
- `restoreLink` -> `bind_d`: avoided `restore`/`link` leakage from planned instruction vocabulary.
- `test_quota_rollover` -> `test_epsilon_matrix`: removed direct scenario nouns from test surface.

**Test names audited:**
- `test_alpha_matrix`
- `test_beta_matrix`
- `test_gamma_matrix`
- `test_delta_matrix`
- `test_epsilon_matrix`
- `test_zeta_matrix`

**Concentration math:**
- Total tests across `flipping_point_contract`: 6
- Per location:
  - A (`internal/a0/core.go`): 2/6 = 0.333333
  - B (`internal/b1/replay.go`): 2/6 = 0.333333
  - C (`internal/c2/roll.go`): 2/6 = 0.333333
  - D (`internal/d3/pair.go`): 2/6 = 0.333333
  - E (`probe/measure.c`): 2/6 = 0.333333
- Cap: 0.5. Max ratio observed: 0.333333. Status: PASS

### Per-test feasibility pre-check
- Test: `test_alpha_matrix`
  Checks: clean scenario report, tree equivalence, and verifier-side filesystem agreement.
  Valid approaches: 2+.
  Chain-dependent: no.
  Exact-value assertions: no fixed oracle constants; digests and records are derived from the test-created source tree.
  Feasibility risk: LOW.
  Recommendation: keep as a medium-hard baseline, but do not let it be the only passing path for NOP.
- Test: `test_beta_matrix`
  Checks: dense identity grouping after an interruption between staging and materialization.
  Valid approaches: 2+.
  Chain-dependent: no.
  Exact-value assertions: source link groups are computed during the test, not copied from a fixture.
  Feasibility risk: MEDIUM.
  Recommendation: keep; it is hard but independently achievable because the test creates its own source tree and interruption.
- Test: `test_gamma_matrix`
  Checks: persisted replay behavior across a process boundary and deterministic repeated restore.
  Valid approaches: 2+.
  Chain-dependent: no.
  Exact-value assertions: expected tree state is derived from the generated operation stream and source inspection.
  Feasibility risk: MEDIUM.
  Recommendation: keep; avoid timing assertions and use deterministic subprocess boundaries.
- Test: `test_delta_matrix`
  Checks: accounting records agree with independent source observations.
  Valid approaches: 2+.
  Chain-dependent: no.
  Exact-value assertions: accounting values are computed from source-side observations in the verifier.
  Feasibility risk: MEDIUM.
  Recommendation: keep; this prevents identity-only fixes from passing.
- Test: `test_epsilon_matrix`
  Checks: period-transition profile remains consistent across restored tree and accounting attribution.
  Valid approaches: 2+.
  Chain-dependent: no.
  Exact-value assertions: no static transition totals; verifier derives expected attribution from profile inputs and source state.
  Feasibility risk: MEDIUM.
  Recommendation: keep; make setup deterministic rather than time-of-day dependent.
- Test: `test_zeta_matrix`
  Checks: mixed stress scenario across all coupled conditions.
  Valid approaches: 2+.
  Chain-dependent: no; self-contained setup, with internal coupling by design.
  Exact-value assertions: all expected values are computed from the generated case and independent inspection.
  Feasibility risk: MEDIUM.
  Recommendation: keep as the hard compositional gate; if it becomes flaky, reduce nondeterminism instead of loosening semantics.

### Step 3b WARN justification
- RC1 Oracle Simplification: ACCEPT WITH JUSTIFICATION. The net delta is +3 lines across five comparable oracle targets, with three shortened files and two expanded files. The shorter files remove defective special-case branches and replace them with shared state transitions; they do not delete whole subsystems or bypass verification. The frontier remains five roots with 392 non-boilerplate oracle LOC, and the verifier still requires coordinated Go/C behavior rather than a cleanup-only patch.
- CR1 Symbol-Table Compliance: ACCEPT WITH JUSTIFICATION. The outside symbols are incidental Go/C declarations and local helpers touched by whole-file source writes, not extra named repair targets exposed to the solver. The manifest still captures the semantic frontier (`phase_a`, `fold_b`, `mark_c`, `bind_d`, `walk_e`), CR2 and CR8 pass, and collapse reports zero oracle-touched symbol overlap with instruction nouns.
- CR7 Grep-Resistance: ACCEPT WITH JUSTIFICATION. The instruction now documents accounting and hardlink contract details requested by review, which introduces two unavoidable path-stem overlaps at the file-path level, but still reports zero oracle-touched symbol overlap. The fix-path symbols remain opaque, and the prompt still does not name packages, functions, the C probe, or root causes; solving still requires tracing replay, grouping, accounting, and native observation behavior across five roots.
- GX3 Oracle Edit Distance: ACCEPT WITH JUSTIFICATION. The real edit distance is 51 non-comment added/removed lines across five roots, which is borderline but not tiny. GX2 and GX4 pass, so the oracle is not hiding a no-op or a tiny semantic change inside bulk rewrites. The changed lines alter replay, grouping, accounting, and native observation behavior that the NOP run fails and the oracle run passes.
