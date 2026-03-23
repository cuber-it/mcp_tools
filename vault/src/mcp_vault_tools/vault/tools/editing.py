"""Single-note editing operations — insert, split, merge."""

from __future__ import annotations

import re
from pathlib import Path

from ..parser import ensure_md_extension, normalize_note_name, parse_note, rebuild_note
from ..registry import VaultRegistry
from ._helpers import resolve
from .crud import vault_write
from .refactoring import _update_links_in_vault


def vault_insert_at(registry: VaultRegistry, path: str, heading: str,
                    content: str, position: str = "append") -> str:
    """Insert content under a specific heading.

    position: 'append' (end of section), 'prepend' (start of section),
    'replace' (replace section content).
    """
    try:
        vault_root, filepath = resolve(registry, path)
        if not filepath.exists():
            return f"Error: note not found: {path}"

        file_content = filepath.read_text(encoding="utf-8")
        fm, body = parse_note(file_content)
        lines = body.split("\n")

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

        section_end = len(lines)
        for i in range(heading_idx + 1, len(lines)):
            match = re.match(r"^(#{1,6})\s+", lines[i])
            if match and len(match.group(1)) <= heading_level:
                section_end = i
                break

        if position == "append":
            insert_idx = section_end
            while insert_idx > heading_idx + 1 and not lines[insert_idx - 1].strip():
                insert_idx -= 1
            lines.insert(insert_idx, "\n" + content)
        elif position == "prepend":
            lines.insert(heading_idx + 1, "\n" + content)
        elif position == "replace":
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

        section_end = len(lines)
        for i in range(heading_idx + 1, len(lines)):
            match = re.match(r"^(#{1,6})\s+", lines[i])
            if match and len(match.group(1)) <= heading_level:
                section_end = i
                break

        section_lines = lines[heading_idx + 1:section_end]
        section_body = "\n".join(section_lines).strip()

        new_name = re.sub(r"[^\w\s-]", "", heading_clean).strip().replace(" ", "-").lower()
        new_rel = str(Path(rel).parent / new_name) if "/" in rel else new_name
        new_fm = {"title": heading_clean}
        if fm.get("tags"):
            new_fm["tags"] = fm["tags"]

        new_path = f"{vc.name}:{new_rel}" if ":" in path else new_rel
        vault_write(registry, new_path, rebuild_note(new_fm, section_body))

        link_line = f"See [[{new_name}]]"
        lines[heading_idx + 1:section_end] = ["\n" + link_line + "\n"]
        new_body = "\n".join(lines)
        filepath.write_text(rebuild_note(fm, new_body), encoding="utf-8")

        return f"Split '{heading}' from {path} -> {new_path}"
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

        merged_fm = {**fm_b, **fm_a}
        tags_a = set(fm_a.get("tags", []) if isinstance(fm_a.get("tags"), list) else [])
        tags_b = set(fm_b.get("tags", []) if isinstance(fm_b.get("tags"), list) else [])
        if tags_a or tags_b:
            merged_fm["tags"] = sorted(tags_a | tags_b)

        merged_body = (
            body_a.rstrip()
            + f"\n\n---\n\n*Merged from [[{normalize_note_name(rel_b)}]]*\n\n"
            + body_b
        )

        target_path = target or path_a
        _, target_file = resolve(registry, target_path)
        target_file.write_text(rebuild_note(merged_fm, merged_body), encoding="utf-8")

        if target_path != path_b:
            _, target_rel = registry.resolve(target_path)
            _update_links_in_vault(vc_a.path, rel_b, target_rel)

        if target_path != path_b:
            file_b.unlink()

        return f"Merged {path_a} + {path_b} -> {target_path}"
    except Exception as e:
        return f"Error: {e}"
