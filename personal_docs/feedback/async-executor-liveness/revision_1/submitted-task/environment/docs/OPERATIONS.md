# Operations notes

Use `/app/scripts/run-matrix.sh` for a full local audit run and `/app/scripts/run-one.sh NAME` for a single shipped plan. Both commands write generated files below `/app/output` and are safe to repeat because the matrix command starts by clearing that directory.

The Rust binary does not need network access. It reads local plan files, produces deterministic report rows, and exits with a nonzero status only when local file I/O fails.

After a local release build, the executable path is `/app/target/release/executor-ctl`. The shipped plans use the lane-a and lane-b labels.
