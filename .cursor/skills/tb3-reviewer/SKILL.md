---
name: tb3-reviewer
description: Step 3b paper-review macro for TB3 tasks. Pull when a task has passed Step 2b (preflight + oracle 1x + NOP) and needs paper review against review-and-submit.mdc and difficulty-calibration.mdc before final approval. Any edit triggers the dirty-flag and returns the task to Step 2b.
disable-model-invocation: true
---

# tb3-reviewer — Step 3b paper-review macro

Paper review only. No oracle, NOP, or approve runs here.
Construction is `tb3-task-author`; packaging is `tb3-packager`.

## 1. Pre-conditions

Stop if any fails.

- `tasks/<task-name>/` exists with required files. Required shape
  depends on task type:
  - **Single-step task:** `instruction.md`, `task.toml`,
    `output_contract.toml`, `environment/`, `solution/solve.sh`,
    `tests/`.
  - **Milestone task** (`task.toml` `version = "2.0"` with `[[steps]]`
    blocks): `task.toml`, `output_contract.toml`, `environment/`,
    `steps/milestone_N/{instruction.md, tests/{test.sh, test_mN.py},
    solution/{solve.sh, solveN.sh}}` per milestone. There must be
    NO root-level `instruction.md`, `tests/`, `solution/`,
    `milestones.md`, or `milestone_X.md` for milestone tasks. See
    `task-creation.mdc` "Milestone task" — the deprecated
    root-level layout is rejected.
- `tasks/<task-name>/.step2b-checksum` exists (Step 2b passed at
  some point).
- Run `python3 scripts/task_integrity.py verify tasks/<task-name>`. If exit
  is 1 (dirty / missing / mismatch), stop and tell the user to
  re-run `./scripts/check-task.sh tasks/<task-name>` and repeat
  oracle 1x + NOP before review.
- **Task type sanity:** new starts of multi-container or UI
  building tasks are no longer accepted. If the task is one of
  these AND review history shows it was started fresh under the new
  policy, surface that as a Hard FAIL. In-progress instances are
  exempt; check the spec / commit history before flagging.

## 2. Pull deeper rules

- `review-and-submit.mdc` should auto-attach via globs as soon as
  you open `tasks/<task-name>/instruction.md`,
  `tasks/<task-name>/output_contract.toml`, or
  `tasks/<task-name>/tests/test_outputs.py`. If it is not in the
  always-applied bucket, pull it explicitly.
- `difficulty-calibration.mdc` is agent-requested — pull it
  explicitly before reviewing.
- Read the full review surface before judging: `task.toml`,
  `output_contract.toml`, `construction_manifest.json`, every file
  under `environment/`, plus every fix-path file in the manifest's
  `symbol_table`. For single-step tasks, also read root-level
  `instruction.md`, `solution/`, and `tests/`. For milestone tasks,
  read each milestone's content under `steps/milestone_N/`
  (`instruction.md`, `tests/{test.sh, test_mN.py}`, and
  `solution/{solve.sh, solveN.sh}`). Partial reads (6-8 files) miss
  defects a 25-file read catches.

## 3. Review against the deeper rules

Walk Step 3b's three sub-steps in order; record one PASS/WARN/FAIL
verdict per item.

- `review-and-submit.mdc` §1-7 — Instruction, Environment, Oracle
  Solution, Verifiers, Task Metadata, Task Structure, Difficulty
  Calibration. Confirm `task.toml` has `[environment] allow_internet =
  false`, verifier deps are pinned in `environment/Dockerfile` (now accepted
  by the fixed `test_deps_in_image` CI check, not runtime installs in
  `test.sh`), platform pipeline Dockerfile checks pass (blocking:
  digest-pinned `FROM`, sanctioned final runtime base, build-context size;
  warnings: `.dockerignore`, hygiene, layer ordering, multi-stage builds —
  see `task-creation.mdc` § environment/Dockerfile), and `tests/test.sh`
  matches the internet-disabled standard or UI template per `task-creation.mdc`. Apt pins are point-in-time: if image build
  fails with `Version '…' was not found`, refresh Debian apt pins (security
  updates drop old versions—`libssl3`, `ca-certificates`, etc.); do not remove
  pins to pass CI.
- `difficulty-calibration.mdc` Part E — when platform agent accuracies
  are available, classify Hard → Medium → Easy using best/worst model
  thresholds.
- `difficulty-calibration.mdc` Part A — collapse audit (smallest
  plausible patch, frontier, requirement-to-file map, oracle LOC,
  discoverability, red flags, residual hardness). Confirm the latest
  Step 2b mechanical record has `scripts/collapse_check.py` at 0 FAIL / 0 WARN.
  Any remaining WARN needs explicit PASS-with-justification from this
  review; do not let WARNs pass silently as "non-fatal."
- `difficulty-calibration.mdc` Part B — per-test feasibility risks
  (single-valid-approach, chain-dependency, order-sensitivity,
  flakiness, niche-technique). Flag any HIGH-risk test.
- `difficulty-calibration.mdc` Part F — platform auto-eval and agent
  discrimination. **Mandatory when reviewing post-upload failures.**
  - `verifier_did_not_run` → Verifier/infra issue, NOT difficulty. Audit
    `test.sh` for runtime installs, missing `reward.txt`, timeouts. See
    `docs/PLATFORM_AUTO_EVAL.md`.
  - Zero agents pass any test (no verifier_did_not_run) → Likely Part B
    issue (chain-dependent, single-path, niche-knowledge). Recommend
    `scripts/verifier_health.py` before redesign.
  - Difficulty check order: verifier must write `reward.txt` before Part E
    runs; fix verifier issues before worrying about calibration.
- Cross-reference the spec's `Reviewer Appendix` to confirm the
  drafted task still satisfies the discovery budget and topology
  enumeration committed in Step 2a.
- **Oracle reality check.** For every non-trivial `solve.sh` op
  (sed/awk, AST rewrites, heredoc writes, `Path.write_text`,
  `python3 -c`), confirm the target file exists and the change is
  part of the substantive fix. A sed against missing markers is a
  no-op inflating diff count without semantic effect — Hard FAIL.
  A sed rewriting only cosmetic comments to clear A16's floor is
  also Hard FAIL — see `difficulty-calibration.mdc` A16 WARN-band policy.

## 4. Findings

Classify every finding:

- **Hard FAIL** — blocks approval. Edit per `workflow-prompts.md`
  Step 3b preservation discipline (predict at-risk gates, smallest
  preservation-safe fix, label preservation-safe or justified
  regression). Any edit dirty-flags the task. Always Hard FAIL
  regardless of mechanical-gate verdicts:
  - `solve.sh` edits a path in the spec's `decoy_manifest`.
  - `construction_manifest.json` missing when the spec names a
    `symbol_table`, `flipping_point_contract`, or `decoy_manifest`.
  - `flipping_point_contract.locations[*].controls_tests` lists a
    test that does not flip when that location is reverted.
  - Any oracle op producing no on-disk change, or only cosmetic
    comment / marker substitution to satisfy A16 (per §3).
  - `instruction.md` defers operational facts (entrypoint
    command, env vars, I/O paths, output schema) to a `.txt`,
    `.md`, `README`, `hints`, or `notes` file under
    `environment/` the instruction says to "follow," "consult,"
    or "see for details" — Instruction honesty rule 4 in
    `task-creation.mdc`. Move the facts into `instruction.md`;
    above length WARN, accept it over re-splitting.
- **WARN** — surface to the user; do not auto-edit.
- **Collapse WARN** — normally return to Step 2b for honest cleanup
  before Step 4. Accept only with a written PASS-with-justification
  explaining why the warning reflects an acceptable task shape rather
  than padding, discoverability, tiny diffs, or verifier shallowness.
- **PASS** — record.

## 5. After any edits

The first task-file edit dirty-flags the task. Before claiming
Step 3b clean:

- Rerun `./scripts/check-task.sh tasks/<task-name>` (rewrites the
  checksum and metrics).
- Rerun `python3 scripts/harbor_gate.py tasks/<task-name> --oracle` and
  `--nop`. Confirm oracle 1.0, NOP 0.0.
- Rerun this skill from §3 to confirm no concept-level regression.

Do not run oracle 10x here — that is Step 4.

## 6. Hand-off

Report:

- Per-section verdict (§1-7 / Part A / Part B).
- Edit ledger (preservation-safe / justified regression / "no edits").
- If edits: post-edit preflight + oracle / NOP results.

Then say verbatim — pick one:

> Step 3b complete; no edits needed. Ready for Step 4 packaging (pull `tb3-packager` skill).
> Step 3b complete after preservation-safe edits. Step 2b PASS re-confirmed. Ready for Step 4 packaging (pull `tb3-packager` skill).

Stop. Do not run `scripts/approve_task.py`, `scripts/validate_submission_zip.py`, or oracle 10x — Step 4.
