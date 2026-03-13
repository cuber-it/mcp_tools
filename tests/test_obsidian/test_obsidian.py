"""Tests for obsidian tools."""

import pytest

from mcp_obsidian_tools.obsidian import register


class TestImport:
    def test_register_exists(self):
        assert callable(register)


class TestTools:
    def test_note_read_exists(self):
        from mcp_obsidian_tools.obsidian import tools
        assert hasattr(tools, "note_read")
        assert callable(tools.note_read)

    def test_note_write_exists(self):
        from mcp_obsidian_tools.obsidian import tools
        assert hasattr(tools, "note_write")
        assert callable(tools.note_write)

    def test_note_append_exists(self):
        from mcp_obsidian_tools.obsidian import tools
        assert hasattr(tools, "note_append")
        assert callable(tools.note_append)

    def test_note_list_exists(self):
        from mcp_obsidian_tools.obsidian import tools
        assert hasattr(tools, "note_list")
        assert callable(tools.note_list)

    def test_search_exists(self):
        from mcp_obsidian_tools.obsidian import tools
        assert hasattr(tools, "search")
        assert callable(tools.search)

    def test_search_by_tag_exists(self):
        from mcp_obsidian_tools.obsidian import tools
        assert hasattr(tools, "search_by_tag")
        assert callable(tools.search_by_tag)

    def test_backlinks_exists(self):
        from mcp_obsidian_tools.obsidian import tools
        assert hasattr(tools, "backlinks")
        assert callable(tools.backlinks)

    def test_outgoing_links_exists(self):
        from mcp_obsidian_tools.obsidian import tools
        assert hasattr(tools, "outgoing_links")
        assert callable(tools.outgoing_links)

    def test_tag_list_exists(self):
        from mcp_obsidian_tools.obsidian import tools
        assert hasattr(tools, "tag_list")
        assert callable(tools.tag_list)

    def test_frontmatter_read_exists(self):
        from mcp_obsidian_tools.obsidian import tools
        assert hasattr(tools, "frontmatter_read")
        assert callable(tools.frontmatter_read)

    def test_frontmatter_update_exists(self):
        from mcp_obsidian_tools.obsidian import tools
        assert hasattr(tools, "frontmatter_update")
        assert callable(tools.frontmatter_update)


# TODO: add functional tests
