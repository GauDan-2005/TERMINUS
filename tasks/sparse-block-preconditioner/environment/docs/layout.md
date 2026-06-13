# Layout notes

Internal modules under `/app` assemble case data into packed layouts used by the iterative driver.

The matrix audit at `/app/output/solver-audit.json` contains a top-level `cases` array. Each element carries name, ok, iterations, final_residual, reported_residual, residual_agrees, and hit_limit as defined below.

- `name` — scenario token
- `ok` — overall row status
- `iterations` — iteration count reported by the iterative solve
- `final_residual` — measured residual of the recovered solution against the original inputs
- `reported_residual` — value emitted through the metric helper
- `residual_agrees` — whether the two residual fields match within tolerance
- `hit_limit` — whether the iteration cap was reached

Per-case output from `run-one.sh` follows the same shape inside a one-element `cases` array written to `/app/output/<name>-audit.json`.
