#!/bin/bash
set -euo pipefail
APP="${APP_ROOT:-/app}"
bash "${APP}/scripts/clean-room.sh"
"${APP}/build/bin/sim_run" --matrix --out "${APP}/output/conservation_audit.json"
