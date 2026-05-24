"""
Unit tests for MCP server

This module provides comprehensive unit tests for the MCP server
in the aiofmp package.
"""

import os
from unittest.mock import patch

import pytest

from aiofmp.base import FMPAuthenticationError
from aiofmp.fmp_client import get_fmp_client, reset_fmp_client
from aiofmp.mcp_server import (
    _resolve_selection_from_env,
    main,
    register_tools,
    run_server,
)


class TestMCPServer:
    """Test MCP server functionality."""

    def setup_method(self):
        """Reset the FMP client before each test."""
        reset_fmp_client()

    def test_get_fmp_client_creation(self):
        """Test FMP client creation."""
        with patch.dict(os.environ, {"FMP_API_KEY": "test_key"}):
            client = get_fmp_client()
            assert client is not None
            assert client.api_key == "test_key"

    def test_get_fmp_client_missing_api_key(self):
        """Test FMP client creation with missing API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(
                FMPAuthenticationError,
                match="FMP_API_KEY environment variable is required",
            ):
                get_fmp_client()

    def test_get_fmp_client_singleton(self):
        """Test that FMP client is a singleton."""
        with patch.dict(os.environ, {"FMP_API_KEY": "test_key"}):
            client1 = get_fmp_client()
            client2 = get_fmp_client()
            assert client1 is client2

    @pytest.mark.asyncio
    async def test_run_server_stdio(self):
        """Test running server with STDIO transport."""
        with patch.dict(
            os.environ, {"FMP_API_KEY": "test_key", "MCP_TRANSPORT": "stdio"}
        ):
            with patch("aiofmp.mcp_server.mcp.run_async") as mock_run_async:
                # Mock the run_async method to return a coroutine
                async def mock_run_coro(*args, **kwargs):
                    pass

                mock_run_async.return_value = mock_run_coro()

                await run_server()

                mock_run_async.assert_called_once_with(transport="stdio")

    @pytest.mark.asyncio
    async def test_run_server_http(self):
        """Test running server with HTTP transport."""
        with patch.dict(
            os.environ,
            {
                "FMP_API_KEY": "test_key",
                "MCP_TRANSPORT": "http",
                "MCP_HOST": "localhost",
                "MCP_PORT": "3000",
            },
        ):
            with patch("aiofmp.mcp_server.mcp.run_async") as mock_run_async:
                # Mock the run_async method to return a coroutine
                async def mock_run_coro(*args, **kwargs):
                    pass

                mock_run_async.return_value = mock_run_coro()

                await run_server()

                mock_run_async.assert_called_once_with(
                    transport="http", host="localhost", port=3000
                )

    @pytest.mark.asyncio
    async def test_run_server_missing_api_key(self):
        """Test running server with missing API key."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("sys.exit") as mock_exit:
                # Mock sys.exit to raise SystemExit to prevent further execution
                mock_exit.side_effect = SystemExit(1)

                with pytest.raises(SystemExit):
                    await run_server()

                mock_exit.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_run_server_keyboard_interrupt(self):
        """Test handling keyboard interrupt."""
        with patch.dict(os.environ, {"FMP_API_KEY": "test_key"}):
            with patch("aiofmp.mcp_server.mcp.run_async") as mock_run_async:
                # Mock the run_async method to raise KeyboardInterrupt
                async def mock_run_coro(*args, **kwargs):
                    raise KeyboardInterrupt()

                mock_run_async.return_value = mock_run_coro()

                await run_server()

                # Should not raise an exception
                assert True

    @pytest.mark.asyncio
    async def test_run_server_general_exception(self):
        """Test handling general exceptions."""
        with patch.dict(os.environ, {"FMP_API_KEY": "test_key"}):
            with patch("aiofmp.mcp_server.mcp.run_async") as mock_run_async:
                mock_run_async.side_effect = Exception("Server error")

                with patch("sys.exit") as mock_exit:
                    await run_server()
                    mock_exit.assert_called_once_with(1)

    def test_main_function(self):
        """Test main function entry point."""
        with patch("aiofmp.mcp_server.asyncio.run") as mock_asyncio_run:
            main()

            # Verify that asyncio.run was called once
            mock_asyncio_run.assert_called_once()
            # The argument should be the result of calling run_server()
            args, _ = mock_asyncio_run.call_args
            # We can't easily test the exact coroutine object, so just verify it was called
            assert len(args) == 1


# Error handler tests removed - FastMCP doesn't support global error handlers
# Error handling is done at the individual tool level


class TestMCPServerConfiguration:
    """Test MCP server configuration."""

    def test_environment_variables(self):
        """Test environment variable configuration."""
        with patch.dict(
            os.environ,
            {
                "FMP_API_KEY": "test_key",
                "MCP_TRANSPORT": "http",
                "MCP_HOST": "localhost",
                "MCP_PORT": "3000",
            },
        ):
            assert os.getenv("FMP_API_KEY") == "test_key"
            assert os.getenv("MCP_TRANSPORT") == "http"
            assert os.getenv("MCP_HOST") == "localhost"
            assert os.getenv("MCP_PORT") == "3000"

    def test_default_configuration(self):
        """Test default configuration values."""
        with patch.dict(os.environ, {}, clear=True):
            assert os.getenv("MCP_TRANSPORT", "stdio") == "stdio"
            assert os.getenv("MCP_HOST", "localhost") == "localhost"
            assert os.getenv("MCP_PORT", "3000") == "3000"

    def test_port_conversion(self):
        """Test port string to integer conversion."""
        with patch.dict(os.environ, {"MCP_PORT": "8080"}):
            port = int(os.getenv("MCP_PORT", "3000"))
            assert port == 8080
            assert isinstance(port, int)


class TestRegisterToolsSelection:
    """Tests for tool-selection behavior in register_tools()."""

    def test_resolve_selection_no_env_returns_full_inventory(self):
        with patch.dict(os.environ, {}, clear=True):
            sel = _resolve_selection_from_env()
        assert len(sel) == 22
        assert sum(len(v) for v in sel.values()) == 177

    def test_resolve_selection_include_only(self):
        with patch.dict(os.environ, {"AIOFMP_MCP_TOOLS": "quote,search"}, clear=True):
            sel = _resolve_selection_from_env()
        assert set(sel) == {"quote", "search"}

    def test_resolve_selection_exclude_only(self):
        with patch.dict(
            os.environ, {"AIOFMP_MCP_EXCLUDE_TOOLS": "form13f,senate"}, clear=True
        ):
            sel = _resolve_selection_from_env()
        assert "form13f" not in sel
        assert "senate" not in sel
        assert "quote" in sel

    def test_resolve_selection_include_and_exclude(self):
        with patch.dict(
            os.environ,
            {
                "AIOFMP_MCP_TOOLS": "chart(*),quote(*)",
                "AIOFMP_MCP_EXCLUDE_TOOLS": "chart(get_intraday_1min)",
            },
            clear=True,
        ):
            sel = _resolve_selection_from_env()
        assert set(sel) == {"chart", "quote"}
        assert "get_intraday_1min" not in sel["chart"]
        assert "get_intraday_1hour" in sel["chart"]

    def test_resolve_selection_per_tool(self):
        with patch.dict(
            os.environ,
            {"AIOFMP_MCP_TOOLS": "quote(get_stock_quote)"},
            clear=True,
        ):
            sel = _resolve_selection_from_env()
        assert sel == {"quote": frozenset({"get_stock_quote"})}

    def test_register_tools_imports_only_selected_categories(self):
        """register_tools() must import exactly the modules in the selection
        and call mcp.remove_tool for tools outside each category's allow-set.

        Mocks importlib + remove_tool so the global `mcp` instance shared with
        other tests isn't mutated.
        """
        from aiofmp.mcp_selection import get_tool_inventory
        from aiofmp.mcp_server import mcp as mcp_instance

        selection = {
            "quote": frozenset({"get_stock_quote"}),
            "search": frozenset(),  # whole-category drop after import
        }
        with patch("aiofmp.mcp_server.importlib.import_module") as mock_import:
            with patch.object(mcp_instance, "remove_tool") as mock_remove:
                register_tools(selection=selection)

        imported = {call.args[0] for call in mock_import.call_args_list}
        assert imported == {"aiofmp.quote_tools", "aiofmp.search_tools"}

        removed = {call.args[0] for call in mock_remove.call_args_list}
        inv = get_tool_inventory()
        expected_removed = (inv["quote"] - {"get_stock_quote"}) | inv["search"]
        assert removed == set(expected_removed)

    def test_register_tools_empty_selection_is_noop(self, caplog):
        register_tools(selection={})
        assert any(
            "no tools will be registered" in rec.message for rec in caplog.records
        )


if __name__ == "__main__":
    pytest.main([__file__])
