# Progress: doc+gate sync to Snorkel reviews (resume notes)

Plan file: /home/gaurav-s-ubuntu/.claude/plans/do-deep-checking-of-elegant-seal.md
Authority model: Snorkel reviews in personal_docs/feedback/ = source of truth (READ-ONLY, never edit).
Real test runner: `python3 -m repo_tests` (unittest; system python has NO pytest).
Pre-existing baseline failure (NOT ours, leave alone): test_doc_size_caps — AGENTS.md 1959B > 1500B cap.

## DONE (Phase B partial — gate code)
- run_static_checks.py: added OFFLINE_INSTALL_PATTERN (pip/uv-pip install + --no-index),
  PACKAGE_INSTALL_LINE_PATTERN, OFFLINE_SETUP_LINE_PATTERNS, offline_prefix_mismatches().
  - first_verifier_command_index() now skips package-install lines (so `pip install ... pytest==x`
    is not mistaken for the verifier command).
  - check_test_sh offline branch (~line 1620): FAILs a line only if NETWORK_INSTALL_PATTERN matches
    AND NOT OFFLINE_INSTALL_PATTERN. venv create/activate treated offline-safe.
  - Verified by inline 7/7 control matrix: offline findlinks/venv/deps-in-dockerfile PASS;
    bare pip / uvx / apt / curl|sh FAIL.
  - Live gate now: tasks/sparse-block-preconditioner exit 0; adaptive exit 0;
    quantized only remaining FAIL = unpinned apt (a TASK fix, Phase C — NOT a gate bug).
- repo_tests/test_run_static_checks.py: added class OfflineSelfContainedTestShTest (6 tests)
  pinning the offline/networked boundary. Ran the static-checks module = all passing (dots).

## VERIFIED STATE (authoritative, via in-process JSON — display parsing was corrupting this session)
- repo_tests: 227 tests, 1 failure = test_doc_size_caps (AGENTS.md 1959>1500, PRE-EXISTING, not ours). feedback/ untouched (git porcelain = 0).
- In-process gate (run_checks) on live tasks:
  - sparse-block-preconditioner: 0 failures (offline test.sh PASSES now)
  - quantized-beam-alignment: 1 failure = apt-pin only (TASK fix, Phase C; offline test.sh PASSES)
  - adaptive-mesh-conservation: 0 failures
- DONE subtasks: B1/B2 (gate offline exemption), B4 (OfflineSelfContainedTestShTest 6 tests),
  A4 (RC1-RC7 -> RC1-RC8+CR1,CR2,CR7-CR9+GX1-GX10 across commands.md, workflow-prompts.md×8,
  review-and-submit.mdc×3, difficulty-calibration.mdc:457, idea-validation.mdc:241,
  task-creation.mdc:17/28/44/46 headings, tb3-task-author SKILL.md:42, web playbook:501;
  task-creation.mdc:26 & :46 left as legit RC1-RC7 scoped descriptions),
  A1 (authority reframe in CLAUDE.md + REPO_CONVENTIONS.md), A3 (issues_fixes.md:19 retracted,
  docker.md Good block pinned + gate note).

## ALL PHASE A + B COMPLETE (verified 233 tests / 1 pre-existing AGENTS fail)
- A2 DONE: offline-wheels self-contained test.sh blessed across task-creation.mdc (deps line +
  full "Offline-wheels self-contained test.sh" subsection with Dockerfile+test.sh examples),
  review-and-submit.mdc (7 lines reframed to "no NETWORKED install; offline --no-index allowed"),
  REPO_CONVENTIONS.md (two-pattern rewrite), workflow-prompts.md (anchor note at L126 + 6 lines),
  Default_Task_Skeleton/tests/test.sh (pointer comment). Networked installs still FAIL.
- A5 DONE: drift sweep → 0 remaining absolute "test.sh must not install" phrasings in editable docs.
- Final gate: sparse PASS, adaptive PASS, quantized = apt-pin FAIL only (Phase C task fix).
  feedback/ untouched. AGENTS.md not grown (1959B). All .py compile.
- Phase B fixtures (task #5) = OPTIONAL belt-and-suspenders; behavior already covered by
  OfflineSelfContainedTestShTest. Skipped unless user wants fixture-level coverage too.

## TOOLING CAVEAT (important for resume)
Bash/Read DISPLAY output is intermittently corrupting this session (injected "wait"/meta lines,
duplicated/dropped lines, mangled words like "FodSizeCaps"). Edits are SAFE (Edit errors on bad
old_string), but VERIFY via: `python3 -c`/heredoc that prints JSON or compact booleans, never by
eyeballing grep/sed/cat dumps. Triple-confirm any old_string across >=2 independent reads before Edit.

## TODO (resume here)
- A2 NOT STARTED (the big one). The canonical tests/test.sh template block in task-creation.mdc
  (## tests/test.sh section) could NOT be read cleanly due to corruption — read it via python repr
  and verify before editing. Pivot the policy from "test.sh must not install anything" to
  "offline-wheels self-contained is the recommended pattern; deps-in-Dockerfile tolerated; networked
  installs forbidden." task-creation.mdc:574 is triple-confirmed and safe to edit.
- B3 fixtures = optional belt-and-suspenders (behavior already covered by B4 test class).
1. CONFIRM full suite: `python3 -m repo_tests 2>&1 | tail -5` → expect "Ran 22x tests ... FAILED (failures=1)"
   where the ONLY failure is test_doc_size_caps (AGENTS.md). If any other fails, investigate.
2. Task #5 (B3): re-aim fixtures — keep >=1 fixture modeling offline-wheels test.sh
   (pip install --no-index --find-links). The in-progress refactor rewrote all fixtures to
   deps-in-Dockerfile; pick one (e.g. release-provenance-drift) to use offline wheels so that
   path has fixture coverage. Update its tests/test.sh + Dockerfile (pip download wheels) +
   cases.py STATIC_CHECK_EXPECTATIONS warnings if they change. (Lower priority — the new
   OfflineSelfContainedTestShTest already covers the behavior; fixture is belt-and-suspenders.)
3. Phase A docs (tasks #7-#10): see plan. Key files:
   - A2 test.sh policy → offline-wheels self-contained standard: .cursor/rules/task-creation.mdc
     (tests/test.sh ~574,711-750,914), review-and-submit.mdc (~51,74,78,297,310,329),
     REPO_CONVENTIONS.md (~127-146), workflow-prompts.md (~334,367,629,673),
     personal_docs/references_announcement/Default_Task_Skeleton/tests/test.sh, skill mirrors.
   - A1 authority reframe: CLAUDE.md "Source of truth" (lines 5-18) + REPO_CONVENTIONS.md one-liner.
     DO NOT grow AGENTS.md (over byte cap).
   - A3 apt pinning (user said correct directly): issues_fixes.md:19 ("do not pin dependency
     versions" → require pins); docker.md unpinned apt-get install examples → pin them.
   - A4 RC1-RC7 → RC1-RC8 + CR1,CR2,CR7-CR9 + GX1-GX10 (all FAIL-blocking; collapse_check.py:3330
     ALL_CHECKS=[...]+_GX_CHECKS): commands.md:44,130; workflow-prompts.md:54,330,338,465,630,679,832,910;
     review-and-submit.mdc:123,280,291; difficulty-calibration.mdc:457; idea-validation.mdc:241;
     .cursor/skills/tb3-task-author/SKILL.md:42; web/chatgpt-task-authoring-playbook.md:501.
4. A5 + verification (task #11): drift sweep; then `python3 -m repo_tests` green-except-AGENTS;
   run_static_checks on the 3 live tasks; `git status --porcelain personal_docs/feedback` empty;
   re-grep RC1-RC7/CR1-CR7 gone; AGENTS.md bytes not increased.
5. Difficulty calibration = SKIP (user decision). 
6. Phase C = task work, AFTER user names the task.

## Gotchas observed
- Parallel/edit-heavy bash batches produced garbled/duplicated tool output this session; prefer
  SMALL sequential bash calls and verify via `python3 -c`/`ast.parse` rather than sed/grep dumps.
- Do not trust "grep -c" duplicate-count readings that looked anomalous; AST + import-count via
  python were the reliable signal (test_run_static_checks.py: 1 import stmt, valid Python).
