"""Tags, frontmatter, properties, and type management."""
from __future__ import annotations

import json
from pathlib import Path

from ..parser import extract_tags, parse_note, rebuild_note
from ..registry import VaultRegistry
from ._helpers import iter_notes, logger, resolve, resolve_single_vault


def vault_tag_list(registry: VaultRegistry, vault: str = "") -> str:
    """List all tags used across the vault with counts."""
    try:
        vc = resolve_single_vault(registry, vault)
        all_tags: dict[str, int] = {}
        for filepath in iter_notes(vc.path):
            content = filepath.read_text(encoding="utf-8")
            fm, _ = parse_note(content)
            tags = extract_tags(content, fm)
            for tag in tags:
                all_tags[tag] = all_tags.get(tag, 0) + 1
        if not all_tags:
            return "(no tags)"
        return "\n".join(f"{tag} ({count})" for tag, count in sorted(all_tags.items()))
    except Exception as e:
        return f"Error: {e}"


def vault_get_frontmatter(registry: VaultRegistry, path: str) -> str:
    """Read YAML frontmatter of a note as JSON."""
    try:
        _, filepath = resolve(registry, path)
        if not filepath.exists():
            return f"Error: note not found: {path}"
        content = filepath.read_text(encoding="utf-8")
        fm, _ = parse_note(content)
        return json.dumps(fm, indent=2, default=str) if fm else "{}"
    except Exception as e:
        return f"Error: {e}"


def vault_set_frontmatter(registry: VaultRegistry, path: str, key: str, value: str) -> str:
    """Set or update a frontmatter field. Auto-registers in types.json."""
    try:
        vault_root, filepath = resolve(registry, path)
        if not filepath.exists():
            return f"Error: note not found: {path}"
        content = filepath.read_text(encoding="utf-8")
        fm, body = parse_note(content)
        fm[key] = value
        filepath.write_text(rebuild_note(fm, body), encoding="utf-8")
        _ensure_type_registered(vault_root, key)
        logger.info("vault_set_frontmatter: %s set %s=%s", path, key, value)
        return f"Set {key}={value} in {path}"
    except Exception as e:
        return f"Error: {e}"


def vault_add_tag(registry: VaultRegistry, path: str, tag: str) -> str:
    """Add a tag to a note's frontmatter."""
    try:
        vault_root, filepath = resolve(registry, path)
        if not filepath.exists():
            return f"Error: note not found: {path}"
        content = filepath.read_text(encoding="utf-8")
        fm, body = parse_note(content)
        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]
        tag_clean = tag.lstrip("#")
        if tag_clean not in tags:
            tags.append(tag_clean)
        fm["tags"] = tags
        filepath.write_text(rebuild_note(fm, body), encoding="utf-8")
        return f"Added tag '{tag_clean}' to {path}"
    except Exception as e:
        return f"Error: {e}"


def vault_remove_tag(registry: VaultRegistry, path: str, tag: str) -> str:
    """Remove a tag from a note's frontmatter."""
    try:
        vault_root, filepath = resolve(registry, path)
        if not filepath.exists():
            return f"Error: note not found: {path}"
        content = filepath.read_text(encoding="utf-8")
        fm, body = parse_note(content)
        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]
        tag_clean = tag.lstrip("#")
        if tag_clean not in tags:
            return f"Tag '{tag_clean}' not found in {path}"
        tags = [t for t in tags if t != tag_clean]
        fm["tags"] = tags
        filepath.write_text(rebuild_note(fm, body), encoding="utf-8")
        logger.info("vault_remove_tag: %s removed '%s'", path, tag_clean)
        return f"Removed tag '{tag_clean}' from {path}"
    except Exception as e:
        return f"Error: {e}"


def vault_remove_frontmatter(registry: VaultRegistry, path: str, key: str) -> str:
    """Remove a frontmatter field from a note."""
    try:
        vault_root, filepath = resolve(registry, path)
        if not filepath.exists():
            return f"Error: note not found: {path}"
        content = filepath.read_text(encoding="utf-8")
        fm, body = parse_note(content)
        if key not in fm:
            return f"Key '{key}' not found in {path}"
        del fm[key]
        filepath.write_text(rebuild_note(fm, body), encoding="utf-8")
        logger.info("vault_remove_frontmatter: %s removed '%s'", path, key)
        return f"Removed '{key}' from {path}"
    except Exception as e:
        return f"Error: {e}"


def _read_types_json(vault_root: Path) -> dict:
    """Read .obsidian/types.json if it exists."""
    types_file = vault_root / ".obsidian" / "types.json"
    if types_file.exists():
        try:
            return json.loads(types_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def _write_types_json(vault_root: Path, data: dict) -> None:
    """Write .obsidian/types.json."""
    obsidian_dir = vault_root / ".obsidian"
    obsidian_dir.mkdir(exist_ok=True)
    types_file = obsidian_dir / "types.json"
    types_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _ensure_type_registered(vault_root: Path, key: str, type_hint: str = "text") -> None:
    """Register a frontmatter key in types.json if not already present."""
    data = _read_types_json(vault_root)
    types = data.get("types", {})
    if key not in types:
        types[key] = type_hint
        data["types"] = types
        _write_types_json(vault_root, data)


def vault_get_types(registry: VaultRegistry, vault: str = "") -> str:
    """Read .obsidian/types.json -- Obsidian's frontmatter type definitions."""
    try:
        vc = resolve_single_vault(registry, vault)
        data = _read_types_json(vc.path)
        return json.dumps(data, indent=2) if data else "(no types.json found)"
    except Exception as e:
        return f"Error: {e}"


def vault_set_type(registry: VaultRegistry, key: str, type_hint: str, vault: str = "") -> str:
    """Set a frontmatter field type in .obsidian/types.json.

    Types: text, number, date, datetime, checkbox, multitext, aliases, tags.
    """
    try:
        valid_types = {"text", "number", "date", "datetime", "checkbox", "multitext", "aliases", "tags"}
        if type_hint not in valid_types:
            return f"Error: invalid type '{type_hint}'. Valid: {', '.join(sorted(valid_types))}"
        vc = resolve_single_vault(registry, vault)
        data = _read_types_json(vc.path)
        types = data.get("types", {})
        types[key] = type_hint
        data["types"] = types
        _write_types_json(vc.path, data)
        logger.info("vault_set_type: %s = %s", key, type_hint)
        return f"Set type {key} = {type_hint}"
    except Exception as e:
        return f"Error: {e}"
