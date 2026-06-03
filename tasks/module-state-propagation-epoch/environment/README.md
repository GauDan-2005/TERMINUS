# Local runtime matrix

This repository models a small local runtime that evaluates a group of scenario descriptions. The JavaScript runner coordinates rows and invokes a Rust helper for numeric records. The main command is `npm run matrix`, which writes a JSON report under the local outcome directory.

The code is intentionally split into small subsystems because the same data travels through queueing, descriptor selection, native calculation, and summary formatting. Documentation in `docs/` describes the repo shape for maintainers.
