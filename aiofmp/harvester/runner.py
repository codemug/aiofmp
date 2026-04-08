"""Harvest runner — executes a single harvest cycle."""

import asyncio
import logging
from datetime import date, timedelta
from typing import Any

from aiofmp.base import FMPRateLimitError
from aiofmp.cachedclient.gap import denormalize_from_date
from aiofmp.cachedclient.registry import CacheableEndpoint, TemporalPattern

from .config import HarvestConfig
from .result import HarvestResult
from .symbols import resolve_symbols

logger = logging.getLogger(__name__)


async def run_harvest(
    cached_client: Any,  # CachedClient (avoid circular import)
    config: HarvestConfig,
) -> list[HarvestResult]:
    """Execute a single harvest cycle across all configured categories."""
    registry = cached_client.registry
    symbols = await resolve_symbols(config.symbols, cached_client)
    results: list[HarvestResult] = []

    logger.info(
        "Starting harvest cycle: %d categories, %d symbols",
        len(config.categories),
        len(symbols),
    )

    today = date.today()

    for category_name in config.categories:
        logger.info("Harvesting category: %s", category_name)

        # Get all cacheable endpoints for this category
        endpoints = [
            ep for ep in registry.all_endpoints() if ep.category == category_name
        ]

        # Apply method filter from overrides
        overrides = config.overrides.get(category_name, {})
        methods_filter = overrides.get("methods")
        if methods_filter:
            endpoints = [ep for ep in endpoints if ep.method in methods_filter]

        lookback = overrides.get("lookback_days", config.lookback_days)
        from_date = today - timedelta(days=lookback)

        for ep in endpoints:
            try:
                if ep.pattern == TemporalPattern.DATE_RANGE:
                    ep_results = await _harvest_date_range(
                        cached_client, ep, symbols, from_date, today,
                    )
                    results.extend(ep_results)

                elif ep.pattern == TemporalPattern.PERIOD_BASED:
                    limit = overrides.get("limit", config.statement_limit)
                    periods = overrides.get("periods", config.periods)
                    ep_results = await _harvest_period_based(
                        cached_client, ep, symbols, limit, periods,
                    )
                    results.extend(ep_results)

            except FMPRateLimitError:
                logger.warning(
                    "Rate limit hit during %s.%s; stopping harvest cycle.",
                    category_name, ep.method,
                )
                return results

        # If category has no cacheable endpoints, log it
        if not endpoints:
            logger.debug("No cacheable endpoints for category '%s'", category_name)

        # Throttle between categories
        if config.throttle.delay_seconds > 0:
            await asyncio.sleep(config.throttle.delay_seconds)

    logger.info(
        "Harvest cycle complete: %d results, %d errors",
        len(results),
        sum(1 for r in results if not r.success),
    )
    return results


async def _harvest_date_range(
    cached_client: Any,
    ep: CacheableEndpoint,
    symbols: list[str],
    from_date: date,
    to_date: date,
) -> list[HarvestResult]:
    """Harvest a DATE_RANGE endpoint by calling the CachedClient method.

    The CachedClient proxy handles gap detection, fetching only missing data,
    and persisting to storage. We just call the method.
    """
    results: list[HarvestResult] = []
    entities = _resolve_entities(ep, symbols)

    for entity_values in entities:
        endpoint_name = f"{ep.category}.{ep.method}"
        entity_label = dict(zip(ep.entity_key_args, entity_values)) if entity_values else None

        try:
            category_obj = getattr(cached_client, ep.category)
            method_fn = getattr(category_obj, ep.method)

            kwargs: dict[str, Any] = {}
            for arg_name, arg_value in zip(ep.entity_key_args, entity_values):
                kwargs[arg_name] = arg_value
            kwargs[ep.from_param] = denormalize_from_date(from_date, ep.date_param_type)
            kwargs[ep.to_param] = denormalize_from_date(to_date, ep.date_param_type)

            logger.info("Harvesting %s %s", endpoint_name, entity_label or "(global)")

            records = await method_fn(**kwargs)
            count = len(records) if records else 0

            results.append(HarvestResult(
                endpoint_name=endpoint_name,
                entity=str(entity_label) if entity_label else None,
                records_fetched=count,
            ))

        except FMPRateLimitError:
            raise
        except Exception as exc:
            msg = f"{endpoint_name} entity={entity_label}: {exc}"
            logger.exception("Error harvesting %s", msg)
            results.append(HarvestResult(
                endpoint_name=endpoint_name,
                entity=str(entity_label) if entity_label else None,
                error=msg,
            ))

    return results


async def _harvest_period_based(
    cached_client: Any,
    ep: CacheableEndpoint,
    symbols: list[str],
    limit: int,
    periods: list[str],
) -> list[HarvestResult]:
    """Harvest a PERIOD_BASED endpoint by calling the CachedClient method.

    The CachedClient proxy handles fetching, merging, and storing.
    """
    results: list[HarvestResult] = []

    if not symbols and ep.entity_key_args:
        logger.warning(
            "No symbols for %s.%s (requires %s); skipping",
            ep.category, ep.method, ep.entity_key_args,
        )
        return results

    # If endpoint has no period_param, iterate once with no period
    applicable_periods: list[str | None] = list(periods) if ep.period_param else [None]

    for symbol in symbols:
        for period in applicable_periods:
            endpoint_name = f"{ep.category}.{ep.method}"

            try:
                category_obj = getattr(cached_client, ep.category)
                method_fn = getattr(category_obj, ep.method)

                kwargs: dict[str, Any] = {}
                for arg_name in ep.entity_key_args:
                    kwargs[arg_name] = symbol
                if ep.limit_param:
                    kwargs[ep.limit_param] = limit
                if ep.period_param and period is not None:
                    kwargs[ep.period_param] = period

                logger.info(
                    "Harvesting %s symbol=%s period=%s limit=%d",
                    endpoint_name, symbol, period, limit,
                )

                records = await method_fn(**kwargs)
                count = len(records) if records else 0

                results.append(HarvestResult(
                    endpoint_name=endpoint_name,
                    entity=f"{symbol}/{period}" if period else symbol,
                    records_fetched=count,
                ))

            except FMPRateLimitError:
                raise
            except Exception as exc:
                msg = f"{endpoint_name} symbol={symbol} period={period}: {exc}"
                logger.exception("Error harvesting %s", msg)
                results.append(HarvestResult(
                    endpoint_name=endpoint_name,
                    entity=f"{symbol}/{period}" if period else symbol,
                    error=msg,
                ))

    return results


def _resolve_entities(
    ep: CacheableEndpoint,
    symbols: list[str],
) -> list[tuple[str, ...]]:
    """Build entity iteration list for an endpoint."""
    if not ep.entity_key_args:
        return [()]  # Global endpoint, call once
    if symbols:
        return [(s,) for s in symbols]
    logger.warning(
        "No symbols for %s.%s (requires %s); skipping",
        ep.category, ep.method, ep.entity_key_args,
    )
    return []
