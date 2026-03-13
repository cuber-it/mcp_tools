"""ScraperClient — HTTP client for scraper."""

from __future__ import annotations

import httpx


class ScraperClient:
    def __init__(self, config: dict) -> None:
        self.config = config
        self._client = httpx.Client()

    # TODO: implement API methods
