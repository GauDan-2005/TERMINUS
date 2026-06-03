#!/bin/bash
set -euo pipefail
APP_ROOT="${APP_ROOT:-/app}"
rm -rf "${APP_ROOT}/output"
mkdir -p "${APP_ROOT}/output"
