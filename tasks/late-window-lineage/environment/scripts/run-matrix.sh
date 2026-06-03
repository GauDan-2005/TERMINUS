#!/bin/bash
set -euo pipefail

cd /app
rm -rf /app/state /app/output
mkdir -p /app/state /app/output
cargo build --quiet --release
/app/target/release/late-window-lab /app/output/window-audit.json
