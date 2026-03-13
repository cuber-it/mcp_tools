"""Pure tool logic for browser — no MCP dependency."""

from __future__ import annotations

def navigate(url: str, wait_until: str = "domcontentloaded") -> str:
    """Navigate to a URL and wait for page load"""
    # TODO: implement
    raise NotImplementedError("navigate")


def screenshot(selector: str = "", path: str = "") -> str:
    """Take a screenshot of the current page or element"""
    # TODO: implement
    raise NotImplementedError("screenshot")


def click(selector: str) -> str:
    """Click an element on the page"""
    # TODO: implement
    raise NotImplementedError("click")


def fill(selector: str, value: str) -> str:
    """Fill a form field with text"""
    # TODO: implement
    raise NotImplementedError("fill")


def select(selector: str, value: str) -> str:
    """Select an option from a dropdown"""
    # TODO: implement
    raise NotImplementedError("select")


def extract_text(selector: str = "body") -> str:
    """Extract text content from the page or element"""
    # TODO: implement
    raise NotImplementedError("extract_text")


def extract_links() -> str:
    """Extract all links from the page"""
    # TODO: implement
    raise NotImplementedError("extract_links")


def extract_table(selector: str = "table") -> str:
    """Extract table data as structured text"""
    # TODO: implement
    raise NotImplementedError("extract_table")


def pdf(path: str) -> str:
    """Render current page as PDF"""
    # TODO: implement
    raise NotImplementedError("pdf")


def evaluate(expression: str) -> str:
    """Execute JavaScript in the page context"""
    # TODO: implement
    raise NotImplementedError("evaluate")


def wait_for(selector: str, timeout: int = 30000) -> str:
    """Wait for an element or condition"""
    # TODO: implement
    raise NotImplementedError("wait_for")


def cookies() -> str:
    """Get all cookies for the current page"""
    # TODO: implement
    raise NotImplementedError("cookies")

