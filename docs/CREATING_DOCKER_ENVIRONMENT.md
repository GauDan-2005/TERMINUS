# Creating Docker Environment

Practical setup guide for a task's container environment: where the Dockerfile
lives, what a starter looks like, how a compose file is shaped, and how to build
and debug the image locally.

This page only summarizes the minimum so you can get an environment working. For
the canonical policy, the per-check rationale, the full canonical-base-image list,
and the CI gates, **`docs/DOCKER_REQUIREMENTS.md` is authoritative and wins on
conflict.** Run `python3 scripts/dockerfile_check.py tasks/<task-name>` before
zipping to surface most image problems locally (exit 0 PASS / 2 WARN / 1 FAIL).

## Basic Dockerfile

The Dockerfile lives at `tasks/<task-name>/environment/Dockerfile`:

```dockerfile
# Digest-pin every FROM. The digest below is an example — pin a current one for
# the canonical base of your task's language (see docs/DOCKER_REQUIREMENTS.md §2).
FROM public.ecr.aws/docker/library/python:3.13-slim-bookworm@sha256:<digest>

WORKDIR /app

# System deps — single apt layer; tmux + asciinema are REQUIRED (real-agent runs
# fail without them even when the oracle passes).
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        asciinema \
        ca-certificates \
        git \
        tmux \
    && rm -rf /var/lib/apt/lists/*

# Language deps — exact-pin every version (run_static_checks.py requires pins).
RUN pip install --no-cache-dir \
    numpy==1.26.4 \
    pandas==2.1.0

# Copy only what the image needs (never `COPY . .`); never copy solution/ or tests/.
COPY app/ /app/

ENV PYTHONPATH=/app
```

With `[environment] allow_internet = false`, the verifier runs offline: bake every
dependency into the image here, not at runtime in `tests/test.sh`.

## Minimum checklist

Before task-specific work, confirm the environment satisfies the basics:

- `environment/Dockerfile` exists and builds.
- The final runtime image installs both `tmux` and `asciinema`.
- Every `FROM` (and every pulled compose `image:`) is digest-pinned with `@sha256:<digest>`.
- The final runtime base is a canonical Terminal-Bench base (full list in
  `docs/DOCKER_REQUIREMENTS.md`) or explicitly exempt (`scratch`); a non-canonical
  pinned base needs a justification in `construction_manifest.json` `base_image`.
- Language dependencies are exact-pinned or lockfile-locked; apt packages are
  version-pinned, use `--no-install-recommends`, and clean `/var/lib/apt/lists/*`
  in the same layer.
- `environment/` is ≤ 100 MiB total and no single file is > 50 MiB.
- Non-trivial tasks include `environment/.dockerignore` (see `REPO_CONVENTIONS.md`).
- The image does **not** copy `solution/`, `tests/`, or hidden verifier assets.
- `tests/test.sh` dependencies are baked into the image; the verifier neither
  installs nor downloads at runtime.

See `docs/DOCKER_REQUIREMENTS.md` for the rationale and examples behind each item.

## docker-compose

Most tasks are single-container. A minimal shape:

```yaml
services:
  task:
    build: .
    working_dir: /app
    environment:
      - PYTHONPATH=/app
```

> **New multi-container tasks are no longer accepted** (in-progress ones may
> finish). If you maintain an existing multi-container task, digest-pin every
> service `image:` and pass service config via environment variables; see
> `docs/DOCKER_REQUIREMENTS.md`.

## Common starter patterns

Digest-pin the base in every pattern (shown as `@sha256:<digest>` placeholders).
These are starting points; for layer ordering, `.dockerignore`, reproducible
downloads, and multi-stage builds, see `docs/DOCKER_REQUIREMENTS.md`.

**Python**
```dockerfile
FROM public.ecr.aws/docker/library/python:3.13-slim-bookworm@sha256:<digest>
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ /app/src/
ENV PYTHONPATH=/app
```

**Node.js**
```dockerfile
FROM public.ecr.aws/docker/library/node:22-bookworm-slim@sha256:<digest>
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY src/ /app/src/
```

**System administration (Ubuntu base)**
```dockerfile
FROM public.ecr.aws/docker/library/ubuntu:24.04@sha256:<digest>
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl nginx vim \
    && rm -rf /var/lib/apt/lists/*
```

**Git repository checked out at a fixed commit** (pin the commit so the agent
cannot see later commits that contain the fix):
```dockerfile
FROM public.ecr.aws/docker/library/python:3.13-slim-bookworm@sha256:<digest>
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/example/repo.git /app \
    && cd /app && git checkout <commit-sha>
```

## Troubleshooting

**Build fails** — build and shell in locally:
```bash
docker build -t my-task tasks/<task-name>/environment
docker run -it my-task bash
```

**Container won't start** — inspect logs: `docker compose logs`.

**Permission issues (macOS)** — in Docker Desktop, Settings → Advanced, enable
"Allow the default Docker socket to be used".

For the complete list of blocking and warning CI checks and Docker-specific fixes,
see `docs/DOCKER_REQUIREMENTS.md` and `docs/PLATFORM_AUTO_EVAL.md`.
