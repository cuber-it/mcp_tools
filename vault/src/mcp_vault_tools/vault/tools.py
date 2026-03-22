"""Vault tool implementations — headless Obsidian-compatible vault operations.

All functions receive a VaultRegistry and a prefixed path (e.g. "arbeit:note.md").
Pure filesystem operations, no SQLite, no index.
"""

from __future__ import annotations

import json
import logging
import re
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

from .parser import (
    _strip_code,
    ensure_md_extension,
    expand_hierarchical_tags,
    extract_links,
    extract_tags,
    extract_wikilinks,
    normalize_note_name,
    parse_note,
    rebuild_note,
)
from .registry import VaultConfig, VaultRegistry

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _safe_resolve(vault_root: Path, rel_path: str) -> Path:
    """Resolve a relative path and ensure it stays within the vault.

    Raises ValueError on path traversal attempts.
    """
    resolved = (vault_root / rel_path).resolve()
    vault_resolved = vault_root.resolve()
    if not str(resolved).startswith(str(vault_resolved) + "/") and resolved != vault_resolved:
        raise ValueError(f"Path traversal blocked: '{rel_path}' escapes vault")
    return resolved


def _resolve(registry: VaultRegistry, path: str) -> tuple[Path, Path]:
    """Resolve prefixed path to (vault_root, full_filepath)."""
    vc, rel = registry.resolve(path)
    vault_root = vc.path
    filepath = _safe_resolve(vault_root, ensure_md_extension(rel))
    return vault_root, filepath


def _resolve_vaults(registry: VaultRegistry, vault: str = "") -> list[VaultConfig]:
    """Resolve vault parameter to list of VaultConfigs.

    '' = default vault, 'name' = specific vault, '*' = all vaults.
    """
    if vault == "*":
        return registry.resolve_all()
    if vault:
        vc = registry.get(vault)
        if not vc:
            raise ValueError(f"Unknown vault '{vault}'")
        return [vc]
    vc, _ = registry.resolve("")
    return [vc]


def _resolve_single_vault(registry: VaultRegistry, vault: str = "") -> VaultConfig:
    """Resolve to a single VaultConfig (for non-search operations)."""
    vc, _ = registry.resolve(vault + ":_" if vault else "_")
    return vc


def _load_obsidianignore(vault_root: Path) -> list[str]:
    """Load .obsidianignore patterns if present."""
    ignore_file = vault_root / ".obsidianignore"
    if ignore_file.exists():
        return [
            line.strip() for line in ignore_file.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
    return []


def _is_ignored(path: Path, vault_root: Path, patterns: list[str]) -> bool:
    """Check if a path matches any .obsidianignore pattern."""
    rel = str(path.relative_to(vault_root))
    for pattern in patterns:
        if re.match(pattern.replace("*", ".*"), rel):
            return True
        if rel.startswith(pattern):
            return True
    return False


def _iter_notes(vault_root: Path, folder: str = "", recursive: bool = True) -> list[Path]:
    """Iterate over markdown files in a vault, respecting .obsidianignore."""
    base = vault_root / folder if folder else vault_root
    if not base.exists():
        return []
    ignore = _load_obsidianignore(vault_root)
    glob_fn = base.rglob if recursive else base.glob
    files = []
    for f in sorted(glob_fn("*.md")):
        if f.name.startswith("."):
            continue
        if ignore and _is_ignored(f, vault_root, ignore):
            continue
        # Skip .obsidian directory
        try:
            f.relative_to(vault_root / ".obsidian")
            continue
        except ValueError:
            pass
        files.append(f)
    return files


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------

def vault_read(registry: VaultRegistry, path: str) -> str:
    """Read a note from the vault (returns frontmatter + body)."""
    try:
        vault_root, filepath = _resolve(registry, path)
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
        vault_root, filepath = _resolve(registry, path)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding="utf-8")
        logger.info("vault_write: %s", path)
        return f"Written: {path}"
    except Exception as e:
        return f"Error: {e}"


def vault_append(registry: VaultRegistry, path: str, content: str) -> str:
    """Append text to an existing note."""
    try:
        vault_root, filepath = _resolve(registry, path)
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
        vault_root, filepath = _resolve(registry, path)
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
        vault_root, filepath = _resolve(registry, path)
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
        vault_root, filepath = _resolve(registry, path)
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
        notes = _iter_notes(vc.path, folder, recursive)
        paths = [str(f.relative_to(vc.path)) for f in notes]
        return "\n".join(paths) if paths else "(empty)"
    except Exception as e:
        return f"Error: {e}"


def vault_exists(registry: VaultRegistry, path: str) -> str:
    """Check if a note exists."""
    try:
        _, filepath = _resolve(registry, path)
        return "true" if filepath.exists() else "false"
    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

def vault_search(registry: VaultRegistry, query: str, vault: str = "", limit: int = 0,
                 regex: bool = False, ignore_case: bool = True) -> str:
    """Full-text search across notes. Use vault='*' for all vaults.

    regex=True to use query as a regular expression.
    ignore_case=True by default (set False for exact case matching).
    """
    try:
        vaults = _resolve_vaults(registry, vault)
        max_results = limit or vaults[0].max_results
        flags = re.IGNORECASE if ignore_case else 0
        pattern = re.compile(query if regex else re.escape(query), flags)
        results = []

        for vc in vaults:
            prefix = f"{vc.name}:" if len(vaults) > 1 else ""
            for filepath in _iter_notes(vc.path):
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
        vaults = _resolve_vaults(registry, vault)

        tag_clean = tag.lstrip("#")
        results = []
        for vc in vaults:
            prefix = f"{vc.name}:" if len(vaults) > 1 else ""
            for filepath in _iter_notes(vc.path):
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
        vaults = _resolve_vaults(registry, vault)

        results = []
        for vc in vaults:
            prefix = f"{vc.name}:" if len(vaults) > 1 else ""
            for filepath in _iter_notes(vc.path):
                content = filepath.read_text(encoding="utf-8")
                fm, _ = parse_note(content)
                fm_value = fm.get(key)
                if fm_value is not None and str(fm_value) == value:
                    results.append(f"{prefix}{filepath.relative_to(vc.path)}")

        return "\n".join(sorted(results)) if results else "(no results)"
    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------------------------
# Links
# ---------------------------------------------------------------------------

def vault_links(registry: VaultRegistry, path: str) -> str:
    """Get all outgoing links from a note (links and embeds separated)."""
    try:
        vault_root, filepath = _resolve(registry, path)
        if not filepath.exists():
            return f"Error: note not found: {path}"
        content = filepath.read_text(encoding="utf-8")
        links = extract_links(content)
        if not links:
            return "(no links)"
        lines = []
        for link in links:
            prefix = "!" if link.is_embed else ""
            suffix = ""
            if link.heading:
                suffix = f"#{link.heading}"
            elif link.block_id:
                suffix = f"#^{link.block_id}"
            alias = f" | {link.alias}" if link.alias else ""
            lines.append(f"{prefix}[[{link.target}{suffix}{alias}]]")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


def vault_backlinks(registry: VaultRegistry, path: str) -> str:
    """Find all notes that link to a given note."""
    try:
        vc, rel = registry.resolve(path)
        target = normalize_note_name(rel)
        results = []
        for filepath in _iter_notes(vc.path):
            content = filepath.read_text(encoding="utf-8")
            links = extract_links(content)
            # Check aliases
            fm, _ = parse_note(content)
            for link in links:
                if link.is_embed:
                    continue
                if normalize_note_name(link.target).lower() == target.lower():
                    results.append(str(filepath.relative_to(vc.path)))
                    break
            else:
                # Check if target has aliases
                target_filepath = vc.path / ensure_md_extension(rel)
                if target_filepath.exists():
                    target_content = target_filepath.read_text(encoding="utf-8")
                    target_fm, _ = parse_note(target_content)
                    aliases = target_fm.get("aliases", [])
                    if isinstance(aliases, str):
                        aliases = [aliases]
                    for link in links:
                        if link.is_embed:
                            continue
                        if normalize_note_name(link.target).lower() in [a.lower() for a in aliases]:
                            results.append(str(filepath.relative_to(vc.path)))
                            break

        return "\n".join(sorted(results)) if results else "(no backlinks)"
    except Exception as e:
        return f"Error: {e}"


def vault_related(registry: VaultRegistry, path: str, depth: int = 1) -> str:
    """Find related notes via link traversal."""
    try:
        vc, rel = registry.resolve(path)
        vault_root = vc.path
        filepath = vault_root / ensure_md_extension(rel)
        if not filepath.exists():
            return f"Error: note not found: {path}"

        visited = set()
        current_level = {str(filepath.relative_to(vault_root))}
        all_related = []

        for _ in range(depth):
            next_level = set()
            for note_path in current_level:
                if note_path in visited:
                    continue
                visited.add(note_path)
                fp = vault_root / note_path
                if not fp.exists():
                    continue
                content = fp.read_text(encoding="utf-8")
                for link in extract_wikilinks(content):
                    link_path = ensure_md_extension(link)
                    if (vault_root / link_path).exists():
                        next_level.add(link_path)
                    else:
                        for found in vault_root.rglob(f"{link}.md"):
                            next_level.add(str(found.relative_to(vault_root)))
                            break
            new_notes = next_level - visited
            if new_notes:
                all_related.extend(sorted(new_notes))
            current_level = next_level

        source = str(filepath.relative_to(vault_root))
        all_related = [r for r in all_related if r != source]
        return "\n".join(all_related) if all_related else "(no related notes)"
    except Exception as e:
        return f"Error: {e}"


def vault_orphans(registry: VaultRegistry, vault: str = "") -> str:
    """Find notes with no incoming links."""
    try:
        vc = _resolve_single_vault(registry, vault)
        vault_root = vc.path
        all_notes = {str(f.relative_to(vault_root)) for f in _iter_notes(vault_root)}
        linked = set()

        for filepath in _iter_notes(vault_root):
            for link in extract_wikilinks(filepath.read_text(encoding="utf-8")):
                link_path = ensure_md_extension(link)
                linked.add(link_path)
                for note in all_notes:
                    if normalize_note_name(note).lower() == normalize_note_name(link).lower():
                        linked.add(note)

        orphans = sorted(all_notes - linked)
        return "\n".join(orphans) if orphans else "(no orphans)"
    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------------------------
# Tags
# ---------------------------------------------------------------------------

def vault_tag_list(registry: VaultRegistry, vault: str = "") -> str:
    """List all tags used across the vault with counts."""
    try:
        vc = _resolve_single_vault(registry, vault)
        all_tags: dict[str, int] = {}
        for filepath in _iter_notes(vc.path):
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


# ---------------------------------------------------------------------------
# Frontmatter
# ---------------------------------------------------------------------------

def vault_get_frontmatter(registry: VaultRegistry, path: str) -> str:
    """Read YAML frontmatter of a note as JSON."""
    try:
        _, filepath = _resolve(registry, path)
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
        vault_root, filepath = _resolve(registry, path)
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
        vault_root, filepath = _resolve(registry, path)
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


# ---------------------------------------------------------------------------
# Properties
# ---------------------------------------------------------------------------

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
    """Read .obsidian/types.json — Obsidian's frontmatter type definitions."""
    try:
        vc = _resolve_single_vault(registry, vault)
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
        vc = _resolve_single_vault(registry, vault)
        data = _read_types_json(vc.path)
        types = data.get("types", {})
        types[key] = type_hint
        data["types"] = types
        _write_types_json(vc.path, data)
        logger.info("vault_set_type: %s = %s", key, type_hint)
        return f"Set type {key} = {type_hint}"
    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------------------------
# Remove
# ---------------------------------------------------------------------------

def vault_remove_tag(registry: VaultRegistry, path: str, tag: str) -> str:
    """Remove a tag from a note's frontmatter."""
    try:
        vault_root, filepath = _resolve(registry, path)
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
        vault_root, filepath = _resolve(registry, path)
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


# ---------------------------------------------------------------------------
# Rename / Move
# ---------------------------------------------------------------------------

def _update_links_in_vault(vault_root: Path, old_name: str, new_name: str) -> int:
    """Update all WikiLinks pointing to old_name to point to new_name.

    Returns number of files modified.
    """
    old_normalized = normalize_note_name(old_name).lower()
    modified = 0
    for filepath in vault_root.rglob("*.md"):
        content = filepath.read_text(encoding="utf-8")
        new_content = content
        # Replace [[old_name...]] with [[new_name...]]

        def replace_link(match):
            raw = match.group(1)
            link_target = raw.split("|")[0].split("#")[0].strip()
            if normalize_note_name(link_target).lower() == old_normalized:
                return match.group(0).replace(link_target, normalize_note_name(new_name))
            return match.group(0)

        new_content = re.sub(r"\[\[([^\]]+)\]\]", replace_link, new_content)
        new_content = re.sub(
            r"!\[\[([^\]]+)\]\]",
            lambda m: "!" + re.sub(
                r"\[\[([^\]]+)\]\]", replace_link,
                "[[" + m.group(1) + "]]"
            ),
            new_content,
        )

        if new_content != content:
            filepath.write_text(new_content, encoding="utf-8")
            modified += 1
    return modified


def vault_rename(registry: VaultRegistry, old_path: str, new_path: str) -> str:
    """Rename a note and update all links pointing to it."""
    try:
        vc_old, rel_old = registry.resolve(old_path)
        vc_new, rel_new = registry.resolve(new_path)
        if vc_old.name != vc_new.name:
            return "Error: cannot rename across vaults"

        old_file = vc_old.path / ensure_md_extension(rel_old)
        new_file = vc_new.path / ensure_md_extension(rel_new)

        if not old_file.exists():
            return f"Error: note not found: {old_path}"
        if new_file.exists():
            return f"Error: target already exists: {new_path}"

        new_file.parent.mkdir(parents=True, exist_ok=True)
        old_file.rename(new_file)
        modified = _update_links_in_vault(vc_old.path, rel_old, rel_new)
        logger.info("vault_rename: %s -> %s (%d links updated)", old_path, new_path, modified)
        return f"Renamed: {old_path} -> {new_path} ({modified} links updated)"
    except Exception as e:
        return f"Error: {e}"


def vault_move(registry: VaultRegistry, path: str, target_folder: str) -> str:
    """Move a note to a different folder and update all links."""
    try:
        vc, rel = registry.resolve(path)
        filename = Path(rel).name
        new_rel = str(Path(target_folder) / filename)
        new_path = f"{vc.name}:{new_rel}" if ":" in path else new_rel
        return vault_rename(registry, path, new_path)
    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------------------------
# Refactoring
# ---------------------------------------------------------------------------

def vault_tag_rename(registry: VaultRegistry, old_tag: str, new_tag: str,
                     vault: str = "", dry_run: bool = False) -> str:
    """Rename a tag across the entire vault (frontmatter + inline).

    dry_run=True shows what would change without modifying files.
    """
    try:
        vc = _resolve_single_vault(registry, vault)
        old_clean = old_tag.lstrip("#")
        new_clean = new_tag.lstrip("#")
        modified = 0
        preview_lines = []

        for filepath in _iter_notes(vc.path):
            content = filepath.read_text(encoding="utf-8")
            fm, body = parse_note(content)

            # Frontmatter tags
            fm_changed = False
            tags = fm.get("tags", [])
            if isinstance(tags, list) and old_clean in tags:
                tags = [new_clean if t == old_clean else t for t in tags]
                fm["tags"] = tags
                fm_changed = True

            # Inline tags
            new_body = re.sub(
                rf"((?:^|\s))#{re.escape(old_clean)}(?=\s|$)",
                rf"\1#{new_clean}",
                body,
            )

            if fm_changed or new_body != body:
                rel = str(filepath.relative_to(vc.path))
                if dry_run:
                    preview_lines.append(rel)
                else:
                    final_body = new_body if new_body != body else body
                    filepath.write_text(rebuild_note(fm, final_body), encoding="utf-8")
                    logger.info("vault_tag_rename: %s (%s -> %s)", rel, old_clean, new_clean)
                modified += 1

        prefix = "[DRY RUN] " if dry_run else ""
        result = f"{prefix}Renamed tag '{old_clean}' -> '{new_clean}' in {modified} notes"
        if dry_run and preview_lines:
            result += "\n" + "\n".join(preview_lines)
        return result
    except Exception as e:
        return f"Error: {e}"


def vault_tag_merge(registry: VaultRegistry, tags: list[str], target_tag: str, vault: str = "") -> str:
    """Merge multiple tags into one."""
    try:
        total = 0
        for tag in tags:
            if tag.lstrip("#") == target_tag.lstrip("#"):
                continue
            result = vault_tag_rename(registry, tag, target_tag, vault)
            if not result.startswith("Error"):
                count = int(re.search(r"(\d+) notes", result).group(1))
                total += count
        return f"Merged {len(tags)} tags into '{target_tag.lstrip('#')}', {total} notes modified"
    except Exception as e:
        return f"Error: {e}"


def vault_bulk_frontmatter(registry: VaultRegistry, key: str, value: str,
                           filter_tag: str = "", vault: str = "", dry_run: bool = False) -> str:
    """Set a frontmatter field in many notes, optionally filtered by tag.

    dry_run=True shows what would change without modifying files.
    """
    try:
        vc = _resolve_single_vault(registry, vault)
        modified = 0
        filter_clean = filter_tag.lstrip("#") if filter_tag else ""
        preview_lines = []

        for filepath in _iter_notes(vc.path):
            content = filepath.read_text(encoding="utf-8")
            fm, body = parse_note(content)

            if filter_clean:
                tags = extract_tags(content, fm)
                if filter_clean not in tags:
                    continue

            rel = str(filepath.relative_to(vc.path))
            if dry_run:
                preview_lines.append(rel)
            else:
                fm[key] = value
                filepath.write_text(rebuild_note(fm, body), encoding="utf-8")
                logger.info("vault_bulk_frontmatter: %s set %s=%s", rel, key, value)
            modified += 1

        prefix = "[DRY RUN] " if dry_run else ""
        result = f"{prefix}Set {key}={value} in {modified} notes"
        if dry_run and preview_lines:
            result += "\n" + "\n".join(preview_lines)
        return result
    except Exception as e:
        return f"Error: {e}"


def vault_broken_links(registry: VaultRegistry, vault: str = "") -> str:
    """Find all broken links (targets that don't exist)."""
    try:
        vc = _resolve_single_vault(registry, vault)
        vault_root = vc.path
        all_notes = {normalize_note_name(str(f.relative_to(vault_root))).lower()
                     for f in _iter_notes(vault_root)}
        broken = []

        for filepath in _iter_notes(vault_root):
            content = filepath.read_text(encoding="utf-8")
            for link in extract_links(content):
                if link.is_embed and not link.target.endswith(".md"):
                    continue  # skip image/file embeds
                target = normalize_note_name(link.target).lower()
                if target not in all_notes:
                    rel = str(filepath.relative_to(vault_root))
                    broken.append(f"{rel} -> [[{link.target}]]")

        return "\n".join(sorted(broken)) if broken else "(no broken links)"
    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def vault_stats(registry: VaultRegistry, vault: str = "") -> str:
    """Vault statistics: notes, tags, links, orphans."""
    try:
        vc = _resolve_single_vault(registry, vault)
        vault_root = vc.path
        notes = _iter_notes(vault_root)
        total_links = 0
        total_tags = set()
        linked_targets = set()

        for filepath in notes:
            content = filepath.read_text(encoding="utf-8")
            fm, _ = parse_note(content)
            links = extract_wikilinks(content)
            total_links += len(links)
            for link in links:
                linked_targets.add(normalize_note_name(link).lower())
            tags = extract_tags(content, fm)
            total_tags.update(tags)

        all_note_names = {
            normalize_note_name(str(f.relative_to(vault_root))).lower()
            for f in notes
        }
        orphan_count = len(all_note_names - linked_targets)

        return json.dumps({
            "vault": vc.name,
            "notes": len(notes),
            "tags": len(total_tags),
            "links": total_links,
            "orphans": orphan_count,
        }, indent=2)
    except Exception as e:
        return f"Error: {e}"


def vault_recent(registry: VaultRegistry, limit: int = 10, vault: str = "") -> str:
    """List recently modified notes."""
    try:
        vc = _resolve_single_vault(registry, vault)
        notes = _iter_notes(vc.path)
        by_mtime = sorted(notes, key=lambda f: f.stat().st_mtime, reverse=True)
        lines = []
        for f in by_mtime[:limit]:
            rel = str(f.relative_to(vc.path))
            mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            lines.append(f"{rel} ({mtime})")
        return "\n".join(lines) if lines else "(empty)"
    except Exception as e:
        return f"Error: {e}"


def vault_health(registry: VaultRegistry, vault: str = "") -> str:
    """Vault health report: stats + orphans + broken links + tag distribution."""
    try:
        stats = vault_stats(registry, vault)
        broken = vault_broken_links(registry, vault)
        orphans = vault_orphans(registry, vault)
        tags = vault_tag_list(registry, vault)

        parts = [
            "=== Stats ===",
            stats,
            "\n=== Broken Links ===",
            broken,
            "\n=== Orphans ===",
            orphans,
            "\n=== Tags ===",
            tags,
        ]
        return "\n".join(parts)
    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------------------------
# Convenience — High-Level
# ---------------------------------------------------------------------------

def vault_create(registry: VaultRegistry, path: str, title: str = "",
                 tags: list[str] | None = None, body: str = "",
                 extra_frontmatter: dict | None = None) -> str:
    """Create a note with structured parameters (no raw markdown needed).

    Example: vault_create("my-note", title="My Note", tags=["project"], body="Content here.")
    Auto-registers new frontmatter keys in types.json.
    """
    try:
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


def vault_find(registry: VaultRegistry, query: str, vault: str = "", limit: int = 0) -> str:
    """Unified search — auto-detects query type.

    '#tag'        → searches tags
    'key:value'   → searches frontmatter
    'anything'    → searches title, tags, body, frontmatter
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
        vaults = _resolve_vaults(registry, vault)

        max_results = limit or vaults[0].max_results
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        results = []

        for vc in vaults:
            prefix = f"{vc.name}:" if len(vaults) > 1 else ""
            for filepath in _iter_notes(vc.path):
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


def vault_summary(registry: VaultRegistry, path: str, recursive: bool = False) -> str:
    """Quick overview: title + tags + preview for one note or a folder.

    Single note: vault_summary("note")
    Folder: vault_summary("folder/", recursive=True)
    """
    try:
        vc, rel = registry.resolve(path)
        target = vc.path / rel

        # Single note
        if not rel.endswith("/") and (vc.path / ensure_md_extension(rel)).exists():
            filepath = vc.path / ensure_md_extension(rel)
            content = filepath.read_text(encoding="utf-8")
            fm, body = parse_note(content)
            title = fm.get("title", normalize_note_name(Path(rel).name))
            tags = extract_tags(content, fm)
            lines = [ln.strip() for ln in body.strip().split("\n") if ln.strip() and not ln.startswith("#")]
            preview = lines[0][:100] if lines else ""
            return json.dumps({
                "path": rel,
                "title": title,
                "tags": tags,
                "preview": preview,
            }, indent=2, default=str)

        # Folder listing with summaries
        folder = rel.rstrip("/")
        notes = _iter_notes(vc.path, folder, recursive)
        summaries = []
        for filepath in notes:
            content = filepath.read_text(encoding="utf-8")
            fm, body = parse_note(content)
            note_rel = str(filepath.relative_to(vc.path))
            title = fm.get("title", normalize_note_name(filepath.stem))
            tags = extract_tags(content, fm)
            lines = [ln.strip() for ln in body.strip().split("\n") if ln.strip() and not ln.startswith("#")]
            preview = lines[0][:80] if lines else ""
            summaries.append(f"{note_rel} | {title} | {', '.join(tags[:3])} | {preview}")

        return "\n".join(summaries) if summaries else "(empty)"
    except Exception as e:
        return f"Error: {e}"


def vault_tree(registry: VaultRegistry, vault: str = "", max_depth: int = 3) -> str:
    """Visual tree of the vault structure."""
    try:
        vc = _resolve_single_vault(registry, vault)
        vault_root = vc.path

        def _tree(directory: Path, prefix: str = "", depth: int = 0) -> list[str]:
            if depth >= max_depth:
                return []
            entries = sorted(directory.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
            entries = [
                e for e in entries
                if not e.name.startswith(".") and e.name != "_templates"
            ]
            lines = []
            for i, entry in enumerate(entries):
                is_last = i == len(entries) - 1
                connector = "└── " if is_last else "├── "
                if entry.is_dir():
                    count = len(list(entry.rglob("*.md")))
                    lines.append(f"{prefix}{connector}{entry.name}/ ({count})")
                    extension = "    " if is_last else "│   "
                    lines.extend(_tree(entry, prefix + extension, depth + 1))
                elif entry.suffix == ".md":
                    lines.append(f"{prefix}{connector}{entry.name}")
            return lines

        lines = [f"{vc.name}/"]
        lines.extend(_tree(vault_root))
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


def vault_copy(registry: VaultRegistry, source: str, target: str) -> str:
    """Duplicate a note (preserves frontmatter)."""
    try:
        _, source_file = _resolve(registry, source)
        if not source_file.exists():
            return f"Error: note not found: {source}"
        content = source_file.read_text(encoding="utf-8")
        return vault_write(registry, target, content)
    except Exception as e:
        return f"Error: {e}"


def vault_frontmatter_keys(registry: VaultRegistry, vault: str = "") -> str:
    """List all frontmatter keys used across the vault with frequency."""
    try:
        vc = _resolve_single_vault(registry, vault)
        key_counts: dict[str, int] = defaultdict(int)

        for filepath in _iter_notes(vc.path):
            content = filepath.read_text(encoding="utf-8")
            fm, _ = parse_note(content)
            for key in fm:
                key_counts[key] += 1

        if not key_counts:
            return "(no frontmatter found)"

        ranked = sorted(key_counts.items(), key=lambda x: x[1], reverse=True)
        return "\n".join(f"{key} ({count})" for key, count in ranked)
    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------------------------
# Advanced Editing
# ---------------------------------------------------------------------------

def vault_replace(registry: VaultRegistry, query: str, replacement: str,
                  vault: str = "", dry_run: bool = False, ignore_case: bool = False,
                  regex: bool = False) -> str:
    """Find and replace text across the entire vault.

    dry_run=True shows what would change without modifying files.
    ignore_case=True for case-insensitive matching.
    regex=True to use query as a regular expression.
    """
    try:
        vc = _resolve_single_vault(registry, vault)
        flags = re.IGNORECASE if ignore_case else 0
        pattern = re.compile(query if regex else re.escape(query), flags)
        modified = 0
        total_replacements = 0
        preview_lines = []

        for filepath in _iter_notes(vc.path):
            content = filepath.read_text(encoding="utf-8")
            new_content, count = pattern.subn(replacement, content)
            if count > 0:
                rel = str(filepath.relative_to(vc.path))
                if dry_run:
                    preview_lines.append(f"{rel}: {count} replacements")
                else:
                    filepath.write_text(new_content, encoding="utf-8")
                    logger.info("vault_replace: %s (%d replacements)", rel, count)
                modified += 1
                total_replacements += count

        prefix = "[DRY RUN] " if dry_run else ""
        result = f"{prefix}Replaced '{query}' -> '{replacement}': {total_replacements} occurrences in {modified} notes"
        if dry_run and preview_lines:
            result += "\n" + "\n".join(preview_lines)
        return result
    except Exception as e:
        return f"Error: {e}"


def vault_insert_at(registry: VaultRegistry, path: str, heading: str, content: str, position: str = "append") -> str:
    """Insert content under a specific heading.

    position: 'append' (end of section), 'prepend' (start of section), 'replace' (replace section content).
    """
    try:
        vault_root, filepath = _resolve(registry, path)
        if not filepath.exists():
            return f"Error: note not found: {path}"

        file_content = filepath.read_text(encoding="utf-8")
        fm, body = parse_note(file_content)
        lines = body.split("\n")

        # Find the heading
        heading_clean = heading.lstrip("#").strip()
        heading_idx = -1
        heading_level = 0
        for i, line in enumerate(lines):
            match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if match and match.group(2).strip() == heading_clean:
                heading_idx = i
                heading_level = len(match.group(1))
                break

        if heading_idx == -1:
            return f"Error: heading '{heading}' not found in {path}"

        # Find end of section (next heading of same or higher level, or end of file)
        section_end = len(lines)
        for i in range(heading_idx + 1, len(lines)):
            match = re.match(r"^(#{1,6})\s+", lines[i])
            if match and len(match.group(1)) <= heading_level:
                section_end = i
                break

        if position == "append":
            # Insert before section end
            insert_idx = section_end
            # Skip trailing blank lines
            while insert_idx > heading_idx + 1 and not lines[insert_idx - 1].strip():
                insert_idx -= 1
            lines.insert(insert_idx, "\n" + content)
        elif position == "prepend":
            # Insert right after heading
            lines.insert(heading_idx + 1, "\n" + content)
        elif position == "replace":
            # Replace everything between heading and next heading
            lines[heading_idx + 1:section_end] = ["\n" + content + "\n"]

        new_body = "\n".join(lines)
        filepath.write_text(rebuild_note(fm, new_body), encoding="utf-8")
        return f"Inserted at '{heading}' ({position}) in {path}"
    except Exception as e:
        return f"Error: {e}"


def vault_split(registry: VaultRegistry, path: str, heading: str) -> str:
    """Split a note at a heading — extracts the section into a new note.

    The new note gets the heading as title. Links are preserved.
    """
    try:
        vc, rel = registry.resolve(path)
        vault_root = vc.path
        filepath = vault_root / ensure_md_extension(rel)
        if not filepath.exists():
            return f"Error: note not found: {path}"

        content = filepath.read_text(encoding="utf-8")
        fm, body = parse_note(content)
        lines = body.split("\n")

        # Find the heading
        heading_clean = heading.lstrip("#").strip()
        heading_idx = -1
        heading_level = 0
        for i, line in enumerate(lines):
            match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if match and match.group(2).strip() == heading_clean:
                heading_idx = i
                heading_level = len(match.group(1))
                break

        if heading_idx == -1:
            return f"Error: heading '{heading}' not found in {path}"

        # Find end of section
        section_end = len(lines)
        for i in range(heading_idx + 1, len(lines)):
            match = re.match(r"^(#{1,6})\s+", lines[i])
            if match and len(match.group(1)) <= heading_level:
                section_end = i
                break

        # Extract section content
        section_lines = lines[heading_idx + 1:section_end]
        section_body = "\n".join(section_lines).strip()

        # Create new note
        new_name = re.sub(r"[^\w\s-]", "", heading_clean).strip().replace(" ", "-").lower()
        new_rel = str(Path(rel).parent / new_name) if "/" in rel else new_name
        new_fm = {"title": heading_clean}
        # Copy relevant tags from parent
        if fm.get("tags"):
            new_fm["tags"] = fm["tags"]

        new_path = f"{vc.name}:{new_rel}" if ":" in path else new_rel
        vault_write(registry, new_path, rebuild_note(new_fm, section_body))

        # Replace section in original with a link
        link_line = f"See [[{new_name}]]"
        lines[heading_idx + 1:section_end] = ["\n" + link_line + "\n"]
        new_body = "\n".join(lines)
        filepath.write_text(rebuild_note(fm, new_body), encoding="utf-8")

        return f"Split '{heading}' from {path} -> {new_path}"
    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------------------------
# Connection Discovery
# ---------------------------------------------------------------------------

def vault_unlinked_mentions(registry: VaultRegistry, path: str) -> str:
    """Find notes that mention this note's name in text but don't link to it.

    The Obsidian killer-feature: discovers implicit connections.
    """
    try:
        vc, rel = registry.resolve(path)
        vault_root = vc.path
        target_name = normalize_note_name(Path(rel).stem)
        if not target_name:
            return "Error: cannot determine note name"

        target_file = vault_root / ensure_md_extension(rel)

        # Also check aliases
        aliases = [target_name]
        if target_file.exists():
            content = target_file.read_text(encoding="utf-8")
            fm, _ = parse_note(content)
            fm_aliases = fm.get("aliases", [])
            if isinstance(fm_aliases, str):
                fm_aliases = [fm_aliases]
            aliases.extend(fm_aliases)

        # Build pattern that matches any alias/name but NOT inside [[...]]
        results = []
        for filepath in _iter_notes(vault_root):
            if filepath == target_file:
                continue
            file_content = filepath.read_text(encoding="utf-8")
            file_rel = str(filepath.relative_to(vault_root))

            # Check if already linked
            linked_targets = [normalize_note_name(lnk).lower() for lnk in extract_wikilinks(file_content)]

            clean = _strip_code(file_content)
            # Remove existing wikilinks from search text
            clean_no_links = re.sub(r"!?\[\[[^\]]+\]\]", "", clean)

            for alias in aliases:
                if alias.lower() in [t.lower() for t in linked_targets]:
                    continue  # already linked
                pattern = re.compile(r"\b" + re.escape(alias) + r"\b", re.IGNORECASE)
                matches = pattern.findall(clean_no_links)
                if matches:
                    # Find first matching line for context
                    for line in clean_no_links.split("\n"):
                        if pattern.search(line):
                            ctx = line.strip()[:100]
                            break
                    else:
                        ctx = ""
                    results.append(f"{file_rel} ({len(matches)}x '{alias}'): {ctx}")
                    break  # one match per file is enough

        return "\n".join(sorted(results)) if results else "(no unlinked mentions)"
    except Exception as e:
        return f"Error: {e}"


def vault_link_suggest(registry: VaultRegistry, path: str, limit: int = 10) -> str:
    """Suggest notes that should be linked — based on shared tags and related content."""
    try:
        vc, rel = registry.resolve(path)
        vault_root = vc.path
        filepath = vault_root / ensure_md_extension(rel)
        if not filepath.exists():
            return f"Error: note not found: {path}"

        content = filepath.read_text(encoding="utf-8")
        fm, _ = parse_note(content)
        source_tags = set(extract_tags(content, fm))
        source_links = set(normalize_note_name(lnk).lower() for lnk in extract_wikilinks(content))
        source_rel = str(filepath.relative_to(vault_root))

        scores: dict[str, tuple[int, list[str]]] = {}

        for other_file in _iter_notes(vault_root):
            other_rel = str(other_file.relative_to(vault_root))
            if other_rel == source_rel:
                continue
            other_name = normalize_note_name(other_rel).lower()
            if other_name in source_links:
                continue  # already linked

            other_content = other_file.read_text(encoding="utf-8")
            other_fm, _ = parse_note(other_content)
            other_tags = set(extract_tags(other_content, other_fm))

            shared = source_tags & other_tags
            if shared:
                scores[other_rel] = (len(shared), sorted(shared))

        ranked = sorted(scores.items(), key=lambda x: x[1][0], reverse=True)[:limit]
        lines = [f"{path} ({count} shared tags: {', '.join(tags)})" for path, (count, tags) in ranked]
        return "\n".join(lines) if lines else "(no suggestions)"
    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------------------------
# Changelog
# ---------------------------------------------------------------------------

def vault_changelog(registry: VaultRegistry, days: int = 7, vault: str = "") -> str:
    """Recent changes grouped by day."""
    try:
        vc = _resolve_single_vault(registry, vault)
        notes = _iter_notes(vc.path)
        now = datetime.now()
        cutoff = now.timestamp() - (days * 86400)

        by_day: dict[str, list[str]] = defaultdict(list)
        for f in notes:
            mtime = f.stat().st_mtime
            if mtime >= cutoff:
                day = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
                rel = str(f.relative_to(vc.path))
                time_str = datetime.fromtimestamp(mtime).strftime("%H:%M")
                by_day[day].append(f"  {time_str} {rel}")

        if not by_day:
            return f"(no changes in the last {days} days)"

        lines = []
        for day in sorted(by_day.keys(), reverse=True):
            lines.append(f"=== {day} ({len(by_day[day])} changes) ===")
            lines.extend(sorted(by_day[day], reverse=True))
            lines.append("")

        return "\n".join(lines).rstrip()
    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------------------------
# Convenience — Daily & Capture
# ---------------------------------------------------------------------------

def vault_daily(registry: VaultRegistry, day: str = "", vault: str = "") -> str:
    """Create or read a daily note. Format from config."""
    try:
        vc = _resolve_single_vault(registry, vault)
        if day:
            try:
                d = datetime.strptime(day, "%Y-%m-%d").date()
            except ValueError:
                return f"Error: invalid date format, use YYYY-MM-DD"
        else:
            d = date.today()

        filename = d.strftime(vc.daily_format) + ".md"
        filepath = vc.path / filename

        if filepath.exists():
            content = filepath.read_text(encoding="utf-8")
            fm, body = parse_note(content)
            result = {"exists": True}
            if fm:
                result["frontmatter"] = fm
            result["body"] = body
            return json.dumps(result, indent=2, default=str)
        else:
            fm = {"date": str(d), "tags": ["daily"]}
            body = f"# {d.strftime('%A, %B %d, %Y')}\n\n"
            filepath.write_text(rebuild_note(fm, body), encoding="utf-8")
            return f"Created daily note: {filename}"
    except Exception as e:
        return f"Error: {e}"


def vault_inbox(registry: VaultRegistry, content: str, vault: str = "") -> str:
    """Quick-capture: append content to the inbox note."""
    try:
        vc = _resolve_single_vault(registry, vault)
        inbox = vc.path / vc.inbox_path
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"\n\n---\n*{timestamp}*\n\n{content}"

        if inbox.exists():
            existing = inbox.read_text(encoding="utf-8")
            inbox.write_text(existing.rstrip() + entry, encoding="utf-8")
        else:
            inbox.write_text(f"# Inbox\n{entry}", encoding="utf-8")

        return f"Added to inbox ({vc.inbox_path})"
    except Exception as e:
        return f"Error: {e}"


def vault_merge(registry: VaultRegistry, path_a: str, path_b: str, target: str = "") -> str:
    """Merge two notes into one. Updates backlinks."""
    try:
        vc_a, rel_a = registry.resolve(path_a)
        vc_b, rel_b = registry.resolve(path_b)
        if vc_a.name != vc_b.name:
            return "Error: cannot merge across vaults"

        file_a = vc_a.path / ensure_md_extension(rel_a)
        file_b = vc_b.path / ensure_md_extension(rel_b)

        if not file_a.exists():
            return f"Error: note not found: {path_a}"
        if not file_b.exists():
            return f"Error: note not found: {path_b}"

        content_a = file_a.read_text(encoding="utf-8")
        content_b = file_b.read_text(encoding="utf-8")
        fm_a, body_a = parse_note(content_a)
        fm_b, body_b = parse_note(content_b)

        # Merge frontmatter (a wins on conflicts, tags are merged)
        merged_fm = {**fm_b, **fm_a}
        tags_a = set(fm_a.get("tags", []) if isinstance(fm_a.get("tags"), list) else [])
        tags_b = set(fm_b.get("tags", []) if isinstance(fm_b.get("tags"), list) else [])
        if tags_a or tags_b:
            merged_fm["tags"] = sorted(tags_a | tags_b)

        merged_body = body_a.rstrip() + f"\n\n---\n\n*Merged from [[{normalize_note_name(rel_b)}]]*\n\n" + body_b

        target_path = target or path_a
        _, target_file = _resolve(registry, target_path)
        target_file.write_text(rebuild_note(merged_fm, merged_body), encoding="utf-8")

        # Update backlinks from B to point to target
        if target_path != path_b:
            _, target_rel = registry.resolve(target_path)
            _update_links_in_vault(vc_a.path, rel_b, target_rel)

        if target_path != path_b:
            file_b.unlink()

        return f"Merged {path_a} + {path_b} -> {target_path}"
    except Exception as e:
        return f"Error: {e}"


def vault_from_template(registry: VaultRegistry, template: str, target: str, variables: dict | None = None) -> str:
    """Create a note from a template with variable substitution."""
    try:
        vc, template_rel = registry.resolve(template)
        template_dir = vc.path / vc.template_dir
        template_file = template_dir / ensure_md_extension(template_rel)

        # Also try direct path if template_dir doesn't have it
        if not template_file.exists():
            template_file = vc.path / ensure_md_extension(template_rel)

        if not template_file.exists():
            return f"Error: template not found: {template}"

        content = template_file.read_text(encoding="utf-8")

        if variables:
            for key, val in variables.items():
                content = content.replace("{{" + key + "}}", str(val))

        now = datetime.now()
        content = content.replace("{{date}}", now.strftime("%Y-%m-%d"))
        content = content.replace("{{time}}", now.strftime("%H:%M"))
        content = content.replace("{{datetime}}", now.strftime("%Y-%m-%d %H:%M"))

        return vault_write(registry, target, content)
    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------------------------
# Multi-Vault
# ---------------------------------------------------------------------------

def vault_list_vaults(registry: VaultRegistry) -> str:
    """List all configured vaults with name, path, and note count."""
    try:
        vaults = registry.list_vaults()
        if not vaults:
            return "(no vaults configured)"
        lines = []
        for vc in vaults:
            count = len(_iter_notes(vc.path))
            default = " (default)" if vc.name == registry.default_name else ""
            lines.append(f"{vc.name}{default}: {vc.path} ({count} notes)")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------------------------
# Composite Operations
# ---------------------------------------------------------------------------

def vault_link_mentions(registry: VaultRegistry, path: str, dry_run: bool = False) -> str:
    """Auto-link all unlinked mentions of a note across the vault.

    Finds text that mentions the note name without [[linking]] it,
    then converts those mentions to WikiLinks.
    """
    try:
        vc, rel = registry.resolve(path)
        vault_root = vc.path
        target_name = normalize_note_name(Path(rel).stem)
        target_file = vault_root / ensure_md_extension(rel)
        if not target_file.exists():
            return f"Error: note not found: {path}"

        aliases = [target_name]
        content = target_file.read_text(encoding="utf-8")
        fm, _ = parse_note(content)
        fm_aliases = fm.get("aliases", [])
        if isinstance(fm_aliases, str):
            fm_aliases = [fm_aliases]
        aliases.extend(fm_aliases)

        modified = 0
        preview_lines = []

        for filepath in _iter_notes(vault_root):
            if filepath == target_file:
                continue
            file_content = filepath.read_text(encoding="utf-8")
            new_content = file_content
            linked_targets = [normalize_note_name(lnk).lower() for lnk in extract_wikilinks(file_content)]

            for alias in aliases:
                if alias.lower() in linked_targets:
                    continue
                # Replace mentions outside of existing wikilinks and code
                pattern = re.compile(r"(?<!\[\[)\b(" + re.escape(alias) + r")\b(?!\]\])", re.IGNORECASE)
                # Don't replace inside [[...]] or `...` or ```...```
                clean = _strip_code(new_content)
                if pattern.search(clean):
                    if dry_run:
                        rel_path = str(filepath.relative_to(vault_root))
                        preview_lines.append(f"{rel_path}: '{alias}'")
                        modified += 1
                        break
                    else:
                        new_content = pattern.sub(f"[[{target_name}|\\1]]", new_content)

            if not dry_run and new_content != file_content:
                filepath.write_text(new_content, encoding="utf-8")
                logger.info("vault_link_mentions: linked '%s' in %s", target_name, filepath.name)
                modified += 1

        prefix = "[DRY RUN] " if dry_run else ""
        result = f"{prefix}Linked mentions of '{target_name}' in {modified} notes"
        if dry_run and preview_lines:
            result += "\n" + "\n".join(preview_lines)
        return result
    except Exception as e:
        return f"Error: {e}"


def vault_archive(registry: VaultRegistry, days: int = 90, archive_folder: str = "archive",
                  vault: str = "", dry_run: bool = False) -> str:
    """Move notes older than N days to an archive folder. Updates links."""
    try:
        vc = _resolve_single_vault(registry, vault)
        vault_root = vc.path
        cutoff = datetime.now().timestamp() - (days * 86400)
        moved = 0
        preview_lines = []

        for filepath in _iter_notes(vault_root):
            # Skip notes already in archive
            rel = str(filepath.relative_to(vault_root))
            if rel.startswith(archive_folder + "/"):
                continue
            if filepath.stat().st_mtime < cutoff:
                if dry_run:
                    mtime = datetime.fromtimestamp(filepath.stat().st_mtime).strftime("%Y-%m-%d")
                    preview_lines.append(f"{rel} (last modified: {mtime})")
                    moved += 1
                else:
                    new_path = Path(archive_folder) / filepath.name
                    new_filepath = vault_root / new_path
                    new_filepath.parent.mkdir(parents=True, exist_ok=True)
                    filepath.rename(new_filepath)
                    _update_links_in_vault(vault_root, rel, str(new_path))
                    logger.info("vault_archive: %s -> %s", rel, new_path)
                    moved += 1

        prefix = "[DRY RUN] " if dry_run else ""
        result = f"{prefix}Archived {moved} notes older than {days} days to {archive_folder}/"
        if dry_run and preview_lines:
            result += "\n" + "\n".join(preview_lines)
        return result
    except Exception as e:
        return f"Error: {e}"


def vault_extract_inline_tags(registry: VaultRegistry, path: str) -> str:
    """Move inline #tags to frontmatter and remove them from body text."""
    try:
        vault_root, filepath = _resolve(registry, path)
        if not filepath.exists():
            return f"Error: note not found: {path}"

        content = filepath.read_text(encoding="utf-8")
        fm, body = parse_note(content)

        # Find inline tags (not in code blocks)
        clean = _strip_code(body)
        inline_tags = set(re.findall(r"(?:^|\s)#([a-zA-Z][a-zA-Z0-9_/-]*)", clean, re.MULTILINE))
        if not inline_tags:
            return f"No inline tags found in {path}"

        # Add to frontmatter
        existing_tags = fm.get("tags", [])
        if isinstance(existing_tags, str):
            existing_tags = [t.strip() for t in existing_tags.split(",")]
        all_tags = set(existing_tags) | inline_tags
        fm["tags"] = sorted(all_tags)

        # Remove inline tags from body
        new_body = body
        for tag in inline_tags:
            new_body = re.sub(rf"(\s)#{re.escape(tag)}(?=\s|$)", r"\1", new_body)
            new_body = re.sub(rf"^#{re.escape(tag)}(?=\s|$)", "", new_body, flags=re.MULTILINE)

        filepath.write_text(rebuild_note(fm, new_body), encoding="utf-8")
        logger.info("vault_extract_inline_tags: %s (%d tags moved)", path, len(inline_tags))
        return f"Extracted {len(inline_tags)} inline tags to frontmatter in {path}: {', '.join(sorted(inline_tags))}"
    except Exception as e:
        return f"Error: {e}"


def vault_backfill_titles(registry: VaultRegistry, vault: str = "", dry_run: bool = False) -> str:
    """Add title to frontmatter for all notes that don't have one. Uses filename as title."""
    try:
        vc = _resolve_single_vault(registry, vault)
        modified = 0
        preview_lines = []

        for filepath in _iter_notes(vc.path):
            content = filepath.read_text(encoding="utf-8")
            fm, body = parse_note(content)
            if "title" not in fm:
                title = normalize_note_name(filepath.stem).replace("-", " ").replace("_", " ")
                rel = str(filepath.relative_to(vc.path))
                if dry_run:
                    preview_lines.append(f"{rel} -> \"{title}\"")
                else:
                    fm["title"] = title
                    filepath.write_text(rebuild_note(fm, body), encoding="utf-8")
                    logger.info("vault_backfill_titles: %s -> '%s'", rel, title)
                modified += 1

        prefix = "[DRY RUN] " if dry_run else ""
        result = f"{prefix}Added titles to {modified} notes"
        if dry_run and preview_lines:
            result += "\n" + "\n".join(preview_lines)
        return result
    except Exception as e:
        return f"Error: {e}"


def vault_standardize(registry: VaultRegistry, vault: str = "", dry_run: bool = False) -> str:
    """Standardize the vault: backfill titles, extract inline tags, register types.

    The 'make my vault clean' button.
    """
    try:
        parts = []

        # 1. Backfill titles
        result = vault_backfill_titles(registry, vault, dry_run)
        parts.append(f"Titles: {result}")

        # 2. Extract inline tags for all notes
        vc = _resolve_single_vault(registry, vault)
        extracted = 0
        for filepath in _iter_notes(vc.path):
            rel = str(filepath.relative_to(vc.path))
            prefixed = f"{vc.name}:{rel}" if vault else rel
            if not dry_run:
                r = vault_extract_inline_tags(registry, prefixed)
                if not r.startswith("No inline") and not r.startswith("Error"):
                    extracted += 1
            else:
                content = filepath.read_text(encoding="utf-8")
                clean = _strip_code(content)
                inline = re.findall(r"(?:^|\s)#([a-zA-Z][a-zA-Z0-9_/-]*)", clean, re.MULTILINE)
                if inline:
                    extracted += 1
        prefix = "[DRY RUN] " if dry_run else ""
        parts.append(f"{prefix}Inline tags: {extracted} notes with inline tags to extract")

        # 3. Register all frontmatter keys in types.json
        if not dry_run:
            for filepath in _iter_notes(vc.path):
                content = filepath.read_text(encoding="utf-8")
                fm, _ = parse_note(content)
                for key in fm:
                    _ensure_type_registered(vc.path, key)
            parts.append("Types: types.json updated")
        else:
            parts.append("[DRY RUN] Types: would update types.json")

        return "\n".join(parts)
    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------------------------
# Graph Analysis
# ---------------------------------------------------------------------------

def _build_graph(vault_root: Path) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """Build outgoing and incoming link maps for the vault.

    Returns (outgoing, incoming) where both are dict[path, set[path]].
    """
    outgoing: dict[str, set[str]] = defaultdict(set)
    incoming: dict[str, set[str]] = defaultdict(set)
    all_notes = {str(f.relative_to(vault_root)): f for f in _iter_notes(vault_root)}
    note_names = {normalize_note_name(p).lower(): p for p in all_notes}

    for rel_path, filepath in all_notes.items():
        content = filepath.read_text(encoding="utf-8")
        for link in extract_wikilinks(content):
            target_name = normalize_note_name(link).lower()
            target_path = note_names.get(target_name)
            if target_path:
                outgoing[rel_path].add(target_path)
                incoming[target_path].add(rel_path)

    # Ensure all notes are in the maps
    for p in all_notes:
        outgoing.setdefault(p, set())
        incoming.setdefault(p, set())

    return dict(outgoing), dict(incoming)


def vault_graph(registry: VaultRegistry, vault: str = "") -> str:
    """Complete link graph as JSON (nodes + edges)."""
    try:
        vc = _resolve_single_vault(registry, vault)
        vault_root = vc.path
        outgoing, _ = _build_graph(vault_root)

        nodes = []
        edges = []
        for filepath in _iter_notes(vault_root):
            rel = str(filepath.relative_to(vault_root))
            content = filepath.read_text(encoding="utf-8")
            fm, _ = parse_note(content)
            tags = extract_tags(content, fm)
            title = fm.get("title", normalize_note_name(Path(rel).name))
            nodes.append({"path": rel, "title": title, "tags": tags})

        for source, targets in outgoing.items():
            for target in targets:
                edges.append({"source": source, "target": target})

        return json.dumps({"nodes": nodes, "edges": edges}, indent=2, default=str)
    except Exception as e:
        return f"Error: {e}"


def vault_hubs(registry: VaultRegistry, limit: int = 10, vault: str = "") -> str:
    """Notes with the most incoming + outgoing links (the central nodes)."""
    try:
        vc = _resolve_single_vault(registry, vault)
        outgoing, incoming = _build_graph(vc.path)

        scores = {}
        for path in set(list(outgoing.keys()) + list(incoming.keys())):
            scores[path] = len(outgoing.get(path, set())) + len(incoming.get(path, set()))

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        lines = [f"{path} ({score} connections)" for path, score in ranked if score > 0]
        return "\n".join(lines) if lines else "(no hubs)"
    except Exception as e:
        return f"Error: {e}"


def vault_clusters(registry: VaultRegistry, vault: str = "") -> str:
    """Find clusters of connected notes (connected components)."""
    try:
        vc = _resolve_single_vault(registry, vault)
        outgoing, incoming = _build_graph(vc.path)

        all_nodes = set(outgoing.keys()) | set(incoming.keys())
        visited = set()
        clusters = []

        for node in all_nodes:
            if node in visited:
                continue
            # BFS
            cluster = set()
            queue = [node]
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                cluster.add(current)
                for neighbor in outgoing.get(current, set()):
                    if neighbor not in visited:
                        queue.append(neighbor)
                for neighbor in incoming.get(current, set()):
                    if neighbor not in visited:
                        queue.append(neighbor)
            clusters.append(sorted(cluster))

        # Sort clusters by size, largest first
        clusters.sort(key=len, reverse=True)
        lines = []
        for i, cluster in enumerate(clusters):
            summary = f"Cluster {i+1} ({len(cluster)} notes): {', '.join(cluster[:5])}"
            if len(cluster) > 5:
                summary += f" ... +{len(cluster) - 5}"
            lines.append(summary)

        return "\n".join(lines) if lines else "(no clusters)"
    except Exception as e:
        return f"Error: {e}"


def vault_bridges(registry: VaultRegistry, vault: str = "") -> str:
    """Find bridge notes — removal would disconnect clusters."""
    try:
        vc = _resolve_single_vault(registry, vault)
        outgoing, incoming = _build_graph(vc.path)

        # Build undirected adjacency
        adj: dict[str, set[str]] = defaultdict(set)
        for node, targets in outgoing.items():
            for t in targets:
                adj[node].add(t)
                adj[t].add(node)

        all_nodes = list(adj.keys())
        if not all_nodes:
            return "(no bridges)"

        # Count connected components
        def count_components(skip: str) -> int:
            visited = set()
            components = 0
            for start in all_nodes:
                if start == skip or start in visited:
                    continue
                components += 1
                queue = [start]
                while queue:
                    current = queue.pop(0)
                    if current in visited or current == skip:
                        continue
                    visited.add(current)
                    for n in adj.get(current, set()):
                        if n not in visited and n != skip:
                            queue.append(n)
            return components

        base_components = count_components("")
        bridges = []
        for node in all_nodes:
            if len(adj[node]) < 2:
                continue
            if count_components(node) > base_components:
                bridges.append(node)

        return "\n".join(sorted(bridges)) if bridges else "(no bridges)"
    except Exception as e:
        return f"Error: {e}"


def vault_dead_ends(registry: VaultRegistry, vault: str = "") -> str:
    """Notes with outgoing links but no incoming links (not orphans — those have no links at all)."""
    try:
        vc = _resolve_single_vault(registry, vault)
        outgoing, incoming = _build_graph(vc.path)

        dead_ends = []
        for path in outgoing:
            if outgoing[path] and not incoming.get(path, set()):
                dead_ends.append(path)

        return "\n".join(sorted(dead_ends)) if dead_ends else "(no dead ends)"
    except Exception as e:
        return f"Error: {e}"


def vault_shortest_path(registry: VaultRegistry, source: str, target: str, vault: str = "") -> str:
    """Find the shortest link path between two notes. Shows how knowledge connects."""
    try:
        vc_s, rel_s = registry.resolve(source)
        vc_t, rel_t = registry.resolve(target)
        if vc_s.name != vc_t.name:
            return "Error: both notes must be in the same vault"

        vault_root = vc_s.path
        source_path = ensure_md_extension(rel_s)
        target_path = ensure_md_extension(rel_t)

        if not (vault_root / source_path).exists():
            return f"Error: note not found: {source}"
        if not (vault_root / target_path).exists():
            return f"Error: note not found: {target}"

        outgoing, incoming = _build_graph(vault_root)

        # BFS for shortest path (undirected)
        adj: dict[str, set[str]] = defaultdict(set)
        for node, targets in outgoing.items():
            for t in targets:
                adj[node].add(t)
                adj[t].add(node)

        visited = {source_path}
        queue = [(source_path, [source_path])]
        target_normalized = normalize_note_name(target_path).lower()

        while queue:
            current, path = queue.pop(0)
            if normalize_note_name(current).lower() == target_normalized:
                return " -> ".join(normalize_note_name(p) for p in path)
            for neighbor in adj.get(current, set()):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return f"(no path between {source} and {target})"
    except Exception as e:
        return f"Error: {e}"


def vault_tag_graph(registry: VaultRegistry, min_overlap: int = 2, vault: str = "") -> str:
    """Tag co-occurrence graph — which tags appear together and how often.

    Shows implicit topic clusters. min_overlap filters weak connections.
    """
    try:
        vc = _resolve_single_vault(registry, vault)
        # Collect tags per note
        note_tags: list[set[str]] = []
        for filepath in _iter_notes(vc.path):
            content = filepath.read_text(encoding="utf-8")
            fm, _ = parse_note(content)
            tags = set(extract_tags(content, fm))
            if len(tags) >= 2:
                note_tags.append(tags)

        # Count co-occurrences
        cooccurrence: dict[tuple[str, str], int] = defaultdict(int)
        for tags in note_tags:
            tag_list = sorted(tags)
            for i in range(len(tag_list)):
                for j in range(i + 1, len(tag_list)):
                    cooccurrence[(tag_list[i], tag_list[j])] += 1

        # Filter and format
        pairs = [(a, b, count) for (a, b), count in cooccurrence.items() if count >= min_overlap]
        pairs.sort(key=lambda x: x[2], reverse=True)

        if not pairs:
            return "(no tag co-occurrences found)"

        lines = [f"{a} <-> {b} ({count} notes)" for a, b, count in pairs]
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


def vault_isolated(registry: VaultRegistry, vault: str = "") -> str:
    """Find truly isolated notes — no links in, no links out, no embeds. Complete islands."""
    try:
        vc = _resolve_single_vault(registry, vault)
        outgoing, incoming = _build_graph(vc.path)

        isolated = []
        for path in outgoing:
            if not outgoing[path] and not incoming.get(path, set()):
                isolated.append(path)

        return "\n".join(sorted(isolated)) if isolated else "(no isolated notes)"
    except Exception as e:
        return f"Error: {e}"


def vault_tag_overlap(registry: VaultRegistry, tag_a: str, tag_b: str, vault: str = "") -> str:
    """Find notes that have both tags — implicit relationships."""
    try:
        vc = _resolve_single_vault(registry, vault)
        a_clean = tag_a.lstrip("#")
        b_clean = tag_b.lstrip("#")
        results = []

        for filepath in _iter_notes(vc.path):
            content = filepath.read_text(encoding="utf-8")
            fm, _ = parse_note(content)
            tags = extract_tags(content, fm)
            if a_clean in tags and b_clean in tags:
                results.append(str(filepath.relative_to(vc.path)))

        return "\n".join(sorted(results)) if results else "(no overlap)"
    except Exception as e:
        return f"Error: {e}"
