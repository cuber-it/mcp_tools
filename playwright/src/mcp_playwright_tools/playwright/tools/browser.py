"""Browser and viewport tools for Playwright."""
from __future__ import annotations

from pathlib import Path

from ..client import BrowserClient


async def screenshot(client: BrowserClient, path: str = "", full_page: bool = False) -> str:
    page = await client.get_page()
    try:
        if path:
            filepath = Path(path).resolve()
            filepath.parent.mkdir(parents=True, exist_ok=True)
            await page.screenshot(path=str(filepath), full_page=full_page)
            return f"Screenshot saved: {filepath}"
        else:
            import base64
            buf = await page.screenshot(full_page=full_page)
            return base64.b64encode(buf).decode()
    except Exception as e:
        return f"Error: {e}"


async def screenshot_element(client: BrowserClient, selector: str, path: str = "element.png") -> str:
    page = await client.get_page()
    try:
        filepath = Path(path).resolve()
        filepath.parent.mkdir(parents=True, exist_ok=True)
        await page.locator(selector).screenshot(path=str(filepath))
        return f"Element screenshot saved: {filepath}"
    except Exception as e:
        return f"Error: {e}"


async def wait_for(client: BrowserClient, selector: str, timeout: int = 10000) -> str:
    page = await client.get_page()
    try:
        await page.wait_for_selector(selector, timeout=timeout)
        return f"Found: {selector}"
    except Exception as e:
        return f"Error (timeout?): {e}"


async def wait_for_hidden(client: BrowserClient, selector: str, timeout: int = 10000) -> str:
    page = await client.get_page()
    try:
        await page.wait_for_selector(selector, state="hidden", timeout=timeout)
        return f"Hidden: {selector}"
    except Exception as e:
        return f"Error (timeout?): {e}"


async def wait_for_url(client: BrowserClient, url_pattern: str, timeout: int = 10000) -> str:
    page = await client.get_page()
    try:
        await page.wait_for_url(url_pattern, timeout=timeout)
        return f"URL reached: {page.url}"
    except Exception as e:
        return f"Error (timeout?): {e}"


async def set_viewport(client: BrowserClient, width: int, height: int) -> str:
    page = await client.get_page()
    try:
        await page.set_viewport_size({"width": width, "height": height})
        return f"Viewport: {width}x{height}"
    except Exception as e:
        return f"Error: {e}"


async def scroll_to(client: BrowserClient, selector: str) -> str:
    page = await client.get_page()
    try:
        await page.locator(selector).scroll_into_view_if_needed()
        return f"Scrolled to: {selector}"
    except Exception as e:
        return f"Error: {e}"


async def scroll_page(client: BrowserClient, direction: str = "down", amount: int = 500) -> str:
    page = await client.get_page()
    try:
        if direction == "top":
            await page.evaluate("window.scrollTo(0, 0)")
        elif direction == "bottom":
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        elif direction == "up":
            await page.evaluate(f"window.scrollBy(0, -{amount})")
        else:
            await page.evaluate(f"window.scrollBy(0, {amount})")
        return f"Scrolled: {direction}"
    except Exception as e:
        return f"Error: {e}"


async def set_headless(client: BrowserClient, headless: bool) -> str:
    try:
        await client.relaunch(headless=headless)
        mode = "headless" if headless else "headed (visible)"
        return f"Browser restarted in {mode} mode. Navigate to a page to continue."
    except Exception as e:
        return f"Error: {e}"


async def set_browser(client: BrowserClient, browser_type: str) -> str:
    try:
        await client.relaunch(browser_type=browser_type)
        return f"Browser switched to {browser_type}. Navigate to a page to continue."
    except Exception as e:
        return f"Error: {e}"
