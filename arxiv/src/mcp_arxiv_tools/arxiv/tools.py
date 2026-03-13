"""Pure tool logic for arxiv — no MCP dependency."""

from __future__ import annotations

from .client import ArxivClient

def search(client: ArxivClient, query: str, limit: int = 10, sort_by: str = "relevance") -> str:
    """Search arXiv papers by query"""
    # TODO: implement
    raise NotImplementedError("search")


def abstract(client: ArxivClient, arxiv_id: str) -> str:
    """Get paper abstract by arXiv ID"""
    # TODO: implement
    raise NotImplementedError("abstract")


def paper(client: ArxivClient, arxiv_id: str) -> str:
    """Get full paper metadata — title, authors, abstract, categories, dates"""
    # TODO: implement
    raise NotImplementedError("paper")


def download(client: ArxivClient, arxiv_id: str, path: str) -> str:
    """Download paper PDF to local path"""
    # TODO: implement
    raise NotImplementedError("download")


def authors(client: ArxivClient, arxiv_id: str) -> str:
    """List authors of a paper"""
    # TODO: implement
    raise NotImplementedError("authors")


def recent(client: ArxivClient, category: str, limit: int = 10) -> str:
    """List recent papers in a category"""
    # TODO: implement
    raise NotImplementedError("recent")

