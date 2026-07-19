# Trail MCP — k3s deployment

Serves the Trail MCP server (the six tools — `functions`, `schema`, `validate`, `describe`, `eval`,
`run`) over **streamable-HTTP** at `http://trail-mcp.ws.local/mcp`. dnsmasq resolves `*.ws.local` →
the Traefik LB, so the host routes automatically once the Ingress exists.

## Two variants

| File | Image | Data it can reach |
|---|---|---|
| `trail-mcp.yaml` (lean) | `trail-py/Dockerfile` (in the trail-lang repo) — `trail-lang[mcp]` only | inline `{"rows":[…]}` and `{"file":"…"}` |
| `trail-mcp-full.yaml` (live) | `Dockerfile.trail-mcp` (this dir) — adds the FMP/EDGAR/GMD providers | the above **plus** `{"config":"/config/trail.yaml"}` (live sources) |

## Build the provider image

Requires the trail repos checked out as siblings (`trail-py`, `trail-fmp`, `trail-edgar`,
`trail-gmd`) — the workspace layout. From the workspace root:

```bash
docker build -f deploy/Dockerfile.trail-mcp -t 192.168.70.168:30500/trail-mcp-full:<tag> .
docker push 192.168.70.168:30500/trail-mcp-full:<tag>   # k3s trusts this local registry
```

## Deploy

```bash
# Credentials — created out-of-band, never committed:
kubectl -n trail create secret generic trail-mcp-creds \
  --from-literal=FMP_API_KEY="<your FMP key>" \
  --from-literal=EDGAR_IDENTITY="Your Name you@example.com"

kubectl apply -f deploy/trail-mcp-full.yaml     # or trail-mcp.yaml for the lean variant
```

The full variant mounts the host FMP Parquet cache (`/home/.../aiofmp-cache/cache` → `/cache`,
single-node) and the trail.yaml ConfigMap at `/config/trail.yaml`.

## Use

Point an MCP client's **streamable-HTTP** transport at `http://trail-mcp.ws.local/mcp`. Tool `data`
argument is one of `{"rows":[…]}`, `{"file":"…"}`, or (full image) `{"config":"/config/trail.yaml"}`.
