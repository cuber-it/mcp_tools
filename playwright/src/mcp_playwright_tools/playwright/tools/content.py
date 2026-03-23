"""Content extraction tools for Playwright."""
from __future__ import annotations

from ..client import BrowserClient


async def get_title(client: BrowserClient) -> str:
    page = await client.get_page()
    return await page.title()


async def get_text(client: BrowserClient, selector: str) -> str:
    page = await client.get_page()
    try:
        loc = page.locator(selector)
        await loc.wait_for(timeout=5000)
        return await loc.inner_text()
    except Exception as e:
        return f"Error: {e}"


async def get_all_texts(client: BrowserClient, selector: str) -> str:
    page = await client.get_page()
    try:
        loc = page.locator(selector)
        count = await loc.count()
        if count == 0:
            return "(no elements found)"
        texts = []
        for i in range(count):
            text = await loc.nth(i).inner_text()
            texts.append(f"{i+1}. {text.strip()}")
        return "\n".join(texts)
    except Exception as e:
        return f"Error: {e}"


async def get_page_content(client: BrowserClient, max_length: int = 10000) -> str:
    page = await client.get_page()
    try:
        text = await page.inner_text("body")
        text = "\n".join(line.strip() for line in text.split("\n") if line.strip())
        if len(text) > max_length:
            text = text[:max_length] + "\n... (truncated)"
        return text
    except Exception as e:
        return f"Error: {e}"


async def get_html(client: BrowserClient, selector: str = "body") -> str:
    page = await client.get_page()
    try:
        return await page.locator(selector).inner_html()
    except Exception as e:
        return f"Error: {e}"


async def get_links(client: BrowserClient) -> str:
    page = await client.get_page()
    try:
        links = await page.eval_on_selector_all(
            "a[href]",
            """els => els.map(e => ({
                text: e.innerText.trim().substring(0, 80),
                href: e.href
            })).filter(l => l.text && l.href).slice(0, 50)"""
        )
        if not links:
            return "(no links found)"
        return "\n".join(f"- {lnk['text']}: {lnk['href']}" for lnk in links)
    except Exception as e:
        return f"Error: {e}"


async def get_attribute(client: BrowserClient, selector: str, attribute: str) -> str:
    page = await client.get_page()
    try:
        loc = page.locator(selector)
        await loc.wait_for(timeout=5000)
        value = await loc.get_attribute(attribute)
        return value if value is not None else "(attribute not found)"
    except Exception as e:
        return f"Error: {e}"
