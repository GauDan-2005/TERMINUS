You are working on a single Terminal-Bench task that was rated **trivial**, **easy**, or **medium** on the platform, or that failed because tests were broken, hidden, or not genuinely engineering-hard.

Your primary objective is to transform this task into a **genuinely HARD** Terminal-Bench task (worst-model pass rate target **≤ 20%**) with **fair, genuine tests** that satisfy Edition 2 requirements and pass all repo-local gates.

Before making any changes:

1. Carefully analyze the entire benchmark summary/report for this task.
2. Study the unit-test results in detail.
3. Identify:
   - Tests solved consistently by agents (easy/trivial tests) — **replace completely**
   - Tests partially solved (medium-value — harden with real coupling, not trick questions)
   - Tests rarely solved (preserve if they test real engineering)
   - Common agent failure patterns
   - Root causes of success and failure
   - Whether difficulty collapsed because of **instruction cheating** (answer recital, polarity contradiction, undefined jargon) or **test cheating** (hidden contracts, oracle-only paths, chain-dependent assertions)
4. Use the benchmark summary as the primary signal when deciding what to preserve, replace, or redesign.

## Hard-only acceptance bar (BLOCKING)

- `task.toml` must keep `difficulty = "hard"`.
- Target **platform HARD** per `@difficulty-calibration.mdc` Part E: worst-model accuracy **≤ 20%** after agent runs.
- If `hard_difficulty_predictor.py` predicts worst-model pass **> 20%** for a Python task, **redesign** — do not ship.
- A task that passes oracle/NOP but agents score >60% on the worst model is **too easy** — redesign, not relabel.

## Blocked categories (BLOCKING)

These `task.toml` categories are **permanently blocked** for new tasks:

- `software-engineering`
- `debugging`

If the task uses either category, **remap** to an accepted category before any other work:

| Blocked | Remap to |
|---------|----------|
| `software-engineering` | `build-and-dependency-management`, `data-processing`, `games`, `machine-learning`, or `system-administration` |
| `debugging` | Same accepted set; keep `task_shape = repair_existing_system` if diagnosis-and-repair is the work |

Also reject proximity to blocked categories:

- Do not keep tags, titles, or framing that exist only because the task is "a debugging exercise."
- Do not use `profile_name: debugging` or challenge families that assume the blocked category label.
- Repair/debug work is fine; the **category metadata** must be an accepted domain.

Run after category fix:

```bash
python3 scripts/lint_spec.py specs/<task-name>.md --strict   # if spec exists
./scripts/check-task.sh --strict tasks/<task-name>
```

## Difficulty Requirements

The goal is NOT to make the task larger.

The goal is to make the task genuinely difficult for frontier models through **realistic engineering complexity** that survives an **honest instruction** (every tested behavior documented in `instruction.md` or visible env — never only in tests).

Difficulty must come from:

- State recovery
- Replay semantics
- Cache invalidation
- Journal reconstruction
- Persistence across runs
- Ordering-sensitive behavior
- Multi-component interactions
- Runtime invariants
- Cross-module dependencies
- Long debugging chains
- Delayed-effect bugs
- Corruption recovery
- Recovery/replay correctness
- Build/runtime workflow complexity
- Design search under constraints (non-repair shapes)
- Adversarial generalization / variant ladders
- Formal correctness obligations

Difficulty must NOT come from:

- Hidden requirements
- Undocumented constants
- Undocumented formulas
- Test reverse-engineering (agents reading `tests/` to learn the contract)
- Hardcoded outputs
- Artificial ambiguity or undefined metaphor jargon with no env anchor
- Trivial bug multiplication
- Random complexity
- Impossible-to-discover behavior
- Instruction answer recital (GX9) or polarity contradiction (GX10)
- Timing/latency thresholds

## Genuine test requirements (BLOCKING)

Every test must be **genuine**: it verifies real engineering outcomes, not oracle imitation or hidden specs.

For each test function, confirm:

1. **Discoverability** — every asserted field, formula, tolerance, and schema is documented in `instruction.md` or visible env code/docs (CR9/GX7/GX8).
2. **Independence** — the test passes without requiring unrelated parts of the solution to be complete first (Part B3).
3. **Multiple valid approaches** — at least two reasonable implementations should pass core tests (Part B5).
4. **No oracle-only paths** — partial-oracle ablations must fail on **behavior**, not compile-only breakage (Part B4).
5. **No chain-dependent gates** — no test requires the full solution stack in exact order unless the prerequisite is established in the environment setup.
6. **Property-based where possible** — prefer derived hashes, metamorphic checks, round-trips, cross-run invariants over exact oracle literals when alternatives are valid.

For tests agents solve consistently:

- **Replace them completely** — do not lightly harden.
- Replace with tests requiring deeper reasoning across **≥3 coordinated locations** (flipping_point_contract).

For tests that are already difficult:

- Preserve them.
- Expand only if doing so increases meaningful engineering complexity.

Add difficult tests covering:

- Replay correctness
- Recovery correctness
- Corruption recovery
- Persistent state reconstruction
- Ordering-sensitive workflows
- Delayed validation
- Runtime invariants
- Cross-command consistency
- Multi-stage workflows
- Multi-run behavior
- Cross-subsystem interactions
- State migration
- Cache invalidation
- Variant-ladder arms (adversarial generalization)

## Architecture Requirements

Avoid tasks that can be solved by:

- Editing one function
- Editing one file
- Following a single failing assertion
- Grepping for a constant
- Simple search-and-replace

The final task should require:

- Understanding multiple modules
- Tracing state across components
- Fixing interacting bugs (repair) or design search under coupling (non-repair)
- Maintaining consistency across workflows
- Understanding system behavior over time
- Fix frontier spread across **≥3 distinct roots** with no single location controlling >50% of tests

## Language Requirements

If the task is implemented primarily in Python and Python makes the task easy, locally patchable, or scriptable:

- Rebuild the core implementation using a stronger systems-oriented language when it materially increases difficulty:
  - Rust, C++, Go, C, Zig, Java
- Only keep Python for minimal verifier/test glue if necessary.

If language migration does not meaningfully increase difficulty, do not migrate — strengthen coupling and tests instead.

Non-Python tasks still must target HARD empirical difficulty.

## Edition 2 Compliance

Ensure:

- No hidden contracts
- No undocumented behavior
- No verifier-only requirements
- No test-only specifications
- Spec-test alignment remains correct (`spec_test_alignment`, `spec_gap_detector`)
- Oracle remains valid
- Deterministic behavior is preserved
- Reviewer compliance is maintained
- `allow_internet = false`; verifier deps baked in Dockerfile
- Collapse stack passes: `scripts/collapse_check.py` (RC1–RC8, CR*, GX1–GX10)

## Additional Fixes

Fix any reviewer issues found in the task, including:

- Docker/runtime image issues
- Rubric issues
- task.toml issues (category, difficulty, timeouts ≤1800s)
- test.sh offline compliance
- verifier compliance issues
- sandbox compliance issues
- infrastructure-related issues
- Similarity/template risk if >25% overall or >35% on any axis

## Validation

After all modifications, run the full gate chain:

```bash
python3 scripts/lint_spec.py specs/<task-name>.md --strict          # if spec exists
python3 scripts/spec_satisfiability.py specs/<task-name>.md --task-dir tasks/<task-name> --strict
python3 scripts/hard_difficulty_predictor.py tasks/<task-name>
python3 scripts/task_gate.py tasks/<task-name> --strict --skip-harbor
./scripts/check-task.sh --strict tasks/<task-name>
python3 scripts/harbor_gate.py tasks/<task-name> --oracle --oracle-stress 3 --nop --nop-stress 3
python3 scripts/collapse_check.py tasks/<task-name>
python3 scripts/reviewer_simulation.py tasks/<task-name>           # reviewer_confidence >= 90
```

Verify:

1. Oracle passes.
2. NOP scores 0.0.
3. Collapse checks pass (no FAIL on RC/GX/CR).
4. Static checks pass (including blocked category rejection).
5. Reviewer requirements satisfied.
6. Task remains solvable by at least one strong agent.
7. Task is substantially harder than the original benchmark version.
8. Tests are genuine — no hidden contracts, no oracle-only discrimination.

Escalate to `scripts/verifier_health.py` if agents score 0% without `verifier_did_not_run`, or if partial-oracle evidence is weak.

## Deliverables

After completing the work:

1. Apply all required fixes.
2. Rebuild and validate the task.
3. Create the final submission-ready ZIP according to repository rules.
4. Provide the final rubric in chat only.
5. Output the rubric in the required format inside a separate copy block.
6. Do not leave any known reviewer, verifier, oracle, rubric, Docker, category, difficulty, or test-genuineness issues unresolved.
