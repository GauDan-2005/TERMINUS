FROM python:3.13-slim@sha256:dc1546eefcbe8caaa1f004f16ab76b204b5e1dbd58ff81b899f21cd40541232f

LABEL org.opencontainers.image.source="terminal-bench-3"
LABEL org.opencontainers.image.revision="local"
LABEL org.opencontainers.image.created="2026-05-25"
LABEL org.opencontainers.image.version="allocator-free-list-drift-v2"
LABEL org.opencontainers.image.licenses="NOASSERTION"

ENV SOURCE_DATE_EPOCH=1735689600
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    asciinema=2.4.0-1 \
    gcc=4:14.2.0-1 \
    libc6-dev=2.41-12+deb13u3 \
    make=4.4.1-2 \
    tmux=3.5a-3 \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir \
    pytest==8.4.1 \
    pytest-json-ctrf==0.3.5

COPY Makefile /app/
COPY include /app/include
COPY config /app/config
COPY docs /app/docs
COPY data /app/data
COPY scripts /app/scripts
COPY pool_a /app/pool_a
COPY list_b /app/list_b
COPY split_c /app/split_c
COPY move_d /app/move_d
COPY acct_e /app/acct_e
COPY read_f /app/read_f
COPY flow_g /app/flow_g
COPY drive_h /app/drive_h
COPY src /app/src
COPY spill_i /app/spill_i
COPY mirror_j /app/mirror_j

RUN make clean -C /app && make -C /app && chmod +x /app/scripts/*.sh

CMD ["sleep", "infinity"]
