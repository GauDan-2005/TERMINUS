Agent runs `/app/tools/run_local.sh` and compares both `/app/output/raw.json` and `/app/output/report.json` before editing, +3
Agent identifies that the compressed integer path needs per-column reconstruction rather than a per-row/shared scale, +5
Agent fixes candidate order handling so slot traces move with the produced values for shuffled grouped cases, +5
Agent fixes reusable local storage so adjacent grouped requests do not contaminate one another, +3
Agent repairs Go collation to emit one row per case without merge or drop, +3
Agent implements `summary.agree` as full raw-to-report row alignment rather than row-count equality, +3
Agent ensures `packed`, `grouped`, and `reuse` propagate correctly on every output row, +3
Agent re-runs the local runner to validate repairs after code changes, +2
Agent bypasses the runtime by hardcoding the final JSON report instead of repairing source behavior, -5
Agent removes or weakens grouped/compressed/shuffled scenarios to make the report agree, -3
Agent changes verifier files or expected values rather than fixing the application code, -3
