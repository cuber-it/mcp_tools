"""Tests for rss tools."""

import pytest

from mcp_rss_tools.rss import register


class TestImport:
    def test_register_exists(self):
        assert callable(register)


class TestTools:
    def test_feed_read_exists(self):
        from mcp_rss_tools.rss import tools
        assert hasattr(tools, "feed_read")
        assert callable(tools.feed_read)

    def test_feed_add_exists(self):
        from mcp_rss_tools.rss import tools
        assert hasattr(tools, "feed_add")
        assert callable(tools.feed_add)

    def test_feed_list_exists(self):
        from mcp_rss_tools.rss import tools
        assert hasattr(tools, "feed_list")
        assert callable(tools.feed_list)

    def test_feed_remove_exists(self):
        from mcp_rss_tools.rss import tools
        assert hasattr(tools, "feed_remove")
        assert callable(tools.feed_remove)

    def test_entries_exists(self):
        from mcp_rss_tools.rss import tools
        assert hasattr(tools, "entries")
        assert callable(tools.entries)

    def test_entry_read_exists(self):
        from mcp_rss_tools.rss import tools
        assert hasattr(tools, "entry_read")
        assert callable(tools.entry_read)

    def test_opml_import_exists(self):
        from mcp_rss_tools.rss import tools
        assert hasattr(tools, "opml_import")
        assert callable(tools.opml_import)

    def test_opml_export_exists(self):
        from mcp_rss_tools.rss import tools
        assert hasattr(tools, "opml_export")
        assert callable(tools.opml_export)


# TODO: add functional tests
