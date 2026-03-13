"""EmailClient — HTTP client for email."""

from __future__ import annotations

import httpx


class EmailClient:
    def __init__(self, config: dict) -> None:
        self.imap_host = config["imap_host"]
        self.smtp_host = config["smtp_host"]
        self.username = config["username"]
        self.password = config["password"]
        self._client = httpx.Client()

    # TODO: implement API methods
