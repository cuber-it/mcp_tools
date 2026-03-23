"""Navigation tools for Playwright."""
from __future__ import annotations

from ..client import BrowserClient


async def navigate(client: BrowserClient, url: str, wait_until: str = "domcontentloaded") -> str:
    page = await client.get_page()
    try:
        await page.goto(url, wait_until=wait_until)
        return f"Navigated to: {page.url}"
    except Exception as e:
        return f"Error: {e}"


async def current_url(client: BrowserClient) -> str:
    page = await client.get_page()
    return page.url


async def go_back(client: BrowserClient) -> str:
    page = await client.get_page()
    await page.go_back()
    return f"Back to: {page.url}"


async def go_forward(client: BrowserClient) -> str:
    page = await client.get_page()
    await page.go_forward()
    return f"Forward to: {page.url}"


async def reload(client: BrowserClient) -> str:
    page = await client.get_page()
    await page.reload()
    return f"Reloaded: {page.url}"
