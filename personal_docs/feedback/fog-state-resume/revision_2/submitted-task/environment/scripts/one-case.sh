#!/bin/bash
set -euo pipefail
if [ "$#" -lt 1 ]; then
  echo "usage: one-case.sh <name>" >&2
  exit 2
fi
name="$1"
out="/app/output/single-${name}.json"
bash /app/scripts/run-matrix.sh --out "$out" --case "$name"
