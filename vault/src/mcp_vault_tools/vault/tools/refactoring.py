"""Vault-wide refactoring operations — rename, move, replace, tag management."""

from __future__ import annotations

import re
from pathlib import Path

from ..parser import (
    ensure_md_extension,
    extract_links,
    extract_tags,
    normalize_note_name,
    parse_note,
    rebuild_note,
)
from ..registry import VaultRegistry
from ._helpers import iter_notes, logger, resolve_single_vault


def _update_links_in_vault(vault_root: Path, old_name: str, new_name: str) -> int:
    """Update all WikiLinks pointing to old_name to point to new_name.

    Returns number of files modified.
    """
    old_normalized = normalize_note_name(old_name).lower()
    modified = 0
    for filepath in vault_root.rglob("*.md"):
        content = filepath.read_text(encoding="utf-8")
        new_content = content

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


def vault_tag_rename(registry: VaultRegistry, old_tag: str, new_tag: str,
                     vault: str = "", dry_run: bool = False) -> str:
    """Rename a tag across the entire vault (frontmatter + inline).

    dry_run=True shows what would change without modifying files.
    """
    try:
        vc = resolve_single_vault(registry, vault)
        old_clean = old_tag.lstrip("#")
        new_clean = new_tag.lstrip("#")
        modified = 0
        preview_lines = []

        for filepath in iter_notes(vc.path):
            content = filepath.read_text(encoding="utf-8")
            fm, body = parse_note(content)

            fm_changed = False
            tags = fm.get("tags", [])
            if isinstance(tags, list) and old_clean in tags:
                tags = [new_clean if t == old_clean else t for t in tags]
                fm["tags"] = tags
                fm_changed = True

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
        vc = resolve_single_vault(registry, vault)
        modified = 0
        filter_clean = filter_tag.lstrip("#") if filter_tag else ""
        preview_lines = []

        for filepath in iter_notes(vc.path):
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
        vc = resolve_single_vault(registry, vault)
        vault_root = vc.path
        all_notes = {
            normalize_note_name(str(f.relative_to(vault_root))).lower()
            for f in iter_notes(vault_root)
        }
        broken = []

        for filepath in iter_notes(vault_root):
            content = filepath.read_text(encoding="utf-8")
            for link in extract_links(content):
                if link.is_embed and not link.target.endswith(".md"):
                    continue
                target = normalize_note_name(link.target).lower()
                if target not in all_notes:
                    rel = str(filepath.relative_to(vault_root))
                    broken.append(f"{rel} -> [[{link.target}]]")

        return "\n".join(sorted(broken)) if broken else "(no broken links)"
    except Exception as e:
        return f"Error: {e}"


def vault_replace(registry: VaultRegistry, query: str, replacement: str,
                  vault: str = "", dry_run: bool = False, ignore_case: bool = False,
                  regex: bool = False) -> str:
    """Find and replace text across the entire vault.

    dry_run=True shows what would change without modifying files.
    ignore_case=True for case-insensitive matching.
    regex=True to use query as a regular expression.
    """
    try:
        vc = resolve_single_vault(registry, vault)
        flags = re.IGNORECASE if ignore_case else 0
        pattern = re.compile(query if regex else re.escape(query), flags)
        modified = 0
        total_replacements = 0
        preview_lines = []

        for filepath in iter_notes(vc.path):
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
        result = (
            f"{prefix}Replaced '{query}' -> '{replacement}': "
            f"{total_replacements} occurrences in {modified} notes"
        )
        if dry_run and preview_lines:
            result += "\n" + "\n".join(preview_lines)
        return result
    except Exception as e:
        return f"Error: {e}"
