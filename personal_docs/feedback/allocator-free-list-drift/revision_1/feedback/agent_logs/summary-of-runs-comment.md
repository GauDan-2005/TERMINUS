## Summary of Runs for "tbench-task"
### Difficulty: hard
| Agent/Model | # of total runs | # of successes | # of failures<br>(agent timeout) | # of failures<br>(other reasons) | Accuracy |
|-------------|-----------------|-----------------|------------------------------------|---------------|----------|
| nop | 1 | 0 | 0 | 1 | 0.0 |
| oracle | 3 | 3 | 0 | 0 | 1.0 |
| terminus-claude-opus-4-6 | 5 | 5 | 0 | 0 | 1.0 |
| terminus-gpt5-2 | 5 | 0 | 0 | 5 | 0.0 |
<details>
<summary>Tests Result</summary>

✅ This task is solvable by the agents.
| Test Name | Successful Runs / Total Runs |
|-------------|------------------------------|
| test_a0 | 5 / 10 |
| test_b1 | 8 / 10 |
| test_c2 | 5 / 10 |
| test_d3 | 9 / 10 |
| test_e4 | 5 / 10 |
| test_f5 | 9 / 10 |
| test_g6 | 5 / 10 |
| test_h7 | 5 / 10 |
| test_i8 | 10 / 10 |
| test_j9 | 10 / 10 |
| test_k0 | 5 / 10 |
| test_l1 | 9 / 10 |
</details>

### Analysis on Agent Failures
| Check       | Outcome  | Explanation              |
|-------------|----------|--------------------------|
| Task Instruction Sufficiency | ❌ FAIL | ## Job Summary

### 1. Overall Results
**0/5 trials passed** — every agent received a final reward of **0.0**. No agents (including GPT-5.2 in `QJ7BGKG`) succeeded. All trials share the same failure root cause.

---

### 2. Common Failure Patterns

**Universal failure mode — surface validation mistaken for correctness:**
Every agent followed the same flawed debugging arc:
1. Ran `run-matrix.sh` / `run-one.sh` → exit code 0 ✓
2. Validated JSON schema (required fields present) ✓
3. Confirmed determinism (two runs identical) ✓
4. **Declared victory** — never checked numerical values against the reference model

None of the agents consulted `/tests/test_outputs.py`, where the `ModelArena` reference implementation defines the expected values. They treated the allocator's self-reported `ok: true` as ground truth.

**Bugs that were never fixed (across all 5 trials):**
| Bug | Location | Symptom |
|---|---|---|
| Off-by-8 byte accounting | `acct_e/acct.c` | `byte_total` inflated (e.g., 264 vs 240 for cedar) |
| Broken bidirectional coalescing | `list_b/list.c` | `fl_count` too high (slate: 2 vs 1, pearl: 3 vs 2) |
| Wrong footer position | `pool_a/tag.c` | Downstream accounting errors |
| Buggy memory copy | `move_d/move.c` | Wrong `byte_total` for realloc (onyx: 1504 vs 1464) |

**Self-inflicted regression (2 trials):**
`QJ7BGKG` and `5e4xtC2` both independently rewrote `flow_g/report.c` to remove the `{"cases": [...]}` array wrapper from `run-one.sh` output — introducing a `test_b1` failure that didn't previously exist. Both agents misread the "same rules" instruction as a bug rather than a format requirement.

**One agent misdiagnosed the problem entirely:**
`WpMWU7F` concluded the issue was non-determinism from free-list traversal order and replaced the simple `sig += total * 17` accumulation with a MurmurHash-style XOR scheme, producing cryptographically-large values (e.g., `17721717616631236708`) instead of expected small integers (e.g., `4080`). This caused 9/12 tests to fail — the worst outcome.

---

### 3. Hack Check

**No cheating detected in any trial.** All 5 trials passed `reward_hacking` checks. No agent accessed the solution directory, modified test files, or wrote to reward files. Failures are genuine capability limitations.

---

### 4. Instruction Issues

**2/5 trials flagged `task_specification: fail`:**

- **`QJ7BGKG`**: The phrase "under the same rules" for `run-one.sh` output format was ambiguous. The agent reasonably interpreted it as consistency properties rather than structural format (the `cases` array wrapper). This gap directly caused a test failure from an otherwise-reasonable design decision.

- **`WpMWU7F`**: The instruction never specifies the exact formulas for `heap_sig` (sum over *allocated* blocks, not free blocks), `fl_sig`, or `byte_total`. These are only encoded in the test file's `ModelArena` reference implementation. The agent's interpretation of "drift" as non-determinism was plausible given only `instruction.md`. **This is a meaningful spec gap** — the correct fix required knowing precise reference formulas that weren't documented in the instructions.

The 3 trials that passed the spec check (`CJuwXnm`, `qm9XpuJ`, `5e4xtC2`) failed due to agent capability limitations, not missing information.

---

### 5. Progress (How Close Did Agents Get?)

All agents reached the same ~40% milestone before stalling:

| Milestone | All 5 Agents |
|---|---|
| Scripts execute without crash | ✅ |
| Valid JSON schema, all required fields | ✅ |
| Deterministic across runs | ✅ |
| Read C source files for algorithmic bugs | ❌ |
| Consulted `/tests/test_outputs.py` reference model | ❌ |
| Fixed `byte_total` accounting | ❌ |
| Fixed coalescing (`fl_count`) | ❌ |

The closest any agent got to an actual fix was `qm9XpuJ`, which at least rebuilt the binary from source (resolving a stale-binary `ledger=null` symptom), but still didn't dig into algorithmic correctness.

---

### 6. Key Differences Between Agents

Only `QJ7BGKG` is identified as GPT-5.2; the others appear to be Claude-based. Notably:
- GPT-5.2 (`QJ7BGKG`) and one Claude agent (`5e4xtC2`) made the *identical* misdiagnosis about `run-one.sh` format — suggesting this is a common trap in the task design, not model-specific.
- `WpMWU7F` was the outlier in attempting an actual source-level fix (albeit the wrong one), which paradoxically produced the worst score (9/12 failures vs. 6-7/12 for others that made no changes).
- No agent demonstrated a materially superior debugging strategy; the failure mode was uniform across models.

**Bottom line:** The task requires reading the test reference implementation as a spec, which no agent did. Prompting agents to explicitly consult `/tests/test_outputs.py` before drawing conclusions would likely be the highest-leverage intervention. |
<!-- test-summary-end -->