"""Rss — MCP plugin.

RSS/Atom feed reader tools for MCP
"""

from __future__ import annotations

from . import tools


def register(mcp, config: dict) -> None:
    """Register rss tools as MCP tools."""
    @mcp.tool()
    def feed_read(url: str, limit: int = 10) -> str:
        """Read a feed and return recent entries"""
        return tools.feed_read(url, limit)

    @mcp.tool()
    def feed_add(url: str, name: str = "") -> str:
        """Add a feed to the tracked list"""
        return tools.feed_add(url, name)

    @mcp.tool()
    def feed_list() -> str:
        """List all tracked feeds"""
        return tools.feed_list()

    @mcp.tool()
    def feed_remove(url: str) -> str:
        """Remove a feed from the tracked list"""
        return tools.feed_remove(url)

    @mcp.tool()
    def entries(limit: int = 20, since_hours: int = 24) -> str:
        """List entries across all tracked feeds"""
        return tools.entries(limit, since_hours)

    @mcp.tool()
    def entry_read(url: str) -> str:
        """Read full content of a feed entry"""
        return tools.entry_read(url)

    @mcp.tool()
    def opml_import(path: str) -> str:
        """Import feeds from OPML file"""
        return tools.opml_import(path)

    @mcp.tool()
    def opml_export(path: str) -> str:
        """Export tracked feeds as OPML"""
        return tools.opml_export(path)
