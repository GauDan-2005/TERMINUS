#!/bin/bash
set -euo pipefail
APP_ROOT="${APP_ROOT:-/app}"
CASE="${1:?case name required}"
mkdir -p "${APP_ROOT}/output"
"${APP_ROOT}/bin/allocctl" one "${CASE}"
