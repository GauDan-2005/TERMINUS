Something in `/app` handles the bundled basalt, flint, shale, garnet, mica, and opal inputs on simple layouts. The combined report drifts once reordered block layouts enter the pipeline. Iteration tallies stall, residual columns disagree with independent measurement, or rows stay dirty even though the iterate looks settled.

Restore `bash /app/scripts/run-matrix.sh` so it writes `/app/output/solver-audit.json`. The per-case helper `bash /app/scripts/run-one.sh <name>` must write `/app/output/<name>-audit.json` matching the matrix slice for the same name. Two matrix runs from unchanged inputs must produce equivalent JSON.

The JSON has a top-level cases array. Each case reports name, ok, iterations, final_residual, reported_residual, residual_agrees, and hit_limit as documented in `/app/docs/layout.md`. Rebuild with CMake before re-running the audit scripts.
