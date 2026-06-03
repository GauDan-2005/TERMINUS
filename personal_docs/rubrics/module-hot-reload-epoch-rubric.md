Agent runs `npm run matrix` and inspects `/app/outcome/report.json` before editing, +2
Agent traces both Node orchestration and the Rust native path (not only one layer), +5
Agent repairs carried counter and native row continuity across cycles, +5
Agent repairs deferred-value ownership so pending work stays with the correct row, +5
Agent repairs row-local descriptor factors without cross-scenario leakage, +5
Agent repairs Rust normalization for older native revisions, +3
Agent derives aggregate totals and status from records rather than constants, +2
Agent hardcodes report JSON or scenario answers, -5
Agent bypasses Node/Rust runtime with a fake runner, -5
Agent mutates fixture or scenario inputs instead of fixing logic, -2
