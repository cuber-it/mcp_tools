"""BrowserClient — Playwright browser lifecycle management.

Manages a single Playwright browser instance with lazy initialization.
No singleton — instantiated per config in register().
"""

from __future__ import annotations

from playwright.async_api import (
    async_playwright,
    Browser,
    BrowserContext,
    Page,
    Playwright,
)


class BrowserClient:
    """Manages Playwright browser lifecycle.

    Config keys:
        headless: bool (default True)
        timeout: int in ms (default 30000)
        browser_type: str (default "chromium")
        slow_mo: int in ms (default 0)
    """

    def __init__(self, config: dict) -> None:
        self._headless: bool = config.get("headless", True)
        self._timeout: int = config.get("timeout", 30000)
        self._browser_type: str = config.get("browser_type", "chromium")
        self._slow_mo: int = config.get("slow_mo", 0)

        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None

    async def get_page(self) -> Page:
        """Return the current page, launching browser if needed."""
        if self._page is None or self._page.is_closed():
            if self._playwright is None:
                self._playwright = await async_playwright().start()
            if self._browser is None:
                launcher = getattr(self._playwright, self._browser_type)
                self._browser = await launcher.launch(
                    headless=self._headless,
                    slow_mo=self._slow_mo,
                )
            if self._context is None:
                self._context = await self._browser.new_context()
            self._page = await self._context.new_page()
            self._page.set_default_timeout(self._timeout)
        return self._page

    async def new_context(self, storage_state: str | None = None) -> BrowserContext:
        """Create a new isolated browser context."""
        if self._browser is None:
            await self.get_page()
        kwargs = {}
        if storage_state:
            kwargs["storage_state"] = storage_state
        ctx = await self._browser.new_context(**kwargs)
        return ctx

    async def new_page(self) -> Page:
        """Open a new page in the current context."""
        if self._context is None:
            await self.get_page()
        self._page = await self._context.new_page()
        self._page.set_default_timeout(self._timeout)
        return self._page

    async def close_page(self) -> bool:
        """Close the current page."""
        if self._page and not self._page.is_closed():
            await self._page.close()
            self._page = None
            return True
        return False

    @property
    def headless(self) -> bool:
        return self._headless

    @property
    def browser_type(self) -> str:
        return self._browser_type

    @property
    def timeout(self) -> int:
        return self._timeout

    async def relaunch(self, headless: bool | None = None, browser_type: str | None = None) -> None:
        """Restart browser with new settings. Closes all pages."""
        if headless is not None:
            self._headless = headless
        if browser_type is not None:
            if browser_type not in ("chromium", "firefox", "webkit"):
                raise ValueError(f"Unknown browser: {browser_type}. Use chromium, firefox, or webkit.")
            self._browser_type = browser_type
        await self.cleanup()
        # Lazy — next get_page() will launch with new settings

    async def cleanup(self) -> None:
        """Clean up all Playwright resources."""
        if self._page and not self._page.is_closed():
            await self._page.close()
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
        self._page = None
        self._context = None
        self._browser = None
        self._playwright = None
