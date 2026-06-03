# Operations

Build the driver with CMake:

```
cmake -S /app -B /app/build
cmake --build /app/build -j2
```

The driver lands at `/app/build/bin/sim_run`. The wrappers under
`/app/scripts` invoke it:

- `bash /app/scripts/run-matrix.sh` runs every bundled scenario and writes
  `/app/output/conservation_audit.json`.
- `bash /app/scripts/run-one.sh <name>` writes `/app/output/<name>-audit.json`.
- `bash /app/scripts/run-replay.sh <name>` writes
  `/app/output/<name>-replay.json`.

Scenario schedules live in `/app/config/cases.toml`. Starting states live in
`/app/data/init`. Snapshots are written under `/app/work` during scenarios
that round-trip through a saved checkpoint.
