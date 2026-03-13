"""Tests for arxiv tools."""

import pytest

from mcp_arxiv_tools.arxiv import register
from mcp_arxiv_tools.arxiv.client import ArxivClient


class TestImport:
    def test_register_exists(self):
        assert callable(register)

    def test_client_class_exists(self):
        assert ArxivClient is not None


class TestTools:
    def test_search_exists(self):
        from mcp_arxiv_tools.arxiv import tools
        assert hasattr(tools, "search")
        assert callable(tools.search)

    def test_abstract_exists(self):
        from mcp_arxiv_tools.arxiv import tools
        assert hasattr(tools, "abstract")
        assert callable(tools.abstract)

    def test_paper_exists(self):
        from mcp_arxiv_tools.arxiv import tools
        assert hasattr(tools, "paper")
        assert callable(tools.paper)

    def test_download_exists(self):
        from mcp_arxiv_tools.arxiv import tools
        assert hasattr(tools, "download")
        assert callable(tools.download)

    def test_authors_exists(self):
        from mcp_arxiv_tools.arxiv import tools
        assert hasattr(tools, "authors")
        assert callable(tools.authors)

    def test_recent_exists(self):
        from mcp_arxiv_tools.arxiv import tools
        assert hasattr(tools, "recent")
        assert callable(tools.recent)


# TODO: add functional tests
