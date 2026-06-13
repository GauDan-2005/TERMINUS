# personal_docs

Authoring notes, runbooks, review artifacts, and reference material for the TERMINUS task repo. These files are **not** part of task submission zips.

## Layout

| Path | Purpose |
|------|---------|
| `STEPS_TO_FOLLOW.md` | End-to-end task authoring runbook |
| `CLI_installation.md` | Snorkel `stb` CLI install and usage |
| `announcement.md` | Project policy updates |
| `references_announcement/` | Platform reference templates and best-practices |
| `prompt.md`, `review.md`, `TODO.md`, `STATUS.md`, `PROGRESS_doc-gate-sync.md` | Active working prompts, checklists, and submission/progress status |
| `reports/` | Execution plans and session reports (e.g. `reports/<task>/<task>-plan.md`) |
| `feedback/`, `feedback.md` | Read-only platform reviewer evidence + the feedback-fetch workflow |
| `rubrics/`, `rubric_*.md`, `revision_*.md` | Per-task rubric snapshots and revision notes |
| `docker_requirements.md`, `review_checklist.md`, `ci_checks.md` | Source specs (canonical copies live in `../docs/DOCKER_REQUIREMENTS.md` and `../docs/REVIEW_CHECKLIST.md`) |
| `Terminal-main-new/` | Latest upstream snapshot (the doc/tooling sync source) |
| `local-scripts-backup-2026-06-13/` | Backup of the 2 overwritten reviewer-validated scripts |

## Repo root

The TERMINUS repo lives at `../` (parent of this folder). Run harbor and static checks from there:

```bash
cd "/media/gaurav-s-ubuntu/COLLEGE MATERIAL/Work/AirDawg/TERMINUS"
```
