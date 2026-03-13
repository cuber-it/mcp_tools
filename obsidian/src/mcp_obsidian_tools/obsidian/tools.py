"""Pure tool logic for obsidian — no MCP dependency."""

from __future__ import annotations

def note_read(path: str) -> str:
    """Read a note from the vault"""
    # TODO: implement
    raise NotImplementedError("note_read")


def note_write(path: str, content: str) -> str:
    """Write or overwrite a note"""
    # TODO: implement
    raise NotImplementedError("note_write")


def note_append(path: str, content: str) -> str:
    """Append text to an existing note"""
    # TODO: implement
    raise NotImplementedError("note_append")


def note_list(folder: str = "", recursive: bool = False) -> str:
    """List notes in a folder"""
    # TODO: implement
    raise NotImplementedError("note_list")


def search(query: str, limit: int = 20) -> str:
    """Full-text search across vault"""
    # TODO: implement
    raise NotImplementedError("search")


def search_by_tag(tag: str) -> str:
    """Find notes with a specific tag"""
    # TODO: implement
    raise NotImplementedError("search_by_tag")


def backlinks(path: str) -> str:
    """Find all notes linking to a given note"""
    # TODO: implement
    raise NotImplementedError("backlinks")


def outgoing_links(path: str) -> str:
    """List all links from a note"""
    # TODO: implement
    raise NotImplementedError("outgoing_links")


def tag_list() -> str:
    """List all tags used in the vault"""
    # TODO: implement
    raise NotImplementedError("tag_list")


def frontmatter_read(path: str) -> str:
    """Read YAML frontmatter of a note"""
    # TODO: implement
    raise NotImplementedError("frontmatter_read")


def frontmatter_update(path: str, key: str, value: str) -> str:
    """Update frontmatter fields of a note"""
    # TODO: implement
    raise NotImplementedError("frontmatter_update")

