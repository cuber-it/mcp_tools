"""Arxiv — MCP plugin.

ArXiv paper search and retrieval tools for MCP
"""

from __future__ import annotations

from .client import ArxivClient
from . import tools


def register(mcp, config: dict) -> None:
    """Register arxiv tools as MCP tools."""
    client = ArxivClient(config)

    @mcp.tool()
    def search(query: str, limit: int = 10, sort_by: str = "relevance") -> str:
        """Search arXiv papers by query"""
        return tools.search(client, query, limit, sort_by)

    @mcp.tool()
    def abstract(arxiv_id: str) -> str:
        """Get paper abstract by arXiv ID"""
        return tools.abstract(client, arxiv_id)

    @mcp.tool()
    def paper(arxiv_id: str) -> str:
        """Get full paper metadata — title, authors, abstract, categories, dates"""
        return tools.paper(client, arxiv_id)

    @mcp.tool()
    def download(arxiv_id: str, path: str) -> str:
        """Download paper PDF to local path"""
        return tools.download(client, arxiv_id, path)

    @mcp.tool()
    def authors(arxiv_id: str) -> str:
        """List authors of a paper"""
        return tools.authors(client, arxiv_id)

    @mcp.tool()
    def recent(category: str, limit: int = 10) -> str:
        """List recent papers in a category"""
        return tools.recent(client, category, limit)
