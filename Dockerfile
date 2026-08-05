# aiofmp MCP server image.
#
# Built from the source tree so a local `docker compose build` and the published
# ghcr.io image (see .github/workflows/docker-publish.yml, which builds this same
# file at each release tag) stay identical. `VERSION` is stamped in by CI from the
# release tag; local builds fall back to "dev".

FROM python:3.13-slim AS base

ARG VERSION=dev
LABEL org.opencontainers.image.title="aiofmp-mcp-server" \
      org.opencontainers.image.description="Asynchronous Financial Modeling Prep API client with MCP server" \
      org.opencontainers.image.source="https://github.com/codemug/aiofmp" \
      org.opencontainers.image.licenses="Apache-2.0" \
      org.opencontainers.image.version="${VERSION}"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install the package + its runtime deps. Copying just the metadata + the
# package tree (not tests/, examples/, scripts/, docs/) keeps the image small
# without losing the editable-install layout the entry points expect.
COPY pyproject.toml README.md ./
COPY aiofmp ./aiofmp

RUN pip install .

# Non-root runtime user. Cache + state dirs are owned by it so the bind-mount
# from the host (./.cache → /cache) stays writable.
RUN useradd --create-home --uid 1000 aiofmp \
    && mkdir -p /cache \
    && chown -R aiofmp:aiofmp /cache /app
USER aiofmp

EXPOSE 3000

# Cache is on by default. The env var is the actual contract get_fmp_client()
# reads, so we set it at the container level (not via --cached) — that way
# any process inside the container (including `docker exec`) sees the same
# state as the running server.
ENV AIOFMP_CACHED=true \
    AIOFMP_CACHE_FILE_PATH=/cache

# TCP liveness on the MCP port: FastMCP returns 406 to a plain GET on /mcp/, so a
# successful connect (not an HTTP response) is the right signal that uvicorn is up.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import socket,sys; s=socket.socket(); s.settimeout(3); s.connect(('127.0.0.1',3000)); s.close()" || exit 1

ENTRYPOINT ["aiofmp-mcp-server"]
# CLI flags here set transport/host/port (env-set MCP_* vars are clobbered
# by the CLI's own defaults, so they must be passed as args).
CMD ["--transport", "http", "--host", "0.0.0.0", "--port", "3000"]
