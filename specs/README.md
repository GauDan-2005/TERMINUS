# Specs Working Notes

The `specs/` folder is a working directory for Step 2 validation artifacts. Files here are reviewed during authoring and are not part of the submitted task package.

## Split spec contract

Each saved Step 2 spec in `specs/<task-name>.md` should contain two distinct sections:

1. `Authoring Brief`
2. `Reviewer Appendix`

The split is intentional:

- `Authoring Brief` is the only section Step 2b should use when drafting task files.
- `Reviewer Appendix` is for human review only. It may include frontier analysis, exhaustive file inventory ideas, oracle notes, and collapse-audit detail that would over-shape drafting if fed back into Step 2b.

## What belongs in each section

`Authoring Brief` should describe:

- The public contract the eventual `instruction.md` and tests must enforce
- The failure topology: symptom clusters, invariants, and interacting subsystems that make the task hard
- The environment shape at a component level, not an exhaustive file-by-file scaffold
- Required artifacts and test intent

`Reviewer Appendix` may describe:

- The implementation plan in more concrete terms
- A proposed exhaustive file tree or component inventory
- Oracle notes
- Collapse-audit analysis and per-test feasibility review

## v2 spec sections (mandatory under `Authoring Brief`)

A v2 spec — one with `version: 2` in its metadata block — must contain three
additional sub-sections under `## Authoring Brief`, each with at least one
bullet. Specs without `version: 2` are treated as v1 and pass silently
(grandfathering for in-flight specs at rollout time).

1. **Triviality avoidance ledger** — for each test in the test plan, list at
   least one specific pattern that would make the test trivial *and* state
   how the design prevents that pattern. The point is to commit to a position
   on triviality risk *before* drafting code.
2. **Per-gate pitfall inventory** — for each Step 2b gate (`run_static_checks.py`,
   `collapse_check.py`, `oracle 10x`, `NOP`), name the closest failure mode
   this design is at risk of and how the design stays clean. One bullet per
   gate is enough; the inventory is a paper commitment, not a tutorial.
3. **Initial draft commitments** — flat list of files the author commits to
   creating, one sentence each with rationale. Files added later that aren't
   in this list flag the spec as "evolved" and require an entry in
   `<task-name>-validation-log.md`.

The shape of each sub-section is described in
`tb3-repo-agent-harness_plan-v2.1.md` §§ 3a / 3b / 3c with worked examples;
the spec linter does not pin the example wording, only that the sub-section
exists with at least one bullet.

## `lint_spec.py` gate

`validate_loop.py select` calls `lint_spec.run(spec_path)` on the picked spec
before promoting it to `specs/<task>.md`. The lint reports per-section
failures with actionable messages — naming which sub-section is missing and
where it expected to find it (under `## Authoring Brief`). A common mistake
is putting one of the three sub-sections under `## Reviewer Appendix`
instead; `lint_spec.py` gives that case a specific failure message rather
than a generic "missing section" so the fix is obvious.

Run the lint directly to debug a spec before re-running `validate_loop.py`:

```bash
python3 lint_spec.py specs/<task-name>.md
# exit 0 = pass, 1 = fail with per-section messages, 2 = bad usage
```

v1 specs do not need any change. New tasks default to v2.

## Other generated files

The validation loop may also create:

- `specs/<task-name>-candidate-N.md` for plateau candidates
- `specs/<task-name>-attempt-N-evidence.json` for structured evidence
- `specs/<task-name>-validation-log.md` for attempt history

These are reviewer artifacts. They are not drafting inputs for Step 2b.
