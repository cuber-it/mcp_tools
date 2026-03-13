"""PrometheusClient — HTTP client for prometheus."""

from __future__ import annotations

import httpx


class PrometheusClient:
    def __init__(self, config: dict) -> None:
        self.url = config["url"]
        self._client = httpx.Client()

    # TODO: implement API methods
