"""Tests for email tools."""

import pytest

from mcp_email_tools.email import register
from mcp_email_tools.email.client import EmailClient


class TestImport:
    def test_register_exists(self):
        assert callable(register)

    def test_client_class_exists(self):
        assert EmailClient is not None


class TestTools:
    def test_inbox_exists(self):
        from mcp_email_tools.email import tools
        assert hasattr(tools, "inbox")
        assert callable(tools.inbox)

    def test_search_exists(self):
        from mcp_email_tools.email import tools
        assert hasattr(tools, "search")
        assert callable(tools.search)

    def test_read_exists(self):
        from mcp_email_tools.email import tools
        assert hasattr(tools, "read")
        assert callable(tools.read)

    def test_folders_exists(self):
        from mcp_email_tools.email import tools
        assert hasattr(tools, "folders")
        assert callable(tools.folders)

    def test_move_exists(self):
        from mcp_email_tools.email import tools
        assert hasattr(tools, "move")
        assert callable(tools.move)

    def test_mark_exists(self):
        from mcp_email_tools.email import tools
        assert hasattr(tools, "mark")
        assert callable(tools.mark)

    def test_send_exists(self):
        from mcp_email_tools.email import tools
        assert hasattr(tools, "send")
        assert callable(tools.send)

    def test_send_html_exists(self):
        from mcp_email_tools.email import tools
        assert hasattr(tools, "send_html")
        assert callable(tools.send_html)

    def test_reply_exists(self):
        from mcp_email_tools.email import tools
        assert hasattr(tools, "reply")
        assert callable(tools.reply)


# TODO: add functional tests
