"""MqttClient — HTTP client for mqtt."""

from __future__ import annotations

import httpx


class MqttClient:
    def __init__(self, config: dict) -> None:
        self.host = config["host"]
        self.port = config["port"]
        self._client = httpx.Client()

    # TODO: implement API methods
