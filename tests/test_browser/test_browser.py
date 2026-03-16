"""Tests for browser tools."""

import pytest

from mcp_browser_tools.browser import register
from mcp_browser_tools.browser.client import BrowserClient


class TestImport:
    def test_register_exists(self):
        assert callable(register)

    def test_client_class_exists(self):
        assert BrowserClient is not None


class TestTools:
    def test_navigate_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "navigate")
        assert callable(tools.navigate)

    def test_current_url_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "current_url")
        assert callable(tools.current_url)

    def test_go_back_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "go_back")
        assert callable(tools.go_back)

    def test_go_forward_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "go_forward")
        assert callable(tools.go_forward)

    def test_reload_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "reload")
        assert callable(tools.reload)

    def test_get_title_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "get_title")
        assert callable(tools.get_title)

    def test_get_text_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "get_text")
        assert callable(tools.get_text)

    def test_get_all_texts_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "get_all_texts")
        assert callable(tools.get_all_texts)

    def test_get_page_content_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "get_page_content")
        assert callable(tools.get_page_content)

    def test_get_html_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "get_html")
        assert callable(tools.get_html)

    def test_get_links_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "get_links")
        assert callable(tools.get_links)

    def test_get_attribute_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "get_attribute")
        assert callable(tools.get_attribute)

    def test_click_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "click")
        assert callable(tools.click)

    def test_fill_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "fill")
        assert callable(tools.fill)

    def test_type_text_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "type_text")
        assert callable(tools.type_text)

    def test_press_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "press")
        assert callable(tools.press)

    def test_select_option_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "select_option")
        assert callable(tools.select_option)

    def test_select_option_by_text_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "select_option_by_text")
        assert callable(tools.select_option_by_text)

    def test_check_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "check")
        assert callable(tools.check)

    def test_uncheck_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "uncheck")
        assert callable(tools.uncheck)

    def test_hover_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "hover")
        assert callable(tools.hover)

    def test_focus_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "focus")
        assert callable(tools.focus)

    def test_clear_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "clear")
        assert callable(tools.clear)

    def test_screenshot_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "screenshot")
        assert callable(tools.screenshot)

    def test_screenshot_element_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "screenshot_element")
        assert callable(tools.screenshot_element)

    def test_wait_for_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "wait_for")
        assert callable(tools.wait_for)

    def test_wait_for_hidden_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "wait_for_hidden")
        assert callable(tools.wait_for_hidden)

    def test_wait_for_url_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "wait_for_url")
        assert callable(tools.wait_for_url)

    def test_set_viewport_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "set_viewport")
        assert callable(tools.set_viewport)

    def test_scroll_to_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "scroll_to")
        assert callable(tools.scroll_to)

    def test_scroll_page_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "scroll_page")
        assert callable(tools.scroll_page)

    def test_find_by_role_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "find_by_role")
        assert callable(tools.find_by_role)

    def test_find_by_text_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "find_by_text")
        assert callable(tools.find_by_text)

    def test_find_by_label_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "find_by_label")
        assert callable(tools.find_by_label)

    def test_find_by_placeholder_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "find_by_placeholder")
        assert callable(tools.find_by_placeholder)

    def test_find_by_test_id_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "find_by_test_id")
        assert callable(tools.find_by_test_id)

    def test_click_by_role_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "click_by_role")
        assert callable(tools.click_by_role)

    def test_click_by_text_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "click_by_text")
        assert callable(tools.click_by_text)

    def test_fill_by_label_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "fill_by_label")
        assert callable(tools.fill_by_label)

    def test_describe_element_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "describe_element")
        assert callable(tools.describe_element)

    def test_find_interactive_elements_exists(self):
        from mcp_browser_tools.browser import tools
        assert hasattr(tools, "find_interactive_elements")
        assert callable(tools.find_interactive_elements)


# TODO: add functional tests
