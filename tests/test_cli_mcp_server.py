"""Tests for the `aiofmp-mcp-server` CLI (tool-selection flags + listing)."""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from aiofmp.cli import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


class TestListTools:
    def test_list_tools_short_circuits_without_api_key(self, runner):
        """--list-tools must work without FMP_API_KEY so users can discover names."""
        with patch.dict(os.environ, {}, clear=True):
            result = runner.invoke(cli, ["mcp-server", "--list-tools"])
        assert result.exit_code == 0
        assert "chart" in result.output
        assert "quote" in result.output
        assert "  - get_stock_quote" in result.output


class TestSpecValidation:
    def test_unknown_category_errors(self, runner):
        with patch.dict(os.environ, {"FMP_API_KEY": "k"}, clear=True):
            result = runner.invoke(cli, ["mcp-server", "--tools", "bogus_cat"])
        assert result.exit_code != 0
        assert "unknown category" in result.output

    def test_unknown_tool_errors(self, runner):
        with patch.dict(os.environ, {"FMP_API_KEY": "k"}, clear=True):
            result = runner.invoke(
                cli, ["mcp-server", "--tools", "quote(no_such_tool)"]
            )
        assert result.exit_code != 0
        assert "unknown tool" in result.output

    def test_empty_effective_selection_errors(self, runner):
        with patch.dict(os.environ, {"FMP_API_KEY": "k"}, clear=True):
            result = runner.invoke(
                cli,
                [
                    "mcp-server",
                    "--tools",
                    "quote(get_stock_quote)",
                    "--exclude-tools",
                    "quote(get_stock_quote)",
                ],
            )
        assert result.exit_code != 0
        assert "empty" in result.output.lower()

    def test_valid_spec_exports_env_and_runs(self, runner):
        """Valid --tools should be exported as AIOFMP_MCP_TOOLS for register_tools."""
        with patch.dict(os.environ, {"FMP_API_KEY": "k"}, clear=True):
            with patch("aiofmp.cli.asyncio.run") as mock_run:
                mock_run.return_value = None
                result = runner.invoke(
                    cli,
                    [
                        "mcp-server",
                        "--tools",
                        "quote(get_stock_quote)",
                    ],
                )
                # CLI exports the spec into env before calling asyncio.run
                # so register_tools (inside run_server) can pick it up.
                assert os.environ.get("AIOFMP_MCP_TOOLS") == "quote(get_stock_quote)"
        assert result.exit_code == 0
        mock_run.assert_called_once()

    def test_exclude_only_exports_env(self, runner):
        with patch.dict(os.environ, {"FMP_API_KEY": "k"}, clear=True):
            with patch("aiofmp.cli.asyncio.run") as mock_run:
                mock_run.return_value = None
                result = runner.invoke(
                    cli,
                    ["mcp-server", "--exclude-tools", "form13f,senate"],
                )
                assert os.environ.get("AIOFMP_MCP_EXCLUDE_TOOLS") == "form13f,senate"
        assert result.exit_code == 0
