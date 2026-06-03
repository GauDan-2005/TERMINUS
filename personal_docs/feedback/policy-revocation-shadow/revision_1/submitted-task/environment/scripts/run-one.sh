#!/bin/bash
cd /app
mkdir -p /app/output
case_name="${1:-alpha}"
cargo run --offline --quiet -- "/app/output/policy-audit-${case_name}.json" "/app/traces/${case_name}.trace"
