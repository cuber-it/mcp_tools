"""DatabaseClient — HTTP client for database."""

from __future__ import annotations

import httpx


class DatabaseClient:
    def __init__(self, config: dict) -> None:
        self.uri = config["uri"]
        self._client = httpx.Client()

    # TODO: implement API methods
