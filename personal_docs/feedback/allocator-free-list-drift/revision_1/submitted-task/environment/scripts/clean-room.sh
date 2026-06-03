#!/bin/bash
set -euo pipefail
APP_ROOT="${APP_ROOT:-/app}"
rm -f "${APP_ROOT}"/output/alloc-audit.json "${APP_ROOT}"/output/*-audit.json
rm -f "${APP_ROOT}"/output/*.ledger.jsonl
