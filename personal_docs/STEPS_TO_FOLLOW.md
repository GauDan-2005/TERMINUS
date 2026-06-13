# Terminal-Bench 3.0 (Edition 2) — End-to-End Task Authoring Runbook

Practical, command-level guide for taking a task from idea → spec → build →
tests → validation → zip → rubric → submission, with the exact rules, documents,
commands, and gotchas. Derived from the full `abi-feature-backtrack` lifecycle
(authoring, compliance audit, redesign-for-hardness, upstream-CI fix).

> Repo root in this environment:
> `/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS` (called `TERMINUS/` below).
> Run every `TERMINUS/` command from that directory.
>
> This runbook lives in `TERMINUS/personal_docs/`. Paths to repo files in section 1
> use a `../` prefix; paths to other personal docs use names relative to this folder.

---

## 0. Environment & tooling (one-time / per-session)

| Tool | Where | Notes |
|---|---|---|
| harbor CLI | `/tmp/opencode/harbor-venv/bin/harbor` (v0.7.0) | NOT on PATH; call by full path. Registered agents include `oracle`, `nop`, `terminus-2` (NOT `terminus`). |
| ruff | `/tmp/opencode/harbor-venv/bin/ruff` (0.15.13) | NOT on default PATH → local `check-task.sh` **skips lint** unless you put this on PATH. Upstream CI runs it → put it on PATH locally to get parity. |
| stb CLI | `~/.local/bin/stb` (v2.2.0) | Platform CLI; `stb keys show` emits AI creds (OpenAI/Portkey). `stb login` is interactive (browser) — only the user can do it. |
| Docker | system `docker` (v28.x) | Daemon must be up (`docker ps`). harbor builds task images here. |
| python3 | system (3.12) | Repo harness scripts are stdlib-only. |

Session prep:
```bash
cd "/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS"
export PATH="/tmp/opencode/harbor-venv/bin:$PATH"   # <-- gives local ruff = upstream parity
eval "$(stb keys show)"                               # exports OPENAI_API_KEY/OPENAI_BASE_URL (Portkey)
docker ps >/dev/null && echo "docker up"
```
Credential reality: `stb keys show` provides **OpenAI/Portkey only**. Anthropic
models route via Portkey using the OpenAI-compatible id `openai/claude-opus-4-6`
(NOT `anthropic/claude-opus-4-6`, which fails "Missing Anthropic API Key").
`stb harbor check` (Step 3a-Q) uses a Claude-Code evaluator and is **infeasible**
with these creds — it is opt-in and `approve_task.py` passes without it.

---

## 1. Documents to read (and which step they govern)

| Document | Governs |
|---|---|
| `../AGENTS.md` | Always-on routing + must-fire bullets |
| `../docs/ARCHITECTURE.md` | Which file owns which layer |
| `../workflow-prompts.md` | The Step 1→4 pipeline + "Ralph discipline" |
| `../commands.md` | Canonical CLI reference + Docker/harbor bring-up |
| `../REPO_CONVENTIONS.md` | Intentional waivers (don't "fix" these) |
| `../.cursor/rules/00-authoring-critical.mdc` | Always-on critical path + forbidden shortcuts |
| `../.cursor/rules/idea-validation.mdc` | Step 2a: 5 hardness axes, 21 anti-trivialization checks, discovery budget, construction manifest |
| `../.cursor/rules/task-creation.mdc` | Step 2b construction contract (layout, instruction, Dockerfile, test.sh, solve.sh) |
| `../.cursor/rules/difficulty-calibration.mdc` | Collapse audit Part A (RC/CR/GX) + Part B per-test feasibility |
| `../.cursor/rules/review-and-submit.mdc` | Step 3b structural review §1-7 + ACCEPT/REJECT criteria |
| `announcement.md` | Project updates: `allow_internet=false`, Hard→Medium→Easy thresholds, Docker best-practices |
| `references_announcement/docker.md` | **Dockerfile & image best-practices — reviewer-verified, NOT gated** (mirrored in `task-creation.mdc` env/Dockerfile + `review-and-submit.mdc` §2) |
| `references_announcement/long_context.md` | `long_context` corpus standard (only if subcategory=`long_context`) |
| `../specs/validation_schema.json` | Exact schema for the Step 2a evidence JSON |
| `../specs/README.md` | Spec-file schema docs |
| `../TASK_PROPOSAL_RUBRIC.md` | **Scoring-rubric authoring guidelines** (the per-task agent-behavior rubric) |
| `../web/TASK_PROPOSAL_RUBRIC.md` | Phase-1 idea-screening rubric (different artifact — Accept/Reject template) |
| `CLI_installation.md` | `stb` CLI install/usage + real-agent commands |

Golden rule: **never invent paths/fields/commands from memory** — open the file
or `commands.md`. Anti-collapse philosophy: a task is only acceptable if it stays
hard *after the instruction is fully honest* — the mechanical gates enforce that
structurally; empirical agent runs enforce it in fact.

---

## 2. The pipeline at a glance (cheapest-gate-first)

```
Step 1  Ideate (ChatGPT seed bank)            web/ bundle
Step 2a Validate idea + author spec            scripts/validate_loop.py  (GATE: GO)
Step 2b Construct task files                   tasks/<t>/...
        → static + collapse + 5 hard-gates     scripts/check-task.sh + scripts/task_gate.py
        → oracle/NOP stress 3/3 (minutes)      scripts/harbor_gate.py --oracle-stress 3 --nop-stress 3
Step 3a (opt) verifier-health / quality-check  scripts/verifier_health.py / stb harbor check
Step 3b Paper review (structural + collapse)   review-and-submit.mdc
Step 4  Oracle 10x + verifier 20x +            scripts/harbor_gate.py --oracle-repeat 10 / --test-repeat 20
        reviewer-sim → zip → approve           scripts/reviewer_simulation.py / scripts/approve_task.py --strict
        Empirical difficulty (real agents)     harbor -a terminus-2
        Rubric (external)                       TASK_PROPOSAL_RUBRIC.md
        Submit                                  stb submissions create
```
**Dirty-flag discipline (critical):** editing ANY file under `tasks/<t>/`
invalidates all prior Step 2b/agent evidence. You must re-enter at the cheapest
unverified gate: `check-task.sh` (rewrites `.step2b-checksum`) → rebuild zip →
oracle/NOP stress 3/3. The 10×/20× and the agent matrix only run on a *locked* tree.
`approve_task.py` mechanically refuses on checksum/zip mismatch.

---

## STEP 1 — Ideate (seed bank)

Read `web/bulk-idea-generation.md` + `web/option-a-seed-refinement.md`. Produce
hard-only ideas (frontier-resistant). Screen with `web/TASK_PROPOSAL_RUBRIC.md`
(Accept/Reject). Inputs you must fix: idea, language(s), difficulty=hard,
category, task name. Blocked: new multi-container, new UI-building, easy/medium,
Python-without-reason. Pick a category where frontier models are weak
(system-admin, build/dependency, debugging, scientific-computing).

---

## STEP 2a — Validate idea & author the spec  (GATE)

Authoring artifacts live in `TERMINUS/specs/`:
- `specs/<t>.md` — Decision, Metadata (`version: 2`), `## Authoring Brief` with
  the **3 mandatory v2 sub-sections**: *Triviality (Avoidance) Ledger*,
  *Per-gate Pitfall Inventory*, *Initial Draft Commitments*, plus the
  Construction manifest (symbol_table, flipping_point_contract, decoy_manifest,
  code_forbidden_tokens).
- `specs/<t>-reviewer.md` — reviewer appendix.
- `specs/<t>-attempt-N-evidence.json` — structured evidence, must satisfy
  `specs/validation_schema.json` exactly. Required top-level keys:
  `hardness_axes`(5), `anti_trivialization_checks`(21), `rubric_axes`(6),
  `instruction_completeness_test`, `discovery_budget`(≥3),
  `instruction_specificity`(level=`symptoms-only`), `attack_path`,
  `smallest_plausible_patch`, `collapse_audit`, `topology_enumeration`(≥3, each
  ≥3 locations), `construction_manifest`, `naming_pass`. (Note: `naming_pass`
  has NO `recomputed_concentration` key — `additionalProperties:false`.)

Rules: `.cursor/rules/idea-validation.mdc`. The instruction must be
**symptoms-only** (no algorithm/file/cause/threshold/schema). `naming_pass.
instruction_nouns_extracted` must equal `construction_manifest.
code_forbidden_tokens` as a set. flipping_point concentration cap ≤ 0.5
(no single location controls a majority of tests); ≥3 locations; symbol_table
≥3 entries; `construction_manifest.json` in the task must later mirror this
block verbatim (the 2-vs-7 drift is a real failure mode — keep them identical).

Commands:
```bash
python3 scripts/validate_loop.py record <task-name> --evidence specs/<task-name>-attempt-N-evidence.json
python3 scripts/validate_loop.py finalize <task-name>      # enforces v2 lint --strict
python3 scripts/lint_spec.py specs/<task-name>.md --strict
python3 scripts/validate_loop.py status <task-name>
```
PASS criteria: `record` prints `ACTION: GO` with `0F, 0W`; `finalize` →
`OK: … passes strict lint`. Iterate the spec/evidence only (cheap) until GO.
Gotcha: `validate_loop.py record` may blank the input evidence file after
reading — keep your source and re-write if you must re-record.

---

## STEP 2b — Construct the task

Standard single-step layout under `tasks/<t>/` (from `task-creation.mdc`):
```
instruction.md  task.toml  output_contract.toml  construction_manifest.json
environment/{Dockerfile, ... ≥20 non-Docker files ...}
solution/solve.sh
tests/{test.sh, test_outputs.py}
```
Key construction rules:
- **instruction.md**: human-voiced, symptoms-only, absolute in-container paths,
  no task-name/canary, no emojis, minimal causal/temporal connectives
  (GX6 flags "explains WHY/WHEN"). Its nouns = `code_forbidden_tokens`.
- **task.toml**: `version="2.0"`, anonymous author, `number_of_milestones=0`,
  `verifier.timeout_sec ≤ 1800`, integer `[environment]` resources.
- **output_contract.toml**: real TOML (newlines!), at task root; banned from zip.
- **environment/**: ≥20 files; opaque fix-path names; NO golden answers, NO
  hints/`STEP:`/`HINT:`, NO `BUG:`/correctional vocab near the defect (GX1),
  NO AI-scaffolding filenames; pinned Dockerfile (digest base + pinned apt) —
  plus the full docker.md checklist in "STEP 2b — Docker/image compliance" below.
- **solution/solve.sh**: `set -euo pipefail`; ADDS substantive logic (RC1),
  ≥80 non-boilerplate semantic-diff LOC over the manifest symbols across ≥2
  roots (RC7/GX3); deterministic (no randomness/network/time).
- **tests/test.sh**: canonical template, **must NOT** add `set -euo pipefail`
  (REPO_CONVENTIONS). Reward footer must use `if [ $? -eq 0 ]; then` immediately
  after pytest — **not** legacy `RC=$?` / `exit "$RC"` (upstream AutoEval rejects it).
- **tests/test_outputs.py**: ≥ (here 12) tests, each with a one-line
  **docstring** (static check requires it), domain-valued assertions, expected
  values **re-derived in python** (not read from env), NOP-failing,
  independent. One import per line (ruff **E401**). No unused imports
  (`hashlib` etc. — GX8 flags test imports with no env/instruction home).
- **construction_manifest.json**: must equal the spec's manifest block. CR8:
  no single solver-visible file may reference >2 manifest symbols → split
  declarations across headers and route orchestration so each file ≤2.

Make the hardness a genuine cross-layer invariant (fixing one layer regresses
another) with state the solver must reconstruct by *running* sequences — not an
answer-shaped one-file patch. A single clean run may look healthy; the defect
emerges across the scripted sequence. Keep one purely-local sub-fix so an
expert path exists (avoid 0/N unsolvable-by-construction).

---

## STEP 2b gates — static + collapse + 5 hard-gates + oracle/NOP stress

One-command preflight (Phase A static + Phase B temp-zip + Phase C checksum):
```bash
export PATH="/tmp/opencode/harbor-venv/bin:$PATH"      # ruff = upstream parity
./scripts/check-task.sh --strict --report-dir /tmp/tb3-gates tasks/<task-name>
```
PASS = exit 0, "Preflight passed (Phase A + B + C)". Collapse WARN (exit 2) is
non-blocking but must be justified at Step 3b; collapse FAIL (exit 1) blocks.

The 5 hard-gates (run via `task_gate.py`; they also write the JSON reports `approve_task.py --strict` consumes):
```bash
python3 scripts/task_gate.py tasks/<task-name> --strict --report-dir /tmp/tb3-gates --skip-harbor
# hard_difficulty_predictor (Python tasks must predict worst-model pass-rate <= 20%),
# spec_test_alignment, spec_gap_detector, sandbox_risk_gate.
```
Individual gates if needed:
```bash
python3 scripts/run_static_checks.py --task-dir tasks/<task-name> --version edition_2
python3 scripts/collapse_check.py tasks/<task-name>           # 0=PASS 1=FAIL 2=WARN
/tmp/opencode/harbor-venv/bin/ruff check tasks/<task-name>/   # default config
```
Collapse signals to know: RC1 (oracle adds, not deletes), RC6 (symptoms-only),
RC7/GX3 (≥80 LOC), RC8 (root distribution), CR1 (symbols match manifest — note
its scanner doesn't parse `.cmake`, so cmake-function symbols WARN; documented),
CR2 (flip ≤0.5/≥3 locs/≥2 roots), CR8 (≤2 manifest symbols/file), GX1 (no
correctional vocab in env), GX6 (instruction not causal), GX9/GX10 (no answer
enumeration / polarity contradiction).

Oracle + NOP **stress 3/3** (the Step 2b correctness gate; needs harbor + creds).
`harbor_gate.py` runs harbor and enforces that *every* trial hits the expected
reward, not just the mean:
```bash
eval "$(stb keys show)"
export PATH="/tmp/opencode/harbor-venv/bin:$PATH"   # harbor_gate finds harbor on PATH
python3 scripts/harbor_gate.py tasks/<task-name> --oracle --oracle-stress 3 --nop --nop-stress 3
```
PASS = oracle **3/3** all at 1.0, NOP **3/3** all at 0.0, 0 errored trials. Then
Docker cleanup (see §Cleanup). Anything off → fix → re-enter at `check-task.sh`.
(Single manual run if you need one: `$H run -p tasks/<t> -a oracle --job-name <t>-oracle-1x -y`.)

Local pre-check before spending harbor: `g++ -std=c++17 …` compile the TUs;
broken baseline should fail the tests' required keys → guarantees NOP=0.

---

## STEP 2b — Docker/image compliance (reviewer-verified — the gates do NOT check this)

`announcement.md` added a Dockerfile & image best-practices standard
(`references_announcement/docker.md`), now mirrored in
`.cursor/rules/task-creation.mdc` "environment/Dockerfile" and
`review-and-submit.mdc` §2. **None of `run_static_checks.py`, `collapse_check.py`,
or `approve_task.py` enforce most of it** — a task can pass every gate and still
violate these rules (the shipped `async-executor-liveness` image did: no
tmux/asciinema, no `.dockerignore`, `COPY . /app`, no OCI labels). Verify each by
hand before zipping; this checklist is part of the acceptance definition:

- [ ] `tmux` AND `asciinema` installed (base image or pinned). **Missing either →
      real-agent (`terminus-2`) runs fail even though the oracle passes.**
- [ ] every `FROM` digest-pinned; prefer a sanctioned base image for the runtime class
- [ ] deps pinned via lockfile; downloaded binaries checksum-verified (no `curl|sh`); `SOURCE_DATE_EPOCH` set
- [ ] layers least→most volatile (manifests before source); NO `COPY . .` / `COPY . /app`
- [ ] `.dockerignore` present (non-trivial tasks)
- [ ] one apt txn: `--no-install-recommends`, no `apt-get upgrade`, `rm -rf /var/lib/apt/lists/*`, pinned versions
- [ ] multi-stage build when the image compiles/bundles (unless the agent itself must compile)
- [ ] source as files, not Dockerfile heredocs; `COPY --chmod`/`--chown`, not recursive `chmod -R`/`chown -R`
- [ ] no `.git`/`.env`/credentials/caches in the image; OpenContainers labels (`org.opencontainers.image.*`)
- [ ] `[environment]` declares `cpus`/`memory_mb`/`storage_mb`/`build_timeout_sec`/`gpus`/`gpu_types`/`docker_flags` from real peak use
- [ ] (only if subcategory=`long_context`) corpus ≥50k document tokens, shipped not generated, authoritative, not grep-solvable — see `references_announcement/long_context.md`

---

## STEP 3a — Optional diagnostics (opt-in, revision-triggered)

- Verifier health (order/partial-oracle): `python3 scripts/verifier_health.py
  --task-dir tasks/<t> --output-json /tmp/<t>-vh.json`.
- Quality check (GPT-5.2/Claude rubric): `stb harbor check tasks/<t> -m
  "openai/gpt-5.2" -o /tmp/<t>-qc.json` then `python3
  scripts/quality_check_adjudicate.py --task-dir tasks/<t> --qc-output /tmp/<t>-qc.json`.
  **Env note:** `stb harbor check` is Claude-Code-based and fails with
  OpenAI/Portkey-only creds ("Claude Code returned an error result"). It is
  opt-in; `approve_task.py` passes without it (quality gate defaults PASS with
  no waiver). Gate-path can be sanity-checked with a synthetic all-pass QC JSON.
  Adjudicate findings as `task-defect` (fix) / `convention-conflict` (waive with
  `enforcing_rule.file`+line) / `unsupported` (waive with negative-lookup).
- Hard-gate drill-down (3a-A): the `task_gate.py` gates (`spec_test_alignment`,
  `spec_gap_detector`, `sandbox_risk_gate`, `hard_difficulty_predictor`) run in
  Step 2b; re-run `python3 scripts/task_gate.py tasks/<t> --strict --report-dir
  /tmp/tb3-gates --skip-harbor` standalone when chasing one of those findings.

---

## STEP 3b — Paper review (no oracle runs)

`.cursor/rules/review-and-submit.mdc` §1–7 (Instruction, Environment, Oracle,
Verifiers, Metadata, Structure, Difficulty) + `difficulty-calibration.mdc`
Part A (residual-hardness/collapse audit) and Part B (per-test feasibility:
single-valid-approach, chain-dependency, order-sensitivity, flakiness). Any
edit → dirty-flag → re-enter Step 2b gates.

---

## STEP 4 — Oracle 10×, zip, approve, difficulty, submit

1) Oracle 10× + verifier 20× flake guards + reviewer simulation (only place 10×/20× run):
```bash
python3 scripts/harbor_gate.py tasks/<t> --oracle-repeat 10   # PASS: 10/10 all at 1.0
python3 scripts/harbor_gate.py tasks/<t> --test-repeat 20     # PASS: 20/20 all at 1.0 (verifier flakiness)
python3 scripts/first_look_packet.py tasks/<t> --out /tmp/<t>-first-look.txt   # then record first_look_result JSON (docs/FIRST_LOOK_DRY_RUN.md)
python3 scripts/reviewer_simulation.py tasks/<t> --strict --report-dir /tmp/tb3-gates \
  --first-look-result /tmp/<t>-first-look-result.json --json   # BLOCK if would_reject or reviewer_confidence < 90
```
(Raw single oracle 10× if needed: `$H run -p tasks/<t> -a oracle -k 10 -n 10 --job-name <t>-oracle-10x -y`.)
2) Build the submission zip (exclusion set mirrors the `-x` list in `scripts/check-task.sh` / `commands.md` § Packaging;
add `*/.*` so nested dotfiles like `state/.keep` don't break source↔zip parity):
```bash
rm -f Task_Ready_To_Submit/<t>.zip
( cd tasks/<t> && zip -rq "../../Task_Ready_To_Submit/<t>.zip" . \
  -x '*/__pycache__/*' '*.pyc' '.*' '*/.*' \
  -x 'output_contract.toml' 'quality_check_adjudication.json' \
  -x 'construction_manifest.json' 'rubric.txt' 'rubrics.txt' \
  -x 'CLAUDE.md' '*/CLAUDE.md' 'AGENTS.md' '*/AGENTS.md' 'skills.md' '*/skills.md' \
  -x '.cursor/*' '*/.cursor/*' '.aider/*' '*/.aider/*' \
  -x '.continue/*' '*/.continue/*' '.claude/*' '*/.claude/*' )
python3 scripts/validate_submission_zip.py Task_Ready_To_Submit/<t>.zip   # RESULT: PASS
```
3) Approval gate (`--strict`; re-checks checksum/static/collapse/zip/parity + the Step 2b gate reports):
```bash
python3 scripts/approve_task.py --strict --task-dir tasks/<t> \
  --zip Task_Ready_To_Submit/<t>.zip --skip-verifier-health \
  --actionability-report /tmp/tb3-gates/<t>-actionability_check.json \
  --no-hidden-contracts-report /tmp/tb3-gates/<t>-no_hidden_contracts.json \
  --obfuscation-lint-report /tmp/tb3-gates/<t>-obfuscation_lint.json \
  --first-look-result /tmp/<t>-first-look-result.json \
  --oracle-job-dir jobs/<oracle-job-dir> --nop-job-dir jobs/<nop-job-dir>
# PASS: "Approval gate: PASS", "Blocking failures: - none". collapse WARN ok.
```
`--skip-verifier-health` is the routine path; swap in `--verifier-health <json>`
only if Step 3a-V ran. The `--actionability-report`/`--no-hidden-contracts-report`/
`--obfuscation-lint-report` paths come from `task_gate.py --report-dir /tmp/tb3-gates`
(Step 2b); `--first-look-result` from the first-look packet (sub-step 1b).

4) **Empirical difficulty** (the real hard-only test — the mechanical gates do
NOT measure it). Use the registered reference agent `terminus-2`:
```bash
$H run -a terminus-2 -m "openai/gpt-5.2"          -p "tasks/<t>" --job-name <t>-gpt-N  -y
$H run -a terminus-2 -m "openai/claude-opus-4-6"  -p "tasks/<t>" --job-name <t>-opus-N -y
```
Method: cheap **2-run probe** (1 GPT-5.2 + 1 Opus). If ≤1 solve → full **6-run
matrix** (×3 each) for the verdict. Target **≤1/6** frontier pass. 100% pass =
too easy (REJECT-level under review-and-submit §7); 0/6 with a deterministic
oracle 10/10 + an expert path = genuinely hard (good). An import/format-only
edit cannot change difficulty — don't re-spend the matrix for it.

5) Submit (platform `stb`; rubric is set in the UI, not the CLI):
```bash
stb projects list
stb submissions create ./tasks/<t> -p PROJECT_ID --time MINUTES
stb submissions list -p PROJECT_ID
```

---

## Rubric authoring (external artifact — never in the zip)

Rubric files (`rubric.txt`/`rubrics.txt`) are in `scripts/validate_submission_zip.py`
`FORBIDDEN_ROOT_FILES`. Keep the rubric **outside** the repo (e.g.
`…/AirDawg/<task>-rubric.md`). Follow `TERMINUS/TASK_PROPOSAL_RUBRIC.md`:
- Every line starts `Agent ` and ends `, [Score]`.
- Scores only ±1, ±2, ±3, ±5 (NEVER ±4). Critical ±5 / Major ±3 / Minor ±1-2.
- Binary; ≥5 checks; **≥3 negative** checks; positive phrasing always.
- **Total cumulative positive ∈ [10, 40]** (per milestone for milestone tasks).
- Map to the optimal solve sequence; no double-counting; no perfect score.
- Trace-evidenced agent behavior only; no pytest/meta checks; no
  oracle/NOP/approval/zip/flakiness references.
Validate by tabulating each rule vs the rubric before delivering.
(`web/TASK_PROPOSAL_RUBRIC.md` is a *different* doc — phase-1 idea screening.)

---

## Docker cleanup (run after EVERY harbor batch — user requirement)

```bash
ids="$(docker ps -aq --filter name='<task-name>__')"; [ -n "$ids" ] && docker rm -f $ids
docker container prune -f; docker image prune -f; docker network prune -f
# final sweep after the last harbor run of a session:
docker system prune -af && docker builder prune -af
```
Only run cleanup after a harbor run has fully exited and its `result.json` is
read (pruning mid-run kills live trials → false errors). If you ran no harbor
workload, do NOT `system prune -af` (it removes unrelated images).

---

## Upstream-CI parity & common failure fixes

| Symptom | Cause | Fix |
|---|---|---|
| Upstream `run_static_checks.py` ruff `E401` | local host had no ruff → lint skipped | one import per line; verify with harbor-venv ruff on PATH |
| `output_contract.toml could not be parsed` | wrote literal `\n` not newlines | real TOML newlines; `tomllib.loads` to verify |
| `missing informative docstrings` | tests lack docstrings | one-line `"""…"""` in every `test_*` |
| collapse `CR8 FAIL` | a file references >2 manifest symbols | split decls across headers; route orchestration |
| collapse `GX1 FAIL` | `BUG:`/correctional comments in env | neutral plausible code; no correctional vocab |
| collapse `GX6 FAIL` | instruction explains WHY/WHEN | terse symptoms-only WHAT; cut after/when/so/because |
| `Unknown agent type: TERMINUS` | `terminus` unregistered in harbor 0.7.0 | use `-a terminus-2` |
| `Missing Anthropic API Key` | `-m anthropic/...` with Portkey creds | use `-m openai/claude-opus-4-6` |
| approve `source/zip mismatch` | stale zip / nested dotfile (`state/.keep`) | rebuild zip with `*/.*` excluded |
| approve `step2b checksum` FAIL | task file edited after preflight | re-run `check-task.sh` (dirty-flag) |

---

## Acceptance definition ("submission-ready")

ALL of: `validate_loop` GO (0F/0W) + `lint_spec --strict` PASS · construction
manifest mirrors spec · `run_static_checks.py` PASS (ruff active) ·
`collapse_check.py` 0 FAIL (WARN justified) · `task_gate.py` 5 hard-gates PASS
(hard_difficulty_predictor ≤20% worst-model for Python, spec_test_alignment,
spec_gap_detector, sandbox_risk_gate) · oracle/NOP **stress 3/3** (3×1.0 / 3×0.0) ·
oracle **10×=10/10** · verifier **20×=20/20** · `reviewer_simulation.py --strict`
reviewer_confidence ≥ 90 · `validate_submission_zip.py` PASS · source↔zip parity PASS ·
`approve_task.py --strict` exit 0 · **empirical difficulty ≤1/6 frontier** (with a
deterministic oracle proving solvability) · **docker.md image checklist verified**
(reviewer-verified — tmux/asciinema, `.dockerignore`, narrow `COPY`, OCI labels,
lockfiles; see "STEP 2b — Docker/image compliance") · rubric authored externally &
rule-conformant · Docker swept · task tree checksum-clean.

The mechanical gates prove *structure*; the agent matrix proves *hardness*.
A task is not done until both pass.
