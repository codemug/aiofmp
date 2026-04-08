"""
Command Line Interface for aiofmp

This module provides the CLI entrypoints for running the MCP server
and harvest commands.
"""

import asyncio
import logging
import os
import sys

import click

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    """aiofmp — Financial Modeling Prep API client."""
    pass


@cli.command("mcp-server")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "http"]),
    default="stdio",
    help="Transport mode for the MCP server (default: stdio)",
)
@click.option(
    "--host", default="localhost", help="Host for HTTP transport (default: localhost)"
)
@click.option(
    "--port", type=int, default=3000, help="Port for HTTP transport (default: 3000)"
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]),
    default="INFO",
    help="Logging level (default: INFO)",
)
@click.option(
    "--api-key",
    help="FMP API key (can also be set via FMP_API_KEY environment variable)",
)
@click.option(
    "--text-content",
    is_flag=True,
    default=False,
    help="Include text content alongside structured content in MCP tool responses (default: text content is empty when structured content is present)",
)
@click.option(
    "--cached",
    is_flag=True,
    default=False,
    help="Enable CachedClient: cache time-series data locally in Parquet files to minimize API calls. Cache dir defaults to ~/.aiofmp/cache (override with AIOFMP_CACHE_FILE_PATH).",
)
def mcp_server(
    transport: str,
    host: str,
    port: int,
    log_level: str,
    api_key: str | None,
    text_content: bool,
    cached: bool,
):
    """
    Start the aiofmp MCP server.

    Examples:
        aiofmp mcp-server
        aiofmp mcp-server --transport http --host 0.0.0.0 --port 8080
        aiofmp mcp-server --api-key your_api_key_here
        aiofmp mcp-server --cached
    """
    from .mcp_server import run_server

    logging.getLogger().setLevel(getattr(logging, log_level.upper()))

    if api_key:
        os.environ["FMP_API_KEY"] = api_key

    os.environ["MCP_TRANSPORT"] = transport
    os.environ["MCP_HOST"] = host
    os.environ["MCP_PORT"] = str(port)
    os.environ["MCP_INCLUDE_TEXT_CONTENT"] = str(text_content)

    if cached:
        os.environ["AIOFMP_CACHED"] = "true"

    if not os.getenv("FMP_API_KEY"):
        logger.error("FMP_API_KEY environment variable is required")
        logger.error("Set it via: export FMP_API_KEY=your_api_key_here")
        logger.error("Or use: aiofmp mcp-server --api-key your_api_key_here")
        sys.exit(1)

    logger.info(f"Starting aiofmp MCP server with {transport} transport")
    if cached:
        cache_dir = os.environ.get("AIOFMP_CACHE_FILE_PATH", "~/.aiofmp/cache")
        logger.info(f"CachedClient enabled, cache dir: {cache_dir}")
    if transport == "http":
        logger.info(f"Server will be available at http://{host}:{port}")

    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Harvest commands
# ---------------------------------------------------------------------------

# Shared options for harvest commands
_harvest_options = [
    click.option("--symbols", "-s", default=None, help="Comma-separated symbols (e.g. AAPL,MSFT,GOOGL)."),
    click.option("--symbols-file", default=None, type=click.Path(exists=True), help="Path to file with symbols (one per line)."),
    click.option("--discover", is_flag=True, default=False, help="Use discover mode (call directory.company_symbols())."),
    click.option("--categories", "-c", default=None, help="Comma-separated categories to harvest (default: all)."),
    click.option("--lookback-days", default=1825, type=int, help="Lookback period in days (default: 1825)."),
    click.option("--statement-limit", default=40, type=int, help="Limit for period-based endpoints (default: 40)."),
    click.option("--api-key", default=None, help="FMP API key (or FMP_API_KEY env var)."),
    click.option("--cache-dir", default=None, help="Cache directory (or AIOFMP_CACHE_FILE_PATH env var)."),
    click.option("--log-level", type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]), default="INFO", help="Logging level."),
]


def _add_harvest_options(func):
    """Apply shared harvest options to a click command."""
    for option in reversed(_harvest_options):
        func = option(func)
    return func


def _resolve_api_key(api_key: str | None) -> str:
    """Resolve API key from argument or environment. Exits on failure."""
    resolved = api_key or os.environ.get("FMP_API_KEY")
    if not resolved:
        logger.error("FMP_API_KEY is required. Set via env var or --api-key.")
        sys.exit(1)
    return resolved


def _build_harvest_config(
    symbols: str | None,
    symbols_file: str | None,
    discover: bool,
    categories: str | None,
    lookback_days: int,
    statement_limit: int,
) -> "HarvestConfig":
    """Build HarvestConfig from CLI options."""
    from aiofmp.harvester import HarvestConfig, SymbolsConfig

    # Build SymbolsConfig
    if symbols_file:
        symbols_cfg = SymbolsConfig(mode=f"file:{symbols_file}")
    elif symbols:
        symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
        symbols_cfg = SymbolsConfig(mode="explicit", symbols=symbol_list)
    else:
        symbols_cfg = SymbolsConfig(mode="discover")

    # Build category list
    kwargs: dict = {
        "symbols": symbols_cfg,
        "lookback_days": lookback_days,
        "statement_limit": statement_limit,
    }
    if categories:
        kwargs["categories"] = [c.strip() for c in categories.split(",") if c.strip()]

    return HarvestConfig(**kwargs)


def _print_harvest_results(results: list) -> None:
    """Print a summary table of harvest results."""
    if not results:
        click.echo("\nNo endpoints harvested.")
        return

    click.echo("\nHarvest Results:")

    succeeded = 0
    failed = 0
    total_records = 0

    for r in results:
        entity = r.entity or "(global)"
        if r.error:
            failed += 1
            click.echo(f"  {r.endpoint_name:40s}  {entity:20s}  ERROR: {r.error}")
        else:
            succeeded += 1
            total_records += r.records_fetched
            click.echo(f"  {r.endpoint_name:40s}  {entity:20s}  {r.records_fetched} records")

    click.echo(
        f"\nSummary: {len(results)} endpoints, "
        f"{succeeded} succeeded, {failed} failed, "
        f"{total_records} total records"
    )


@cli.command("harvest")
@_add_harvest_options
def harvest(
    symbols: str | None,
    symbols_file: str | None,
    discover: bool,
    categories: str | None,
    lookback_days: int,
    statement_limit: int,
    api_key: str | None,
    cache_dir: str | None,
    log_level: str,
):
    """Run a single harvest cycle to warm the cache.

    Examples:
        aiofmp harvest --symbols AAPL,MSFT,GOOGL
        aiofmp harvest -s AAPL -c chart,statements
        aiofmp harvest --discover --lookback-days 365
        aiofmp harvest --symbols-file symbols.txt
    """
    from aiofmp import FmpClient
    from aiofmp.cachedclient import CachedClient
    from aiofmp.harvester import Harvester

    logging.getLogger().setLevel(getattr(logging, log_level.upper()))
    resolved_key = _resolve_api_key(api_key)

    if cache_dir:
        os.environ["AIOFMP_CACHE_FILE_PATH"] = cache_dir

    config = _build_harvest_config(
        symbols=symbols,
        symbols_file=symbols_file,
        discover=discover,
        categories=categories,
        lookback_days=lookback_days,
        statement_limit=statement_limit,
    )

    async def _run():
        fmp = FmpClient(api_key=resolved_key)
        cached = CachedClient(fmp)
        harvester = Harvester(cached, config)
        async with cached:
            return await harvester.run_once()

    try:
        results = asyncio.run(_run())
        _print_harvest_results(results)
    except KeyboardInterrupt:
        logger.info("Harvest stopped by user")
    except Exception as e:
        logger.error(f"Harvest error: {e}")
        sys.exit(1)


@cli.command("harvest-serve")
@_add_harvest_options
@click.option("--interval", default=3600, type=int, help="Seconds between harvest cycles (default: 3600).")
@click.option("--no-run-on-start", is_flag=True, default=False, help="Don't run immediately on start.")
def harvest_serve(
    symbols: str | None,
    symbols_file: str | None,
    discover: bool,
    categories: str | None,
    lookback_days: int,
    statement_limit: int,
    api_key: str | None,
    cache_dir: str | None,
    log_level: str,
    interval: int,
    no_run_on_start: bool,
):
    """Run harvest on a schedule.

    Examples:
        aiofmp harvest-serve --symbols AAPL,MSFT
        aiofmp harvest-serve -s AAPL --interval 1800 --no-run-on-start
        aiofmp harvest-serve --discover --interval 7200
    """
    from aiofmp import FmpClient
    from aiofmp.cachedclient import CachedClient
    from aiofmp.harvester import Harvester, SchedulerConfig

    logging.getLogger().setLevel(getattr(logging, log_level.upper()))
    resolved_key = _resolve_api_key(api_key)

    if cache_dir:
        os.environ["AIOFMP_CACHE_FILE_PATH"] = cache_dir

    config = _build_harvest_config(
        symbols=symbols,
        symbols_file=symbols_file,
        discover=discover,
        categories=categories,
        lookback_days=lookback_days,
        statement_limit=statement_limit,
    )
    config.scheduler = SchedulerConfig(
        interval_seconds=interval,
        run_on_start=not no_run_on_start,
    )

    async def _run():
        fmp = FmpClient(api_key=resolved_key)
        cached = CachedClient(fmp)
        harvester = Harvester(cached, config)
        async with cached:
            await harvester.run_scheduled()

    logger.info("Starting harvest-serve (interval=%ds)", interval)

    try:
        asyncio.run(_run())
    except KeyboardInterrupt:
        logger.info("Harvest-serve stopped by user")
    except Exception as e:
        logger.error(f"Harvest-serve error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
