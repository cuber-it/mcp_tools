"""WikipediaClient — HTTP client for Wikipedia REST + MediaWiki APIs."""

from __future__ import annotations

import httpx

API_REST = "https://{lang}.wikipedia.org/api/rest_v1"
API_MEDIAWIKI = "https://{lang}.wikipedia.org/w/api.php"

USER_AGENT = (
    "mcp-wikipedia-tools/1.0.0 "
    "(https://github.com/cuber-it/mcp_tools; sonstige@uc-it.de)"
)


class WikipediaClient:
    def __init__(self, config: dict) -> None:
        self._client = httpx.Client(
            headers={"User-Agent": USER_AGENT},
            follow_redirects=True,
            timeout=15.0,
        )

    def rest(self, lang: str, path: str) -> dict:
        """GET request to Wikipedia REST API."""
        url = f"{API_REST.format(lang=lang)}/{path}"
        r = self._client.get(url)
        r.raise_for_status()
        return r.json()

    def query(self, lang: str, **params) -> dict:
        """GET request to MediaWiki API (action=query)."""
        params = {"action": "query", "format": "json", **params}
        url = API_MEDIAWIKI.format(lang=lang)
        r = self._client.get(url, params=params)
        r.raise_for_status()
        return r.json()

    def opensearch(self, lang: str, search: str, limit: int = 10) -> list:
        """OpenSearch API for quick search."""
        params = {
            "action": "opensearch",
            "search": search,
            "limit": limit,
            "format": "json",
        }
        url = API_MEDIAWIKI.format(lang=lang)
        r = self._client.get(url, params=params)
        r.raise_for_status()
        return r.json()

    def _first_page(self, data: dict) -> dict:
        """Extract first page from MediaWiki query result."""
        pages = data.get("query", {}).get("pages", {})
        if not pages:
            return {}
        return next(iter(pages.values()))
