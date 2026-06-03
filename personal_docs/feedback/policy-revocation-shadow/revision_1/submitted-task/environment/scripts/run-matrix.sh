#!/bin/bash
cd /app
mkdir -p /app/output
cargo run --offline --quiet -- \
  /app/output/policy-audit.json \
  /app/traces/alpha.trace \
  /app/traces/beta.trace \
  /app/traces/gamma.trace \
  /app/traces/delta.trace \
  /app/traces/epsilon.trace \
  /app/traces/zeta.trace
