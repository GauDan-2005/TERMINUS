# personal_docs

Authoring notes, runbooks, review artifacts, and reference material for the TERMINUS task repo. These files are **not** part of task submission zips.

## Layout

| Path | Purpose |
|------|---------|
| `STEPS_TO_FOLLOW.md` | End-to-end task authoring runbook |
| `AGENT SETUP MANIFEST.txt` | Host environment snapshot (tool versions + `stb` CLI install) |
| `review.md`, `TODO.md`, `STATUS.md` | Active working checklists and submission/progress status |
| `feedback.md` | Feedback-fetch workflow notes |
| `Project_ideas.md`, `project_ideas_new.md` | Task idea banks |
| `docs/` | Local reference docs (CI checks, difficulty, Docker best-practices, gate reconciliations, long-context); canonical copies live in `../docs/DOCKER_REQUIREMENTS.md` and `../docs/REVIEW_CHECKLIST.md` |
| `feedback/` | Read-only platform reviewer evidence + the feedback-fetch workflow |
| `questions/` | Authored per-task submission Q&A |
| `reports/` | Session reports (e.g. `reports/<task>-<date>.md`) |
| `rubrics/` | Per-task rubric snapshots |

## Repo root

The TERMINUS repo lives at `../` (parent of this folder). Run harbor and static checks from there:

```bash
cd "/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS"
```
