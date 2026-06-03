# Operations

Use `/app/tools/run_local.sh` inside the container to refresh `/app/output/raw.json` and `/app/output/report.json`. The runner is self-contained and does not contact external services.

Packed integer rows expand with per-column scales `[2, 3, 5]` and biases `[1, -1, 2]` before downstream token derivation. Each column index picks its own scale and bias pair.
