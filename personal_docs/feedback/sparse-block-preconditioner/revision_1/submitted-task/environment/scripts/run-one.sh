#!/bin/bash
set -euo pipefail
APP_ROOT="${APP_ROOT:-/app}"
NAME="${1:?case name required}"
OUT="${APP_ROOT}/output"
mkdir -p "${OUT}"
bash "${APP_ROOT}/scripts/clean-room.sh"
"${APP_ROOT}/bin/solverctl" one "${NAME}"
