"""TraefikClient — HTTP client for traefik."""

from __future__ import annotations

import httpx


class TraefikClient:
    def __init__(self, config: dict) -> None:
        self.url = config["url"]
        self._client = httpx.Client()

    # TODO: implement API methods
