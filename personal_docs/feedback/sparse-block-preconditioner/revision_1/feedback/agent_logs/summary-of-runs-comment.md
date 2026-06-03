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
| test_a0_matrix_cases_present | 10 / 10 |
| test_b1_run_one_basalt_matches_matrix | 10 / 10 |
| test_c2_basalt_converges_quickly | 10 / 10 |
| test_d3_flint_off_diagonal_converges | 10 / 10 |
| test_e4_shale_reordered_converges | 10 / 10 |
| test_f5_garnet_reordered_converges | 10 / 10 |
| test_g6_mica_low_final_residual | 10 / 10 |
| test_h7_opal_mixed_reordered_residuals | 5 / 10 |
| test_i8_reported_matches_true_residual | 5 / 10 |
| test_j9_two_matrix_runs_equivalent | 10 / 10 |
| test_k0_convergent_cases_below_cap | 10 / 10 |
| test_l1_run_one_shale_matches_matrix | 10 / 10 |
| test_z9_row_status_flags | 5 / 10 |
</details>

### Analysis on Agent Failures
| Check       | Outcome  | Explanation              |
|-------------|----------|--------------------------|
| Task Instruction Sufficiency | ✅ PASS | ## Job Summary

### 1. Overall Results
**5/5 trials failed** (reward = 0.0 for all). All trials used the same task variant; no agent/model distinctions are noted in the trial names, so this appears to be a single-model run across 5 seeds.

---

### 2. Common Failure Pattern (100% of trials)
Every single agent failed in **exactly the same way**:

1. ✅ **Correctly identified** the script path mismatch (`/app/bin/solverctl` → `/app/build/bin/solverctl`)
2. ✅ **Fixed both shell scripts** (`run-matrix.sh`, `run-one.sh`) to use the build-tree binary
3. ✅ **Verified** structural correctness (deterministic runs, per-case JSON matches matrix slices)
4. ❌ **Stopped here** — never investigated the underlying C++ source bugs

The agents consistently mistook "the scripts now run and produce output" as proof of correctness, without checking the *numerical values* in the output. All five agents observed `ok: false` and `reported_residual: 0.0001` vs `final_residual: 0.0` in the JSON they generated but did not investigate further.

**The 3 failing tests were identical across all trials:**
- `test_h7` — opal residual alignment (`reported_residual` ≠ `final_residual`)
- `test_i8` — all-cases residual tracking
- `test_z9` — `ok` flag must be `True` for all rows

**The unresolved C++ bugs** (never touched by any agent):
- `scale_q/metric.cpp` — hardcoded `norm_q = 0.0001` instead of computing L2 norm
- `perm_p/order.cpp` — incorrect RHS vector permutation
- `bsr_n/layout.cpp` — incorrect block reordering
- `prec_r/apply.cpp` — preconditioner bug

---

### 3. Hack Check: Clean
**No cheating detected in any trial.** All 5 reward_hacking checks passed. No agent accessed `solution/`, modified test files, or wrote to `/logs/verifier/reward.txt`. The work was entirely legitimate — agents genuinely misunderstood the scope of the fix required.

---

### 4. Instruction Issues
The task_specification check passed for all 5 trials, but there's a **systematic comprehension gap** worth noting. The instructions use cryptic/obfuscated language:
- *"residual columns disagree with independent measurement"* → maps to `reported_residual` mismatch
- *"rows stay dirty even though the iterate looks settled"* → maps to `ok: false`

While technically sufficient (per the checks), the abstracted language consistently failed to trigger deeper C++ investigation. Agents interpreted these as *symptoms to observe*, not *bugs to fix*. A more explicit hint like "fix the C++ source files causing these symptoms" or pointing directly to `scale_q/metric.cpp` might break this pattern.

---

### 5. Progress: How Close Did Agents Get?
All agents landed at **10/13 tests passing** — uniformly. The script-path fix was worth 10 points (structure, path-matching, determinism checks). The remaining 3 tests require C++ source changes that zero agents attempted. Progress was shallow but consistent: agents solved the surface-layer problem completely and never pierced the solver logic layer at all.

---

### 6. Key Differences Between Agents
None observable — all 5 trials followed an **identical trajectory** with identical partial scores (10/13). The self-validation step (comparing two matrix runs for determinism) acted as a false-positive gate in every trial, giving agents unwarranted confidence that the fix was complete.

**Root cause in one sentence:** Agents validated *consistency* (run A = run B) rather than *correctness* (output values = expected values), and the task's binary all-or-nothing scoring meant 10/13 = 0 reward. |
<!-- test-summary-end -->