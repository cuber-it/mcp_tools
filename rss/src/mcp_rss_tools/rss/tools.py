"""Pure tool logic for rss — no MCP dependency."""

from __future__ import annotations

def feed_read(url: str, limit: int = 10) -> str:
    """Read a feed and return recent entries"""
    # TODO: implement
    raise NotImplementedError("feed_read")


def feed_add(url: str, name: str = "") -> str:
    """Add a feed to the tracked list"""
    # TODO: implement
    raise NotImplementedError("feed_add")


def feed_list() -> str:
    """List all tracked feeds"""
    # TODO: implement
    raise NotImplementedError("feed_list")


def feed_remove(url: str) -> str:
    """Remove a feed from the tracked list"""
    # TODO: implement
    raise NotImplementedError("feed_remove")


def entries(limit: int = 20, since_hours: int = 24) -> str:
    """List entries across all tracked feeds"""
    # TODO: implement
    raise NotImplementedError("entries")


def entry_read(url: str) -> str:
    """Read full content of a feed entry"""
    # TODO: implement
    raise NotImplementedError("entry_read")


def opml_import(path: str) -> str:
    """Import feeds from OPML file"""
    # TODO: implement
    raise NotImplementedError("opml_import")


def opml_export(path: str) -> str:
    """Export tracked feeds as OPML"""
    # TODO: implement
    raise NotImplementedError("opml_export")

