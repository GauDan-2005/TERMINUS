# Fetch and archive platform feedback for a task

Use this prompt whenever you need a **full snapshot** of Snorkel submission feedback for one TERMINUS task. Each run creates a **new revision folder** under `personal_docs/feedback/{task_name}/revision_{N}/` — never overwrite an existing revision.

---

## Inputs

Replace placeholders before running:

| Placeholder       | Example                                                            |
| ----------------- | ------------------------------------------------------------------ |
| `{task_name}`     | `autograd-tape-alias`                                              |
| `{project_id}`    | `bfe79c33-8ab0-4061-9849-08d3207c9927`                             |
| `{submission_id}` | from `stb submissions list` or `tasks/{task_name}/.snorkel_config` |

---

## Prompt (give this to the agent)

```md
Fetch and document ALL platform feedback for TERMINUS task `{task_name}`.

Repo root:
/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS

Project ID:
{project_id}

## 1. Resolve submission ID

If unknown, list submissions and pick the latest row for this folder name:

    cd "/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS"
    stb submissions list --project-id {project_id} --show-folder-names

Prefer the submission linked in `tasks/{task_name}/.snorkel_config` if present.
If multiple submissions exist for the same folder, document all IDs in README but archive the **latest / active** one (the one in `.snorkel_config`, or the most recent created_at).

Record: submission_id, assignment_id, platform state (NEEDS_REVISION, EVALUATION_PENDING, etc.), created_at.

## 2. Choose revision number (always increment)

Output root:
personal_docs/feedback/{task_name}/

Rules:

- List existing `revision_*` directories under that path.
- Next revision = max(N) + 1, or `revision_1` if none exist.
- **Never** overwrite an existing revision folder.

Example path:
personal_docs/feedback/{task_name}/revision_3/

## 3. Pull everything from the platform

Run from repo root:

    stb submissions feedback {submission_id}
    stb submissions download {submission_id} -o "<revision_dir>/submitted-task"
    stb submissions fetch-task {submission_id} -o "<revision_dir>/metadata"

Copy the feedback bundle written by `stb submissions feedback` (under `/tmp/feedback_{submission_id}_*/`) into:

    <revision_dir>/feedback/

Expected feedback contents:

- notes.txt — revision notes, difficulty summary, quality checks
- agent_review.txt — harness agent review (warnings/suggestions)
- agent_logs/ — difficulty-check artifacts (if agents ran): summary-of-runs-comment.md, analyze-output-tbench-task.json, jobs/

Optional (for human review in browser):
stb submissions view {submission_id}

## 4. Write documentation inside the revision folder

Create these files in `<revision_dir>/`:

### README.md (required)

- Submission identity table (IDs, dates, state, folder name)
- Revision notes (verbatim from platform)
- Headline signals: difficulty, instruction sufficiency, quality checks, test quality, AutoEval build
- Agent performance table + per-test pass rates
- Common failure patterns and instruction gaps (from notes.txt / agent_logs)
- Directory layout map
- Refresh commands (feedback / download / fetch-task / view)
- Pointer to live workspace: `tasks/{task_name}/`

### revision-priorities.md (required)

- P0: platform blockers (AutoEval fail, build timeout)
- P1: instruction sufficiency / agent failure drivers
- P2: agent-review convention nits (pytest placement, category, etc.)
- P3: items that passed — no change needed
- Tests agents never pass (if applicable)

### rubric.txt (if present in metadata or personal_docs/rubrics/{task_name}-rubric.\*)

- Copy platform rubric lines; note sum if known (must be 10–40)

### metadata/submission\_{short_id}.json

- Full payload from `fetch-task` (keep as-is)

### metadata/submission\_{short_id}\_summary.json (recommended)

- Trimmed top-level summary if full JSON is huge (>100 KB)

Do **not** edit files under `submitted-task/` — that is the exact uploaded zip.

## 5. Sanity checks

- [ ] New revision folder exists and previous revisions untouched
- [ ] feedback/notes.txt and agent_review.txt present
- [ ] submitted-task/instruction.md matches what was on platform at fetch time
- [ ] README states submission state at time of capture (with date)
- [ ] If agent_logs/ missing, note in README that difficulty check did not run or failed early

## 6. Report back

Reply with:

- Path to the new revision folder
- Submission ID and platform state
- Top 3 revision priorities (one line each)
```

---

## Quick reference — CLI commands

```bash
cd "/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS"

# List submissions (find task + state)
stb submissions list --project-id bfe79c33-8ab0-4061-9849-08d3207c9927 --show-folder-names

# Fetch feedback bundle → /tmp/feedback_<id>_*/
stb submissions feedback <SUBMISSION_ID>

# Download submitted zip (extracted)
stb submissions download <SUBMISSION_ID> -o personal_docs/feedback/<task>/revision_<N>/submitted-task

# Full assignment metadata JSON
stb submissions fetch-task <SUBMISSION_ID> -o personal_docs/feedback/<task>/revision_<N>/metadata

# Open Experts UI
stb submissions view <SUBMISSION_ID>
```

---

## Directory layout (per revision)

```
personal_docs/feedback/{task_name}/
└── revision_{N}/
    ├── README.md
    ├── revision-priorities.md
    ├── rubric.txt
    ├── feedback/
    │   ├── notes.txt
    │   ├── agent_review.txt
    │   └── agent_logs/          # optional; ~25 MB when present
    ├── submitted-task/          # exact platform zip
    └── metadata/
        ├── submission_<id>.json
        └── submission_<id>_summary.json
```

---

## Revision numbering

| Situation                           | Next folder   |
| ----------------------------------- | ------------- |
| No prior archives                   | `revision_1/` |
| `revision_1/` exists                | `revision_2/` |
| `revision_1/` … `revision_4/` exist | `revision_5/` |

Each fetch is a **point-in-time snapshot**. After you `stb submissions update` and platform state changes, run this workflow again to create the next revision — do not replace the old folder.

---

## What each feedback artifact contains

| Artifact                                   | Use for                                                           |
| ------------------------------------------ | ----------------------------------------------------------------- |
| **notes.txt → Revision Notes**             | Why NEEDS_REVISION (AutoEval fail, timeout, human note)           |
| **notes.txt → Summary (difficulty check)** | HARD/MEDIUM, agent 0/N, per-test pass rates                       |
| **notes.txt → Analysis on Agent Failures** | Instruction sufficiency FAIL + failure patterns                   |
| **notes.txt → Quality check summary**      | 10-axis automated pass/fail                                       |
| **agent_review.txt**                       | Harness warnings (pytest in Dockerfile, category, etc.)           |
| **agent_logs/**                            | Per-trial trajectories, verifier stdout, analyze-output JSON      |
| **submitted-task/**                        | Ground truth of what reviewers evaluated                          |
| **metadata/\*.json**                       | Rubric text, test quality report, evaluation outcome, form fields |

---

## Notes

- `stb submissions feedback` has **no delete** command; archiving locally is your history.
- Use **`stb submissions update`** (not `create`) when revising a NEEDS_REVISION submission to avoid duplicate submission IDs.
- Older archives live under `personal_docs/reports/` from before this layout; new work uses `personal_docs/feedback/` only.
