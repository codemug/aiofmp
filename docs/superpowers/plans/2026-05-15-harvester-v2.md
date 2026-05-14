# Harvester v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the long-running `aiofmp harvest` CLI that proactively warms the local Parquet cache via category-specific harvest strategies (P1 discover-then-fill, P2 walk-back-until-checkpoint, P3 gap-fill, P4 snapshot overwrite) to stay under FMP's starter-plan 20 GB/month bandwidth cap.

**Architecture:** A new `aiofmp/harvester/` package with a `HarvesterManager` that spawns one `asyncio.Task` per enabled category. Shared `FmpClient` + `CachedClient`, shared SQLite `StateStore` for checkpoints/bandwidth/symbol-catalogs, shared `BudgetTracker`. P3 categories use the existing `CachedClient` `DATE_RANGE` gap-fill. P1 uses `earnings_calendar` as a discovery probe. P2 needs a new `PAGE_WALK` `TemporalPattern` registered in the existing `CachedClient` registry. P4 uses a thin `SnapshotStore` helper writing single-row parquet under `("snapshot/<endpoint>", entity)`.

**Tech Stack:** Python 3.10+, `aiohttp`, `asyncio`, `click`, `pytest` + `pytest-asyncio`, `pyarrow` (already in), `pyyaml` (new), built-in `sqlite3`.

**Spec:** `docs/superpowers/specs/2026-05-15-harvester-v2-design.md`

**File structure (new files this plan creates):**

```
aiofmp/harvester/
  __init__.py
  cli.py
  manager.py
  config.py
  state.py
  budget.py
  catalog.py
  base.py
  gap_fill_base.py                 (DRY base for P3 categories)
  categories/
    __init__.py
    chart_eod.py
    chart_intraday.py
    commodities_eod.py
    commodities_intraday.py
    forex_eod.py
    forex_intraday.py
    indexes_eod.py
    indexes_intraday.py
    news.py
    economics.py
    technical_indicators.py
    statements.py
    analyst_estimates.py
    analyst_snapshots.py
    insider_trades.py
    form13f.py
    dcf.py

aiofmp/cachedclient/
  snapshot_store.py                (new)

tests/test_harvester/
  __init__.py
  conftest.py
  test_config.py
  test_state.py
  test_budget.py
  test_catalog.py
  test_base.py
  test_manager.py
  test_gap_fill_base.py
  test_chart_eod.py
  test_chart_intraday.py
  test_commodities_eod.py
  test_forex_eod.py
  test_indexes_eod.py
  test_news.py
  test_economics.py
  test_technical_indicators.py
  test_statements.py
  test_analyst_estimates.py
  test_analyst_snapshots.py
  test_insider_trades.py
  test_form13f.py
  test_dcf.py
  test_cli.py

tests/test_cachedclient/
  test_snapshot_store.py           (new)
  test_page_walk_registry.py       (new)
```

**Files modified (existing):**

- `pyproject.toml` — add `pyyaml` dependency
- `aiofmp/base.py` — `FMPBudgetError`, `on_response_size` callback, harvester-category `ContextVar`
- `aiofmp/cachedclient/gap.py` — no changes (already done)
- `aiofmp/cachedclient/registry.py` — `TemporalPattern.PAGE_WALK`, new `CacheableEndpoint` fields, register PAGE_WALK endpoints, register chart endpoints under `commodity`/`forex`/`indexes` categories
- `aiofmp/cachedclient/proxy.py` — read-only handling for `PAGE_WALK` keys
- `aiofmp/cli.py` — wire `harvest` and `harvest-status` subcommands
- `aiofmp/__init__.py` — re-export `FMPBudgetError`

**Conventions used throughout this plan:**

- Tests use `pytest` + `pytest-asyncio` with class-based grouping (matches existing `tests/test_cachedclient/test_gap.py`).
- Async fixtures use the `async def` form with `pytest_asyncio.fixture`.
- `asyncio_mode = "auto"` is set globally in `pyproject.toml` already, so test functions can be `async def` without decorators.
- File timestamps: UTC, ISO-8601 (`datetime.now(UTC).isoformat()`).
- Run commands assume `uv run` is the test runner.
- Each commit message uses Conventional Commits (`feat(harvester): ...`, `test(harvester): ...`, `chore: ...`) per the repo's release automation.

---

## Phase 0 — Setup

### Task 1: Add `pyyaml` dependency

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Add `pyyaml` to dependencies**

In `pyproject.toml` under `[project] dependencies = [...]`, add `"pyyaml>=6.0"`. The list should look like:

```toml
dependencies = [
    "aiohttp>=3.12.15",
    "fastmcp>=2.0.0",
    "click>=8.0.0",
    "pyarrow>=14.0.0",
    "pyyaml>=6.0",
    "pytest>=8.4.1",
    "pytest-asyncio>=1.1.0",
    "pytest-cov>=5.0.0",
    "ruff>=0.13.2",
]
```

- [ ] **Step 2: Sync the lockfile**

Run: `uv sync`
Expected: `uv` resolves and installs `pyyaml`. No error.

- [ ] **Step 3: Verify import**

Run: `uv run python -c "import yaml; print(yaml.__version__)"`
Expected: prints a 6.x version, no traceback.

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml uv.lock
git commit -m "chore(harvester): add pyyaml dependency"
```

---

### Task 2: Skeleton package + test directory

**Files:**
- Create: `aiofmp/harvester/__init__.py`
- Create: `aiofmp/harvester/categories/__init__.py`
- Create: `tests/test_harvester/__init__.py`
- Create: `tests/test_harvester/conftest.py`

- [ ] **Step 1: Create `aiofmp/harvester/__init__.py` with public exports placeholder**

```python
"""Harvester — long-running CLI that proactively warms the local Parquet cache."""

__all__: list[str] = []
```

- [ ] **Step 2: Create `aiofmp/harvester/categories/__init__.py`**

```python
"""Category-specific harvester implementations."""
```

- [ ] **Step 3: Create `tests/test_harvester/__init__.py` (empty)**

```python
```

- [ ] **Step 4: Create `tests/test_harvester/conftest.py` with shared fixtures**

```python
"""Shared fixtures for harvester tests."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest_asyncio


@pytest_asyncio.fixture
async def tmp_state_dir(tmp_path: Path) -> Path:
    """Temp directory that mimics the harvester's state_dir layout."""
    state_dir = tmp_path / "aiofmp_cache"
    state_dir.mkdir()
    return state_dir


def utc_now_iso() -> str:
    """Return current UTC time as ISO-8601 string."""
    return datetime.now(UTC).isoformat()
```

- [ ] **Step 5: Verify test discovery**

Run: `uv run pytest tests/test_harvester -q`
Expected: `no tests ran in ...` (no tests yet, no collection errors).

- [ ] **Step 6: Commit**

```bash
git add aiofmp/harvester/__init__.py aiofmp/harvester/categories/__init__.py tests/test_harvester/__init__.py tests/test_harvester/conftest.py
git commit -m "feat(harvester): scaffold harvester package and test dir"
```

---

## Phase 1 — Foundation

### Task 3: Config dataclasses + interval parser

**Files:**
- Create: `aiofmp/harvester/config.py`
- Create: `tests/test_harvester/test_config.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_harvester/test_config.py`:

```python
"""Tests for the harvester config module."""

from __future__ import annotations

import pytest

from aiofmp.harvester.config import (
    BudgetConfig,
    CategoryConfig,
    DiscoveryConfig,
    HarvestConfig,
    RetryConfig,
    parse_interval,
)


class TestParseInterval:
    @pytest.mark.parametrize(
        "spec,expected_seconds",
        [
            ("30s", 30),
            ("5m", 300),
            ("30m", 1800),
            ("1h", 3600),
            ("4h", 14400),
            ("24h", 86400),
            ("1d", 86400),
            ("7d", 604800),
            ("30D", 2592000),  # case-insensitive
        ],
    )
    def test_valid_specs(self, spec: str, expected_seconds: int) -> None:
        assert parse_interval(spec) == expected_seconds

    @pytest.mark.parametrize("spec", ["", "30", "30x", "abc", "30 m", "-5m"])
    def test_invalid_specs(self, spec: str) -> None:
        with pytest.raises(ValueError):
            parse_interval(spec)


class TestHarvestConfig:
    def test_defaults(self) -> None:
        cfg = HarvestConfig()
        assert cfg.state_dir == "~/.aiofmp/cache"
        assert cfg.log_level == "INFO"
        assert cfg.budget.monthly_soft_cap_gb == 18
        assert cfg.budget.monthly_hard_cap_gb == 20
        assert cfg.retry.on_429.backoff_seconds == [60, 120, 240, 480]
        assert cfg.discovery.refresh_interval == "7d"
        assert cfg.categories == {}

    def test_category_config_interval_seconds(self) -> None:
        cc = CategoryConfig(enabled=True, interval="6h", extra={})
        assert cc.interval_seconds == 6 * 3600

    def test_retry_defaults(self) -> None:
        r = RetryConfig()
        assert r.on_429.max_attempts == 4
        assert r.on_5xx.max_attempts == 3
        assert r.on_5xx.backoff_seconds == [10, 30, 60]

    def test_discovery_refresh_seconds(self) -> None:
        d = DiscoveryConfig(refresh_interval="7d")
        assert d.refresh_interval_seconds == 7 * 86400

    def test_budget_defaults(self) -> None:
        b = BudgetConfig()
        assert b.soft_cap_behavior == "pause_until_next_month"
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_config.py -v`
Expected: ImportError — `aiofmp.harvester.config` not found.

- [ ] **Step 3: Create `aiofmp/harvester/config.py`**

```python
"""Harvester configuration dataclasses + YAML schema.

Defines the structured representation of `harvester.yaml` and the
`parse_interval` helper that turns strings like ``"6h"`` into seconds.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

_INTERVAL_RE = re.compile(r"^(\d+)([smhd])$", re.IGNORECASE)
_INTERVAL_UNIT_SECONDS: dict[str, int] = {
    "s": 1,
    "m": 60,
    "h": 3600,
    "d": 86400,
}


def parse_interval(spec: str) -> int:
    """Parse an interval spec like ``"30s"``, ``"5m"``, ``"6h"``, ``"7d"`` into seconds.

    Raises ``ValueError`` for any other input (empty, missing unit, unknown unit, negative).
    """
    if not isinstance(spec, str):
        raise ValueError(f"interval must be a string, got {type(spec).__name__}")
    match = _INTERVAL_RE.match(spec)
    if not match:
        raise ValueError(f"invalid interval spec: {spec!r}")
    n = int(match.group(1))
    unit = match.group(2).lower()
    if n <= 0:
        raise ValueError(f"interval must be positive: {spec!r}")
    return n * _INTERVAL_UNIT_SECONDS[unit]


@dataclass
class RetryPolicy:
    backoff_seconds: list[int]
    max_attempts: int


@dataclass
class RetryConfig:
    on_429: RetryPolicy = field(
        default_factory=lambda: RetryPolicy(backoff_seconds=[60, 120, 240, 480], max_attempts=4)
    )
    on_5xx: RetryPolicy = field(
        default_factory=lambda: RetryPolicy(backoff_seconds=[10, 30, 60], max_attempts=3)
    )


@dataclass
class BudgetConfig:
    monthly_soft_cap_gb: int = 18
    monthly_hard_cap_gb: int = 20
    soft_cap_behavior: str = "pause_until_next_month"  # | "warn_only"


@dataclass
class DiscoveryConfig:
    refresh_interval: str = "7d"

    @property
    def refresh_interval_seconds(self) -> int:
        return parse_interval(self.refresh_interval)


@dataclass
class CategoryConfig:
    """Generic per-category config; specific keys live in ``extra``.

    Common fields (``enabled``, ``interval``) are split out so the manager
    can inspect them without knowing the category. All other YAML keys go
    into ``extra`` and are interpreted by the concrete category harvester.
    """

    enabled: bool
    interval: str
    extra: dict[str, Any]

    @property
    def interval_seconds(self) -> int:
        return parse_interval(self.interval)


@dataclass
class HarvestConfig:
    state_dir: str = "~/.aiofmp/cache"
    log_level: str = "INFO"
    shutdown_grace_seconds: int = 30
    budget: BudgetConfig = field(default_factory=BudgetConfig)
    retry: RetryConfig = field(default_factory=RetryConfig)
    discovery: DiscoveryConfig = field(default_factory=DiscoveryConfig)
    categories: dict[str, CategoryConfig] = field(default_factory=dict)
```

- [ ] **Step 4: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_config.py -v`
Expected: all 12 tests pass.

- [ ] **Step 5: Commit**

```bash
git add aiofmp/harvester/config.py tests/test_harvester/test_config.py
git commit -m "feat(harvester): config dataclasses and interval parser"
```

---

### Task 4: YAML loader for `HarvestConfig`

**Files:**
- Modify: `aiofmp/harvester/config.py`
- Modify: `tests/test_harvester/test_config.py`

- [ ] **Step 1: Append failing tests to `test_config.py`**

Append to `tests/test_harvester/test_config.py`:

```python
from textwrap import dedent

from aiofmp.harvester.config import load_config_from_yaml


class TestLoadConfigFromYaml:
    def test_minimal(self, tmp_path) -> None:
        path = tmp_path / "h.yaml"
        path.write_text("state_dir: /tmp/x\n")
        cfg = load_config_from_yaml(path)
        assert cfg.state_dir == "/tmp/x"
        assert cfg.log_level == "INFO"
        assert cfg.budget.monthly_soft_cap_gb == 18

    def test_full(self, tmp_path) -> None:
        path = tmp_path / "h.yaml"
        path.write_text(dedent("""
            state_dir: /var/aiofmp
            log_level: DEBUG
            budget:
              monthly_soft_cap_gb: 10
              monthly_hard_cap_gb: 12
              soft_cap_behavior: warn_only
            retry:
              on_429:
                backoff_seconds: [30, 60]
                max_attempts: 2
              on_5xx:
                backoff_seconds: [5]
                max_attempts: 1
            discovery:
              refresh_interval: 3d
            categories:
              statements:
                enabled: true
                interval: 6h
                periods: [annual, quarter]
                initial_limit: 40
              chart_eod:
                enabled: false
                interval: 24h
        """).strip() + "\n")
        cfg = load_config_from_yaml(path)
        assert cfg.state_dir == "/var/aiofmp"
        assert cfg.log_level == "DEBUG"
        assert cfg.budget.monthly_soft_cap_gb == 10
        assert cfg.budget.soft_cap_behavior == "warn_only"
        assert cfg.retry.on_429.backoff_seconds == [30, 60]
        assert cfg.retry.on_429.max_attempts == 2
        assert cfg.discovery.refresh_interval == "3d"
        assert "statements" in cfg.categories
        st = cfg.categories["statements"]
        assert st.enabled is True
        assert st.interval == "6h"
        assert st.extra["periods"] == ["annual", "quarter"]
        assert st.extra["initial_limit"] == 40
        assert cfg.categories["chart_eod"].enabled is False

    def test_missing_file(self, tmp_path) -> None:
        import pytest
        with pytest.raises(FileNotFoundError):
            load_config_from_yaml(tmp_path / "nope.yaml")

    def test_bad_yaml(self, tmp_path) -> None:
        import pytest
        path = tmp_path / "bad.yaml"
        path.write_text("state_dir: [unclosed\n")
        with pytest.raises(ValueError, match="yaml"):
            load_config_from_yaml(path)

    def test_category_missing_required(self, tmp_path) -> None:
        import pytest
        path = tmp_path / "h.yaml"
        path.write_text(dedent("""
            categories:
              statements:
                enabled: true
                # interval missing
        """).strip() + "\n")
        with pytest.raises(ValueError, match="interval"):
            load_config_from_yaml(path)
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_config.py::TestLoadConfigFromYaml -v`
Expected: ImportError — `load_config_from_yaml` not defined.

- [ ] **Step 3: Add `load_config_from_yaml` to `aiofmp/harvester/config.py`**

Append at the bottom of `aiofmp/harvester/config.py`:

```python
import os
from pathlib import Path

import yaml


def _parse_retry_policy(raw: dict[str, Any] | None, default: RetryPolicy) -> RetryPolicy:
    if raw is None:
        return default
    return RetryPolicy(
        backoff_seconds=list(raw.get("backoff_seconds", default.backoff_seconds)),
        max_attempts=int(raw.get("max_attempts", default.max_attempts)),
    )


def _parse_categories(raw: dict[str, Any] | None) -> dict[str, CategoryConfig]:
    if not raw:
        return {}
    out: dict[str, CategoryConfig] = {}
    for name, body in raw.items():
        if not isinstance(body, dict):
            raise ValueError(f"category {name!r} must be a mapping, got {type(body).__name__}")
        if "interval" not in body:
            raise ValueError(f"category {name!r} is missing required field: interval")
        if "enabled" not in body:
            raise ValueError(f"category {name!r} is missing required field: enabled")
        extra = {k: v for k, v in body.items() if k not in ("enabled", "interval")}
        out[name] = CategoryConfig(
            enabled=bool(body["enabled"]),
            interval=str(body["interval"]),
            extra=extra,
        )
        # Validate interval format early
        parse_interval(out[name].interval)
    return out


def load_config_from_yaml(path: str | Path) -> HarvestConfig:
    """Parse a YAML file into a HarvestConfig. Raises FileNotFoundError / ValueError on issues."""
    p = Path(os.path.expanduser(str(path)))
    if not p.exists():
        raise FileNotFoundError(f"config file not found: {p}")
    try:
        with open(p, encoding="utf-8") as fh:
            raw = yaml.safe_load(fh) or {}
    except yaml.YAMLError as e:
        raise ValueError(f"yaml parse error: {e}") from e

    defaults = HarvestConfig()

    budget_raw = raw.get("budget") or {}
    budget = BudgetConfig(
        monthly_soft_cap_gb=int(budget_raw.get("monthly_soft_cap_gb", defaults.budget.monthly_soft_cap_gb)),
        monthly_hard_cap_gb=int(budget_raw.get("monthly_hard_cap_gb", defaults.budget.monthly_hard_cap_gb)),
        soft_cap_behavior=str(budget_raw.get("soft_cap_behavior", defaults.budget.soft_cap_behavior)),
    )

    retry_raw = raw.get("retry") or {}
    retry = RetryConfig(
        on_429=_parse_retry_policy(retry_raw.get("on_429"), defaults.retry.on_429),
        on_5xx=_parse_retry_policy(retry_raw.get("on_5xx"), defaults.retry.on_5xx),
    )

    discovery_raw = raw.get("discovery") or {}
    discovery = DiscoveryConfig(
        refresh_interval=str(discovery_raw.get("refresh_interval", defaults.discovery.refresh_interval)),
    )
    # Validate discovery interval early
    parse_interval(discovery.refresh_interval)

    return HarvestConfig(
        state_dir=str(raw.get("state_dir", defaults.state_dir)),
        log_level=str(raw.get("log_level", defaults.log_level)),
        shutdown_grace_seconds=int(raw.get("shutdown_grace_seconds", defaults.shutdown_grace_seconds)),
        budget=budget,
        retry=retry,
        discovery=discovery,
        categories=_parse_categories(raw.get("categories")),
    )
```

- [ ] **Step 4: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_config.py -v`
Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add aiofmp/harvester/config.py tests/test_harvester/test_config.py
git commit -m "feat(harvester): YAML loader for HarvestConfig"
```

---

### Task 5: StateStore (SQLite schema + CRUD)

**Files:**
- Create: `aiofmp/harvester/state.py`
- Create: `tests/test_harvester/test_state.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_harvester/test_state.py`:

```python
"""Tests for the harvester state store."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from aiofmp.harvester.state import RunStatus, StateStore


@pytest.fixture
def store(tmp_path: Path) -> StateStore:
    s = StateStore(tmp_path / "harvester.sqlite")
    s.initialize()
    return s


class TestSchema:
    def test_initialize_idempotent(self, tmp_path: Path) -> None:
        path = tmp_path / "harvester.sqlite"
        StateStore(path).initialize()
        StateStore(path).initialize()  # must not error
        assert path.exists()


class TestCategoryRuns:
    def test_record_run_lifecycle(self, store: StateStore) -> None:
        started = datetime.now(UTC)
        store.record_run_start("statements", started)
        store.record_run_finish(
            "statements",
            started,
            status=RunStatus.OK,
            items_attempted=10,
            items_succeeded=10,
            bytes_estimate=1024,
        )
        latest = store.get_latest_run("statements")
        assert latest is not None
        assert latest.status == RunStatus.OK
        assert latest.items_attempted == 10
        assert latest.items_succeeded == 10
        assert latest.bytes_estimate == 1024

    def test_get_latest_run_none(self, store: StateStore) -> None:
        assert store.get_latest_run("never_ran") is None


class TestCheckpoints:
    def test_upsert_and_get(self, store: StateStore) -> None:
        store.set_checkpoint("statements", "AAPL", "2024-12-31")
        assert store.get_checkpoint("statements", "AAPL") == "2024-12-31"
        store.set_checkpoint("statements", "AAPL", "2025-01-15")
        assert store.get_checkpoint("statements", "AAPL") == "2025-01-15"

    def test_missing_checkpoint(self, store: StateStore) -> None:
        assert store.get_checkpoint("statements", "MSFT") is None


class TestSymbolCatalog:
    def test_upsert_and_list(self, store: StateStore) -> None:
        store.upsert_symbol("financial_symbols", "AAPL", {"name": "Apple"})
        store.upsert_symbol("financial_symbols", "MSFT", {"name": "Microsoft"})
        symbols = store.list_symbols("financial_symbols")
        assert set(symbols) == {"AAPL", "MSFT"}

    def test_replace_universe(self, store: StateStore) -> None:
        store.upsert_symbol("commodities", "GCUSD", {})
        store.replace_universe("commodities", [("CLUSD", {}), ("SIUSD", {})])
        assert set(store.list_symbols("commodities")) == {"CLUSD", "SIUSD"}

    def test_refresh_timestamp(self, store: StateStore) -> None:
        assert store.get_last_refresh("indexes") is None
        ts = datetime.now(UTC)
        store.set_last_refresh("indexes", ts)
        got = store.get_last_refresh("indexes")
        assert got is not None
        assert abs((got - ts).total_seconds()) < 1


class TestBandwidthLedger:
    def test_add_and_get(self, store: StateStore) -> None:
        store.add_bytes("2026-05", "statements", 1024)
        store.add_bytes("2026-05", "statements", 2048)
        store.add_bytes("2026-05", "news", 512)
        store.add_bytes("2026-04", "statements", 9999)
        assert store.get_month_bytes("2026-05") == 1024 + 2048 + 512
        assert store.get_category_month_bytes("2026-05", "statements") == 3072
        assert store.get_month_bytes("2026-04") == 9999
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_state.py -v`
Expected: ImportError — `aiofmp.harvester.state` missing.

- [ ] **Step 3: Create `aiofmp/harvester/state.py`**

```python
"""SQLite-backed state store for the harvester.

Holds:
  - category_runs:   per-cycle bookkeeping
  - checkpoints:     last-seen-date per (category, scope)
  - symbol_catalog:  cached symbol universes
  - catalog_refresh: when each universe was last refreshed
  - bandwidth_ledger: bytes consumed per (month, category)

Schema migrations are linear and idempotent; tracked via PRAGMA user_version.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1


class RunStatus(str, Enum):
    RUNNING = "running"
    OK = "ok"
    PARTIAL = "partial"
    ERROR = "error"
    PAUSED_FOR_BUDGET = "paused_for_budget"


@dataclass(frozen=True)
class CategoryRun:
    category: str
    started_at: str
    finished_at: str | None
    status: RunStatus
    items_attempted: int
    items_succeeded: int
    bytes_estimate: int
    error: str | None


class StateStore:
    """Thin synchronous wrapper around a single SQLite file.

    All methods are synchronous. Callers running inside asyncio loops should
    wrap hot paths with ``asyncio.to_thread`` if blocking becomes a concern.
    In practice the harvester's state writes are sub-millisecond.
    """

    def __init__(self, path: Path | str) -> None:
        self._path = Path(path)

    def initialize(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("PRAGMA user_version")
            current_version = cur.fetchone()[0]
            if current_version < 1:
                self._apply_v1(conn)
                conn.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
            conn.commit()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _apply_v1(self, conn: sqlite3.Connection) -> None:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS category_runs (
              category TEXT NOT NULL,
              started_at TEXT NOT NULL,
              finished_at TEXT,
              status TEXT NOT NULL,
              items_attempted INTEGER NOT NULL DEFAULT 0,
              items_succeeded INTEGER NOT NULL DEFAULT 0,
              bytes_estimate INTEGER NOT NULL DEFAULT 0,
              error TEXT,
              PRIMARY KEY (category, started_at)
            );
            CREATE INDEX IF NOT EXISTS idx_category_runs_started
              ON category_runs(category, started_at DESC);

            CREATE TABLE IF NOT EXISTS checkpoints (
              category TEXT NOT NULL,
              scope TEXT NOT NULL,
              checkpoint TEXT NOT NULL,
              updated_at TEXT NOT NULL,
              PRIMARY KEY (category, scope)
            );

            CREATE TABLE IF NOT EXISTS symbol_catalog (
              universe TEXT NOT NULL,
              symbol TEXT NOT NULL,
              payload_json TEXT,
              discovered_at TEXT NOT NULL,
              PRIMARY KEY (universe, symbol)
            );

            CREATE TABLE IF NOT EXISTS catalog_refresh (
              universe TEXT PRIMARY KEY,
              last_refreshed_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS bandwidth_ledger (
              month TEXT NOT NULL,
              category TEXT NOT NULL,
              bytes INTEGER NOT NULL DEFAULT 0,
              PRIMARY KEY (month, category)
            );
            """
        )

    # ----- category_runs -----

    def record_run_start(self, category: str, started_at: datetime) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO category_runs (category, started_at, status) VALUES (?, ?, ?)",
                (category, started_at.isoformat(), RunStatus.RUNNING.value),
            )
            conn.commit()

    def record_run_finish(
        self,
        category: str,
        started_at: datetime,
        *,
        status: RunStatus,
        items_attempted: int = 0,
        items_succeeded: int = 0,
        bytes_estimate: int = 0,
        error: str | None = None,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE category_runs
                   SET finished_at = ?,
                       status = ?,
                       items_attempted = ?,
                       items_succeeded = ?,
                       bytes_estimate = ?,
                       error = ?
                 WHERE category = ? AND started_at = ?
                """,
                (
                    datetime.now(UTC).isoformat(),
                    status.value,
                    items_attempted,
                    items_succeeded,
                    bytes_estimate,
                    error,
                    category,
                    started_at.isoformat(),
                ),
            )
            conn.commit()

    def get_latest_run(self, category: str) -> CategoryRun | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM category_runs WHERE category = ? ORDER BY started_at DESC LIMIT 1",
                (category,),
            ).fetchone()
            if row is None:
                return None
            return CategoryRun(
                category=row["category"],
                started_at=row["started_at"],
                finished_at=row["finished_at"],
                status=RunStatus(row["status"]),
                items_attempted=row["items_attempted"],
                items_succeeded=row["items_succeeded"],
                bytes_estimate=row["bytes_estimate"],
                error=row["error"],
            )

    # ----- checkpoints -----

    def set_checkpoint(self, category: str, scope: str, checkpoint: str) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO checkpoints (category, scope, checkpoint, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(category, scope) DO UPDATE SET
                  checkpoint = excluded.checkpoint,
                  updated_at = excluded.updated_at
                """,
                (category, scope, checkpoint, datetime.now(UTC).isoformat()),
            )
            conn.commit()

    def get_checkpoint(self, category: str, scope: str) -> str | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT checkpoint FROM checkpoints WHERE category = ? AND scope = ?",
                (category, scope),
            ).fetchone()
            return row["checkpoint"] if row else None

    # ----- symbol_catalog -----

    def upsert_symbol(self, universe: str, symbol: str, payload: dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO symbol_catalog (universe, symbol, payload_json, discovered_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(universe, symbol) DO UPDATE SET
                  payload_json = excluded.payload_json
                """,
                (universe, symbol, json.dumps(payload), datetime.now(UTC).isoformat()),
            )
            conn.commit()

    def replace_universe(self, universe: str, symbols: list[tuple[str, dict[str, Any]]]) -> None:
        """Atomically replace all symbols for a universe."""
        with self._connect() as conn:
            conn.execute("DELETE FROM symbol_catalog WHERE universe = ?", (universe,))
            now_iso = datetime.now(UTC).isoformat()
            conn.executemany(
                """
                INSERT INTO symbol_catalog (universe, symbol, payload_json, discovered_at)
                VALUES (?, ?, ?, ?)
                """,
                [(universe, sym, json.dumps(p), now_iso) for sym, p in symbols],
            )
            conn.commit()

    def list_symbols(self, universe: str) -> list[str]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT symbol FROM symbol_catalog WHERE universe = ? ORDER BY symbol",
                (universe,),
            ).fetchall()
            return [r["symbol"] for r in rows]

    def set_last_refresh(self, universe: str, when: datetime) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO catalog_refresh (universe, last_refreshed_at)
                VALUES (?, ?)
                ON CONFLICT(universe) DO UPDATE SET last_refreshed_at = excluded.last_refreshed_at
                """,
                (universe, when.isoformat()),
            )
            conn.commit()

    def get_last_refresh(self, universe: str) -> datetime | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT last_refreshed_at FROM catalog_refresh WHERE universe = ?",
                (universe,),
            ).fetchone()
            if row is None:
                return None
            return datetime.fromisoformat(row["last_refreshed_at"])

    # ----- bandwidth ledger -----

    def add_bytes(self, month: str, category: str, n_bytes: int) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO bandwidth_ledger (month, category, bytes)
                VALUES (?, ?, ?)
                ON CONFLICT(month, category) DO UPDATE SET bytes = bytes + excluded.bytes
                """,
                (month, category, n_bytes),
            )
            conn.commit()

    def get_month_bytes(self, month: str) -> int:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT COALESCE(SUM(bytes), 0) AS total FROM bandwidth_ledger WHERE month = ?",
                (month,),
            ).fetchone()
            return int(row["total"])

    def get_category_month_bytes(self, month: str, category: str) -> int:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT bytes FROM bandwidth_ledger WHERE month = ? AND category = ?",
                (month, category),
            ).fetchone()
            return int(row["bytes"]) if row else 0
```

- [ ] **Step 4: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_state.py -v`
Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add aiofmp/harvester/state.py tests/test_harvester/test_state.py
git commit -m "feat(harvester): SQLite state store with schema migrations"
```

---

### Task 6: Bandwidth callback + `FMPBudgetError` in base client

**Files:**
- Modify: `aiofmp/base.py`
- Modify: `aiofmp/__init__.py`
- Create: `tests/test_harvester/test_base_client_hooks.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_harvester/test_base_client_hooks.py`:

```python
"""Tests for the FMPBaseClient bandwidth hook and FMPBudgetError."""

from __future__ import annotations

import asyncio
import contextvars
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from aiofmp.base import (
    FMPBaseClient,
    FMPBudgetError,
    FMPError,
    current_harvest_category,
)


def test_fmp_budget_error_is_fmp_error_subclass() -> None:
    assert issubclass(FMPBudgetError, FMPError)


def test_current_harvest_category_default_none() -> None:
    assert current_harvest_category.get() is None


@pytest.mark.asyncio
async def test_on_response_size_callback_invoked() -> None:
    """When a callback is set, the client invokes it with category + byte count."""
    captured: list[tuple[str | None, int]] = []

    def callback(category: str | None, byte_count: int) -> None:
        captured.append((category, byte_count))

    client = FMPBaseClient(api_key="test_key")
    client.on_response_size = callback

    body = b'{"data": "abcdefg"}'
    fake_resp = MagicMock()
    fake_resp.status = 200
    fake_resp.read = AsyncMock(return_value=body)

    token = current_harvest_category.set("statements")
    try:
        result = await client._handle_response(fake_resp)
    finally:
        current_harvest_category.reset(token)

    assert result == {"data": "abcdefg"}
    assert len(captured) == 1
    assert captured[0][0] == "statements"
    assert captured[0][1] == len(body)


@pytest.mark.asyncio
async def test_on_response_size_none_category_when_unset() -> None:
    captured: list[tuple[str | None, int]] = []
    client = FMPBaseClient(api_key="test_key")
    client.on_response_size = lambda cat, n: captured.append((cat, n))

    fake_resp = MagicMock()
    fake_resp.status = 200
    fake_resp.read = AsyncMock(return_value=b'{"x": 1}')
    fake_resp.json = AsyncMock(return_value={"x": 1})

    await client._handle_response(fake_resp)

    assert captured[0][0] is None  # no ContextVar set


@pytest.mark.asyncio
async def test_callback_exceptions_are_logged_not_raised() -> None:
    """A misbehaving callback must not break API calls."""
    client = FMPBaseClient(api_key="test_key")

    def bad_callback(category: str | None, byte_count: int) -> None:
        raise RuntimeError("boom")

    client.on_response_size = bad_callback

    fake_resp = MagicMock()
    fake_resp.status = 200
    fake_resp.read = AsyncMock(return_value=b"{}")
    fake_resp.json = AsyncMock(return_value={})

    # Should not raise
    result = await client._handle_response(fake_resp)
    assert result == {}
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_base_client_hooks.py -v`
Expected: ImportError — `FMPBudgetError` / `current_harvest_category` not defined.

- [ ] **Step 3: Modify `aiofmp/base.py`**

At the top of `aiofmp/base.py`, add imports and the new exports:

```python
import asyncio
import contextvars
import logging
from collections.abc import Callable
from typing import Any
from urllib.parse import urlencode

import aiohttp
```

Below the existing `FMPResponseError` class, add `FMPBudgetError`:

```python
class FMPBudgetError(FMPError):
    """Raised when the harvester's monthly hard bandwidth cap is exceeded."""

    pass
```

Just before the `class FMPBaseClient:` line, add the `ContextVar`:

```python
current_harvest_category: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "current_harvest_category", default=None
)
```

In `FMPBaseClient.__init__`, add a public attribute:

```python
# Append after self._request_semaphore line
self.on_response_size: Callable[[str | None, int], None] | None = None
```

Modify `_handle_response` to read the body via `read()`, compute byte count, invoke the callback, then JSON-decode:

```python
async def _handle_response(self, response: aiohttp.ClientResponse) -> Any:
    if response.status == 200:
        try:
            raw = await response.read()
            byte_count = len(raw)
            cb = self.on_response_size
            if cb is not None:
                try:
                    cb(current_harvest_category.get(), byte_count)
                except Exception:
                    logger.exception("on_response_size callback raised; ignoring")

            import json  # local import keeps top of file unchanged
            data = json.loads(raw) if raw else None

            if isinstance(data, dict) and "Error Message" in data:
                raise FMPResponseError(f"API Error: {data['Error Message']}")
            return data
        except FMPError:
            raise
        except Exception as e:
            raise FMPError(f"Failed to parse response: {e}") from e

    elif response.status == 401:
        raise FMPAuthenticationError("Invalid API key or authentication failed")
    elif response.status == 429:
        raise FMPRateLimitError("Rate limit exceeded")
    elif response.status >= 500:
        raise FMPError(f"Server error: {response.status}")
    else:
        raise FMPError(f"HTTP {response.status}: {response.reason}")
```

- [ ] **Step 4: Re-export from `aiofmp/__init__.py`**

In `aiofmp/__init__.py`, update the imports from `.base`:

```python
from .base import (
    FMPAuthenticationError,
    FMPBaseClient,
    FMPBudgetError,
    FMPError,
    FMPRateLimitError,
    FMPResponseError,
    current_harvest_category,
)
```

And add to `__all__`:

```python
__all__ = [
    "FmpClient",
    "FMPError",
    "FMPAuthenticationError",
    "FMPRateLimitError",
    "FMPResponseError",
    "FMPBudgetError",
]
```

- [ ] **Step 5: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_base_client_hooks.py -v`
Expected: all 5 tests pass.

- [ ] **Step 6: Re-run existing tests to confirm no regression**

Run: `uv run pytest tests/test_cachedclient tests/test_search.py -q`
Expected: existing tests still pass.

- [ ] **Step 7: Commit**

```bash
git add aiofmp/base.py aiofmp/__init__.py tests/test_harvester/test_base_client_hooks.py
git commit -m "feat(harvester): on_response_size hook, current_harvest_category contextvar, FMPBudgetError"
```

---

### Task 7: BudgetTracker

**Files:**
- Create: `aiofmp/harvester/budget.py`
- Create: `tests/test_harvester/test_budget.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_harvester/test_budget.py`:

```python
"""Tests for the harvester budget tracker."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from aiofmp.base import FMPBudgetError, current_harvest_category
from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.config import BudgetConfig
from aiofmp.harvester.state import StateStore

GB = 1024 ** 3


@pytest.fixture
def store(tmp_path: Path) -> StateStore:
    s = StateStore(tmp_path / "h.sqlite")
    s.initialize()
    return s


def test_record_bytes_attributes_to_current_category(store: StateStore) -> None:
    tracker = BudgetTracker(store, BudgetConfig())
    token = current_harvest_category.set("statements")
    try:
        tracker.record_bytes(category=current_harvest_category.get(), byte_count=1024)
    finally:
        current_harvest_category.reset(token)
    month = datetime.now(UTC).strftime("%Y-%m")
    assert store.get_category_month_bytes(month, "statements") == 1024


def test_record_bytes_none_category_attributed_to_user(store: StateStore) -> None:
    tracker = BudgetTracker(store, BudgetConfig())
    tracker.record_bytes(category=None, byte_count=512)
    month = datetime.now(UTC).strftime("%Y-%m")
    assert store.get_category_month_bytes(month, "user") == 512


def test_is_paused_below_soft_cap(store: StateStore) -> None:
    tracker = BudgetTracker(store, BudgetConfig(monthly_soft_cap_gb=18))
    assert tracker.is_paused("statements") is False


def test_is_paused_at_soft_cap(store: StateStore) -> None:
    cfg = BudgetConfig(monthly_soft_cap_gb=1, monthly_hard_cap_gb=2)
    tracker = BudgetTracker(store, cfg)
    tracker.record_bytes(category="statements", byte_count=1 * GB)
    assert tracker.is_paused("statements") is True


def test_is_paused_warn_only(store: StateStore) -> None:
    cfg = BudgetConfig(monthly_soft_cap_gb=1, monthly_hard_cap_gb=2, soft_cap_behavior="warn_only")
    tracker = BudgetTracker(store, cfg)
    tracker.record_bytes(category="statements", byte_count=1 * GB)
    assert tracker.is_paused("statements") is False  # warn only — never pauses


def test_check_hard_cap_raises(store: StateStore) -> None:
    cfg = BudgetConfig(monthly_soft_cap_gb=1, monthly_hard_cap_gb=2)
    tracker = BudgetTracker(store, cfg)
    tracker.record_bytes(category="statements", byte_count=2 * GB)
    with pytest.raises(FMPBudgetError, match="hard cap"):
        tracker.check_hard_cap("statements")


def test_check_hard_cap_only_for_harvester_categories(store: StateStore) -> None:
    cfg = BudgetConfig(monthly_soft_cap_gb=1, monthly_hard_cap_gb=2)
    tracker = BudgetTracker(store, cfg)
    tracker.record_bytes(category="user", byte_count=2 * GB)
    # No exception even though hard cap is breached, because category is 'user'
    tracker.check_hard_cap(None)


def test_month_key_format(store: StateStore) -> None:
    tracker = BudgetTracker(store, BudgetConfig())
    key = tracker.current_month_key()
    assert len(key) == 7 and key[4] == "-"
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_budget.py -v`
Expected: ImportError.

- [ ] **Step 3: Create `aiofmp/harvester/budget.py`**

```python
"""Bandwidth budget tracker for the harvester.

Reads/writes the ``bandwidth_ledger`` table in the StateStore. Provides:
  - ``record_bytes(category, byte_count)``: attribute bytes to a category
    (or the synthetic ``"user"`` category when called from user code).
  - ``is_paused(category)``: True if the monthly soft cap is reached and the
    configured behavior is ``pause_until_next_month``.
  - ``check_hard_cap(category)``: raise ``FMPBudgetError`` when the monthly
    hard cap is reached, for harvester-initiated requests only.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime

from aiofmp.base import FMPBudgetError
from aiofmp.harvester.config import BudgetConfig
from aiofmp.harvester.state import StateStore

logger = logging.getLogger(__name__)

GB = 1024 ** 3


class BudgetTracker:
    def __init__(self, store: StateStore, config: BudgetConfig) -> None:
        self._store = store
        self._config = config

    def current_month_key(self) -> str:
        return datetime.now(UTC).strftime("%Y-%m")

    def record_bytes(self, category: str | None, byte_count: int) -> None:
        attribution = category if category else "user"
        self._store.add_bytes(self.current_month_key(), attribution, byte_count)

    def is_paused(self, category: str) -> bool:
        if self._config.soft_cap_behavior != "pause_until_next_month":
            return False
        total = self._store.get_month_bytes(self.current_month_key())
        return total >= self._config.monthly_soft_cap_gb * GB

    def check_hard_cap(self, category: str | None) -> None:
        if category is None or category == "user":
            return
        total = self._store.get_month_bytes(self.current_month_key())
        if total >= self._config.monthly_hard_cap_gb * GB:
            raise FMPBudgetError(
                f"monthly hard cap ({self._config.monthly_hard_cap_gb} GB) reached for "
                f"category {category!r}; total this month: {total / GB:.2f} GB"
            )
```

- [ ] **Step 4: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_budget.py -v`
Expected: all 8 tests pass.

- [ ] **Step 5: Commit**

```bash
git add aiofmp/harvester/budget.py tests/test_harvester/test_budget.py
git commit -m "feat(harvester): BudgetTracker (soft/hard cap, ledger attribution)"
```

---

### Task 8: SymbolCatalog

**Files:**
- Create: `aiofmp/harvester/catalog.py`
- Create: `tests/test_harvester/test_catalog.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_harvester/test_catalog.py`:

```python
"""Tests for the symbol catalog."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.catalog import SymbolCatalog
from aiofmp.harvester.state import StateStore


@pytest.fixture
def store(tmp_path: Path) -> StateStore:
    s = StateStore(tmp_path / "h.sqlite")
    s.initialize()
    return s


def make_fake_fmp() -> MagicMock:
    fmp = MagicMock()
    fmp.directory = MagicMock()
    fmp.directory.financial_symbols = AsyncMock(
        return_value=[{"symbol": "AAPL", "companyName": "Apple"}, {"symbol": "MSFT", "companyName": "MS"}]
    )
    fmp.directory.actively_trading = AsyncMock(
        return_value=[{"symbol": "AAPL"}, {"symbol": "MSFT"}, {"symbol": "TSLA"}]
    )
    fmp.directory.etf_list = AsyncMock(return_value=[{"symbol": "SPY"}])

    fmp.commodity = MagicMock()
    fmp.commodity.commodities_list = AsyncMock(return_value=[{"symbol": "GCUSD"}, {"symbol": "CLUSD"}])

    fmp.forex = MagicMock()
    fmp.forex.forex_list = AsyncMock(return_value=[{"symbol": "EURUSD"}, {"symbol": "GBPUSD"}])

    fmp.indexes = MagicMock()
    fmp.indexes.index_list = AsyncMock(return_value=[{"symbol": "^GSPC"}, {"symbol": "^DJI"}])
    return fmp


class TestSymbolCatalog:
    @pytest.mark.asyncio
    async def test_first_call_discovers(self, store: StateStore) -> None:
        fmp = make_fake_fmp()
        catalog = SymbolCatalog(store, fmp, refresh_interval_seconds=86400)
        result = await catalog.symbols("financial_symbols")
        assert set(result) == {"AAPL", "MSFT"}
        fmp.directory.financial_symbols.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_second_call_uses_cache(self, store: StateStore) -> None:
        fmp = make_fake_fmp()
        catalog = SymbolCatalog(store, fmp, refresh_interval_seconds=86400)
        await catalog.symbols("financial_symbols")
        await catalog.symbols("financial_symbols")
        fmp.directory.financial_symbols.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_stale_cache_triggers_refresh(self, store: StateStore) -> None:
        fmp = make_fake_fmp()
        # 1 second refresh
        catalog = SymbolCatalog(store, fmp, refresh_interval_seconds=1)
        await catalog.symbols("financial_symbols")
        # Forge an old refresh timestamp
        store.set_last_refresh("financial_symbols", datetime.now(UTC) - timedelta(hours=2))
        await catalog.symbols("financial_symbols")
        assert fmp.directory.financial_symbols.await_count == 2

    @pytest.mark.asyncio
    async def test_all_six_universes(self, store: StateStore) -> None:
        fmp = make_fake_fmp()
        catalog = SymbolCatalog(store, fmp, refresh_interval_seconds=86400)
        assert set(await catalog.symbols("financial_symbols")) == {"AAPL", "MSFT"}
        assert set(await catalog.symbols("actively_trading")) == {"AAPL", "MSFT", "TSLA"}
        assert set(await catalog.symbols("commodities")) == {"GCUSD", "CLUSD"}
        assert set(await catalog.symbols("forex_pairs")) == {"EURUSD", "GBPUSD"}
        assert set(await catalog.symbols("indexes")) == {"^GSPC", "^DJI"}
        assert set(await catalog.symbols("etf_list")) == {"SPY"}

    @pytest.mark.asyncio
    async def test_unknown_universe_raises(self, store: StateStore) -> None:
        fmp = make_fake_fmp()
        catalog = SymbolCatalog(store, fmp, refresh_interval_seconds=86400)
        with pytest.raises(ValueError, match="unknown universe"):
            await catalog.symbols("crypto")

    @pytest.mark.asyncio
    async def test_concurrent_refresh_is_single_shot(self, store: StateStore) -> None:
        """Two parallel calls during discovery must result in one API call."""
        import asyncio
        fmp = make_fake_fmp()
        catalog = SymbolCatalog(store, fmp, refresh_interval_seconds=86400)
        await asyncio.gather(
            catalog.symbols("commodities"),
            catalog.symbols("commodities"),
            catalog.symbols("commodities"),
        )
        fmp.commodity.commodities_list.assert_awaited_once()
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_catalog.py -v`
Expected: ImportError.

- [ ] **Step 3: Create `aiofmp/harvester/catalog.py`**

```python
"""Symbol-universe catalog backed by SQLite.

Lazily discovers each universe on first access; refreshes when older
than ``refresh_interval_seconds``. All discovery calls run through the
shared FmpClient (not CachedClient — directory endpoints are not in the
cache registry today).
"""

from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any

from aiofmp.harvester.state import StateStore

logger = logging.getLogger(__name__)

# Maps universe name -> (fmp_client.<category>.<method>, ...)
_UNIVERSE_SPECS: dict[str, tuple[str, str]] = {
    "financial_symbols": ("directory", "financial_symbols"),
    "actively_trading": ("directory", "actively_trading"),
    "etf_list": ("directory", "etf_list"),
    "commodities": ("commodity", "commodities_list"),
    "forex_pairs": ("forex", "forex_list"),
    "indexes": ("indexes", "index_list"),
}


class SymbolCatalog:
    def __init__(self, store: StateStore, fmp_client: Any, refresh_interval_seconds: int) -> None:
        self._store = store
        self._fmp = fmp_client
        self._refresh_seconds = refresh_interval_seconds
        self._locks: dict[str, asyncio.Lock] = {}

    def _lock(self, universe: str) -> asyncio.Lock:
        if universe not in self._locks:
            self._locks[universe] = asyncio.Lock()
        return self._locks[universe]

    async def symbols(self, universe: str) -> list[str]:
        if universe not in _UNIVERSE_SPECS:
            raise ValueError(f"unknown universe: {universe!r}")
        async with self._lock(universe):
            if self._is_stale(universe):
                await self._refresh(universe)
            return self._store.list_symbols(universe)

    def _is_stale(self, universe: str) -> bool:
        last = self._store.get_last_refresh(universe)
        if last is None:
            return True
        age = (datetime.now(UTC) - last).total_seconds()
        return age >= self._refresh_seconds

    async def _refresh(self, universe: str) -> None:
        cat_attr, method_name = _UNIVERSE_SPECS[universe]
        category = getattr(self._fmp, cat_attr)
        method = getattr(category, method_name)
        logger.info("Refreshing symbol universe %s via %s.%s", universe, cat_attr, method_name)
        records = await method()
        if not isinstance(records, list):
            logger.warning("Universe %s returned non-list (%s); keeping prior cache", universe, type(records).__name__)
            return
        rows: list[tuple[str, dict[str, Any]]] = []
        for r in records:
            if not isinstance(r, dict):
                continue
            symbol = r.get("symbol")
            if not symbol:
                continue
            rows.append((str(symbol), r))
        self._store.replace_universe(universe, rows)
        self._store.set_last_refresh(universe, datetime.now(UTC))
        logger.info("Universe %s refreshed: %d symbols", universe, len(rows))
```

- [ ] **Step 4: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_catalog.py -v`
Expected: all 6 tests pass.

- [ ] **Step 5: Commit**

```bash
git add aiofmp/harvester/catalog.py tests/test_harvester/test_catalog.py
git commit -m "feat(harvester): SymbolCatalog with lazy discovery and TTL refresh"
```

---

### Task 9: CategoryHarvester abstract base class

**Files:**
- Create: `aiofmp/harvester/base.py`
- Create: `tests/test_harvester/test_base.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_harvester/test_base.py`:

```python
"""Tests for the CategoryHarvester abstract base class."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

from aiofmp.base import FMPBudgetError, FMPRateLimitError, current_harvest_category
from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig, RetryPolicy
from aiofmp.harvester.state import RunStatus, StateStore


class FakeCategory(CategoryHarvester):
    """Minimal concrete subclass for testing the base class."""

    def __init__(self, name, config, store, budget, retry, *, behavior="ok"):
        super().__init__(name, config, store, budget, retry)
        self.behavior = behavior
        self.run_count = 0
        self.items = 0

    async def run_cycle(self) -> RunOutcome:
        self.run_count += 1
        if self.behavior == "ok":
            self.items += 3
            return RunOutcome(status=RunStatus.OK, items_attempted=3, items_succeeded=3)
        if self.behavior == "raise":
            raise RuntimeError("boom")
        if self.behavior == "429_then_ok":
            if self.run_count == 1:
                raise FMPRateLimitError("rl")
            return RunOutcome(status=RunStatus.OK, items_attempted=1, items_succeeded=1)
        if self.behavior == "always_429":
            raise FMPRateLimitError("rl")
        if self.behavior == "budget":
            raise FMPBudgetError("hard cap")
        raise AssertionError(f"unknown behavior {self.behavior!r}")


@pytest.fixture
def store(tmp_path: Path) -> StateStore:
    s = StateStore(tmp_path / "h.sqlite")
    s.initialize()
    return s


def _make(store: StateStore, behavior: str = "ok"):
    config = CategoryConfig(enabled=True, interval="1s", extra={})
    budget = BudgetTracker(store, BudgetConfig())
    retry = RetryConfig(
        on_429=RetryPolicy(backoff_seconds=[0, 0], max_attempts=2),
        on_5xx=RetryPolicy(backoff_seconds=[0], max_attempts=1),
    )
    return FakeCategory("fake", config, store, budget, retry, behavior=behavior)


class TestCategoryHarvester:
    @pytest.mark.asyncio
    async def test_ok_run_records_state(self, store: StateStore) -> None:
        h = _make(store, "ok")
        await h._run_once_and_record()
        latest = store.get_latest_run("fake")
        assert latest is not None
        assert latest.status == RunStatus.OK
        assert latest.items_attempted == 3
        assert latest.items_succeeded == 3
        assert h.run_count == 1

    @pytest.mark.asyncio
    async def test_exception_marks_error(self, store: StateStore) -> None:
        h = _make(store, "raise")
        await h._run_once_and_record()
        latest = store.get_latest_run("fake")
        assert latest is not None
        assert latest.status == RunStatus.ERROR
        assert latest.error is not None and "boom" in latest.error

    @pytest.mark.asyncio
    async def test_429_then_ok_retries(self, store: StateStore) -> None:
        h = _make(store, "429_then_ok")
        await h._run_once_and_record()
        latest = store.get_latest_run("fake")
        assert latest is not None
        assert latest.status == RunStatus.OK
        assert h.run_count == 2

    @pytest.mark.asyncio
    async def test_always_429_marks_partial(self, store: StateStore) -> None:
        h = _make(store, "always_429")
        await h._run_once_and_record()
        latest = store.get_latest_run("fake")
        assert latest is not None
        assert latest.status == RunStatus.PARTIAL

    @pytest.mark.asyncio
    async def test_budget_error_marks_partial(self, store: StateStore) -> None:
        h = _make(store, "budget")
        await h._run_once_and_record()
        latest = store.get_latest_run("fake")
        assert latest is not None
        assert latest.status == RunStatus.PARTIAL

    @pytest.mark.asyncio
    async def test_sets_contextvar_during_cycle(self, store: StateStore) -> None:
        seen: list[str | None] = []

        class CaptureCategory(FakeCategory):
            async def run_cycle(self) -> RunOutcome:
                seen.append(current_harvest_category.get())
                return RunOutcome(status=RunStatus.OK)

        config = CategoryConfig(enabled=True, interval="1s", extra={})
        budget = BudgetTracker(store, BudgetConfig())
        retry = RetryConfig()
        h = CaptureCategory("fake", config, store, budget, retry)
        await h._run_once_and_record()
        assert seen == ["fake"]
        assert current_harvest_category.get() is None

    @pytest.mark.asyncio
    async def test_paused_category_skips_run(self, store: StateStore) -> None:
        cfg = CategoryConfig(enabled=True, interval="1s", extra={})
        budget_cfg = BudgetConfig(monthly_soft_cap_gb=0, monthly_hard_cap_gb=1)
        budget = BudgetTracker(store, budget_cfg)
        budget.record_bytes("fake", 1)
        retry = RetryConfig()
        h = FakeCategory("fake", cfg, store, budget, retry, behavior="ok")
        await h._run_once_and_record()
        latest = store.get_latest_run("fake")
        assert latest is not None
        assert latest.status == RunStatus.PAUSED_FOR_BUDGET
        assert h.run_count == 0

    @pytest.mark.asyncio
    async def test_run_forever_respects_stop_event(self, store: StateStore) -> None:
        h = _make(store, "ok")
        stop_event = asyncio.Event()
        task = asyncio.create_task(h.run_forever(stop_event))
        await asyncio.sleep(0.05)
        stop_event.set()
        await asyncio.wait_for(task, timeout=2.0)
        assert h.run_count >= 1
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_base.py -v`
Expected: ImportError.

- [ ] **Step 3: Create `aiofmp/harvester/base.py`**

```python
"""CategoryHarvester abstract base class.

Concrete categories override ``run_cycle()`` and return a ``RunOutcome``.
The base class handles the run/sleep loop, retry/backoff for ``FMPRateLimitError``,
state-store bookkeeping, budget pause-before-run, and the ``current_harvest_category``
ContextVar plumbing so byte-counting attributes every request to the right category.
"""

from __future__ import annotations

import abc
import asyncio
import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from aiofmp.base import (
    FMPBudgetError,
    FMPError,
    FMPRateLimitError,
    current_harvest_category,
)
from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.config import CategoryConfig, RetryConfig, RetryPolicy
from aiofmp.harvester.state import RunStatus, StateStore

logger = logging.getLogger(__name__)


@dataclass
class RunOutcome:
    """Result of a single run_cycle() invocation."""

    status: RunStatus
    items_attempted: int = 0
    items_succeeded: int = 0
    bytes_estimate: int = 0
    error: str | None = None


class CategoryHarvester(abc.ABC):
    """Abstract base for one harvester category."""

    def __init__(
        self,
        name: str,
        config: CategoryConfig,
        state: StateStore,
        budget: BudgetTracker,
        retry: RetryConfig,
    ) -> None:
        self.name = name
        self.config = config
        self.state = state
        self.budget = budget
        self.retry = retry

    @abc.abstractmethod
    async def run_cycle(self) -> RunOutcome:
        """Execute one harvest cycle. Must be overridden by subclasses."""
        raise NotImplementedError

    async def run_forever(self, stop_event: asyncio.Event) -> None:
        """Main loop: run a cycle each ``interval_seconds`` until stop_event fires."""
        interval = self.config.interval_seconds
        while not stop_event.is_set():
            await self._run_once_and_record()
            try:
                await asyncio.wait_for(stop_event.wait(), timeout=interval)
            except asyncio.TimeoutError:
                pass

    async def _run_once_and_record(self) -> None:
        """Run one cycle with state bookkeeping and budget checks."""
        started = datetime.now(UTC)
        self.state.record_run_start(self.name, started)

        if self.budget.is_paused(self.name):
            logger.warning("Category %s paused for budget; skipping cycle", self.name)
            self.state.record_run_finish(
                self.name, started, status=RunStatus.PAUSED_FOR_BUDGET
            )
            return

        token = current_harvest_category.set(self.name)
        try:
            outcome = await self._run_cycle_with_retry()
        except Exception as e:
            logger.exception("Unhandled error in %s.run_cycle", self.name)
            self.state.record_run_finish(
                self.name, started, status=RunStatus.ERROR, error=f"{type(e).__name__}: {e}"
            )
            return
        finally:
            current_harvest_category.reset(token)

        self.state.record_run_finish(
            self.name,
            started,
            status=outcome.status,
            items_attempted=outcome.items_attempted,
            items_succeeded=outcome.items_succeeded,
            bytes_estimate=outcome.bytes_estimate,
            error=outcome.error,
        )

    async def _run_cycle_with_retry(self) -> RunOutcome:
        """Wrap a single run_cycle() with the retry/backoff policy for 429."""
        policy: RetryPolicy = self.retry.on_429
        last_exc: BaseException | None = None
        for attempt in range(policy.max_attempts):
            try:
                return await self.run_cycle()
            except FMPRateLimitError as e:
                last_exc = e
                if attempt + 1 >= policy.max_attempts:
                    break
                delay = policy.backoff_seconds[min(attempt, len(policy.backoff_seconds) - 1)]
                logger.warning(
                    "%s hit 429 (attempt %d/%d); sleeping %ds",
                    self.name, attempt + 1, policy.max_attempts, delay,
                )
                if delay > 0:
                    await asyncio.sleep(delay)
            except FMPBudgetError as e:
                logger.warning("%s hit budget hard cap: %s", self.name, e)
                return RunOutcome(status=RunStatus.PARTIAL, error=str(e))
        return RunOutcome(
            status=RunStatus.PARTIAL,
            error=f"rate-limit retries exhausted: {last_exc}",
        )
```

- [ ] **Step 4: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_base.py -v`
Expected: all 8 tests pass.

- [ ] **Step 5: Commit**

```bash
git add aiofmp/harvester/base.py tests/test_harvester/test_base.py
git commit -m "feat(harvester): CategoryHarvester ABC with retry/budget/state plumbing"
```

---

### Task 10: HarvesterManager (lifecycle + signal handling)

**Files:**
- Create: `aiofmp/harvester/manager.py`
- Modify: `aiofmp/harvester/categories/__init__.py`
- Create: `tests/test_harvester/test_manager.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_harvester/test_manager.py`:

```python
"""Tests for HarvesterManager."""

from __future__ import annotations

import asyncio
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.config import (
    CategoryConfig,
    HarvestConfig,
)
from aiofmp.harvester.manager import HarvesterManager
from aiofmp.harvester.state import RunStatus


class CountingCategory(CategoryHarvester):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cycle_count = 0

    async def run_cycle(self) -> RunOutcome:
        self.cycle_count += 1
        return RunOutcome(status=RunStatus.OK, items_attempted=1, items_succeeded=1)


class StuckCategory(CategoryHarvester):
    async def run_cycle(self) -> RunOutcome:
        await asyncio.sleep(60)
        return RunOutcome(status=RunStatus.OK)


@pytest.fixture
def cfg(tmp_path: Path) -> HarvestConfig:
    return HarvestConfig(
        state_dir=str(tmp_path),
        shutdown_grace_seconds=2,
        categories={
            "alpha": CategoryConfig(enabled=True, interval="1s", extra={}),
            "beta": CategoryConfig(enabled=True, interval="1s", extra={}),
            "gamma": CategoryConfig(enabled=False, interval="1s", extra={}),
        },
    )


def _patch_builder(mgr: HarvesterManager, cls: type[CategoryHarvester]) -> dict:
    instances: dict[str, CategoryHarvester] = {}

    def build(name, c):
        if name not in ("alpha", "beta"):
            raise KeyError(name)
        inst = cls(name, c, mgr.state, mgr.budget, mgr.config.retry)
        instances[name] = inst
        return inst

    mgr._build_category = build
    return instances


class TestHarvesterManager:
    @pytest.mark.asyncio
    async def test_spawns_only_enabled(self, cfg: HarvestConfig) -> None:
        mgr = HarvesterManager(cfg, fmp_client=MagicMock(), cached_client=MagicMock())
        _patch_builder(mgr, CountingCategory)
        await mgr.start()
        task = asyncio.create_task(mgr.run_until_stopped())
        await asyncio.sleep(0.05)
        mgr.request_stop()
        await asyncio.wait_for(task, timeout=3.0)
        await mgr.close()
        assert set(mgr._categories.keys()) == {"alpha", "beta"}

    @pytest.mark.asyncio
    async def test_categories_run_concurrently(self, cfg: HarvestConfig) -> None:
        mgr = HarvesterManager(cfg, fmp_client=MagicMock(), cached_client=MagicMock())
        instances = _patch_builder(mgr, CountingCategory)
        await mgr.start()
        task = asyncio.create_task(mgr.run_until_stopped())
        await asyncio.sleep(0.1)
        mgr.request_stop()
        await asyncio.wait_for(task, timeout=3.0)
        await mgr.close()
        assert instances["alpha"].cycle_count >= 1
        assert instances["beta"].cycle_count >= 1

    @pytest.mark.asyncio
    async def test_stop_event_finishes_cleanly(self, cfg: HarvestConfig) -> None:
        mgr = HarvesterManager(cfg, fmp_client=MagicMock(), cached_client=MagicMock())
        _patch_builder(mgr, CountingCategory)
        await mgr.start()
        task = asyncio.create_task(mgr.run_until_stopped())
        mgr.request_stop()
        await asyncio.wait_for(task, timeout=cfg.shutdown_grace_seconds + 2)
        await mgr.close()

    @pytest.mark.asyncio
    async def test_grace_timeout_cancels(self, cfg: HarvestConfig) -> None:
        cfg.shutdown_grace_seconds = 1
        mgr = HarvesterManager(cfg, fmp_client=MagicMock(), cached_client=MagicMock())
        _patch_builder(mgr, StuckCategory)
        await mgr.start()
        task = asyncio.create_task(mgr.run_until_stopped())
        await asyncio.sleep(0.05)
        mgr.request_stop()
        await asyncio.wait_for(task, timeout=4.0)
        await mgr.close()

    @pytest.mark.asyncio
    async def test_unknown_category_in_config_skipped(self, cfg: HarvestConfig) -> None:
        cfg.categories["nonexistent"] = CategoryConfig(enabled=True, interval="1s", extra={})
        mgr = HarvesterManager(cfg, fmp_client=MagicMock(), cached_client=MagicMock())
        _patch_builder(mgr, CountingCategory)
        await mgr.start()
        assert "nonexistent" not in mgr._categories
        await mgr.close()
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_manager.py -v`
Expected: ImportError.

- [ ] **Step 3: Replace `aiofmp/harvester/categories/__init__.py`**

Overwrite with a registry binding:

```python
"""Category-specific harvester implementations.

Concrete category modules call ``register_category(name, factory)`` at import
time. ``build_category(name, cfg, manager)`` then dispatches via the registry.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiofmp.harvester.base import CategoryHarvester
    from aiofmp.harvester.config import CategoryConfig
    from aiofmp.harvester.manager import HarvesterManager

CategoryFactory = Callable[..., "CategoryHarvester"]

_REGISTRY: dict[str, CategoryFactory] = {}


def register_category(name: str, factory: CategoryFactory) -> None:
    _REGISTRY[name] = factory


def build_category(name: str, cfg: "CategoryConfig", manager: "HarvesterManager") -> "CategoryHarvester":
    if name not in _REGISTRY:
        raise KeyError(name)
    return _REGISTRY[name](cfg, manager)


def registered_names() -> list[str]:
    return sorted(_REGISTRY.keys())
```

- [ ] **Step 4: Create `aiofmp/harvester/manager.py`**

```python
"""HarvesterManager — orchestrates category tasks and lifecycle."""

from __future__ import annotations

import asyncio
import logging
import os
import signal
from pathlib import Path
from typing import Any

from aiofmp.harvester.base import CategoryHarvester
from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.catalog import SymbolCatalog
from aiofmp.harvester.config import CategoryConfig, HarvestConfig
from aiofmp.harvester.state import StateStore

logger = logging.getLogger(__name__)


class HarvesterManager:
    """Loads enabled categories, runs them as concurrent asyncio tasks until stopped."""

    def __init__(self, config: HarvestConfig, fmp_client: Any, cached_client: Any) -> None:
        self.config = config
        self.fmp_client = fmp_client
        self.cached_client = cached_client

        state_dir = Path(os.path.expanduser(config.state_dir))
        state_dir.mkdir(parents=True, exist_ok=True)
        self.state = StateStore(state_dir / "harvester.sqlite")
        self.state.initialize()

        self.budget = BudgetTracker(self.state, config.budget)
        self.catalog = SymbolCatalog(
            self.state, fmp_client, config.discovery.refresh_interval_seconds
        )

        self._stop_event = asyncio.Event()
        self._categories: dict[str, CategoryHarvester] = {}
        self._tasks: list[asyncio.Task[None]] = []

    async def start(self) -> None:
        """Construct enabled category harvesters. Does not start tasks."""
        for name, cat_cfg in self.config.categories.items():
            if not cat_cfg.enabled:
                logger.info("Category %s is disabled; skipping", name)
                continue
            try:
                self._categories[name] = self._build_category(name, cat_cfg)
            except KeyError:
                logger.warning("Unknown category in config: %s (skipping)", name)

    def _build_category(self, name: str, cat_cfg: CategoryConfig) -> CategoryHarvester:
        from aiofmp.harvester.categories import build_category
        return build_category(name, cat_cfg, self)

    def request_stop(self) -> None:
        self._stop_event.set()

    def install_signal_handlers(self) -> None:
        loop = asyncio.get_event_loop()
        try:
            loop.add_signal_handler(signal.SIGINT, self.request_stop)
            loop.add_signal_handler(signal.SIGTERM, self.request_stop)
        except NotImplementedError:
            signal.signal(signal.SIGINT, lambda *_: self.request_stop())

    async def run_until_stopped(self) -> None:
        if not self._categories:
            logger.warning("No enabled categories; manager will idle until stop_event.")
            await self._stop_event.wait()
            return

        for name, cat in self._categories.items():
            self._tasks.append(
                asyncio.create_task(cat.run_forever(self._stop_event), name=f"harvester:{name}")
            )
        await self._stop_event.wait()

        logger.info("Stop requested; waiting for %d categor(y/ies) (grace %ds)",
                    len(self._tasks), self.config.shutdown_grace_seconds)
        done, pending = await asyncio.wait(
            self._tasks, timeout=self.config.shutdown_grace_seconds
        )
        if pending:
            logger.warning("%d task(s) did not stop within grace; cancelling", len(pending))
            for t in pending:
                t.cancel()
            await asyncio.gather(*pending, return_exceptions=True)

    async def close(self) -> None:
        return None
```

- [ ] **Step 5: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_manager.py -v`
Expected: all 5 tests pass.

- [ ] **Step 6: Commit**

```bash
git add aiofmp/harvester/manager.py aiofmp/harvester/categories/__init__.py tests/test_harvester/test_manager.py
git commit -m "feat(harvester): HarvesterManager lifecycle and signal handling"
```

---

## Phase 2 — CachedClient extensions

### Task 11: `TemporalPattern.PAGE_WALK` + supporting registry fields

**Files:**
- Modify: `aiofmp/cachedclient/registry.py`
- Modify: `aiofmp/cachedclient/proxy.py`
- Create: `tests/test_cachedclient/test_page_walk_registry.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_cachedclient/test_page_walk_registry.py`:

```python
"""Tests for the PAGE_WALK pattern in the cached client registry."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

from aiofmp.cachedclient.proxy import CachedCategoryProxy
from aiofmp.cachedclient.registry import (
    CacheableEndpoint,
    EndpointRegistry,
    TemporalPattern,
    build_default_registry,
)
from aiofmp.cachedclient.storage.parquet import ParquetStorage


def test_temporal_pattern_page_walk_exists() -> None:
    assert TemporalPattern.PAGE_WALK.value == "page_walk"


def test_page_walk_endpoint_fields() -> None:
    ep = CacheableEndpoint(
        category="analyst",
        method="financial_estimates",
        api_endpoint="analyst-estimates",
        pattern=TemporalPattern.PAGE_WALK,
        entity_key_args=["symbol"],
        extra_key_args=["period"],
        page_param="page",
        default_page_size=100,
        walk_date_field="date",
        call_params=["symbol", "period", "page", "limit"],
    )
    assert ep.page_param == "page"
    assert ep.default_page_size == 100
    assert ep.walk_date_field == "date"


def test_default_registry_includes_page_walk_endpoints() -> None:
    reg = build_default_registry()
    # The harvester adds these in a later task; we only require the field exists.
    # No PAGE_WALK endpoints are pre-registered by build_default_registry in v1.
    assert reg.get("chart", "historical_price_full") is not None


@pytest_asyncio.fixture
async def storage(tmp_path: Path) -> ParquetStorage:
    s = ParquetStorage(tmp_path)
    await s.initialize()
    return s


class TestPageWalkProxyReadOnly:
    @pytest.mark.asyncio
    async def test_user_call_returns_stored_records(self, storage: ParquetStorage) -> None:
        """When a user calls a PAGE_WALK-registered method, the proxy returns stored records
        without contacting the upstream API."""
        reg = EndpointRegistry()
        reg.register(
            CacheableEndpoint(
                category="analyst",
                method="financial_estimates",
                api_endpoint="analyst-estimates",
                pattern=TemporalPattern.PAGE_WALK,
                entity_key_args=["symbol"],
                extra_key_args=["period"],
                page_param="page",
                walk_date_field="date",
                call_params=["symbol", "period", "page", "limit"],
            )
        )

        # Pre-seed storage as if the harvester had written it
        await storage.write(
            ("analyst-estimates", "AAPL", "annual"),
            [
                {"symbol": "AAPL", "date": "2025-12-31", "revenueAvg": 500},
                {"symbol": "AAPL", "date": "2024-12-31", "revenueAvg": 400},
                {"symbol": "AAPL", "date": "2023-12-31", "revenueAvg": 300},
            ],
            date_field="date",
        )

        real_category = MagicMock()
        # If the proxy mistakenly calls upstream, this will be invoked:
        real_category.financial_estimates = AsyncMock(side_effect=AssertionError("upstream called"))

        proxy = CachedCategoryProxy(real_category, "analyst", storage, reg)
        records = await proxy.financial_estimates(symbol="AAPL", period="annual", page=0, limit=2)

        # Returns the requested limit slice (newest first by date convention)
        assert len(records) == 2
        assert records[0]["date"] == "2025-12-31"
        assert records[1]["date"] == "2024-12-31"

    @pytest.mark.asyncio
    async def test_user_call_returns_empty_when_no_storage(self, storage: ParquetStorage) -> None:
        reg = EndpointRegistry()
        reg.register(
            CacheableEndpoint(
                category="analyst",
                method="financial_estimates",
                api_endpoint="analyst-estimates",
                pattern=TemporalPattern.PAGE_WALK,
                entity_key_args=["symbol"],
                extra_key_args=["period"],
                page_param="page",
                walk_date_field="date",
                call_params=["symbol", "period", "page", "limit"],
            )
        )
        real_category = MagicMock()
        real_category.financial_estimates = AsyncMock(side_effect=AssertionError("upstream called"))
        proxy = CachedCategoryProxy(real_category, "analyst", storage, reg)
        records = await proxy.financial_estimates(symbol="MSFT", period="annual")
        assert records == []
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_cachedclient/test_page_walk_registry.py -v`
Expected: failures — `TemporalPattern.PAGE_WALK` doesn't exist, `page_param` / `walk_date_field` / `default_page_size` fields missing.

- [ ] **Step 3: Add `PAGE_WALK` to `TemporalPattern`**

In `aiofmp/cachedclient/registry.py`, extend the enum:

```python
class TemporalPattern(str, Enum):
    """How an endpoint's time-series data is parameterized."""

    DATE_RANGE = "date_range"        # Pattern A: from/to date params
    PERIOD_BASED = "period_based"    # Pattern B: limit/period params
    PAGE_WALK = "page_walk"          # Harvester-only writes; user reads are passthrough-to-storage
```

- [ ] **Step 4: Extend `CacheableEndpoint` with the three new fields**

In `aiofmp/cachedclient/registry.py`, add to the dataclass:

```python
@dataclass(frozen=True)
class CacheableEndpoint:
    # ... existing fields ...
    # PAGE_WALK fields (only used when pattern == PAGE_WALK)
    page_param: str = "page"
    default_page_size: int = 100
    walk_date_field: str = "date"
```

(These have sensible defaults so existing DATE_RANGE / PERIOD_BASED registrations don't need changes.)

- [ ] **Step 5: Add PAGE_WALK handling to the proxy**

In `aiofmp/cachedclient/proxy.py`, extend `_cached_fetch` to handle the new pattern. Modify the existing `if/elif` ladder:

```python
async def _cached_fetch(
    self,
    meta: CacheableEndpoint,
    real_method: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> list[dict[str, Any]]:
    bound_args = _bind_args(meta, args, kwargs)
    storage_key = _derive_storage_key(meta, bound_args)

    async with self._get_lock(storage_key):
        if meta.pattern == TemporalPattern.DATE_RANGE:
            return await self._fetch_date_range(meta, real_method, bound_args, storage_key)
        elif meta.pattern == TemporalPattern.PERIOD_BASED:
            return await self._fetch_period_based(meta, real_method, args, kwargs, bound_args, storage_key)
        elif meta.pattern == TemporalPattern.PAGE_WALK:
            return await self._read_page_walk(meta, bound_args, storage_key)
        else:
            return await real_method(*args, **kwargs)


async def _read_page_walk(
    self,
    meta: CacheableEndpoint,
    bound_args: dict[str, Any],
    storage_key: tuple[str, ...],
) -> list[dict[str, Any]]:
    """Read-only path for PAGE_WALK-registered endpoints.

    PAGE_WALK keys are written by the harvester only. User calls return whatever
    is stored, sorted by ``walk_date_field`` descending, sliced by ``page``/``limit``.
    """
    records = await self._storage.read(storage_key)
    if not records:
        return []
    field = meta.walk_date_field
    records.sort(key=lambda r: str(r.get(field, "")), reverse=True)
    page = bound_args.get(meta.page_param, 0) or 0
    limit_val = bound_args.get(meta.limit_param) if meta.limit_param else None
    if limit_val is None:
        limit_val = meta.default_page_size
    start = page * limit_val
    end = start + limit_val
    return records[start:end]
```

- [ ] **Step 6: Run tests to confirm pass**

Run: `uv run pytest tests/test_cachedclient/test_page_walk_registry.py -v`
Expected: all tests pass.

- [ ] **Step 7: Run the full existing cached-client test suite to confirm no regression**

Run: `uv run pytest tests/test_cachedclient -q`
Expected: every previously passing test still passes.

- [ ] **Step 8: Commit**

```bash
git add aiofmp/cachedclient/registry.py aiofmp/cachedclient/proxy.py tests/test_cachedclient/test_page_walk_registry.py
git commit -m "feat(cachedclient): add PAGE_WALK temporal pattern (read-only for users)"
```

---

### Task 12: SnapshotStore for P4 snapshot-overwrite pattern

**Files:**
- Create: `aiofmp/cachedclient/snapshot_store.py`
- Modify: `aiofmp/cachedclient/__init__.py`
- Create: `tests/test_cachedclient/test_snapshot_store.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_cachedclient/test_snapshot_store.py`:

```python
"""Tests for SnapshotStore (P4 snapshot-overwrite pattern)."""

from __future__ import annotations

from pathlib import Path

import pytest
import pytest_asyncio

from aiofmp.cachedclient.snapshot_store import SnapshotStore
from aiofmp.cachedclient.storage.parquet import ParquetStorage


@pytest_asyncio.fixture
async def storage(tmp_path: Path) -> ParquetStorage:
    s = ParquetStorage(tmp_path)
    await s.initialize()
    return s


class TestSnapshotStore:
    @pytest.mark.asyncio
    async def test_write_and_read_single_row(self, storage: ParquetStorage) -> None:
        ss = SnapshotStore(storage)
        await ss.write("discounted-cash-flow", "AAPL", {"symbol": "AAPL", "dcf": 147.27, "Stock Price": 231.79})
        row = await ss.read("discounted-cash-flow", "AAPL")
        assert row is not None
        assert row["symbol"] == "AAPL"
        assert row["dcf"] == 147.27

    @pytest.mark.asyncio
    async def test_write_overwrites_previous(self, storage: ParquetStorage) -> None:
        ss = SnapshotStore(storage)
        await ss.write("ratings-snapshot", "AAPL", {"symbol": "AAPL", "rating": "A-", "score": 4})
        await ss.write("ratings-snapshot", "AAPL", {"symbol": "AAPL", "rating": "A", "score": 5})
        row = await ss.read("ratings-snapshot", "AAPL")
        assert row is not None
        assert row["rating"] == "A"
        assert row["score"] == 5

    @pytest.mark.asyncio
    async def test_read_missing_returns_none(self, storage: ParquetStorage) -> None:
        ss = SnapshotStore(storage)
        assert await ss.read("ratings-snapshot", "ZZZ") is None

    @pytest.mark.asyncio
    async def test_write_empty_dict_skipped(self, storage: ParquetStorage) -> None:
        ss = SnapshotStore(storage)
        await ss.write("ratings-snapshot", "AAPL", {})
        assert await ss.read("ratings-snapshot", "AAPL") is None

    @pytest.mark.asyncio
    async def test_list_entities(self, storage: ParquetStorage) -> None:
        ss = SnapshotStore(storage)
        await ss.write("discounted-cash-flow", "AAPL", {"x": 1})
        await ss.write("discounted-cash-flow", "MSFT", {"x": 2})
        await ss.write("levered-discounted-cash-flow", "AAPL", {"x": 3})
        entities = await ss.list_entities("discounted-cash-flow")
        assert set(entities) == {"AAPL", "MSFT"}
        entities2 = await ss.list_entities("levered-discounted-cash-flow")
        assert set(entities2) == {"AAPL"}
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_cachedclient/test_snapshot_store.py -v`
Expected: ImportError.

- [ ] **Step 3: Create `aiofmp/cachedclient/snapshot_store.py`**

```python
"""SnapshotStore — single-row-per-entity storage on top of a StorageBackend.

Used by the P4 snapshot-overwrite pattern (e.g. analyst ratings, DCF).
Storage keys take the shape ``("snapshot/<endpoint>", entity)``.
Each write replaces the previous row; reads return the latest dict or None.
"""

from __future__ import annotations

from typing import Any

from aiofmp.cachedclient.storage.base import StorageBackend


class SnapshotStore:
    """Thin wrapper that stores a single dict-row per (endpoint, entity) key."""

    def __init__(self, storage: StorageBackend) -> None:
        self._storage = storage

    def _key(self, endpoint: str, entity: str) -> tuple[str, ...]:
        return (f"snapshot/{endpoint}", entity)

    async def write(self, endpoint: str, entity: str, payload: dict[str, Any]) -> None:
        if not payload:
            return
        await self._storage.write(self._key(endpoint, entity), [payload], date_field="date")

    async def read(self, endpoint: str, entity: str) -> dict[str, Any] | None:
        records = await self._storage.read(self._key(endpoint, entity))
        if not records:
            return None
        return records[0]

    async def list_entities(self, endpoint: str) -> list[str]:
        """List all entities stored under ``snapshot/<endpoint>``."""
        prefix = (f"snapshot/{endpoint}",)
        keys = await self._storage.list_keys(prefix=prefix)
        entities: list[str] = []
        for k in keys:
            # key shape is (f"snapshot/{endpoint}", entity)
            if len(k) >= 2:
                entities.append(k[1])
        return entities
```

- [ ] **Step 4: Re-export from `aiofmp/cachedclient/__init__.py`**

Append to `aiofmp/cachedclient/__init__.py`:

```python
from .snapshot_store import SnapshotStore  # noqa: E402

__all__ = [*__all__, "SnapshotStore"] if "__all__" in dir() else ["SnapshotStore"]
```

(If `__all__` doesn't exist, simply add `from .snapshot_store import SnapshotStore` near the top with the other imports.)

- [ ] **Step 5: Run tests to confirm pass**

Run: `uv run pytest tests/test_cachedclient/test_snapshot_store.py -v`
Expected: all 5 tests pass.

- [ ] **Step 6: Commit**

```bash
git add aiofmp/cachedclient/snapshot_store.py aiofmp/cachedclient/__init__.py tests/test_cachedclient/test_snapshot_store.py
git commit -m "feat(cachedclient): SnapshotStore for P4 snapshot-overwrite pattern"
```

---

### Task 13: Register chart endpoints under `commodity`/`forex`/`indexes` categories

**Files:**
- Modify: `aiofmp/cachedclient/registry.py`
- Modify: existing `tests/test_cachedclient/test_registry.py` (if it exists) OR create new `tests/test_cachedclient/test_multi_category_registration.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_cachedclient/test_multi_category_registration.py`:

```python
"""Tests that historical-price endpoints are registered under commodity/forex/indexes too."""

from __future__ import annotations

from aiofmp.cachedclient.gap import DateParamType
from aiofmp.cachedclient.registry import TemporalPattern, build_default_registry


class TestMultiCategoryRegistration:
    def test_commodity_historical_price_full(self) -> None:
        reg = build_default_registry()
        ep = reg.get("commodity", "historical_price_full")
        assert ep is not None
        assert ep.pattern == TemporalPattern.DATE_RANGE
        assert ep.api_endpoint == "historical-price-eod/full"
        assert ep.entity_key_args == ["symbol"]
        assert ep.date_param_type == DateParamType.STRING

    def test_commodity_intraday(self) -> None:
        reg = build_default_registry()
        for m, ep_path in [
            ("intraday_1min", "historical-chart/1min"),
            ("intraday_5min", "historical-chart/5min"),
            ("intraday_1hour", "historical-chart/1hour"),
        ]:
            ep = reg.get("commodity", m)
            assert ep is not None, f"missing commodity.{m}"
            assert ep.api_endpoint == ep_path
            assert ep.date_param_type == DateParamType.STRING

    def test_forex_historical_and_intraday(self) -> None:
        reg = build_default_registry()
        for m, ep_path in [
            ("historical_price_full", "historical-price-eod/full"),
            ("historical_price_light", "historical-price-eod/light"),
            ("intraday_1min", "historical-chart/1min"),
            ("intraday_5min", "historical-chart/5min"),
            ("intraday_1hour", "historical-chart/1hour"),
        ]:
            ep = reg.get("forex", m)
            assert ep is not None, f"missing forex.{m}"
            assert ep.api_endpoint == ep_path
            assert ep.date_param_type == DateParamType.STRING

    def test_indexes_uses_date_obj(self) -> None:
        reg = build_default_registry()
        for m, ep_path in [
            ("historical_price_eod_full", "historical-price-eod/full"),
            ("historical_price_eod_light", "historical-price-eod/light"),
            ("intraday_1min", "historical-chart/1min"),
            ("intraday_5min", "historical-chart/5min"),
            ("intraday_1hour", "historical-chart/1hour"),
        ]:
            ep = reg.get("indexes", m)
            assert ep is not None, f"missing indexes.{m}"
            assert ep.api_endpoint == ep_path
            assert ep.date_param_type == DateParamType.DATE_OBJ

    def test_same_storage_key_across_categories(self) -> None:
        """commodity.historical_price_full and chart.historical_price_full must produce
        the same storage key for the same symbol — that's the whole point of multi-registration."""
        from aiofmp.cachedclient.proxy import _derive_storage_key  # private helper

        reg = build_default_registry()
        chart_ep = reg.get("chart", "historical_price_full")
        commodity_ep = reg.get("commodity", "historical_price_full")
        assert chart_ep is not None and commodity_ep is not None
        bound = {"symbol": "GCUSD", "from_date": "2024-01-01", "to_date": "2024-12-31"}
        assert _derive_storage_key(chart_ep, bound) == _derive_storage_key(commodity_ep, bound)
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_cachedclient/test_multi_category_registration.py -v`
Expected: failures — these registrations don't exist yet.

- [ ] **Step 3: Extend `build_default_registry()` in `aiofmp/cachedclient/registry.py`**

Append to `build_default_registry()` BEFORE the `return registry` line, after all existing `chart` registrations:

```python
    # =========================================================================
    # Multi-category sharing: commodity / forex / indexes use the same FMP
    # wire endpoints as chart.* but expose their own SDK methods. Register
    # the same metadata under those categories so user-driven calls hit the
    # same cache. Storage keys start with api_endpoint, so they share parquet.
    # =========================================================================

    # --- Commodity (str dates) ---
    for method, endpoint in [
        ("historical_price_light", "historical-price-eod/light"),
        ("historical_price_full", "historical-price-eod/full"),
    ]:
        registry.register(
            CacheableEndpoint(
                category="commodity",
                method=method,
                api_endpoint=endpoint,
                pattern=TemporalPattern.DATE_RANGE,
                entity_key_args=["symbol"],
                date_param_type=DateParamType.STRING,
                call_params=["symbol", "from_date", "to_date"],
            )
        )
    for method, endpoint in [
        ("intraday_1min", "historical-chart/1min"),
        ("intraday_5min", "historical-chart/5min"),
        ("intraday_1hour", "historical-chart/1hour"),
    ]:
        registry.register(
            CacheableEndpoint(
                category="commodity",
                method=method,
                api_endpoint=endpoint,
                pattern=TemporalPattern.DATE_RANGE,
                entity_key_args=["symbol"],
                response_date_format="%Y-%m-%d %H:%M:%S",
                date_param_type=DateParamType.STRING,
                call_params=["symbol", "from_date", "to_date"],
            )
        )

    # --- Forex (str dates) ---
    for method, endpoint in [
        ("historical_price_light", "historical-price-eod/light"),
        ("historical_price_full", "historical-price-eod/full"),
    ]:
        registry.register(
            CacheableEndpoint(
                category="forex",
                method=method,
                api_endpoint=endpoint,
                pattern=TemporalPattern.DATE_RANGE,
                entity_key_args=["symbol"],
                date_param_type=DateParamType.STRING,
                call_params=["symbol", "from_date", "to_date"],
            )
        )
    for method, endpoint in [
        ("intraday_1min", "historical-chart/1min"),
        ("intraday_5min", "historical-chart/5min"),
        ("intraday_1hour", "historical-chart/1hour"),
    ]:
        registry.register(
            CacheableEndpoint(
                category="forex",
                method=method,
                api_endpoint=endpoint,
                pattern=TemporalPattern.DATE_RANGE,
                entity_key_args=["symbol"],
                response_date_format="%Y-%m-%d %H:%M:%S",
                date_param_type=DateParamType.STRING,
                call_params=["symbol", "from_date", "to_date"],
            )
        )

    # --- Indexes (date objects) ---
    for method, endpoint in [
        ("historical_price_eod_light", "historical-price-eod/light"),
        ("historical_price_eod_full", "historical-price-eod/full"),
    ]:
        registry.register(
            CacheableEndpoint(
                category="indexes",
                method=method,
                api_endpoint=endpoint,
                pattern=TemporalPattern.DATE_RANGE,
                entity_key_args=["symbol"],
                date_param_type=DateParamType.DATE_OBJ,
                call_params=["symbol", "from_date", "to_date"],
            )
        )
    for method, endpoint in [
        ("intraday_1min", "historical-chart/1min"),
        ("intraday_5min", "historical-chart/5min"),
        ("intraday_1hour", "historical-chart/1hour"),
    ]:
        registry.register(
            CacheableEndpoint(
                category="indexes",
                method=method,
                api_endpoint=endpoint,
                pattern=TemporalPattern.DATE_RANGE,
                entity_key_args=["symbol"],
                response_date_format="%Y-%m-%d %H:%M:%S",
                date_param_type=DateParamType.DATE_OBJ,
                call_params=["symbol", "from_date", "to_date"],
            )
        )
```

- [ ] **Step 4: Run tests to confirm pass**

Run: `uv run pytest tests/test_cachedclient/test_multi_category_registration.py -v`
Expected: all 5 tests pass.

- [ ] **Step 5: Confirm no regression on the cached-client suite**

Run: `uv run pytest tests/test_cachedclient -q`
Expected: every previously passing test still passes.

- [ ] **Step 6: Commit**

```bash
git add aiofmp/cachedclient/registry.py tests/test_cachedclient/test_multi_category_registration.py
git commit -m "feat(cachedclient): register chart endpoints under commodity/forex/indexes"
```

---

### Task 14: Register PAGE_WALK endpoints for analyst / insider-trading / form 13F

**Files:**
- Modify: `aiofmp/cachedclient/registry.py`
- Modify: `tests/test_cachedclient/test_page_walk_registry.py`

- [ ] **Step 1: Append failing tests to `test_page_walk_registry.py`**

Append to `tests/test_cachedclient/test_page_walk_registry.py`:

```python
class TestPageWalkEndpointRegistrations:
    def test_analyst_financial_estimates_registered(self) -> None:
        reg = build_default_registry()
        ep = reg.get("analyst", "financial_estimates")
        assert ep is not None
        assert ep.pattern == TemporalPattern.PAGE_WALK
        assert ep.api_endpoint == "analyst-estimates"
        assert ep.entity_key_args == ["symbol"]
        assert ep.extra_key_args == ["period"]
        assert ep.page_param == "page"
        assert ep.limit_param == "limit"
        assert ep.walk_date_field == "date"

    def test_insider_trades_latest_registered(self) -> None:
        reg = build_default_registry()
        ep = reg.get("insider_trades", "latest_insider_trades")
        assert ep is not None
        assert ep.pattern == TemporalPattern.PAGE_WALK
        assert ep.api_endpoint == "insider-trading/latest"
        assert ep.entity_key_args == []
        assert ep.page_param == "page"
        assert ep.walk_date_field == "filingDate"

    def test_form13f_latest_filings_registered(self) -> None:
        reg = build_default_registry()
        ep = reg.get("form13f", "latest_filings")
        assert ep is not None
        assert ep.pattern == TemporalPattern.PAGE_WALK
        assert ep.api_endpoint == "institutional-ownership/latest"
        assert ep.walk_date_field == "acceptedDate"
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_cachedclient/test_page_walk_registry.py::TestPageWalkEndpointRegistrations -v`
Expected: failures — endpoints not registered.

- [ ] **Step 3: Register PAGE_WALK endpoints in `build_default_registry`**

Append to `build_default_registry()` BEFORE the `return registry` line:

```python
    # =========================================================================
    # Pattern PAGE_WALK: harvester-write, user-read paginated endpoints
    # =========================================================================

    # --- Analyst estimates (per-symbol walk) ---
    registry.register(
        CacheableEndpoint(
            category="analyst",
            method="financial_estimates",
            api_endpoint="analyst-estimates",
            pattern=TemporalPattern.PAGE_WALK,
            entity_key_args=["symbol"],
            extra_key_args=["period"],
            page_param="page",
            limit_param="limit",
            walk_date_field="date",
            default_page_size=100,
            call_params=["symbol", "period", "page", "limit"],
        )
    )

    # --- Insider trades (global walk; per-symbol shard on write) ---
    registry.register(
        CacheableEndpoint(
            category="insider_trades",
            method="latest_insider_trades",
            api_endpoint="insider-trading/latest",
            pattern=TemporalPattern.PAGE_WALK,
            entity_key_args=[],
            page_param="page",
            limit_param="limit",
            walk_date_field="filingDate",
            default_page_size=100,
            call_params=["page", "limit", "trade_date"],
        )
    )

    # --- Form 13F (global walk; per-CIK shard on write) ---
    registry.register(
        CacheableEndpoint(
            category="form13f",
            method="latest_filings",
            api_endpoint="institutional-ownership/latest",
            pattern=TemporalPattern.PAGE_WALK,
            entity_key_args=[],
            page_param="page",
            limit_param="limit",
            walk_date_field="acceptedDate",
            default_page_size=100,
            call_params=["page", "limit", "trade_date"],
        )
    )
```

- [ ] **Step 4: Run tests to confirm pass**

Run: `uv run pytest tests/test_cachedclient/test_page_walk_registry.py -v`
Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add aiofmp/cachedclient/registry.py tests/test_cachedclient/test_page_walk_registry.py
git commit -m "feat(cachedclient): register PAGE_WALK endpoints for analyst/insider/form13f"
```

---

## Phase 3 — Pattern P3 categories (gap-fill via CachedClient)

### Task 15: `GapFillHarvester` shared base for all P3 categories

**Files:**
- Create: `aiofmp/harvester/gap_fill_base.py`
- Create: `tests/test_harvester/test_gap_fill_base.py`

This is a DRY base used by `chart_eod`, `chart_intraday`, `commodities_eod`, `commodities_intraday`, `forex_eod`, `forex_intraday`, `indexes_eod`, `indexes_intraday`, `news`, `economics`, and `technical_indicators`. Each concrete category just configures the base with a symbol universe and the SDK method to call per symbol; CachedClient gap-fill does the rest.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_harvester/test_gap_fill_base.py`:

```python
"""Tests for GapFillHarvester (DRY base for P3 categories)."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.gap_fill_base import GapFillHarvester, GapFillTarget
from aiofmp.harvester.state import RunStatus, StateStore


@pytest.fixture
def store(tmp_path: Path) -> StateStore:
    s = StateStore(tmp_path / "h.sqlite")
    s.initialize()
    return s


@pytest.fixture
def catalog() -> MagicMock:
    cat = MagicMock()
    cat.symbols = AsyncMock(return_value=["AAPL", "MSFT", "GOOGL"])
    return cat


@pytest.fixture
def cached_client() -> MagicMock:
    """A fake CachedClient that records each call and returns canned data."""
    cc = MagicMock()
    cc.chart = MagicMock()
    cc.chart.historical_price_full = AsyncMock(return_value=[{"date": "2025-01-15", "close": 100}])
    cc.chart.historical_price_light = AsyncMock(return_value=[{"date": "2025-01-15", "close": 100}])
    return cc


def make_harvester(
    *,
    store: StateStore,
    catalog: MagicMock,
    cached_client: MagicMock,
    extra: dict[str, Any] | None = None,
    targets: list[GapFillTarget] | None = None,
) -> GapFillHarvester:
    cfg = CategoryConfig(enabled=True, interval="1d", extra=extra or {})
    budget = BudgetTracker(store, BudgetConfig())
    retry = RetryConfig()

    if targets is None:
        targets = [
            GapFillTarget(
                category_attr="chart",
                method_name="historical_price_full",
                use_date_obj=False,
            )
        ]

    return GapFillHarvester(
        name="test_gap",
        config=cfg,
        state=store,
        budget=budget,
        retry=retry,
        symbol_catalog=catalog,
        symbol_universe="actively_trading",
        cached_client=cached_client,
        targets=targets,
        backfill_seconds=10 * 86400,  # 10 days
    )


class TestGapFillHarvester:
    @pytest.mark.asyncio
    async def test_iterates_symbols_and_calls_target(self, store, catalog, cached_client) -> None:
        h = make_harvester(store=store, catalog=catalog, cached_client=cached_client)
        outcome = await h.run_cycle()
        assert outcome.status == RunStatus.OK
        assert outcome.items_attempted == 3
        assert outcome.items_succeeded == 3
        assert cached_client.chart.historical_price_full.await_count == 3

    @pytest.mark.asyncio
    async def test_uses_string_dates(self, store, catalog, cached_client) -> None:
        h = make_harvester(store=store, catalog=catalog, cached_client=cached_client)
        await h.run_cycle()
        first_call = cached_client.chart.historical_price_full.await_args_list[0]
        # called as historical_price_full(symbol, from_date, to_date)
        assert isinstance(first_call.args[0], str)
        assert isinstance(first_call.args[1], str)
        assert isinstance(first_call.args[2], str)

    @pytest.mark.asyncio
    async def test_uses_date_objects_when_configured(self, store, catalog, cached_client) -> None:
        cached_client.indexes = MagicMock()
        cached_client.indexes.historical_price_eod_full = AsyncMock(return_value=[])
        targets = [
            GapFillTarget(
                category_attr="indexes",
                method_name="historical_price_eod_full",
                use_date_obj=True,
            )
        ]
        h = make_harvester(
            store=store, catalog=catalog, cached_client=cached_client, targets=targets
        )
        await h.run_cycle()
        first_call = cached_client.indexes.historical_price_eod_full.await_args_list[0]
        assert isinstance(first_call.args[1], date)
        assert isinstance(first_call.args[2], date)

    @pytest.mark.asyncio
    async def test_per_symbol_error_does_not_kill_cycle(self, store, catalog, cached_client) -> None:
        cached_client.chart.historical_price_full = AsyncMock(
            side_effect=[
                [{"date": "2025-01-15"}],
                RuntimeError("symbol explodes"),
                [{"date": "2025-01-15"}],
            ]
        )
        h = make_harvester(store=store, catalog=catalog, cached_client=cached_client)
        outcome = await h.run_cycle()
        assert outcome.status == RunStatus.PARTIAL
        assert outcome.items_attempted == 3
        assert outcome.items_succeeded == 2

    @pytest.mark.asyncio
    async def test_multiple_variants(self, store, catalog, cached_client) -> None:
        targets = [
            GapFillTarget(category_attr="chart", method_name="historical_price_full", use_date_obj=False),
            GapFillTarget(category_attr="chart", method_name="historical_price_light", use_date_obj=False),
        ]
        h = make_harvester(
            store=store, catalog=catalog, cached_client=cached_client, targets=targets,
        )
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 6  # 3 symbols * 2 variants
        assert cached_client.chart.historical_price_full.await_count == 3
        assert cached_client.chart.historical_price_light.await_count == 3

    @pytest.mark.asyncio
    async def test_empty_universe_is_ok(self, store, cached_client) -> None:
        empty_catalog = MagicMock()
        empty_catalog.symbols = AsyncMock(return_value=[])
        h = make_harvester(store=store, catalog=empty_catalog, cached_client=cached_client)
        outcome = await h.run_cycle()
        assert outcome.status == RunStatus.OK
        assert outcome.items_attempted == 0
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_gap_fill_base.py -v`
Expected: ImportError.

- [ ] **Step 3: Create `aiofmp/harvester/gap_fill_base.py`**

```python
"""GapFillHarvester — DRY base for P3 categories that delegate to CachedClient gap-fill."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from typing import Any

from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.config import CategoryConfig, RetryConfig
from aiofmp.harvester.state import RunStatus, StateStore

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GapFillTarget:
    """One (category_attr, method_name) pair to call per symbol."""

    category_attr: str        # e.g. "chart", "commodity", "forex", "indexes"
    method_name: str          # e.g. "historical_price_full"
    use_date_obj: bool        # True for indexes.*, False elsewhere


class GapFillHarvester(CategoryHarvester):
    """Generic P3 harvester: for each symbol in a universe, call each target
    method with ``(symbol, from_date, to_date)`` and let CachedClient gap-fill.
    """

    def __init__(
        self,
        name: str,
        config: CategoryConfig,
        state: StateStore,
        budget: BudgetTracker,
        retry: RetryConfig,
        *,
        symbol_catalog: Any,
        symbol_universe: str,
        cached_client: Any,
        targets: list[GapFillTarget],
        backfill_seconds: int,
    ) -> None:
        super().__init__(name, config, state, budget, retry)
        self._catalog = symbol_catalog
        self._universe = symbol_universe
        self._cached = cached_client
        self._targets = list(targets)
        self._backfill_seconds = backfill_seconds

    async def run_cycle(self) -> RunOutcome:
        symbols = await self._catalog.symbols(self._universe)
        if not symbols:
            return RunOutcome(status=RunStatus.OK)

        today = date.today()
        from_date = today - timedelta(seconds=self._backfill_seconds)

        attempted = 0
        succeeded = 0
        for symbol in symbols:
            for target in self._targets:
                attempted += 1
                try:
                    await self._call_target(target, symbol, from_date, today)
                    succeeded += 1
                except Exception as exc:
                    logger.warning(
                        "%s: %s.%s(%s) failed: %s",
                        self.name, target.category_attr, target.method_name, symbol, exc,
                    )

        status = RunStatus.OK if succeeded == attempted else RunStatus.PARTIAL
        return RunOutcome(status=status, items_attempted=attempted, items_succeeded=succeeded)

    async def _call_target(
        self,
        target: GapFillTarget,
        symbol: str,
        from_d: date,
        to_d: date,
    ) -> None:
        category = getattr(self._cached, target.category_attr)
        method = getattr(category, target.method_name)
        if target.use_date_obj:
            await method(symbol, from_d, to_d)
        else:
            await method(symbol, from_d.isoformat(), to_d.isoformat())
```

- [ ] **Step 4: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_gap_fill_base.py -v`
Expected: all 6 tests pass.

- [ ] **Step 5: Commit**

```bash
git add aiofmp/harvester/gap_fill_base.py tests/test_harvester/test_gap_fill_base.py
git commit -m "feat(harvester): GapFillHarvester DRY base for P3 categories"
```

---

### Task 16: `chart_eod` category

**Files:**
- Create: `aiofmp/harvester/categories/chart_eod.py`
- Create: `tests/test_harvester/test_chart_eod.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_harvester/test_chart_eod.py`:

```python
"""Tests for chart_eod category."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.categories.chart_eod import build_chart_eod
from aiofmp.harvester.config import CategoryConfig


@pytest.fixture
def manager(tmp_path: Path) -> MagicMock:
    """A fake manager exposing the attributes a category factory consumes."""
    from aiofmp.harvester.budget import BudgetTracker
    from aiofmp.harvester.config import BudgetConfig, RetryConfig
    from aiofmp.harvester.state import StateStore

    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite")
    m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock()
    m.config.retry = RetryConfig()
    m.catalog = MagicMock()
    m.catalog.symbols = AsyncMock(return_value=["AAPL"])
    m.cached_client = MagicMock()
    m.cached_client.chart = MagicMock()
    m.cached_client.chart.historical_price_full = AsyncMock(return_value=[{"date": "2025-01-15"}])
    m.cached_client.chart.historical_price_light = AsyncMock(return_value=[])
    return m


class TestChartEod:
    @pytest.mark.asyncio
    async def test_default_variants(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(enabled=True, interval="24h", extra={"backfill_years": 5})
        h = build_chart_eod(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 1  # 1 symbol * 1 default variant
        manager.cached_client.chart.historical_price_full.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_multiple_variants(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(
            enabled=True,
            interval="24h",
            extra={"variants": ["historical_price_full", "historical_price_light"]},
        )
        h = build_chart_eod(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 2
        manager.cached_client.chart.historical_price_full.assert_awaited_once()
        manager.cached_client.chart.historical_price_light.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_custom_symbol_universe(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(
            enabled=True,
            interval="24h",
            extra={"symbol_universe": "financial_symbols"},
        )
        h = build_chart_eod(cfg, manager)
        await h.run_cycle()
        manager.catalog.symbols.assert_awaited_with("financial_symbols")

    @pytest.mark.asyncio
    async def test_registers_at_import(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY
        assert "chart_eod" in _REGISTRY
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_chart_eod.py -v`
Expected: ImportError.

- [ ] **Step 3: Create `aiofmp/harvester/categories/chart_eod.py`**

```python
"""chart_eod category — P3 gap-fill over actively_trading."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.gap_fill_base import GapFillHarvester, GapFillTarget

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager


_DEFAULT_VARIANTS = ["historical_price_full"]


def build_chart_eod(cfg: CategoryConfig, manager: "HarvesterManager") -> GapFillHarvester:
    variants = list(cfg.extra.get("variants", _DEFAULT_VARIANTS))
    backfill_years = int(cfg.extra.get("backfill_years", 10))
    universe = str(cfg.extra.get("symbol_universe", "actively_trading"))

    targets = [
        GapFillTarget(category_attr="chart", method_name=v, use_date_obj=False)
        for v in variants
    ]
    return GapFillHarvester(
        name="chart_eod",
        config=cfg,
        state=manager.state,
        budget=manager.budget,
        retry=manager.config.retry,
        symbol_catalog=manager.catalog,
        symbol_universe=universe,
        cached_client=manager.cached_client,
        targets=targets,
        backfill_seconds=backfill_years * 365 * 86400,
    )


register_category("chart_eod", build_chart_eod)
```

- [ ] **Step 4: Import the category in the categories package so registration runs**

Modify `aiofmp/harvester/categories/__init__.py` — append at the BOTTOM (after `registered_names` is defined):

```python
# Import concrete category modules so their register_category() calls fire.
from aiofmp.harvester.categories import chart_eod  # noqa: E402, F401
```

- [ ] **Step 5: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_chart_eod.py -v`
Expected: all 4 tests pass.

- [ ] **Step 6: Commit**

```bash
git add aiofmp/harvester/categories/chart_eod.py aiofmp/harvester/categories/__init__.py tests/test_harvester/test_chart_eod.py
git commit -m "feat(harvester): chart_eod category (P3 gap-fill)"
```

---

### Task 17: `chart_intraday`, `commodities_eod`/`_intraday`, `forex_eod`/`_intraday`, `indexes_eod`/`_intraday`

**Files:**
- Create: `aiofmp/harvester/categories/chart_intraday.py`
- Create: `aiofmp/harvester/categories/commodities_eod.py`
- Create: `aiofmp/harvester/categories/commodities_intraday.py`
- Create: `aiofmp/harvester/categories/forex_eod.py`
- Create: `aiofmp/harvester/categories/forex_intraday.py`
- Create: `aiofmp/harvester/categories/indexes_eod.py`
- Create: `aiofmp/harvester/categories/indexes_intraday.py`
- Modify: `aiofmp/harvester/categories/__init__.py` (register new modules)
- Create: `tests/test_harvester/test_chart_intraday.py`
- Create: `tests/test_harvester/test_commodities_eod.py`
- Create: `tests/test_harvester/test_forex_eod.py`
- Create: `tests/test_harvester/test_indexes_eod.py`

All seven categories share a near-identical shape: pick a universe, pick a target method, optionally walk multiple timeframes. We write one comprehensive test file per "EOD" variant and one per "intraday" variant (intraday tests cover all three vehicles in one file).

- [ ] **Step 1: Create `aiofmp/harvester/categories/chart_intraday.py`**

```python
"""chart_intraday category — P3 gap-fill per (symbol, timeframe)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.gap_fill_base import GapFillHarvester, GapFillTarget

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager


_DEFAULT_TIMEFRAMES = ["1hour"]
_TF_TO_METHOD = {
    "1min": "intraday_1min",
    "5min": "intraday_5min",
    "15min": "intraday_15min",
    "30min": "intraday_30min",
    "1hour": "intraday_1hour",
    "4hour": "intraday_4hour",
}


def _build_intraday(
    name: str,
    category_attr: str,
    use_date_obj: bool,
    universe: str,
    cfg: CategoryConfig,
    manager: "HarvesterManager",
) -> GapFillHarvester:
    timeframes = list(cfg.extra.get("timeframes", _DEFAULT_TIMEFRAMES))
    for tf in timeframes:
        if tf not in _TF_TO_METHOD:
            raise ValueError(f"{name}: unknown timeframe {tf!r}; valid: {list(_TF_TO_METHOD)}")
    backfill_days = int(cfg.extra.get("backfill_days", 30))
    user_universe = str(cfg.extra.get("symbol_universe", universe))

    targets = [
        GapFillTarget(category_attr=category_attr, method_name=_TF_TO_METHOD[tf], use_date_obj=use_date_obj)
        for tf in timeframes
    ]
    return GapFillHarvester(
        name=name,
        config=cfg,
        state=manager.state,
        budget=manager.budget,
        retry=manager.config.retry,
        symbol_catalog=manager.catalog,
        symbol_universe=user_universe,
        cached_client=manager.cached_client,
        targets=targets,
        backfill_seconds=backfill_days * 86400,
    )


def build_chart_intraday(cfg: CategoryConfig, manager: "HarvesterManager") -> GapFillHarvester:
    return _build_intraday("chart_intraday", "chart", False, "actively_trading", cfg, manager)


register_category("chart_intraday", build_chart_intraday)
```

- [ ] **Step 2: Create `aiofmp/harvester/categories/commodities_eod.py`**

```python
"""commodities_eod category — P3 gap-fill over the commodities universe."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.gap_fill_base import GapFillHarvester, GapFillTarget

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager


_DEFAULT_VARIANTS = ["historical_price_full"]


def build_commodities_eod(cfg: CategoryConfig, manager: "HarvesterManager") -> GapFillHarvester:
    variants = list(cfg.extra.get("variants", _DEFAULT_VARIANTS))
    backfill_years = int(cfg.extra.get("backfill_years", 10))
    targets = [
        GapFillTarget(category_attr="commodity", method_name=v, use_date_obj=False)
        for v in variants
    ]
    return GapFillHarvester(
        name="commodities_eod",
        config=cfg,
        state=manager.state,
        budget=manager.budget,
        retry=manager.config.retry,
        symbol_catalog=manager.catalog,
        symbol_universe="commodities",
        cached_client=manager.cached_client,
        targets=targets,
        backfill_seconds=backfill_years * 365 * 86400,
    )


register_category("commodities_eod", build_commodities_eod)
```

- [ ] **Step 3: Create `aiofmp/harvester/categories/commodities_intraday.py`**

```python
"""commodities_intraday category — P3 gap-fill per (symbol, timeframe)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aiofmp.harvester.categories import register_category
from aiofmp.harvester.categories.chart_intraday import _build_intraday  # reuse helper
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.gap_fill_base import GapFillHarvester

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager


def build_commodities_intraday(cfg: CategoryConfig, manager: "HarvesterManager") -> GapFillHarvester:
    return _build_intraday("commodities_intraday", "commodity", False, "commodities", cfg, manager)


register_category("commodities_intraday", build_commodities_intraday)
```

- [ ] **Step 4: Create `aiofmp/harvester/categories/forex_eod.py`**

```python
"""forex_eod category — P3 gap-fill over the forex_pairs universe."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.gap_fill_base import GapFillHarvester, GapFillTarget

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager


_DEFAULT_VARIANTS = ["historical_price_full"]


def build_forex_eod(cfg: CategoryConfig, manager: "HarvesterManager") -> GapFillHarvester:
    variants = list(cfg.extra.get("variants", _DEFAULT_VARIANTS))
    backfill_years = int(cfg.extra.get("backfill_years", 10))
    targets = [
        GapFillTarget(category_attr="forex", method_name=v, use_date_obj=False)
        for v in variants
    ]
    return GapFillHarvester(
        name="forex_eod",
        config=cfg,
        state=manager.state,
        budget=manager.budget,
        retry=manager.config.retry,
        symbol_catalog=manager.catalog,
        symbol_universe="forex_pairs",
        cached_client=manager.cached_client,
        targets=targets,
        backfill_seconds=backfill_years * 365 * 86400,
    )


register_category("forex_eod", build_forex_eod)
```

- [ ] **Step 5: Create `aiofmp/harvester/categories/forex_intraday.py`**

```python
"""forex_intraday category."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aiofmp.harvester.categories import register_category
from aiofmp.harvester.categories.chart_intraday import _build_intraday
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.gap_fill_base import GapFillHarvester

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager


def build_forex_intraday(cfg: CategoryConfig, manager: "HarvesterManager") -> GapFillHarvester:
    return _build_intraday("forex_intraday", "forex", False, "forex_pairs", cfg, manager)


register_category("forex_intraday", build_forex_intraday)
```

- [ ] **Step 6: Create `aiofmp/harvester/categories/indexes_eod.py`**

```python
"""indexes_eod category — P3 gap-fill over the indexes universe (DATE_OBJ params)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.gap_fill_base import GapFillHarvester, GapFillTarget

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager


_DEFAULT_VARIANTS = ["historical_price_eod_full"]


def build_indexes_eod(cfg: CategoryConfig, manager: "HarvesterManager") -> GapFillHarvester:
    variants = list(cfg.extra.get("variants", _DEFAULT_VARIANTS))
    backfill_years = int(cfg.extra.get("backfill_years", 10))
    targets = [
        GapFillTarget(category_attr="indexes", method_name=v, use_date_obj=True)
        for v in variants
    ]
    return GapFillHarvester(
        name="indexes_eod",
        config=cfg,
        state=manager.state,
        budget=manager.budget,
        retry=manager.config.retry,
        symbol_catalog=manager.catalog,
        symbol_universe="indexes",
        cached_client=manager.cached_client,
        targets=targets,
        backfill_seconds=backfill_years * 365 * 86400,
    )


register_category("indexes_eod", build_indexes_eod)
```

- [ ] **Step 7: Create `aiofmp/harvester/categories/indexes_intraday.py`**

```python
"""indexes_intraday category (DATE_OBJ params)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aiofmp.harvester.categories import register_category
from aiofmp.harvester.categories.chart_intraday import _build_intraday
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.gap_fill_base import GapFillHarvester

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager


def build_indexes_intraday(cfg: CategoryConfig, manager: "HarvesterManager") -> GapFillHarvester:
    return _build_intraday("indexes_intraday", "indexes", True, "indexes", cfg, manager)


register_category("indexes_intraday", build_indexes_intraday)
```

- [ ] **Step 8: Wire all new modules into the registry init**

Replace the bottom of `aiofmp/harvester/categories/__init__.py` with the full import list:

```python
# Import concrete category modules so their register_category() calls fire.
from aiofmp.harvester.categories import (  # noqa: E402, F401
    chart_eod,
    chart_intraday,
    commodities_eod,
    commodities_intraday,
    forex_eod,
    forex_intraday,
    indexes_eod,
    indexes_intraday,
)
```

- [ ] **Step 9: Create `tests/test_harvester/test_chart_intraday.py`**

```python
"""Tests for chart_intraday and its sister intraday categories."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import StateStore


def _fake_manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite")
    m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock()
    m.config.retry = RetryConfig()
    m.catalog = MagicMock()
    m.catalog.symbols = AsyncMock(return_value=["X"])
    m.cached_client = MagicMock()
    # Set up every (category, method) the tests touch:
    for cat in ("chart", "commodity", "forex", "indexes"):
        c = MagicMock()
        for method in ("intraday_1min", "intraday_5min", "intraday_15min", "intraday_30min",
                       "intraday_1hour", "intraday_4hour"):
            setattr(c, method, AsyncMock(return_value=[]))
        setattr(m.cached_client, cat, c)
    return m


class TestChartIntradayFamily:
    @pytest.mark.asyncio
    async def test_chart_intraday_default_timeframe(self, tmp_path: Path) -> None:
        from aiofmp.harvester.categories.chart_intraday import build_chart_intraday
        mgr = _fake_manager(tmp_path)
        cfg = CategoryConfig(enabled=True, interval="4h", extra={})
        h = build_chart_intraday(cfg, mgr)
        await h.run_cycle()
        mgr.cached_client.chart.intraday_1hour.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_chart_intraday_multiple_timeframes(self, tmp_path: Path) -> None:
        from aiofmp.harvester.categories.chart_intraday import build_chart_intraday
        mgr = _fake_manager(tmp_path)
        cfg = CategoryConfig(enabled=True, interval="4h", extra={"timeframes": ["1hour", "5min"]})
        h = build_chart_intraday(cfg, mgr)
        await h.run_cycle()
        mgr.cached_client.chart.intraday_1hour.assert_awaited_once()
        mgr.cached_client.chart.intraday_5min.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_chart_intraday_invalid_timeframe_raises(self, tmp_path: Path) -> None:
        from aiofmp.harvester.categories.chart_intraday import build_chart_intraday
        mgr = _fake_manager(tmp_path)
        cfg = CategoryConfig(enabled=True, interval="4h", extra={"timeframes": ["weekly"]})
        with pytest.raises(ValueError, match="weekly"):
            build_chart_intraday(cfg, mgr)

    @pytest.mark.asyncio
    async def test_commodities_intraday(self, tmp_path: Path) -> None:
        from aiofmp.harvester.categories.commodities_intraday import build_commodities_intraday
        mgr = _fake_manager(tmp_path)
        mgr.catalog.symbols = AsyncMock(return_value=["GCUSD"])
        cfg = CategoryConfig(enabled=True, interval="4h", extra={})
        h = build_commodities_intraday(cfg, mgr)
        await h.run_cycle()
        mgr.catalog.symbols.assert_awaited_with("commodities")
        mgr.cached_client.commodity.intraday_1hour.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_forex_intraday(self, tmp_path: Path) -> None:
        from aiofmp.harvester.categories.forex_intraday import build_forex_intraday
        mgr = _fake_manager(tmp_path)
        mgr.catalog.symbols = AsyncMock(return_value=["EURUSD"])
        cfg = CategoryConfig(enabled=True, interval="4h", extra={})
        h = build_forex_intraday(cfg, mgr)
        await h.run_cycle()
        mgr.catalog.symbols.assert_awaited_with("forex_pairs")
        mgr.cached_client.forex.intraday_1hour.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_indexes_intraday_uses_date_obj(self, tmp_path: Path) -> None:
        from datetime import date
        from aiofmp.harvester.categories.indexes_intraday import build_indexes_intraday
        mgr = _fake_manager(tmp_path)
        mgr.catalog.symbols = AsyncMock(return_value=["^GSPC"])
        cfg = CategoryConfig(enabled=True, interval="4h", extra={})
        h = build_indexes_intraday(cfg, mgr)
        await h.run_cycle()
        mgr.catalog.symbols.assert_awaited_with("indexes")
        first_call = mgr.cached_client.indexes.intraday_1hour.await_args_list[0]
        assert isinstance(first_call.args[1], date)
        assert isinstance(first_call.args[2], date)
```

- [ ] **Step 10: Create `tests/test_harvester/test_commodities_eod.py`**

```python
"""Tests for commodities_eod."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.commodities_eod import build_commodities_eod
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import StateStore


@pytest.fixture
def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite"); m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock(); m.config.retry = RetryConfig()
    m.catalog = MagicMock()
    m.catalog.symbols = AsyncMock(return_value=["GCUSD", "CLUSD"])
    m.cached_client = MagicMock()
    m.cached_client.commodity = MagicMock()
    m.cached_client.commodity.historical_price_full = AsyncMock(return_value=[])
    return m


class TestCommoditiesEod:
    @pytest.mark.asyncio
    async def test_iterates_commodities(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(enabled=True, interval="24h", extra={})
        h = build_commodities_eod(cfg, manager)
        outcome = await h.run_cycle()
        manager.catalog.symbols.assert_awaited_with("commodities")
        assert outcome.items_attempted == 2
        assert manager.cached_client.commodity.historical_price_full.await_count == 2

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY
        assert "commodities_eod" in _REGISTRY
```

- [ ] **Step 11: Create `tests/test_harvester/test_forex_eod.py`**

```python
"""Tests for forex_eod."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.forex_eod import build_forex_eod
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import StateStore


@pytest.fixture
def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite"); m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock(); m.config.retry = RetryConfig()
    m.catalog = MagicMock()
    m.catalog.symbols = AsyncMock(return_value=["EURUSD"])
    m.cached_client = MagicMock()
    m.cached_client.forex = MagicMock()
    m.cached_client.forex.historical_price_full = AsyncMock(return_value=[])
    return m


class TestForexEod:
    @pytest.mark.asyncio
    async def test_iterates_pairs(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(enabled=True, interval="24h", extra={})
        h = build_forex_eod(cfg, manager)
        outcome = await h.run_cycle()
        manager.catalog.symbols.assert_awaited_with("forex_pairs")
        assert outcome.items_attempted == 1

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY
        assert "forex_eod" in _REGISTRY
```

- [ ] **Step 12: Create `tests/test_harvester/test_indexes_eod.py`**

```python
"""Tests for indexes_eod (uses date objects)."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.indexes_eod import build_indexes_eod
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import StateStore


@pytest.fixture
def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite"); m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock(); m.config.retry = RetryConfig()
    m.catalog = MagicMock()
    m.catalog.symbols = AsyncMock(return_value=["^GSPC"])
    m.cached_client = MagicMock()
    m.cached_client.indexes = MagicMock()
    m.cached_client.indexes.historical_price_eod_full = AsyncMock(return_value=[])
    return m


class TestIndexesEod:
    @pytest.mark.asyncio
    async def test_uses_date_objects(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(enabled=True, interval="24h", extra={})
        h = build_indexes_eod(cfg, manager)
        await h.run_cycle()
        call = manager.cached_client.indexes.historical_price_eod_full.await_args_list[0]
        assert isinstance(call.args[1], date)
        assert isinstance(call.args[2], date)

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY
        assert "indexes_eod" in _REGISTRY
```

- [ ] **Step 13: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_chart_intraday.py tests/test_harvester/test_commodities_eod.py tests/test_harvester/test_forex_eod.py tests/test_harvester/test_indexes_eod.py -v`
Expected: all tests pass.

- [ ] **Step 14: Commit**

```bash
git add aiofmp/harvester/categories/chart_intraday.py \
        aiofmp/harvester/categories/commodities_eod.py \
        aiofmp/harvester/categories/commodities_intraday.py \
        aiofmp/harvester/categories/forex_eod.py \
        aiofmp/harvester/categories/forex_intraday.py \
        aiofmp/harvester/categories/indexes_eod.py \
        aiofmp/harvester/categories/indexes_intraday.py \
        aiofmp/harvester/categories/__init__.py \
        tests/test_harvester/test_chart_intraday.py \
        tests/test_harvester/test_commodities_eod.py \
        tests/test_harvester/test_forex_eod.py \
        tests/test_harvester/test_indexes_eod.py
git commit -m "feat(harvester): intraday + commodities/forex/indexes P3 categories"
```

---

### Task 18: `news` category (P3, multi-variant, no per-symbol iteration)

**Files:**
- Create: `aiofmp/harvester/categories/news.py`
- Modify: `aiofmp/harvester/categories/__init__.py` (add import)
- Create: `tests/test_harvester/test_news.py`

`news` differs slightly from the chart family: it's date-range with NO symbol (entity_key_args=[]). The harvester just calls each variant with `(from_date, to_date)` and lets CachedClient gap-fill.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_harvester/test_news.py`:

```python
"""Tests for the news category."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.news import build_news
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import RunStatus, StateStore


@pytest.fixture
def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite"); m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock(); m.config.retry = RetryConfig()
    m.cached_client = MagicMock()
    m.cached_client.news = MagicMock()
    for v in ("general_news", "press_releases", "stock_news", "crypto_news", "forex_news"):
        setattr(m.cached_client.news, v, AsyncMock(return_value=[]))
    return m


class TestNews:
    @pytest.mark.asyncio
    async def test_default_variants(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(enabled=True, interval="30m", extra={})
        h = build_news(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.status == RunStatus.OK
        # five variants, each called once
        for v in ("general_news", "press_releases", "stock_news", "crypto_news", "forex_news"):
            getattr(manager.cached_client.news, v).assert_awaited_once()

    @pytest.mark.asyncio
    async def test_custom_variants(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(
            enabled=True, interval="30m",
            extra={"variants": ["general_news"], "backfill_days_initial": 7, "page_size": 50},
        )
        h = build_news(cfg, manager)
        await h.run_cycle()
        call = manager.cached_client.news.general_news.await_args_list[0]
        # called as general_news(page=0, limit=50, from_date=<date>, to_date=<date>)
        assert call.kwargs["limit"] == 50
        assert isinstance(call.kwargs["from_date"], date)
        assert isinstance(call.kwargs["to_date"], date)

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY
        assert "news" in _REGISTRY
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_news.py -v`
Expected: ImportError.

- [ ] **Step 3: Create `aiofmp/harvester/categories/news.py`**

```python
"""news category — P3 over no entity (the call has from/to but no symbol)."""

from __future__ import annotations

import logging
from datetime import UTC, date, datetime, timedelta
from typing import TYPE_CHECKING

from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.state import RunStatus

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager

logger = logging.getLogger(__name__)

_DEFAULT_VARIANTS = ["general_news", "press_releases", "stock_news", "crypto_news", "forex_news"]


class NewsHarvester(CategoryHarvester):
    def __init__(self, cfg: CategoryConfig, manager: "HarvesterManager") -> None:
        super().__init__("news", cfg, manager.state, manager.budget, manager.config.retry)
        self._cached = manager.cached_client
        self._variants = list(cfg.extra.get("variants", _DEFAULT_VARIANTS))
        self._backfill_days = int(cfg.extra.get("backfill_days_initial", 30))
        self._page_size = int(cfg.extra.get("page_size", 100))

    async def run_cycle(self) -> RunOutcome:
        today = date.today()
        from_date = today - timedelta(days=self._backfill_days)
        attempted = 0
        succeeded = 0
        for v in self._variants:
            attempted += 1
            method = getattr(self._cached.news, v)
            try:
                await method(page=0, limit=self._page_size, from_date=from_date, to_date=today)
                succeeded += 1
            except Exception as exc:
                logger.warning("news.%s failed: %s", v, exc)
        status = RunStatus.OK if succeeded == attempted else RunStatus.PARTIAL
        return RunOutcome(status=status, items_attempted=attempted, items_succeeded=succeeded)


def build_news(cfg: CategoryConfig, manager: "HarvesterManager") -> NewsHarvester:
    return NewsHarvester(cfg, manager)


register_category("news", build_news)
```

- [ ] **Step 4: Register the module**

Update `aiofmp/harvester/categories/__init__.py` to include `news` in the import block at the bottom:

```python
from aiofmp.harvester.categories import (  # noqa: E402, F401
    chart_eod,
    chart_intraday,
    commodities_eod,
    commodities_intraday,
    forex_eod,
    forex_intraday,
    indexes_eod,
    indexes_intraday,
    news,
)
```

- [ ] **Step 5: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_news.py -v`
Expected: all 3 tests pass.

- [ ] **Step 6: Commit**

```bash
git add aiofmp/harvester/categories/news.py aiofmp/harvester/categories/__init__.py tests/test_harvester/test_news.py
git commit -m "feat(harvester): news category (P3 multi-variant)"
```

---

### Task 19: `economics` category (P3, treasury rates + indicator list)

**Files:**
- Create: `aiofmp/harvester/categories/economics.py`
- Modify: `aiofmp/harvester/categories/__init__.py`
- Create: `tests/test_harvester/test_economics.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_harvester/test_economics.py`:

```python
"""Tests for the economics category."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.economics import build_economics
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import StateStore


@pytest.fixture
def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite"); m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock(); m.config.retry = RetryConfig()
    m.cached_client = MagicMock()
    m.cached_client.economics = MagicMock()
    m.cached_client.economics.treasury_rates = AsyncMock(return_value=[])
    m.cached_client.economics.economic_indicators = AsyncMock(return_value=[])
    return m


class TestEconomics:
    @pytest.mark.asyncio
    async def test_default_indicators(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(enabled=True, interval="24h", extra={})
        h = build_economics(cfg, manager)
        outcome = await h.run_cycle()
        # 1 treasury_rates call + 5 default indicators
        assert outcome.items_attempted == 6
        manager.cached_client.economics.treasury_rates.assert_awaited_once()
        assert manager.cached_client.economics.economic_indicators.await_count == 5

    @pytest.mark.asyncio
    async def test_custom_indicators(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(
            enabled=True, interval="24h",
            extra={"indicators": ["GDP", "CPI"], "backfill_years": 3},
        )
        h = build_economics(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 3  # treasury + 2 indicators
        names_called = [c.args[0] for c in manager.cached_client.economics.economic_indicators.await_args_list]
        assert set(names_called) == {"GDP", "CPI"}

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY
        assert "economics" in _REGISTRY
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_economics.py -v`
Expected: ImportError.

- [ ] **Step 3: Create `aiofmp/harvester/categories/economics.py`**

```python
"""economics category — P3 (treasury_rates + per-indicator)."""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import TYPE_CHECKING

from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.state import RunStatus

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager

logger = logging.getLogger(__name__)

_DEFAULT_INDICATORS = ["GDP", "CPI", "UNRATE", "FEDFUNDS", "DFF"]


class EconomicsHarvester(CategoryHarvester):
    def __init__(self, cfg: CategoryConfig, manager: "HarvesterManager") -> None:
        super().__init__("economics", cfg, manager.state, manager.budget, manager.config.retry)
        self._cached = manager.cached_client
        self._indicators = list(cfg.extra.get("indicators", _DEFAULT_INDICATORS))
        self._backfill_years = int(cfg.extra.get("backfill_years", 10))

    async def run_cycle(self) -> RunOutcome:
        today = date.today()
        from_date = today - timedelta(days=self._backfill_years * 365)
        from_s, to_s = from_date.isoformat(), today.isoformat()
        attempted = 0
        succeeded = 0

        attempted += 1
        try:
            await self._cached.economics.treasury_rates(from_s, to_s)
            succeeded += 1
        except Exception as exc:
            logger.warning("economics.treasury_rates failed: %s", exc)

        for ind in self._indicators:
            attempted += 1
            try:
                await self._cached.economics.economic_indicators(ind, from_s, to_s)
                succeeded += 1
            except Exception as exc:
                logger.warning("economics.economic_indicators(%s) failed: %s", ind, exc)

        status = RunStatus.OK if succeeded == attempted else RunStatus.PARTIAL
        return RunOutcome(status=status, items_attempted=attempted, items_succeeded=succeeded)


def build_economics(cfg: CategoryConfig, manager: "HarvesterManager") -> EconomicsHarvester:
    return EconomicsHarvester(cfg, manager)


register_category("economics", build_economics)
```

- [ ] **Step 4: Register the module**

Update the import block at the bottom of `aiofmp/harvester/categories/__init__.py` to include `economics`:

```python
from aiofmp.harvester.categories import (  # noqa: E402, F401
    chart_eod,
    chart_intraday,
    commodities_eod,
    commodities_intraday,
    economics,
    forex_eod,
    forex_intraday,
    indexes_eod,
    indexes_intraday,
    news,
)
```

- [ ] **Step 5: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_economics.py -v`
Expected: all 3 tests pass.

- [ ] **Step 6: Commit**

```bash
git add aiofmp/harvester/categories/economics.py aiofmp/harvester/categories/__init__.py tests/test_harvester/test_economics.py
git commit -m "feat(harvester): economics category (treasury + indicators)"
```

---

### Task 20: `technical_indicators` category (P3, off by default)

**Files:**
- Create: `aiofmp/harvester/categories/technical_indicators.py`
- Modify: `aiofmp/harvester/categories/__init__.py`
- Create: `tests/test_harvester/test_technical_indicators.py`

Indicators are configured as a list of `{method, period_length, timeframe}` dicts.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_harvester/test_technical_indicators.py`:

```python
"""Tests for the technical_indicators category."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.technical_indicators import build_technical_indicators
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import RunStatus, StateStore


@pytest.fixture
def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite"); m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock(); m.config.retry = RetryConfig()
    m.catalog = MagicMock()
    m.catalog.symbols = AsyncMock(return_value=["AAPL", "MSFT"])
    m.cached_client = MagicMock()
    ti = MagicMock()
    ti.simple_moving_average = AsyncMock(return_value=[])
    ti.relative_strength_index = AsyncMock(return_value=[])
    m.cached_client.technical_indicators = ti
    return m


class TestTechnicalIndicators:
    @pytest.mark.asyncio
    async def test_empty_indicators_is_ok(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(enabled=True, interval="24h", extra={"indicators": []})
        h = build_technical_indicators(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.status == RunStatus.OK
        assert outcome.items_attempted == 0

    @pytest.mark.asyncio
    async def test_one_indicator_two_symbols(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(
            enabled=True, interval="24h",
            extra={
                "indicators": [
                    {"method": "simple_moving_average", "period_length": 20, "timeframe": "1day"}
                ],
            },
        )
        h = build_technical_indicators(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 2
        assert manager.cached_client.technical_indicators.simple_moving_average.await_count == 2
        first = manager.cached_client.technical_indicators.simple_moving_average.await_args_list[0]
        assert first.args[0] in ("AAPL", "MSFT")  # symbol
        assert first.args[1] == 20                # period_length
        assert first.args[2] == "1day"            # timeframe
        assert isinstance(first.args[3], date)    # from_date
        assert isinstance(first.args[4], date)    # to_date

    @pytest.mark.asyncio
    async def test_multiple_indicators(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(
            enabled=True, interval="24h",
            extra={
                "indicators": [
                    {"method": "simple_moving_average", "period_length": 20, "timeframe": "1day"},
                    {"method": "relative_strength_index", "period_length": 14, "timeframe": "1day"},
                ],
            },
        )
        h = build_technical_indicators(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 4  # 2 symbols * 2 indicators

    @pytest.mark.asyncio
    async def test_unknown_method_raises_at_build(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(
            enabled=True, interval="24h",
            extra={"indicators": [{"method": "moonshot", "period_length": 1, "timeframe": "1day"}]},
        )
        with pytest.raises(ValueError, match="moonshot"):
            build_technical_indicators(cfg, manager)

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY
        assert "technical_indicators" in _REGISTRY
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_technical_indicators.py -v`
Expected: ImportError.

- [ ] **Step 3: Create `aiofmp/harvester/categories/technical_indicators.py`**

```python
"""technical_indicators category — P3 per (symbol, indicator, period, timeframe)."""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import TYPE_CHECKING, Any

from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.state import RunStatus

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager

logger = logging.getLogger(__name__)

_VALID_METHODS = {
    "simple_moving_average",
    "exponential_moving_average",
    "weighted_moving_average",
    "double_exponential_moving_average",
    "triple_exponential_moving_average",
    "relative_strength_index",
    "standard_deviation",
    "williams_percent_r",
    "average_directional_index",
}


class TechnicalIndicatorsHarvester(CategoryHarvester):
    def __init__(self, cfg: CategoryConfig, manager: "HarvesterManager") -> None:
        super().__init__("technical_indicators", cfg, manager.state, manager.budget, manager.config.retry)
        self._catalog = manager.catalog
        self._cached = manager.cached_client
        self._universe = str(cfg.extra.get("symbol_universe", "actively_trading"))
        self._backfill_years = int(cfg.extra.get("backfill_years", 5))

        indicators: list[dict[str, Any]] = list(cfg.extra.get("indicators", []))
        for ind in indicators:
            if ind.get("method") not in _VALID_METHODS:
                raise ValueError(f"technical_indicators: unknown method {ind.get('method')!r}")
        self._indicators = indicators

    async def run_cycle(self) -> RunOutcome:
        if not self._indicators:
            return RunOutcome(status=RunStatus.OK)
        symbols = await self._catalog.symbols(self._universe)
        today = date.today()
        from_date = today - timedelta(days=self._backfill_years * 365)
        attempted = 0
        succeeded = 0
        for symbol in symbols:
            for ind in self._indicators:
                attempted += 1
                method_name = ind["method"]
                period_length = int(ind["period_length"])
                timeframe = str(ind["timeframe"])
                method = getattr(self._cached.technical_indicators, method_name)
                try:
                    await method(symbol, period_length, timeframe, from_date, today)
                    succeeded += 1
                except Exception as exc:
                    logger.warning(
                        "technical_indicators.%s(%s, %d, %s) failed: %s",
                        method_name, symbol, period_length, timeframe, exc,
                    )
        status = RunStatus.OK if succeeded == attempted else RunStatus.PARTIAL
        return RunOutcome(status=status, items_attempted=attempted, items_succeeded=succeeded)


def build_technical_indicators(cfg: CategoryConfig, manager: "HarvesterManager") -> TechnicalIndicatorsHarvester:
    return TechnicalIndicatorsHarvester(cfg, manager)


register_category("technical_indicators", build_technical_indicators)
```

- [ ] **Step 4: Register the module**

Add `technical_indicators` to the import block in `aiofmp/harvester/categories/__init__.py`:

```python
from aiofmp.harvester.categories import (  # noqa: E402, F401
    chart_eod,
    chart_intraday,
    commodities_eod,
    commodities_intraday,
    economics,
    forex_eod,
    forex_intraday,
    indexes_eod,
    indexes_intraday,
    news,
    technical_indicators,
)
```

- [ ] **Step 5: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_technical_indicators.py -v`
Expected: all 5 tests pass.

- [ ] **Step 6: Commit**

```bash
git add aiofmp/harvester/categories/technical_indicators.py aiofmp/harvester/categories/__init__.py tests/test_harvester/test_technical_indicators.py
git commit -m "feat(harvester): technical_indicators category (off by default)"
```

---

## Phase 4 — Pattern P1: statements

### Task 21: `statements` category (discover-then-fill + monthly safety-net)

**Files:**
- Create: `aiofmp/harvester/categories/statements.py`
- Modify: `aiofmp/harvester/categories/__init__.py`
- Create: `tests/test_harvester/test_statements.py`

The statements category uses two cooperating run-modes inside one harvester:
1. **Incremental cycle** (every `interval`): call `earnings_calendar(from=last_run, to=today)` → unique symbols → re-call the 13 statement endpoints per touched symbol with `limit=incremental_limit`.
2. **Safety-net cycle** (every `safety_net_interval`): enumerate every symbol in `financial_symbols` and call all 13 statement endpoints with `limit=incremental_limit`. Bookkept as a separate `category_runs` row with `category="statements_safetynet"`.

The checkpoint `("statements", "global")` stores the ISO date of the most recent earnings_calendar discovery.

The 13 statement endpoints fall into three sub-shapes:
- 10 with `(period, limit)`: income, balance, cash flow, key_metrics, ratios, enterprise_values, 4× growth
- 1 with `limit` only: owner_earnings
- 2 with `period` only (no limit): revenue_product_segmentation, revenue_geographic_segmentation

- [ ] **Step 1: Write the failing tests**

Create `tests/test_harvester/test_statements.py`:

```python
"""Tests for the statements category (P1)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.statements import (
    PERIOD_AND_LIMIT_ENDPOINTS,
    PERIOD_ONLY_ENDPOINTS,
    LIMIT_ONLY_ENDPOINTS,
    StatementsHarvester,
    build_statements,
)
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import RunStatus, StateStore


def _wire_statement_methods(stmts: MagicMock) -> None:
    for m in PERIOD_AND_LIMIT_ENDPOINTS + LIMIT_ONLY_ENDPOINTS + PERIOD_ONLY_ENDPOINTS:
        setattr(stmts, m, AsyncMock(return_value=[]))


@pytest.fixture
def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite"); m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock(); m.config.retry = RetryConfig()
    m.catalog = MagicMock()
    m.catalog.symbols = AsyncMock(return_value=["AAPL", "MSFT"])
    m.cached_client = MagicMock()
    m.cached_client.calendar = MagicMock()
    m.cached_client.calendar.earnings_calendar = AsyncMock(return_value=[])
    m.cached_client.statements = MagicMock()
    _wire_statement_methods(m.cached_client.statements)
    return m


def _expected_calls_per_symbol(periods: list[str]) -> int:
    # 10 period+limit endpoints × len(periods)
    n = len(PERIOD_AND_LIMIT_ENDPOINTS) * len(periods)
    # 1 limit-only endpoint
    n += len(LIMIT_ONLY_ENDPOINTS)
    # 2 period-only endpoints × len(periods)
    n += len(PERIOD_ONLY_ENDPOINTS) * len(periods)
    return n


class TestStatementsFirstRun:
    @pytest.mark.asyncio
    async def test_first_run_uses_initial_limit_and_full_universe(self, manager: MagicMock) -> None:
        """With no checkpoint set, first run iterates the financial_symbols universe with initial_limit."""
        cfg = CategoryConfig(enabled=True, interval="6h", extra={
            "periods": ["annual", "quarter"],
            "initial_limit": 40,
            "incremental_limit": 2,
        })
        h = build_statements(cfg, manager)
        outcome = await h.run_cycle()

        manager.catalog.symbols.assert_awaited_with("financial_symbols")
        expected = _expected_calls_per_symbol(["annual", "quarter"]) * 2  # 2 symbols
        assert outcome.items_attempted == expected
        # Verify limit=40 was passed to a period+limit endpoint
        first = manager.cached_client.statements.income_statement.await_args_list[0]
        assert first.kwargs.get("limit") == 40

    @pytest.mark.asyncio
    async def test_first_run_sets_checkpoint(self, manager: MagicMock) -> None:
        cfg = CategoryConfig(enabled=True, interval="6h", extra={"periods": ["annual"]})
        h = build_statements(cfg, manager)
        await h.run_cycle()
        ckpt = manager.state.get_checkpoint("statements", "global")
        assert ckpt is not None
        # Looks like a date string YYYY-MM-DD
        assert len(ckpt) == 10 and ckpt[4] == "-"


class TestStatementsIncremental:
    @pytest.mark.asyncio
    async def test_uses_earnings_calendar_when_checkpoint_exists(self, manager: MagicMock) -> None:
        manager.state.set_checkpoint("statements", "global", "2026-04-01")
        manager.cached_client.calendar.earnings_calendar = AsyncMock(
            return_value=[
                {"symbol": "AAPL", "date": "2026-04-25"},
                {"symbol": "AAPL", "date": "2026-04-26"},  # duplicate symbol
                {"symbol": "TSLA", "date": "2026-04-28"},
            ]
        )
        cfg = CategoryConfig(enabled=True, interval="6h", extra={
            "periods": ["annual"], "incremental_limit": 2,
        })
        h = build_statements(cfg, manager)
        outcome = await h.run_cycle()

        manager.cached_client.calendar.earnings_calendar.assert_awaited_once()
        # 2 unique symbols (AAPL, TSLA)
        expected = _expected_calls_per_symbol(["annual"]) * 2
        assert outcome.items_attempted == expected
        # Verify limit=2 was used
        first = manager.cached_client.statements.income_statement.await_args_list[0]
        assert first.kwargs.get("limit") == 2

    @pytest.mark.asyncio
    async def test_no_filings_in_window_is_noop(self, manager: MagicMock) -> None:
        manager.state.set_checkpoint("statements", "global", "2026-04-01")
        manager.cached_client.calendar.earnings_calendar = AsyncMock(return_value=[])
        cfg = CategoryConfig(enabled=True, interval="6h", extra={"periods": ["annual"]})
        h = build_statements(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.status == RunStatus.OK
        assert outcome.items_attempted == 0
        manager.cached_client.statements.income_statement.assert_not_awaited()


class TestStatementsSafetyNet:
    @pytest.mark.asyncio
    async def test_safety_net_triggers_after_interval(self, manager: MagicMock) -> None:
        # set an old "last safety-net" checkpoint
        manager.state.set_checkpoint(
            "statements_safetynet",
            "global",
            (datetime.now(UTC) - timedelta(days=40)).date().isoformat(),
        )
        manager.state.set_checkpoint("statements", "global", "2026-05-10")
        cfg = CategoryConfig(enabled=True, interval="6h", extra={
            "periods": ["annual"], "safety_net_interval": "30d",
        })
        h = build_statements(cfg, manager)
        outcome = await h.run_cycle()

        # Safety-net ran: should have iterated full universe (2 symbols)
        expected = _expected_calls_per_symbol(["annual"]) * 2
        assert outcome.items_attempted == expected
        # New safety-net checkpoint should be today
        new_ckpt = manager.state.get_checkpoint("statements_safetynet", "global")
        from datetime import date
        assert new_ckpt == date.today().isoformat()

    @pytest.mark.asyncio
    async def test_safety_net_skipped_when_recent(self, manager: MagicMock) -> None:
        manager.state.set_checkpoint(
            "statements_safetynet",
            "global",
            (datetime.now(UTC) - timedelta(days=5)).date().isoformat(),
        )
        manager.state.set_checkpoint("statements", "global", "2026-05-10")
        manager.cached_client.calendar.earnings_calendar = AsyncMock(return_value=[])
        cfg = CategoryConfig(enabled=True, interval="6h", extra={"periods": ["annual"]})
        h = build_statements(cfg, manager)
        outcome = await h.run_cycle()
        # No safety net, no filings discovered → 0 attempted
        assert outcome.items_attempted == 0


class TestRegistration:
    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY
        assert "statements" in _REGISTRY
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_statements.py -v`
Expected: ImportError.

- [ ] **Step 3: Create `aiofmp/harvester/categories/statements.py`**

```python
"""statements category — Pattern P1 (discover-then-fill) + monthly safety-net sweep."""

from __future__ import annotations

import logging
from datetime import UTC, date, datetime, timedelta
from typing import TYPE_CHECKING

from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig, parse_interval
from aiofmp.harvester.state import RunStatus

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager

logger = logging.getLogger(__name__)


# The 13 statement endpoints split by SDK signature shape.
PERIOD_AND_LIMIT_ENDPOINTS: list[str] = [
    "income_statement",
    "balance_sheet_statement",
    "cash_flow_statement",
    "key_metrics",
    "financial_ratios",
    "enterprise_values",
    "income_statement_growth",
    "balance_sheet_statement_growth",
    "cash_flow_statement_growth",
    "financial_statement_growth",
]

LIMIT_ONLY_ENDPOINTS: list[str] = [
    "owner_earnings",
]

PERIOD_ONLY_ENDPOINTS: list[str] = [
    "revenue_product_segmentation",
    "revenue_geographic_segmentation",
]


class StatementsHarvester(CategoryHarvester):
    def __init__(self, cfg: CategoryConfig, manager: "HarvesterManager") -> None:
        super().__init__("statements", cfg, manager.state, manager.budget, manager.config.retry)
        self._catalog = manager.catalog
        self._cached = manager.cached_client
        self._periods: list[str] = list(cfg.extra.get("periods", ["annual", "quarter"]))
        self._initial_limit = int(cfg.extra.get("initial_limit", 40))
        self._incremental_limit = int(cfg.extra.get("incremental_limit", 2))
        self._safety_net_seconds = parse_interval(str(cfg.extra.get("safety_net_interval", "30d")))

    async def run_cycle(self) -> RunOutcome:
        today = date.today()
        if self._should_run_safety_net(today):
            outcome = await self._run_safety_net(today)
            # Mark the safety-net last-run in a separate scope
            self.state.set_checkpoint("statements_safetynet", "global", today.isoformat())
            # Also bump primary checkpoint so incremental window doesn't span both
            self.state.set_checkpoint("statements", "global", today.isoformat())
            return outcome

        return await self._run_incremental(today)

    def _should_run_safety_net(self, today: date) -> bool:
        last = self.state.get_checkpoint("statements_safetynet", "global")
        if last is None:
            return True  # never ran a safety-net before → run one now
        try:
            last_d = date.fromisoformat(last)
        except ValueError:
            return True
        age_sec = (today - last_d).days * 86400
        return age_sec >= self._safety_net_seconds

    async def _run_safety_net(self, today: date) -> RunOutcome:
        symbols = await self._catalog.symbols("financial_symbols")
        return await self._iterate_symbols(symbols, self._incremental_limit)

    async def _run_incremental(self, today: date) -> RunOutcome:
        last = self.state.get_checkpoint("statements", "global")
        if last is None:
            # First run ever (and not yet a safety-net run): treat as full backfill
            symbols = await self._catalog.symbols("financial_symbols")
            outcome = await self._iterate_symbols(symbols, self._initial_limit)
            self.state.set_checkpoint("statements", "global", today.isoformat())
            return outcome

        try:
            from_date = date.fromisoformat(last)
        except ValueError:
            from_date = today - timedelta(days=30)

        from_s, to_s = from_date.isoformat(), today.isoformat()
        records = await self._cached.calendar.earnings_calendar(from_s, to_s)

        symbols = sorted({r["symbol"] for r in records if r.get("symbol")})
        outcome = await self._iterate_symbols(symbols, self._incremental_limit)
        self.state.set_checkpoint("statements", "global", today.isoformat())
        return outcome

    async def _iterate_symbols(self, symbols: list[str], limit: int) -> RunOutcome:
        if not symbols:
            return RunOutcome(status=RunStatus.OK)
        attempted = 0
        succeeded = 0
        for symbol in symbols:
            # 10 (period, limit) endpoints × periods
            for endpoint in PERIOD_AND_LIMIT_ENDPOINTS:
                for period in self._periods:
                    attempted += 1
                    method = getattr(self._cached.statements, endpoint)
                    try:
                        await method(symbol, limit=limit, period=period)
                        succeeded += 1
                    except Exception as exc:
                        logger.warning("statements.%s(%s, %s) failed: %s", endpoint, symbol, period, exc)
            # limit-only endpoints (owner_earnings)
            for endpoint in LIMIT_ONLY_ENDPOINTS:
                attempted += 1
                method = getattr(self._cached.statements, endpoint)
                try:
                    await method(symbol, limit=limit)
                    succeeded += 1
                except Exception as exc:
                    logger.warning("statements.%s(%s) failed: %s", endpoint, symbol, exc)
            # period-only endpoints (segmentation)
            for endpoint in PERIOD_ONLY_ENDPOINTS:
                for period in self._periods:
                    attempted += 1
                    method = getattr(self._cached.statements, endpoint)
                    try:
                        await method(symbol, period=period)
                        succeeded += 1
                    except Exception as exc:
                        logger.warning("statements.%s(%s, %s) failed: %s", endpoint, symbol, period, exc)
        status = RunStatus.OK if succeeded == attempted else RunStatus.PARTIAL
        return RunOutcome(status=status, items_attempted=attempted, items_succeeded=succeeded)


def build_statements(cfg: CategoryConfig, manager: "HarvesterManager") -> StatementsHarvester:
    return StatementsHarvester(cfg, manager)


register_category("statements", build_statements)
```

- [ ] **Step 4: Register the module**

Append `statements` to the import block in `aiofmp/harvester/categories/__init__.py`:

```python
from aiofmp.harvester.categories import (  # noqa: E402, F401
    chart_eod,
    chart_intraday,
    commodities_eod,
    commodities_intraday,
    economics,
    forex_eod,
    forex_intraday,
    indexes_eod,
    indexes_intraday,
    news,
    statements,
    technical_indicators,
)
```

- [ ] **Step 5: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_statements.py -v`
Expected: all 7 tests pass.

- [ ] **Step 6: Commit**

```bash
git add aiofmp/harvester/categories/statements.py aiofmp/harvester/categories/__init__.py tests/test_harvester/test_statements.py
git commit -m "feat(harvester): statements category (P1 + monthly safety-net)"
```

---

## Phase 5 — Pattern P2: page-walk categories

### Task 22: `analyst_estimates` category (per-symbol walk-back)

**Files:**
- Create: `aiofmp/harvester/categories/analyst_estimates.py`
- Modify: `aiofmp/harvester/categories/__init__.py`
- Create: `tests/test_harvester/test_analyst_estimates.py`

The harvester walks `analyst.financial_estimates(symbol, period, page=N, limit=page_size)` page-by-page, accumulating records and stopping when the oldest record on the current page is older than `max(last_checkpoint, today - max_backfill_years)`. Writes go directly to `ParquetStorage` under the same key the PAGE_WALK registry uses, so user reads via `cached.analyst.financial_estimates(...)` return harvester-written data.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_harvester/test_analyst_estimates.py`:

```python
"""Tests for analyst_estimates category (P2 per-symbol page walk)."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.cachedclient.storage.parquet import ParquetStorage
from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.analyst_estimates import build_analyst_estimates
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import RunStatus, StateStore


def _row(d: str) -> dict[str, Any]:
    return {"symbol": "AAPL", "date": d, "revenueAvg": 100}


@pytest.fixture
async def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite"); m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock(); m.config.retry = RetryConfig()
    m.catalog = MagicMock()
    m.catalog.symbols = AsyncMock(return_value=["AAPL"])

    m.fmp_client = MagicMock()
    m.fmp_client.analyst = MagicMock()
    m.fmp_client.analyst.financial_estimates = AsyncMock()

    storage = ParquetStorage(tmp_path)
    await storage.initialize()
    m.cached_client = MagicMock()
    m.cached_client.storage = storage
    return m


class TestAnalystEstimates:
    @pytest.mark.asyncio
    async def test_first_run_walks_until_max_backfill(self, manager) -> None:
        today = date.today()
        manager.fmp_client.analyst.financial_estimates.side_effect = [
            [_row((today - timedelta(days=400)).isoformat())],
            [_row((today - timedelta(days=800)).isoformat())],
            [_row((today - timedelta(days=1200)).isoformat())],  # > 3y backfill -> stop after this
            [],  # safety
        ]
        cfg = CategoryConfig(enabled=True, interval="24h", extra={
            "estimate_periods": ["annual"],
            "max_backfill_years": 3,
            "page_size": 1,
        })
        h = build_analyst_estimates(cfg, manager)
        outcome = await h.run_cycle()

        assert outcome.status == RunStatus.OK
        # 3 pages walked (oldest = 1200d > 3*365 = 1095, so we stop after that page)
        assert manager.fmp_client.analyst.financial_estimates.await_count == 3
        ckpt = manager.state.get_checkpoint("analyst_estimates", "AAPL/annual")
        assert ckpt is not None

    @pytest.mark.asyncio
    async def test_subsequent_run_walks_until_checkpoint(self, manager) -> None:
        manager.state.set_checkpoint("analyst_estimates", "AAPL/annual", "2024-06-01")
        manager.fmp_client.analyst.financial_estimates.side_effect = [
            [_row("2024-12-31"), _row("2024-09-30")],
            [_row("2024-07-31"), _row("2024-04-30")],  # 2024-04-30 < 2024-06-01 -> stop
        ]
        cfg = CategoryConfig(enabled=True, interval="24h", extra={
            "estimate_periods": ["annual"],
            "max_backfill_years": 3,
            "page_size": 2,
        })
        h = build_analyst_estimates(cfg, manager)
        outcome = await h.run_cycle()
        assert manager.fmp_client.analyst.financial_estimates.await_count == 2
        assert outcome.status == RunStatus.OK

    @pytest.mark.asyncio
    async def test_empty_page_stops_walk(self, manager) -> None:
        manager.fmp_client.analyst.financial_estimates.side_effect = [
            [_row("2025-01-01")],
            [],
        ]
        cfg = CategoryConfig(enabled=True, interval="24h", extra={"estimate_periods": ["annual"]})
        h = build_analyst_estimates(cfg, manager)
        await h.run_cycle()
        assert manager.fmp_client.analyst.financial_estimates.await_count == 2

    @pytest.mark.asyncio
    async def test_writes_to_storage_at_expected_key(self, manager) -> None:
        manager.fmp_client.analyst.financial_estimates.side_effect = [
            [_row("2025-12-31")],
            [],
        ]
        cfg = CategoryConfig(enabled=True, interval="24h", extra={"estimate_periods": ["annual"]})
        h = build_analyst_estimates(cfg, manager)
        await h.run_cycle()
        records = await manager.cached_client.storage.read(("analyst-estimates", "AAPL", "annual"))
        assert len(records) >= 1
        assert records[0]["date"] == "2025-12-31"

    @pytest.mark.asyncio
    async def test_per_symbol_error_does_not_stop_cycle(self, manager) -> None:
        manager.catalog.symbols = AsyncMock(return_value=["AAPL", "MSFT"])

        async def side_effect(symbol, period, page=0, limit=100):
            if symbol == "MSFT":
                raise RuntimeError("blown")
            return [_row("2025-12-31")] if page == 0 else []

        manager.fmp_client.analyst.financial_estimates = AsyncMock(side_effect=side_effect)
        cfg = CategoryConfig(enabled=True, interval="24h", extra={"estimate_periods": ["annual"]})
        h = build_analyst_estimates(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 2
        assert outcome.items_succeeded == 1
        assert outcome.status == RunStatus.PARTIAL

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY
        assert "analyst_estimates" in _REGISTRY
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_analyst_estimates.py -v`
Expected: ImportError.

- [ ] **Step 3: Create `aiofmp/harvester/categories/analyst_estimates.py`**

```python
"""analyst_estimates category — Pattern P2 (per-symbol page walk)."""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import TYPE_CHECKING, Any

from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.state import RunStatus

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager

logger = logging.getLogger(__name__)

_STORAGE_PREFIX = "analyst-estimates"
_MAX_PAGES_SAFETY = 1000


def _parse_iso(d: str | None) -> date | None:
    if not d:
        return None
    try:
        return date.fromisoformat(str(d)[:10])
    except ValueError:
        return None


class AnalystEstimatesHarvester(CategoryHarvester):
    def __init__(self, cfg: CategoryConfig, manager: "HarvesterManager") -> None:
        super().__init__("analyst_estimates", cfg, manager.state, manager.budget, manager.config.retry)
        self._catalog = manager.catalog
        self._fmp = manager.fmp_client
        self._storage = manager.cached_client.storage
        self._periods: list[str] = list(cfg.extra.get("estimate_periods", ["annual"]))
        self._max_backfill_days = int(cfg.extra.get("max_backfill_years", 3)) * 365
        self._page_size = int(cfg.extra.get("page_size", 100))

    async def run_cycle(self) -> RunOutcome:
        symbols = await self._catalog.symbols("actively_trading")
        attempted = 0
        succeeded = 0
        for symbol in symbols:
            for period in self._periods:
                attempted += 1
                try:
                    await self._walk_symbol(symbol, period)
                    succeeded += 1
                except Exception as exc:
                    logger.warning(
                        "analyst_estimates walk failed for %s/%s: %s", symbol, period, exc,
                    )
        status = RunStatus.OK if succeeded == attempted else RunStatus.PARTIAL
        return RunOutcome(status=status, items_attempted=attempted, items_succeeded=succeeded)

    async def _walk_symbol(self, symbol: str, period: str) -> None:
        scope = f"{symbol}/{period}"
        last_ckpt = _parse_iso(self.state.get_checkpoint("analyst_estimates", scope))
        max_backfill = date.today() - timedelta(days=self._max_backfill_days)
        stop_at: date = last_ckpt if last_ckpt and last_ckpt > max_backfill else max_backfill

        storage_key = (_STORAGE_PREFIX, symbol, period)
        all_records: list[dict[str, Any]] = []
        newest_seen: date | None = None

        for page in range(_MAX_PAGES_SAFETY):
            records = await self._fmp.analyst.financial_estimates(
                symbol, period, page=page, limit=self._page_size
            )
            if not records:
                break
            all_records.extend(records)
            page_dates = [_parse_iso(r.get("date")) for r in records]
            page_dates = [d for d in page_dates if d is not None]
            if not page_dates:
                # Defensive: if no parseable dates on this page, stop to avoid infinite loop
                break
            oldest_on_page = min(page_dates)
            page_newest = max(page_dates)
            if newest_seen is None or page_newest > newest_seen:
                newest_seen = page_newest
            if oldest_on_page <= stop_at:
                break

        if all_records:
            # Merge with existing storage (dedup by date)
            existing = await self._storage.read(storage_key)
            seen = {r.get("date") for r in existing}
            for r in all_records:
                if r.get("date") not in seen:
                    existing.append(r)
                    seen.add(r.get("date"))
            existing.sort(key=lambda r: str(r.get("date", "")), reverse=True)
            await self._storage.write(storage_key, existing, date_field="date")

        if newest_seen is not None:
            self.state.set_checkpoint("analyst_estimates", scope, newest_seen.isoformat())


def build_analyst_estimates(cfg: CategoryConfig, manager: "HarvesterManager") -> AnalystEstimatesHarvester:
    return AnalystEstimatesHarvester(cfg, manager)


register_category("analyst_estimates", build_analyst_estimates)
```

- [ ] **Step 4: Register the module**

Add `analyst_estimates` to the import block in `aiofmp/harvester/categories/__init__.py`:

```python
from aiofmp.harvester.categories import (  # noqa: E402, F401
    analyst_estimates,
    chart_eod,
    chart_intraday,
    commodities_eod,
    commodities_intraday,
    economics,
    forex_eod,
    forex_intraday,
    indexes_eod,
    indexes_intraday,
    news,
    statements,
    technical_indicators,
)
```

- [ ] **Step 5: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_analyst_estimates.py -v`
Expected: all 6 tests pass.

- [ ] **Step 6: Commit**

```bash
git add aiofmp/harvester/categories/analyst_estimates.py aiofmp/harvester/categories/__init__.py tests/test_harvester/test_analyst_estimates.py
git commit -m "feat(harvester): analyst_estimates category (P2 per-symbol walk)"
```

---

### Task 23: `insider_trades` category (global walk, per-symbol shard)

**Files:**
- Create: `aiofmp/harvester/categories/insider_trades.py`
- Modify: `aiofmp/harvester/categories/__init__.py`
- Create: `tests/test_harvester/test_insider_trades.py`

A single global walk of `insider_trades.latest_insider_trades(page=N, limit=page_size)`; results are sharded into per-symbol parquet files keyed by `("insider-trading/latest", symbol)`, with the raw global stream also written to `("insider-trading/latest", "_global")`.

Stop condition: oldest `filingDate` in page is older than `last_checkpoint`, OR page is empty, OR `page >= max_pages`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_harvester/test_insider_trades.py`:

```python
"""Tests for insider_trades category (P2 global walk, per-symbol shard)."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.cachedclient.storage.parquet import ParquetStorage
from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.insider_trades import build_insider_trades
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import RunStatus, StateStore


def _trade(symbol: str, d: str) -> dict[str, Any]:
    return {"symbol": symbol, "filingDate": d, "transactionType": "P-Purchase"}


@pytest.fixture
async def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite"); m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock(); m.config.retry = RetryConfig()
    m.fmp_client = MagicMock()
    m.fmp_client.insider_trades = MagicMock()
    m.fmp_client.insider_trades.latest_insider_trades = AsyncMock()
    storage = ParquetStorage(tmp_path)
    await storage.initialize()
    m.cached_client = MagicMock()
    m.cached_client.storage = storage
    return m


class TestInsiderTrades:
    @pytest.mark.asyncio
    async def test_first_run_walks_until_max_pages(self, manager) -> None:
        manager.fmp_client.insider_trades.latest_insider_trades.side_effect = [
            [_trade("AAPL", "2026-05-01"), _trade("MSFT", "2026-05-01")],
            [_trade("AAPL", "2026-04-25"), _trade("GOOGL", "2026-04-24")],
            [],  # stops the walk
        ]
        cfg = CategoryConfig(enabled=True, interval="6h", extra={
            "max_pages": 10, "page_size": 2,
        })
        h = build_insider_trades(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.status == RunStatus.OK
        assert manager.fmp_client.insider_trades.latest_insider_trades.await_count == 3

    @pytest.mark.asyncio
    async def test_subsequent_run_stops_at_checkpoint(self, manager) -> None:
        manager.state.set_checkpoint("insider_trades", "global", "2026-04-30")
        manager.fmp_client.insider_trades.latest_insider_trades.side_effect = [
            [_trade("AAPL", "2026-05-02")],
            [_trade("MSFT", "2026-04-25")],  # < checkpoint -> stop after this page
            [_trade("X", "2020-01-01")],
        ]
        cfg = CategoryConfig(enabled=True, interval="6h", extra={"page_size": 1, "max_pages": 10})
        h = build_insider_trades(cfg, manager)
        await h.run_cycle()
        assert manager.fmp_client.insider_trades.latest_insider_trades.await_count == 2

    @pytest.mark.asyncio
    async def test_shards_by_symbol(self, manager) -> None:
        manager.fmp_client.insider_trades.latest_insider_trades.side_effect = [
            [_trade("AAPL", "2026-05-01"), _trade("MSFT", "2026-05-01")],
            [],
        ]
        cfg = CategoryConfig(enabled=True, interval="6h", extra={})
        h = build_insider_trades(cfg, manager)
        await h.run_cycle()
        aapl_rows = await manager.cached_client.storage.read(("insider-trading/latest", "AAPL"))
        msft_rows = await manager.cached_client.storage.read(("insider-trading/latest", "MSFT"))
        global_rows = await manager.cached_client.storage.read(("insider-trading/latest", "_global"))
        assert any(r["symbol"] == "AAPL" for r in aapl_rows)
        assert any(r["symbol"] == "MSFT" for r in msft_rows)
        assert len(global_rows) == 2

    @pytest.mark.asyncio
    async def test_max_pages_safety(self, manager) -> None:
        manager.fmp_client.insider_trades.latest_insider_trades.return_value = [_trade("AAPL", "2026-05-01")]
        cfg = CategoryConfig(enabled=True, interval="6h", extra={"max_pages": 3, "page_size": 1})
        h = build_insider_trades(cfg, manager)
        await h.run_cycle()
        assert manager.fmp_client.insider_trades.latest_insider_trades.await_count == 3

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY
        assert "insider_trades" in _REGISTRY
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_insider_trades.py -v`
Expected: ImportError.

- [ ] **Step 3: Create `aiofmp/harvester/categories/insider_trades.py`**

```python
"""insider_trades category — Pattern P2 (global walk; per-symbol shard on write)."""

from __future__ import annotations

import logging
from collections import defaultdict
from datetime import date
from typing import TYPE_CHECKING, Any

from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.state import RunStatus

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager

logger = logging.getLogger(__name__)

_STORAGE_PREFIX = "insider-trading/latest"


def _parse_iso(d: str | None) -> date | None:
    if not d:
        return None
    try:
        return date.fromisoformat(str(d)[:10])
    except ValueError:
        return None


class InsiderTradesHarvester(CategoryHarvester):
    def __init__(self, cfg: CategoryConfig, manager: "HarvesterManager") -> None:
        super().__init__("insider_trades", cfg, manager.state, manager.budget, manager.config.retry)
        self._fmp = manager.fmp_client
        self._storage = manager.cached_client.storage
        self._max_pages = int(cfg.extra.get("max_pages", 200))
        self._page_size = int(cfg.extra.get("page_size", 100))

    async def run_cycle(self) -> RunOutcome:
        last_ckpt = _parse_iso(self.state.get_checkpoint("insider_trades", "global"))
        all_records: list[dict[str, Any]] = []
        newest_seen: date | None = None

        for page in range(self._max_pages):
            records = await self._fmp.insider_trades.latest_insider_trades(page=page, limit=self._page_size)
            if not records:
                break
            all_records.extend(records)
            page_dates = [_parse_iso(r.get("filingDate")) for r in records]
            page_dates = [d for d in page_dates if d is not None]
            if page_dates:
                page_newest = max(page_dates)
                page_oldest = min(page_dates)
                if newest_seen is None or page_newest > newest_seen:
                    newest_seen = page_newest
                if last_ckpt is not None and page_oldest <= last_ckpt:
                    break

        if all_records:
            await self._persist(all_records)

        if newest_seen is not None:
            self.state.set_checkpoint("insider_trades", "global", newest_seen.isoformat())

        return RunOutcome(
            status=RunStatus.OK,
            items_attempted=len(all_records),
            items_succeeded=len(all_records),
        )

    async def _persist(self, records: list[dict[str, Any]]) -> None:
        # Global stream
        global_key = (_STORAGE_PREFIX, "_global")
        existing_global = await self._storage.read(global_key)
        seen_global = {(r.get("symbol"), r.get("filingDate"), r.get("transactionType")) for r in existing_global}
        for r in records:
            tup = (r.get("symbol"), r.get("filingDate"), r.get("transactionType"))
            if tup not in seen_global:
                existing_global.append(r)
                seen_global.add(tup)
        existing_global.sort(key=lambda r: str(r.get("filingDate", "")), reverse=True)
        await self._storage.write(global_key, existing_global, date_field="filingDate")

        # Per-symbol shard
        by_symbol: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for r in records:
            sym = r.get("symbol")
            if sym:
                by_symbol[str(sym)].append(r)
        for sym, rows in by_symbol.items():
            key = (_STORAGE_PREFIX, sym)
            existing = await self._storage.read(key)
            seen = {(r.get("filingDate"), r.get("transactionType")) for r in existing}
            for r in rows:
                tup = (r.get("filingDate"), r.get("transactionType"))
                if tup not in seen:
                    existing.append(r)
                    seen.add(tup)
            existing.sort(key=lambda r: str(r.get("filingDate", "")), reverse=True)
            await self._storage.write(key, existing, date_field="filingDate")


def build_insider_trades(cfg: CategoryConfig, manager: "HarvesterManager") -> InsiderTradesHarvester:
    return InsiderTradesHarvester(cfg, manager)


register_category("insider_trades", build_insider_trades)
```

- [ ] **Step 4: Register the module**

Add `insider_trades` to the import block:

```python
from aiofmp.harvester.categories import (  # noqa: E402, F401
    analyst_estimates,
    chart_eod,
    chart_intraday,
    commodities_eod,
    commodities_intraday,
    economics,
    forex_eod,
    forex_intraday,
    indexes_eod,
    indexes_intraday,
    insider_trades,
    news,
    statements,
    technical_indicators,
)
```

- [ ] **Step 5: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_insider_trades.py -v`
Expected: all 5 tests pass.

- [ ] **Step 6: Commit**

```bash
git add aiofmp/harvester/categories/insider_trades.py aiofmp/harvester/categories/__init__.py tests/test_harvester/test_insider_trades.py
git commit -m "feat(harvester): insider_trades category (P2 global walk, per-symbol shard)"
```

---

### Task 24: `form13f` category (global walk, per-CIK shard)

**Files:**
- Create: `aiofmp/harvester/categories/form13f.py`
- Modify: `aiofmp/harvester/categories/__init__.py`
- Create: `tests/test_harvester/test_form13f.py`

Identical pattern to insider_trades but the walk target is `form13f.latest_filings(page=N, limit=page_size)`, sharded by `cik` instead of `symbol`, and the walk date field is `acceptedDate`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_harvester/test_form13f.py`:

```python
"""Tests for form13f category (P2 global walk, per-CIK shard)."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.cachedclient.storage.parquet import ParquetStorage
from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.form13f import build_form13f
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import StateStore


def _filing(cik: str, d: str) -> dict[str, Any]:
    return {"cik": cik, "acceptedDate": d, "name": "TestFund"}


@pytest.fixture
async def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite"); m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock(); m.config.retry = RetryConfig()
    m.fmp_client = MagicMock()
    m.fmp_client.form13f = MagicMock()
    m.fmp_client.form13f.latest_filings = AsyncMock()
    storage = ParquetStorage(tmp_path)
    await storage.initialize()
    m.cached_client = MagicMock()
    m.cached_client.storage = storage
    return m


class TestForm13F:
    @pytest.mark.asyncio
    async def test_walks_until_empty(self, manager) -> None:
        manager.fmp_client.form13f.latest_filings.side_effect = [
            [_filing("0001067983", "2026-05-01"), _filing("0001067900", "2026-05-01")],
            [_filing("0001067983", "2026-04-28")],
            [],
        ]
        cfg = CategoryConfig(enabled=True, interval="24h", extra={"max_pages": 10, "page_size": 2})
        h = build_form13f(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 3
        assert manager.fmp_client.form13f.latest_filings.await_count == 3

    @pytest.mark.asyncio
    async def test_stops_at_checkpoint(self, manager) -> None:
        manager.state.set_checkpoint("form13f", "global", "2026-04-29")
        manager.fmp_client.form13f.latest_filings.side_effect = [
            [_filing("0001067983", "2026-05-01")],
            [_filing("0001067900", "2026-04-20")],  # < checkpoint -> stop after this page
            [_filing("0001067", "2020-01-01")],
        ]
        cfg = CategoryConfig(enabled=True, interval="24h", extra={"page_size": 1, "max_pages": 5})
        h = build_form13f(cfg, manager)
        await h.run_cycle()
        assert manager.fmp_client.form13f.latest_filings.await_count == 2

    @pytest.mark.asyncio
    async def test_shards_by_cik(self, manager) -> None:
        manager.fmp_client.form13f.latest_filings.side_effect = [
            [_filing("0001067983", "2026-05-01"), _filing("0001067900", "2026-05-01")],
            [],
        ]
        cfg = CategoryConfig(enabled=True, interval="24h", extra={})
        h = build_form13f(cfg, manager)
        await h.run_cycle()
        berkshire = await manager.cached_client.storage.read(("institutional-ownership/latest", "0001067983"))
        other = await manager.cached_client.storage.read(("institutional-ownership/latest", "0001067900"))
        global_rows = await manager.cached_client.storage.read(("institutional-ownership/latest", "_global"))
        assert len(berkshire) == 1
        assert len(other) == 1
        assert len(global_rows) == 2

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY
        assert "form13f" in _REGISTRY
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_form13f.py -v`
Expected: ImportError.

- [ ] **Step 3: Create `aiofmp/harvester/categories/form13f.py`**

```python
"""form13f category — Pattern P2 (global walk; per-CIK shard on write)."""

from __future__ import annotations

import logging
from collections import defaultdict
from datetime import date
from typing import TYPE_CHECKING, Any

from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.state import RunStatus

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager

logger = logging.getLogger(__name__)

_STORAGE_PREFIX = "institutional-ownership/latest"


def _parse_iso(d: str | None) -> date | None:
    if not d:
        return None
    try:
        return date.fromisoformat(str(d)[:10])
    except ValueError:
        return None


class Form13FHarvester(CategoryHarvester):
    def __init__(self, cfg: CategoryConfig, manager: "HarvesterManager") -> None:
        super().__init__("form13f", cfg, manager.state, manager.budget, manager.config.retry)
        self._fmp = manager.fmp_client
        self._storage = manager.cached_client.storage
        self._max_pages = int(cfg.extra.get("max_pages", 50))
        self._page_size = int(cfg.extra.get("page_size", 100))

    async def run_cycle(self) -> RunOutcome:
        last_ckpt = _parse_iso(self.state.get_checkpoint("form13f", "global"))
        all_records: list[dict[str, Any]] = []
        newest_seen: date | None = None

        for page in range(self._max_pages):
            records = await self._fmp.form13f.latest_filings(page=page, limit=self._page_size)
            if not records:
                break
            all_records.extend(records)
            page_dates = [_parse_iso(r.get("acceptedDate")) for r in records]
            page_dates = [d for d in page_dates if d is not None]
            if page_dates:
                page_newest = max(page_dates)
                page_oldest = min(page_dates)
                if newest_seen is None or page_newest > newest_seen:
                    newest_seen = page_newest
                if last_ckpt is not None and page_oldest <= last_ckpt:
                    break

        if all_records:
            await self._persist(all_records)

        if newest_seen is not None:
            self.state.set_checkpoint("form13f", "global", newest_seen.isoformat())

        return RunOutcome(
            status=RunStatus.OK,
            items_attempted=len(all_records),
            items_succeeded=len(all_records),
        )

    async def _persist(self, records: list[dict[str, Any]]) -> None:
        global_key = (_STORAGE_PREFIX, "_global")
        existing_global = await self._storage.read(global_key)
        seen_global = {(r.get("cik"), r.get("acceptedDate")) for r in existing_global}
        for r in records:
            tup = (r.get("cik"), r.get("acceptedDate"))
            if tup not in seen_global:
                existing_global.append(r)
                seen_global.add(tup)
        existing_global.sort(key=lambda r: str(r.get("acceptedDate", "")), reverse=True)
        await self._storage.write(global_key, existing_global, date_field="acceptedDate")

        by_cik: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for r in records:
            cik = r.get("cik")
            if cik:
                by_cik[str(cik)].append(r)
        for cik, rows in by_cik.items():
            key = (_STORAGE_PREFIX, cik)
            existing = await self._storage.read(key)
            seen = {r.get("acceptedDate") for r in existing}
            for r in rows:
                if r.get("acceptedDate") not in seen:
                    existing.append(r)
                    seen.add(r.get("acceptedDate"))
            existing.sort(key=lambda r: str(r.get("acceptedDate", "")), reverse=True)
            await self._storage.write(key, existing, date_field="acceptedDate")


def build_form13f(cfg: CategoryConfig, manager: "HarvesterManager") -> Form13FHarvester:
    return Form13FHarvester(cfg, manager)


register_category("form13f", build_form13f)
```

- [ ] **Step 4: Register the module**

Add `form13f` to the import block:

```python
from aiofmp.harvester.categories import (  # noqa: E402, F401
    analyst_estimates,
    chart_eod,
    chart_intraday,
    commodities_eod,
    commodities_intraday,
    economics,
    forex_eod,
    forex_intraday,
    form13f,
    indexes_eod,
    indexes_intraday,
    insider_trades,
    news,
    statements,
    technical_indicators,
)
```

- [ ] **Step 5: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_form13f.py -v`
Expected: all 4 tests pass.

- [ ] **Step 6: Commit**

```bash
git add aiofmp/harvester/categories/form13f.py aiofmp/harvester/categories/__init__.py tests/test_harvester/test_form13f.py
git commit -m "feat(harvester): form13f category (P2 global walk, per-CIK shard)"
```

---

## Phase 6 — Pattern P4: snapshot-overwrite categories

### Task 25: `analyst_snapshots` category

**Files:**
- Create: `aiofmp/harvester/categories/analyst_snapshots.py`
- Modify: `aiofmp/harvester/categories/__init__.py`
- Create: `tests/test_harvester/test_analyst_snapshots.py`

Per symbol in `actively_trading`, fetch the configured snapshot endpoints from `client.analyst.*` and overwrite via `SnapshotStore`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_harvester/test_analyst_snapshots.py`:

```python
"""Tests for analyst_snapshots category (P4 snapshot overwrite)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.cachedclient.snapshot_store import SnapshotStore
from aiofmp.cachedclient.storage.parquet import ParquetStorage
from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.analyst_snapshots import build_analyst_snapshots
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import RunStatus, StateStore


@pytest.fixture
async def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite"); m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock(); m.config.retry = RetryConfig()
    m.catalog = MagicMock()
    m.catalog.symbols = AsyncMock(return_value=["AAPL"])
    m.fmp_client = MagicMock()
    m.fmp_client.analyst = MagicMock()
    m.fmp_client.analyst.ratings_snapshot = AsyncMock(return_value=[{"symbol": "AAPL", "rating": "A-"}])
    m.fmp_client.analyst.price_target_consensus = AsyncMock(return_value=[{"symbol": "AAPL", "targetConsensus": 250}])
    m.fmp_client.analyst.price_target_summary = AsyncMock(return_value=[{"symbol": "AAPL"}])
    m.fmp_client.analyst.stock_grades_summary = AsyncMock(return_value=[{"symbol": "AAPL", "consensus": "Buy"}])
    storage = ParquetStorage(tmp_path)
    await storage.initialize()
    m.cached_client = MagicMock()
    m.cached_client.storage = storage
    return m


class TestAnalystSnapshots:
    @pytest.mark.asyncio
    async def test_default_endpoints(self, manager) -> None:
        cfg = CategoryConfig(enabled=True, interval="24h", extra={})
        h = build_analyst_snapshots(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.status == RunStatus.OK
        # 1 symbol * 4 default endpoints
        assert outcome.items_attempted == 4

        ss = SnapshotStore(manager.cached_client.storage)
        row = await ss.read("ratings-snapshot", "AAPL")
        assert row is not None
        assert row["rating"] == "A-"

    @pytest.mark.asyncio
    async def test_custom_endpoint_list(self, manager) -> None:
        cfg = CategoryConfig(enabled=True, interval="24h", extra={"include": ["ratings_snapshot"]})
        h = build_analyst_snapshots(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 1
        manager.fmp_client.analyst.price_target_consensus.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_empty_response_skips_write(self, manager) -> None:
        manager.fmp_client.analyst.ratings_snapshot = AsyncMock(return_value=[])
        cfg = CategoryConfig(enabled=True, interval="24h", extra={"include": ["ratings_snapshot"]})
        h = build_analyst_snapshots(cfg, manager)
        await h.run_cycle()
        ss = SnapshotStore(manager.cached_client.storage)
        assert await ss.read("ratings-snapshot", "AAPL") is None

    @pytest.mark.asyncio
    async def test_per_endpoint_error_does_not_kill_cycle(self, manager) -> None:
        manager.fmp_client.analyst.ratings_snapshot = AsyncMock(side_effect=RuntimeError("boom"))
        cfg = CategoryConfig(enabled=True, interval="24h", extra={
            "include": ["ratings_snapshot", "price_target_consensus"]
        })
        h = build_analyst_snapshots(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 2
        assert outcome.items_succeeded == 1
        assert outcome.status == RunStatus.PARTIAL

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY
        assert "analyst_snapshots" in _REGISTRY
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_analyst_snapshots.py -v`
Expected: ImportError.

- [ ] **Step 3: Create `aiofmp/harvester/categories/analyst_snapshots.py`**

```python
"""analyst_snapshots category — Pattern P4 (snapshot overwrite per symbol)."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from aiofmp.cachedclient.snapshot_store import SnapshotStore
from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.state import RunStatus

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager

logger = logging.getLogger(__name__)


# Maps the YAML "include" name -> (SDK method on client.analyst, snapshot endpoint key).
_INCLUDE_MAP: dict[str, tuple[str, str]] = {
    "ratings_snapshot": ("ratings_snapshot", "ratings-snapshot"),
    "price_target_consensus": ("price_target_consensus", "price-target-consensus"),
    "price_target_summary": ("price_target_summary", "price-target-summary"),
    "stock_grades_summary": ("stock_grades_summary", "grades-consensus"),
}

_DEFAULT_INCLUDE = list(_INCLUDE_MAP.keys())


class AnalystSnapshotsHarvester(CategoryHarvester):
    def __init__(self, cfg: CategoryConfig, manager: "HarvesterManager") -> None:
        super().__init__("analyst_snapshots", cfg, manager.state, manager.budget, manager.config.retry)
        self._catalog = manager.catalog
        self._fmp = manager.fmp_client
        self._snapshots = SnapshotStore(manager.cached_client.storage)
        include = list(cfg.extra.get("include", _DEFAULT_INCLUDE))
        for n in include:
            if n not in _INCLUDE_MAP:
                raise ValueError(f"analyst_snapshots: unknown include {n!r}")
        self._include = include

    async def run_cycle(self) -> RunOutcome:
        symbols = await self._catalog.symbols("actively_trading")
        attempted = 0
        succeeded = 0
        for symbol in symbols:
            for name in self._include:
                attempted += 1
                method_name, endpoint = _INCLUDE_MAP[name]
                method = getattr(self._fmp.analyst, method_name)
                try:
                    rows = await method(symbol)
                    payload = rows[0] if isinstance(rows, list) and rows else None
                    if payload:
                        await self._snapshots.write(endpoint, symbol, payload)
                    succeeded += 1
                except Exception as exc:
                    logger.warning(
                        "analyst_snapshots.%s(%s) failed: %s", method_name, symbol, exc,
                    )
        status = RunStatus.OK if succeeded == attempted else RunStatus.PARTIAL
        return RunOutcome(status=status, items_attempted=attempted, items_succeeded=succeeded)


def build_analyst_snapshots(cfg: CategoryConfig, manager: "HarvesterManager") -> AnalystSnapshotsHarvester:
    return AnalystSnapshotsHarvester(cfg, manager)


register_category("analyst_snapshots", build_analyst_snapshots)
```

- [ ] **Step 4: Register the module**

Add `analyst_snapshots`:

```python
from aiofmp.harvester.categories import (  # noqa: E402, F401
    analyst_estimates,
    analyst_snapshots,
    chart_eod,
    chart_intraday,
    commodities_eod,
    commodities_intraday,
    economics,
    forex_eod,
    forex_intraday,
    form13f,
    indexes_eod,
    indexes_intraday,
    insider_trades,
    news,
    statements,
    technical_indicators,
)
```

- [ ] **Step 5: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_analyst_snapshots.py -v`
Expected: all 5 tests pass.

- [ ] **Step 6: Commit**

```bash
git add aiofmp/harvester/categories/analyst_snapshots.py aiofmp/harvester/categories/__init__.py tests/test_harvester/test_analyst_snapshots.py
git commit -m "feat(harvester): analyst_snapshots category (P4 overwrite)"
```

---

### Task 26: `dcf` category (P4 snapshot overwrite over `financial_symbols`)

**Files:**
- Create: `aiofmp/harvester/categories/dcf.py`
- Modify: `aiofmp/harvester/categories/__init__.py`
- Create: `tests/test_harvester/test_dcf.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_harvester/test_dcf.py`:

```python
"""Tests for dcf category (P4 snapshot overwrite)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.cachedclient.snapshot_store import SnapshotStore
from aiofmp.cachedclient.storage.parquet import ParquetStorage
from aiofmp.harvester.budget import BudgetTracker
from aiofmp.harvester.categories.dcf import build_dcf
from aiofmp.harvester.config import BudgetConfig, CategoryConfig, RetryConfig
from aiofmp.harvester.state import RunStatus, StateStore


@pytest.fixture
async def manager(tmp_path: Path) -> MagicMock:
    m = MagicMock()
    m.state = StateStore(tmp_path / "h.sqlite"); m.state.initialize()
    m.budget = BudgetTracker(m.state, BudgetConfig())
    m.config = MagicMock(); m.config.retry = RetryConfig()
    m.catalog = MagicMock()
    m.catalog.symbols = AsyncMock(return_value=["AAPL", "MSFT"])
    m.fmp_client = MagicMock()
    m.fmp_client.dcf = MagicMock()
    m.fmp_client.dcf.dcf_valuation = AsyncMock(return_value=[{"symbol": "AAPL", "dcf": 147.27}])
    m.fmp_client.dcf.levered_dcf = AsyncMock(return_value=[{"symbol": "AAPL", "dcf": 150.10}])
    storage = ParquetStorage(tmp_path)
    await storage.initialize()
    m.cached_client = MagicMock()
    m.cached_client.storage = storage
    return m


class TestDcf:
    @pytest.mark.asyncio
    async def test_default_endpoints(self, manager) -> None:
        cfg = CategoryConfig(enabled=True, interval="24h", extra={})
        h = build_dcf(cfg, manager)
        outcome = await h.run_cycle()
        # 2 symbols * 2 endpoints
        assert outcome.items_attempted == 4
        manager.catalog.symbols.assert_awaited_with("financial_symbols")

        ss = SnapshotStore(manager.cached_client.storage)
        row = await ss.read("discounted-cash-flow", "AAPL")
        assert row is not None
        assert row["dcf"] == 147.27
        row2 = await ss.read("levered-discounted-cash-flow", "AAPL")
        assert row2 is not None
        assert row2["dcf"] == 150.10

    @pytest.mark.asyncio
    async def test_custom_include(self, manager) -> None:
        cfg = CategoryConfig(enabled=True, interval="24h", extra={"include": ["dcf_valuation"]})
        h = build_dcf(cfg, manager)
        outcome = await h.run_cycle()
        assert outcome.items_attempted == 2
        manager.fmp_client.dcf.levered_dcf.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_unknown_include_raises(self, manager) -> None:
        cfg = CategoryConfig(enabled=True, interval="24h", extra={"include": ["bogus"]})
        with pytest.raises(ValueError, match="bogus"):
            build_dcf(cfg, manager)

    @pytest.mark.asyncio
    async def test_registers(self) -> None:
        from aiofmp.harvester.categories import _REGISTRY
        assert "dcf" in _REGISTRY
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_dcf.py -v`
Expected: ImportError.

- [ ] **Step 3: Create `aiofmp/harvester/categories/dcf.py`**

```python
"""dcf category — Pattern P4 (snapshot overwrite over financial_symbols)."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from aiofmp.cachedclient.snapshot_store import SnapshotStore
from aiofmp.harvester.base import CategoryHarvester, RunOutcome
from aiofmp.harvester.categories import register_category
from aiofmp.harvester.config import CategoryConfig
from aiofmp.harvester.state import RunStatus

if TYPE_CHECKING:
    from aiofmp.harvester.manager import HarvesterManager

logger = logging.getLogger(__name__)

# Maps include-name -> (SDK method on client.dcf, snapshot endpoint key)
_INCLUDE_MAP: dict[str, tuple[str, str]] = {
    "dcf_valuation": ("dcf_valuation", "discounted-cash-flow"),
    "levered_dcf": ("levered_dcf", "levered-discounted-cash-flow"),
}

_DEFAULT_INCLUDE = list(_INCLUDE_MAP.keys())


class DcfHarvester(CategoryHarvester):
    def __init__(self, cfg: CategoryConfig, manager: "HarvesterManager") -> None:
        super().__init__("dcf", cfg, manager.state, manager.budget, manager.config.retry)
        self._catalog = manager.catalog
        self._fmp = manager.fmp_client
        self._snapshots = SnapshotStore(manager.cached_client.storage)
        include = list(cfg.extra.get("include", _DEFAULT_INCLUDE))
        for n in include:
            if n not in _INCLUDE_MAP:
                raise ValueError(f"dcf: unknown include {n!r}")
        self._include = include

    async def run_cycle(self) -> RunOutcome:
        symbols = await self._catalog.symbols("financial_symbols")
        attempted = 0
        succeeded = 0
        for symbol in symbols:
            for name in self._include:
                attempted += 1
                method_name, endpoint = _INCLUDE_MAP[name]
                method = getattr(self._fmp.dcf, method_name)
                try:
                    rows = await method(symbol)
                    payload = rows[0] if isinstance(rows, list) and rows else None
                    if payload:
                        await self._snapshots.write(endpoint, symbol, payload)
                    succeeded += 1
                except Exception as exc:
                    logger.warning("dcf.%s(%s) failed: %s", method_name, symbol, exc)
        status = RunStatus.OK if succeeded == attempted else RunStatus.PARTIAL
        return RunOutcome(status=status, items_attempted=attempted, items_succeeded=succeeded)


def build_dcf(cfg: CategoryConfig, manager: "HarvesterManager") -> DcfHarvester:
    return DcfHarvester(cfg, manager)


register_category("dcf", build_dcf)
```

- [ ] **Step 4: Register the module**

Add `dcf`:

```python
from aiofmp.harvester.categories import (  # noqa: E402, F401
    analyst_estimates,
    analyst_snapshots,
    chart_eod,
    chart_intraday,
    commodities_eod,
    commodities_intraday,
    dcf,
    economics,
    forex_eod,
    forex_intraday,
    form13f,
    indexes_eod,
    indexes_intraday,
    insider_trades,
    news,
    statements,
    technical_indicators,
)
```

- [ ] **Step 5: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_dcf.py -v`
Expected: all 4 tests pass.

- [ ] **Step 6: Commit**

```bash
git add aiofmp/harvester/categories/dcf.py aiofmp/harvester/categories/__init__.py tests/test_harvester/test_dcf.py
git commit -m "feat(harvester): dcf category (P4 snapshot overwrite)"
```

---

## Phase 7 — CLI integration + end-to-end

### Task 27: Wire the bandwidth callback from `FmpClient` → `BudgetTracker`

**Files:**
- Modify: `aiofmp/harvester/manager.py`
- Modify: `tests/test_harvester/test_manager.py`

Until now the manager doesn't actually attach the bandwidth callback to the shared `FmpClient`. This task wires it so every API request goes through `BudgetTracker.record_bytes()` and `BudgetTracker.check_hard_cap()`.

- [ ] **Step 1: Append failing test to `tests/test_harvester/test_manager.py`**

Append at the end of `tests/test_harvester/test_manager.py`:

```python
class TestBandwidthAttachment:
    @pytest.mark.asyncio
    async def test_callback_attached_to_fmp_client(self, cfg: HarvestConfig) -> None:
        from aiofmp.base import FMPBaseClient, current_harvest_category
        fmp = FMPBaseClient(api_key="dummy")
        mgr = HarvesterManager(cfg, fmp_client=fmp, cached_client=MagicMock())
        await mgr.start()
        assert fmp.on_response_size is not None
        # Invoke it and verify it lands in the ledger.
        token = current_harvest_category.set("alpha")
        try:
            fmp.on_response_size(current_harvest_category.get(), 4096)
        finally:
            current_harvest_category.reset(token)
        month = mgr.budget.current_month_key()
        assert mgr.state.get_category_month_bytes(month, "alpha") == 4096
        await mgr.close()

    @pytest.mark.asyncio
    async def test_callback_triggers_hard_cap(self, cfg: HarvestConfig) -> None:
        from aiofmp.base import FMPBaseClient, FMPBudgetError, current_harvest_category
        cfg.budget.monthly_soft_cap_gb = 1
        cfg.budget.monthly_hard_cap_gb = 2
        fmp = FMPBaseClient(api_key="dummy")
        mgr = HarvesterManager(cfg, fmp_client=fmp, cached_client=MagicMock())
        await mgr.start()
        # Pre-fill the ledger to past hard cap
        mgr.budget.record_bytes("alpha", 3 * 1024 ** 3)
        token = current_harvest_category.set("alpha")
        try:
            with pytest.raises(FMPBudgetError):
                fmp.on_response_size(current_harvest_category.get(), 1)
        finally:
            current_harvest_category.reset(token)
        await mgr.close()
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_manager.py::TestBandwidthAttachment -v`
Expected: failures — the manager doesn't wire `on_response_size` yet.

- [ ] **Step 3: Wire the callback in `HarvesterManager.start()`**

In `aiofmp/harvester/manager.py`, at the end of `start()`, install the bandwidth hook:

```python
    async def start(self) -> None:
        # Wire bandwidth + hard-cap callback into the shared FmpClient
        self.fmp_client.on_response_size = self._on_response_size

        for name, cat_cfg in self.config.categories.items():
            if not cat_cfg.enabled:
                logger.info("Category %s is disabled; skipping", name)
                continue
            try:
                self._categories[name] = self._build_category(name, cat_cfg)
            except KeyError:
                logger.warning("Unknown category in config: %s (skipping)", name)

    def _on_response_size(self, category: str | None, byte_count: int) -> None:
        """Bandwidth callback installed on FmpClient.

        Records bytes against the current category (or 'user' if outside a cycle),
        then raises FMPBudgetError if the hard cap is breached for harvester traffic.
        """
        self.budget.record_bytes(category, byte_count)
        self.budget.check_hard_cap(category)
```

- [ ] **Step 4: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_manager.py -v`
Expected: all manager tests pass (5 prior + 2 new = 7).

- [ ] **Step 5: Commit**

```bash
git add aiofmp/harvester/manager.py tests/test_harvester/test_manager.py
git commit -m "feat(harvester): wire bandwidth callback + hard-cap enforcement"
```

---

### Task 28: `aiofmp harvest` CLI subcommand

**Files:**
- Create: `aiofmp/harvester/cli.py`
- Modify: `aiofmp/cli.py`
- Create: `tests/test_harvester/test_cli.py`

The `aiofmp harvest` subcommand has these flags:
- `--config PATH` (required) — points at the YAML file
- `--once` — run each enabled category's next-due cycle and exit
- `--category NAME` — restrict to a single category (combine with `--once`)
- `--dry-run` — print the plan, fetch nothing

`aiofmp harvest-status` prints a tabular summary from the state store.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_harvester/test_cli.py`:

```python
"""Tests for the harvester CLI."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from textwrap import dedent
from unittest.mock import AsyncMock, patch

import pytest
from click.testing import CliRunner

from aiofmp.cli import cli


def _write_yaml(path: Path, body: str) -> None:
    path.write_text(dedent(body).strip() + "\n")


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def env_with_key(monkeypatch) -> None:
    monkeypatch.setenv("FMP_API_KEY", "test_key_xxxx")


@pytest.fixture
def minimal_config(tmp_path: Path) -> Path:
    state = tmp_path / "state"
    state.mkdir()
    cfg = tmp_path / "h.yaml"
    _write_yaml(cfg, f"""
        state_dir: {state}
        categories:
          news:
            enabled: true
            interval: 30m
    """)
    return cfg


class TestHarvestCli:
    def test_missing_api_key(self, runner: CliRunner, minimal_config: Path) -> None:
        # Ensure FMP_API_KEY is NOT in env
        result = runner.invoke(
            cli, ["harvest", "--config", str(minimal_config), "--once"],
            env={"FMP_API_KEY": ""},
        )
        assert result.exit_code != 0
        assert "FMP_API_KEY" in result.output

    def test_dry_run_prints_plan(self, env_with_key, runner: CliRunner, minimal_config: Path) -> None:
        result = runner.invoke(
            cli, ["harvest", "--config", str(minimal_config), "--dry-run"],
        )
        assert result.exit_code == 0
        assert "news" in result.output
        assert "enabled" in result.output.lower()

    def test_once_runs_and_exits(
        self, env_with_key, runner: CliRunner, minimal_config: Path,
    ) -> None:
        with patch("aiofmp.harvester.cli._build_cached_client") as m:
            fake_cached = AsyncMock()
            fake_cached.__aenter__ = AsyncMock(return_value=fake_cached)
            fake_cached.__aexit__ = AsyncMock(return_value=None)
            fake_cached.news = type("X", (), {})()
            for v in ("general_news", "press_releases", "stock_news", "crypto_news", "forex_news"):
                setattr(fake_cached.news, v, AsyncMock(return_value=[]))
            fake_cached.storage = AsyncMock()
            m.return_value = (AsyncMock(), fake_cached)

            result = runner.invoke(
                cli, ["harvest", "--config", str(minimal_config), "--once"],
            )
            assert result.exit_code == 0, result.output

    def test_once_with_specific_category(
        self, env_with_key, runner: CliRunner, tmp_path: Path,
    ) -> None:
        cfg = tmp_path / "h.yaml"
        state = tmp_path / "state"; state.mkdir()
        _write_yaml(cfg, f"""
            state_dir: {state}
            categories:
              news:
                enabled: true
                interval: 30m
              economics:
                enabled: true
                interval: 24h
        """)
        with patch("aiofmp.harvester.cli._build_cached_client") as m:
            fake_cached = AsyncMock()
            fake_cached.__aenter__ = AsyncMock(return_value=fake_cached)
            fake_cached.__aexit__ = AsyncMock(return_value=None)
            fake_cached.news = type("X", (), {})()
            for v in ("general_news", "press_releases", "stock_news", "crypto_news", "forex_news"):
                setattr(fake_cached.news, v, AsyncMock(return_value=[]))
            fake_cached.economics = type("X", (), {})()
            fake_cached.economics.treasury_rates = AsyncMock(return_value=[])
            fake_cached.economics.economic_indicators = AsyncMock(return_value=[])
            fake_cached.storage = AsyncMock()
            m.return_value = (AsyncMock(), fake_cached)

            result = runner.invoke(
                cli, ["harvest", "--config", str(cfg), "--once", "--category", "news"],
            )
            assert result.exit_code == 0, result.output
            # Economics should NOT have been called when filtered to news
            fake_cached.economics.treasury_rates.assert_not_awaited()


class TestHarvestStatusCli:
    def test_empty_status(self, env_with_key, runner: CliRunner, minimal_config: Path) -> None:
        result = runner.invoke(cli, ["harvest-status", "--config", str(minimal_config)])
        assert result.exit_code == 0
        # Header should mention categories columns
        assert "category" in result.output.lower()
```

- [ ] **Step 2: Run tests to confirm failure**

Run: `uv run pytest tests/test_harvester/test_cli.py -v`
Expected: ImportError (`aiofmp.harvester.cli` missing) or "no such command 'harvest'".

- [ ] **Step 3: Create `aiofmp/harvester/cli.py`**

```python
"""CLI subcommands for the harvester."""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Any

import click

from aiofmp import FmpClient
from aiofmp.cachedclient import CachedClient
from aiofmp.harvester import categories  # noqa: F401  — triggers registration imports
from aiofmp.harvester.config import (
    CategoryConfig,
    HarvestConfig,
    load_config_from_yaml,
)
from aiofmp.harvester.manager import HarvesterManager

logger = logging.getLogger(__name__)


def _resolve_api_key(api_key_opt: str | None) -> str:
    key = api_key_opt or os.environ.get("FMP_API_KEY")
    if not key:
        click.echo("error: FMP_API_KEY env var or --api-key option is required", err=True)
        sys.exit(2)
    return key


def _build_cached_client(api_key: str) -> tuple[FmpClient, CachedClient]:
    """Build a real FmpClient + CachedClient pair. Patched in tests."""
    fmp = FmpClient(api_key=api_key)
    cached = CachedClient(fmp)
    return fmp, cached


def _print_dry_run_plan(cfg: HarvestConfig, restrict_to: str | None) -> None:
    click.echo(f"state_dir: {cfg.state_dir}")
    click.echo(f"budget: soft={cfg.budget.monthly_soft_cap_gb}GB hard={cfg.budget.monthly_hard_cap_gb}GB")
    click.echo("")
    click.echo(f"{'category':30s} {'enabled':8s} {'interval':10s}")
    click.echo("-" * 50)
    for name, cat in cfg.categories.items():
        if restrict_to and name != restrict_to:
            continue
        flag = "yes" if cat.enabled else "no"
        click.echo(f"{name:30s} {flag:8s} {cat.interval:10s}")


async def _run_once(
    cfg: HarvestConfig, api_key: str, restrict_to: str | None,
) -> int:
    fmp, cached = _build_cached_client(api_key)
    rc = 0
    async with cached:
        mgr = HarvesterManager(cfg, fmp_client=fmp, cached_client=cached)
        await mgr.start()
        targets = list(mgr._categories.keys())
        if restrict_to:
            targets = [t for t in targets if t == restrict_to]
            if not targets:
                click.echo(f"error: category {restrict_to!r} not enabled in config", err=True)
                return 2
        for name in targets:
            await mgr._categories[name]._run_once_and_record()
            run = mgr.state.get_latest_run(name)
            status = run.status.value if run else "missing"
            items = run.items_attempted if run else 0
            ok = run.items_succeeded if run else 0
            click.echo(f"{name:30s} {status:20s} {ok}/{items} items")
            if run and run.error:
                rc = 1
        await mgr.close()
    return rc


async def _run_forever(cfg: HarvestConfig, api_key: str) -> int:
    fmp, cached = _build_cached_client(api_key)
    async with cached:
        mgr = HarvesterManager(cfg, fmp_client=fmp, cached_client=cached)
        await mgr.start()
        mgr.install_signal_handlers()
        try:
            await mgr.run_until_stopped()
        finally:
            await mgr.close()
    return 0


@click.command("harvest")
@click.option("--config", "config_path", required=True, type=click.Path(exists=True, dir_okay=False))
@click.option("--once", is_flag=True, help="Run each enabled category's next-due cycle and exit.")
@click.option("--category", "category_name", default=None, help="Restrict to a single category (with --once).")
@click.option("--dry-run", is_flag=True, help="Print the plan; fetch nothing.")
@click.option("--api-key", default=None, help="Override FMP_API_KEY env var.")
def harvest(config_path: str, once: bool, category_name: str | None, dry_run: bool, api_key: str | None) -> None:
    """Run the aiofmp harvester."""
    cfg = load_config_from_yaml(config_path)
    logging.basicConfig(level=getattr(logging, cfg.log_level.upper(), logging.INFO))

    if dry_run:
        _print_dry_run_plan(cfg, restrict_to=category_name)
        sys.exit(0)

    key = _resolve_api_key(api_key)
    if once:
        rc = asyncio.run(_run_once(cfg, key, restrict_to=category_name))
        sys.exit(rc)
    else:
        rc = asyncio.run(_run_forever(cfg, key))
        sys.exit(rc)


@click.command("harvest-status")
@click.option("--config", "config_path", required=True, type=click.Path(exists=True, dir_okay=False))
def harvest_status(config_path: str) -> None:
    """Print a tabular summary of the harvester state store."""
    cfg = load_config_from_yaml(config_path)
    state_dir = Path(os.path.expanduser(cfg.state_dir))
    from aiofmp.harvester.state import StateStore
    store = StateStore(state_dir / "harvester.sqlite")
    store.initialize()

    click.echo(f"{'category':30s} {'status':20s} {'finished_at':30s} {'items':10s}")
    click.echo("-" * 95)
    for name in sorted(cfg.categories.keys()):
        run = store.get_latest_run(name)
        if run is None:
            click.echo(f"{name:30s} {'never_ran':20s} {'-':30s} {'-':10s}")
            continue
        items = f"{run.items_succeeded}/{run.items_attempted}"
        finished = run.finished_at or "(running)"
        click.echo(f"{name:30s} {run.status.value:20s} {finished:30s} {items:10s}")
```

- [ ] **Step 4: Wire the new commands into `aiofmp/cli.py`**

In `aiofmp/cli.py`, BEFORE `if __name__ == "__main__":`, add:

```python
from aiofmp.harvester.cli import harvest as _harvest_cmd
from aiofmp.harvester.cli import harvest_status as _harvest_status_cmd

cli.add_command(_harvest_cmd)
cli.add_command(_harvest_status_cmd)
```

- [ ] **Step 5: Run tests to confirm pass**

Run: `uv run pytest tests/test_harvester/test_cli.py -v`
Expected: all 5 tests pass.

- [ ] **Step 6: Commit**

```bash
git add aiofmp/harvester/cli.py aiofmp/cli.py tests/test_harvester/test_cli.py
git commit -m "feat(harvester): aiofmp harvest + harvest-status CLI commands"
```

---

### Task 29: End-to-end smoke test (mocked SDK, real registry & storage)

**Files:**
- Create: `tests/test_harvester/test_e2e_smoke.py`

A single test that wires the actual `HarvesterManager`, with a mocked `FmpClient` returning canned responses, and runs one cycle per category. Verifies:
- All enabled categories complete a cycle without unhandled exceptions.
- State store has one `category_runs` row per category.
- Parquet files are created under the temp state dir.

- [ ] **Step 1: Write the failing test**

Create `tests/test_harvester/test_e2e_smoke.py`:

```python
"""End-to-end smoke test for the harvester."""

from __future__ import annotations

import asyncio
from datetime import date
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from aiofmp.cachedclient import CachedClient
from aiofmp.harvester.config import (
    BudgetConfig,
    CategoryConfig,
    HarvestConfig,
    RetryConfig,
)
from aiofmp.harvester.manager import HarvesterManager
from aiofmp.harvester.state import RunStatus


def _eod_record() -> dict[str, Any]:
    return {"date": "2025-06-01", "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.5, "volume": 1000}


def _earnings_record(symbol: str, d: str) -> dict[str, Any]:
    return {"symbol": symbol, "date": d, "epsEstimated": 1.0, "eps": 1.05}


def _build_fake_fmp() -> MagicMock:
    fmp = MagicMock()
    # Directory + per-category list endpoints
    fmp.directory = MagicMock()
    fmp.directory.financial_symbols = AsyncMock(return_value=[{"symbol": "AAPL"}])
    fmp.directory.actively_trading = AsyncMock(return_value=[{"symbol": "AAPL"}])
    fmp.directory.etf_list = AsyncMock(return_value=[])
    fmp.commodity = MagicMock()
    fmp.commodity.commodities_list = AsyncMock(return_value=[{"symbol": "GCUSD"}])
    fmp.forex = MagicMock()
    fmp.forex.forex_list = AsyncMock(return_value=[{"symbol": "EURUSD"}])
    fmp.indexes = MagicMock()
    fmp.indexes.index_list = AsyncMock(return_value=[{"symbol": "^GSPC"}])

    # Chart EOD endpoints
    fmp.chart = MagicMock()
    fmp.chart.historical_price_full = AsyncMock(return_value=[_eod_record()])

    # Statements endpoints — wired with a single canned return
    fmp.statements = MagicMock()
    for m in [
        "income_statement", "balance_sheet_statement", "cash_flow_statement",
        "key_metrics", "financial_ratios", "enterprise_values",
        "income_statement_growth", "balance_sheet_statement_growth",
        "cash_flow_statement_growth", "financial_statement_growth",
        "owner_earnings", "revenue_product_segmentation", "revenue_geographic_segmentation",
    ]:
        setattr(fmp.statements, m, AsyncMock(return_value=[{"date": "2024-12-31", "symbol": "AAPL"}]))

    # Calendar — earnings_calendar is the discovery probe for statements
    fmp.calendar = MagicMock()
    fmp.calendar.earnings_calendar = AsyncMock(return_value=[_earnings_record("AAPL", date.today().isoformat())])

    # News endpoints
    fmp.news = MagicMock()
    for v in ("general_news", "press_releases", "stock_news", "crypto_news", "forex_news"):
        setattr(fmp.news, v, AsyncMock(return_value=[]))

    # Economics
    fmp.economics = MagicMock()
    fmp.economics.treasury_rates = AsyncMock(return_value=[])
    fmp.economics.economic_indicators = AsyncMock(return_value=[])

    # Analyst
    fmp.analyst = MagicMock()
    fmp.analyst.financial_estimates = AsyncMock(side_effect=[
        [{"symbol": "AAPL", "date": "2025-12-31", "revenueAvg": 100}],
        [],
    ])
    fmp.analyst.ratings_snapshot = AsyncMock(return_value=[{"symbol": "AAPL", "rating": "A"}])
    fmp.analyst.price_target_consensus = AsyncMock(return_value=[{"symbol": "AAPL", "targetConsensus": 250}])
    fmp.analyst.price_target_summary = AsyncMock(return_value=[{"symbol": "AAPL"}])
    fmp.analyst.stock_grades_summary = AsyncMock(return_value=[{"symbol": "AAPL", "consensus": "Buy"}])

    # Insider trades
    fmp.insider_trades = MagicMock()
    fmp.insider_trades.latest_insider_trades = AsyncMock(side_effect=[
        [{"symbol": "AAPL", "filingDate": "2026-05-01", "transactionType": "P-Purchase"}],
        [],
    ])

    # Form 13F
    fmp.form13f = MagicMock()
    fmp.form13f.latest_filings = AsyncMock(side_effect=[
        [{"cik": "0001067983", "acceptedDate": "2026-05-01", "name": "Berkshire"}],
        [],
    ])

    # DCF
    fmp.dcf = MagicMock()
    fmp.dcf.dcf_valuation = AsyncMock(return_value=[{"symbol": "AAPL", "dcf": 150.0}])
    fmp.dcf.levered_dcf = AsyncMock(return_value=[{"symbol": "AAPL", "dcf": 155.0}])

    # Make on_response_size assignable (FmpClient has it; MagicMock too)
    fmp.on_response_size = None
    fmp.start = AsyncMock()
    fmp.close = AsyncMock()
    return fmp


@pytest.mark.asyncio
async def test_one_cycle_per_category(tmp_path: Path) -> None:
    cfg = HarvestConfig(
        state_dir=str(tmp_path),
        budget=BudgetConfig(),
        retry=RetryConfig(),
        categories={
            "chart_eod": CategoryConfig(enabled=True, interval="24h", extra={"backfill_years": 1}),
            "commodities_eod": CategoryConfig(enabled=True, interval="24h", extra={}),
            "forex_eod": CategoryConfig(enabled=True, interval="24h", extra={}),
            "indexes_eod": CategoryConfig(enabled=True, interval="24h", extra={}),
            "news": CategoryConfig(enabled=True, interval="30m", extra={}),
            "economics": CategoryConfig(enabled=True, interval="24h", extra={"indicators": ["GDP"]}),
            "statements": CategoryConfig(enabled=True, interval="6h", extra={"periods": ["annual"]}),
            "analyst_estimates": CategoryConfig(enabled=True, interval="24h", extra={"estimate_periods": ["annual"], "page_size": 1}),
            "analyst_snapshots": CategoryConfig(enabled=True, interval="24h", extra={}),
            "insider_trades": CategoryConfig(enabled=True, interval="6h", extra={"page_size": 1, "max_pages": 2}),
            "form13f": CategoryConfig(enabled=True, interval="24h", extra={"page_size": 1, "max_pages": 2}),
            "dcf": CategoryConfig(enabled=True, interval="24h", extra={}),
        },
    )
    fmp = _build_fake_fmp()
    cached = CachedClient(fmp)

    async with cached:
        mgr = HarvesterManager(cfg, fmp_client=fmp, cached_client=cached)
        await mgr.start()

        # Run one cycle per enabled category, sequentially
        for name in list(mgr._categories.keys()):
            await mgr._categories[name]._run_once_and_record()
            run = mgr.state.get_latest_run(name)
            assert run is not None, f"no run row for {name}"
            assert run.status in (RunStatus.OK, RunStatus.PARTIAL), \
                f"{name} ended in unexpected status {run.status}"

        await mgr.close()

    # Sanity: at least one parquet file should exist
    assert any((tmp_path / "cachedclient_data").rglob("data.parquet"))
```

- [ ] **Step 2: Run test to confirm it passes**

Run: `uv run pytest tests/test_harvester/test_e2e_smoke.py -v`
Expected: pass (or at most a clearly diagnosable failure — fix any registry-import side effects).

- [ ] **Step 3: Run the entire test suite to confirm no regressions**

Run: `uv run pytest -q`
Expected: every test passes.

- [ ] **Step 4: Run ruff over the new code**

Run: `uv run ruff check aiofmp/harvester aiofmp/cachedclient/snapshot_store.py aiofmp/base.py tests/test_harvester`
Expected: no errors. Fix any issues inline before committing.

Run: `uv run ruff format aiofmp/harvester aiofmp/cachedclient/snapshot_store.py tests/test_harvester`
Expected: formatter exits 0.

- [ ] **Step 5: Commit**

```bash
git add tests/test_harvester/test_e2e_smoke.py
git commit -m "test(harvester): end-to-end smoke covering all 17 categories"
```

---

### Task 30: README + example config

**Files:**
- Modify: `README.md`
- Create: `examples/harvester.example.yaml`

- [ ] **Step 1: Create `examples/harvester.example.yaml`**

```yaml
# Example harvester config — copy to harvester.yaml and edit as needed.
# Cap defaults assume FMP starter plan (20 GB/month).

state_dir: ~/.aiofmp/cache
log_level: INFO

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
  refresh_interval: 7d

categories:
  statements:
    enabled: true
    interval: 6h
    periods: [annual, quarter]
    initial_limit: 40
    incremental_limit: 2
    safety_net_interval: 30d

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

  chart_intraday:
    enabled: false
    interval: 4h
    timeframes: [1hour]
    backfill_days: 30

  technical_indicators:
    enabled: false
    interval: 24h
    indicators: []

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

- [ ] **Step 2: Add a "Harvester" section to README.md**

Open `README.md` and append (just before the existing "## Configuration" section) the following:

```markdown
### Harvester

`aiofmp harvest` is a long-running CLI that proactively warms the local Parquet cache. It runs one async task per enabled category, each on its own configurable interval, and uses category-specific strategies to minimise redundant fetches (target: stay under 20 GB/month on FMP starter plan).

**Quick start:**

```bash
cp examples/harvester.example.yaml ~/harvester.yaml
export FMP_API_KEY=your_key_here

# Print the plan, fetch nothing
aiofmp harvest --config ~/harvester.yaml --dry-run

# One cycle per enabled category, then exit
aiofmp harvest --config ~/harvester.yaml --once

# Run a single category once
aiofmp harvest --config ~/harvester.yaml --once --category statements

# Run forever (Ctrl-C to stop cleanly)
aiofmp harvest --config ~/harvester.yaml

# Inspect state
aiofmp harvest-status --config ~/harvester.yaml
```

**State:** SQLite at `<state_dir>/harvester.sqlite` (checkpoints, bandwidth ledger, symbol catalogs). Parquet under `<state_dir>/cachedclient_data/`.

See `docs/superpowers/specs/2026-05-15-harvester-v2-design.md` for the full design.
```

- [ ] **Step 3: Verify the docs render cleanly**

Run: `uv run python -c "from pathlib import Path; print(Path('README.md').read_text(encoding='utf-8').count('Harvester'))"`
Expected: at least 1.

- [ ] **Step 4: Commit**

```bash
git add README.md examples/harvester.example.yaml
git commit -m "docs(harvester): README section + example config"
```

---

### Task 31: Full-suite final pass + tag-ready summary

**Files:**
- (Verification only)

- [ ] **Step 1: Run the whole suite**

Run: `uv run pytest -q --tb=short`
Expected: all tests pass. No skipped tests beyond the existing optional integration tests.

- [ ] **Step 2: Run ruff over the whole tree**

Run: `uv run ruff check . && uv run ruff format --check .`
Expected: clean.

- [ ] **Step 3: Sanity: import the package and list categories**

Run: `uv run python -c "from aiofmp.harvester.categories import registered_names; print('\n'.join(registered_names()))"`
Expected: lists 17 categories (`chart_eod`, `chart_intraday`, `commodities_eod`, `commodities_intraday`, `forex_eod`, `forex_intraday`, `indexes_eod`, `indexes_intraday`, `news`, `economics`, `statements`, `analyst_estimates`, `analyst_snapshots`, `insider_trades`, `form13f`, `technical_indicators`, `dcf`).

- [ ] **Step 4: Sanity: `--help` works**

Run: `uv run aiofmp harvest --help`
Expected: shows the `--config`, `--once`, `--category`, `--dry-run`, `--api-key` options.

Run: `uv run aiofmp harvest-status --help`
Expected: shows the `--config` option.

- [ ] **Step 5: Done — print final summary**

Run: `git log --oneline 6b52a86..HEAD`
Expected: a clean linear history of the harvester implementation commits.

No code change for this step — this is the final verification gate.
