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
| test_t01_flow | 7 / 10 |
| test_t02_flow | 7 / 10 |
| test_t03_flow | 10 / 10 |
| test_t04_flow | 8 / 10 |
| test_t05_flow | 10 / 10 |
| test_t06_flow | 7 / 10 |
| test_t07_flow | 10 / 10 |
| test_t08_flow | 7 / 10 |
| test_t09_flow | 10 / 10 |
| test_t10_flow | 10 / 10 |
| test_t11_flow | 10 / 10 |
| test_t12_flow | 10 / 10 |
</details>

### Analysis on Agent Failures
| Check       | Outcome  | Explanation              |
|-------------|----------|--------------------------|
| Task Instruction Sufficiency | ✅ PASS | ## Job Summary: Rust Policy-Audit Repair Task

### 1. Overall Results
**0/5 trials passed** (reward = 0 for all). No agent achieved the required all-12-tests threshold.

| Trial | Tests Passed | Score |
|-------|-------------|-------|
| tbench-task__jFfrbM2 | 11/12 | 0 |
| tbench-task__caAuuvM | 11/12 | 0 |
| tbench-task__mQtpYiX | 8/12 | 0 |
| tbench-task__UBRzt2u | 8/12 | 0 |
| tbench-task__28y5d44 | 8/12 | 0 |

Two agents got very close (11/12); three got stuck at 8/12.

---

### 2. Common Failure Patterns

**Pattern A — Cache invalidation on grant/revoke (affected all 8/12 agents, likely present in 11/12 agents too):**
The most pervasive bug. The `store`/`wrap_g` cache keyed only on `(object, mode)` without embedding subject state, so after a `revoke` or `grant` event, subsequent checks return stale verdicts. This caused `alpha` post-revoke to wrongly return `allow` (t01, t08) and `beta` post-grant to wrongly return `deny` (t02) in trials __UBRzt2u__ and __28y5d44__.

**Pattern B — `group_slot` keyed by `(object, mode)` instead of `(subject, object, mode)` (t06, affects 3+ trials):**
In `zeta`'s grouped-replay batch, a blocked subject's denial pollutes the slot for a non-blocked subject. Trials __jFfrbM2__, __28y5d44__, and __mQtpYiX__ explicitly note `test_t06_flow` failing for this reason.

**Pattern C — Global epoch clock breaking per-subject reuse detection (t04, affects __caAuuvM__, __UBRzt2u__, __28y5d44__):**
Agents switched from per-subject tick counters to a global monotonic clock to fix epoch monotonicity. This broke the "reused for stable subjects" requirement: an unrelated `revoke bob` advances the global clock, changing alice's apparent epoch and preventing her second check from being marked `reused: true`.

**Pattern D — `cargo` not on PATH (all 5 trials):**
Every agent hit this environmental obstacle. Two agents (__mQtpYiX__) never successfully recompiled—their source fixes were correct but the old binary ran, yielding 8/12. The other agents found the toolchain at `/usr/local/cargo/bin` or `/usr/local/rustup` and recovered.

---

### 3. Hack Check
**All 5 agents: clean.** No agent accessed `solution/`, modified test files, or wrote to `/logs/verifier/reward.txt`. All `reward_hacking` checks passed. Work was confined to legitimate source edits in `k0`–`k8`, `src/`, and shell scripts.

---

### 4. Instruction/Specification Issues
**None detected.** All 5 `task_specification` checks passed. The specification adequately covers delegation-chain denial, `reused` marking for stable subjects, per-subject epochs, `batch_id`/`delegated_from` semantics, and deterministic reruns. Failures were implementation errors, not spec gaps.

---

### 5. Progress (Failed Trials)

| Tier | Trials | Root Cause of Remaining Failures |
|------|--------|----------------------------------|
| 11/12 (very close) | __jFfrbM2__, __caAuuvM__ | Single test: either t06 group_slot isolation or t04 epoch/reuse logic |
| 8/12 | __mQtpYiX__, __UBRzt2u__, __28y5d44__ | Cache invalidation + group_slot key + (in __mQtpYiX__) binary never recompiled |

All agents correctly fixed delegation-chain blocking (`k4/e.rs`) and at least some epoch/reuse logic. The cache invalidation problem was the hardest bug — it requires understanding that the cache must be keyed on or invalidated by subject state changes, not just `(object, mode)`.

---

### 6. Key Takeaways

- The **11/12 agents were one targeted fix away** from full credit, making this a high-value debugging target for future runs.
- The **`cargo`-not-in-PATH environment issue** cost one agent entirely (__mQtpYiX__) and slowed all others; pre-seeding PATH or documenting toolchain location in the task would reduce wasted steps.
- The **cache invalidation + group_slot key bugs** are the hardest and most consequential; a hint toward "check how the cache is keyed relative to subject state changes" could unlock the remaining failures.
- No model identity differences are available, but the 11/12 agents appear to have done more thorough delegation-chain and epoch fixes before getting stuck, suggesting more systematic source-reading in early exploration. |
<!-- test-summary-end -->