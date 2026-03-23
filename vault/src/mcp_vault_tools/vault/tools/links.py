"""Link operations: outgoing, backlinks, related, orphans."""
from __future__ import annotations

from ..parser import (
    ensure_md_extension,
    extract_links,
    extract_wikilinks,
    normalize_note_name,
    parse_note,
)
from ..registry import VaultRegistry
from ._helpers import iter_notes, resolve, resolve_single_vault


def vault_links(registry: VaultRegistry, path: str) -> str:
    """Get all outgoing links from a note (links and embeds separated)."""
    try:
        vault_root, filepath = resolve(registry, path)
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
        for filepath in iter_notes(vc.path):
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
        vc = resolve_single_vault(registry, vault)
        vault_root = vc.path
        all_notes = {str(f.relative_to(vault_root)) for f in iter_notes(vault_root)}
        linked = set()

        for filepath in iter_notes(vault_root):
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
