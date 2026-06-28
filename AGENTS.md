# AGENTS.md

TB3 Ed2 authoring. Unit `tasks/<task-name>/`. Start `docs/ARCHITECTURE.md`.
Always-on router — open the linked file before acting.

## Non-negotiables

1. No PASS/READY/APPROVED/SUBMIT claim without command output.
2. Never invent paths, `task.toml` fields, or commands — open the file first.
3. Empirical difficulty (`agent_test.sh`, real frontier agents, worst-model ≤20%) is a hard Step 4 gate; proxies never replace it.
4. Task edits stale Step 2b evidence — re-run `check-task.sh` + `task_gate.py`.
5. No new multi-container/UI; no templated/re-skin tasks.
6. Submission zip excludes internal artifacts and AI scaffolding (`AGENTS.md`, `.cursor/`, `.claude/`, …) — full ban list in `REPO_CONVENTIONS.md`.

## Route to detail

| Need | File |
|---|---|
| Commands + full gate chain (Step 2a→4) | `commands.md`, `workflow-prompts.md` |
| Dockerfile rules + canonical base images | `docs/PLATFORM_AUTO_EVAL.md`, `docs/DOCKER_REQUIREMENTS.md` |
| Diversity (7 cat, 9 lang, `minimal` blocked, milestones) | `docs/PORTAL_ACCEPTANCE_GUIDE.md`, `docs/EDITION2_SUBMISSION_GUIDE.md` |
| Step 1 seed uniqueness | `scripts/seed_uniqueness_check.py`, `.cursor/rules/idea-validation.mdc` |
| Rubrics (`# Rubric N`, UI-only, ±N) | `TASK_PROPOSAL_RUBRIC.md` |
| Authoring + review policy | `.cursor/rules/`, `docs/HARD_BUT_FAIR_AUTHORING.md`, `docs/REVIEW_CHECKLIST.md` |
| Portal / auto-eval / audit log | `docs/PORTAL_ACCEPTANCE_GUIDE.md`, `docs/REPOSITORY_AUDIT_REPORT.md` |
