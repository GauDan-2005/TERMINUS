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
| test_a0_storm_seam_balance | 10 / 10 |
| test_b1_canyon_seam_balance | 10 / 10 |
| test_e4_spire_collapse_conserves | 10 / 10 |
| test_f5_plume_round_trip_conserves | 10 / 10 |
| test_g6_basin_resumed_moment | 7 / 10 |
| test_h7_dune_resumed_moment | 7 / 10 |
| test_i8_tampered_snapshot_rejected | 6 / 10 |
| test_no_canary_in_sources | 10 / 10 |
| test_c2_plume_adjacency | 3 / 10 |
| test_d3_spire_adjacency | 3 / 10 |
| test_j9_basin_resumed_adjacency | 2 / 10 |
| test_k0_canyon_halo_band | 0 / 10 |
| test_l1_dune_halo_band | 0 / 10 |
</details>

### Analysis on Agent Failures
| Check       | Outcome  | Explanation              |
|-------------|----------|--------------------------|
| Task Instruction Sufficiency | ❌ FAIL | ## Job Summary

### 1. Overall Results
**0/10 trials passed** (reward = 0.0 for all). The grading is all-or-nothing requiring 13/13 tests to pass. Test scores across trials:

| Trial | Tests Passed | Model |
|---|---|---|
| tbench-task__LtsGCdN | 11/13 | unspecified |
| tbench-task__BCHtgzv | 11/13 | unspecified |
| tbench-task__6yDxiy9 | 8/13 | unspecified |
| tbench-task__23eqdDA | 8/13 | unspecified |
| tbench-task__cQB5Xxu | 8/13 | GPT-5.2 |
| tbench-task__yhCBVvd | 8/13 | unspecified |
| tbench-task__FsaNAAx | 7/13 | unspecified |
| tbench-task__rx4RNUG | 7/13 | GPT-5.2 |
| tbench-task__PpyQgbY | 5/13 | unspecified |
| tbench-task__daVHZDC | 5/13 | unspecified |

---

### 2. Common Failure Patterns

Nearly every agent found the same 3 "obvious" conservation bugs and stopped there:

**Bugs reliably fixed (8–10/10 agents):**
- `fold_q` in `agg_q/blend.cpp`: arithmetic mean → volume-weighted average during cell merges
- `op_m` in `acc_m/edge_corr.cpp`: storing only one flux entry per group → one per subface
- Vault I/O (`srl_p/serial.cpp`, `rsm_k/resume.cpp`): not saving/restoring the FluxBank

**Bugs reliably missed:**
- **Adjacency tracking** (`lnk_n/relate.cpp`): `step_n` never populates `child0`/`child_count`, so `adjacency` is always 0. Missed by 7–8 agents; caused 3 test failures each time. The symptom (always-zero adjacency) is diagnostic in the output, but agents satisfied with `drift_ratio ≈ 0` stopped before investigating it.
- **Halo offset bug** (`sync_b/halo.cpp` or `drv_u/run_blend.cpp`): `op_b` called with `d=1` offset instead of `d=0`, returning wrong ghost-band values. Missed by 7–8 agents; caused 2 test failures each time.
- **Fingerprint/tamper detection** (`srl_p/serial.cpp`, `rsm_k/resume.cpp`): `SIGNATURE_MISMATCH` rejection required for the tampered-snapshot test. Missed by ~5 agents (others happened to implement it while overhauling serialization).

**The core pattern:** Agents anchored on conservation-drift symptoms, verified `drift_ratio ≈ 0` and `base_match: true`, declared success, and never cross-checked `adjacency` or `halo_q` against the reference.

---

### 3. Hack Check
**No cheating detected.** All 10 trials received `reward_hacking: pass`. Agents consistently read source files, edited production C++ code, rebuilt via CMake, and ran the test harness legitimately. No agent accessed the solution directory, modified test files, or wrote to reward artifacts.

---

### 4. Systematic Instruction Issues

**4 trials flagged `task_specification: fail`** (tbench-task__23eqdDA, tbench-task__PpyQgbY, tbench-task__daVHZDC, tbench-task__rx4RNUG), pointing to two gaps:

1. **Fingerprint/SIGNATURE_MISMATCH test (test_i8)**: The instructions describe a conservation/drift problem but never mention tamper detection, fingerprinting, or the `SIGNATURE_MISMATCH` string that test_i8 requires. Multiple reviewers flagged this as a genuine spec gap.

2. **Adjacency requirement not hinted by symptoms**: The failing adjacency tests require fixing `lnk_n/relate.cpp`, but a conservation-drift symptom description gives no signal that relation-building is broken. Agents that read the file often failed to connect it to `adjacency = 0` output.

**6 trials passed `task_specification`**, arguing that the instruction's requirement for "agreement with an independent recomputation of every scenario" and `layout.md` documenting all fields was sufficient — a borderline judgment call. The halo and adjacency bugs are discoverable by reading the code; the fingerprint test is the stronger spec gap.

---

### 5. Progress (How Close Did Agents Get?)

Average: **~8.1/13 tests passed** across all trials.

- **Best performers (11/13):** LtsGCdN and BCHtgzv were one fix away from success.
  - LtsGCdN *regressed* by making an unnecessary and incorrect change to the leaf distribution formula in `run_refine.cpp` (introduced a non-conservative normalization where none was needed), directly causing the 2 halo_q failures.
  - BCHtgzv missed only the `op_b` offset bug in `sync_b/halo.cpp`.
- **Mid-tier (7–8/13):** Most agents fixed serialization and the core conservation bugs but missed both adjacency and halo.
- **Weakest (5/13):** PpyQgbY and daVHZDC skipped serialization fixes and/or introduced regressions (PpyQgbY added unnecessary renormalization; daVHZDC explicitly dismissed the adjacency bug as "outside the conservation requirement").

---

### 6. GPT-5.2 vs. Other Agents

The two GPT-5.2 trials (cQB5Xxu and rx4RNUG) landed in the middle of the pack:
- **cQB5Xxu (8/13)**: Correctly implemented fingerprint validation (rare among all agents), fixed 4 of the 5 core bugs, but missed adjacency tracking and halo_q. Notably *noticed* `adjacency: 0` in output but didn't investigate why.
- **rx4RNUG (7/13)**: Fixed adjacency tracking in `lnk_n/relate.cpp` (one of very few to do so), but failed to fix serialization completely or halo indexing.

No meaningful quality gap between GPT-5.2 and the unspecified agents — both groups clustered around 7–8/13, with individual variation depending on which bugs each agent happened to focus on. |
<!-- test-summary-end -->