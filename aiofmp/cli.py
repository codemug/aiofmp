"""
Command Line Interface for aiofmp

This module provides the CLI entrypoint for running the MCP server.
"""

import asyncio
import logging
import os
import sys

import click

from .mcp_server import run_server

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.group()
def cli() -> None:
    """aiofmp — Financial Modeling Prep async client toolkit."""


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
@click.option(
    "--tools",
    "tools_spec",
    default=None,
    help=(
        "Restrict which MCP tools are registered. Spec syntax: "
        "'category' or 'category(*)' for all tools in a category, "
        "'category(tool1,tool2)' for specific tools, comma-separated. "
        "Example: --tools 'chart(*),quote(get_stock_quote),search'. "
        "Use --list-tools to discover names. Env: AIOFMP_MCP_TOOLS."
    ),
)
@click.option(
    "--exclude-tools",
    "exclude_tools_spec",
    default=None,
    help=(
        "Same syntax as --tools, but prunes from the include set. "
        "Useful with or without --tools. Env: AIOFMP_MCP_EXCLUDE_TOOLS."
    ),
)
@click.option(
    "--list-tools",
    "list_tools",
    is_flag=True,
    default=False,
    help="Print available categories and tools, then exit.",
)
def mcp_server(
    transport: str,
    host: str,
    port: int,
    log_level: str,
    api_key: str | None,
    text_content: bool,
    cached: bool,
    tools_spec: str | None,
    exclude_tools_spec: str | None,
    list_tools: bool,
):
    """
    Start the aiofmp MCP server.

    This command starts the Model Context Protocol (MCP) server that exposes
    all Financial Modeling Prep API endpoints as AI-friendly tools.

    Examples:
        # Start with STDIO transport (for Claude Desktop)
        aiofmp-mcp-server

        # Start with HTTP transport
        aiofmp-mcp-server --transport http --host 0.0.0.0 --port 8080

        # Set API key via command line
        aiofmp-mcp-server --api-key your_api_key_here

        # Set log level
        aiofmp-mcp-server --log-level DEBUG

        # Include text content alongside structured content
        aiofmp-mcp-server --text-content

        # Enable local caching of time-series data
        aiofmp-mcp-server --cached
    """
    # Set logging level
    logging.getLogger().setLevel(getattr(logging, log_level.upper()))

    # --list-tools is a discovery short-circuit; no server start, no API key needed.
    if list_tools:
        from .mcp_selection import format_inventory

        click.echo(format_inventory())
        return

    # Validate tool selection specs early so a bad CLI value errors out before
    # we open any client sessions. We re-parse them inside register_tools(),
    # but doing it here lets click report errors with proper exit codes.
    if tools_spec is not None or exclude_tools_spec is not None:
        from .mcp_selection import compute_selection, get_tool_inventory, parse_spec

        inventory = get_tool_inventory()
        try:
            include = parse_spec(tools_spec, inventory) if tools_spec else None
            exclude = (
                parse_spec(exclude_tools_spec, inventory)
                if exclude_tools_spec
                else None
            )
            effective = compute_selection(include, exclude, inventory)
        except ValueError as e:
            raise click.UsageError(str(e)) from e
        if not effective:
            raise click.UsageError(
                "Tool selection is empty after combining --tools and --exclude-tools; "
                "no tools would be registered."
            )
        if tools_spec:
            os.environ["AIOFMP_MCP_TOOLS"] = tools_spec
        if exclude_tools_spec:
            os.environ["AIOFMP_MCP_EXCLUDE_TOOLS"] = exclude_tools_spec

    # Set API key if provided
    if api_key:
        os.environ["FMP_API_KEY"] = api_key

    # Set transport mode
    os.environ["MCP_TRANSPORT"] = transport
    os.environ["MCP_HOST"] = host
    os.environ["MCP_PORT"] = str(port)

    # Set text content flag
    os.environ["MCP_INCLUDE_TEXT_CONTENT"] = str(text_content)

    # Set cached flag
    if cached:
        os.environ["AIOFMP_CACHED"] = "true"

    # Validate API key
    if not os.getenv("FMP_API_KEY"):
        logger.error("FMP_API_KEY environment variable is required")
        logger.error("Set it via: export FMP_API_KEY=your_api_key_here")
        logger.error("Or use: aiofmp-mcp-server --api-key your_api_key_here")
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


from aiofmp.harvester.cli import harvest as _harvest_cmd  # noqa: E402
from aiofmp.harvester.cli import harvest_status as _harvest_status_cmd  # noqa: E402

cli.add_command(_harvest_cmd)
cli.add_command(_harvest_status_cmd)


if __name__ == "__main__":
    cli()
