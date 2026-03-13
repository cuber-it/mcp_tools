"""Tests for scraper tools."""

import pytest

from mcp_scraper_tools.scraper import register
from mcp_scraper_tools.scraper.client import ScraperClient


class TestImport:
    def test_register_exists(self):
        assert callable(register)

    def test_client_class_exists(self):
        assert ScraperClient is not None


class TestTools:
    def test_fetch_exists(self):
        from mcp_scraper_tools.scraper import tools
        assert hasattr(tools, "fetch")
        assert callable(tools.fetch)

    def test_extract_exists(self):
        from mcp_scraper_tools.scraper import tools
        assert hasattr(tools, "extract")
        assert callable(tools.extract)

    def test_links_exists(self):
        from mcp_scraper_tools.scraper import tools
        assert hasattr(tools, "links")
        assert callable(tools.links)

    def test_metadata_exists(self):
        from mcp_scraper_tools.scraper import tools
        assert hasattr(tools, "metadata")
        assert callable(tools.metadata)

    def test_sitemap_exists(self):
        from mcp_scraper_tools.scraper import tools
        assert hasattr(tools, "sitemap")
        assert callable(tools.sitemap)

    def test_table_exists(self):
        from mcp_scraper_tools.scraper import tools
        assert hasattr(tools, "table")
        assert callable(tools.table)

    def test_headers_exists(self):
        from mcp_scraper_tools.scraper import tools
        assert hasattr(tools, "headers")
        assert callable(tools.headers)

    def test_status_exists(self):
        from mcp_scraper_tools.scraper import tools
        assert hasattr(tools, "status")
        assert callable(tools.status)


# TODO: add functional tests
