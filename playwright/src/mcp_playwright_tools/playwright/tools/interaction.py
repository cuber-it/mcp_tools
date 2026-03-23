"""Interaction tools for Playwright."""
from __future__ import annotations

from ..client import BrowserClient


async def click(client: BrowserClient, selector: str) -> str:
    page = await client.get_page()
    try:
        await page.click(selector, timeout=5000)
        await page.wait_for_load_state("domcontentloaded")
        return f"Clicked: {selector}"
    except Exception as e:
        return f"Error: {e}"


async def fill(client: BrowserClient, selector: str, text: str) -> str:
    page = await client.get_page()
    try:
        await page.fill(selector, text, timeout=5000)
        return f"Filled: {selector}"
    except Exception as e:
        return f"Error: {e}"


async def type_text(client: BrowserClient, selector: str, text: str, delay: int = 50) -> str:
    page = await client.get_page()
    try:
        await page.type(selector, text, delay=delay)
        return f"Typed into: {selector}"
    except Exception as e:
        return f"Error: {e}"


async def press(client: BrowserClient, key: str) -> str:
    page = await client.get_page()
    try:
        await page.keyboard.press(key)
        return f"Pressed: {key}"
    except Exception as e:
        return f"Error: {e}"


async def select_option(client: BrowserClient, selector: str, value: str) -> str:
    page = await client.get_page()
    try:
        await page.select_option(selector, value, timeout=5000)
        return f"Selected: {value} in {selector}"
    except Exception as e:
        return f"Error: {e}"


async def select_option_by_text(client: BrowserClient, selector: str, text: str) -> str:
    page = await client.get_page()
    try:
        await page.select_option(selector, label=text, timeout=5000)
        return f"Selected: '{text}' in {selector}"
    except Exception as e:
        return f"Error: {e}"


async def check(client: BrowserClient, selector: str) -> str:
    page = await client.get_page()
    try:
        await page.check(selector, timeout=5000)
        return f"Checked: {selector}"
    except Exception as e:
        return f"Error: {e}"


async def uncheck(client: BrowserClient, selector: str) -> str:
    page = await client.get_page()
    try:
        await page.uncheck(selector, timeout=5000)
        return f"Unchecked: {selector}"
    except Exception as e:
        return f"Error: {e}"


async def hover(client: BrowserClient, selector: str) -> str:
    page = await client.get_page()
    try:
        await page.hover(selector, timeout=5000)
        return f"Hovered: {selector}"
    except Exception as e:
        return f"Error: {e}"


async def focus(client: BrowserClient, selector: str) -> str:
    page = await client.get_page()
    try:
        await page.focus(selector, timeout=5000)
        return f"Focused: {selector}"
    except Exception as e:
        return f"Error: {e}"


async def clear(client: BrowserClient, selector: str) -> str:
    page = await client.get_page()
    try:
        await page.fill(selector, "", timeout=5000)
        return f"Cleared: {selector}"
    except Exception as e:
        return f"Error: {e}"
