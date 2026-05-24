"""Tests for the MCP tool-selection grammar and inventory."""

from __future__ import annotations

import pytest

from aiofmp.mcp_selection import (
    compute_selection,
    format_inventory,
    get_tool_inventory,
    parse_spec,
)


@pytest.fixture
def fake_inventory() -> dict[str, frozenset[str]]:
    """Small inventory we control, so parser tests don't drift with real tool names."""
    return {
        "chart": frozenset({"get_intraday_1min", "get_intraday_1hour", "get_full"}),
        "quote": frozenset({"get_stock_quote", "get_aftermarket_quote"}),
        "search": frozenset({"search_symbols", "search_companies"}),
    }


class TestInventory:
    def test_inventory_has_22_categories(self):
        inv = get_tool_inventory()
        assert len(inv) == 22

    def test_inventory_total_tool_count(self):
        inv = get_tool_inventory()
        total = sum(len(v) for v in inv.values())
        assert total == 177

    def test_inventory_contains_known_tools(self):
        inv = get_tool_inventory()
        assert "get_stock_quote" in inv["quote"]
        assert "search_symbols" in inv["search"]
        assert "get_intraday_1hour" in inv["chart"]

    def test_inventory_excludes_helper_module(self):
        inv = get_tool_inventory()
        assert "mcp" not in inv  # mcp_tools.py has no @mcp.tool defs

    def test_inventory_is_cached(self):
        assert get_tool_inventory() is get_tool_inventory()


class TestParseSpec:
    def test_bare_category(self, fake_inventory):
        result = parse_spec("chart", fake_inventory)
        assert result == {"chart": None}

    def test_star_in_parens(self, fake_inventory):
        result = parse_spec("chart(*)", fake_inventory)
        assert result == {"chart": None}

    def test_single_tool(self, fake_inventory):
        result = parse_spec("chart(get_intraday_1hour)", fake_inventory)
        assert result == {"chart": frozenset({"get_intraday_1hour"})}

    def test_multiple_tools(self, fake_inventory):
        result = parse_spec(
            "chart(get_intraday_1hour,get_intraday_1min)", fake_inventory
        )
        assert result == {
            "chart": frozenset({"get_intraday_1hour", "get_intraday_1min"})
        }

    def test_multiple_categories(self, fake_inventory):
        result = parse_spec("chart(*),quote(get_stock_quote),search", fake_inventory)
        assert result == {
            "chart": None,
            "quote": frozenset({"get_stock_quote"}),
            "search": None,
        }

    def test_whitespace_tolerated(self, fake_inventory):
        result = parse_spec(
            "  chart ( get_intraday_1hour , get_full ) , quote ", fake_inventory
        )
        assert result == {
            "chart": frozenset({"get_intraday_1hour", "get_full"}),
            "quote": None,
        }

    def test_universal_star(self, fake_inventory):
        result = parse_spec("*", fake_inventory)
        assert result == dict.fromkeys(fake_inventory)

    def test_star_with_other_entries_errors(self, fake_inventory):
        with pytest.raises(ValueError, match="must be the only entry"):
            parse_spec("*,chart", fake_inventory)

    def test_unknown_category_errors(self, fake_inventory):
        with pytest.raises(ValueError, match="unknown category 'bogus'"):
            parse_spec("bogus", fake_inventory)

    def test_unknown_tool_errors(self, fake_inventory):
        with pytest.raises(ValueError, match="unknown tool"):
            parse_spec("chart(no_such_tool)", fake_inventory)

    def test_empty_parens_errors(self, fake_inventory):
        with pytest.raises(ValueError, match="empty parens"):
            parse_spec("chart()", fake_inventory)

    def test_empty_tool_name_errors(self, fake_inventory):
        with pytest.raises(ValueError, match="empty tool name"):
            parse_spec("chart(get_full,)", fake_inventory)

    def test_duplicate_category_errors(self, fake_inventory):
        with pytest.raises(ValueError, match="duplicate category"):
            parse_spec("chart(*),chart(get_full)", fake_inventory)

    def test_unmatched_open_paren_errors(self, fake_inventory):
        with pytest.raises(ValueError, match="unmatched '\\('"):
            parse_spec("chart(get_full", fake_inventory)

    def test_unmatched_close_paren_errors(self, fake_inventory):
        with pytest.raises(ValueError, match="unmatched '\\)'"):
            parse_spec("chart)", fake_inventory)

    def test_empty_spec_errors(self, fake_inventory):
        with pytest.raises(ValueError, match="empty spec"):
            parse_spec("", fake_inventory)

    def test_only_commas_errors(self, fake_inventory):
        with pytest.raises(ValueError, match="empty spec"):
            parse_spec(",,", fake_inventory)


class TestComputeSelection:
    def test_no_filters_returns_full_inventory(self, fake_inventory):
        result = compute_selection(None, None, fake_inventory)
        assert {c: set(t) for c, t in result.items()} == {
            c: set(t) for c, t in fake_inventory.items()
        }

    def test_include_only_category(self, fake_inventory):
        include = parse_spec("chart", fake_inventory)
        result = compute_selection(include, None, fake_inventory)
        assert set(result) == {"chart"}
        assert result["chart"] == fake_inventory["chart"]

    def test_include_specific_tools(self, fake_inventory):
        include = parse_spec("chart(get_full)", fake_inventory)
        result = compute_selection(include, None, fake_inventory)
        assert result == {"chart": frozenset({"get_full"})}

    def test_exclude_only_whole_category(self, fake_inventory):
        exclude = parse_spec("chart", fake_inventory)
        result = compute_selection(None, exclude, fake_inventory)
        assert "chart" not in result
        assert "quote" in result
        assert "search" in result

    def test_exclude_only_specific_tool(self, fake_inventory):
        exclude = parse_spec("chart(get_intraday_1min)", fake_inventory)
        result = compute_selection(None, exclude, fake_inventory)
        assert "get_intraday_1min" not in result["chart"]
        assert "get_intraday_1hour" in result["chart"]

    def test_include_and_exclude_combined(self, fake_inventory):
        include = parse_spec("chart(*),quote(*)", fake_inventory)
        exclude = parse_spec("chart(get_intraday_1min)", fake_inventory)
        result = compute_selection(include, exclude, fake_inventory)
        assert set(result) == {"chart", "quote"}
        assert "get_intraday_1min" not in result["chart"]
        assert "get_intraday_1hour" in result["chart"]
        assert result["quote"] == fake_inventory["quote"]

    def test_exclude_prunes_to_empty_drops_category(self, fake_inventory):
        include = parse_spec("chart(get_full)", fake_inventory)
        exclude = parse_spec("chart(get_full)", fake_inventory)
        result = compute_selection(include, exclude, fake_inventory)
        assert "chart" not in result

    def test_exclude_unrelated_category_is_noop(self, fake_inventory):
        include = parse_spec("chart", fake_inventory)
        exclude = parse_spec("quote", fake_inventory)
        result = compute_selection(include, exclude, fake_inventory)
        assert set(result) == {"chart"}


class TestFormatInventory:
    def test_format_includes_all_categories(self, fake_inventory):
        out = format_inventory(fake_inventory)
        assert "chart" in out
        assert "quote" in out
        assert "search" in out

    def test_format_lists_tools_indented(self, fake_inventory):
        out = format_inventory(fake_inventory)
        assert "  - get_stock_quote" in out

    def test_format_restrict_to_one_category(self, fake_inventory):
        out = format_inventory(fake_inventory, restrict=["chart"])
        assert "chart" in out
        assert "quote" not in out

    def test_format_unknown_category_reported(self, fake_inventory):
        out = format_inventory(fake_inventory, restrict=["bogus"])
        assert "unknown category" in out
