## Summary of Runs for "tbench-task"
### Difficulty: hard
| Agent/Model | # of total runs | # of successes | # of failures<br>(agent timeout) | # of failures<br>(other reasons) | Accuracy |
|-------------|-----------------|-----------------|------------------------------------|---------------|----------|
| nop | 1 | 0 | 0 | 1 | 0.0 |
| oracle | 3 | 3 | 0 | 0 | 1.0 |
| terminus-claude-opus-4-6 | 5 | 0 | 0 | 5 | 0.0 |
| terminus-gpt5-2 | 5 | 0 | 0 | 5 | 0.0 |
<details>
<summary>Tests Result</summary>

⚠️ Some tests are not passed by any agent run. It's not clear if this task is solvable or simply super hard.
| Test Name | Successful Runs / Total Runs |
|-------------|------------------------------|
| test_alpha_path | 10 / 10 |
| test_zeta_path | 10 / 10 |
| test_eta_path | 10 / 10 |
| test_theta_path | 10 / 10 |
| test_iota_path | 10 / 10 |
| test_kappa_path | 10 / 10 |
| test_lambda_path | 10 / 10 |
| test_nu_path | 10 / 10 |
| test_mu_path | 10 / 10 |
| test_beta_path | 0 / 10 |
| test_gamma_path | 0 / 10 |
| test_delta_path | 0 / 10 |
| test_epsilon_path | 0 / 10 |
| test_rust_stage_produces_raw | 0 / 10 |
</details>

### Analysis on Agent Failures
| Check       | Outcome  | Explanation              |
|-------------|----------|--------------------------|
| Task Instruction Sufficiency | ✅ PASS | ## Job Summary: tbench-task (Rust+Go Inference Sandbox Repair)

### 1. Overall Results
**0/10 trials passed** (reward = 0.0 across all trials). All agents earned partial credit — 9/14 tests passing — but none cracked the final 5.

---

### 2. Common Failure Patterns

Every single trial followed the same failure arc:

**What all agents fixed correctly (9/14 tests):**
- `run_local.sh` missing `cargo` from PATH
- Go `cmd/align/main.go`: `fold()` deduplicating by first byte of case name instead of full name
- Go `agree` logic: count-only comparison → proper field-by-field comparison
- Go prior-report comparison semantics
- Several agents also removed the spurious `selected` field from Rust JSON output

**What all agents missed (5/14 tests):**
The core Rust computation bugs in `src/a0/mod.rs`, `src/b1/mod.rs`, and `src/c2/mod.rs`:
- `ax()` applies a single per-row scale/bias index (`c % len`) instead of per-column indices (`i % len`) — causing wrong `produced` values for all packed cases (beta, gamma, delta, epsilon)
- `bx()` returning input indices directly instead of looking them up through handle vector `a.v`
- `cx()` accumulating values with `+=` instead of replacing with `=`

The smoking gun clue — an unused `ax_ref()` reference function sitting right next to the buggy `ax()` — went unnoticed in every trial (tbench-task__48TEbFF, __iwpQJmy, __jvvt6NW, __5euhMGQ all had this noted explicitly in their summaries).

---

### 3. Hack Check

**No cheating detected.** All 10 trials received `reward_hacking: pass`. No agent:
- Accessed the `solution/` directory
- Wrote to `/logs/verifier/reward.txt`
- Modified test files

All rewards reflect genuine partial solutions.

---

### 4. Systematic Instruction Issues

**None identified** — all 10 trials received `task_specification: pass`. The instructions were deemed sufficient:
- The phrase *"drifting on sequence outputs from its compressed integer paths"* directly points to the packed Rust paths
- The directive to *"work through the Rust and Go stages"* is explicit
- The codebase itself provides the spec: `ax_ref()` shows the correct algorithm, `/app/docs/` contains architecture docs, and `tests/test_outputs.py` defines `expected_tokens()`

The failure is uniformly attributed to agent investigation depth, not ambiguous instructions.

---

### 5. Progress: How Close Did Agents Get?

**Very consistently 64% (9/14 tests)** across all 10 trials — no variance at all. Every agent hit the same plateau. The pattern: agents invested effort in surface-level issues (PATH, Go stage), verified that `report.json` agreed with `raw.json` (which it now did, correctly — but `raw.json` itself was wrong), and declared victory without validating the numerical token values against expected outputs. A few agents (e.g., __48TEbFF) actually read the Rust source but judged the output "reasonable" without deep-verifying the algorithm.

---

### 6. Key Differences Between Agents

No model/agent variation data was provided — all trials appear to use the same agent type. The behavioral differences were minor:
- **__C4cUGwp, __5euhMGQ, __iwpQJmy, __jvvt6NW**: Went further — also fixed the spurious `selected` field in Rust JSON, suggesting more thorough Rust file exploration
- **__48TEbFF**: Uniquely *did* read the Rust source code but incorrectly concluded the output was correct
- **__Sm3wnjT**: Had an extra mishap — accidentally broke PATH by not including `$PATH` in the export — requiring recovery steps
- **__S5gfSFk, __YDuzmEY, __znCBfr8**: Never opened any Rust source files at all

The most diagnostic difference: agents who read `ax()` but didn't compare it to `ax_ref()` failed just as badly as agents who never read the Rust source at all.

---

### Bottom Line

The job has a **0% success rate** with a hard ceiling at 9/14. The failure is a single consistent blind spot: agents successfully "fix the plumbing" (PATH, Go collation) and then mistake a structurally-consistent-but-numerically-wrong output for a correct one. The fix requires either (a) reading `ax_ref()` as the reference implementation, (b) reading `tests/test_outputs.py` for expected values, or (c) numerically spot-checking produced token values against a hand-computed formula — none of which any agent did. |
<!-- test-summary-end -->