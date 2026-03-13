"""Paperless — MCP plugin.

Paperless-ngx document management tools for MCP

Config keys:
    url: (required)
    token: (required)
"""

from __future__ import annotations

from .client import PaperlessClient
from . import tools


def register(mcp, config: dict) -> None:
    """Register paperless tools as MCP tools."""
    client = PaperlessClient(config)

    @mcp.tool()
    def document_list(limit: int = 25, tag: str = "", correspondent: str = "") -> str:
        """List documents with optional filters"""
        return tools.document_list(client, limit, tag, correspondent)

    @mcp.tool()
    def document_search(query: str, limit: int = 25) -> str:
        """Full-text search across all documents"""
        return tools.document_search(client, query, limit)

    @mcp.tool()
    def document_get(document_id: int) -> str:
        """Get document details and content"""
        return tools.document_get(client, document_id)

    @mcp.tool()
    def document_upload(path: str, title: str = "") -> str:
        """Upload a new document"""
        return tools.document_upload(client, path, title)

    @mcp.tool()
    def document_download(document_id: int, path: str) -> str:
        """Download a document file"""
        return tools.document_download(client, document_id, path)

    @mcp.tool()
    def tag_list() -> str:
        """List all tags"""
        return tools.tag_list(client)

    @mcp.tool()
    def tag_assign(document_id: int, tag: str) -> str:
        """Assign a tag to a document"""
        return tools.tag_assign(client, document_id, tag)

    @mcp.tool()
    def tag_remove(document_id: int, tag: str) -> str:
        """Remove a tag from a document"""
        return tools.tag_remove(client, document_id, tag)

    @mcp.tool()
    def correspondent_list() -> str:
        """List all correspondents"""
        return tools.correspondent_list(client)

    @mcp.tool()
    def correspondent_assign(document_id: int, correspondent: str) -> str:
        """Assign a correspondent to a document"""
        return tools.correspondent_assign(client, document_id, correspondent)

    @mcp.tool()
    def doctype_list() -> str:
        """List all document types"""
        return tools.doctype_list(client)

    @mcp.tool()
    def doctype_assign(document_id: int, doctype: str) -> str:
        """Assign a document type to a document"""
        return tools.doctype_assign(client, document_id, doctype)
