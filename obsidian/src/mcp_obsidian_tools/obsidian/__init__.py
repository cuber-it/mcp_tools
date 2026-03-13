"""Obsidian — MCP plugin.

Obsidian vault tools for MCP — read, write, search, links, tags, frontmatter
"""

from __future__ import annotations

from . import tools


def register(mcp, config: dict) -> None:
    """Register obsidian tools as MCP tools."""
    @mcp.tool()
    def note_read(path: str) -> str:
        """Read a note from the vault"""
        return tools.note_read(path)

    @mcp.tool()
    def note_write(path: str, content: str) -> str:
        """Write or overwrite a note"""
        return tools.note_write(path, content)

    @mcp.tool()
    def note_append(path: str, content: str) -> str:
        """Append text to an existing note"""
        return tools.note_append(path, content)

    @mcp.tool()
    def note_list(folder: str = "", recursive: bool = False) -> str:
        """List notes in a folder"""
        return tools.note_list(folder, recursive)

    @mcp.tool()
    def search(query: str, limit: int = 20) -> str:
        """Full-text search across vault"""
        return tools.search(query, limit)

    @mcp.tool()
    def search_by_tag(tag: str) -> str:
        """Find notes with a specific tag"""
        return tools.search_by_tag(tag)

    @mcp.tool()
    def backlinks(path: str) -> str:
        """Find all notes linking to a given note"""
        return tools.backlinks(path)

    @mcp.tool()
    def outgoing_links(path: str) -> str:
        """List all links from a note"""
        return tools.outgoing_links(path)

    @mcp.tool()
    def tag_list() -> str:
        """List all tags used in the vault"""
        return tools.tag_list()

    @mcp.tool()
    def frontmatter_read(path: str) -> str:
        """Read YAML frontmatter of a note"""
        return tools.frontmatter_read(path)

    @mcp.tool()
    def frontmatter_update(path: str, key: str, value: str) -> str:
        """Update frontmatter fields of a note"""
        return tools.frontmatter_update(path, key, value)
