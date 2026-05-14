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

    # Should not raise
    result = await client._handle_response(fake_resp)
    assert result == {}
