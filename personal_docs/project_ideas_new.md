# Project Ideas — New Candidate Bank (Rust / Go)

Generated from:

- `web/terminal-bench-task-creation.md`
- `.cursor/rules/difficulty-calibration.mdc`
- `.cursor/rules/idea-validation.mdc`

Cross-checked for originality against the **full existing bank**: the 16 attempted/submitted
tasks, 2 pending, and 27 candidate seeds in `personal_docs/Project_ideas.md`, plus the historical
shipped tasks named in `difficulty-calibration.mdc` (`grandchild-exit-leak`, `pipe-close-shadow`,
`child-finalization-gap`, `counter-restore-replay`, `slot-lineage-drift`, `key-ring-alias`,
`staple-cache-shadow`).

## Constraints applied

- **Hard-only** target; offline verifier path (`allow_internet = false`).
- **Languages: Rust / Go only** (the existing bank overuses C++/C/Python).
- **No `software-engineering`, no `debugging`** categories — these can no longer be submitted.
- No multi-container, no UI-building tasks. No Python.
- Prefer milestone decomposition where the work splits into sequential stages.

## Originality strategy (addresses the anti-spam / anti-templating criteria)

The current bank's dominant failure-of-originality risk: ~15 of the 16 attempted tasks use the
**same template** — *"run a matrix command → write `audit.json` → repair so all 6 cases report
`ok:true` after replay/restart drift."* That sameness is exactly what reads as
templated / minor-modification-of-prior-work.

So every idea below deliberately varies **both** the `task_shape` **and** the verifier shape away
from "replay-drift repair," and every idea is anchored to a **named real system** (not a synthetic
or AI-pattern construction). This directly targets the rejection criteria: automated/AI-generated,
synthetic/spam, templated, minor-mod-of-accepted, low-effort, and the originality floor.

Legend: ⚠️ = a known collapse/verification risk to resolve during Step 2a/2b.

---

## 1. system-administration

### cgroup-budget-solver

- **Task shape:** optimization_under_constraints
- **Profile:** config_policy_precedence
- **Language:** Go
- **Idea:** Assign cgroup-v2 limits (`cpu.weight`, `memory.{min,low,high,max}`, `io.max`) across a
  delegated service tree so aggregate guarantees hold, no parent over-commits its delegated budget,
  burst-headroom constraints hold, and a stated fairness objective is maximized. The verifier scores
  the objective and checks the hard constraints; many valid assignments pass.
- **Hard because:** memory **protection redistribution** (unused `memory.min`/`low` propagates down
  the subtree) is non-textbook; weight-relative vs absolute limits interact; this is a real
  constrained search, not a knob-set.
- **Distinct from:** nothing in the bank is an optimization/solver — all 16 attempted are repairs.
  Closest is `service-unit-env-precedence` (a precedence *repair*; this is a *search*).
- **Real source:** kernel cgroup-v2 memory-protection model; systemd resource control.

### overlayfs-whiteout-flatten

- **Task shape:** repair_existing_system (symptoms-only)
- **Profile:** filesystem_state_reconstruction
- **Language:** Go
- **Idea:** A userspace image-layer flattener (umoci-style) produces flattened trees that diverge
  from kernel overlay semantics for specific layer stacks.
- **Hard because:** whiteout (`.wh.`) ordering, opaque-dir markers (`trusted.overlay.opaque`),
  metadata copy-up precedence across N layers, and hardlink preservation must coordinate — the agent
  discovers *which* merge stage is wrong.
- **Distinct from:** `staged-snapshot-drift` is snapshot/restore drift; this is union-merge
  semantics.
- **Real source:** Linux overlayfs + OCI image-spec whiteouts; umoci / containers-storage.

---

## 2. build-and-dependency-management

### cargo-feature-unification

- **Task shape:** reverse_engineering
- **Profile:** build_dependency_toolchain
- **Language:** Rust
- **Idea:** Infer/repair Cargo **resolver-v2** feature unification across a workspace graph:
  `default-features=false`, optional deps, `dep:` syntax, **weak features** (`pkg?/feat`), and the
  host/build/target/dev-dependency boundaries that do *not* unify. Output the resolved feature set
  per crate per target.
- **Hard because:** resolver-v2 weak-feature + target-split unification is famously subtle (not the
  naïve "features are a union"); it spans the whole manifest graph.
- **Distinct from:** all existing build tasks are *stale-cache* repairs (`abi-feature-backtrack`,
  `cross-toolchain-cache-poison`, `abi-cache-relink-drift`); this is resolution semantics, not cache
  invalidation.
- **Real source:** Cargo book features chapter; RFC 2957 (weak dependency features).
- ⚠️ Scope discipline at 2b so it does not become a spec recitation.

### go-mvs-graph-pruning

- **Task shape:** repair_existing_system (symptoms-only)
- **Profile:** build_dependency_toolchain
- **Language:** Go
- **Idea:** A module resolver computes wrong build lists under `require` / `exclude` / `replace` /
  `retract` combined with the **pruned module graph** (Go 1.17+ lazy loading). Symptoms: certain
  graphs select wrong versions or load too much.
- **Hard because:** MVS is not SAT-style resolution; the graph-pruning interaction with
  `replace` / `exclude` is exactly where most mental models break.
- **Distinct from:** fresh — no version-selection task exists in the bank.
- **Real source:** `go.dev/ref/mod`; Russ Cox MVS papers.

---

## 3. data-processing

### ivm-retraction-divergence

- **Task shape:** repair_existing_system (symptoms-only)
- **Profile:** distributed_reconciliation
- **Language:** Rust
- **Idea:** A differential-dataflow-style materialized-view engine maintained incrementally diverges
  from a full batch recompute for certain **delete/retraction** sequences crossing GROUP BY / join
  boundaries.
- **Hard because:** multiplicity arithmetic, retraction correctness across join→aggregate, and
  consolidation must coordinate. Verifier is **metamorphic** (incremental == batch over random op
  streams) — robust, not a golden file.
- **Distinct from:** `late-window-lineage` / `cdc-tombstone-merge-order` are streaming
  reconciliation; this is incremental-view-maintenance *math*.
- **Real source:** Materialize / DBSP / timely-differential dataflow.

### bitemporal-asof-correction

- **Task shape:** reverse_engineering
- **Profile:** file_format_serialization (temporal data)
- **Language:** Go
- **Idea:** A bitemporal store (valid-time + transaction-time) answers as-of queries wrong when
  **retroactive valid-time corrections** interact with transaction-time snapshots. Infer the
  temporal semantics from query/result examples and generalize.
- **Hard because:** bitemporal as-of reasoning is notoriously error-prone; corrections vs snapshots
  is the exact trap.
- **Distinct from:** nothing temporal-data in the bank.
- **Real source:** SQL:2011 temporal tables; XTDB / Crux.

### hnsw-delete-recall

- **Task shape:** repair_existing_system (symptoms-only)
- **Profile:** ml_adversarial_robustness
- **Language:** Go
- **Idea:** An HNSW vector index loses recall / leaves vectors unreachable after delete-heavy
  workloads (tombstones + re-insertion break graph connectivity at upper layers).
- **Hard because:** connectivity maintenance on deletion is a genuinely open-ish problem; layer
  reassignment and neighbor re-linking couple. Verifier: recall@k vs brute-force + an **exact
  reachability invariant**, fixed seed.
- **Distinct from:** fresh — no ANN/vector-search task exists.
- **Real source:** HNSW paper (Malkov & Yashunin); known qdrant/weaviate deletion limitations.
- ⚠️ Recall verification must be seed-pinned to stay 20/20 deterministic.

---

## 4. games

### navmesh-generation

- **Task shape:** constrained_build
- **Profile:** floating_point_numeric_policy (computational geometry)
- **Language:** Rust
- **Idea:** Build a navmesh from polygon obstacles (Recast-style): region partition → contour trace →
  convex polygonization under a vertex budget. Concave/degenerate obstacle stacks currently yield
  non-convex or wrongly-disconnected regions.
- **Hard because:** watershed partitioning + contour simplification + convex merge is hard geometry.
  Verifier checks **topological invariants** (convexity, connectivity, coverage, path existence for
  query pairs) — many valid meshes accepted.
- **Distinct from:** all existing games tasks are rollback/replay/snapshot determinism; this is
  geometry construction. (First `constrained_build` shape in the bank.)
- **Real source:** Recast/Detour (Mikko Mononen).

### trigger-stack-resolution

- **Task shape:** repair_existing_system (symptoms-only)
- **Profile:** concurrency_ordering
- **Language:** Go
- **Idea:** A card / auto-battler rules engine resolves simultaneous and nested triggered abilities
  wrong: the stack (LIFO) + APNAP ordering + replacement effects + **state-based actions re-checked
  after each resolution** don't coordinate.
- **Hard because:** it is *not* a lookup table — four interacting rule subsystems; symptoms-only
  ("nested triggers occasionally resolve out of order").
- **Distinct from:** fresh; not a simulator-determinism task.
- **Real source:** MTG comprehensive rules (the stack, APNAP); Forge / XMage engines.

### order-independent-procgen *(secondary)*

- **Task shape:** repair_existing_system (symptoms-only)
- **Profile:** state_recovery_crash_consistency
- **Language:** Go
- **Idea:** A chunked world generator must produce identical chunks regardless of visit order, but
  cross-chunk features (rivers / structures spanning boundaries) read neighbor state and break it.
- **Hard because:** cross-boundary feature placement must be made deterministic and order-independent
  via correct region seeding/coordination.
- **Distinct from:** this is **spatial** order-independence, not temporal replay-determinism.
- **Real source:** Minecraft-style chunk generation.

---

## 5. machine-learning

*Rust/Go, discrete and deterministic — sidesteps the Python HARD blocker and float-flakiness.*

### bpe-tokenizer-roundtrip

- **Task shape:** repair_existing_system (symptoms-only)
- **Profile:** file_format_serialization
- **Language:** Rust
- **Idea:** A byte-level BPE tokenizer (HF-`tokenizers`-style) gives wrong IDs / misaligned offset
  mappings for Unicode (NFC/NFD combining marks, emoji, byte-fallback) and merge-rank ties.
- **Hard because:** normalization ↔ pretokenization ↔ merge-priority ↔ offset-mapping interact;
  byte-level BPE edge cases are rare in training data. Round-trip + offset verification is fully
  discrete.
- **Distinct from:** `quantized-beam-alignment` / `autograd-tape-alias` are numeric; this is
  text/serialization.
- **Real source:** HF `tokenizers` (Rust); GPT-2 byte-level BPE.

### grammar-constrained-decoding

- **Task shape:** adversarial_generalization
- **Profile:** file_format_serialization
- **Language:** Rust
- **Idea:** A grammar-constrained decoder (GBNF / outlines-style) occasionally emits strings the
  grammar forbids because the **token-boundary vs grammar-symbol-boundary** mask is wrong for
  multi-token terminals. Must be robust on a held-out grammar set.
- **Hard because:** token/grammar boundary mismatch is subtle; discrete mask verification (no
  floats).
- **Distinct from:** fresh; no decoding/grammar task.
- **Real source:** llama.cpp GBNF; outlines.

---

## 6. security

### x509-path-building

- **Task shape:** adversarial_generalization
- **Profile:** security_authority_split
- **Language:** Go
- **Idea:** Repair a cert-chain validator that rejects valid **cross-signed** chains and accepts ones
  violating **name constraints** / basic-constraints. Must be robust against a **held-out adversarial
  chain set** (not enumerated in the prompt).
- **Hard because:** *path building* (not validation) is the part libraries famously get wrong —
  bridge-CA, cross-signs, name-constraint inheritance. Held-out attacks block overfitting.
- **Distinct from:** existing security tasks are capability / revocation / provenance; this is PKI
  path building.
- **Real source:** RFC 5280 path building; real cross-sign expiry incidents; Go `crypto/x509`
  path-building limits.
- ⚠️ Bound to path-building + name-constraints + a few EKU cases, not all of RFC 5280.

### seccomp-bpf-codegen

- **Task shape:** repair_existing_system (symptoms-only)
- **Profile:** security_authority_split
- **Language:** Go
- **Idea:** A policy compiler emits cBPF that **permits a syscall it should deny** when an argument
  comparison is involved — the classic 64-bit arg high/low-32-bit split bug + first-match rule
  precedence + jump-offset computation.
- **Hard because:** cBPF codegen + 64-bit arg semantics + overlapping-rule precedence couple;
  security-critical correctness.
- **Distinct from:** fresh; no syscall/BPF task.
- **Real source:** libseccomp 64-bit-arg CVE class.

---

## 7. scientific-computing

*Rust/Go, not the C++ mesh / sparse-solver family the bank has saturated.*

### robust-geometric-predicates

- **Task shape:** repair_existing_system (symptoms-only) — can be framed formal_reasoning
- **Profile:** floating_point_numeric_policy
- **Language:** Rust
- **Idea:** A Delaunay triangulation produces invalid (crossing/duplicate) triangles or loops
  forever on near-degenerate (collinear/cocircular) inputs because orientation/incircle predicates
  use naïve floating point.
- **Hard because:** requires adaptive-precision / consistent symbolic-perturbation predicates **and**
  keeping the triangulation algorithm correct. Verifier checks Delaunay empty-circle + planarity
  invariants (deterministic inputs).
- **Distinct from:** `sparse-block-preconditioner` / `adaptive-mesh-conservation` are solvers; this
  is geometric robustness.
- **Real source:** Shewchuk adaptive predicates; Triangle / CGAL.
- ⚠️ Seed-pinned inputs to stay 20/20 deterministic.

### symplectic-adaptive-integrator *(secondary)*

- **Task shape:** repair_existing_system (symptoms-only)
- **Profile:** floating_point_numeric_policy
- **Language:** Go
- **Idea:** A symplectic integrator (leapfrog / Verlet) loses energy/structure preservation over long
  runs because adaptive timestepping was bolted on naïvely (adaptive + symplectic is incompatible
  unless done carefully).
- **Hard because:** the adaptivity must be reformulated to preserve the symplectic structure, not
  just reduce local error.
- **Distinct from:** `adaptive-mesh-conservation` is spatial flux conservation; this is temporal
  structure preservation.
- **Real source:** molecular-dynamics / celestial-mechanics integrator literature.

---

## Coverage & originality summary

| Category | Ideas | Task shapes covered |
|---|---|---|
| system-administration | cgroup-budget-solver, udev-precedence-reconstruct, overlayfs-whiteout-flatten | optimization, reverse-eng, repair |
| build-and-dependency-management | cargo-feature-unification, go-mvs-graph-pruning | reverse-eng, repair |
| data-processing | ivm-retraction-divergence, bitemporal-asof-correction, hnsw-delete-recall | repair, reverse-eng |
| games | navmesh-generation, trigger-stack-resolution, order-independent-procgen | **constrained-build**, repair |
| machine-learning | bpe-tokenizer-roundtrip, grammar-constrained-decoding | repair, **adversarial-generalization** |
| security | x509-path-building, seccomp-bpf-codegen | adversarial-generalization, repair |
| scientific-computing | robust-geometric-predicates, symplectic-adaptive-integrator | repair, (formal-reasoning alt) |

- **All 6 task shapes are represented** (vs the current bank, which is ~100% repair).
- **All 17 verifier shapes break the "matrix → audit.json → replay-drift" mold:** solver-scoring,
  infer-and-generalize, topological invariants, round-trip/offset, recall@k + reachability,
  allow/deny vectors, metamorphic batch-equality.
- Every idea names a real system and is distinct from all 45 existing seeds — directly addressing the
  AI-generated / synthetic / templated / minor-mod rejection criteria.

## Caveats to resolve at Step 2a / 2b

- `hnsw-delete-recall` and `robust-geometric-predicates` need seed-pinned verification to stay 20/20
  deterministic.
- `x509-path-building` and `cargo-feature-unification` need tight scope discipline so they do not
  become RFC/spec recitation.

## Language distribution

- **Rust (6):** cargo-feature-unification,
  ivm-retraction-divergence, navmesh-generation, bpe-tokenizer-roundtrip,
  grammar-constrained-decoding, robust-geometric-predicates
- **Go (10):** cgroup-budget-solver, overlayfs-whiteout-flatten, go-mvs-graph-pruning,
  bitemporal-asof-correction, hnsw-delete-recall, trigger-stack-resolution,
  order-independent-procgen, x509-path-building, seccomp-bpf-codegen,
  symplectic-adaptive-integrator

---

## Promoted from the legacy bank (`Project_ideas.md`) — filtered for non-overlap

These entries were extracted from the **unused** ideas in `personal_docs/Project_ideas.md` — the
2 `Pending` tasks plus the 27 `Candidate seeds` (the 16 `✅ Attempted` are already "used"). Each of
the 29 was independently researched and then **adversarially re-screened** (default = refute the
keep) against this bank on five filters: (1) collision with an existing new-bank idea, (2) near-
duplication of an already-attempted task (originality floor), (3) blocked category
(`software-engineering` / `debugging`) with no clean re-home, (4) the over-used "matrix →
`audit.json` → replay/restart/snapshot-drift repair" template, and (5) the Rust/Go + offline-
determinism constraints.

**Result: 7 of 29 survived.** All seven are Rust/Go, single-container, offline-verifiable, and use a
verifier shape that breaks the replay-drift mold (structural round-trip equality, ordered token-list
equality, DAG isomorphism, metamorphic logical-state equality, bit-reproducibility, allow/deny
vectors). Two were re-homed out of the blocked `debugging` category into `data-processing`. The 22
exclusions are logged at the end of this section. Same legend: ⚠️ = a collapse/verification risk to
resolve during Step 2a/2b.

**Category: build-and-dependency-management**

### pkgconfig-sysroot-shadow

- **Task shape:** reverse_engineering
- **Profile:** build_dependency_toolchain
- **Language:** Go
- **Idea:** An offline cross-compilation toolchain shim wraps `pkg-config`: it parses `.pc` files,
  resolves the transitive `Requires` / `Requires.private` graph, and emits the `--cflags`/`--libs`
  token list a cross-build consumes. Under `PKG_CONFIG_SYSROOT_DIR` plus split `PKG_CONFIG_PATH` /
  `PKG_CONFIG_LIBDIR` roots, the resolver merges metadata wrong so headers (`-I`) resolve against one
  sysroot while libraries (`-L`) land in another — silently mixing host and target ABIs.
- **Hard because:** it is not one wrong path to hardcode — several `pkg-config` rules must all hold at
  once: sysroot-prefix rewriting applies to prefix-derived `-I`/`-L` tokens but not to literal/absolute
  tokens; `Requires.private`/`Libs.private` contribute only to `--static` closures; the `Requires` DAG
  needs topological order with order-preserving dedup; variable expansion (`${prefix}`, `${pcfiledir}`,
  recursive vars) must precede sysroot prefixing. The agent reverse-engineers the precedence/merge order
  from observed output and repairs token provenance. Pure discrete string/path/graph resolution — exact,
  metamorphic-checkable, no floats.
- **Distinct from:** `cargo-feature-unification` is feature-boolean unification with no filesystem/sysroot
  paths; `go-mvs-graph-pruning` selects *which versions*, not *where headers vs libs resolve*. Unlike the
  attempted `abi-feature-backtrack` there is no incremental stale-cache / rebuild-sequence dimension — a
  single deterministic resolve-and-compare, no replay/restart/`audit.json` loop.
- **Real source:** freedesktop `pkg-config` / `pkgconf`: the `.pc` keyword grammar (`Cflags`, `Libs`,
  `Requires`, `Requires.private`, `Libs.private`, `Cflags.private`) and `PKG_CONFIG_SYSROOT_DIR` /
  `PKG_CONFIG_PATH` / `PKG_CONFIG_LIBDIR` sysroot-prefix behavior in `pkg-config(1)` / `pkgconf(1)` /
  `pc(5)`, plus `pkgconf` fragment dedup and `--static` private-dep handling.
- ⚠️ Pin the reference oracle to one implementation's exact semantics (prefer `pkgconf`) — `pkg-config`
  vs `pkgconf` differ on dedup and `Requires.private`; verify **exact ordered token sequences** (not set
  equality) to prevent trivial collapse. Operate on synthetic sysroot trees + `.pc` fixtures so the
  verifier stays offline and deterministic.

**Category: data-processing**

### column-shard-rehydrate

- **Task shape:** repair_existing_system (symptoms-only)
- **Profile:** file_format_serialization
- **Language:** Rust
- **Idea:** A Parquet/Arrow-style columnar engine assembles nested list/struct columns wrong after a
  shard (row-group) is split and dictionary pages are reused across the new shards: repetition/definition
  levels, RLE/bit-packed null runs, and dictionary index references desync at page boundaries, so query
  materialization reconstructs wrong nesting cardinality or wrong dictionary values. Repair the
  shred/assembly path so rehydrated nested records exactly equal the pre-shard records for every
  projection.
- **Hard because:** correct reconstruction is the Dremel record-assembly FSM — each nested list boundary
  is encoded only implicitly via the `(repetition_level, definition_level)` pair, so a single off-by-one
  in level accounting silently merges or splits arrays with no crash. Shard splitting forces the assembler
  to re-establish level state mid-stream at a page boundary that no longer aligns to a record boundary, and
  dictionary reuse means an index valid in the original page can decode to a stale value after the split.
  The bug surfaces only on specific empty-vs-null-vs-present combinations at depth, demanding full
  level-algebra reasoning, not a constant.
- **Distinct from:** `bpe-tokenizer-roundtrip` shares the byte-exact round-trip flavor but operates on a
  flat byte stream with merge-rank/Unicode mechanics, not hierarchical rep/def levels. `ivm-retraction-divergence`
  / `hnsw-delete-recall` use recompute/recall oracles; here the verifier is **structural round-trip equality
  of nested records, with no temporal/persistence loop** (unlike attempted `late-window-lineage` /
  `staged-snapshot-drift`). Adjacent to `dictionary-rollover-nesting` below but with a different trigger:
  this task's fault is *row-group splitting + cross-shard dictionary reuse*, not mid-chunk dictionary-cap
  fallback.
- **Real source:** Dremel record shredding/assembly (Melnik et al., *Dremel: Interactive Analysis of
  Web-Scale Datasets*, VLDB 2010) defining repetition/definition levels; the Apache Parquet format spec
  (nested encoding, dictionary + RLE/bit-packing hybrid, row groups/pages) and Apache Arrow layout;
  implementable on the Rust `parquet`/`arrow-rs` crates.
- ⚠️ Keep deterministic and float-free (integer/dictionary-coded payloads, fixed page/row-group sizes) so
  the verifier is exact nested-record equality. Ensure the planted bug requires genuine cross-page
  level-state reasoning (split lands mid-record, dictionary reuse creates a real index/value ambiguity),
  not a trivial bounds fix. Hold the encoder/reference assembler fixed so only the buggy re-shard path is
  under repair.

### dictionary-rollover-nesting

- **Task shape:** repair_existing_system (symptoms-only)
- **Profile:** file_format_serialization
- **Language:** Rust
- **Idea:** A Parquet-style columnar writer/reader for nested records corrupts values when a column's
  dictionary page hits its size cap mid-column and must fall back from `RLE_DICTIONARY` to `PLAIN`
  encoding for the remaining data pages. Repair the encoder/decoder so the dictionary-index reset at the
  fallback boundary, the repetition/definition-level runs, and the null runs that straddle page boundaries
  all reconstruct the original nested records byte-for-byte.
- **Hard because:** the bug lives where four independently-correct subsystems compose: (1) dictionary
  fallback — once the dictionary page exceeds the cap, later pages in the same column chunk must switch to
  `PLAIN`, and a naive writer keeps emitting indices the reader can no longer resolve; (2) Dremel shredding
  — levels are RLE/bit-packed independently of values, so a fallback-inserted page boundary desyncs level
  runs from value runs; (3) null handling — `definition_level < max` means "no value present," so null runs
  must not consume dictionary indices, and an off-by-one shifts every following value; (4) materialization
  replays levels and values together. No single knob — the solver must locate where the
  one-encoding-per-page / levels-vs-values-alignment / dictionary-scope invariant breaks.
- **Distinct from:** `bpe-tokenizer-roundtrip` is a flat token stream, not a paged columnar container with
  fallback + nested levels. `late-window-lineage` / `ivm-retraction-divergence` are streaming/incremental
  aggregation, not on-disk format serialization; `hnsw-delete-recall` / `bitemporal-asof-correction` are
  query/index-semantics with no binary-format layer. Adjacent to `column-shard-rehydrate` above but with a
  different trigger: this fault is *mid-chunk dictionary-cap fallback (`RLE_DICTIONARY`→`PLAIN`)*, not
  row-group splitting with cross-shard dictionary reuse.
- **Real source:** Apache Parquet format spec — the dictionary-encoding rules
  (`PLAIN_DICTIONARY`/`RLE_DICTIONARY` and the dictionary-page-size fallback to `PLAIN`) in
  `parquet-format` `Encodings.md`, combined with the rep/def-level shredding model from Melnik et al.
  (*Dremel*, VLDB 2010); reference: `arrow-rs` `parquet` crate dictionary-fallback path.
- ⚠️ Define a small fixed binary subformat (or pin one `arrow-rs` version) so reference bytes are
  deterministic and round-trip is exact — do not depend on a third-party writer's nondeterministic
  dictionary ordering. Scope to one physical type + one nesting level (e.g. `optional list<int>`) to bound
  the search while preserving the fallback × levels × nulls interaction; make the bug genuine level/index
  accounting, not a greppable constant.

### compaction-crash-replay-gap *(re-homed from blocked `debugging`)*

- **Task shape:** repair_existing_system (symptoms-only)
- **Profile:** state_recovery_crash_consistency (LSM crash-consistent recovery)
- **Language:** Go
- **Idea:** An LSM-tree key-value store recovers without error after a compaction is interrupted
  mid-merge, but a delete tombstone stops shadowing an older same-key value because the recovery path
  loses sequence-number ordering between the surviving input SSTables and the partially written output.
  Repair the MANIFEST/WAL replay + compaction-resume logic so post-recovery reads return exactly the
  committed logical state (deleted keys stay deleted, newest write wins) for every injected crash point.
- **Hard because:** the agent must reconstruct the pre-crash committed state from heterogeneous on-disk
  evidence (MANIFEST version edits, WAL, input vs partial-output SSTables) and obey LSM sequence-number
  visibility: a tombstone with seqno *S* must hide every same-key value with seqno `< S` regardless of
  which level it lands on after a resumed compaction, and a compaction's version-edit must apply
  all-or-nothing on recovery. The bug fires only at specific interruption points (output flushed but
  version-edit uncommitted; a tombstone dropped during a bottommost compaction that wrongly assumed no
  older value remained), so it demands modeling the merge/GC invariant, not patching one branch.
- **Distinct from:** `hnsw-delete-recall` tombstones govern graph reachability, not read-visibility under
  crash recovery. Attempted `staged-snapshot-drift` is filesystem snapshot-tree drift; this is LSM
  compaction + seqno recovery (logical KV equivalence, not tree shape). Attempted `adaptive-mesh-conservation`
  is also checkpoint/restart but float conservation; this is fully discrete integer-seqno/byte-exact KV
  state. The oracle is **post-recovery-reads == pre-crash-committed-state under crash injection**, not an
  `ok:true` audit matrix.
- **Real source:** RocksDB/LevelDB compaction and recovery — MANIFEST version edits + WAL replay, internal
  keys with sequence numbers and value types (`kTypeValue`/`kTypeDeletion`), tombstone dropping during
  bottommost compaction, atomic `VersionEdit` installation; grounded in O'Neil, Cheng, Gawlick & O'Neil,
  *The Log-Structured Merge-Tree* (Acta Informatica 1996).
- ⚠️ Build the verifier as a metamorphic logical-state oracle (idealized in-memory KV map vs the store's
  post-recovery reads) plus an explicit tombstone-shadowing invariant — not a pass/fail status file. Crash
  injection must be deterministic (fixed, enumerated fault points keyed to I/O boundaries, no random
  timing). Confirm the bug is genuinely state-dependent so a trivial "always replay the full WAL" patch
  does not pass.

### trace-correlator-clock-skew *(re-homed from blocked `debugging`)*

- **Task shape:** reverse_engineering
- **Profile:** distributed_reconciliation
- **Language:** Go
- **Idea:** A local trace correlator ingests per-service span logs whose wall-clock timestamps are
  independently skewed, with retries emitting duplicate spans (same logical operation, different
  attempt/clock) and send/receive markers linking spans across services. Reconstruct the unique causal
  (happens-before) ordering and deduplicated span tree, ignoring timestamps, so the recovered DAG matches a
  hidden ground-truth lineage on every held-out trace.
- **Hard because:** correctness cannot use timestamps at all — the candidate builds the
  Lamport/vector-clock happens-before closure from structural edges (parent-child + cross-service
  send/recv) while collapsing retry duplicates without merging genuinely concurrent operations. Naive
  solutions sort by timestamp (skew breaks it), dedup by `(op-id, timestamp)` (retries differ in clock), or
  dedup by count (duplicates inflate counts) — all pass shallow checks but yield a wrong DAG. The real work
  is recovering a partial order plus a canonical tie-break that is invariant to clock skew and attempt
  count: inference over the artifact graph, not a tunable parameter.
- **Distinct from:** attempted `late-window-lineage` does streaming windowed *aggregation* matched to batch
  recompute; this does no aggregation — its oracle is **graph isomorphism to ground-truth lineage**.
  Attempted `timer-replay-coalescence` coalesces scheduled-job firings after clock jumps (scheduling
  correctness); this reconciles cross-service span causality + retry duplicates (ordering inference).
  `bitemporal-asof-correction` *trusts* two timestamp axes; this rejects timestamps entirely and infers
  order from structure.
- **Real source:** Leslie Lamport, *Time, Clocks, and the Ordering of Events in a Distributed System*
  (CACM 1978) for happens-before; Fidge (1988) / Mattern (1989) vector clocks; Google Dapper (Sigelman et
  al., 2010) and the OpenTelemetry trace/span data model (`trace_id`, `span_id`, `parent_span_id`, span
  links) for the concrete span/retry artifact format.
- ⚠️ If every span carries an unambiguous `parent_span_id` the order is trivially the tree and the task is
  EASY — engineer genuine cross-service links (send/recv markers, missing parents requiring transitive
  inference). Concurrent events form a partial order with multiple valid total orders, so the verifier must
  check the **partial order (reachability/closure) plus a deterministic canonical tie-break**, not one total
  order. Keep all inputs discrete (no float timestamp arithmetic in the oracle).

**Category: security**

### policy-canonicalization-bypass

- **Task shape:** adversarial_generalization
- **Profile:** config_policy_precedence
- **Language:** Go
- **Idea:** An HTTP authorization gateway decides allow/deny on request paths, but the policy matcher, the
  router/parser, and the audit logger each canonicalize paths differently (percent-encoded slashes,
  dot-segment collapse, merged/trailing slashes, case, unicode/overlong forms), so an attacker crafts an
  equivalent path the matcher denies-by-default yet the router serves as a protected resource. Implement one
  canonical path form shared by all three layers so deny decisions, served routes, and recorded denial
  evidence agree on every equivalence class — verified against held-out adversarial encoding fixtures.
- **Hard because:** the bug is a semantic gap between three independently-written canonicalizers, not a
  missing knob. Correctness requires defining the full equivalence relation over path encodings (RFC 3986
  normalization, percent-decoding order, dot-segment removal, slash merging, unicode normalization) and
  proving matcher, router, and audit all collapse each class to the same representative; a one-line
  `normalize()` fails because the order between decode and dot-segment removal itself creates new bypasses,
  and the audit layer must key denial evidence on the canonical form. Held-out adversarial fixtures punish
  any partial normalization, forcing the general invariant.
- **Distinct from:** `seccomp-bpf-codegen` is numeric cBPF arg-split/precedence codegen, not string
  canonicalization; `x509-path-building` is certificate-graph path search, not resource-path normalization
  (it is the nearest new-bank neighbor only via the shared `adversarial_generalization` + held-out-fixtures
  framing). Attempted `policy-revocation-shadow` bypass is *temporal* (stale epoch / negative-cache reuse
  over a delegation graph); here the bypass is *encoding-equivalence divergence across layers* with no
  time/cache dimension.
- **Real source:** Envoy `ext_authz` / RBAC path-normalization authorization bypass via encoded slashes and
  dot-segments (CVE-2021-29492; Envoy's `normalize_path` / `merge_slashes` /
  `path_with_escaped_slashes_action` settings added to close cross-component path confusion), grounded in
  RFC 3986 §6 (URI normalization/equivalence) and RFC 9110 path handling; related: Orange Tsai, *Breaking
  Parser Logic*.
- ⚠️ Fix one deterministic canonical form and a precise equivalence relation so the verifier is unambiguous;
  design held-out fixtures solvable only by the general invariant (avoid under-specification that lets a
  partial normalizer pass and over-specification that leaks the answer). Require multi-layer agreement plus
  canonical-keyed denial evidence so a single off-the-shelf `normalize()` cannot trivially pass.

**Category: scientific-computing**

### adaptive-quadrature-cache-policy

- **Task shape:** repair_existing_system (symptoms-only)
- **Profile:** floating_point_numeric_policy (deterministic numeric reproducibility)
- **Language:** Go
- **Idea:** An adaptive Gauss-Kronrod quadrature engine (QUADPACK QAGS-style global-error-budget
  refinement) with a panel-evaluation cache produces different integrals and different refinement trees
  when the same integrand is queried over the same region but with intervals supplied in a different order
  or batching. Make the engine bit-reproducible: identical integral value, identical subdivision tree, and
  identical cache contents for any permutation/re-batching of equivalent inputs.
- **Hard because:** it is not "just sort the inputs." Reproducibility needs four interacting fixes a
  canonicalization shortcut cannot satisfy together: (1) cache keys independent of arrival order and of the
  floating-point path that produced a panel; (2) a total, deterministic tie-break on the error-budget
  priority queue so refinement picks the same panels in the same sequence regardless of insertion order;
  (3) a fixed associative reduction order for summing panel contributions (a canonical tree-fold over panel
  index) so IEEE-754 non-associativity does not leak ordering into result bits; (4) an order-independent
  global convergence/tolerance test, since the adaptive stopping point is coupled to the running global
  error estimate. The shared global tolerance budget makes local decisions non-independent — that coupling
  is what defeats per-input canonicalization.
- **Distinct from:** `symplectic-adaptive-integrator` preserves structure/energy of a flow (drift-bound
  verifier); this is *bit-reproducibility of a quadrature cache across input orderings* (metamorphic-equality
  verifier). Attempted `order-independent-procgen` is spatial chunk-generation order-independence with no
  numeric reduction-order or tolerance-budget mechanism. `robust-geometric-predicates` is about the
  correctness of a *sign* on degenerate geometry, not reproducibility of an accumulated/cached result.
  `ivm-retraction-divergence` shares the metamorphic shape but over relational retractions, not float
  reduction order.
- **Real source:** QUADPACK (Piessens, de Doncker-Kapenga, Überhuber & Kahaner, *QUADPACK: A Subroutine
  Package for Automatic Integration*, Springer 1983) — the QAGS/QAG adaptive Gauss-Kronrod routines with a
  global error-budget worklist, as re-implemented in GSL (`gsl_integration_qags`) and SciPy
  (`scipy.integrate.quad`); the reduction-order/non-associativity angle mirrors N. Higham, *The Accuracy of
  Floating Point Summation* (SIAM J. Sci. Comput., 1993).
- ⚠️ Forbid FMA contraction and any concurrency in the reduction so Go yields bit-identical doubles; pin
  `GOARCH` and use closed-form polynomial/rational integrands (pure-arithmetic Gauss-Kronrod node
  evaluations) so bit-equality is well-defined. Design integrand/tolerance regimes so the global-budget
  coupling genuinely forces an order-independent priority-queue + budget redesign (not "sort + canonical
  fold"), with adversarial held-out orderings/batchings. Verify **exact integral bits AND the serialized
  refinement tree/cache**, not a tolerance band.

### Exclusion log (22 of 29 dropped)

Filters: **dup-attempted** = near-duplicate or direct seed of an already-attempted task (originality
floor); **collides-newbank** = same mechanism as an existing new-bank idea; **redundant-template** =
another instance of the matrix→`audit.json`→replay/restart/snapshot-drift repair mold. Blocked-category
seeds (`software-engineering`/`debugging`) are noted where that compounded the verdict.

| Excluded idea | Legacy origin | Verdict | Collides / duplicates |
|---|---|---|---|
| cross-toolchain-cache-poison | build / pending | dup-attempted | `abi-feature-backtrack` (stale-cache repair family; new-bank build ideas are resolution-semantics, not cache) |
| journaled-quota-resurrection | system-admin / seed | dup-attempted + redundant-template | `staged-snapshot-drift` (quota rollover + restart + state drift) |
| mount-propagation-epoch-cleanup | system-admin / seed | collides-newbank | `overlayfs-whiteout-flatten` (Go userspace reimpl of a Linux kernel VFS subsystem vs kernel ground truth) |
| service-unit-env-precedence-drift | system-admin / seed | redundant-template | precedence-across-restart/reload variant; echoes `timer-replay-coalescence` |
| split-toolchain-provenance-lock | build / seed | dup-attempted | `abi-feature-backtrack` (incremental build-cache invalidation; also C++-coupled) |
| abi-cache-relink-drift | build / seed | dup-attempted | `abi-feature-backtrack` (identical stale-ABI-after-feature-flag mechanism) |
| window-lineage-replay | data / seed | dup-attempted | `late-window-lineage` (same system, hook, and verifier shape) |
| cdc-tombstone-merge-order | data / seed | redundant-template | reorder-convergence template with a CDC noun; near `ivm-retraction-divergence` / `late-window-lineage` space |
| rollback-input-fork | games / seed | dup-attempted | `rollback-combat-desync` (deterministic rollback input-ordering, trace/hash oracle) |
| ecs-authority-snapshot-drift | games / seed | redundant-template | stale-snapshot-restore-repair mold; echoes `staged-snapshot-drift` / `rollback-combat-desync` |
| pathfinder-replay-cost-skew | games / seed | redundant-template | replay-determinism mold; near attempted `rollback-combat-desync`, distinct-but-thin vs `order-independent-procgen` |
| hot-reload-epoch-shadow | software-eng / seed | dup-attempted (+ blocked cat) | `module-hot-reload-epoch` (plugin hot-reload + module-cache epochs, near-verbatim) |
| incremental-type-index-phantom | software-eng / seed | dup-attempted (+ blocked cat) | `incremental-index-invalidation` (stale/phantom defs after incremental invalidation) |
| plugin-capability-contract-leak | software-eng / seed | dup-attempted (+ blocked cat) | `policy-revocation-shadow` (capability-attenuation over dependency edges) |
| optimizer-checkpoint-alias-drift | machine-learning / seed | redundant-template | echoes `autograd-tape-alias` (ML alias-tracking) + resume/restart state-drift mold; float-determinism risk |
| quantized-calibration-split-leak | machine-learning / seed | dup-attempted | `quantized-beam-alignment` (quantization state leaking across batches; float flakiness) |
| feature-store-backfill-poisoning | machine-learning / seed | collides-newbank | `bitemporal-asof-correction` (stripped of ML vocab it is point-in-time-correct retrieval) |
| async-finalizer-shadow | debugging / seed | dup-attempted (+ blocked cat) | `async-executor-liveness` (cancellation + bounded queues + nested spawn) |
| delegated-token-revocation-lag | security / seed | dup-attempted | `policy-revocation-shadow` (delegation chains + batch eval + negative-cache reuse) |
| archive-attestation-confused-root | security / seed | dup-attempted | `artifact-provenance-timewarp` (offline verifier defeated by mirror rollback + key rotation) |
| stencil-halo-checkpoint-drift | scientific-computing / seed | dup-attempted | `adaptive-mesh-conservation` (AMR + checkpoint restart + boundary bookkeeping; restart-drift mold) |
| sparse-preconditioner-lineage | scientific-computing / seed | dup-attempted | `sparse-block-preconditioner` (stale/desynced preconditioner, false convergence) |

### Promoted-set distribution

- **Languages:** Rust (2) — column-shard-rehydrate, dictionary-rollover-nesting; Go (5) —
  pkgconfig-sysroot-shadow, compaction-crash-replay-gap, trace-correlator-clock-skew,
  policy-canonicalization-bypass, adaptive-quadrature-cache-policy.
- **Categories:** build-and-dependency-management (1), data-processing (4, incl. 2 re-homed from blocked
  `debugging`), security (1), scientific-computing (1).
- **Task shapes:** repair_existing_system (4), reverse_engineering (2), adversarial_generalization (1).
- ⚠️ **Adjacency to resolve before authoring:** `column-shard-rehydrate` and `dictionary-rollover-nesting`
  are both Parquet/Dremel nested-record reconstruction tasks (different triggers — row-group split + cross-
  shard dictionary reuse vs. mid-chunk dictionary-cap fallback). They pass the new-bank collision filter
  independently, but to avoid a templated-pair impression, ship at most one in any single submission batch
  and keep the other as a backup, or sharpen the trigger contrast further at Step 2a.
