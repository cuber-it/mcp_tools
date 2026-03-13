"""Tests for http tools."""

import pytest

from mcp_http_tools.http import register
from mcp_http_tools.http.client import HttpClient


class TestImport:
    def test_register_exists(self):
        assert callable(register)

    def test_client_class_exists(self):
        assert HttpClient is not None


class TestTools:
    def test_http_request_exists(self):
        from mcp_http_tools.http import tools
        assert hasattr(tools, "http_request")
        assert callable(tools.http_request)

    def test_http_json_exists(self):
        from mcp_http_tools.http import tools
        assert hasattr(tools, "http_json")
        assert callable(tools.http_json)

    def test_http_download_exists(self):
        from mcp_http_tools.http import tools
        assert hasattr(tools, "http_download")
        assert callable(tools.http_download)

    def test_http_head_exists(self):
        from mcp_http_tools.http import tools
        assert hasattr(tools, "http_head")
        assert callable(tools.http_head)

    def test_http_status_exists(self):
        from mcp_http_tools.http import tools
        assert hasattr(tools, "http_status")
        assert callable(tools.http_status)

    def test_http_form_post_exists(self):
        from mcp_http_tools.http import tools
        assert hasattr(tools, "http_form_post")
        assert callable(tools.http_form_post)

    def test_json_query_exists(self):
        from mcp_http_tools.http import tools
        assert hasattr(tools, "json_query")
        assert callable(tools.json_query)


# TODO: add functional tests
