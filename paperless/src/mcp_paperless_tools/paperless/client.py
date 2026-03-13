"""PaperlessClient — HTTP client for paperless."""

from __future__ import annotations

import httpx


class PaperlessClient:
    def __init__(self, config: dict) -> None:
        self.url = config["url"]
        self.token = config["token"]
        self._client = httpx.Client()

    # TODO: implement API methods
