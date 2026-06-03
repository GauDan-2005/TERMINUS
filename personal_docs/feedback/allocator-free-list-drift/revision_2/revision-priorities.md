# Revision Priorities — allocator-free-list-drift (revision_2)

Submission `74fd6fa2-2ca6-46dd-97f1-c88fe2367919` is `NEEDS_REVISION`. The
platform note says *"AutoEval … Build status: FAILED (995b70b0)"*, but the build
that "failed" is the **difficulty-check** job and it failed **only because
`solvable=False`** — no candidate agent passed. There is **no compile/build
error** (oracle 3/3, image builds, `.o` issue from revision_1 is gone, other
builds + `fast_static_checks` SUCCEEDED). So the entire blocker reduces to one
thing: **agents can't pass because `instruction.md` defines `byte_total` in a way
that contradicts the test reference model.** Fix that and the build flips back to
SUCCEEDED.

Everything below is derived from `feedback/notes.txt`,
`feedback/agent_logs/`, `metadata/submission_74fd6fa2.json`, the archived
`submitted-task/` files, and a rev1→rev2 `instruction.md` diff.

---

## P0 — Solvability blocker (fixes the "failed build")

**1. Correct the `byte_total` definition in `instruction.md` (decisive).**

- Current — `submitted-task/instruction.md` **line 5**:
  > "…fl_count counts free blocks; **byte_total tracks live allocated payload bytes**."
- Reality — `tests/test_outputs.py:274` `rec["byte_total"] = self.allocated`,
  where `self.allocated` only ever changes via `_note(delta)` and every `_note`
  passes a **full aligned block size** (`align(req + HDR + FTR)`, with HDR=16,
  FTR=8, ALIGN=8), never the user payload. So `byte_total` = sum of full block
  sizes of live blocks **including 16-byte header + 8-byte footer, aligned** —
  *not* requested payload bytes.
- Effect: 7/10 trials fixed every other bug and failed **only** byte_total; the 4
  tests that are 0/10 (test_a0, test_c2, test_g6, test_k0) all assert byte_total.
- **Edit 1 (decisive):** replace the byte_total clause on line 5 with, e.g.:
  > "…byte_total tracks the sum of full block sizes of live allocated blocks;
  > each block's size includes its 16-byte header and 8-byte footer and is rounded
  > up to an 8-byte boundary, i.e. `align(requested_payload + 16 + 8)`. It is the
  > total allocated bytes **including overhead**, NOT the sum of user-requested
  > payload bytes."
- **Edit 2 (supporting):** add the block-size model near the formulas so agents
  don't have to reverse-engineer the C:
  > "Block size for a request of S payload bytes is `align(S + HDR + FTR)` with
  > HDR=16, FTR=8, ALIGN=8; `align(n) = (n + 7) & ~7`. heap_sig, fl_sig, fl_count
  > and byte_total all operate on full block sizes, never raw payload sizes."
- **Edit 3 (whole-block consumption):** state that when an allocation/grow consumes
  a free block whose leftover would be below the 40-byte minimum block, the whole
  block is taken (no split) and its full size counts toward byte_total — matches
  `test_outputs.py:186-190` (`total >= need + MIN_BLK`) and the `_note(total)` path.
- **Edit 5 (consistency sweep):** ensure no residual "payload bytes" wording
  anywhere implies byte_total = requested size (line 5 is the only occurrence).

> **Why not just change the test?** The corrected C / oracle already produce
> full-block byte_total (oracle 3/3), and the rubric line 6 framing is about
> *acct_e* not adding spurious padding to the live tally — the model is the
> intended ground truth. The cheapest, lowest-risk fix is the instruction wording,
> not the model. Keep all the revision_1→2 schema additions (`report.h` StepRec,
> field list, case order, run-one envelope) — those fixed the quality check and
> must stay.

**Verification after the edit:** re-run the cheap Step 2b gates in order —
`./scripts/check-task.sh tasks/allocator-free-list-drift` → oracle 1× → NOP — then
re-trigger the difficulty/AutoEval harness. Target: candidate agents can now pass
(`solvable=True`), difficulty stays HARD, build `995…`-equivalent returns
SUCCEEDED.

---

## P1 — Secondary spec ambiguity (helps test_g6 / test_h7 heap_sig)

**2. Specify realloc-move slot-index semantics in `instruction.md`.**

- Reality — `tests/test_outputs.py:247-270`: a relocating realloc (grow not
  satisfiable in place or by merging the following free block) **allocates a new
  slot** (`nidx = len(self.slots)`, appends), frees+coalesces the original block,
  marks the original slot dead (`self.live[idx] = False`), and reports the **new**
  index as `result_index` (line 270). In-place shrink / forward-merge grow keep
  the same index (lines 228, 245).
- Instruction currently says nothing about slot lifecycle on realloc; an agent
  reasonably assumes the original index is preserved and stays freeable → fails
  pearl `heap_sig` (trial `rvNb4GD`).
- **Edit 4:** add a sentence:
  > "A realloc that must relocate the block allocates a NEW slot in allocation
  > order, frees and coalesces the original block, marks the original slot dead,
  > and reports the new slot index as result_index; a later free of the original
  > index must fail (result_index -1). In-place shrink and forward-merge grow keep
  > the same slot index."

---

## P2 — Harness agent-review (WARNING) — surface, don't silently apply

The harness review is a **WARNING only and is independent of the NEEDS_REVISION**
(which is driven by the failed difficulty build, P0). Both warnings conflict with
the repo's documented **offline** policy, so they need author judgment, not a
mechanical fix.

1. **pytest/pytest-json-ctrf in Dockerfile (lines 20-22)** — reviewer wants them
   in `tests/test.sh`. The task sets `[environment].allow_internet = false`, so a
   runtime `pip install` in test.sh would fail offline; `REPO_CONVENTIONS.md`
   (lines 127-145, 203-209) requires verifier deps pinned in the image build,
   which is what lines 20-22 do. **Conflict.** Recommended: keep the image install
   and add a short rebuttal note when resubmitting (the reviewer's suggested
   `curl … uv … uv pip install` rewrite cannot be made functional offline).
2. **test.sh "not standard uv format" (lines 1-19)** — same offline conflict; the
   submitted `python -m pytest … ; if [ $? -eq 0 ]` template is this repo's
   canonical offline verifier shape. Recommended: keep as-is, rebut.
3. **Instruction symptom sentence (suggestion, line 1)** — optional; reviewer
   rates it "acceptable as-is" for a hard task. If applied, add one symptom line in
   the existing terse voice (e.g. "compiles cleanly but emits incorrect audit
   signatures and can crash on certain plan sequences"); do **not** convert to a
   Task/Output template layout.

> Note: per the repo's feedback-over-docs guidance, reviewer feedback normally
> takes precedence over CI/docs — *but only when the result stays functional*.
> Here the reviewer's fix is infeasible under `allow_internet=false`, so the
> functional resolution is to keep the image install and rebut, while explicitly
> surfacing the conflict rather than ignoring it.

---

## P3 — Already passing (no change needed)

- **Quality check 10/10** — all axes pass, including the two (`behavior_in_task_description`,
  `structured_data_schema`) that failed in revision_1.
- **Test-quality judge** — ROBUST / ACCEPT; reference-model suite, no hardcoding.
- **Packaging** — 0 `.o` files; `.dockerignore` excludes `**/*.o`; `make clean &&
  make` from source; digest-pinned base; pinned apt/pip. The revision_1 build
  blocker is fully resolved.
- **Solvability proof** — oracle 3/3; bugs are real and embedded in C source.
- **Difficulty** — HARD, not in dispute.

---

## Tests agents never pass — test_a0, test_c2, test_g6, test_k0 (all 0/10)

All four assert `byte_total`. They are **not** mis-scaled or unsolvable — the
oracle passes them. They will flip once P0 (byte_total wording) lands, because
agents will then compute the same full-block total the model expects. test_g6 and
test_h7 (4/10) additionally depend on P1 (realloc-move slot semantics).

## Suggested change order

1. Apply P0 Edits 1-3 + 5 to `instruction.md` (byte_total + block-size model +
   whole-block consumption + consistency sweep).
2. Apply P1 Edit 4 (realloc-move slot semantics).
3. Re-run cheap Step 2b gates (`check-task.sh` → oracle 1× → NOP); confirm oracle
   still 100% and instruction now describes what the tests check.
4. Re-trigger difficulty/AutoEval; confirm `solvable=True` and build SUCCEEDED.
5. Decide P2 rebuttal stance; keep Dockerfile/test.sh as-is unless policy changes.
6. `stb submissions update 74fd6fa2-2ca6-46dd-97f1-c88fe2367919`; capture
   `revision_3/` via the feedback workflow.
