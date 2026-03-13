"""Pure tool logic for wikipedia — no MCP dependency."""

from __future__ import annotations

from .client import WikipediaClient

def search(client: WikipediaClient, query: str, lang: str = "en", limit: int = 10) -> str:
    """Search Wikipedia articles"""
    # TODO: implement
    raise NotImplementedError("search")


def article(client: WikipediaClient, title: str, lang: str = "en") -> str:
    """Get full article content as Markdown"""
    # TODO: implement
    raise NotImplementedError("article")


def summary(client: WikipediaClient, title: str, lang: str = "en") -> str:
    """Get article summary (first section)"""
    # TODO: implement
    raise NotImplementedError("summary")


def links(client: WikipediaClient, title: str, lang: str = "en") -> str:
    """List all links from an article"""
    # TODO: implement
    raise NotImplementedError("links")


def categories(client: WikipediaClient, title: str, lang: str = "en") -> str:
    """List categories of an article"""
    # TODO: implement
    raise NotImplementedError("categories")


def random(client: WikipediaClient, lang: str = "en") -> str:
    """Get a random article summary"""
    # TODO: implement
    raise NotImplementedError("random")

