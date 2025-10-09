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


@click.command()
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
def mcp_server(
    transport: str,
    host: str,
    port: int,
    log_level: str,
    api_key: str | None,
    text_content: bool,
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
    """
    # Set logging level
    logging.getLogger().setLevel(getattr(logging, log_level.upper()))

    # Set API key if provided
    if api_key:
        os.environ["FMP_API_KEY"] = api_key

    # Set transport mode
    os.environ["MCP_TRANSPORT"] = transport
    os.environ["MCP_HOST"] = host
    os.environ["MCP_PORT"] = str(port)

    # Set text content flag
    os.environ["MCP_INCLUDE_TEXT_CONTENT"] = str(text_content)

    # Validate API key
    if not os.getenv("FMP_API_KEY"):
        logger.error("FMP_API_KEY environment variable is required")
        logger.error("Set it via: export FMP_API_KEY=your_api_key_here")
        logger.error("Or use: aiofmp-mcp-server --api-key your_api_key_here")
        sys.exit(1)

    logger.info(f"Starting aiofmp MCP server with {transport} transport")
    if transport == "http":
        logger.info(f"Server will be available at http://{host}:{port}")

    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
