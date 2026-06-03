## Summary of Runs for "tbench-task"
### Difficulty: trivial
| Agent/Model | # of total runs | # of successes | # of failures<br>(agent timeout) | # of failures<br>(other reasons) | Accuracy |
|-------------|-----------------|-----------------|------------------------------------|---------------|----------|
| nop | 1 | 0 | 0 | 1 | 0.0 |
| oracle | 3 | 3 | 0 | 0 | 1.0 |
| terminus-claude-opus-4-6 | 5 | 5 | 0 | 0 | 1.0 |
| terminus-gpt5-2 | 5 | 5 | 0 | 0 | 1.0 |
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
| test_h7_opal_mixed_reordered_residuals | 10 / 10 |
| test_i8_reported_matches_true_residual | 10 / 10 |
| test_j9_two_matrix_runs_equivalent | 10 / 10 |
| test_k0_convergent_cases_below_cap | 10 / 10 |
| test_l1_run_one_shale_matches_matrix | 10 / 10 |
| test_z9_row_status_flags | 10 / 10 |
</details>

### Analysis on Agent Failures
| Check       | Outcome  | Explanation              |
|-------------|----------|--------------------------|
| Task Instruction Sufficiency | ➖ NOT_APPLICABLE | debug output not available |
<!-- test-summary-end -->