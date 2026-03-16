"""HomeMatic JSON-RPC client for CCU3/OpenCCU.

Handles session-based authentication with automatic login and renewal.
All API calls go through the central `call()` method which manages
session lifecycle transparently.

Protocol: JSON-RPC 1.1 via HTTP POST to /api/homematic.cgi
Auth: Session.login returns a session ID, passed as _session_id_ parameter.
Sessions expire after ~30 minutes without renewal.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class CCUError(Exception):
    """Error returned by the CCU JSON-RPC API."""

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"CCU error {code}: {message}")


class CCUClient:
    """HomeMatic CCU JSON-RPC client.

    Args:
        url: Base URL of the CCU (e.g. http://192.168.178.53)
        username: Login username
        password: Login password
        timeout: HTTP request timeout in seconds
    """

    ENDPOINT = "/api/homematic.cgi"

    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        timeout: float = 15.0,
    ):
        self.base_url = url.rstrip("/")
        self._username = username
        self._password = password
        self._client = httpx.Client(timeout=timeout)
        self._session_id: str | None = None
        self._request_id = 0

    # --- Session management ---

    def _login(self) -> str:
        """Authenticate and return a new session ID."""
        data = self._raw_call(
            "Session.login",
            {"username": self._username, "password": self._password},
            authenticated=False,
        )
        if not data:
            raise CCUError(0, "Session.login returned empty result")
        self._session_id = data
        logger.debug("CCU session established")
        return data

    def _ensure_session(self) -> str:
        """Return a valid session ID, logging in if necessary."""
        if self._session_id is None:
            self._login()
        return self._session_id  # type: ignore[return-value]

    def renew(self) -> None:
        """Explicitly renew the current session."""
        if self._session_id:
            try:
                self._raw_call("Session.renew", {"_session_id_": self._session_id}, authenticated=False)
                logger.debug("CCU session renewed")
            except CCUError:
                self._session_id = None
                self._login()

    def logout(self) -> None:
        """End the current session."""
        if self._session_id:
            try:
                self._raw_call(
                    "Session.logout",
                    {"_session_id_": self._session_id},
                    authenticated=False,
                )
            except Exception:
                pass
            self._session_id = None

    def close(self) -> None:
        """Logout and close the HTTP client."""
        self.logout()
        self._client.close()

    # --- Core RPC ---

    def call(self, method: str, params: dict[str, Any] | None = None) -> Any:
        """Call a CCU JSON-RPC method with automatic session handling.

        If the call fails with a session error, re-authenticates once and retries.

        Args:
            method: JSON-RPC method name (e.g. "Device.listAllDetail")
            params: Method parameters (session ID is added automatically)

        Returns:
            The "result" field from the JSON-RPC response.

        Raises:
            CCUError: If the API returns an error after retry.
        """
        params = dict(params) if params else {}
        params["_session_id_"] = self._ensure_session()

        try:
            return self._raw_call(method, params)
        except CCUError as e:
            if e.code in (401, 400, -1):
                # Session expired — re-login and retry once
                logger.debug("Session expired (code %d), re-authenticating", e.code)
                self._session_id = None
                params["_session_id_"] = self._ensure_session()
                return self._raw_call(method, params)
            raise

    def _raw_call(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        *,
        authenticated: bool = True,
    ) -> Any:
        """Execute a raw JSON-RPC call.

        Args:
            method: JSON-RPC method name
            params: Parameters dict
            authenticated: If True and call fails, may trigger re-auth in caller

        Returns:
            The "result" field from the response.

        Raises:
            CCUError: If the response contains an error.
            httpx.HTTPError: On transport errors.
        """
        self._request_id += 1
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": self._request_id,
        }

        resp = self._client.post(
            f"{self.base_url}{self.ENDPOINT}",
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()

        error = data.get("error")
        if error:
            raise CCUError(error.get("code", -1), error.get("message", str(error)))

        return data.get("result")

    # --- Convenience helpers for typed calls ---

    def call_interface(
        self,
        method: str,
        interface: str,
        address: str = "",
        **kwargs: Any,
    ) -> Any:
        """Shorthand for Interface.* methods that require interface + address."""
        params: dict[str, Any] = {"interface": interface}
        if address:
            params["address"] = address
        params.update(kwargs)
        return self.call(f"Interface.{method}", params)

    def __repr__(self) -> str:
        return f"CCUClient({self.base_url!r}, user={self._username!r})"
