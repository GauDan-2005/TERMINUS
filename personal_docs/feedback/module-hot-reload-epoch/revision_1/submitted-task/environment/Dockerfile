FROM rust:1.85.0-slim-bookworm@sha256:c842cc0357b91bb15ad2bb89934513d0d226f711fac7f7fedb176d3311714d47

LABEL org.opencontainers.image.source="terminal-bench-3"
LABEL org.opencontainers.image.revision="local"
LABEL org.opencontainers.image.created="2026-05-22"
LABEL org.opencontainers.image.version="module-hot-reload-epoch-v1"
LABEL org.opencontainers.image.licenses="NOASSERTION"

WORKDIR /app

ENV SOURCE_DATE_EPOCH=1767225600
ENV PATH="/usr/local/cargo/bin:/opt/pytest/bin:${PATH}"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        asciinema=2.2.0-1 \
        nodejs=18.20.4+dfsg-1~deb12u2 \
        npm=9.2.0~ds1-1 \
        python3=3.11.2-1+b1 \
        python3-pip=23.0.1+dfsg-1 \
        python3-venv=3.11.2-1+b1 \
        tmux=3.3a-3 \
    && python3 -m venv /opt/pytest \
    && rm -rf /var/lib/apt/lists/*

RUN /opt/pytest/bin/pip install --no-cache-dir         pytest==8.4.1         pytest-json-ctrf==0.3.5

COPY package.json package-lock.json ./
COPY Cargo.toml Cargo.lock ./
COPY README.md ./README.md
COPY docs/ ./docs/
COPY fixtures/ ./fixtures/
COPY a1/ ./a1/
COPY b2/ ./b2/
COPY c3/ ./c3/
COPY d4/ ./d4/
COPY src/ ./src/
COPY --chmod=0755 tools/run_matrix.js ./tools/run_matrix.js
COPY --chmod=0755 scripts/clean-local.sh ./scripts/clean-local.sh

RUN cargo build --locked --bin mhre_native

CMD ["sleep", "infinity"]
