# Container Image

The aiofmp MCP server is published as a multi-arch container image on the GitHub Container Registry:

```
ghcr.io/codemug/aiofmp-mcp-server
```

- **Architectures:** `linux/amd64`, `linux/arm64`
- **Tags:** `latest` (the most recent release) and each release version, e.g. `1.4.0`
- By default the image runs the MCP server over **HTTP on port 3000** with the local Parquet cache
  enabled.

A Financial Modeling Prep API key is required. [Get one here](https://site.financialmodelingprep.com/developer/docs/pricing).

## Quick start

```bash
docker run --rm -p 3000:3000 -e FMP_API_KEY=your_key_here \
  ghcr.io/codemug/aiofmp-mcp-server:latest
```

The server listens at `http://localhost:3000/mcp/` (streamable-HTTP). Point your MCP client's HTTP
transport at that URL.

## Docker Compose (recommended)

The repository ships a [`docker-compose.yaml`](../docker-compose.yaml) that runs the published image
with sensible defaults — resource limits, a persistent cache volume, and a health check:

```bash
# 1. Provide your API key (this file is gitignored)
echo "FMP_API_KEY=your_key_here" > .env

# 2. Pull and run the published image
docker compose pull
docker compose up
```

Build from local source instead of the published image:

```bash
docker compose up --build
```

Pin a specific image version by setting `AIOFMP_IMAGE_TAG` in `.env` (defaults to `latest`):

```
AIOFMP_IMAGE_TAG=1.4.0
```

## Configuration

The image reads its configuration from environment variables:

| Variable | Default (in image) | Purpose |
|---|---|---|
| `FMP_API_KEY` | — (**required**) | Financial Modeling Prep API key |
| `AIOFMP_CACHED` | `true` | Enable the local Parquet cache for time-series data |
| `AIOFMP_CACHE_FILE_PATH` | `/cache` | Where the cache is written (mount a volume here to persist it) |
| `AIOFMP_MCP_TOOLS` | — | Restrict which tools are registered (allowlist) — see [Selective tool registration](#selective-tool-registration) |
| `AIOFMP_MCP_EXCLUDE_TOOLS` | — | Prune tools from the registered set (denylist) |

**Transport / host / port / log level are command arguments, not environment variables.** The image's
default command already passes `--transport http --host 0.0.0.0 --port 3000`, which overrides any
`MCP_*` env vars. Change them by replacing the command:

```bash
docker run --rm -p 8080:8080 -e FMP_API_KEY=your_key_here \
  ghcr.io/codemug/aiofmp-mcp-server:latest \
  --transport http --host 0.0.0.0 --port 8080 --log-level DEBUG
```

In Compose, set the service `command:` (a commented example is included in `docker-compose.yaml`). The
full flag reference lives in the [CLI Reference](../README.md#cli-reference).

## Persisting the cache

The cache lives at `/cache` inside the container. Mount a host directory there so it survives restarts
and is shared across runs:

```bash
docker run --rm -p 3000:3000 -e FMP_API_KEY=your_key_here \
  -v "$PWD/.cache:/cache" \
  ghcr.io/codemug/aiofmp-mcp-server:latest
```

The bundled Compose file does this for you; override the host path with `AIOFMP_CACHE_DIR` in `.env`
(defaults to `./.cache`):

```
AIOFMP_CACHE_DIR=/mnt/data/aiofmp-cache
```

## Selective tool registration

The server registers its full set of MCP tools across 22 categories by default. To narrow what an AI
agent has to reason about, pass an allowlist and/or denylist via environment variables. The spec
grammar is `category`, `category(*)`, or `category(tool1,tool2)`, comma-separated — the full grammar
is documented under [Selective Tool Registration](../README.md#selective-tool-registration).

```bash
# Only the chart, quote, and search categories
docker run --rm -p 3000:3000 -e FMP_API_KEY=your_key_here \
  -e AIOFMP_MCP_TOOLS="chart(*),quote(*),search(*)" \
  ghcr.io/codemug/aiofmp-mcp-server:latest

# Everything except the 13F and senate tools
docker run --rm -p 3000:3000 -e FMP_API_KEY=your_key_here \
  -e AIOFMP_MCP_EXCLUDE_TOOLS="form13f,senate" \
  ghcr.io/codemug/aiofmp-mcp-server:latest
```

## Health check

The image defines a TCP health check on port 3000. (FastMCP returns HTTP 406 to a plain `GET /mcp/`, so
a socket connect — not an HTTP request — is the correct liveness signal.) `docker ps` and Compose
report the container's health automatically.

## Connecting an MCP client

With the container running over HTTP, point a streamable-HTTP MCP client at:

```
http://localhost:3000/mcp/
```

For a stdio-based client such as Claude Desktop it is usually simpler to run the `aiofmp-mcp-server`
CLI directly rather than through the container — see [MCP Server Usage](../README.md#mcp-server-usage).

## Image provenance

Images are built and pushed by
[`.github/workflows/docker-publish.yml`](../.github/workflows/docker-publish.yml) on each release,
multi-arch, with build provenance and an SBOM attached. OCI labels link every image back to this
repository and record the version it was built from.
