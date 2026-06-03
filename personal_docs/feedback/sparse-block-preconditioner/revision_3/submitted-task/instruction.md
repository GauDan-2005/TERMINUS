The tools under `/app` take the bundled basalt, flint, shale, garnet, mica, and opal inputs and produce a combined report. Right now that report cannot be trusted: across the cases, some iteration tallies are off, some residual columns disagree with an independently computed value, and some rows are not reported as settled when they should be.

Restore `bash /app/scripts/run-matrix.sh` so it writes `/app/output/solver-audit.json`. The per-case helper `bash /app/scripts/run-one.sh <name>` must write `/app/output/<name>-audit.json` matching the matrix slice for the same name. Two matrix runs from unchanged inputs must produce equivalent JSON.

The JSON has a top-level cases array. Each case reports name, ok, iterations, final_residual, reported_residual, residual_agrees, and hit_limit as documented in `/app/docs/layout.md`. Rebuild with CMake before re-running the audit scripts.

A fully correct run is one where every case in the audit reports ok true, the two residual columns agree, and all of those values match an independent reference computed from the same inputs.
