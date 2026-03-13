"""Browser — MCP plugin.

Browser automation tools for MCP — navigate, extract, screenshot, interact
"""

from __future__ import annotations

from . import tools


def register(mcp, config: dict) -> None:
    """Register browser tools as MCP tools."""
    @mcp.tool()
    def navigate(url: str, wait_until: str = "domcontentloaded") -> str:
        """Navigate to a URL and wait for page load"""
        return tools.navigate(url, wait_until)

    @mcp.tool()
    def screenshot(selector: str = "", path: str = "") -> str:
        """Take a screenshot of the current page or element"""
        return tools.screenshot(selector, path)

    @mcp.tool()
    def click(selector: str) -> str:
        """Click an element on the page"""
        return tools.click(selector)

    @mcp.tool()
    def fill(selector: str, value: str) -> str:
        """Fill a form field with text"""
        return tools.fill(selector, value)

    @mcp.tool()
    def select(selector: str, value: str) -> str:
        """Select an option from a dropdown"""
        return tools.select(selector, value)

    @mcp.tool()
    def extract_text(selector: str = "body") -> str:
        """Extract text content from the page or element"""
        return tools.extract_text(selector)

    @mcp.tool()
    def extract_links() -> str:
        """Extract all links from the page"""
        return tools.extract_links()

    @mcp.tool()
    def extract_table(selector: str = "table") -> str:
        """Extract table data as structured text"""
        return tools.extract_table(selector)

    @mcp.tool()
    def pdf(path: str) -> str:
        """Render current page as PDF"""
        return tools.pdf(path)

    @mcp.tool()
    def evaluate(expression: str) -> str:
        """Execute JavaScript in the page context"""
        return tools.evaluate(expression)

    @mcp.tool()
    def wait_for(selector: str, timeout: int = 30000) -> str:
        """Wait for an element or condition"""
        return tools.wait_for(selector, timeout)

    @mcp.tool()
    def cookies() -> str:
        """Get all cookies for the current page"""
        return tools.cookies()
