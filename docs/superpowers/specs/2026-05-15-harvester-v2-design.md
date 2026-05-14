# Harvester v2 — Design

**Date:** 2026-05-15
**Status:** Approved (pending user review of written spec)
**Owners:** codemug
**Related code:** `aiofmp/cachedclient/`, `aiofmp/base.py`, `aiofmp/cli.py`

## 1. Goal & non-goals

**Goal.** A long-running CLI process (`aiofmp harvest --config harvester.yaml`) that proactively warms the local Parquet cache with FMP data, choosing per-category strategies that minimize redundant fetches and stay under the 20 GB/month FMP starter-plan cap.

**Non-goals.**

- Not a data analytics or query tool. Reads/queries remain the user's job via `CachedClient`.
- Not a generic scheduler. It only knows how to harvest FMP categories.
- Does not modify on-demand `CachedClient` semantics. User-driven queries behave identically whether the harvester is running or not.
- Does not auto-promote new categories without code changes. Adding a category is a typed, reviewed addition.

## 2. Architecture

```
aiofmp harvest --config harvester.yaml
        │
        ▼
HarvesterManager
  ├─ load YAML → HarvestConfig
  ├─ create one FmpClient + CachedClient (shared, reused across categories)
  ├─ create StateStore (sqlite3 at <state_dir>/harvester.sqlite)
  ├─ create BudgetTracker (reads/writes to StateStore)
  ├─ create SymbolCatalog (reads/writes to StateStore)
  ├─ register SIGINT/SIGTERM → stop_event
  └─ spawn one asyncio.Task per enabled category

CategoryHarvester (abstract base, one running task per concrete subclass):
  while not stop_event.is_set():
      await wait_until(next_due, stop_event)
      if await budget.is_paused(category): continue
      await run_cycle()                    # category-specific logic
      state.record_run(category, status, items, bytes)
      next_due = now + interval

  on CancelledError:
      flush partial checkpoint
      mark current run 'partial'
      re-raise

Manager: await asyncio.gather(*tasks, return_exceptions=True), then close.
```

**Module layout (new):**

```
aiofmp/harvester/
  __init__.py            (public exports)
  cli.py                 (click subcommand wiring)
  manager.py             (HarvesterManager, lifecycle, signal handling)
  config.py              (YAML schema → dataclasses, interval parsing)
  state.py               (StateStore — sqlite3 wrapper, schema migrations)
  budget.py              (BudgetTracker)
  catalog.py             (SymbolCatalog — discover and persist symbol universes)
  base.py                (CategoryHarvester ABC, retry/backoff, cycle bookkeeping)
  categories/
    statements.py
    analyst_estimates.py
    analyst_snapshots.py
    insider_trades.py
    form13f.py
    chart_eod.py
    chart_intraday.py
    technical_indicators.py
    news.py
    economics.py
    commodities_eod.py
    commodities_intraday.py
    forex_eod.py
    forex_intraday.py
    indexes_eod.py
    indexes_intraday.py
    dcf.py
```

**Touched code outside `harvester/`:**

- `aiofmp/cli.py` — wire `aiofmp harvest` and `aiofmp harvest-status` subcommands.
- `aiofmp/cachedclient/registry.py` — add `TemporalPattern.PAGE_WALK`, supporting fields on `CacheableEndpoint`, and register the new endpoints (analyst estimates, insider trades, form 13F). Also register the historical-price-eod and historical-chart endpoints under the `commodity`, `forex`, and `indexes` categories so user-driven calls to those category methods hit the same cache as the existing `chart.*` registrations (storage key is keyed off `api_endpoint`, so all four categories share parquet location).
- `aiofmp/cachedclient/proxy.py` — read-only handling for `PAGE_WALK` keys when called from user code (no implicit writes).
- `aiofmp/base.py` — emit response-size estimate to a callback so `BudgetTracker` can attribute bytes per category; add `FMPBudgetError` exception raised when the monthly hard cap is exceeded.

No changes to existing parquet layout or `StorageBackend` interface.

## 3. Symbol catalog

Six "universes" are sourced from FMP's directory and per-category list endpoints. Each universe is discovered lazily on first use, cached in `symbol_catalog` (SQLite), and refreshed when older than `discovery.refresh_interval` (default 7 days).

| Universe | FMP endpoint | Used by |
| --- | --- | --- |
| `financial_symbols` | `directory.financial_symbols()` | statements, dcf |
| `actively_trading` | `directory.actively_trading()` | analyst_estimates, analyst_snapshots, chart_eod, chart_intraday, technical_indicators, insider_trades sharding |
| `commodities` | `commodity.commodities_list()` | commodities_eod, commodities_intraday |
| `forex_pairs` | `forex.forex_list()` | forex_eod, forex_intraday |
| `indexes` | `indexes.index_list()` | indexes_eod, indexes_intraday |
| `etf_list` | `directory.etf_list()` | (no category harvests ETFs yet; kept for future) |

`SymbolCatalog.symbols(universe: str) -> list[str]` returns the cached list and triggers a refresh if expired. Directory endpoints themselves are passthrough in `CachedClient` today — `symbol_catalog` is their de facto cache.

## 4. The four harvest patterns

| Pattern | Idea | First run | Subsequent runs |
| --- | --- | --- | --- |
| **P1 Discover-then-fill** | Use a "what changed since X" endpoint to find work, then fetch only that. | Full backfill for every catalog symbol. | Hit the discovery endpoint with `from = last_run`. Only touched symbols get fetched. |
| **P2 Walk-back-until-checkpoint** | Page from newest backwards until first record < checkpoint or max_backfill reached. | Walk pages until oldest record < `today - max_backfill`. | Walk until oldest record in page < `last_run`. |
| **P3 Gap-fill (CachedClient native)** | Request the full window; `CachedClient` gap detection fetches only what's missing. | First call fetches the full window. | Subsequent calls fetch only the tail (or any holes). |
| **P4 Snapshot overwrite** | Fetch latest snapshot per symbol; replace stored copy. | Same as subsequent: fetch + replace. | Fetch + replace. |

## 5. Per-category strategies

| Category | Pattern | Discovery / walk endpoint | Persistence | Default interval |
| --- | --- | --- | --- | --- |
| **statements** | P1 | `calendar.earnings_calendar(from=last_run, to=now)` returns symbols with filings in the window. For each touched symbol, call all 13 statement endpoints. Specifics: the 10 period+limit endpoints (income, balance, cash flow, key_metrics, ratios, enterprise_values, 4× growth) run for both `annual` and `quarter` with `limit=incremental_limit` (default 2); `owner_earnings` runs once with `limit=incremental_limit` (no period param); the 2 segmentation endpoints run once per `period`. First run uses `limit=initial_limit` (default 40). Plus monthly safety-net sweep (Section 6). | `CachedClient` `PERIOD_BASED` (existing) | 6h |
| **analyst_estimates** | P2 | Per symbol in `actively_trading`, walk `analyst.financial_estimates(symbol, period='annual', page=N, limit=page_size)` until first record date < `min(last_run, today - max_backfill_years)`. | New `PAGE_WALK` registry entry, key `("analyst-estimates", symbol, "annual")`. | 24h |
| **analyst_snapshots** | P4 | Per symbol in `actively_trading`: `ratings_snapshot`, `price_target_consensus`, `price_target_summary`, `stock_grades_summary`. | New simple snapshot storage: key `("snapshot/<api-endpoint>", symbol)` → single-row parquet, overwritten each cycle. | 24h |
| **chart_eod** | P3 | Per symbol in `actively_trading`: `cached.chart.historical_price_full(symbol, today - backfill_years, today)`. Variants list also supports `historical_price_light` / `historical_price_unadjusted` / `historical_price_dividend_adjusted`. | `CachedClient` `DATE_RANGE` (existing) | 24h |
| **chart_intraday** *(off by default)* | P3 | Per `(symbol, timeframe)` for symbols in `actively_trading`: `cached.chart.intraday_<tf>(symbol, today - backfill_days, today)`. | `CachedClient` `DATE_RANGE` (existing) | 4h |
| **technical_indicators** *(off by default)* | P3 | Per `(symbol, indicator, period_length, timeframe)`: `cached.technical_indicators.<method>(...)`. Configurable list. | `CachedClient` `DATE_RANGE` (existing) | 24h |
| **news** | P3 | For each variant in `[general_news, press_releases, stock_news, crypto_news, forex_news]`: `cached.news.<variant>(from = today - backfill_days_initial, to = now, limit = page_size)`. The `CachedClient` `DATE_RANGE` gap detector handles the incremental tail — after the first cycle each subsequent cycle only fetches the new days. The harvester walks `page` until a returned batch is empty or its newest record falls in the existing cache window. | `CachedClient` `DATE_RANGE` (existing) | 30m |
| **insider_trades** | P2 (global walk, per-symbol shard on write) | `insider_trades.latest_insider_trades(page=N, limit=page_size)` until oldest `filingDate < last_run` or page index ≥ `max_pages`. | New `PAGE_WALK` entry. Records sharded by `symbol` into key `("insider-trading/latest", symbol)`. A second key `("insider-trading/latest", "_global")` holds the raw global stream for completeness. | 6h |
| **form13f** | P2 (global walk, per-CIK shard on write) | `form13f.latest_filings(page=N, limit=page_size)` until oldest `acceptedDate < last_run` or page index ≥ `max_pages`. | New `PAGE_WALK` entry. Records sharded by `cik` into key `("institutional-ownership/latest", cik)`. Per-CIK detail extracts (`filings_extract`) are NOT harvested in v1 — fetched on-demand by users. | 24h |
| **economics** | P3 | `cached.economics.treasury_rates(today - backfill_years, today)` plus per-indicator `cached.economics.economic_indicators(name, today - backfill_years, today)`. Indicators come from config (default: `GDP`, `CPI`, `UNRATE`, `FEDFUNDS`, `DFF`). | `CachedClient` `DATE_RANGE` (existing) | 24h |
| **commodities_eod** | P3 | For each symbol in `commodities` universe (~50 symbols), `cached.commodity.historical_price_full(symbol, today - backfill_years, today)`. Variants list also supports `historical_price_light`. | `CachedClient` `DATE_RANGE` (new registration under `commodity` category, shared parquet with `chart.historical_price_full`) | 24h |
| **commodities_intraday** *(off by default)* | P3 | Per `(symbol, timeframe)` for symbols in `commodities` universe: `cached.commodity.intraday_<tf>(symbol, today - backfill_days, today)`. | `CachedClient` `DATE_RANGE` (new registration under `commodity` category) | 4h |
| **forex_eod** | P3 | For each symbol in `forex_pairs` universe (~200–300 pairs), `cached.forex.historical_price_full(symbol, today - backfill_years, today)`. Variants list also supports `historical_price_light`. | `CachedClient` `DATE_RANGE` (new registration under `forex` category) | 24h |
| **forex_intraday** *(off by default)* | P3 | Per `(symbol, timeframe)` for symbols in `forex_pairs` universe: `cached.forex.intraday_<tf>(symbol, today - backfill_days, today)`. | `CachedClient` `DATE_RANGE` (new registration under `forex` category) | 4h |
| **indexes_eod** | P3 | For each symbol in `indexes` universe (~100–200), `cached.indexes.historical_price_eod_full(symbol, today - backfill_years, today)`. Variants list also supports `historical_price_eod_light`. | `CachedClient` `DATE_RANGE` (new registration under `indexes` category, `DATE_OBJ` date type) | 24h |
| **indexes_intraday** *(off by default)* | P3 | Per `(symbol, timeframe)` for symbols in `indexes` universe: `cached.indexes.intraday_<tf>(symbol, today - backfill_days, today)`. | `CachedClient` `DATE_RANGE` (new registration under `indexes` category, `DATE_OBJ`) | 4h |
| **dcf** | P4 | Per symbol in `financial_symbols`: `dcf.dcf_valuation(symbol)` and `dcf.levered_dcf(symbol)`. Both return one-row point-in-time snapshots that change only when underlying statements change. `custom_dcf_*` is NOT harvested (user-parameterized). | Snapshot store: key `("snapshot/<api-endpoint>", symbol)` → single-row parquet, overwritten each cycle. | 24h |

### New CachedClient surface area

- Add `TemporalPattern.PAGE_WALK = "page_walk"` and supporting `CacheableEndpoint` fields: `page_param: str`, `walk_date_field: str`, `default_page_size: int`.
- `PAGE_WALK` keys are **harvester-write, user-read**. The proxy:
  - On normal user call to a `PAGE_WALK`-registered method: read all stored records, filter to the call's `limit`/`page`/`symbol` filter, return. Never writes.
  - The harvester does not call the proxy for these endpoints; it calls the raw `FmpClient` method and writes directly to `StorageBackend` via the same key the proxy would read from.
- Snapshot (P4) storage: a tiny helper `SnapshotStore` writes one-row parquet under `("snapshot/<endpoint>", entity)` and is read by the proxy via passthrough today (no change to user-facing semantics).

## 6. Monthly safety-net sweep (statements)

In addition to the incremental P1 flow, statements run a full safety-net sweep every `safety_net_interval` (default `30d`). During a safety-net cycle the category ignores `last_run` for the earnings-calendar probe and instead enumerates every symbol in `financial_symbols`, calling each statement endpoint with `limit=incremental_limit` (default 2). This catches filings missed by earnings-calendar discovery (e.g. non-US issuers, funds without earnings calls).

The safety-net cycle is bookkept as a separate `category_runs` row (category=`statements_safetynet`) so its bandwidth and timing are observable independently.

## 7. Config schema (YAML)

```yaml
# harvester.yaml
state_dir: ~/.aiofmp/cache              # parquet + harvester.sqlite both live here
log_level: INFO                         # DEBUG | INFO | WARNING | ERROR

budget:
  monthly_soft_cap_gb: 18
  monthly_hard_cap_gb: 20
  soft_cap_behavior: pause_until_next_month   # | warn_only

retry:
  on_429:
    backoff_seconds: [60, 120, 240, 480]
    max_attempts: 4
  on_5xx:
    backoff_seconds: [10, 30, 60]
    max_attempts: 3

discovery:
  refresh_interval: 7d                  # how often to refresh symbol catalogs

categories:
  statements:
    enabled: true
    interval: 6h
    periods: [annual, quarter]
    initial_limit: 40                   # first-time per symbol
    incremental_limit: 2                # per discovery hit
    safety_net_interval: 30d            # full sweep cadence

  analyst_estimates:
    enabled: true
    interval: 24h
    estimate_periods: [annual]
    max_backfill_years: 3
    page_size: 100

  analyst_snapshots:
    enabled: true
    interval: 24h
    include: [ratings_snapshot, price_target_consensus, price_target_summary, stock_grades_summary]

  chart_eod:
    enabled: true
    interval: 24h
    variants: [historical_price_full]
    backfill_years: 10
    symbol_universe: actively_trading

  chart_intraday:
    enabled: false
    interval: 4h
    timeframes: [1hour]
    backfill_days: 30
    symbol_universe: actively_trading

  technical_indicators:
    enabled: false
    interval: 24h
    indicators: []                       # [{method: simple_moving_average, period_length: 20, timeframe: 1day}, ...]
    symbol_universe: actively_trading

  news:
    enabled: true
    interval: 30m
    variants: [general_news, press_releases, stock_news, crypto_news, forex_news]
    backfill_days_initial: 30
    page_size: 100

  insider_trades:
    enabled: true
    interval: 6h
    max_pages: 200
    page_size: 100

  form13f:
    enabled: true
    interval: 24h
    max_pages: 50
    page_size: 100

  economics:
    enabled: true
    interval: 24h
    indicators: [GDP, CPI, UNRATE, FEDFUNDS, DFF]
    backfill_years: 10

  commodities_eod:
    enabled: true
    interval: 24h
    variants: [historical_price_full]
    backfill_years: 10

  commodities_intraday:
    enabled: false
    interval: 4h
    timeframes: [1hour]
    backfill_days: 30

  forex_eod:
    enabled: true
    interval: 24h
    variants: [historical_price_full]
    backfill_years: 10

  forex_intraday:
    enabled: false
    interval: 4h
    timeframes: [1hour]
    backfill_days: 30

  indexes_eod:
    enabled: true
    interval: 24h
    variants: [historical_price_eod_full]
    backfill_years: 10

  indexes_intraday:
    enabled: false
    interval: 4h
    timeframes: [1hour]
    backfill_days: 30

  dcf:
    enabled: true
    interval: 24h
    include: [dcf_valuation, levered_dcf]
```

**Interval parsing.** `Ns`, `Nm`, `Nh`, `Nd` (case-insensitive). Validation rejects anything else.

## 8. State store (SQLite)

`<state_dir>/harvester.sqlite`:

```sql
CREATE TABLE category_runs (
  category TEXT NOT NULL,
  started_at TEXT NOT NULL,            -- ISO8601 UTC
  finished_at TEXT,
  status TEXT NOT NULL,                -- 'running' | 'ok' | 'partial' | 'error' | 'paused_for_budget'
  items_attempted INTEGER NOT NULL DEFAULT 0,
  items_succeeded INTEGER NOT NULL DEFAULT 0,
  bytes_estimate INTEGER NOT NULL DEFAULT 0,
  error TEXT,
  PRIMARY KEY (category, started_at)
);

CREATE TABLE checkpoints (
  category TEXT NOT NULL,
  scope TEXT NOT NULL,                 -- 'global' | '<symbol>' | '<symbol>/<period>' | '<cik>' | etc.
  checkpoint TEXT NOT NULL,            -- ISO8601 date or datetime
  updated_at TEXT NOT NULL,
  PRIMARY KEY (category, scope)
);

CREATE TABLE symbol_catalog (
  universe TEXT NOT NULL,              -- 'financial_symbols' | 'actively_trading' | 'commodities'
                                       --   | 'forex_pairs' | 'indexes' | 'etf_list'
  symbol TEXT NOT NULL,
  payload_json TEXT,                   -- whole row from FMP
  discovered_at TEXT NOT NULL,
  PRIMARY KEY (universe, symbol)
);

CREATE TABLE catalog_refresh (
  universe TEXT PRIMARY KEY,
  last_refreshed_at TEXT NOT NULL
);

CREATE TABLE bandwidth_ledger (
  month TEXT NOT NULL,                 -- 'YYYY-MM' UTC
  category TEXT NOT NULL,
  bytes INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (month, category)
);

CREATE INDEX idx_category_runs_started ON category_runs(category, started_at DESC);
```

Schema version table + simple linear migrations live alongside in `state.py`.

## 9. Failure & budget behavior

- **429 (rate limit).** Caught in `CategoryHarvester._run_with_backoff`. Sleeps `retry.on_429.backoff_seconds[attempt]` then retries. Exhaustion → mark current cycle `partial`, persist whatever checkpoint progress was made, schedule next cycle normally.
- **5xx.** Same retry ladder via `retry.on_5xx`.
- **Other exceptions during a per-item fetch.** Logged, counted in `items_attempted` but not `items_succeeded`, cycle continues — one bad symbol does not kill the category.
- **Cycle-wide exception (config bug, SDK bug).** Caught by `CategoryHarvester.run()`, logged with traceback, cycle marked `error`. Task keeps running and will retry on next due time.
- **Soft cap.** Before each cycle, `BudgetTracker.is_paused(category)` sums `bandwidth_ledger` for the current UTC month. If ≥ `monthly_soft_cap_gb` → log a warning, write a `paused_for_budget` row to `category_runs`, return. Resumes naturally on the first cycle of the next UTC month (month rollover detection happens at the top of each `wait_until`).
- **Hard cap.** A hot per-request check inside `FMPBaseClient` — when accumulated month bytes ≥ `monthly_hard_cap_gb`, raise `FMPBudgetError` (new exception in `aiofmp/base.py`, subclass of `FMPError`). The category catches it, marks the cycle `partial`, and sleeps until next month. The hard-cap check applies to harvester-initiated requests only (those with a category context); user-driven `CachedClient` queries are never blocked, but they are still tallied under the `'user'` category in `bandwidth_ledger` for visibility.

## 10. Byte accounting

`FMPBaseClient._handle_response` is extended with an optional `on_response_size(category: str | None, byte_count: int)` callback. The harvester registers a callback per CategoryHarvester via a `contextvars.ContextVar[str]` set at the top of each cycle so concurrent categories attribute bytes correctly. Byte count is `len(raw_body)` after `response.read()` — close enough for soft/hard cap decisions; chunked responses rarely carry an accurate Content-Length.

User-driven `CachedClient` calls (not harvester-initiated) write to a `bandwidth_ledger` row with `category = 'user'` so the harvester's budget isn't polluted by ad-hoc queries.

## 11. CLI

```bash
aiofmp harvest --config harvester.yaml                    # run forever
aiofmp harvest --config harvester.yaml --once             # one cycle per category, then exit
aiofmp harvest --config harvester.yaml --category news --once   # one-shot single category
aiofmp harvest --config harvester.yaml --dry-run          # print plan, fetch nothing
aiofmp harvest-status --config harvester.yaml             # summary table from state store
```

`--config` defaults to `./harvester.yaml`, then `~/.aiofmp/harvester.yaml`.

`--once` and `--dry-run` exit code: 0 on success, 1 on any category error.

## 12. Lifecycle

1. `cli.harvest` loads YAML → validates → builds `HarvestConfig`.
2. `HarvesterManager.__init__(config)`, then `await manager.start()`:
   - opens SQLite, applies schema migrations,
   - constructs shared `FmpClient` and `CachedClient`, enters async context,
   - constructs `BudgetTracker` and `SymbolCatalog`,
   - registers SIGINT/SIGTERM handlers that set `manager.stop_event`.
3. Manager builds the list of enabled `CategoryHarvester` instances and spawns one task each.
4. `await asyncio.gather(*tasks, return_exceptions=True)` — main loop.
5. On stop: every task observes `stop_event`, finishes its current cycle iteration (or catches `CancelledError` if cancellation is forced after a grace timeout), flushes state, returns.
6. `manager.close()` closes the CachedClient context and SQLite. Process exits 0.

Grace timeout: configurable `shutdown_grace_seconds` (default 30s). After grace, tasks are cancelled.

## 13. Testing strategy

- **Unit tests per category** (`tests/test_harvester/test_<category>.py`):
  - Mock the FMP SDK methods with deterministic responses.
  - Assert correct call sequence, checkpoint advancement, retry behavior, per-pattern stop conditions.
  - Parameterize the P1–P4 patterns over their representative categories.
- **StateStore tests:** in-memory SQLite, schema migration idempotency, checkpoint upsert semantics, bandwidth-ledger month rollover.
- **BudgetTracker tests:** soft/hard cap behavior, attribution under concurrent categories (uses a fake `FMPBaseClient` that emits a stream of fake byte counts).
- **SymbolCatalog tests:** discovery, refresh-when-stale, never-refresh-when-fresh, persistence across process restarts.
- **Manager tests:** SIGINT path, grace timeout cancellation, partial-checkpoint persistence on cancel.
- **CLI smoke tests:** `--dry-run` prints expected plan, `--once --category news` runs a single category against mocked SDK and asserts state-store side effects.
- **Optional integration test** (skipped unless `FMP_API_KEY` set): `aiofmp harvest --config tiny.yaml --once --category news` against the real FMP API; assert files appear under a temporary `state_dir`.

Target ≥80% line coverage on the new `aiofmp/harvester/` package.

## 14. Risks & open items

- **Earnings-calendar accuracy for statements discovery.** Filings released without an earnings call may be missed by the P1 incremental flow. Mitigated by the monthly safety-net sweep (Section 6).
- **Global walks fan out into per-entity shards.** Insider trades and form 13F are walked globally but stored per-symbol/per-CIK. A user querying the "global" stream via the SDK will get the passthrough live response; the harvester's per-entity shards are the cache. This is by design but worth a comment in the registry.
- **PAGE_WALK is harvester-write-only.** Documented explicitly in the registry and in the user-facing docs for `CachedClient`.
- **Byte counting is approximate.** Acceptable for soft/hard cap decisions; not suitable for FMP-side billing reconciliation.
- **Concurrency.** Up to N category tasks fight for the shared `FmpClient` semaphore (default `max_concurrent_requests = 10`). If this turns out to be too aggressive, lower it via `FmpClient(max_concurrent_requests=...)` exposed through config in a follow-up.
- **Stop-vs-finish under load.** Categories with very long cycles (initial full sweep) may not respect `stop_event` quickly. The cooperative cancellation contract is: check `stop_event` between symbols, not within a single SDK call. Grace timeout escalates to `CancelledError`.

## 15. Open extension points (deferred, not v1)

- Multi-tier symbol watchlists (tier1 = full harvest, tier2 = statements only, etc.).
- HTTP server exposing `/healthz` and `/metrics`.
- Form 13F per-CIK extract auto-harvest.
- Live structured logging (JSONL to disk).
- Resume-from-checkpoint inside a single cycle (e.g. resume statements sweep at symbol N+1).
