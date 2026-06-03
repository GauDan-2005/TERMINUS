#!/bin/bash
set -euo pipefail
APP="${APP_ROOT:-/app}"
NAME="${1:?scenario name required}"
mkdir -p "${APP}/output" "${APP}/work"
"${APP}/build/bin/sim_run" --one "${NAME}" --out "${APP}/output/${NAME}-audit.json"
