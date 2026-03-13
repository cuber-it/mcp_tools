"""Pure tool logic for http — no MCP dependency."""

from __future__ import annotations

from .client import HttpClient

def http_request(client: HttpClient, url: str, method: str = "GET", data: str = "", headers: str = "", timeout: int = 30) -> str:
    """Make an HTTP request"""
    # TODO: implement
    raise NotImplementedError("http_request")


def http_json(client: HttpClient, url: str, query: str = "") -> str:
    """GET a URL and parse JSON response"""
    # TODO: implement
    raise NotImplementedError("http_json")


def http_download(client: HttpClient, url: str, path: str) -> str:
    """Download a file from URL"""
    # TODO: implement
    raise NotImplementedError("http_download")


def http_head(client: HttpClient, url: str) -> str:
    """Get HTTP headers without body"""
    # TODO: implement
    raise NotImplementedError("http_head")


def http_status(client: HttpClient, url: str, expected: int = 200) -> str:
    """Check if a URL is reachable (status code)"""
    # TODO: implement
    raise NotImplementedError("http_status")


def http_form_post(client: HttpClient, url: str, fields: str) -> str:
    """Submit a form (multipart/form-data)"""
    # TODO: implement
    raise NotImplementedError("http_form_post")


def json_query(client: HttpClient, path: str, query: str = "") -> str:
    """Query a local JSON file"""
    # TODO: implement
    raise NotImplementedError("json_query")

