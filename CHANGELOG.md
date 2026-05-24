# Changelog

All notable changes to this project will be documented in this file. See [Conventional Commits](https://conventionalcommits.org) for commit guidelines.

## [Unreleased]

### Features
- **MCP server: selective tool registration.** New `--tools` / `--exclude-tools` CLI flags (with `AIOFMP_MCP_TOOLS` / `AIOFMP_MCP_EXCLUDE_TOOLS` env equivalents) let users restrict which of the 177 MCP tools get registered. The spec grammar mixes category-level and per-tool granularity: `chart` or `chart(*)` for a whole category, `chart(get_intraday_1hour,get_historical_price_full)` for specific tools, comma-separated. When both flags are set, the include set is the universe and exclude prunes from it.
- **MCP server: `--list-tools` flag** prints the full inventory of available categories and tool names, then exits. Does not require an API key.

## [1.2.0] - 2026-05-24

### Features
- **Harvester.** New `aiofmp harvest` / `aiofmp harvest-status` CLI commands: a long-running daemon that proactively warms the local Parquet cache for 17 categories on per-category intervals (chart EOD/intraday, statements, news, analyst estimates/snapshots, insider trades, form 13F, commodities, forex, indexes, economics, DCF, technical indicators).
- **Plan-aware operation.** Reads an FMP plan tier (`basic`/`starter`/`premium`/`ultimate`) from `harvester.yaml`, paces requests via a sliding-window per-minute rate limiter, applies a US-only symbol filter on Starter, and auto-disables categories or endpoints that are entirely paywalled on the chosen plan (e.g. `form13f`, `period=quarter` for `key_metrics`, the `1min` intraday timeframe, the `press_releases` news variant).
- **Per-category paywall short-circuit with re-probe TTL.** After N consecutive HTTP 402s within a cycle, the harvester ends the cycle as `PARTIAL` and skips subsequent cycles for ~24h before re-probing — avoids burning requests against a fully-paywalled endpoint.
- **Bandwidth budget tracker.** SQLite-backed monthly ledger attributes bytes to the category that made the request; soft cap pauses categories until next month; hard cap raises `FMPBudgetError`.
- **SQLite state store.** Per-cycle bookkeeping, last-seen-date checkpoints, symbol-universe catalogs with TTL refresh, and the bandwidth ledger live in `<state_dir>/harvester.sqlite`.
- **Symbol catalog.** Lazily discovers six universes (financial symbols, actively trading, ETFs, commodities, forex pairs, indexes) and refreshes them on a configurable interval; supports payload-aware filters so the indexes universe can drop non-USD listings using FMP's `currency` field.
- **Caching pattern coverage.** New `PAGE_WALK` temporal pattern in `CachedClient` (harvester-write, user-read) for analyst estimates, insider trades, and form 13F. New `SnapshotStore` for the P4 single-row-per-entity pattern used by analyst ratings and DCF.
- **Multi-category cache sharing.** Chart endpoints (`historical-price-eod/*`, intraday) are now registered under `commodity`, `forex`, and `indexes` categories too, so the shared FMP wire endpoint hits the same Parquet store regardless of which SDK category was called.
- **Bandwidth callback + ContextVar.** `FmpClient.on_response_size` reports each response body size, with `current_harvest_category` ContextVar attributing the bytes to the category that initiated the call (or `"user"` outside a harvester cycle).
- **`aiofmp` CLI group.** Existing `aiofmp-mcp-server` entry point is preserved; new `aiofmp` umbrella command wraps `harvest` and `harvest-status`.

### Fixes
- Atomic Parquet writes (write to `.tmp`, then rename) so an interrupted flush can't leave a 0-byte or partially-written file in the cache.
- Recover from 0-byte / corrupt Parquet files on read (delete and refetch) rather than erroring out.
- Sanitize Parquet records before write: stringify columns containing integers outside the float64-safe range (|x| > 2^53), stringify mixed string/numeric columns that appear during append, and null out empty struct values (`{"data": {}}`) that pyarrow can't infer a schema for.
- Per-minute rate-limit margin (~17%) under the documented plan caps to absorb residual server-side 429s.
- 429 and 5xx are transparently retried inside `_make_request` with bounded backoff; everything else (auth, paywall, parse, budget) propagates immediately so callers can apply per-exception policy.
- Per-category retry policy (`retry.on_429`, `retry.on_5xx`) wraps each `run_cycle` independently of the inner client retries.
- Cooperative cancellation: harvester cycles check `should_stop()` between symbols and pages so SIGINT propagates promptly.
- Statements safety-net seeds its checkpoint on first run and is bookkept under a separate `statements_safetynet` category row in the state store.
- News pagination uses a safety cap and short-circuits on empty pages.
- Symbol-catalog refresh treats permanent (4xx other than 429/402) errors as terminal and does not retry them.
- Use FMP's own economic-indicator names (`GDP`, `realGDP`, `CPI`, ...) — FRED codes like `UNRATE` / `FEDFUNDS` return `"Invalid name"`.
- Correct `financial_symbols` endpoint path.
- Quiet log lines for expected paywalls (info-level skip instead of warning per item) and at-startup category auto-disables.
- `aiofmp` CLI entry point is registered.

### Tests
- End-to-end smoke test covering all 17 harvester categories.
- Live-run regression coverage for paywall-memory paths, the mixed-column sanitization, and the 5xx retry policy.

### Docs
- Harvester README section plus `examples/harvester.example.yaml` tuned for Starter plan defaults.

## [1.1.0] - 2026-03-05

### Features
- **CachedClient.** A drop-in caching wrapper around `FmpClient`. Intercepts cacheable time-series methods, stores data in local Parquet files, and only fetches missing date ranges from the API on subsequent calls.
- Supported caching patterns:
  - **Date-range endpoints** (chart, economics, calendar, news, technical indicators, ...): gap detection fetches only the missing slices.
  - **Period-based endpoints** (income statements, balance sheets, ratios, ...): fetches fresh data and merges with stored history by date.
  - **Non-cacheable endpoints** (profiles, quotes, search, ...): pass through directly to the FMP API.
- Pluggable `StorageBackend` interface; ships with `ParquetStorage` (default location: `~/.aiofmp/cache`, override via `AIOFMP_CACHE_FILE_PATH`).
- `EndpointRegistry` describes which SDK methods are cacheable, the temporal pattern, the storage key, and the response date field.
- MCP server gains an `--cached` flag / `AIOFMP_CACHED` env var that switches the underlying client to `CachedClient` so MCP tool calls benefit from the same cache.

## [1.0.0] - 2025-10-21

### Features
- Initial release of aiofmp.
- Async-first Python client for the Financial Modeling Prep API built on asyncio + aiohttp.
- Category-based organization with 22 API categories: analyst, calendar, chart, commodity, company, COT, crypto, DCF, directory, economics, ETF, forex, form 13F, indexes, insider trades, market performance, news, quote, search, senate, statements, technical indicators.
- Built-in MCP (Model Context Protocol) server (`aiofmp-mcp-server`) exposing 177 tools to AI assistants via FastMCP.
- Both STDIO and HTTP transports for the MCP server.
- Comprehensive error handling with typed exceptions: `FMPError`, `FMPAuthenticationError`, `FMPRateLimitError`, `FMPResponseError`, `FMPServerError`, `FMPPaywallError`.
- Connection pooling, configurable timeouts, exponential-backoff retries, and a per-process concurrent-request semaphore.
- Full type hints throughout the codebase.
- 500+ unit tests covering every category and the MCP tool layer.
