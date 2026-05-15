"""Shared fixtures for harvester tests."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

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
