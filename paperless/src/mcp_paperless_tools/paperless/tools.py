"""Pure tool logic for paperless — no MCP dependency."""

from __future__ import annotations

from .client import PaperlessClient

def document_list(client: PaperlessClient, limit: int = 25, tag: str = "", correspondent: str = "") -> str:
    """List documents with optional filters"""
    # TODO: implement
    raise NotImplementedError("document_list")


def document_search(client: PaperlessClient, query: str, limit: int = 25) -> str:
    """Full-text search across all documents"""
    # TODO: implement
    raise NotImplementedError("document_search")


def document_get(client: PaperlessClient, document_id: int) -> str:
    """Get document details and content"""
    # TODO: implement
    raise NotImplementedError("document_get")


def document_upload(client: PaperlessClient, path: str, title: str = "") -> str:
    """Upload a new document"""
    # TODO: implement
    raise NotImplementedError("document_upload")


def document_download(client: PaperlessClient, document_id: int, path: str) -> str:
    """Download a document file"""
    # TODO: implement
    raise NotImplementedError("document_download")


def tag_list(client: PaperlessClient) -> str:
    """List all tags"""
    # TODO: implement
    raise NotImplementedError("tag_list")


def tag_assign(client: PaperlessClient, document_id: int, tag: str) -> str:
    """Assign a tag to a document"""
    # TODO: implement
    raise NotImplementedError("tag_assign")


def tag_remove(client: PaperlessClient, document_id: int, tag: str) -> str:
    """Remove a tag from a document"""
    # TODO: implement
    raise NotImplementedError("tag_remove")


def correspondent_list(client: PaperlessClient) -> str:
    """List all correspondents"""
    # TODO: implement
    raise NotImplementedError("correspondent_list")


def correspondent_assign(client: PaperlessClient, document_id: int, correspondent: str) -> str:
    """Assign a correspondent to a document"""
    # TODO: implement
    raise NotImplementedError("correspondent_assign")


def doctype_list(client: PaperlessClient) -> str:
    """List all document types"""
    # TODO: implement
    raise NotImplementedError("doctype_list")


def doctype_assign(client: PaperlessClient, document_id: int, doctype: str) -> str:
    """Assign a document type to a document"""
    # TODO: implement
    raise NotImplementedError("doctype_assign")

