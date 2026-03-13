"""Scraper — MCP plugin.

Web scraping tools for MCP — fetch pages, extract content, parse metadata
"""

from __future__ import annotations

from .client import ScraperClient
from . import tools


def register(mcp, config: dict) -> None:
    """Register scraper tools as MCP tools."""
    client = ScraperClient(config)

    @mcp.tool()
    def fetch(url: str) -> str:
        """Fetch a URL and return content as clean Markdown"""
        return tools.fetch(client, url)

    @mcp.tool()
    def extract(url: str, selector: str, attribute: str = "") -> str:
        """Extract content using CSS selector"""
        return tools.extract(client, url, selector, attribute)

    @mcp.tool()
    def links(url: str, filter: str = "") -> str:
        """Extract all links from a page"""
        return tools.links(client, url, filter)

    @mcp.tool()
    def metadata(url: str) -> str:
        """Extract page metadata — title, description, OG tags"""
        return tools.metadata(client, url)

    @mcp.tool()
    def sitemap(url: str, limit: int = 100) -> str:
        """Parse sitemap.xml and list URLs"""
        return tools.sitemap(client, url, limit)

    @mcp.tool()
    def table(url: str, selector: str = "table") -> str:
        """Extract HTML table as structured text"""
        return tools.table(client, url, selector)

    @mcp.tool()
    def headers(url: str) -> str:
        """Show HTTP response headers for a URL"""
        return tools.headers(client, url)

    @mcp.tool()
    def status(url: str) -> str:
        """Check HTTP status code of a URL"""
        return tools.status(client, url)
