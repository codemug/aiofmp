"""
MCP Server for Financial Modeling Prep API

This module provides the core MCP server implementation using FastMCP,
exposing all FMP API endpoints as MCP tools for use with AI assistants.
"""

import asyncio
import logging
import os
import sys

from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("FMP MCP Server")


def register_tools():
    """Register all MCP tools from the various modules."""
    try:
        # Import and register tools from each category
        from . import (  # noqa: F401
            analyst_tools,
            calendar_tools,
            chart_tools,
            commodity_tools,
            company_tools,
            cot_tools,
            crypto_tools,
            dcf_tools,
            directory_tools,
            economics_tools,
            etf_tools,
            forex_tools,
            form13f_tools,
            indexes_tools,
            insider_trades_tools,
            market_performance_tools,
            news_tools,
            quote_tools,
            search_tools,
            senate_tools,
            statements_tools,
            technical_indicators_tools,
        )

        logger.info("Successfully registered all MCP tools")
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
