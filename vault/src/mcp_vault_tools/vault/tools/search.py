"""Search operations for vault notes."""
from __future__ import annotations

import json
import re

from ..parser import expand_hierarchical_tags, extract_tags, parse_note
from ..registry import VaultRegistry
from ._helpers import iter_notes, resolve_vaults


def vault_search(registry: VaultRegistry, query: str, vault: str = "", limit: int = 0,
                 regex: bool = False, ignore_case: bool = True) -> str:
    """Full-text search across notes. Use vault='*' for all vaults.

    regex=True to use query as a regular expression.
    ignore_case=True by default (set False for exact case matching).
    """
    try:
        vaults = resolve_vaults(registry, vault)
        max_results = limit or vaults[0].max_results
        flags = re.IGNORECASE if ignore_case else 0
        pattern = re.compile(query if regex else re.escape(query), flags)
        results = []

        for vc in vaults:
            prefix = f"{vc.name}:" if len(vaults) > 1 else ""
            for filepath in iter_notes(vc.path):
                content = filepath.read_text(encoding="utf-8")
                fm, _ = parse_note(content)
                aliases = fm.get("aliases", [])
                if isinstance(aliases, str):
                    aliases = [aliases]
                alias_text = " ".join(str(a) for a in aliases)
                searchable = content + "\n" + alias_text

                matches = pattern.findall(searchable)
                if matches:
                    rel = str(filepath.relative_to(vc.path))
                    context = ""
                    if alias_text and pattern.search(alias_text):
                        context = f"[alias] {alias_text.strip()[:100]}"
                    else:
                        for line in content.split("\n"):
                            if pattern.search(line):
                                context = line.strip()[:100]
                                break
                    results.append(f"{prefix}{rel} ({len(matches)}x): {context}")
                    if len(results) >= max_results:
                        break
            if len(results) >= max_results:
                break

        return "\n".join(results) if results else "(no results)"
    except Exception as e:
        return f"Error: {e}"


def vault_search_tag(registry: VaultRegistry, tag: str, vault: str = "") -> str:
    """Find notes with a specific tag."""
    try:
        vaults = resolve_vaults(registry, vault)

        tag_clean = tag.lstrip("#")
        results = []
        for vc in vaults:
            prefix = f"{vc.name}:" if len(vaults) > 1 else ""
            for filepath in iter_notes(vc.path):
                content = filepath.read_text(encoding="utf-8")
                fm, _ = parse_note(content)
                tags = extract_tags(content, fm)
                expanded = expand_hierarchical_tags(tags)
                if tag_clean in tags or tag_clean in expanded:
                    results.append(f"{prefix}{filepath.relative_to(vc.path)}")

        return "\n".join(sorted(results)) if results else "(no results)"
    except Exception as e:
        return f"Error: {e}"


def vault_search_frontmatter(registry: VaultRegistry, key: str, value: str, vault: str = "") -> str:
    """Find notes by frontmatter field value."""
    try:
        vaults = resolve_vaults(registry, vault)

        results = []
        for vc in vaults:
            prefix = f"{vc.name}:" if len(vaults) > 1 else ""
            for filepath in iter_notes(vc.path):
                content = filepath.read_text(encoding="utf-8")
                fm, _ = parse_note(content)
                fm_value = fm.get(key)
                if fm_value is not None and str(fm_value) == value:
                    results.append(f"{prefix}{filepath.relative_to(vc.path)}")

        return "\n".join(sorted(results)) if results else "(no results)"
    except Exception as e:
        return f"Error: {e}"


def vault_find(registry: VaultRegistry, query: str, vault: str = "", limit: int = 0) -> str:
    """Unified search -- auto-detects query type.

    '#tag'        -> searches tags
    'key:value'   -> searches frontmatter
    'anything'    -> searches title, tags, body, frontmatter
    """
    try:
        # Tag search
        if query.startswith("#"):
            return vault_search_tag(registry, query, vault)

        # Frontmatter key:value search
        if ":" in query and not query.startswith("*"):
            parts = query.split(":", 1)
            key, value = parts[0].strip(), parts[1].strip()
            if key and value and " " not in key:
                result = vault_search_frontmatter(registry, key, value, vault)
                if "(no results)" not in result:
                    return result

        # Full search across everything
        vaults = resolve_vaults(registry, vault)

        max_results = limit or vaults[0].max_results
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        results = []

        for vc in vaults:
            prefix = f"{vc.name}:" if len(vaults) > 1 else ""
            for filepath in iter_notes(vc.path):
                content = filepath.read_text(encoding="utf-8")
                fm, body = parse_note(content)
                title = fm.get("title", "")
                tags = " ".join(extract_tags(content, fm))
                aliases = fm.get("aliases", [])
                if isinstance(aliases, str):
                    aliases = [aliases]
                alias_str = " ".join(str(a) for a in aliases)
                fm_str = json.dumps(fm, default=str)
                searchable = f"{title} {alias_str} {tags} {fm_str} {body}"

                if pattern.search(searchable):
                    rel = str(filepath.relative_to(vc.path))
                    # Best context: prefer title match, then first body match
                    ctx = ""
                    if title and pattern.search(title):
                        ctx = f"[title] {title}"
                    elif pattern.search(tags):
                        ctx = f"[tag] {tags}"
                    else:
                        for line in body.split("\n"):
                            if pattern.search(line):
                                ctx = line.strip()[:100]
                                break
                    results.append(f"{prefix}{rel}: {ctx}")
                    if len(results) >= max_results:
                        break
            if len(results) >= max_results:
                break

        return "\n".join(results) if results else "(no results)"
    except Exception as e:
        return f"Error: {e}"
