#!/bin/bash
set -euo pipefail

bash /app/scripts/clean-room.sh
cargo run --quiet --release --bin executor-ctl -- --out /app/output/executor-audit.json --work /app/output/runtime
