from __future__ import annotations

import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path

import run_static_checks
from repo_tests.cases import COMMON_STATIC_PASS_MESSAGES, FIXTURE_TASKS_DIR, STATIC_CHECK_EXPECTATIONS

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "run_static_checks"


class RunStaticChecksRegressionTest(unittest.TestCase):
    """Pin repo-level static checker results for the checked-in benchmark fixtures."""

    def copy_fixture(self, fixture_name: str, tmpdir: str) -> Path:
        fixture_dir = FIXTURES_DIR / fixture_name
        task_dir = Path(tmpdir) / fixture_name
        shutil.copytree(fixture_dir, task_dir)
        return task_dir

    def test_fixture_tasks_keep_pinned_static_check_results(self) -> None:
        for task_name, expected in STATIC_CHECK_EXPECTATIONS.items():
            with self.subTest(task=task_name):
                reporter = run_static_checks.run_checks(FIXTURE_TASKS_DIR / task_name)
                self.assertEqual(reporter.failures, [])
                self.assertEqual(reporter.warnings, expected["warnings"])
                for message in COMMON_STATIC_PASS_MESSAGES:
                    self.assertIn(message, reporter.passes)

    def test_cli_exit_code_stays_successful_for_fixture_tasks(self) -> None:
        for task_name in STATIC_CHECK_EXPECTATIONS:
            with self.subTest(task=task_name):
                stdout = io.StringIO()
                with contextlib.redirect_stdout(stdout):
                    exit_code = run_static_checks.main(
                        ["--task-dir", str(FIXTURE_TASKS_DIR / task_name), "--version", "edition_2"]
                    )
                self.assertEqual(exit_code, 0)
                self.assertIn("PASS", stdout.getvalue())

    def test_legacy_rc_reward_footer_is_rejected(self) -> None:
        fixture = FIXTURE_TASKS_DIR / "implicit-step-restart"
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = Path(tmpdir) / fixture.name
            shutil.copytree(fixture, task_dir)

            test_sh = task_dir / "tests" / "test.sh"
            test_sh.write_text(
                """#!/bin/bash

mkdir -p /logs/verifier

if [ "$PWD" = "/" ]; then
  echo "Error: No working directory set. Please set a WORKDIR in your Dockerfile before running this script."
  exit 1
fi

python -m pytest -o cache_dir=/tmp/pytest_cache --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA
RC=$?

if [ "$RC" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi

exit "$RC"
""",
                encoding="utf-8",
            )

            reporter = run_static_checks.run_checks(task_dir)

        self.assertTrue(
            any("legacy RC=$?" in failure for failure in reporter.failures),
            reporter.failures,
        )

    def test_reward_json_footer_is_rejected(self) -> None:
        fixture = FIXTURE_TASKS_DIR / "implicit-step-restart"
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = Path(tmpdir) / fixture.name
            shutil.copytree(fixture, task_dir)

            test_sh = task_dir / "tests" / "test.sh"
            content = test_sh.read_text(encoding="utf-8")
            test_sh.write_text(
                content.replace("/logs/verifier/reward.txt", "/logs/verifier/reward.json"),
                encoding="utf-8",
            )

            reporter = run_static_checks.run_checks(task_dir)

        self.assertIn(
            "tests/test.sh must emit /logs/verifier/reward.txt; reward.json is not supported by the Edition 2 template",
            reporter.failures,
        )

    def test_internal_harness_path_leak_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = self.copy_fixture("public-contract-standard", tmpdir)
            instruction_path = task_dir / "instruction.md"
            instruction_path.write_text(
                instruction_path.read_text(encoding="utf-8")
                + "\nDo not touch `/app/.state/private-cache.bin` while preparing the output.\n",
                encoding="utf-8",
            )

            reporter = run_static_checks.run_checks(task_dir, {"output_contract"})

        self.assertIn(
            "instruction.md must not mention internal_harness_files unless they are also declared in user_visible_outputs: /app/.state/private-cache.bin",
            reporter.failures,
        )

    def test_internal_harness_path_is_allowed_when_it_is_also_user_visible(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = self.copy_fixture("public-contract-standard", tmpdir)
            contract_path = task_dir / "output_contract.toml"
            contract_path.write_text(
                contract_path.read_text(encoding="utf-8").replace(
                    'internal_harness_files = [\n  "/app/.state/private-cache.bin",\n]',
                    'internal_harness_files = [\n  "/app/out/report.json",\n]',
                ),
                encoding="utf-8",
            )

            reporter = run_static_checks.run_checks(task_dir, {"output_contract"})

        self.assertEqual(reporter.failures, [])
        self.assertIn("output contract matches the declared user-visible outputs and schema checks", reporter.passes)

    def test_milestone_instruction_requires_signal_completion_directive(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = self.copy_fixture("public-contract-milestone", tmpdir)
            instruction_path = task_dir / "steps" / "milestone_1" / "instruction.md"
            instruction_path.write_text(
                "For the current step, write `/app/out/report.json` as JSON with `checksum` and `status` fields.\n",
                encoding="utf-8",
            )

            reporter = run_static_checks.run_checks(task_dir, {"instruction"})

        self.assertIn(
            "steps/milestone_1/instruction.md: Milestone tasks must tell the agent to signal completion before advancing to the next milestone",
            reporter.failures,
        )

    def test_milestone_instruction_passes_with_signal_completion_directive(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = self.copy_fixture("public-contract-milestone", tmpdir)

            reporter = run_static_checks.run_checks(task_dir, {"instruction"})

        self.assertEqual(reporter.failures, [])

    def test_milestone_word_in_instruction_emits_nonblocking_warning(self) -> None:
        """Mirror of the upstream instruction-eval rule: when the literal word
        'milestone' (or 'milestones') appears in instruction.md, surface a
        non-blocking warning so authors can rephrase before submit. The check
        must not promote to a failure — the upstream eval is non-blocking and
        the static checker has to stay aligned."""
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = self.copy_fixture("public-contract-milestone", tmpdir)

            reporter = run_static_checks.run_checks(task_dir, {"instruction"})

        self.assertEqual(reporter.failures, [])
        milestone_warnings = [
            warning for warning in reporter.warnings
            if "instruction.md contains the word 'milestone'" in warning
        ]
        self.assertEqual(len(milestone_warnings), 1, reporter.warnings)
        self.assertIn("2 occurrence(s)", milestone_warnings[0])
        self.assertIn("non-blocking", milestone_warnings[0])

    def test_milestone_word_warning_is_silent_when_instruction_uses_neutral_wording(self) -> None:
        """Authors who follow the upstream guidance and rephrase 'milestone' as
        'step' (or similar neutral wording) should not see the warning. The
        underlying milestone task still has number_of_milestones = 2 in
        task.toml; the static check must look at the prose only, not the
        metadata."""
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = self.copy_fixture("public-contract-milestone", tmpdir)
            for instruction_path in sorted((task_dir / "steps").glob("milestone_*/instruction.md")):
                instruction_path.write_text(
                    "For the current step, write `/app/out/report.json` as JSON with `checksum` and "
                    "`status` fields. Signal completion before you advance to the next step.\n",
                    encoding="utf-8",
                )

            reporter = run_static_checks.run_checks(task_dir, {"instruction"})

        self.assertEqual(reporter.failures, [])
        milestone_warnings = [
            warning for warning in reporter.warnings
            if "instruction.md contains the word 'milestone'" in warning
        ]
        self.assertEqual(milestone_warnings, [])

    def test_milestone_word_warning_ignores_underscored_identifiers(self) -> None:
        """Identifiers like `milestone_count` (e.g. mentioned inside backticks
        as a metadata field name) must not trigger the warning — the underscore
        prevents `\\b` from matching, and the rule targets prose usage of the
        word, not field-name references."""
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = self.copy_fixture("public-contract-milestone", tmpdir)
            instruction_path = task_dir / "steps" / "milestone_1" / "instruction.md"
            instruction_path.write_text(
                "Write `/app/out/report.json` as JSON with `checksum` and `status` fields. "
                "The `milestone_count` field in `task.toml` is metadata, not user-facing. "
                "Signal completion before you advance to the next step.\n",
                encoding="utf-8",
            )

            reporter = run_static_checks.run_checks(task_dir, {"instruction"})

        self.assertEqual(reporter.failures, [])
        milestone_warnings = [
            warning for warning in reporter.warnings
            if "instruction.md contains the word 'milestone'" in warning
        ]
        self.assertEqual(milestone_warnings, [])

    def test_oracle_knob_discoverability_warns_when_flag_is_invisible(self) -> None:
        """A knob referenced by solve.sh but absent from instruction.md
        AND absent from every comment/doc under environment/ must warn.

        Reproduces the rollback-replay-divergence failure mode: the oracle
        flips two CMake cache variables the agent cannot discover, so agents
        rewrite the source and lose the conditional-compilation ladder the
        grader depends on."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = FIXTURE_TASKS_DIR / "rollback-replay-divergence"
            task_dir = Path(tmpdir) / "rollback-replay-divergence"
            shutil.copytree(source, task_dir)

            instruction = task_dir / "instruction.md"
            instruction.write_text(
                instruction.read_text(encoding="utf-8")
                .replace("`TB_TIMELINE_MODE`", "the timeline knob")
                .replace("`TB_REEXEC_MODE`", "the re-exec knob"),
                encoding="utf-8",
            )
            cmake = task_dir / "environment" / "CMakeLists.txt"
            lines = cmake.read_text(encoding="utf-8").splitlines(keepends=True)
            cmake.write_text(
                "".join(
                    line for line in lines
                    if not line.lstrip().startswith("#")
                ),
                encoding="utf-8",
            )

            reporter = run_static_checks.run_checks(
                task_dir, {"oracle_knob_discoverability"}
            )

        warnings = [w for w in reporter.warnings if "build knobs" in w]
        self.assertEqual(len(warnings), 1, reporter.warnings)
        self.assertIn("TB_TIMELINE_MODE", warnings[0])
        self.assertIn("TB_REEXEC_MODE", warnings[0])

    def test_oracle_knob_discoverability_passes_when_flag_is_named_in_instruction(self) -> None:
        """Mentioning the knob in instruction.md alone clears the check even if
        the environment/ sources have no comment for it."""
        reporter = run_static_checks.run_checks(
            FIXTURE_TASKS_DIR / "rollback-replay-divergence",
            {"oracle_knob_discoverability"},
        )
        self.assertEqual(reporter.failures, [])
        self.assertIn(
            "build knobs required by solve.sh and tests are discoverable from instruction.md or environment/",
            reporter.passes,
        )

    def test_oracle_knob_discoverability_ignores_standard_cmake_knobs(self) -> None:
        """Standard CMake / compiler knobs (CMAKE_BUILD_TYPE, CC, CFLAGS, ...)
        must never trigger the check, even if they never appear in
        instruction.md. Tasks that only use standard knobs report a clean
        'no bespoke build knobs required' pass."""
        reporter = run_static_checks.run_checks(
            FIXTURE_TASKS_DIR / "byzantine-storage-rebalance",
            {"oracle_knob_discoverability"},
        )
        self.assertEqual(reporter.failures, [])
        self.assertEqual([], [w for w in reporter.warnings if "build knobs" in w])

    def test_oracle_path_discoverability_warns_when_install_path_is_invisible(self) -> None:
        """Reproduces the rollback-replay-divergence v4 failure mode: agents
        built the binary, ran it, produced the correct SIGNOFF digests, and
        still failed every test because nothing told them to install the
        binary at /app/bin/netplay_matrix. The check must catch this by
        warning that the test-required path is undocumented."""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = FIXTURE_TASKS_DIR / "rollback-replay-divergence"
            task_dir = Path(tmpdir) / "rollback-replay-divergence"
            shutil.copytree(source, task_dir)

            instruction = task_dir / "instruction.md"
            instruction.write_text(
                instruction.read_text(encoding="utf-8")
                .replace("install it at `/app/bin/netplay_matrix`", "install the binary")
                .replace("`/app/bin/netplay_matrix`", "the binary")
                .replace("netplay_matrix", "the matrix driver"),
                encoding="utf-8",
            )
            shipped_binary = task_dir / "environment" / "bin" / "netplay_matrix"
            if shipped_binary.exists():
                shipped_binary.unlink()

            reporter = run_static_checks.run_checks(
                task_dir, {"oracle_path_discoverability"}
            )

        warnings = [w for w in reporter.warnings if "agent must create" in w]
        self.assertEqual(len(warnings), 1, reporter.warnings)
        self.assertIn("/app/bin/netplay_matrix", warnings[0])

    def test_oracle_path_discoverability_passes_when_path_is_named_in_instruction(self) -> None:
        """Positive case on the patched fixture: every absolute /app path the
        tests resolve is either in the shipped tree, under a standard build-
        output prefix, or named in instruction.md / environment/."""
        reporter = run_static_checks.run_checks(
            FIXTURE_TASKS_DIR / "rollback-replay-divergence",
            {"oracle_path_discoverability"},
        )
        self.assertEqual(reporter.failures, [])
        self.assertIn(
            "agent-target paths declared in tests/ are discoverable from instruction.md or environment/",
            reporter.passes,
        )

    def test_oracle_path_discoverability_accepts_string_literals_in_source(self) -> None:
        """Paths mentioned only as quoted string literals in source files
        (e.g. ``const DefaultPath = \"/app/config/foo.yaml\"`` in Go,
        ``std::string work_dir = \"/app/work\"`` in C++) are discoverable —
        the agent can grep for them. This distinguishes paths from build
        knobs, where bare-code references don't count.

        Specifically: byzantine-storage-rebalance documents
        /app/config/sim_defaults.yaml only via a Go string-literal
        constant; the check must not warn on it."""
        reporter = run_static_checks.run_checks(
            FIXTURE_TASKS_DIR / "byzantine-storage-rebalance",
            {"oracle_path_discoverability"},
        )
        self.assertEqual(reporter.failures, [])
        self.assertEqual([], [w for w in reporter.warnings if "agent must create" in w])

    def test_oracle_path_discoverability_skips_standard_build_output_dirs(self) -> None:
        """Paths under /app/build/ (cmake), /app/target/ (cargo), /app/dist/
        and similar standard build-tool output directories are managed by
        the agent's toolchain and don't need to be documented in
        instruction.md."""
        reporter = run_static_checks.run_checks(
            FIXTURE_TASKS_DIR / "release-provenance-drift",
            {"oracle_path_discoverability"},
        )
        self.assertEqual(reporter.failures, [])
        warnings_with_build_dirs = [
            w for w in reporter.warnings
            if "/app/build/" in w or "/app/target/" in w
        ]
        self.assertEqual(warnings_with_build_dirs, [])

    def test_instruction_test_vocabulary_catches_extended_assertion_shapes(self) -> None:
        """The vocabulary check must catch all four assertion shapes:
        ``X == LITERAL``, ``X.startswith(LITERAL)``, ``LITERAL in X``,
        and ``len(X) == NUMBER`` — for any X reading an instruction-named
        field. Reproduces the release-provenance-drift gap where
        ``len(snapshot["epoch"]) == 24`` was tested but never documented."""
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = Path(tmpdir) / "vocab_test"
            task_dir.mkdir()
            (task_dir / "instruction.md").write_text(
                "Output a `result` field. The status field is also part of the contract.\n"
            )
            tests = task_dir / "tests"
            tests.mkdir()
            (tests / "test_outputs.py").write_text(
                "def test_a():\n"
                "    obj = {}\n"
                "    assert obj['result'] == 'undocumented_value'\n"
                "    assert obj['result'].startswith('undocumented_prefix')\n"
                "    assert obj['result'].endswith('undocumented_suffix')\n"
                "    assert 'undocumented_substring' in obj['result']\n"
                "    assert len(obj['result']) == 42\n"
            )

            named_fields = run_static_checks._instruction_named_fields(
                (task_dir / "instruction.md").read_text(encoding="utf-8")
            )
            findings = run_static_checks._literal_assertions_on_named_fields(
                tests / "test_outputs.py", named_fields
            )

        literals_found = {literal for _, _, literal in findings}
        self.assertIn("undocumented_value", literals_found)         # ==
        self.assertIn("undocumented_prefix", literals_found)        # startswith
        self.assertIn("undocumented_suffix", literals_found)        # endswith
        self.assertIn("undocumented_substring", literals_found)     # in
        self.assertIn("42", literals_found)                         # len ==

    def test_instruction_test_vocabulary_passes_when_extended_literals_are_documented(self) -> None:
        """Counterpart to the negative test: when each literal IS named in
        instruction.md, no warning fires across all four assertion shapes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = Path(tmpdir) / "vocab_pass"
            task_dir.mkdir()
            (task_dir / "instruction.md").write_text(
                "The `result` field equals 'documented_value', begins with "
                "'documented_prefix', ends with 'documented_suffix', contains "
                "the substring 'documented_substring', and has length 42.\n"
            )
            tests = task_dir / "tests"
            tests.mkdir()
            (tests / "test_outputs.py").write_text(
                "def test_a():\n"
                "    obj = {}\n"
                "    assert obj['result'] == 'documented_value'\n"
                "    assert obj['result'].startswith('documented_prefix')\n"
                "    assert obj['result'].endswith('documented_suffix')\n"
                "    assert 'documented_substring' in obj['result']\n"
                "    assert len(obj['result']) == 42\n"
            )

            named_fields = run_static_checks._instruction_named_fields(
                (task_dir / "instruction.md").read_text(encoding="utf-8")
            )
            findings = run_static_checks._literal_assertions_on_named_fields(
                tests / "test_outputs.py", named_fields
            )
            instruction_text = (task_dir / "instruction.md").read_text(encoding="utf-8")
            undocumented = [
                (field, literal) for _, field, literal in findings
                if literal not in instruction_text
            ]

        self.assertEqual(undocumented, [])

    def test_timeout_coherence_warns_when_subprocess_timeouts_exceed_verifier(self) -> None:
        """Reproduces the implicit-step-restart v6 failure mode: tests/
        declare explicit ``subprocess.run(..., timeout=N)`` ceilings on
        each cmake step (180+180+60+120+120+30 = 690s), but the verifier
        budget was 600s. The check must sum those literals and warn when
        the sum exceeds verifier.timeout_sec — that's the real wall-time
        ceiling, not the build-site count."""
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = Path(tmpdir) / "tsum"
            task_dir.mkdir()
            (task_dir / "task.toml").write_text(
                'version = "2.0"\n'
                "[metadata]\n"
                'author_name = "anonymous"\n'
                'author_email = "anonymous"\n'
                'difficulty = "hard"\n'
                'category = "debugging"\n'
                'tags = []\n'
                'languages = ["c++"]\n'
                'codebase_size = "small"\n'
                "number_of_milestones = 0\n"
                "subcategories = []\n"
                "expert_time_estimate_min = 60\n"
                "junior_time_estimate_min = 240\n"
                "[agent]\n"
                "timeout_sec = 1800\n"
                "[verifier]\n"
                "timeout_sec = 600\n"
                "[environment]\n"
                "build_timeout_sec = 600\n"
                "cpus = 2\n"
                "memory_mb = 4096\n"
                "storage_mb = 10240\n"
            )
            tests = task_dir / "tests"
            tests.mkdir()
            # Tests with explicit per-call timeouts summing > verifier
            (tests / "test_outputs.py").write_text(
                "import subprocess\n"
                "def test_x():\n"
                "    subprocess.run(['cmake', '-S', '.', '-B', 'build'], timeout=180)\n"
                "    subprocess.run(['cmake', '--build', 'build'], timeout=180)\n"
                "    subprocess.run(['./bin'], timeout=60)\n"
                "    subprocess.run(['cmake', '-S', 'p', '-B', 'pb'], timeout=120)\n"
                "    subprocess.run(['cmake', '--build', 'pb'], timeout=120)\n"
                "    subprocess.run(['./pb/probe'], timeout=30)\n"
            )

            reporter = run_static_checks.run_checks(task_dir, {"timeout_coherence"})

        sum_warnings = [w for w in reporter.warnings if "exceeds verifier" in w]
        self.assertEqual(len(sum_warnings), 1, reporter.warnings)
        self.assertIn("690s", sum_warnings[0])
        self.assertIn("600s", sum_warnings[0])

    def test_timeout_coherence_passes_when_subprocess_timeout_sum_fits_verifier(self) -> None:
        """Counterpart positive: same six subprocesses, verifier raised to
        900s, the sum (690s) fits under it, and the new rule stays silent."""
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = Path(tmpdir) / "tfit"
            task_dir.mkdir()
            (task_dir / "task.toml").write_text(
                'version = "2.0"\n'
                "[metadata]\n"
                'author_name = "anonymous"\n'
                'author_email = "anonymous"\n'
                'difficulty = "hard"\n'
                'category = "debugging"\n'
                'tags = []\n'
                'languages = ["c++"]\n'
                'codebase_size = "small"\n'
                "number_of_milestones = 0\n"
                "subcategories = []\n"
                "expert_time_estimate_min = 60\n"
                "junior_time_estimate_min = 240\n"
                "[agent]\n"
                "timeout_sec = 1800\n"
                "[verifier]\n"
                "timeout_sec = 900\n"
                "[environment]\n"
                "build_timeout_sec = 600\n"
                "cpus = 2\n"
                "memory_mb = 4096\n"
                "storage_mb = 10240\n"
            )
            tests = task_dir / "tests"
            tests.mkdir()
            (tests / "test_outputs.py").write_text(
                "import subprocess\n"
                "def test_x():\n"
                "    subprocess.run(['cmake', '-S', '.', '-B', 'build'], timeout=180)\n"
                "    subprocess.run(['cmake', '--build', 'build'], timeout=180)\n"
                "    subprocess.run(['./bin'], timeout=60)\n"
                "    subprocess.run(['cmake', '-S', 'p', '-B', 'pb'], timeout=120)\n"
                "    subprocess.run(['cmake', '--build', 'pb'], timeout=120)\n"
                "    subprocess.run(['./pb/probe'], timeout=30)\n"
            )

            reporter = run_static_checks.run_checks(task_dir, {"timeout_coherence"})

        sum_warnings = [w for w in reporter.warnings if "exceeds verifier" in w]
        self.assertEqual(sum_warnings, [])

    def test_environment_hidden_instructions_passes_on_realistic_environment_prose(self) -> None:
        """Realistic environment context — descriptive prose about how the
        system behaves, what the tests consume, what the public API does — must
        not trigger the hidden-instructions check. The shipped fixture
        environments are all in this style and must stay PASS."""
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = self.copy_fixture("public-contract-standard", tmpdir)
            env_dir = task_dir / "environment"
            env_dir.mkdir(exist_ok=True)
            (env_dir / "README.md").write_text(
                "# Widget Service\n\n"
                "The widget service exposes an HTTP API for inspecting "
                "registered widgets. The user-agent header is forwarded to "
                "downstream callers. Diagnostic output is consumed by the "
                "verifier and should remain deterministic.\n",
                encoding="utf-8",
            )
            reporter = run_static_checks.run_checks(task_dir, {"environment_hidden_instructions"})

        self.assertEqual(reporter.failures, [], reporter.failures)
        self.assertIn(
            "environment/ contains no hidden-instruction patterns",
            reporter.passes,
        )

    def test_environment_hidden_instructions_fails_on_solver_directed_phrase(self) -> None:
        """A markdown file inside environment/ that contains explicit
        solver-direction phrasing ('Claude should call ...') must FAIL the
        new check. This is the canonical failure mode the upstream
        instruction-eval is trying to prevent."""
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = self.copy_fixture("public-contract-standard", tmpdir)
            env_dir = task_dir / "environment"
            env_dir.mkdir(exist_ok=True)
            (env_dir / "NOTES.md").write_text(
                "# Implementation notes\n\n"
                "Claude should call `widget.recompute()` after every state "
                "transition; otherwise the cache becomes stale.\n",
                encoding="utf-8",
            )
            reporter = run_static_checks.run_checks(task_dir, {"environment_hidden_instructions"})

        hidden_failures = [
            failure for failure in reporter.failures
            if "hidden-instruction content" in failure
        ]
        self.assertEqual(len(hidden_failures), 1, reporter.failures)
        self.assertIn("environment/NOTES.md", hidden_failures[0])
        self.assertIn("solver-direction phrase", hidden_failures[0])

    def test_environment_hidden_instructions_fails_on_solution_reveal_phrase(self) -> None:
        """'The fix is to ...' / 'to solve this task ...' phrasing inside
        environment/ is a solution-reveal even when no AI brand name is named.
        These need to FAIL because they short-circuit the engineering
        challenge — the agent reads the answer instead of doing the work."""
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = self.copy_fixture("public-contract-standard", tmpdir)
            env_dir = task_dir / "environment"
            env_dir.mkdir(exist_ok=True)
            # Plain Python file: only solver-direction patterns apply, prose
            # patterns (HINT/STEP) don't, but solution-reveal IS a solver-
            # direction pattern and must fire even in source-code comments.
            (env_dir / "core.py").write_text(
                "# The fix is to swap the lock acquisition order in `commit`.\n"
                "def commit():\n"
                "    pass\n",
                encoding="utf-8",
            )
            reporter = run_static_checks.run_checks(task_dir, {"environment_hidden_instructions"})

        hidden_failures = [
            failure for failure in reporter.failures
            if "hidden-instruction content" in failure
        ]
        self.assertEqual(len(hidden_failures), 1, reporter.failures)
        self.assertIn("environment/core.py", hidden_failures[0])

    def test_environment_hidden_instructions_fails_on_walkthrough_in_markdown(self) -> None:
        """Markdown files inside environment/ with `STEP 1:` / `HINT:` line
        lead-ins or the literal word `walkthrough` are walkthroughs by any
        reasonable definition; these are exactly what the upstream rule
        prohibits."""
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = self.copy_fixture("public-contract-standard", tmpdir)
            env_dir = task_dir / "environment"
            env_dir.mkdir(exist_ok=True)
            (env_dir / "GUIDE.md").write_text(
                "# Step-by-step walkthrough\n\n"
                "STEP 1: open `core.py` and locate the `commit` function.\n"
                "STEP 2: change the lock acquisition order.\n"
                "STEP 3: rerun the tests.\n",
                encoding="utf-8",
            )
            reporter = run_static_checks.run_checks(task_dir, {"environment_hidden_instructions"})

        hidden_failures = [
            failure for failure in reporter.failures
            if "hidden-instruction content" in failure
        ]
        self.assertEqual(len(hidden_failures), 1, reporter.failures)
        self.assertIn("environment/GUIDE.md", hidden_failures[0])
        self.assertIn("prescriptive prose marker", hidden_failures[0])

    def test_environment_hidden_instructions_does_not_fire_on_todo_in_source_code(self) -> None:
        """Plain `# TODO: handle empty input` style comments inside source
        code are a normal idiom and must NOT trip the prose-only patterns.
        The prose patterns (HINT/STEP) are scoped to .md/.txt/.rst/.markdown
        files specifically because TODO/FIXME/HINT in comments are routine."""
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = self.copy_fixture("public-contract-standard", tmpdir)
            env_dir = task_dir / "environment"
            env_dir.mkdir(exist_ok=True)
            (env_dir / "core.py").write_text(
                "# TODO: handle empty input gracefully\n"
                "# HINT: the iterator may yield None\n"
                "# STEP 1: this is a comment header for a unit, not a walkthrough\n"
                "def normalize(items):\n"
                "    return [item for item in items if item]\n",
                encoding="utf-8",
            )
            reporter = run_static_checks.run_checks(task_dir, {"environment_hidden_instructions"})

        self.assertEqual(reporter.failures, [], reporter.failures)

    def test_environment_hidden_instructions_does_not_fire_on_user_agent_or_software_agent(self) -> None:
        """The word 'agent' in production senses (user-agent, HTTP agent,
        software agent, agent registration) is intentionally not flagged.
        Banning it would create false positives across most realistic
        web-service tasks; the rule only bans solver-direction phrasing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = self.copy_fixture("public-contract-standard", tmpdir)
            env_dir = task_dir / "environment"
            env_dir.mkdir(exist_ok=True)
            (env_dir / "transport.py").write_text(
                '"""HTTP transport layer.\n\n'
                "The user agent header is forwarded to downstream services.\n"
                "Each registered agent must implement the `dispatch()` protocol.\n"
                'The agent registry is keyed by agent ID.\n"""\n',
                encoding="utf-8",
            )
            reporter = run_static_checks.run_checks(task_dir, {"environment_hidden_instructions"})

        self.assertEqual(reporter.failures, [], reporter.failures)

    def test_environment_hidden_instructions_skipped_when_no_environment_dir(self) -> None:
        """Tasks without an environment/ directory (rare but legal during
        scaffolding) must produce a skip-style PASS, not a failure. The
        public-contract-standard fixture happens to ship without one, which
        exercises this path naturally."""
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = self.copy_fixture("public-contract-standard", tmpdir)
            self.assertFalse((task_dir / "environment").exists())

            reporter = run_static_checks.run_checks(task_dir, {"environment_hidden_instructions"})

        self.assertEqual(reporter.failures, [])
        self.assertIn(
            "environment/ hidden-instruction check skipped (no environment/ directory)",
            reporter.passes,
        )

    def _write_dockerfile_task(self, tmpdir: str, dockerfile: str, *, dockerignore: bool = False) -> Path:
        """Minimal Edition 2 task with a custom Dockerfile, for exercising the
        docker.md image checks in isolation via run_checks(..., {"dockerfile"})."""
        task_dir = Path(tmpdir) / "dockertask"
        env = task_dir / "environment"
        env.mkdir(parents=True)
        (task_dir / "task.toml").write_text(
            'version = "2.0"\n'
            "[metadata]\n"
            'author_name = "anonymous"\n'
            'author_email = "anonymous"\n'
            'difficulty = "hard"\n'
            'category = "debugging"\n'
            "tags = []\n"
            'languages = ["python"]\n'
            'codebase_size = "small"\n'
            "number_of_milestones = 0\n"
            "subcategories = []\n"
            "expert_time_estimate_min = 60\n"
            "junior_time_estimate_min = 240\n"
            "[agent]\n"
            "timeout_sec = 1800\n"
            "[verifier]\n"
            "timeout_sec = 600\n"
            "[environment]\n"
            "allow_internet = false\n"
            "build_timeout_sec = 600\n"
            "cpus = 2\n"
            "memory_mb = 4096\n"
            "storage_mb = 10240\n",
            encoding="utf-8",
        )
        (env / "Dockerfile").write_text(dockerfile, encoding="utf-8")
        if dockerignore:
            (env / ".dockerignore").write_text("solution/\ntests/\n", encoding="utf-8")
        return task_dir

    def test_dockerfile_broad_context_copy_is_rejected(self) -> None:
        """`COPY . /app` (or `ADD . <dest>`) copies the whole build context and is a
        docker.md hard failure; authors must copy narrow paths instead."""
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = self._write_dockerfile_task(
                tmpdir,
                "FROM python:3.11-slim@sha256:abc\nWORKDIR /app\nCOPY . /app\n",
            )
            reporter = run_static_checks.run_checks(task_dir, {"dockerfile"})

        broad = [f for f in reporter.failures if "whole build context" in f]
        self.assertEqual(len(broad), 1, reporter.failures)
        self.assertIn("COPY . /app", broad[0])

    def test_dockerfile_narrow_copy_is_accepted(self) -> None:
        """Narrow COPY paths (`COPY src/ /app/src/`) do not trip the
        broad-context-copy rule."""
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = self._write_dockerfile_task(
                tmpdir,
                "FROM python:3.11-slim@sha256:abc\nWORKDIR /app\nCOPY src/ /app/src/\n",
                dockerignore=True,
            )
            reporter = run_static_checks.run_checks(task_dir, {"dockerfile"})

        self.assertEqual([f for f in reporter.failures if "whole build context" in f], [])

    def test_dockerfile_warns_on_missing_session_tools_and_dockerignore(self) -> None:
        """Missing tmux/asciinema and a missing environment/.dockerignore are
        non-blocking docker.md WARNs (a static scan cannot see the base image, so
        they cannot be hard failures)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = self._write_dockerfile_task(
                tmpdir,
                "FROM python:3.11-slim@sha256:abc\nWORKDIR /app\nCOPY app/ /app/\n",
            )
            reporter = run_static_checks.run_checks(task_dir, {"dockerfile"})

        self.assertEqual(reporter.failures, [])
        self.assertEqual(len([w for w in reporter.warnings if "tmux/asciinema" in w]), 1)
        self.assertEqual(len([w for w in reporter.warnings if ".dockerignore is recommended" in w]), 1)

    def test_dockerfile_session_tools_and_dockerignore_present_clears_warnings(self) -> None:
        """Installing tmux + asciinema (pinned) and shipping environment/.dockerignore
        clears both docker.md WARNs and produces no failures."""
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = self._write_dockerfile_task(
                tmpdir,
                "FROM python:3.11-slim@sha256:abc\n"
                "WORKDIR /app\n"
                "RUN apt-get update \\\n"
                "    && apt-get install -y --no-install-recommends tmux=3.3a-3 asciinema=2.4.0-1 \\\n"
                "    && rm -rf /var/lib/apt/lists/*\n"
                "COPY app/ /app/\n",
                dockerignore=True,
            )
            reporter = run_static_checks.run_checks(task_dir, {"dockerfile"})

        self.assertEqual(reporter.failures, [])
        self.assertEqual([w for w in reporter.warnings if "tmux/asciinema" in w], [])
        self.assertEqual([w for w in reporter.warnings if ".dockerignore is recommended" in w], [])


class OfflineSelfContainedTestShTest(unittest.TestCase):
    """tests/test.sh under allow_internet=false may be self-contained via an
    OFFLINE wheelhouse install (pip install --no-index --find-links=/opt/wheels),
    optionally inside a venv. This is the reviewer-blessed pattern (sparse-block-
    preconditioner rev3, module-hot-reload-epoch passed review with it). A
    networked install (bare pip / uvx / curl|sh / apt) must still FAIL. The
    deps-baked-in-Dockerfile shape (test.sh installs nothing) also stays valid.

    Base fixture: implicit-step-restart (standard task, allow_internet=false).
    Only tests/test.sh is mutated per case.
    """

    BASE_FIXTURE = "implicit-step-restart"

    HEAD = (
        "#!/bin/bash\n\n"
        "mkdir -p /logs/verifier\n\n"
        'if [ "$PWD" = "/" ]; then\n'
        '  echo "Error: No working directory set. Please set a WORKDIR in your Dockerfile before running this script."\n'
        "  exit 1\n"
        "fi\n\n"
    )
    PYTEST = (
        "python -m pytest -o cache_dir=/tmp/pytest_cache "
        "--ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA\n"
    )
    REWARD = (
        "\nif [ $? -eq 0 ]; then\n"
        "    echo 1 > /logs/verifier/reward.txt\n"
        "else\n"
        "    echo 0 > /logs/verifier/reward.txt\n"
        "fi\n"
    )

    OFFLINE_TEST_SH_FAILURE = (
        "verifier-time network/package setup when [environment].allow_internet is false"
    )
    PREFIX_FAILURE = "preserve the official offline non-UI pre-pytest semantics"

    def _run_with_test_sh(self, body: str) -> run_static_checks.Reporter:
        fixture = FIXTURE_TASKS_DIR / self.BASE_FIXTURE
        with tempfile.TemporaryDirectory() as tmpdir:
            task_dir = Path(tmpdir) / fixture.name
            shutil.copytree(fixture, task_dir)
            (task_dir / "tests" / "test.sh").write_text(body, encoding="utf-8")
            return run_static_checks.run_checks(task_dir)

    def _offline_or_prefix_failures(self, reporter: run_static_checks.Reporter) -> list[str]:
        return [
            failure
            for failure in reporter.failures
            if self.OFFLINE_TEST_SH_FAILURE in failure or self.PREFIX_FAILURE in failure
        ]

    def test_offline_findlinks_install_passes(self) -> None:
        """`pip install --no-index --find-links` (line-continued) is offline-safe."""
        body = (
            self.HEAD
            + "pip install --no-cache-dir --no-index --find-links=/opt/wheels \\\n"
            + "  pytest==8.4.1 pytest-json-ctrf==0.3.5\n\n"
            + self.PYTEST
            + self.REWARD
        )
        reporter = self._run_with_test_sh(body)
        self.assertEqual(self._offline_or_prefix_failures(reporter), [])

    def test_offline_venv_then_findlinks_install_passes(self) -> None:
        """venv create + activate + offline wheelhouse install is offline-safe."""
        body = (
            self.HEAD
            + "python3 -m venv /tmp/tbench-testing\n"
            + ". /tmp/tbench-testing/bin/activate\n"
            + "pip install --no-index --find-links /opt/wheels pytest==8.4.1 pytest-json-ctrf==0.3.5\n\n"
            + self.PYTEST
            + self.REWARD
        )
        reporter = self._run_with_test_sh(body)
        self.assertEqual(self._offline_or_prefix_failures(reporter), [])

    def test_deps_in_dockerfile_no_install_passes(self) -> None:
        """The baked-in-Dockerfile shape (test.sh installs nothing) stays valid."""
        body = self.HEAD + self.PYTEST + self.REWARD
        reporter = self._run_with_test_sh(body)
        self.assertEqual(self._offline_or_prefix_failures(reporter), [])

    def test_bare_pip_install_fails(self) -> None:
        """A networked `pip install` (no --no-index) must still FAIL offline."""
        body = (
            self.HEAD
            + "pip install pytest==8.4.1 pytest-json-ctrf==0.3.5\n\n"
            + self.PYTEST
            + self.REWARD
        )
        reporter = self._run_with_test_sh(body)
        self.assertTrue(
            any(self.OFFLINE_TEST_SH_FAILURE in f for f in reporter.failures),
            reporter.failures,
        )

    def test_uvx_networked_install_fails(self) -> None:
        """uvx fetches from the network; it must FAIL under allow_internet=false."""
        body = (
            self.HEAD
            + "uvx -w pytest==8.4.1 -w pytest-json-ctrf==0.3.5 pytest "
            + "--ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA\n"
            + self.REWARD
        )
        reporter = self._run_with_test_sh(body)
        self.assertTrue(
            any(self.OFFLINE_TEST_SH_FAILURE in f for f in reporter.failures),
            reporter.failures,
        )

    def test_apt_install_fails(self) -> None:
        """A runtime apt-get install must FAIL under allow_internet=false."""
        body = (
            self.HEAD
            + "apt-get install -y curl\n\n"
            + self.PYTEST
            + self.REWARD
        )
        reporter = self._run_with_test_sh(body)
        self.assertTrue(
            any(self.OFFLINE_TEST_SH_FAILURE in f for f in reporter.failures),
            reporter.failures,
        )
