IDEA:

# scientific-computing

## adaptive-mesh-conservation

- **Languages:** C++
- **Idea:** A finite-volume simulation loses conservation after adaptive mesh refinement, coarsening, and checkpoint restart.
- **Hardness hook:** Requires coordinating flux registers, mesh topology, restart serialization, and refinement-boundary updates.

===

These are the prompts for each task:

```md
# 0. session prep (run once, from the TERMINUS dir)

cd "/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS"
export PATH="/tmp/opencode/harbor-venv/bin:$PATH"   # ruff parity with upstream CI
eval "$(stb keys show)" # OpenAI/Portkey creds for harbor
docker ps >/dev/null && echo "docker up"

Read these FIRST and treat them as the source of truth (the gates do NOT cover all of them):

- /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS/personal_docs/STEPS_TO_FOLLOW.md (the runbook)
- /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS/personal_docs/announcement.md (the new changes)
- /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS/personal_docs/references_announcement/docker.md
- /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS/personal_docs/references_announcement/issues_fixes.md
- /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS/personal_docs/references_announcement/long_context.md
- /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS/.cursor/rules (all .mdc)
- /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS/workflow-prompts.md

---

# 1. create or update the task

Use the IDEA above and follow .cursor/rules (task-creation.mdc is the construction
contract). If tasks/<task-name>/ already exists, UPDATE it in place — do not
regenerate from scratch and clobber existing work. Single-step debugging/Rust
task, difficulty = hard, [environment].allow_internet = false. Do NOT label it
long_context (long_context.md does not apply to this task).

---

# 2. tests + difficulty calibration

Generate 6+ behavior tests (aim 10-15): each with a one-line docstring, domain-valued
assertions re-derived in code (not read from env), NOP-failing, independent.
Calibrate as HARD per .cursor/rules/difficulty-calibration.mdc — collapse RC/CR/GX
must be 0 FAIL and the instruction must stay symptoms-only.

---

# 3. Docker & image compliance (REQUIRED — reviewer-verified, the checkers do NOT enforce this)

Apply references_announcement/docker.md and the "environment/Dockerfile" section of
task-creation.mdc by hand. None of run_static_checks.py / collapse_check.py /
approve_task.py catch these, so confirm ALL of them yourself:

- tmux AND asciinema installed (missing either => real-agent runs fail though oracle passes)
- every FROM digest-pinned; sanctioned base image for the runtime class
- deps pinned via lockfile; downloaded binaries checksum-verified (no curl|sh); SOURCE_DATE_EPOCH set
- layers least->most volatile (manifests before source); NO `COPY . .` / `COPY . /app`
- .dockerignore present (non-trivial tasks)
- one apt txn: --no-install-recommends, no apt-get upgrade, rm -rf /var/lib/apt/lists/\*, pinned versions
- multi-stage build if the image compiles/bundles (unless the agent itself must compile)
- source as files (no Dockerfile heredocs); COPY --chmod/--chown, not recursive chmod -R/chown -R
- no .git/.env/credentials/caches in the image; OpenContainers labels (org.opencontainers.image.\*)
- [environment] declares cpus/memory_mb/storage_mb/build_timeout_sec/gpus/gpu_types/docker_flags from real peak use

---

# 4. oracle 1x + NOP + run the tests (then clean up Docker)

Give me an oracle command I can run, and run it yourself:
H=/tmp/opencode/harbor-venv/bin/harbor
$H run -p "tasks/<task-name>" -a oracle --job-name <task>-oracle-1x -y
$H run -p "tasks/<task-name>" -a nop --job-name <task>-nop-1x -y
PASS = oracle mean 1.0, NOP 0.0, 0 errored trials. Then run Docker cleanup
(see STEPS_TO_FOLLOW.md "Docker cleanup").

---

# 5. fix-check-loop (cheapest gate first; build the zip BEFORE approve)

Loop until green; after ANY task edit re-enter at check-task.sh (dirty-flag):
./scripts/check-task.sh tasks/<task-name>
python3 run_static_checks.py --task-dir tasks/<task-name> --version edition_2
python3 collapse_check.py tasks/<task-name>

# build the zip (step 7) THEN:

python3 approve_task.py --task-dir tasks/<task-name> --zip Task_Ready_To_Submit/<task-name>.zip --skip-verifier-health
quality_check_adjudicate.py is OPT-IN: `stb harbor check` needs Claude-Code creds
that are unavailable here, so do NOT loop on it — approve_task.py passes without it.
Clean up Docker after each harbor batch.

---

# 6. empirical difficulty (the announcement's REAL hard test; gates measure structure only)

Confirm HARD per announcement.md (Hard -> Medium -> Easy by frontier accuracy):
H=/tmp/opencode/harbor-venv/bin/harbor
$H run -a terminus-2 -m "openai/gpt-5.2" -p "tasks/<task-name>" --job-name <task>-gpt-N -y
$H run -a terminus-2 -m "openai/claude-opus-4-6" -p "tasks/<task-name>" --job-name <task>-opus-N -y
Target <=1/6 frontier pass with a deterministic oracle (10/10). Clean up Docker after.

---

# 7. create zip

Build per validate_submission_zip.py (exclusion set = scripts/check-task.sh:64-73 plus `*/.*`):
python3 validate_submission_zip.py Task_Ready_To_Submit/<task-name>.zip # must print PASS

---

# 8. generate rubrics (external file — never inside the zip)

Follow /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS/TASK_PROPOSAL_RUBRIC.md
(the ROOT file = scoring rubric; the web/ one is idea-screening). Total positive
score 10-40; scores only +/-1, +/-2, +/-3, +/-5 (never +/-4); >=5 checks incl.
```

===

Check this for steps to follow: /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS/personal_docs/STEPS_TO_FOLLOW.md
Ive already given the Idea here.

Make sure you check all the referenced files, docs and rules and skills that were mentioned

===

Use these files, since there are new changes, so adhere to these files and make relevant changes to the task, then test and rezip as required.

Workflow Proposal file: /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS/workflow-prompts.md

References files: /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS/personal_docs/references_announcement
New announcement changes: /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS/personal_docs/announcement.md
CLI testing: /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS/personal_docs/CLI_installation.md

====================================================================================

Great now document the plan in here: /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS/personal_docs/reports/rollback-combat/rollback-combat-plan.md
and start executing the plan

====================================================================================

This is the Status file: /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS/personal_docs/STATUS.md

I want you to maintain a status of all the tasks here.
The status should have all the onse which already come when we check for status using `stb submissions list --project-id bfe79c33-8ab0-4061-9849-08d3207c9927`

but should also have a column for local dev, it should have, submitted, in progress, working on revision, needs revision, accepted.

===

check this file: /media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS/personal_docs/feedback.md

and do `stb submissions list --project-id bfe79c33-8ab0-4061-9849-08d3207c9927` to get the list of all submissions that need revision.
Finally according to the doc(feedback.md) file the latest feedbacks in the feedback/ folder for all the tasks separately.
