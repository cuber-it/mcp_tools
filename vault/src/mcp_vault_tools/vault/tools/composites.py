"""Composite operations: link mentions, archive, extract tags, backfill, standardize."""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from ..parser import (
    _strip_code,
    ensure_md_extension,
    extract_wikilinks,
    normalize_note_name,
    parse_note,
    rebuild_note,
)
from ..registry import VaultRegistry
from ._helpers import iter_notes, logger, resolve, resolve_single_vault
from .editing import _update_links_in_vault
from .frontmatter import _ensure_type_registered


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

        for filepath in iter_notes(vault_root):
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
        vc = resolve_single_vault(registry, vault)
        vault_root = vc.path
        cutoff = datetime.now().timestamp() - (days * 86400)
        moved = 0
        preview_lines = []

        for filepath in iter_notes(vault_root):
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
        vault_root, filepath = resolve(registry, path)
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
        vc = resolve_single_vault(registry, vault)
        modified = 0
        preview_lines = []

        for filepath in iter_notes(vc.path):
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
        vc = resolve_single_vault(registry, vault)
        extracted = 0
        for filepath in iter_notes(vc.path):
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
            for filepath in iter_notes(vc.path):
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
        for filepath in iter_notes(vault_root):
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
    """Suggest notes that should be linked -- based on shared tags and related content."""
    try:
        from ..parser import extract_tags

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

        for other_file in iter_notes(vault_root):
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
