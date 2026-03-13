"""WikipediaClient — HTTP client for wikipedia."""

from __future__ import annotations

import httpx


class WikipediaClient:
    def __init__(self, config: dict) -> None:
        self.config = config
        self._client = httpx.Client()

    # TODO: implement API methods
