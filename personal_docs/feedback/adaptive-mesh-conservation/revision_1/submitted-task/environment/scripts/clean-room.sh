#!/bin/bash
set -euo pipefail
APP="${APP_ROOT:-/app}"
rm -rf "${APP}/output" "${APP}/work"
mkdir -p "${APP}/output" "${APP}/work"
