"""Tests for wikipedia tools — against live API."""

import json
import pytest

from mcp_wikipedia_tools.wikipedia import register
from mcp_wikipedia_tools.wikipedia.client import WikipediaClient
from mcp_wikipedia_tools.wikipedia import tools


class TestImport:
    def test_register_exists(self):
        assert callable(register)

    def test_client_class_exists(self):
        assert WikipediaClient is not None


class TestClient:
    @pytest.fixture
    def client(self):
        return WikipediaClient({})

    def test_opensearch(self, client):
        data = client.opensearch("en", "Python programming", limit=3)
        assert isinstance(data, list)
        assert len(data) == 4  # [query, titles, descriptions, urls]
        assert len(data[1]) > 0

    def test_rest_summary(self, client):
        data = client.rest("en", "page/summary/Python_(programming_language)")
        assert "title" in data
        assert "extract" in data

    def test_query_extracts(self, client):
        data = client.query("en", titles="Python_(programming_language)", prop="extracts", explaintext=True)
        page = client._first_page(data)
        assert "extract" in page
        assert len(page["extract"]) > 100

    def test_query_missing_page(self, client):
        data = client.query("en", titles="Xyzzy_nonexistent_page_12345", prop="extracts", explaintext=True)
        page = client._first_page(data)
        assert "missing" in page


class TestTools:
    @pytest.fixture
    def client(self):
        return WikipediaClient({})

    def test_search(self, client):
        result = json.loads(tools.search(client, "Python programming", limit=3))
        assert "results" in result
        assert len(result["results"]) > 0
        assert "title" in result["results"][0]
        assert "url" in result["results"][0]

    def test_search_german(self, client):
        result = json.loads(tools.search(client, "Python Programmiersprache", lang="de", limit=3))
        assert "results" in result
        assert result["lang"] == "de"

    def test_article(self, client):
        text = tools.article(client, "Python_(programming_language)")
        assert "programming language" in text.lower()
        assert len(text) > 1000

    def test_article_not_found(self, client):
        result = json.loads(tools.article(client, "Xyzzy_nonexistent_page_12345"))
        assert "error" in result

    def test_summary(self, client):
        result = json.loads(tools.summary(client, "Python_(programming_language)"))
        assert result["title"] == "Python (programming language)"
        assert len(result["extract"]) > 50
        assert "url" in result

    def test_links(self, client):
        result = json.loads(tools.links(client, "Python_(programming_language)"))
        assert result["count"] > 10
        assert len(result["links"]) == result["count"]

    def test_links_not_found(self, client):
        result = json.loads(tools.links(client, "Xyzzy_nonexistent_page_12345"))
        assert "error" in result

    def test_categories(self, client):
        result = json.loads(tools.categories(client, "Python_(programming_language)"))
        assert len(result["categories"]) > 0
        for cat in result["categories"]:
            assert not cat.startswith("Category:")

    def test_random(self, client):
        result = json.loads(tools.random(client))
        assert "title" in result
        assert len(result["extract"]) > 0
        assert "url" in result
