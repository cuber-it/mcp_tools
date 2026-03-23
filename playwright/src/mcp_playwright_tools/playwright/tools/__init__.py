"""Playwright tool implementations."""
from .navigation import navigate, current_url, go_back, go_forward, reload
from .content import (
    get_title, get_text, get_all_texts, get_page_content,
    get_html, get_links, get_attribute,
)
from .interaction import (
    click, fill, type_text, press, select_option, select_option_by_text,
    check, uncheck, hover, focus, clear,
)
from .browser import (
    screenshot, screenshot_element, wait_for, wait_for_hidden, wait_for_url,
    set_viewport, scroll_to, scroll_page, set_browser, set_headless,
)
from .locators import (
    find_by_role, find_by_text, find_by_label, find_by_placeholder,
    find_by_test_id, click_by_role, click_by_text, fill_by_label,
    describe_element, find_interactive_elements,
)

__all__ = [
    # Navigation
    "navigate", "current_url", "go_back", "go_forward", "reload",
    # Content
    "get_title", "get_text", "get_all_texts", "get_page_content",
    "get_html", "get_links", "get_attribute",
    # Interaction
    "click", "fill", "type_text", "press", "select_option",
    "select_option_by_text", "check", "uncheck", "hover", "focus", "clear",
    # Browser
    "screenshot", "screenshot_element", "wait_for", "wait_for_hidden",
    "wait_for_url", "set_viewport", "scroll_to", "scroll_page",
    "set_browser", "set_headless",
    # Locators
    "find_by_role", "find_by_text", "find_by_label", "find_by_placeholder",
    "find_by_test_id", "click_by_role", "click_by_text", "fill_by_label",
    "describe_element", "find_interactive_elements",
]
