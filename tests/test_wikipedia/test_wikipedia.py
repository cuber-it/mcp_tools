"""Tests for wikipedia tools."""

import pytest

from mcp_wikipedia_tools.wikipedia import register
from mcp_wikipedia_tools.wikipedia.client import WikipediaClient


class TestImport:
    def test_register_exists(self):
        assert callable(register)

    def test_client_class_exists(self):
        assert WikipediaClient is not None


class TestTools:
    def test_search_exists(self):
        from mcp_wikipedia_tools.wikipedia import tools
        assert hasattr(tools, "search")
        assert callable(tools.search)

    def test_article_exists(self):
        from mcp_wikipedia_tools.wikipedia import tools
        assert hasattr(tools, "article")
        assert callable(tools.article)

    def test_summary_exists(self):
        from mcp_wikipedia_tools.wikipedia import tools
        assert hasattr(tools, "summary")
        assert callable(tools.summary)

    def test_links_exists(self):
        from mcp_wikipedia_tools.wikipedia import tools
        assert hasattr(tools, "links")
        assert callable(tools.links)

    def test_categories_exists(self):
        from mcp_wikipedia_tools.wikipedia import tools
        assert hasattr(tools, "categories")
        assert callable(tools.categories)

    def test_random_exists(self):
        from mcp_wikipedia_tools.wikipedia import tools
        assert hasattr(tools, "random")
        assert callable(tools.random)


# TODO: add functional tests
