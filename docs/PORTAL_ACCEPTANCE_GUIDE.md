# Portal Acceptance Guide — maximize first-pass acceptance

How to align with the **Terminus EC Training portal** while using this repo's
**stricter local gates** as acceptance insurance. Portal rules define what CI
blocks; repo rules catch what peer review, LLMaJ, and agent eval reject *before*
you upload.

Training portal: [Terminus EC Training](https://snorkel-ai.github.io/Terminus-EC-Training-stateful/)

In-repo mirror: `docs/EDITION2_SUBMISSION_GUIDE.md` · Commands: `commands.md`

---

## Platform vs repo (intentional differences)

| Topic | Portal (Jun 2026) | This repo (acceptance insurance) |
|-------|-------------------|----------------------------------|
| `codebase_size` | `minimal`, `small`, `large` all accepted | Same — metadata must match file count; **prefer `small`/`large`** for portfolio variety |
| Model difficulty | **Medium + Hard** accepted; Easy (>80%) blocked | **Target Hard**; `hard_difficulty_predictor.py` blocks Python with predicted worst-model pass >20% |
| Oracle runs | Platform oracle agent: **3 runs** | Local: `--oracle-stress 3` + `--oracle-repeat 10` for flake detection |
| `test.sh` reward | Inline `$?` or `rc=$?` after pytest (variable form **preferred**) | Both accepted; `rc=$?` documented as preferred in `task-creation.mdc` |
| Multi-container / UI | Documented for in-flight work | **New starts blocked** in this repo |
| Hidden contracts / collapse | Peer review + LLMaJ | **Mechanical gates** before zip (`collapse_check`, `spec_test_alignment`, `no_hidden_contracts`) |
| Rubrics | UI-only; `# Rubric 1` for all tasks; `# Rubric N` per milestone | Same + `TASK_PROPOSAL_RUBRIC.md` |

**Rule of thumb:** pass every repo gate in `commands.md` → you are aligned with portal CI **and** pre-empt most revision feedback.

---

## Portal changelog (synced Jun 2026)

| Date | Change |
|------|--------|
| **Jun 12** | Canonical digest-pinned ECR base images (10 families); non-canonical bases need credible Dockerfile/`README.md` justification |
| **Jun 12** | Difficulty-check models: **GPT-5.5** + **Claude Opus 4.8** (thresholds unchanged) |
| **Jun 3** | `minimal` codebase re-allowed; `rc=$?` preferred in `test.sh`; rubrics require `# Rubric 1` (and `# Rubric N` per milestone); Common Errors maps feedback categories |
| **May 27** | Digest-pinned `FROM`, canonical/sanctioned final runtime bases, build-context limits; no trailing `exit` in `test.sh` |
| **May 15** | Long Context Checklist required for `long_context` subcategory |

---

## Four-step review pipeline

Every submission passes:

1. **CI checks** — structure, Dockerfile, `test.sh`, typos, sizes
2. **LLMaJ (GPT-5.5)** — `behavior_in_task_description`, `behavior_in_tests`, `anti_cheating_measures`, etc.
3. **Peer review** — Reviewer Checklist (HIGH/MEDIUM/LOW severities)
4. **Agent eval** — GPT-5.5 + Opus 4.8, **5 runs each**

Local workflow runs steps 1–2 equivalents plus oracle/NOP/collapse **before** zip.

---

## Diversity (new submissions only)

| Axis | Portal | Repo recommendation |
|------|--------|---------------------|
| Codebase size | `minimal` (0–19), `small` (20–200), `large` (200+) | Match actual count; vary portfolio across sizes |
| Implementation language | Any of **9 accepted families** (10 common tags) | Spread across Python, JS/TS, Go, Rust, Java, C/C++, Ruby, Bash — do not cluster on Python; ask author when language unset (`task-creation.mdc` § Accepted implementation languages) |
| Model difficulty | Medium + Hard | **Aim Hard** (≤20% worst or best model) |
| Easy | Blocked (>80% worst model) | Blocked |
| Python | Must be **Hard** empirical | `hard_difficulty_predictor.py` enforces ≤20% predicted worst-model pass |
| Milestones | Optional; preferred (higher pay) | Preferred |

Tasks already in revision queue are **not** subject to new diversity checks.

---

## Quality guidelines (portal + repo)

From portal `reference/quality-guidelines.md` — all tasks must satisfy:

### High-level requirements

- **Human prompt styling** — `instruction.md` reads like engineer→agent chat; not LLM-polished spec prose
- **Multi-step** — requires chaining **≥5 terminal commands**, intermediate state, error recovery or branching
- **Testable** — every requirement maps to a deterministic pytest assertion
- **Novel** — distinct from TB1/TB2/TB3 and your prior submissions (`reviewer_simulation` `template_risk`)
- **No privileged ops** — no `--privileged`, docker.sock, `SYS_ADMIN`
- **Standalone** — completes without human input after start

### Scenarios to avoid

| # | Rule | Feedback category |
|---|------|-------------------|
| 1 | No latency/throughput/memory tests | `test_alignment` |
| 2 | Identical oracle/agent test conditions (no oracle-only branches) | `test_alignment` |
| 3 | Tag `custom_docker_compose` / `is_multi_container` if applicable | metadata |
| 4 | No runtime URL fetches for task data | `environment` |
| 5 | Do not create `/tests` or `/solution` in Dockerfile | `environment` |
| 6 | Always write `reward.txt` (`0` on failure); no early `exit` before reward block | `test_build` |
| 7 | Default env vars in `test.sh` (`${TEST_DIR:-/tests}`) | `test_build` |
| 8 | No oracle-replication thresholds (~5% of oracle performance) | `task_difficulty` |

---

## Instruction (six principles)

1. Concise (typically 1–3 short paragraphs)
2. Well-specified outputs and paths
3. Interesting real engineering
4. No hints or solution walkthrough
5. Unique vs prior benchmark tasks
6. Absolute paths (`/app/...`)

Also: no canary string; no task name in body; environment docs describe **what**, not step-by-step **how**.

---

## tests/test.sh (canonical)

Verifier deps in **Dockerfile only** (`allow_internet = false`).

**Preferred** (portal Jun 3):

```bash
#!/bin/bash

if [ "$PWD" = "/" ]; then
    echo "Error: No working directory set. Please set a WORKDIR in your Dockerfile."
    exit 1
fi

pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA
rc=$?

if [ "$rc" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
```

- No `set -e` before reward block
- No trailing `exit` after `fi`
- Inline `if [ $? -eq 0 ]` still accepted by CI

---

## Rubrics (submission UI only)

Workflow:

1. Check **Generate rubric** → submit for CI (not reviewer)
2. Edit generated rubric in textbox
3. **Uncheck Generate rubric** → send to reviewer

Format:

- Every line: `Agent …, +N` or `Agent …, -N` (ASCII `-` only)
- Scores: ±1, ±2, ±3, ±5 — **never ±4**
- ≥3 distinct **negative** criteria
- 10–40 cumulative **positive** points (per milestone for milestone tasks)
- **All tasks:** `# Rubric 1` header required on its own line before criteria
- **Milestone tasks:** also `# Rubric 2`, `# Rubric 3`, … for each additional milestone

---

## Agent evaluation — solvable vs passing

| Term | Meaning |
|------|---------|
| **Passing a run** | All tests pass in one agent run |
| **Solvable** | Across 10 runs, **each test passes at least once** |

A task can be **solvable but never fully pass** — that is acceptable if failures are fair (not impossible infra).

**Difficulty labels** (5 runs × 2 models; evaluate Hard → Medium → Easy, stop at first match):

| Label | Threshold |
|-------|-----------|
| Hard | ≤20% on **best** model OR ≤20% on **worst** model |
| Medium | 20% < worst ≤ 60% |
| Easy | 60% < worst ≤ 80% |
| Reject | worst > 80% |

---

## Test-quality eval flags (double-check after manual review)

| Flag | Meaning |
|------|---------|
| `req-gap` | Instruction requires something with no test |
| `weak-assertion` | Test too loose to catch wrong solutions |
| `phantom-spec` | Test enforces undocumented behavior |
| `flaky-execution` | Correct solution can fail on timing/infra |
| `vacuous-test` | Test passes regardless of output |

---

## Reviewer feedback categories

Map revisions to these portal categories (see Common Errors):

| Category | Typical issues |
|----------|----------------|
| `instruction_styling` | Verbose LLM prose, relative paths, ambiguous language |
| `expose_answers` | Hints, golden values in env, answer-shaped instructions |
| `test_alignment` | Missing coverage, brittle tests, latency checks |
| `test_build` | `test.sh` runtime installs, reward file not written |
| `oracle` | Hardcoded solution, non-determinism |
| `environment` | Missing tmux/asciinema, reserved dirs, scaffolding filenames |
| `pinning` | Unpinned FROM/deps (distinct from general `environment`) |
| `task_difficulty` | Too easy, oracle-replication thresholds, impossible |

---

## Long context (`subcategories` includes `long_context`)

Required checklist (portal `reviewing-tasks/long-context-checklist.md`):

- ≥**50k tokens** of document-like content (not JSON/CSV/log dumps)
- Corpus **shipped** in `environment/`, authoritative to solution
- Requires **semantic reading**, not grep/keyword search
- Verifier asserts outputs that depend on document details
- Instruction points to document locations without leaking answers

---

## Pre-submission acceptance checklist

### Design

- [ ] ≥5 command multi-step task; human-written `instruction.md`
- [ ] Target **Hard** empirical difficulty; Python ≤20% predicted worst-model pass
- [ ] ≥3 documented failure modes + advanced engineering category
- [ ] Originality check — not a reskin of sibling tasks
- [ ] No latency tests, oracle-only branches, oracle-replication thresholds

### Files

- [ ] `task.toml`: `version = "2.0"`, `allow_internet = false`, accurate `codebase_size`
- [ ] Dockerfile: digest-pinned `FROM`, canonical final runtime base (or justified non-canonical), `tmux` + `asciinema`, verifier deps
- [ ] `test.sh`: preferred `rc=$?` reward block; no runtime network installs
- [ ] Every instruction requirement has a pytest with docstring
- [ ] Milestone layout if applicable (`steps/milestone_N/`)

### Repo gates (evidence required)

```bash
python3 scripts/lint_spec.py specs/<task>.md --strict
python3 scripts/spec_satisfiability.py specs/<task>.md --strict
python3 scripts/hard_difficulty_predictor.py specs/<task>.md --strict
python3 scripts/task_gate.py tasks/<task> --strict --report-dir /tmp/tb3-gates --skip-harbor
./scripts/check-task.sh --strict --report-dir /tmp/tb3-gates tasks/<task>
python3 scripts/harbor_gate.py tasks/<task> --oracle --oracle-stress 3 --nop --nop-stress 3
python3 scripts/step2b_ready.py tasks/<task> --strict --report-dir /tmp/tb3-gates ...
python3 scripts/harbor_gate.py tasks/<task> --oracle-repeat 10
python3 scripts/harbor_gate.py tasks/<task> --test-repeat 20
python3 scripts/reviewer_simulation.py tasks/<task> --strict   # confidence ≥ 90
python3 scripts/package_task.py tasks/<task> --out Task_Ready_To_Submit/<task>.zip --validate
python3 scripts/first_look_packet.py tasks/<task> --out /tmp/<task>-first-look.txt
python3 scripts/approve_task.py --strict --task-dir tasks/<task> --zip Task_Ready_To_Submit/<task>.zip
```

### Submission UI

- [ ] Rubric edited; Generate rubric **unchecked** before send to reviewer
- [ ] Rubric uses `# Rubric 1` header (and `# Rubric N` per milestone when applicable)
- [ ] Inspiration ID in form if applicable (submission-only field)

---

## When revision happens anyway

1. Read **all** feedback — address every point in one revision
2. Leave a revision summary in the UI
3. Re-run full repo gate stack (task edits stale `.step2b-checksum`)
4. Use `docs/PLATFORM_AUTO_EVAL.md` for `verifier_did_not_run` / `0/10` symptoms
5. Disputes: platform checkbox only, with concrete evidence
