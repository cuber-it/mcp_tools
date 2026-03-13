"""HomeAssistantClient — HTTP client for homeassistant."""

from __future__ import annotations

import httpx


class HomeAssistantClient:
    def __init__(self, config: dict) -> None:
        self.url = config["url"]
        self.token = config["token"]
        self._client = httpx.Client()

    # TODO: implement API methods
