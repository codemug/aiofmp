"""CachedCategoryProxy — intercepts category method calls for caching."""

import asyncio
import logging
from collections.abc import Callable
from datetime import date
from typing import Any

from .gap import (
    DateRange,
    compute_gaps,
    denormalize_from_date,
    normalize_to_date,
)
from .registry import CacheableEndpoint, EndpointRegistry, TemporalPattern
from .storage.base import StorageBackend

logger = logging.getLogger(__name__)


def _bind_args(
    meta: CacheableEndpoint,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> dict[str, Any]:
    """Map positional *args* to named params using ``meta.call_params``, then merge *kwargs*."""
    bound: dict[str, Any] = {}
    for i, name in enumerate(meta.call_params):
        if i < len(args):
            bound[name] = args[i]
    bound.update(kwargs)
    return bound


def _derive_storage_key(
    meta: CacheableEndpoint,
    bound_args: dict[str, Any],
) -> tuple[str, ...]:
    """Build the storage key tuple from endpoint metadata and bound call arguments.

    Examples:
        ("historical-price-eod/full", "AAPL")
        ("income-statement", "AAPL", "annual")
        ("technical-indicators/sma", "AAPL", "10", "1day")
    """
    key_parts: list[str] = [meta.api_endpoint]
    for arg_name in meta.entity_key_args:
        key_parts.append(str(bound_args[arg_name]))
    for arg_name in meta.extra_key_args:
        val = bound_args.get(arg_name)
        if val is not None:
            key_parts.append(str(val))
        else:
            key_parts.append("_default")
    return tuple(key_parts)


class CachedCategoryProxy:
    """Proxy that intercepts calls on a category and applies cache logic.

    Non-cacheable methods pass through to the real category unchanged.
    """

    def __init__(
        self,
        real_category: Any,
        category_name: str,
        storage: StorageBackend,
        registry: EndpointRegistry,
    ) -> None:
        self._real = real_category
        self._category_name = category_name
        self._storage = storage
        self._registry = registry
        self._locks: dict[tuple[str, ...], asyncio.Lock] = {}

    def _get_lock(self, key: tuple[str, ...]) -> asyncio.Lock:
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()
        return self._locks[key]

    def __getattr__(self, name: str) -> Any:
        real_method = getattr(self._real, name)

        meta = self._registry.get(self._category_name, name)
        if meta is None:
            # Not cacheable: pass through directly
            return real_method

        async def cached_call(*args: Any, **kwargs: Any) -> Any:
            return await self._cached_fetch(meta, real_method, args, kwargs)

        cached_call.__name__ = name
        cached_call.__qualname__ = f"{self._category_name}.{name}"
        cached_call.__doc__ = real_method.__doc__
        return cached_call

    async def _cached_fetch(
        self,
        meta: CacheableEndpoint,
        real_method: Callable[..., Any],
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Main cache orchestration for a single call."""
        bound_args = _bind_args(meta, args, kwargs)

        storage_key = _derive_storage_key(meta, bound_args)

        async with self._get_lock(storage_key):
            if meta.pattern == TemporalPattern.DATE_RANGE:
                return await self._fetch_date_range(
                    meta, real_method, bound_args, storage_key
                )
            elif meta.pattern == TemporalPattern.PERIOD_BASED:
                return await self._fetch_period_based(
                    meta, real_method, args, kwargs, bound_args, storage_key
                )
            else:
                # Unknown pattern: pass through
                return await real_method(*args, **kwargs)

    async def _fetch_date_range(
        self,
        meta: CacheableEndpoint,
        real_method: Callable[..., Any],
        bound_args: dict[str, Any],
        storage_key: tuple[str, ...],
    ) -> list[dict[str, Any]]:
        """Cache logic for Pattern A (date-range) endpoints."""
        raw_from = bound_args.get(meta.from_param)
        raw_to = bound_args.get(meta.to_param)

        from_date = normalize_to_date(raw_from, meta.date_param_type)
        to_date = normalize_to_date(raw_to, meta.date_param_type)

        # If no date range specified, fetch everything and persist
        if from_date is None and to_date is None:
            result = await real_method(**bound_args)
            if result:
                await self._storage.write(
                    storage_key,
                    result,
                    meta.response_date_field,
                    meta.response_date_format,
                )
            return result

        # Default to_date to today if only from_date is specified
        if to_date is None:
            to_date = date.today()
        # If only to_date is specified (no from_date), pass through
        if from_date is None:
            return await real_method(**bound_args)

        requested = DateRange(start=from_date, end=to_date)

        # Check storage
        stored_range = await self._storage.get_stored_range(storage_key)
        stored_min = stored_range.min_date if stored_range else None
        stored_max = stored_range.max_date if stored_range else None

        # Compute gaps
        gaps = compute_gaps(requested, stored_min, stored_max)

        if not gaps:
            logger.debug("Cache hit for %s, reading from storage", storage_key)
            return await self._storage.read(storage_key, from_date, to_date)

        # Fetch each gap from the API
        logger.debug("Cache miss for %s, fetching %d gap(s)", storage_key, len(gaps))
        fresh_records: list[dict[str, Any]] = []
        for gap in gaps:
            gap_args = dict(bound_args)
            gap_args[meta.from_param] = denormalize_from_date(
                gap.start, meta.date_param_type
            )
            gap_args[meta.to_param] = denormalize_from_date(
                gap.end, meta.date_param_type
            )
            gap_result = await real_method(**gap_args)
            if gap_result:
                fresh_records.extend(gap_result)

        # Append fresh data to storage
        if fresh_records:
            await self._storage.append(
                storage_key,
                fresh_records,
                meta.response_date_field,
                meta.response_date_format,
            )

        # Read the full requested range from storage
        return await self._storage.read(storage_key, from_date, to_date)

    async def _fetch_period_based(
        self,
        meta: CacheableEndpoint,
        real_method: Callable[..., Any],
        original_args: tuple[Any, ...],
        original_kwargs: dict[str, Any],
        bound_args: dict[str, Any],
        storage_key: tuple[str, ...],
    ) -> list[dict[str, Any]]:
        """Cache logic for Pattern B (period-based) endpoints."""
        original_limit = bound_args.get(meta.limit_param) if meta.limit_param else None

        # Always fetch from API with the caller's original params
        result = await real_method(*original_args, **original_kwargs)

        # Read existing stored data
        stored_data = await self._storage.read(storage_key)

        # Merge: index by date field, fresh data wins on conflicts
        merged: dict[str, dict[str, Any]] = {}
        for record in stored_data:
            date_val = record.get(meta.response_date_field)
            if date_val is not None:
                merged[str(date_val)] = record

        for record in result:
            date_val = record.get(meta.response_date_field)
            if date_val is not None:
                merged[str(date_val)] = record

        # Sort by date descending (most recent first, statements convention)
        all_records = sorted(
            merged.values(),
            key=lambda r: str(r.get(meta.response_date_field, "")),
            reverse=True,
        )

        # Write merged data back to storage
        if all_records:
            await self._storage.write(
                storage_key,
                all_records,
                meta.response_date_field,
                meta.response_date_format,
            )

        # Apply original limit for the return value
        if original_limit is not None:
            return all_records[:original_limit]
        return all_records
