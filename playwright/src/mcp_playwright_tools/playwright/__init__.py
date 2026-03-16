"""Playwright — MCP plugin.

Playwright browser automation tools for MCP — navigation, interaction,
content extraction, and semantic locators.

Config keys (all optional):
    headless: bool (default True)
    timeout: int ms (default 30000)
    browser_type: str (default "chromium")
    slow_mo: int ms (default 0)
"""

from __future__ import annotations

from .client import BrowserClient
from . import tools


def register(mcp, config: dict) -> None:
    """Register playwright tools as MCP tools."""
    client = BrowserClient(config)

    # --- Navigation (5) ---

    @mcp.tool()
    async def navigate(url: str, wait_until: str = "domcontentloaded") -> str:
        """Navigate to a URL and wait for page load"""
        return await tools.navigate(client, url, wait_until)

    @mcp.tool()
    async def current_url() -> str:
        """Get the current page URL"""
        return await tools.current_url(client)

    @mcp.tool()
    async def go_back() -> str:
        """Navigate back in browser history"""
        return await tools.go_back(client)

    @mcp.tool()
    async def go_forward() -> str:
        """Navigate forward in browser history"""
        return await tools.go_forward(client)

    @mcp.tool()
    async def reload() -> str:
        """Reload the current page"""
        return await tools.reload(client)

    # --- Content (7) ---

    @mcp.tool()
    async def get_title() -> str:
        """Get the current page title"""
        return await tools.get_title(client)

    @mcp.tool()
    async def get_text(selector: str) -> str:
        """Get visible text of an element"""
        return await tools.get_text(client, selector)

    @mcp.tool()
    async def get_all_texts(selector: str) -> str:
        """Get visible text of all matching elements"""
        return await tools.get_all_texts(client, selector)

    @mcp.tool()
    async def get_page_content(max_length: int = 10000) -> str:
        """Get all visible text on the page"""
        return await tools.get_page_content(client, max_length)

    @mcp.tool()
    async def get_html(selector: str = "body") -> str:
        """Get inner HTML of an element"""
        return await tools.get_html(client, selector)

    @mcp.tool()
    async def get_links() -> str:
        """Get all links on the page (text + href)"""
        return await tools.get_links(client)

    @mcp.tool()
    async def get_attribute(selector: str, attribute: str) -> str:
        """Get an attribute value from an element"""
        return await tools.get_attribute(client, selector, attribute)

    # --- Interaction (11) ---

    @mcp.tool()
    async def click(selector: str) -> str:
        """Click an element"""
        return await tools.click(client, selector)

    @mcp.tool()
    async def fill(selector: str, text: str) -> str:
        """Fill an input field with text"""
        return await tools.fill(client, selector, text)

    @mcp.tool()
    async def type_text(selector: str, text: str, delay: int = 50) -> str:
        """Type text character by character (for autocomplete etc.)"""
        return await tools.type_text(client, selector, text, delay)

    @mcp.tool()
    async def press(key: str) -> str:
        """Press a keyboard key (Enter, Tab, Escape, etc.)"""
        return await tools.press(client, key)

    @mcp.tool()
    async def select_option(selector: str, value: str) -> str:
        """Select a dropdown option by value"""
        return await tools.select_option(client, selector, value)

    @mcp.tool()
    async def select_option_by_text(selector: str, text: str) -> str:
        """Select a dropdown option by visible text"""
        return await tools.select_option_by_text(client, selector, text)

    @mcp.tool()
    async def check(selector: str) -> str:
        """Check a checkbox"""
        return await tools.check(client, selector)

    @mcp.tool()
    async def uncheck(selector: str) -> str:
        """Uncheck a checkbox"""
        return await tools.uncheck(client, selector)

    @mcp.tool()
    async def hover(selector: str) -> str:
        """Hover over an element"""
        return await tools.hover(client, selector)

    @mcp.tool()
    async def focus(selector: str) -> str:
        """Focus an element"""
        return await tools.focus(client, selector)

    @mcp.tool()
    async def clear(selector: str) -> str:
        """Clear an input field"""
        return await tools.clear(client, selector)

    # --- Browser (8) ---

    @mcp.tool()
    async def screenshot(path: str = "screenshot.png", full_page: bool = False) -> str:
        """Take a screenshot of the page"""
        return await tools.screenshot(client, path, full_page)

    @mcp.tool()
    async def screenshot_element(selector: str, path: str = "element.png") -> str:
        """Take a screenshot of a specific element"""
        return await tools.screenshot_element(client, selector, path)

    @mcp.tool()
    async def wait_for(selector: str, timeout: int = 10000) -> str:
        """Wait for an element to appear"""
        return await tools.wait_for(client, selector, timeout)

    @mcp.tool()
    async def wait_for_hidden(selector: str, timeout: int = 10000) -> str:
        """Wait for an element to disappear"""
        return await tools.wait_for_hidden(client, selector, timeout)

    @mcp.tool()
    async def wait_for_url(url_pattern: str, timeout: int = 10000) -> str:
        """Wait for the URL to match a pattern"""
        return await tools.wait_for_url(client, url_pattern, timeout)

    @mcp.tool()
    async def set_viewport(width: int, height: int) -> str:
        """Set the browser viewport size"""
        return await tools.set_viewport(client, width, height)

    @mcp.tool()
    async def scroll_to(selector: str) -> str:
        """Scroll an element into view"""
        return await tools.scroll_to(client, selector)

    @mcp.tool()
    async def scroll_page(direction: str = "down", amount: int = 500) -> str:
        """Scroll the page up or down"""
        return await tools.scroll_page(client, direction, amount)

    # --- Browser Settings (2) ---

    @mcp.tool()
    async def set_headless(headless: bool) -> str:
        """Switch browser between headless and headed (visible) mode. Restarts browser."""
        return await tools.set_headless(client, headless)

    @mcp.tool()
    async def set_browser(browser_type: str) -> str:
        """Switch browser engine: chromium, firefox, or webkit. Restarts browser."""
        return await tools.set_browser(client, browser_type)

    # --- Semantic Locators (10) ---

    @mcp.tool()
    async def find_by_role(role: str, name: str = "") -> str:
        """Find element by ARIA role (button, link, textbox, heading, etc.)"""
        return await tools.find_by_role(client, role, name)

    @mcp.tool()
    async def find_by_text(text: str, exact: bool = False) -> str:
        """Find element by visible text"""
        return await tools.find_by_text(client, text, exact)

    @mcp.tool()
    async def find_by_label(label: str) -> str:
        """Find form element by its label text"""
        return await tools.find_by_label(client, label)

    @mcp.tool()
    async def find_by_placeholder(placeholder: str) -> str:
        """Find input element by placeholder text"""
        return await tools.find_by_placeholder(client, placeholder)

    @mcp.tool()
    async def find_by_test_id(test_id: str) -> str:
        """Find element by data-testid attribute"""
        return await tools.find_by_test_id(client, test_id)

    @mcp.tool()
    async def click_by_role(role: str, name: str = "") -> str:
        """Click element found by ARIA role"""
        return await tools.click_by_role(client, role, name)

    @mcp.tool()
    async def click_by_text(text: str) -> str:
        """Click element found by visible text"""
        return await tools.click_by_text(client, text)

    @mcp.tool()
    async def fill_by_label(label: str, value: str) -> str:
        """Fill input found by its label text"""
        return await tools.fill_by_label(client, label, value)

    @mcp.tool()
    async def describe_element(selector: str) -> str:
        """Get ARIA role, text, and attributes of an element"""
        return await tools.describe_element(client, selector)

    @mcp.tool()
    async def find_interactive_elements() -> str:
        """List all clickable and fillable elements on the page"""
        return await tools.find_interactive_elements(client)
