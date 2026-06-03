# TERMINUS — Submission Status

**Project:** Terminus-2nd-Edition (`bfe79c33-8ab0-4061-9849-08d3207c9927`)
**Last fetched:** 2026-06-02 (`stb submissions list --show-folder-names`, then missing NEEDS_REVISION feedback snapshots)
**Source command:** `stb submissions list --project-id bfe79c33-8ab0-4061-9849-08d3207c9927 --show-folder-names`

---

## Snapshot

| Bucket | Count | Tasks |
| --- | ---: | --- |
| Accepted | 7 | artifact-provenance-timewarp, autograd-tape-alias, rollback-combat-desync, late-window-lineage, abi-feature-backtrack, staged-snapshot-drift, timer-replay-coalescence |
| Submitted / awaiting platform | 3 | allocator-free-list-drift, module-state-propagation-epoch, _(unnamed offer)_ |
| Working on revision | 7 | sparse-block-preconditioner, quantized-beam-alignment, fog-state-resume, policy-revocation-shadow, adaptive-mesh-conservation, incremental-index-invalidation, async-executor-liveness |
| Needs revision without local feedback archive | 0 | — |
| Superseded | 0 | — |
| **Total submission rows** | **17** | |

All current **NEEDS_REVISION** rows now have a latest feedback archive under `personal_docs/feedback/<task>/revision_N/`.

---

## Local Dev legend

| Value | Meaning |
| --- | --- |
| `accepted` | Platform marked ACCEPTED — no further work expected |
| `submitted` | Sent to platform (REVIEW_PENDING / OFFERED / EVALUATION_PENDING) — waiting on reviewer or AutoEval |
| `working on revision` | Platform returned NEEDS_REVISION and a feedback archive exists under `personal_docs/feedback/<task>/revision_N/` |
| `needs revision` | Platform returned NEEDS_REVISION but no feedback archive exists yet |
| `in progress` | Local task folder exists but nothing submitted yet |
| `superseded` | Older submission for a task that has a newer active row |

---

## 2026-06-02 update

### Platform state changes since the 2026-05-29 status file

| Task | Previous tracked state | Current platform state | Feedback archive |
| --- | --- | --- | --- |
| sparse-block-preconditioner | NEEDS_REVISION | **NEEDS_REVISION** | `feedback/sparse-block-preconditioner/revision_3/` |
| quantized-beam-alignment | EVALUATION_PENDING | **NEEDS_REVISION** | `feedback/quantized-beam-alignment/revision_3/` |
| fog-state-resume | REVIEW_PENDING | **NEEDS_REVISION** | `feedback/fog-state-resume/revision_2/` |
| policy-revocation-shadow | REVIEW_PENDING | **NEEDS_REVISION** | `feedback/policy-revocation-shadow/revision_1/` |
| adaptive-mesh-conservation | NEEDS_REVISION | **NEEDS_REVISION** | `feedback/adaptive-mesh-conservation/revision_1/` |
| incremental-index-invalidation | REVIEW_PENDING | **NEEDS_REVISION** | `feedback/incremental-index-invalidation/revision_1/` |
| async-executor-liveness | REVIEW_PENDING | **NEEDS_REVISION** | `feedback/async-executor-liveness/revision_1/` |
| late-window-lineage | REVIEW_PENDING | **ACCEPTED** | — |
| staged-snapshot-drift | EVALUATION_PENDING | **ACCEPTED** | `feedback/staged-snapshot-drift/revision_1/`, `revision_2/` |
| allocator-free-list-drift | REVIEW_PENDING | REVIEW_PENDING | `feedback/allocator-free-list-drift/revision_1/`, `revision_2/` |
| module-state-propagation-epoch | REVIEW_PENDING | REVIEW_PENDING | `feedback/module-hot-reload-epoch/revision_1/` (old name) |

### Feedback fetched in this pass

Created the missing latest archives according to `personal_docs/feedback.md`:

- `personal_docs/feedback/fog-state-resume/revision_2/`
- `personal_docs/feedback/policy-revocation-shadow/revision_1/`
- `personal_docs/feedback/incremental-index-invalidation/revision_1/`
- `personal_docs/feedback/async-executor-liveness/revision_1/`

Each new archive includes `feedback/notes.txt`, `feedback/agent_review.txt`, `feedback/agent_logs/`, `submitted-task/`, `metadata/submission_<short_id>.json`, `README.md`, `revision-priorities.md`, and a metadata summary JSON. `fog-state-resume/revision_2/` also includes a copied `rubric.txt` from `personal_docs/rubrics/`.

---

## Full submission log (newest first)

| # | Submission ID | Created | Task Folder | Platform State | Local Dev | Notes |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | `286b5bea-fc9b-4ecf-906f-10bb68c68582` | 2026-05-25 15:56 | _(unnamed)_ | OFFERED | submitted | No folder name on platform — offer awaiting pickup/review flow |
| 2 | `64f78238-acf5-4cce-ba2a-100ea9b5a20f` | 2026-05-25 15:49 | sparse-block-preconditioner | NEEDS_REVISION | working on revision | Latest archive `revision_3/`; blocker is difficulty collapse/TRIVIAL despite quality passing |
| 3 | `4e774a51-688e-46e0-b7bc-c56194572f8c` | 2026-05-25 14:09 | quantized-beam-alignment | NEEDS_REVISION | working on revision | Latest archive `revision_3/`; HARD but no frontier agent solved all tests |
| 4 | `ec8bf6df-d0d2-40bf-ba64-67ea0f67e002` | 2026-05-25 13:05 | fog-state-resume | NEEDS_REVISION | working on revision | Latest archive `revision_2/`; missing ward active-state contract and caching cleanup request |
| 5 | `146c63b3-85f3-4018-b032-b7d5da93e1af` | 2026-05-25 13:03 | artifact-provenance-timewarp | ACCEPTED | accepted | Accepted; local task/zip artifacts are no longer present in this checkout |
| 6 | `8e46cde4-634a-4ebf-882a-f45479d48af2` | 2026-05-25 13:02 | autograd-tape-alias | ACCEPTED | accepted | Accepted; local task/zip artifacts are no longer present in this checkout |
| 7 | `74fd6fa2-2ca6-46dd-97f1-c88fe2367919` | 2026-05-25 13:00 | allocator-free-list-drift | REVIEW_PENDING | submitted | Rev-2 pushed; archives `revision_1/`, `revision_2/` |
| 8 | `52218157-dee7-483f-a7f5-5653ee5e1d01` | 2026-05-23 21:25 | policy-revocation-shadow | NEEDS_REVISION | working on revision | Latest archive `revision_1/`; strengthen metadata-field and dynamic-trace verifier coverage |
| 9 | `ea9c5aae-7199-46c6-bf5b-236691b01936` | 2026-05-23 18:58 | module-state-propagation-epoch | REVIEW_PENDING | submitted | Renamed from module-hot-reload-epoch; archive remains under old name `feedback/module-hot-reload-epoch/revision_1/` |
| 10 | `5586b05b-0661-46a5-a2a6-1d98344b0ada` | 2026-05-22 13:15 | adaptive-mesh-conservation | NEEDS_REVISION | working on revision | Archive `revision_1/`; instruction/spec gap plus pytest placement feedback |
| 11 | `f0ec5d42-9e1a-4709-9852-acfa502041c5` | 2026-05-19 06:38 | incremental-index-invalidation | NEEDS_REVISION | working on revision | Archive `revision_1/`; blocking `tests/test.sh` exit-code propagation issue |
| 12 | `7243aade-daa1-4513-96d0-7366734d930d` | 2026-05-18 23:44 | async-executor-liveness | NEEDS_REVISION | working on revision | Archive `revision_1/`; add explicit root `parent` = `"-"` sentence |
| 13 | `88956422-7ff6-4c4c-8b62-79ce74e97ff6` | 2026-05-16 21:00 | rollback-combat-desync | ACCEPTED | accepted | Accepted; local task/zip artifacts are no longer present in this checkout |
| 14 | `79073757-78ac-40e1-93a9-14b27143fd8a` | 2026-05-16 15:29 | late-window-lineage | ACCEPTED | accepted | Accepted; local task folder and zip are present |
| 15 | `f198d486-9aa4-4ed0-88f1-3d20c469f528` | 2026-05-16 05:59 | abi-feature-backtrack | ACCEPTED | accepted | Accepted; local task/zip artifacts are no longer present in this checkout |
| 16 | `d6d229bf-537c-414f-a71f-74582b7ee47c` | 2026-05-15 19:40 | staged-snapshot-drift | ACCEPTED | accepted | Accepted after prior revision cycle; local task folder, zip, and feedback archives are present |
| 17 | `2d70f1dd-80c4-467b-bc9c-147878b240d5` | 2026-05-15 11:58 | timer-replay-coalescence | ACCEPTED | accepted | Accepted; local task/zip artifacts are no longer present in this checkout |

---

## Per-task latest state (16 named folders)

| Task Folder | Latest Submission | Platform State | Local Dev | Feedback archive(s) | Local task dir? | Zip? |
| --- | --- | --- | --- | --- | --- | --- |
| abi-feature-backtrack | `f198d486-9aa4-4ed0-88f1-3d20c469f528` | ACCEPTED | accepted | — | — | — |
| adaptive-mesh-conservation | `5586b05b-0661-46a5-a2a6-1d98344b0ada` | NEEDS_REVISION | working on revision | `revision_1` | ✓ | ✓ |
| allocator-free-list-drift | `74fd6fa2-2ca6-46dd-97f1-c88fe2367919` | REVIEW_PENDING | submitted | `revision_1`, `revision_2` | ✓ | ✓ |
| artifact-provenance-timewarp | `146c63b3-85f3-4018-b032-b7d5da93e1af` | ACCEPTED | accepted | — (deleted 2026-05-29) | — | — |
| async-executor-liveness | `7243aade-daa1-4513-96d0-7366734d930d` | NEEDS_REVISION | working on revision | `revision_1` | ✓ | ✓ |
| autograd-tape-alias | `8e46cde4-634a-4ebf-882a-f45479d48af2` | ACCEPTED | accepted | — | — | — |
| fog-state-resume | `ec8bf6df-d0d2-40bf-ba64-67ea0f67e002` | NEEDS_REVISION | working on revision | `revision_1`, `revision_2` | ✓ | ✓ |
| incremental-index-invalidation | `f0ec5d42-9e1a-4709-9852-acfa502041c5` | NEEDS_REVISION | working on revision | `revision_1` | ✓ | ✓ |
| late-window-lineage | `79073757-78ac-40e1-93a9-14b27143fd8a` | ACCEPTED | accepted | — | ✓ | ✓ |
| module-state-propagation-epoch | `ea9c5aae-7199-46c6-bf5b-236691b01936` | REVIEW_PENDING | submitted | `revision_1` under `module-hot-reload-epoch/` | ✓ | ✓ |
| policy-revocation-shadow | `52218157-dee7-483f-a7f5-5653ee5e1d01` | NEEDS_REVISION | working on revision | `revision_1` | ✓ | ✓ |
| quantized-beam-alignment | `4e774a51-688e-46e0-b7bc-c56194572f8c` | NEEDS_REVISION | working on revision | `revision_1`, `revision_2`, `revision_3` | ✓ | ✓ |
| rollback-combat-desync | `88956422-7ff6-4c4c-8b62-79ce74e97ff6` | ACCEPTED | accepted | — | — | — |
| sparse-block-preconditioner | `64f78238-acf5-4cce-ba2a-100ea9b5a20f` | NEEDS_REVISION | working on revision | `revision_1`, `revision_2`, `revision_3` | ✓ | ✓ |
| staged-snapshot-drift | `d6d229bf-537c-414f-a71f-74582b7ee47c` | ACCEPTED | accepted | `revision_1`, `revision_2` | ✓ | ✓ |
| timer-replay-coalescence | `2d70f1dd-80c4-467b-bc9c-147878b240d5` | ACCEPTED | accepted | — | — | — |

---

## Current revision queue

| Task | Latest archive | Primary blocker / next action |
| --- | --- | --- |
| sparse-block-preconditioner | `feedback/sparse-block-preconditioner/revision_3/` | Platform says TRIVIAL: both frontier agents solve 5/5. Needs redesign/hardness increase, not a small wording fix. |
| quantized-beam-alignment | `feedback/quantized-beam-alignment/revision_3/` | HARD but possibly too hard: no non-oracle agent solved all tests; core Rust computation bugs remain 0/10 across five tests. |
| fog-state-resume | `feedback/fog-state-resume/revision_2/` | Add missing ward active-state preservation contract and handle caching-file cleanup request. |
| policy-revocation-shadow | `feedback/policy-revocation-shadow/revision_1/` | Add verifier coverage for `principal`/`resource`/`action` metadata and a dynamic trace/source guard against canned audit output. |
| adaptive-mesh-conservation | `feedback/adaptive-mesh-conservation/revision_1/` | Fix instruction gap for signature/fingerprint rejection and adjacency hints; triage pytest placement warning under offline policy. |
| incremental-index-invalidation | `feedback/incremental-index-invalidation/revision_1/` | Fix `tests/test.sh` so pytest exit status controls both `reward.txt` and process exit. |
| async-executor-liveness | `feedback/async-executor-liveness/revision_1/` | Add one explicit sentence: root records emit `parent` as string `"-"` in JSON, ledger JSONL, and journal output. |

---

## Refresh commands

```bash
cd "/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS"

# Refresh this status (re-pull platform state)
stb submissions list --project-id bfe79c33-8ab0-4061-9849-08d3207c9927 --show-folder-names

# Pull feedback for a NEEDS_REVISION task (see personal_docs/feedback.md for full workflow)
stb submissions feedback <SUBMISSION_ID>
stb submissions download <SUBMISSION_ID> -o "personal_docs/feedback/<task>/revision_<N>/submitted-task"
stb submissions fetch-task <SUBMISSION_ID> -o "personal_docs/feedback/<task>/revision_<N>/metadata"

# Update an existing submission after revision (do NOT use create — would duplicate IDs)
stb submissions update tasks/<task-folder> -t <minutes>
```

---

## Maintenance notes

- Reconcile this file whenever platform state changes after a submission, revision push, or reviewer action.
- When a NEEDS_REVISION row appears without an archive, mark Local Dev = `needs revision`, run the feedback workflow in [`feedback.md`](feedback.md), then flip it to `working on revision`.
- When `stb submissions update` is run, set Local Dev = `submitted` and Platform State = `EVALUATION_PENDING` until AutoEval/reviewer returns.
- `module-hot-reload-epoch` is now `module-state-propagation-epoch` on the platform; its feedback archive still lives under the old folder name.
- Per-revision feedback workflow: [`feedback.md`](feedback.md). Archives: [`feedback/`](feedback/).
