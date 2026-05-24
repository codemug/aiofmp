"""Tool-selection grammar for the MCP server.

Lets users restrict which of the 177 MCP tools get registered. Supports
category-level and per-tool granularity via a small spec grammar:

    chart                                 -> all tools in chart
    chart(*)                              -> all tools in chart
    chart(get_intraday_1hour)             -> just that one tool
    chart(get_intraday_1hour,get_historical_price_full)  -> those tools
    *                                     -> everything (default)

A spec is a comma-separated list of such entries. Two specs can be combined:
the ``--tools`` allowlist defines the universe and ``--exclude-tools`` prunes
from it.

The tool inventory is discovered by AST-scanning ``aiofmp/*_tools.py`` for
``@mcp.tool``-decorated ``(async )def`` functions. This avoids importing the
tool modules (which would side-effect the global ``mcp`` instance) just to
validate a CLI flag.
"""

from __future__ import annotations

import ast
import functools
import pathlib

#: ``None`` in the allow-set means "all tools in this category".
#: A ``frozenset`` means exactly those tool names.
CategoryAllow = frozenset[str] | None
ParsedSpec = dict[str, CategoryAllow]


@functools.cache
def get_tool_inventory() -> dict[str, frozenset[str]]:
    """Return ``{category: frozenset(tool_names)}`` for every ``*_tools.py``.

    Result is cached for the process lifetime. The scan reads files only;
    it does not import the tool modules.
    """
    inv: dict[str, frozenset[str]] = {}
    here = pathlib.Path(__file__).parent
    for path in sorted(here.glob("*_tools.py")):
        if path.name == "mcp_tools.py":
            continue
        tree = ast.parse(path.read_text())
        tools: list[str] = []
        for node in tree.body:
            if not isinstance(node, ast.AsyncFunctionDef | ast.FunctionDef):
                continue
            for dec in node.decorator_list:
                target = dec.func if isinstance(dec, ast.Call) else dec
                if (
                    isinstance(target, ast.Attribute)
                    and target.attr == "tool"
                    and isinstance(target.value, ast.Name)
                    and target.value.id == "mcp"
                ):
                    tools.append(node.name)
                    break
        category = path.stem.removesuffix("_tools")
        inv[category] = frozenset(tools)
    return inv


def _split_top_level(spec: str) -> list[str]:
    """Split ``spec`` on commas, respecting parentheses."""
    parts: list[str] = []
    depth = 0
    start = 0
    for i, ch in enumerate(spec):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                raise ValueError(f"unmatched ')' at position {i} in spec {spec!r}")
        elif ch == "," and depth == 0:
            parts.append(spec[start:i])
            start = i + 1
    if depth != 0:
        raise ValueError(f"unmatched '(' in spec {spec!r}")
    parts.append(spec[start:])
    return [p.strip() for p in parts if p.strip()]


def _parse_entry(
    entry: str, inventory: dict[str, frozenset[str]]
) -> tuple[str, CategoryAllow]:
    """Parse one entry like ``chart`` or ``chart(*)`` or ``chart(t1,t2)``."""
    if "(" not in entry:
        name = entry.strip()
        return (name, None)

    if not entry.endswith(")"):
        raise ValueError(
            f"malformed entry {entry!r}; expected 'category' or 'category(...)'"
        )
    name, _, inside = entry[:-1].partition("(")
    name = name.strip()
    inside = inside.strip()
    if not inside:
        raise ValueError(
            f"empty parens in {entry!r}; use '{name}(*)' or list tool names"
        )
    if inside == "*":
        return (name, None)

    tool_names = [t.strip() for t in inside.split(",")]
    if any(not t for t in tool_names):
        raise ValueError(f"empty tool name in {entry!r}")
    return (name, frozenset(tool_names))


def parse_spec(
    spec: str, inventory: dict[str, frozenset[str]] | None = None
) -> ParsedSpec:
    """Parse a comma-separated tool spec into ``{category: allow-set}``.

    Validates every category and every tool name against the inventory.
    """
    if inventory is None:
        inventory = get_tool_inventory()
    entries = _split_top_level(spec)
    if not entries:
        raise ValueError("empty spec")

    result: ParsedSpec = {}
    for entry in entries:
        cat, allow = _parse_entry(entry, inventory)
        if cat == "*":
            if len(entries) != 1:
                raise ValueError("'*' must be the only entry when used")
            return dict.fromkeys(inventory)
        if not cat:
            raise ValueError(f"empty category name in {entry!r}")
        if cat not in inventory:
            raise ValueError(f"unknown category {cat!r}; valid: {sorted(inventory)}")
        if cat in result:
            raise ValueError(f"duplicate category {cat!r} in spec")
        if allow is not None:
            unknown = allow - inventory[cat]
            if unknown:
                raise ValueError(
                    f"unknown tool(s) in {cat!r}: {sorted(unknown)}; "
                    f"valid tools: {sorted(inventory[cat])}"
                )
        result[cat] = allow
    return result


def compute_selection(
    include: ParsedSpec | None,
    exclude: ParsedSpec | None,
    inventory: dict[str, frozenset[str]] | None = None,
) -> dict[str, frozenset[str]]:
    """Combine ``include`` and ``exclude`` into a per-category allow-set.

    Semantics:
      - ``include=None`` → start with everything in the inventory.
      - ``include`` set → start with just those (categories, tools).
      - ``exclude`` then prunes from the working set; categories that end up
        empty are dropped entirely.

    The returned dict maps each surviving category to the exact frozenset of
    tools that should remain registered. Categories absent from the result
    should not be imported at all.
    """
    if inventory is None:
        inventory = get_tool_inventory()

    if include is None:
        working: dict[str, set[str]] = {c: set(inventory[c]) for c in inventory}
    else:
        working = {}
        for cat, allow in include.items():
            working[cat] = set(inventory[cat]) if allow is None else set(allow)

    if exclude:
        for cat, allow in exclude.items():
            if cat not in working:
                continue
            if allow is None:
                del working[cat]
            else:
                working[cat] -= allow
                if not working[cat]:
                    del working[cat]

    return {c: frozenset(t) for c, t in working.items() if t}


def format_inventory(
    inventory: dict[str, frozenset[str]] | None = None,
    restrict: list[str] | None = None,
) -> str:
    """Human-readable inventory listing for ``--list-tools``."""
    if inventory is None:
        inventory = get_tool_inventory()
    lines: list[str] = []
    cats = sorted(inventory) if restrict is None else restrict
    for cat in cats:
        if cat not in inventory:
            lines.append(f"{cat}: unknown category")
            continue
        tools = sorted(inventory[cat])
        lines.append(f"{cat} ({len(tools)}):")
        for t in tools:
            lines.append(f"  - {t}")
    return "\n".join(lines)
