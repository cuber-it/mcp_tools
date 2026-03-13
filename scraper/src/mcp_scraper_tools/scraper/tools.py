"""Pure tool logic for scraper — no MCP dependency."""

from __future__ import annotations

from .client import ScraperClient

def fetch(client: ScraperClient, url: str) -> str:
    """Fetch a URL and return content as clean Markdown"""
    # TODO: implement
    raise NotImplementedError("fetch")


def extract(client: ScraperClient, url: str, selector: str, attribute: str = "") -> str:
    """Extract content using CSS selector"""
    # TODO: implement
    raise NotImplementedError("extract")


def links(client: ScraperClient, url: str, filter: str = "") -> str:
    """Extract all links from a page"""
    # TODO: implement
    raise NotImplementedError("links")


def metadata(client: ScraperClient, url: str) -> str:
    """Extract page metadata — title, description, OG tags"""
    # TODO: implement
    raise NotImplementedError("metadata")


def sitemap(client: ScraperClient, url: str, limit: int = 100) -> str:
    """Parse sitemap.xml and list URLs"""
    # TODO: implement
    raise NotImplementedError("sitemap")


def table(client: ScraperClient, url: str, selector: str = "table") -> str:
    """Extract HTML table as structured text"""
    # TODO: implement
    raise NotImplementedError("table")


def headers(client: ScraperClient, url: str) -> str:
    """Show HTTP response headers for a URL"""
    # TODO: implement
    raise NotImplementedError("headers")


def status(client: ScraperClient, url: str) -> str:
    """Check HTTP status code of a URL"""
    # TODO: implement
    raise NotImplementedError("status")

