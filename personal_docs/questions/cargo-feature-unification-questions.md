# Submission Questions — cargo-feature-unification

Authored answers to the three TB3 submission questions (Difficulty, Solution,
Verification). Each answer is 1-2 paragraphs, grounded in the built task
(`tasks/cargo-feature-unification`): the five staged passes `m1`-`m5`, the
`r6`-`r8` decoys, the independent Python resolver-v2 verifier, and the empirical
result (GPT-5.5 0/5, fail-good, HARD / trust HIGH).

## 1. Difficulty Explanation

> Describe in your own words why your task is challenging for humans and agents to solve.

The engine builds and runs, and the output looks plausibly correct: it emits a plain transitive union of features, which is the right answer for every easy case where Cargo's lanes agree. The only evidence the solver gets (observed.json) covers exactly those lane-agreeing cases, so naive validation passes and the bug stays hidden until you hit inputs where resolver-v2's rules diverge from a flat union. The fix frontier is opaque too: five identically-named apply stubs with no answer key, so an agent can't pattern-match a fix and has to reverse-engineer the real model from the docs and the engine's behavior.

It's hard rather than just tedious because five independent resolver-v2 concerns interact, and each one fails silently on its own: default-feature drop/expand, lane non-unification (target/host/dev don't merge), cfg() target gating, dep: namespacing, and the weak pkg?/feat least-fixpoint. Fix four of them and it still fails, because the fifth keeps emitting the naive union, and there's no intermediate signal for which concern is still wrong. The sharpest trap is the coupling between lane-scoping and dep: namespacing on the host lane: an agent that gets lanes right but mishandles a namespaced dependency on the build graph drops a feature (ser) and fails only the comprehensive case. That's where GPT-5.5 failed all five trials. The weak fixpoint is a second non-local trap, since whether a weak reference fires depends on whether some other, possibly later-activated path makes its dependency live, so a single forward pass gets it wrong.

## 2. Solution Explanation

> Describe your high-level approach to this task and key insights in forming the solution.

The engine is a pipeline. It parses the workspace manifests into a graph of edges, where each edge carries its lane/kind, cfg guard, default-features flag, optional flag, and requested features. Then it runs five staged passes over that graph, closes the feature set to a fixpoint, and emits each crate's sorted, de-duplicated feature list. Solving the task means filling in the five stub apply bodies so each pass implements one resolver-v2 rule. m1 (defaults): an edge contributes default only if it keeps default-features, and a kept default expands into its member features before propagating. m2 (lanes): out-of-lane edges are marked not-kept, so the target, host, and dev contexts never unify and build-only or dev-only deps can't leak into the target lane. m3 (cfg): an edge participates only when its cfg(...) predicate holds for the queried triple, evaluated by guard_holds. m4 (dep:): per crate, the dependency names referenced through dep: tokens are masked, so the implicit same-name feature is suppressed and the bare dep name isn't surfaced as a feature. m5 (weak): a least-fixpoint loop that lets a weak pkg?/feat token fire only once its dependency is independently live, iterating until nothing changes.

These operations belong at different stages relative to closure. Lane partition and cfg gating prune the graph before the feature set is closed. dep: namespacing rewrites what counts as a feature in the first place. Only the weak rule needs iteration, because activation can cascade. Getting the ordering right is the hard part: prune, then rewrite, then close, then resolve weak references to a fixed point. The rest follows from implementing each rule faithfully against the documented model.

## 3. Verification Explanation

> Explain how your tests are verifying correctness.

The verifier (tests/test_outputs.py) has an independent Python implementation of resolver-v2, a separate port rather than a copy of the Rust engine, so a bug shared between the engine and the checker can't slip through both. For each test it builds held-out workspaces (not the data/ workspaces the solver can inspect), runs the agent's engine on them through run.sh, and asserts that the engine's entire output dictionary equals the independently recomputed resolution, across multiple target triples and lanes. Because it compares the whole dict rather than spot-checking membership, hard-coding the visible samples can't pass: the expectations are regenerated on workspaces the solver never saw.

The coverage is laid out to localize failure. Each of the five concerns has its own held-out workspaces that isolate it: default drop and transitive expand, host/dev lane separation, cfg included vs excluded, namespaced single and paired, and weak dormant / two-refs / activates. There's also an all-lanes test that exercises the laneÃdep: coupling. A partial engine then fails exactly the subset of tests for the rules it hasn't fixed, and nothing else. Ablation backs this up: the correct oracle passes all 15 tests deterministically (confirmed over 20 repeats), the naive engine fails, and reverting any single stage flips only that stage's tests. That last property is what makes the per-concern difficulty signal trustworthy.
