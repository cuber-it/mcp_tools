"""Playwright tool implementations — no MCP dependency.

All functions receive a BrowserClient as first argument.
Async because Playwright is async-native.

Later this will split into navigation.py, content.py, interaction.py,
browser.py, locators.py with tools.py becoming a re-export facade.
"""

from __future__ import annotations

from pathlib import Path

from .client import BrowserClient


# ---------------------------------------------------------------------------
# Navigation (5)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Content (7)
# ---------------------------------------------------------------------------

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
        return "\n".join(f"- {l['text']}: {l['href']}" for l in links)
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


# ---------------------------------------------------------------------------
# Interaction (11)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Browser (8)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Browser Settings (2)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Semantic Locators (10)
# ---------------------------------------------------------------------------

async def find_by_role(client: BrowserClient, role: str, name: str = "") -> str:
    page = await client.get_page()
    try:
        kwargs = {}
        if name:
            kwargs["name"] = name
        loc = page.get_by_role(role, **kwargs)
        count = await loc.count()
        if count == 0:
            return f"(no elements with role '{role}' found)"
        texts = []
        for i in range(min(count, 20)):
            text = await loc.nth(i).inner_text()
            texts.append(f"{i+1}. {text.strip()[:80]}")
        return f"Found {count} element(s) with role '{role}':\n" + "\n".join(texts)
    except Exception as e:
        return f"Error: {e}"


async def find_by_text(client: BrowserClient, text: str, exact: bool = False) -> str:
    page = await client.get_page()
    try:
        loc = page.get_by_text(text, exact=exact)
        count = await loc.count()
        if count == 0:
            return f"(no elements with text '{text}' found)"
        results = []
        for i in range(min(count, 10)):
            el = loc.nth(i)
            tag = await el.evaluate("e => e.tagName.toLowerCase()")
            inner = (await el.inner_text())[:80]
            results.append(f"{i+1}. <{tag}> {inner}")
        return f"Found {count} element(s):\n" + "\n".join(results)
    except Exception as e:
        return f"Error: {e}"


async def find_by_label(client: BrowserClient, label: str) -> str:
    page = await client.get_page()
    try:
        loc = page.get_by_label(label)
        count = await loc.count()
        if count == 0:
            return f"(no input with label '{label}' found)"
        tag = await loc.first.evaluate("e => e.tagName.toLowerCase() + '[type=' + (e.type||'') + ']'")
        return f"Found input with label '{label}': <{tag}>"
    except Exception as e:
        return f"Error: {e}"


async def find_by_placeholder(client: BrowserClient, placeholder: str) -> str:
    page = await client.get_page()
    try:
        loc = page.get_by_placeholder(placeholder)
        count = await loc.count()
        if count == 0:
            return f"(no input with placeholder '{placeholder}' found)"
        return f"Found {count} input(s) with placeholder '{placeholder}'"
    except Exception as e:
        return f"Error: {e}"


async def find_by_test_id(client: BrowserClient, test_id: str) -> str:
    page = await client.get_page()
    try:
        loc = page.get_by_test_id(test_id)
        count = await loc.count()
        if count == 0:
            return f"(no element with test-id '{test_id}' found)"
        tag = await loc.first.evaluate("e => e.tagName.toLowerCase()")
        text = (await loc.first.inner_text())[:80]
        return f"Found <{tag}> with test-id '{test_id}': {text}"
    except Exception as e:
        return f"Error: {e}"


async def click_by_role(client: BrowserClient, role: str, name: str = "") -> str:
    page = await client.get_page()
    try:
        kwargs = {}
        if name:
            kwargs["name"] = name
        await page.get_by_role(role, **kwargs).click()
        await page.wait_for_load_state("domcontentloaded")
        label = f"role={role}" + (f", name='{name}'" if name else "")
        return f"Clicked: {label}"
    except Exception as e:
        return f"Error: {e}"


async def click_by_text(client: BrowserClient, text: str) -> str:
    page = await client.get_page()
    try:
        await page.get_by_text(text).click()
        await page.wait_for_load_state("domcontentloaded")
        return f"Clicked text: '{text}'"
    except Exception as e:
        return f"Error: {e}"


async def fill_by_label(client: BrowserClient, label: str, value: str) -> str:
    page = await client.get_page()
    try:
        await page.get_by_label(label).fill(value)
        return f"Filled '{label}' with: {value}"
    except Exception as e:
        return f"Error: {e}"


async def describe_element(client: BrowserClient, selector: str) -> str:
    page = await client.get_page()
    try:
        loc = page.locator(selector)
        await loc.wait_for(timeout=5000)
        info = await loc.evaluate("""e => ({
            tag: e.tagName.toLowerCase(),
            role: e.getAttribute('role') || '',
            text: (e.innerText || '').substring(0, 100),
            id: e.id || '',
            classes: e.className || '',
            type: e.type || '',
            name: e.name || '',
            value: e.value || '',
            href: e.href || '',
            placeholder: e.placeholder || '',
            ariaLabel: e.getAttribute('aria-label') || '',
            testId: e.getAttribute('data-testid') || '',
            visible: e.offsetParent !== null,
            enabled: !e.disabled,
        })""")
        lines = [f"<{info['tag']}>"]
        for key in ['role', 'id', 'classes', 'type', 'name', 'text', 'value',
                     'href', 'placeholder', 'ariaLabel', 'testId']:
            if info.get(key):
                lines.append(f"  {key}: {info[key]}")
        lines.append(f"  visible: {info['visible']}, enabled: {info['enabled']}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


async def find_interactive_elements(client: BrowserClient) -> str:
    page = await client.get_page()
    try:
        elements = await page.evaluate("""() => {
            const sel = 'a, button, input, select, textarea, [role="button"], [role="link"], [onclick]';
            return Array.from(document.querySelectorAll(sel)).slice(0, 50).map(e => ({
                tag: e.tagName.toLowerCase(),
                type: e.type || '',
                text: (e.innerText || e.value || e.placeholder || e.getAttribute('aria-label') || '').substring(0, 60).trim(),
                id: e.id || '',
                name: e.name || '',
                role: e.getAttribute('role') || '',
                testId: e.getAttribute('data-testid') || '',
                href: e.tagName === 'A' ? e.href : '',
            }));
        }""")
        if not elements:
            return "(no interactive elements found)"
        lines = []
        for i, el in enumerate(elements):
            parts = [f"{i+1}. <{el['tag']}"]
            if el['type']:
                parts[0] += f" type={el['type']}"
            parts[0] += ">"
            if el['text']:
                parts.append(f'"{el["text"]}"')
            if el['id']:
                parts.append(f"id={el['id']}")
            if el['name']:
                parts.append(f"name={el['name']}")
            if el['testId']:
                parts.append(f"testid={el['testId']}")
            lines.append(" ".join(parts))
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"
