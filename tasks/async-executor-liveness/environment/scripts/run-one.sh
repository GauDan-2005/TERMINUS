#!/bin/bash
set -euo pipefail

case_name="${1:?case name required}"
out="${2:-/app/output/executor-audit.json}"
work="${3:-/app/output/runtime}"
mkdir -p /app/output
cargo run --quiet --release --bin executor-ctl -- --case "$case_name" --out "$out" --work "$work"
