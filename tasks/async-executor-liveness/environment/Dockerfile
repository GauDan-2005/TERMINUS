FROM rust:1.85.0-bookworm@sha256:0ff31c9ffa641a62e48d543fb00b4960955ea375f40776f40f585b89e654cc5e

LABEL org.opencontainers.image.source="terminal-bench-3"
LABEL org.opencontainers.image.revision="local"
LABEL org.opencontainers.image.created="2026-05-22"
LABEL org.opencontainers.image.version="async-executor-liveness-v1"
LABEL org.opencontainers.image.licenses="NOASSERTION"

ENV PATH="/usr/local/cargo/bin:${PATH}"
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        asciinema=2.2.0-1 \
        python3-pip=23.0.1+dfsg-1 \
        tmux=3.3a-3 \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --break-system-packages --no-cache-dir \
    pytest==8.4.1 \
    pytest-json-ctrf==0.3.5

COPY Cargo.lock Cargo.toml /app/
COPY book_b/ /app/book_b/
COPY core_a/ /app/core_a/
COPY data/ /app/data/
COPY docs/ /app/docs/
COPY drive_g/ /app/drive_g/
COPY flow_e/ /app/flow_e/
COPY gate_c/ /app/gate_c/
COPY host_d/ /app/host_d/
COPY mirror_j/ /app/mirror_j/
COPY note_k/ /app/note_k/
COPY read_h/ /app/read_h/
COPY scripts/ /app/scripts/
COPY spill_i/ /app/spill_i/
COPY src/ /app/src/
COPY types_f/ /app/types_f/

RUN chmod +x /app/scripts/run-matrix.sh /app/scripts/run-one.sh /app/scripts/clean-room.sh

CMD ["sleep", "infinity"]
