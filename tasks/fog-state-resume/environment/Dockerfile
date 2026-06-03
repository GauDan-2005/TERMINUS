FROM python:3.13-slim@sha256:dc1546eefcbe8caaa1f004f16ab76b204b5e1dbd58ff81b899f21cd40541232f

LABEL org.opencontainers.image.source="terminal-bench-3"
LABEL org.opencontainers.image.revision="local"
LABEL org.opencontainers.image.created="2026-05-25"
LABEL org.opencontainers.image.version="fog-state-resume-v1"
LABEL org.opencontainers.image.licenses="NOASSERTION"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    asciinema=2.4.0-1 \
    golang-go=2:1.24~2 \
    gcc=4:14.2.0-1 \
    libc6-dev=2.41-12+deb13u3 \
    make=4.4.1-2 \
    tmux=3.5a-3 \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir \
    pytest==8.4.1 \
    pytest-json-ctrf==0.3.5

ENV CGO_ENABLED=1
ENV SOURCE_DATE_EPOCH=1700000000

COPY Makefile go.mod README.md /app/
COPY cmd /app/cmd
COPY config /app/config
COPY data /app/data
COPY docs /app/docs
COPY internal /app/internal
COPY probe /app/probe
COPY scripts /app/scripts

RUN make -s build

RUN chmod +x /app/scripts/run-matrix.sh /app/scripts/one-case.sh /app/scripts/clean-room.sh

CMD ["sleep", "infinity"]
