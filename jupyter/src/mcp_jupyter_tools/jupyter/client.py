"""JupyterClient — HTTP client for jupyter."""

from __future__ import annotations

import httpx


class JupyterClient:
    def __init__(self, config: dict) -> None:
        self.url = config["url"]
        self.token = config["token"]
        self._client = httpx.Client()

    # TODO: implement API methods
