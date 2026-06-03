# Terminal-Bench 3.0 Edition 2 — Standalone Task Creation Guide

Use this file as the canonical authoring reference inside the standalone `web` bundle.

- If any older note or example conflicts with this guide, follow this guide.
- This guide is synced to the current active authoring rules.
- If the active rules are silent or ambiguous on a point, prefer the stricter interpretation already stated elsewhere in this bundle. If the bundle still does not resolve it, flag the ambiguity instead of inventing a new rule.
- The default Edition 2 authoring and review profile in this bundle is hard-only. Draft `difficulty = "hard"`, and if a candidate later looks empirically `medium`, regenerate or stop rather than carrying it forward.

## Intake Rules

### Required inputs

1. **Task idea**
   What should the task accomplish? What problem should the agent solve?

2. **Programming language(s)**
   Use the primary implementation languages the task actually needs.

3. **Difficulty**
   The default Edition 2 path in this bundle pursues `hard` only, and the final label must still be supported empirically.

4. **Category**
   Allowed values:
   - `system-administration`
   - `build-and-dependency-management`
   - `data-processing`
   - `games`
   - `software-engineering`
   - `machine-learning`
   - `debugging`
   - `security`
   - `scientific-computing`

5. **Task name**
   A short kebab-case directory name such as `distributed-trace-analysis`.

### Optional inputs

- `subcategories`
  Use only the recognized Edition 2 values:
  - `api_integration`
  - `db_interaction`
  - `long_context`
  - `tool_specific`
  - `ui_building`

- `number_of_milestones`
  Use `0` for non-milestone tasks. Use milestone structure only when it is genuinely needed.

### Fixed values for this standalone bundle

- `author_name = "anonymous"`
- `author_email = "anonymous"`
- `version = "2.0"`
- drafting default: `difficulty = "hard"`

Treat the `hard` default during ideation as provisional until benchmarked. If later evidence says the task is `medium`, send it back to regeneration or stop instead of downgrading and continuing.

## Current Acceptance Gates

Apply these gates while shaping the task:

- `minimal` codebase size is blocked on the platform and treated as a blocking failure in this repo. The environment must have 20+ files (excluding Dockerfile/docker-compose) for `small` (20-200), or 200+ for `large`
- `easy` and `medium` are blocked for this bundle; accepted tasks should end up `hard`
- Python tasks are accepted only when the empirical difficulty is `hard`
- during ideation, avoid Python unless there is a compelling reason to choose it
- prefer single-container tasks; multi-container should be rare and justified
- avoid FastAPI during ideation unless there is a compelling reason to choose it
- `api_integration` tasks must mock the API locally in Docker with no external web dependency
- `long_context` tasks must require at least 50k tokens of reading, roughly 50-150 pages, and semantic reasoning; do not fake this with simple parsing or keyword search (see "Subcategory Guardrails" below for the full corpus standard)

## No-Collapse Principle

The biggest authoring failure mode is not a weak idea. It is a **strong idea family collapsing into a weak concrete instance**.

Do not judge the task only at the idea stage. Judge it again after the implementation plan becomes concrete.

This bundle explicitly rejects tasks that collapse into:

- disclosed policy-knob transcription
- finite state-table or phase-table repair
- toy SSH / SFTP / jail / permissions hardening checklists
- pre-factored recipe completion such as safe extractors or path-sanitization helpers
- spec-complete "fix broken code" where the instruction gives every algorithm, threshold, schema, and formula — making the job a spec-to-code diff regardless of output complexity

Real systems, real daemons, security flavor, and complex output (many JSON fields, many tests, multi-stage pipelines) do not rescue those patterns. Complex output that fans out from a few simple fixes is not hardness.

## Concrete Drafting Rule

When shaping the idea, ask:

- what is the smallest plausible successful patch?
- how many obvious files or helpers are in the editable frontier?
- does the prompt map 1:1 onto those files?
- is the solver mostly filling in a standard recipe or declarative table?
- would a strong model likely solve the task in one pass without much verifier-guided search?
- **what specific facts must the agent discover from the codebase that are NOT in the instruction?** List at least 3. If you cannot, the task is easy.
- **would the instruction need to give exact values, schemas, or formulas for the verifier to work?** If yes, the agent will just diff the spec against the code — that is always easy.

If the answers point toward an easy concrete instance, regenerate or stop before drafting.

## Recommended Workflow

1. Run the mandatory pre-Phase-0 idea search from `chatgpt-task-authoring-playbook.md`.
2. Screen the strongest survivor with `TASK_PROPOSAL_RUBRIC.md`.
3. Run the mandatory implementation-collapse audit before committing to an implementation plan.
4. Use `chatgpt-task-authoring-playbook.md` for intake and proposal shaping. Task drafting happens in Cursor, not ChatGPT.

## Subcategory Guardrails

- `long_context` is only appropriate when the task truly depends on at least 50k tokens of reading, roughly 50-150 pages, and semantic reasoning. If simple parsing, filtering, or keyword search is enough, do not label it `long_context`. The full corpus standard (authoritative version in `task-creation.mdc` "Long-context corpus requirements"):
  - At least 50k tokens of *document-like* content (markdown/txt/PDF/docx/HTML/notebooks/chat logs/emails/papers/docs/narrative logs), measured after excluding code, config, and structured data.
  - The corpus is shipped with the task, not generated by a setup script; it is authoritative to the solution and the agent must read it to solve correctly.
  - Not solvable by grep/keyword search/field extraction/top-k. Not primarily JSON/JSONL/CSV/TSV/database dumps or uniform logs. Not filler, boilerplate, or many tiny files padded to size.
  - The verifier asserts values that depend on details in the documents; multi-document tasks require cross-document reconciliation; the instruction says where the documents live without leaking the answer path.
- `api_integration` is only appropriate when the API is mocked locally in Docker with no external web access. If the task depends on a live remote API, do not label it `api_integration`.
- `ui_building` is only appropriate for genuine UI tasks that use the UI verifier stack rather than ordinary pytest-only backend validation.

## Dockerfile & image rules

Condensed from the canonical Dockerfile rules; the authoritative version is `task-creation.mdc` "environment/Dockerfile". Most are reviewer-verified (no static check yet).

- Install `tmux` and `asciinema` (sanctioned base image or pinned install) — the agent session needs both; missing either fails every run.
- Pin every `FROM` by digest; prefer a sanctioned base image for the runtime class.
- Reproducible builds: pin deps with lockfiles, checksum-verify downloaded binaries (no `curl | sh`), set `SOURCE_DATE_EPOCH`, build with BuildKit.
- Order layers least→most volatile (manifests before source); no `COPY . .`; ship a `.dockerignore` for non-trivial tasks.
- One apt transaction with `--no-install-recommends`, no `apt-get upgrade`, `rm -rf /var/lib/apt/lists/*`, pinned versions; use multi-stage builds to keep build tools out of the runtime image.
- Store source as files (no Dockerfile heredocs); set permissions with `COPY --chmod`/`--chown`; keep `.git`/`.env`/credentials/caches out.
- Never copy `solution/`/`tests/`/answers into the image; all downloads happen at build time; the runtime is offline (`allow_internet = false`).
- Declare `[environment]` resources (`cpus`, `memory_mb`, `storage_mb`, `build_timeout_sec`, `gpus`, `gpu_types`, `docker_flags`) from real peak usage; add OpenContainers image labels.

## Difficulty Evaluation

Final difficulty uses the May 2026 ordering: classify **Hard → Medium → Easy** and stop at the first matching band.

- `hard` if the best model passes at most 20%; if that does not apply, also `hard` if the worst model passes at most 20%
- `medium` if `20% < worst-model accuracy <= 60%`
- `easy` if `60% < worst-model accuracy <= 80%` and is blocked for this repo's hard-only path
- if frontier models pass 100%, the task is too trivial
- if frontier models succeed at a high rate, solve extremely quickly, or repeatedly solve the task by opening only the obvious files first, treat that as strong evidence the concrete draft collapsed
- for this bundle, only the `hard` band is acceptable

The standalone bundle may still draft ideas as `hard` by default during ideation. That default is not a substitute for real benchmarking.
