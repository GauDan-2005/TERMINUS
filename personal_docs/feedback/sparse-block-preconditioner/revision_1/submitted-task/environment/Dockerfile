FROM python:3.13-slim@sha256:dc1546eefcbe8caaa1f004f16ab76b204b5e1dbd58ff81b899f21cd40541232f

LABEL org.opencontainers.image.source="terminal-bench-3"
LABEL org.opencontainers.image.revision="local"
LABEL org.opencontainers.image.created="2026-05-25"
LABEL org.opencontainers.image.version="sparse-block-preconditioner-v1"
LABEL org.opencontainers.image.licenses="NOASSERTION"

ENV SOURCE_DATE_EPOCH=1735689600
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    asciinema=2.4.0-1 \
    cmake=3.31.6-2 \
    g++=4:14.2.0-1 \
    libc6-dev=2.41-12+deb13u3 \
    make=4.4.1-2 \
    tmux=3.5a-3 \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir \
    pytest==8.4.1 \
    pytest-json-ctrf==0.3.5

COPY CMakeLists.txt /app/
COPY include /app/include
COPY config /app/config
COPY docs /app/docs
COPY data /app/data
COPY scripts /app/scripts
COPY csr_m /app/csr_m
COPY bsr_n /app/bsr_n
COPY perm_p /app/perm_p
COPY prec_r /app/prec_r
COPY scale_q /app/scale_q
COPY solve_s /app/solve_s
COPY flow_t /app/flow_t
COPY drive_u /app/drive_u
COPY src /app/src
COPY spill_v /app/spill_v
COPY mirror_w /app/mirror_w

RUN chmod +x /app/scripts/*.sh

CMD ["sleep", "infinity"]
