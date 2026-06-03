#!/bin/bash
set -euo pipefail
cargo --version
mkdir -p /app/output /app/bin
cargo build --release --quiet --manifest-path /app/Cargo.toml
/app/target/release/local-infer-sandbox /app/output/raw.json
go build -o /app/bin/align /app/cmd/align/main.go
/app/bin/align /app/output/raw.json /app/output/report.json
