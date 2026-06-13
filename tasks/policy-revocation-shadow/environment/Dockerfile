FROM rust:1.85.0-bookworm@sha256:0ff31c9ffa641a62e48d543fb00b4960955ea375f40776f40f585b89e654cc5e

LABEL org.opencontainers.image.source="terminal-bench-3"
LABEL org.opencontainers.image.revision="local"
LABEL org.opencontainers.image.created="2026-05-24"
LABEL org.opencontainers.image.version="policy-revocation-shadow-v1"
LABEL org.opencontainers.image.licenses="NOASSERTION"

ENV SOURCE_DATE_EPOCH=1735689600
ENV PATH="/usr/local/cargo/bin:${PATH}"
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        asciinema=2.2.0-1 \
        python3-pip=23.0.1+dfsg-1 \
        tmux=3.3a-3 \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip download --no-cache-dir --only-binary=:all: \
    --dest /opt/test-wheels \
    pytest==8.4.1 \
    pytest-json-ctrf==0.3.5

COPY Cargo.lock Cargo.toml README.md /app/
COPY docs/ /app/docs/
COPY fixtures/ /app/fixtures/
COPY k0/ /app/k0/
COPY k1/ /app/k1/
COPY k2/ /app/k2/
COPY k3/ /app/k3/
COPY k4/ /app/k4/
COPY k5/ /app/k5/
COPY k6/ /app/k6/
COPY k7/ /app/k7/
COPY k8/ /app/k8/
COPY scripts/ /app/scripts/
COPY src/ /app/src/
COPY traces/ /app/traces/

RUN cargo build --locked --quiet

RUN chmod +x /app/scripts/run-matrix.sh /app/scripts/run-one.sh

CMD ["sleep", "infinity"]
