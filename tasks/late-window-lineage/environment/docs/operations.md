# Operations notes

`scripts/run-matrix.sh` is the normal local command. It removes old runtime state, builds the Rust binary, and writes the current audit to `output/window-audit.json`.

Intermediate state files may appear under `state/` during a run. They are runtime artifacts and can be removed between runs. The command does that cleanup before starting a new audit.
