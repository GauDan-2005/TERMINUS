FROM python:3.13-slim@sha256:dc1546eefcbe8caaa1f004f16ab76b204b5e1dbd58ff81b899f21cd40541232f

LABEL org.opencontainers.image.source="terminal-bench-3"
LABEL org.opencontainers.image.revision="local"
LABEL org.opencontainers.image.created="2026-05-22"
LABEL org.opencontainers.image.version="late-window-lineage-v1"
LABEL org.opencontainers.image.licenses="NOASSERTION"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    asciinema=2.4.0-1 \
    cargo=1.85.0+dfsg3-1 \
    rustc=1.85.0+dfsg3-1 \
    tmux=3.5a-3 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    pytest==8.4.1 \
    pytest-json-ctrf==0.3.5

COPY Cargo.toml README.md /app/
COPY data/ /app/data/
COPY docs/ /app/docs/
COPY scripts/ /app/scripts/
COPY src/ /app/src/

RUN chmod +x /app/scripts/run-matrix.sh

CMD ["sleep", "infinity"]
