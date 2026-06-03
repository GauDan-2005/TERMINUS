#!/bin/bash
set -euo pipefail
APP_ROOT="${APP_ROOT:-/app}"
OUT="${APP_ROOT}/output"
mkdir -p "${OUT}"
bash "${APP_ROOT}/scripts/clean-room.sh"
"${APP_ROOT}/bin/solverctl" matrix
