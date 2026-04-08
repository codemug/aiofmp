"""Symbol resolution for the harvester."""

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


async def resolve_symbols(
    config: Any,  # SymbolsConfig
    cached_client: Any,  # CachedClient
) -> list[str]:
    mode = config.mode

    if mode == "explicit":
        logger.info("Symbol mode=explicit, %d symbols configured", len(config.symbols))
        return list(config.symbols)

    if mode == "discover":
        return await _discover_symbols(cached_client)

    if mode.startswith("file:"):
        file_path = mode[len("file:"):]
        return _read_symbols_from_file(file_path)

    logger.warning("Unknown symbol mode '%s'; returning empty list", mode)
    return []


async def _discover_symbols(cached_client: Any) -> list[str]:
    """Discover symbols by calling directory.company_symbols()."""
    try:
        records = await cached_client.directory.company_symbols()
        if not records:
            logger.warning("directory.company_symbols() returned empty; no symbols discovered")
            return []
        symbols = [r["symbol"] for r in records if r.get("symbol")]
        logger.info("Discovered %d symbols via directory.company_symbols()", len(symbols))
        return symbols
    except Exception as exc:
        logger.warning("Failed to discover symbols: %s", exc)
        return []


def _read_symbols_from_file(file_path: str) -> list[str]:
    """Read symbols from a text file, one per line."""
    path = Path(file_path)
    if not path.exists():
        logger.warning("Symbol file not found: %s", path)
        return []
    text = path.read_text(encoding="utf-8")
    symbols = [line.strip().upper() for line in text.splitlines() if line.strip()]
    logger.info("Loaded %d symbols from '%s'", len(symbols), path)
    return symbols
