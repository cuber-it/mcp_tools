"""CRUD operations and high-level note creation."""
from __future__ import annotations

import json
import re

from ..parser import ensure_md_extension, parse_note, rebuild_note
from ..registry import VaultRegistry
from ._helpers import iter_notes, logger, resolve


def vault_read(registry: VaultRegistry, path: str) -> str:
    """Read a note from the vault (returns frontmatter + body)."""
    try:
        vault_root, filepath = resolve(registry, path)
        if not filepath.exists():
            return f"Error: note not found: {path}"
        content = filepath.read_text(encoding="utf-8")
        fm, body = parse_note(content)
        result = {}
        if fm:
            result["frontmatter"] = fm
        result["body"] = body
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Error: {e}"


def vault_write(registry: VaultRegistry, path: str, content: str) -> str:
    """Write or overwrite a note in the vault."""
    try:
        vault_root, filepath = resolve(registry, path)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding="utf-8")
        logger.info("vault_write: %s", path)
        return f"Written: {path}"
    except Exception as e:
        return f"Error: {e}"


def vault_append(registry: VaultRegistry, path: str, content: str) -> str:
    """Append text to an existing note."""
    try:
        vault_root, filepath = resolve(registry, path)
        if not filepath.exists():
            return f"Error: note not found: {path}"
        existing = filepath.read_text(encoding="utf-8")
        filepath.write_text(existing.rstrip() + "\n\n" + content, encoding="utf-8")
        logger.info("vault_append: %s", path)
        return f"Appended to: {path}"
    except Exception as e:
        return f"Error: {e}"


def vault_prepend(registry: VaultRegistry, path: str, content: str) -> str:
    """Prepend text to a note's body (after frontmatter, before existing content)."""
    try:
        vault_root, filepath = resolve(registry, path)
        if not filepath.exists():
            return f"Error: note not found: {path}"
        existing = filepath.read_text(encoding="utf-8")
        fm, body = parse_note(existing)
        new_body = content + "\n\n" + body.lstrip()
        filepath.write_text(rebuild_note(fm, new_body), encoding="utf-8")
        logger.info("vault_prepend: %s", path)
        return f"Prepended to: {path}"
    except Exception as e:
        return f"Error: {e}"


def vault_delete(registry: VaultRegistry, path: str) -> str:
    """Delete a note from the vault."""
    try:
        vault_root, filepath = resolve(registry, path)
        if not filepath.exists():
            return f"Error: note not found: {path}"
        filepath.unlink()
        logger.info("vault_delete: %s", path)
        return f"Deleted: {path}"
    except Exception as e:
        return f"Error: {e}"


def vault_headings(registry: VaultRegistry, path: str) -> str:
    """List all headings in a note with their level. Useful before vault_insert_at or vault_split."""
    try:
        vault_root, filepath = resolve(registry, path)
        if not filepath.exists():
            return f"Error: note not found: {path}"
        content = filepath.read_text(encoding="utf-8")
        _, body = parse_note(content)
        headings = []
        for line in body.split("\n"):
            match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                indent = "  " * (level - 1)
                headings.append(f"{indent}{'#' * level} {text}")
        return "\n".join(headings) if headings else "(no headings)"
    except Exception as e:
        return f"Error: {e}"


def vault_list(registry: VaultRegistry, path: str = "", recursive: bool = False) -> str:
    """List notes in a folder."""
    try:
        vc, folder = registry.resolve(path) if path else (registry.resolve("")[0], "")
        notes = iter_notes(vc.path, folder, recursive)
        paths = [str(f.relative_to(vc.path)) for f in notes]
        return "\n".join(paths) if paths else "(empty)"
    except Exception as e:
        return f"Error: {e}"


def vault_exists(registry: VaultRegistry, path: str) -> str:
    """Check if a note exists."""
    try:
        _, filepath = resolve(registry, path)
        return "true" if filepath.exists() else "false"
    except Exception as e:
        return f"Error: {e}"


def vault_create(registry: VaultRegistry, path: str, title: str = "",
                 tags: list[str] | None = None, body: str = "",
                 extra_frontmatter: dict | None = None) -> str:
    """Create a note with structured parameters (no raw markdown needed).

    Example: vault_create("my-note", title="My Note", tags=["project"], body="Content here.")
    Auto-registers new frontmatter keys in types.json.
    """
    try:
        from .frontmatter import _ensure_type_registered

        fm = {}
        if title:
            fm["title"] = title
        if tags:
            fm["tags"] = tags
        if extra_frontmatter:
            fm.update(extra_frontmatter)
        content = rebuild_note(fm, body) if fm else body
        result = vault_write(registry, path, content)
        # Auto-register frontmatter keys in types.json
        if fm and not result.startswith("Error"):
            vc, _ = registry.resolve(path)
            for key in fm:
                _ensure_type_registered(vc.path, key)
        return result
    except Exception as e:
        return f"Error: {e}"
