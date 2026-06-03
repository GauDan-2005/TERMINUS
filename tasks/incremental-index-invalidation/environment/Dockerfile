FROM python:3.13-slim@sha256:dc1546eefcbe8caaa1f004f16ab76b204b5e1dbd58ff81b899f21cd40541232f

LABEL org.opencontainers.image.source="terminal-bench-3"
LABEL org.opencontainers.image.revision="local"
LABEL org.opencontainers.image.created="2026-05-22"
LABEL org.opencontainers.image.version="incremental-index-invalidation-v1"
LABEL org.opencontainers.image.licenses="NOASSERTION"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    asciinema=2.4.0-1 \
    cargo=1.85.0+dfsg3-1 \
    rustc=1.85.0+dfsg3-1 \
    tmux=3.5a-3 \
    && rm -rf /var/lib/apt/lists/*

COPY wheels/ /app/wheels/
COPY Cargo.toml README.md /app/
COPY fixtures/ /app/fixtures/
COPY r0/ /app/r0/
COPY r1/ /app/r1/
COPY r2/ /app/r2/
COPY r3/ /app/r3/
COPY r4/ /app/r4/
COPY r5/ /app/r5/
COPY r6/ /app/r6/
COPY r7/ /app/r7/
COPY r8/ /app/r8/
COPY scripts/ /app/scripts/
COPY src/ /app/src/
COPY traces/ /app/traces/

RUN chmod +x /app/scripts/run-matrix.sh

CMD ["sleep", "infinity"]
