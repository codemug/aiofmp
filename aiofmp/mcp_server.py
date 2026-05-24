"""
MCP Server for Financial Modeling Prep API

This module provides the core MCP server implementation using FastMCP,
exposing all FMP API endpoints as MCP tools for use with AI assistants.
"""

import asyncio
import importlib
import logging
import os
import sys

from fastmcp import FastMCP

from .mcp_selection import (
    compute_selection,
    get_tool_inventory,
    parse_spec,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("FMP MCP Server")


def _resolve_selection_from_env() -> dict[str, frozenset[str]]:
    """Read ``AIOFMP_MCP_TOOLS`` / ``AIOFMP_MCP_EXCLUDE_TOOLS`` and resolve.

    Returns the per-category allow-set the registrar should honor. Empty env
    vars mean "no restriction on this side".
    """
    inventory = get_tool_inventory()
    include_spec = os.getenv("AIOFMP_MCP_TOOLS", "").strip()
    exclude_spec = os.getenv("AIOFMP_MCP_EXCLUDE_TOOLS", "").strip()
    include = parse_spec(include_spec, inventory) if include_spec else None
    exclude = parse_spec(exclude_spec, inventory) if exclude_spec else None
    return compute_selection(include, exclude, inventory)


def register_tools(selection: dict[str, frozenset[str]] | None = None) -> None:
    """Register MCP tools, optionally restricted to a per-category allow-set.

    Args:
        selection: ``{category: frozenset(tool_names)}`` of tools to keep. When
            ``None``, the selection is resolved from the
            ``AIOFMP_MCP_TOOLS`` / ``AIOFMP_MCP_EXCLUDE_TOOLS`` env vars, falling
            back to "register everything" if neither is set.

    Categories not present in ``selection`` are never imported. Within an
    imported category, tools that aren't in the allow-set are removed via
    ``mcp.remove_tool``.
    """
    inventory = get_tool_inventory()

    if selection is None:
        selection = _resolve_selection_from_env()

    if not selection:
        logger.warning(
            "MCP tool selection is empty; no tools will be registered. "
            "Check AIOFMP_MCP_TOOLS / AIOFMP_MCP_EXCLUDE_TOOLS."
        )
        return

    try:
        for cat in selection:
            importlib.import_module(f"aiofmp.{cat}_tools")

        kept = 0
        removed = 0
        for cat, allowed in selection.items():
            for tool_name in inventory[cat] - allowed:
                mcp.remove_tool(tool_name)
                removed += 1
            kept += len(allowed)

        logger.info(
            "Registered %d MCP tool(s) across %d categor(y/ies); pruned %d",
            kept,
            len(selection),
            removed,
        )
    except ImportError as e:
        logger.error(f"Failed to import tool modules: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to register tools: {e}")
        raise


def setup_error_handling():
    """Setup error handling for MCP tools."""
    # FastMCP doesn't support global error handlers
    # Error handling is done at the individual tool level
    pass


async def run_server():
    """Run the MCP server with the specified transport.

    This function uses FastMCP's run_async method to avoid asyncio event loop conflicts
    that can occur when using the synchronous run method in certain environments.
    """
    try:
        # Get configuration from environment variables
        transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
        host = os.getenv("MCP_HOST", "localhost")
        port = int(os.getenv("MCP_PORT", "3000"))

        # Validate API key
        api_key = os.getenv("FMP_API_KEY")
        if not api_key:
            logger.error("FMP_API_KEY environment variable is required")
            sys.exit(1)
            return  # This line will never be reached, but helps with static analysis

        # Register tools and setup error handling
        register_tools()
        setup_error_handling()

        logger.info(f"Starting FMP MCP Server with {transport} transport")
        logger.info(
            f"API Key: {'*' * (len(api_key) - 4) + api_key[-4:] if len(api_key) > 4 else '****'}"
        )

        # Run the server based on transport type
        if transport == "http":
            logger.info(f"Starting HTTP server on {host}:{port}")
            await mcp.run_async(transport="http", host=host, port=port)
        else:
            logger.info("Starting STDIO server")
            await mcp.run_async(transport="stdio")

    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


def main():
    """Main entry point for the MCP server."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
