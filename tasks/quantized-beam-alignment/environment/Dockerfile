FROM rust:1.89-bookworm@sha256:c842cc0357b91bb15ad2bb89934513d0d226f711fac7f7fedb176d3311714d47

ARG SOURCE_DATE_EPOCH=1710000000
ENV SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH}

LABEL org.opencontainers.image.source="terminal-bench-local"
LABEL org.opencontainers.image.revision="quantized-beam-alignment-v1"
LABEL org.opencontainers.image.created="2026-05-22T00:00:00Z"
LABEL org.opencontainers.image.version="1.0"
LABEL org.opencontainers.image.licenses="MIT"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      asciinema \
      ca-certificates \
      golang-go \
      python-is-python3 \
      python3-pip \
      python3-venv \
      tmux \
    && rm -rf /var/lib/apt/lists/*

# Pre-stage verifier wheels at build time (network is available during build).
# tests/test.sh installs them offline so the verifier needs no network at runtime.
RUN python3 -m pip download --no-cache-dir --dest /opt/wheels \
      pytest==8.4.1 \
      pytest-json-ctrf==0.3.5

WORKDIR /app

COPY Cargo.toml Cargo.lock go.mod go.sum ./
COPY docs/ ./docs/
COPY config/ ./config/
COPY data/ ./data/
COPY src/ ./src/
COPY cmd/ ./cmd/
COPY internal/ ./internal/
COPY --chmod=0755 tools/run_local.sh ./tools/run_local.sh

RUN cargo fetch --locked --manifest-path /app/Cargo.toml
