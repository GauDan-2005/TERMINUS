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
| test_b1 | 10 / 10 |
| test_d3 | 10 / 10 |
| test_e4 | 4 / 10 |
| test_f5 | 8 / 10 |
| test_h7 | 4 / 10 |
| test_i8 | 10 / 10 |
| test_j9 | 10 / 10 |
| test_l1 | 10 / 10 |
| test_a0 | 0 / 10 |
| test_c2 | 0 / 10 |
| test_g6 | 0 / 10 |
| test_k0 | 0 / 10 |
</details>

### Analysis on Agent Failures
| Check       | Outcome  | Explanation              |
|-------------|----------|--------------------------|
| Task Instruction Sufficiency | ❌ FAIL | ## Job Summary: C Heap Allocator Harness Repair

### 1. Overall Results
**0/10 trials passed** (all reward = 0.0). No agent achieved the binary pass threshold despite varying levels of effort and code investigation.

---

### 2. Common Failure Patterns

**Pattern A — Insufficient Investigation (3 trials: eKkYeh7, 9eBT7gZ, riwDKdt)**
These agents never opened C source files at all. They ran the existing harness, validated structural properties (JSON field names, case ordering, determinism), and declared success. They passed 6/12 tests (format/structure checks) but failed all value-correctness tests.

**Pattern B — `byte_total` Misinterpretation (7 trials: UrJ2btN, C46aG3j, NFyNJ3R, iw4gJg2, fxKPJ4J, rvNb4GD, zfpGxQ4)**
These agents correctly identified and often fixed the other bugs (footer offset, spurious `+8`, half-copy, missing backward coalescing), but all failed on `byte_total`. They interpreted "live allocated payload bytes" as the user-requested size (e.g., 64 for `alloc(64)`), while the reference `ModelArena` tracks full block sizes including HDR (16) + FTR (8) overhead (e.g., 88 for the same alloc). This caused 4 failing tests per trial.

**Pattern C — Additional Regressions (2 trials)**
- **zfpGxQ4**: Introduced over-aggressive coalescing during split by calling `list_coalesce` instead of `xb1`, breaking the coral case.
- **NFyNJ3R**: Rewrote `slot_split.c` introducing new forward/backward coalesce errors, failing additional cases.
- **rvNb4GD**: Fixed realloc to preserve the original slot index (reasonable reading of the spec), but the test model expects a new slot index on move, causing `pearl heap_sig` failure.

---

### 3. Hack Check
**No cheating detected across all 10 trials.** Every agent's reward_hacking check passed. No agent accessed the `solution/` directory, modified test files, or wrote to reward/grading files. All 0.0 rewards are legitimate.

---

### 4. Systematic Instruction Issues

**Critical spec ambiguity — `byte_total`:** 7 of 10 task_specification checks were marked **fail**, all citing the same issue: the instruction states *"byte_total tracks live allocated payload bytes"*, but `ModelArena` computes it as `align(req + HDR + FTR)` — total block size including overhead. In standard allocator terminology, "payload bytes" means user-requested bytes *excluding* overhead. The correct instruction wording should have been something like "total allocated block bytes including header and footer overhead."

**Secondary spec ambiguity — `realloc` slot indexing (rvNb4GD):** The instruction implies freeing by original slot index should work, but the test model creates a new slot on realloc-move and lets the original die — opposite behavior. The instruction doesn't specify this clearly enough.

The 3 trials marked task_specification: **pass** (eKkYeh7, 9eBT7gZ, riwDKdt) were lazy agents whose failure was entirely due to not reading source code — the spec was adequate for their bugs but they never engaged with it.

---

### 5. Progress (How Close Did Agents Get?)

| Trial | Tests Passed | Primary Remaining Gap |
|---|---|---|
| UrJ2btN, C46aG3j, fxKPJ4J | **8/12** | Only `byte_total` interpretation wrong |
| zfpGxQ4 | **7/12** | `byte_total` + one regression in split |
| rvNb4GD | **6/12** | `byte_total` + realloc semantics |
| eKkYeh7, 9eBT7gZ, riwDKdt, iw4gJg2 | **6/12** | Never fixed value bugs |
| NFyNJ3R | **5/12** | `byte_total` + introduced new regressions |

The best agents (UrJ2btN, C46aG3j, fxKPJ4J) were effectively one spec clarification away from passing — they correctly fixed 4/5 bugs and only failed on the ambiguous `byte_total` wording.

---

### 6. Key Takeaways

- The **`byte_total` spec ambiguity is the decisive blocker**: a single word change ("payload bytes" → "full block bytes including overhead") would likely have flipped 7 trials from 0 to potential passes.
- **Depth of investigation** separated agents: Pattern A agents scored 6/12 with no effort; Pattern B agents scored 6–8/12 with substantial debugging. No agent reached 9/12.
- **Binary grading is harsh**: The best agents passed 67% of individual tests yet earned 0 reward, obscuring meaningful progress signal.
- **No model diversity noted** in the provided summaries — all trials appear to run the same agent type under the same task variant. |
<!-- test-summary-end -->