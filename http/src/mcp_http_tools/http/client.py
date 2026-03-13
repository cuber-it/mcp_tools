"""HttpClient — HTTP client for http."""

from __future__ import annotations

import httpx


class HttpClient:
    def __init__(self, config: dict) -> None:
        self.config = config
        self._client = httpx.Client()

    # TODO: implement API methods
