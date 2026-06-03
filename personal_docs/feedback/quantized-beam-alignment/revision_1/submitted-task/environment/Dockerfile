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
      asciinema=2.2.0-1 \
      golang-go=2:1.19~1 \
      python-is-python3=3.11.2-1+deb12u1 \
      python3-pip=23.0.1+dfsg-1 \
      tmux=3.3a-3 \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir --break-system-packages \
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
