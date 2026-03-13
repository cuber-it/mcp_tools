"""DockerClient — HTTP client for docker."""

from __future__ import annotations

import httpx


class DockerClient:
    def __init__(self, config: dict) -> None:
        self.base_url = config["base_url"]
        self._client = httpx.Client()

    # TODO: implement API methods
