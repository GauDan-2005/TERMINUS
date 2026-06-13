# TERMINUS — Submission Status

**Project:** Terminus-2nd-Edition (`bfe79c33-8ab0-4061-9849-08d3207c9927`)
**Last fetched:** 2026-06-03 (`stb submissions list`)
**Source command:** `stb submissions list --project-id bfe79c33-8ab0-4061-9849-08d3207c9927 --show-folder-names`

Buckets: **8 accepted · 1 review-pending · 1 offered · 7 needs-revision** (17 rows total).
All 7 NEEDS_REVISION rows have a latest feedback archive under `personal_docs/feedback/<task>/revision_N/` matching the current submission ID — nothing outstanding to fetch.

---

## Current status (newest first)

| # | Submission ID | Created | Task | Platform State | Feedback archive |
| ---: | --- | --- | --- | --- | --- |
| 1 | `286b5bea-fc9b-4ecf-906f-10bb68c68582` | 05/25 15:56 | _(unnamed offer)_ | OFFERED | — |
| 2 | `64f78238-acf5-4cce-ba2a-100ea9b5a20f` | 05/25 15:49 | sparse-block-preconditioner | NEEDS_REVISION | `revision_3` |
| 3 | `4e774a51-688e-46e0-b7bc-c56194572f8c` | 05/25 14:09 | quantized-beam-alignment | NEEDS_REVISION | `revision_3` |
| 4 | `ec8bf6df-d0d2-40bf-ba64-67ea0f67e002` | 05/25 13:05 | fog-state-resume | NEEDS_REVISION | `revision_2` |
| 5 | `146c63b3-85f3-4018-b032-b7d5da93e1af` | 05/25 13:03 | artifact-provenance-timewarp | ACCEPTED | — |
| 6 | `8e46cde4-634a-4ebf-882a-f45479d48af2` | 05/25 13:02 | autograd-tape-alias | ACCEPTED | — |
| 7 | `74fd6fa2-2ca6-46dd-97f1-c88fe2367919` | 05/25 13:00 | allocator-free-list-drift | ACCEPTED | `revision_1`, `revision_2` |
| 8 | `52218157-dee7-483f-a7f5-5653ee5e1d01` | 05/23 21:25 | policy-revocation-shadow | NEEDS_REVISION | `revision_1` |
| 9 | `ea9c5aae-7199-46c6-bf5b-236691b01936` | 05/23 18:58 | module-state-propagation-epoch | REVIEW_PENDING | `revision_1` (under `module-hot-reload-epoch/`) |
| 10 | `5586b05b-0661-46a5-a2a6-1d98344b0ada` | 05/22 13:15 | adaptive-mesh-conservation | NEEDS_REVISION | `revision_1` |
| 11 | `f0ec5d42-9e1a-4709-9852-acfa502041c5` | 05/19 06:38 | incremental-index-invalidation | NEEDS_REVISION | `revision_1` |
| 12 | `7243aade-daa1-4513-96d0-7366734d930d` | 05/18 23:44 | async-executor-liveness | NEEDS_REVISION | `revision_1` |
| 13 | `88956422-7ff6-4c4c-8b62-79ce74e97ff6` | 05/16 21:00 | rollback-combat-desync | ACCEPTED | — |
| 14 | `79073757-78ac-40e1-93a9-14b27143fd8a` | 05/16 15:29 | late-window-lineage | ACCEPTED | — |
| 15 | `f198d486-9aa4-4ed0-88f1-3d20c469f528` | 05/16 05:59 | abi-feature-backtrack | ACCEPTED | — |
| 16 | `d6d229bf-537c-414f-a71f-74582b7ee47c` | 05/15 19:40 | staged-snapshot-drift | ACCEPTED | `revision_1`, `revision_2` |
| 17 | `2d70f1dd-80c4-467b-bc9c-147878b240d5` | 05/15 11:58 | timer-replay-coalescence | ACCEPTED | — |

> Change since 2026-06-02: **allocator-free-list-drift** moved REVIEW_PENDING → **ACCEPTED**. All other rows unchanged.

---

## Revisions queue (NEEDS_REVISION)

| Task | Latest archive | Primary blocker / next action |
| --- | --- | --- |
| sparse-block-preconditioner | `feedback/sparse-block-preconditioner/revision_3/` | rev_4 hardening implemented + locally validated (oracle 13/13 reward=1, nop reward=0; collapse 0-FAIL/2-WARN; RC6 symptoms-only; run_static_checks PASS; packaging PASS). Root cause was deeper than wording: old inputs were so well-conditioned that 3 of 4 bugs were inert (task = single +1e-4). Re-authored inputs so all 4 bugs bite (A layout + B perm + D norm observable; C preconditioner is a subtle green-but-wrong on the exact iteration count); orchestrator now measures the true residual against the original system (fixes always-~0 final_residual). PENDING before `stb submissions update`: live frontier difficulty runs (gpt-5.2 / opus-4-6 ×5) to confirm ≥MEDIUM. |
| quantized-beam-alignment | `feedback/quantized-beam-alignment/revision_3/` | HARD but possibly too hard: no non-oracle agent solved all tests; core Rust computation bugs remain 0/10 across five tests. |
| fog-state-resume | `feedback/fog-state-resume/revision_2/` | Add missing ward active-state preservation contract and handle caching-file cleanup request. |
| policy-revocation-shadow | `feedback/policy-revocation-shadow/revision_1/` | rev_1 implemented + locally validated: `test_t13` (principal/resource/action) + runtime dynamic-trace `test_t14` + `rm -f` source guard in run-matrix/run-one; offline wheelhouse test.sh (clears agent_review warning, allow_internet stays false). oracle 10×=10/10, nop 0.0, approve_task exit 0, zip validated. Rubric regenerated → `personal_docs/rubrics/policy-revocation-shadow-rubric.md` (positives 25→28, within 10–40; adds metadata-coverage criterion + dynamic/anti-canned reframe). PENDING: `stb submissions update -s 52218157…`. |
| adaptive-mesh-conservation | `feedback/adaptive-mesh-conservation/revision_1/` | Fix instruction gap for signature/fingerprint rejection and adjacency hints; triage pytest placement warning under offline policy. |
| incremental-index-invalidation | `feedback/incremental-index-invalidation/revision_1/` | Fix `tests/test.sh` so pytest exit status controls both `reward.txt` and process exit. |
| async-executor-liveness | `feedback/async-executor-liveness/revision_1/` | Add one explicit sentence: root records emit `parent` as string `"-"` in JSON, ledger JSONL, and journal output. |

---

## Reference

**Platform-state legend:** `ACCEPTED` = done, no further work · `REVIEW_PENDING` / `OFFERED` = waiting on reviewer/AutoEval · `NEEDS_REVISION` = platform returned feedback, revision in progress (archive exists under `feedback/<task>/revision_N/`).

**Refresh commands:**

```bash
cd "/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS"

# Re-pull platform state for this file
stb submissions list --project-id bfe79c33-8ab0-4061-9849-08d3207c9927 --show-folder-names

# Pull feedback for a NEEDS_REVISION task (full workflow: personal_docs/feedback.md)
stb submissions feedback <SUBMISSION_ID>
stb submissions download <SUBMISSION_ID> -o "personal_docs/feedback/<task>/revision_<N>/submitted-task"
stb submissions fetch-task <SUBMISSION_ID> -o "personal_docs/feedback/<task>/revision_<N>/metadata"

# Revise an existing submission (use update, NOT create — create duplicates IDs)
stb submissions update tasks/<task-folder> -t <minutes>
```

**Notes:**
- Reconcile this file after any submission, revision push, or reviewer action.
- A new NEEDS_REVISION row needs its feedback pulled via [`feedback.md`](feedback.md) before it can move to the revision queue.
- `module-hot-reload-epoch` was renamed to `module-state-propagation-epoch` on the platform; its feedback archive stays under the old folder name.
- Feedback workflow: [`feedback.md`](feedback.md) · Archives: [`feedback/`](feedback/).
