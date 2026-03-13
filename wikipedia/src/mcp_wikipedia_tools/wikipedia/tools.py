"""Pure tool logic for wikipedia — no MCP dependency."""

from __future__ import annotations

import json

from .client import WikipediaClient


def search(client: WikipediaClient, query: str, lang: str = "en", limit: int = 10) -> str:
    """Search Wikipedia articles"""
    data = client.opensearch(lang, query, limit)
    # opensearch returns [query, [titles], [descriptions], [urls]]
    if len(data) < 4:
        return json.dumps({"results": []})
    results = [
        {"title": t, "url": u}
        for t, u in zip(data[1], data[3])
    ]
    return json.dumps({"query": query, "lang": lang, "results": results}, indent=2)


def article(client: WikipediaClient, title: str, lang: str = "en") -> str:
    """Get full article content as plain text"""
    data = client.query(lang, titles=title, prop="extracts", explaintext=True)
    page = client._first_page(data)
    if not page or "missing" in page:
        return json.dumps({"error": f"Article '{title}' not found", "lang": lang})
    return page.get("extract", "")


def summary(client: WikipediaClient, title: str, lang: str = "en") -> str:
    """Get article summary (first section)"""
    data = client.rest(lang, f"page/summary/{title}")
    return json.dumps({
        "title": data.get("title", title),
        "description": data.get("description", ""),
        "extract": data.get("extract", ""),
        "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
    }, indent=2)


def links(client: WikipediaClient, title: str, lang: str = "en") -> str:
    """List all links from an article"""
    all_links = []
    plcontinue = None

    while True:
        params = {"titles": title, "prop": "links", "pllimit": "max"}
        if plcontinue:
            params["plcontinue"] = plcontinue
        data = client.query(lang, **params)
        page = client._first_page(data)
        if not page or "missing" in page:
            return json.dumps({"error": f"Article '{title}' not found", "lang": lang})
        all_links.extend(l["title"] for l in page.get("links", []))
        cont = data.get("continue", {})
        if "plcontinue" not in cont:
            break
        plcontinue = cont["plcontinue"]

    return json.dumps({"title": title, "lang": lang, "count": len(all_links), "links": all_links}, indent=2)


def categories(client: WikipediaClient, title: str, lang: str = "en") -> str:
    """List categories of an article"""
    data = client.query(lang, titles=title, prop="categories", cllimit="max")
    page = client._first_page(data)
    if not page or "missing" in page:
        return json.dumps({"error": f"Article '{title}' not found", "lang": lang})
    cats = [c["title"].removeprefix("Category:") for c in page.get("categories", [])]
    return json.dumps({"title": title, "lang": lang, "categories": cats}, indent=2)


def random(client: WikipediaClient, lang: str = "en") -> str:
    """Get a random article summary"""
    data = client.rest(lang, "page/random/summary")
    return json.dumps({
        "title": data.get("title", ""),
        "description": data.get("description", ""),
        "extract": data.get("extract", ""),
        "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
    }, indent=2)
