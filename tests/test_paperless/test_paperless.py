"""Tests for paperless tools."""

import pytest

from mcp_paperless_tools.paperless import register
from mcp_paperless_tools.paperless.client import PaperlessClient


class TestImport:
    def test_register_exists(self):
        assert callable(register)

    def test_client_class_exists(self):
        assert PaperlessClient is not None


class TestTools:
    def test_document_list_exists(self):
        from mcp_paperless_tools.paperless import tools
        assert hasattr(tools, "document_list")
        assert callable(tools.document_list)

    def test_document_search_exists(self):
        from mcp_paperless_tools.paperless import tools
        assert hasattr(tools, "document_search")
        assert callable(tools.document_search)

    def test_document_get_exists(self):
        from mcp_paperless_tools.paperless import tools
        assert hasattr(tools, "document_get")
        assert callable(tools.document_get)

    def test_document_upload_exists(self):
        from mcp_paperless_tools.paperless import tools
        assert hasattr(tools, "document_upload")
        assert callable(tools.document_upload)

    def test_document_download_exists(self):
        from mcp_paperless_tools.paperless import tools
        assert hasattr(tools, "document_download")
        assert callable(tools.document_download)

    def test_tag_list_exists(self):
        from mcp_paperless_tools.paperless import tools
        assert hasattr(tools, "tag_list")
        assert callable(tools.tag_list)

    def test_tag_assign_exists(self):
        from mcp_paperless_tools.paperless import tools
        assert hasattr(tools, "tag_assign")
        assert callable(tools.tag_assign)

    def test_tag_remove_exists(self):
        from mcp_paperless_tools.paperless import tools
        assert hasattr(tools, "tag_remove")
        assert callable(tools.tag_remove)

    def test_correspondent_list_exists(self):
        from mcp_paperless_tools.paperless import tools
        assert hasattr(tools, "correspondent_list")
        assert callable(tools.correspondent_list)

    def test_correspondent_assign_exists(self):
        from mcp_paperless_tools.paperless import tools
        assert hasattr(tools, "correspondent_assign")
        assert callable(tools.correspondent_assign)

    def test_doctype_list_exists(self):
        from mcp_paperless_tools.paperless import tools
        assert hasattr(tools, "doctype_list")
        assert callable(tools.doctype_list)

    def test_doctype_assign_exists(self):
        from mcp_paperless_tools.paperless import tools
        assert hasattr(tools, "doctype_assign")
        assert callable(tools.doctype_assign)


# TODO: add functional tests
