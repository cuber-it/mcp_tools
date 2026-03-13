"""Tests for browser tools."""

import pytest

from mcp_browser_tools.browser import register


class TestImport:
    def test_register_exists(self):
        assert callable(register)


class TestTools:
    def test_navigate_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "navigate")
        assert callable(tools.navigate)

    def test_screenshot_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "screenshot")
        assert callable(tools.screenshot)

    def test_click_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "click")
        assert callable(tools.click)

    def test_fill_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "fill")
        assert callable(tools.fill)

    def test_select_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "select")
        assert callable(tools.select)

    def test_extract_text_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "extract_text")
        assert callable(tools.extract_text)

    def test_extract_links_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "extract_links")
        assert callable(tools.extract_links)

    def test_extract_table_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "extract_table")
        assert callable(tools.extract_table)

    def test_pdf_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "pdf")
        assert callable(tools.pdf)

    def test_evaluate_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "evaluate")
        assert callable(tools.evaluate)

    def test_wait_for_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "wait_for")
        assert callable(tools.wait_for)

    def test_cookies_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "cookies")
        assert callable(tools.cookies)


# TODO: add functional tests
