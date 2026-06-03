## Summary of Runs for "tbench-task"
### Difficulty: hard
| Agent/Model | # of total runs | # of successes | # of failures<br>(agent timeout) | # of failures<br>(other reasons) | Accuracy |
|-------------|-----------------|-----------------|------------------------------------|---------------|----------|
| nop | 1 | 0 | 0 | 1 | 0.0 |
| oracle | 3 | 3 | 0 | 0 | 1.0 |
| terminus-claude-opus-4-6 | 5 | 5 | 0 | 0 | 1.0 |
| terminus-gpt5-2 | 5 | 1 | 0 | 4 | 0.2 |
<details>
<summary>Tests Result</summary>

✅ This task is solvable by the agents.
| Test Name | Successful Runs / Total Runs |
|-------------|------------------------------|
| test_audit_file_written | 10 / 10 |
| test_case_row_clean[rook] | 10 / 10 |
| test_case_row_clean[bishop] | 10 / 10 |
| test_case_row_clean[knight] | 10 / 10 |
| test_case_row_clean[lancer] | 10 / 10 |
| test_case_row_clean[sentinel] | 10 / 10 |
| test_case_row_clean[warden] | 10 / 10 |
| test_case_row_clean[ranger] | 10 / 10 |
| test_single_case_parity | 10 / 10 |
| test_path_sig_match_01 | 10 / 10 |
| test_step_geometry_03 | 10 / 10 |
| test_target_visibility_02 | 10 / 10 |
| test_modifier_active_05 | 6 / 10 |
| test_jsonl_order_04 | 10 / 10 |
| test_trace_align_06 | 10 / 10 |
| test_driver_binary_present | 10 / 10 |
</details>

### Analysis on Agent Failures
| Check       | Outcome  | Explanation              |
|-------------|----------|--------------------------|
| Task Instruction Sufficiency | ❌ FAIL | ## Job Summary

### 1. Overall Results
**All 4 trials failed (reward = 0.0).** Every trial was stopped by the same single test: `test_modifier_active_05`. No trial achieved a passing score. The one trial where a model was named (tbench-task__NBRGFaP, **gpt-5.2**) was the only one that made meaningful progress; the other three trials used unidentified agents that made zero code changes.

---

### 2. Common Failure Pattern
The failure is perfectly uniform across all trials: **15/16 tests pass, `test_modifier_active_05` fails.** The test asserts `ward[0]["active"] is True` for the "sentinel" case after a save/restore cycle. The root cause is an off-by-one error in `mod/effect.go` (the `ExpiryTurn`/`SyncBoundary` function uses `currentTurn + rem - 1` instead of `currentTurn + rem`), causing the ward modifier to appear expired one turn too early on the resume path.

Three of four agents never found this file. The fourth found everything *except* this file.

---

### 3. Hack Check: Clean Sweep
**No cheating detected in any trial.** All four trials received `reward_hacking: pass`. Agents operated legitimately — reading source files, running the matrix script, and inspecting output JSON. No agent touched `solution/`, modified test files, or wrote to `reward.txt`.

---

### 4. Systematic Instruction Issue
This is the most significant finding: **all four trials received `task_specification: fail`**, pointing to a structural problem with the task spec rather than just agent failure.

The instructions define "clean" as:
- `ok=true`, `illegal=0` on both fresh and resume paths
- Signatures match
- JSON/records/log sidecars list the same resolved moves in order

The sentinel case satisfies **all of these criteria** even with the ward bug present — the audit's `ok` field does not surface the `active`-state divergence. The test `test_modifier_active_05` checks a behavioral invariant that is entirely absent from the spec's cleanliness definition. An agent faithfully implementing the stated criteria will conclude the task is done and be wrong.

This caused three agents (tbench-task__8CW9zAs, tbench-task__TZy8jSk, tbench-task__foWX5nR) to declare success after seeing `ok=True` across all 7 cases — a reasonable conclusion given the spec.

---

### 5. Progress on Failed Trials

| Trial | Code Changes | Tests Passed | Distance from Goal |
|---|---|---|---|
| tbench-task__8CW9zAs | None | 15/16 | Far — never investigated source |
| tbench-task__TZy8jSk | None | 15/16 | Far — never investigated source |
| tbench-task__foWX5nR | None | 15/16 | Far — never investigated source |
| tbench-task__NBRGFaP | Fixed `store/pack.go`, `exec/run.go` | 15/16 | **Close** — 1 file away (`mod/effect.go`) |

The first three agents all took the same path: run the script → check JSON → conclude done. **NBRGFaP (gpt-5.2)** stands out as genuinely engaging with the codebase: it diagnosed visibility mismatches and duplicate-move bugs, applied real fixes, and narrowed the failure to a single off-by-one in one function. It was one targeted edit away from solving the task.

---

### 6. Key Differences Between Agents

The critical differentiator was **whether the agent treated `ok=True` in the audit as conclusive**. Three agents did and immediately terminated. GPT-5.2 did not — it dug into the Go source, found and fixed multiple legitimate bugs, and got within one file of the solution. The remaining gap (missing `mod/effect.go`) may also reflect the spec gap: even a thorough agent would have no spec-based reason to look for an active-state bug.

**Recommendation:** The task spec should be updated to explicitly list ward modifier active-state preservation after restore as a "clean" criterion, and/or the audit script's `ok` field should be extended to flag `active`-field divergences in effect rows. |
<!-- test-summary-end -->