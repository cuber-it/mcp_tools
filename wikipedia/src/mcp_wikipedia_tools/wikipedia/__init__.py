"""Wikipedia — MCP plugin.

Wikipedia tools for MCP — search, articles, summaries, multilingual
"""

from __future__ import annotations

from .client import WikipediaClient
from . import tools


def register(mcp, config: dict) -> None:
    """Register wikipedia tools as MCP tools."""
    client = WikipediaClient(config)

    @mcp.tool()
    def search(query: str, lang: str = "en", limit: int = 10) -> str:
        """Search Wikipedia articles"""
        return tools.search(client, query, lang, limit)

    @mcp.tool()
    def article(title: str, lang: str = "en") -> str:
        """Get full article content as Markdown"""
        return tools.article(client, title, lang)

    @mcp.tool()
    def summary(title: str, lang: str = "en") -> str:
        """Get article summary (first section)"""
        return tools.summary(client, title, lang)

    @mcp.tool()
    def links(title: str, lang: str = "en") -> str:
        """List all links from an article"""
        return tools.links(client, title, lang)

    @mcp.tool()
    def categories(title: str, lang: str = "en") -> str:
        """List categories of an article"""
        return tools.categories(client, title, lang)

    @mcp.tool()
    def random(lang: str = "en") -> str:
        """Get a random article summary"""
        return tools.random(client, lang)
