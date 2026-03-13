"""Http — MCP plugin.

HTTP client tools for MCP — requests, JSON, downloads, headers, status checks
"""

from __future__ import annotations

from .client import HttpClient
from . import tools


def register(mcp, config: dict) -> None:
    """Register http tools as MCP tools."""
    client = HttpClient(config)

    @mcp.tool()
    def http_request(url: str, method: str = "GET", data: str = "", headers: str = "", timeout: int = 30) -> str:
        """Make an HTTP request"""
        return tools.http_request(client, url, method, data, headers, timeout)

    @mcp.tool()
    def http_json(url: str, query: str = "") -> str:
        """GET a URL and parse JSON response"""
        return tools.http_json(client, url, query)

    @mcp.tool()
    def http_download(url: str, path: str) -> str:
        """Download a file from URL"""
        return tools.http_download(client, url, path)

    @mcp.tool()
    def http_head(url: str) -> str:
        """Get HTTP headers without body"""
        return tools.http_head(client, url)

    @mcp.tool()
    def http_status(url: str, expected: int = 200) -> str:
        """Check if a URL is reachable (status code)"""
        return tools.http_status(client, url, expected)

    @mcp.tool()
    def http_form_post(url: str, fields: str) -> str:
        """Submit a form (multipart/form-data)"""
        return tools.http_form_post(client, url, fields)

    @mcp.tool()
    def json_query(path: str, query: str = "") -> str:
        """Query a local JSON file"""
        return tools.json_query(client, path, query)
