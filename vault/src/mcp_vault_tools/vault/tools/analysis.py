"""Analysis, changelog, convenience, daily/capture, and multi-vault operations."""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

from ..parser import (
    ensure_md_extension,
    extract_tags,
    extract_wikilinks,
    normalize_note_name,
    parse_note,
    rebuild_note,
)
from ..registry import VaultRegistry
from ._helpers import iter_notes, resolve, resolve_single_vault
from .crud import vault_write


def vault_stats(registry: VaultRegistry, vault: str = "") -> str:
    """Vault statistics: notes, tags, links, orphans."""
    try:
        vc = resolve_single_vault(registry, vault)
        vault_root = vc.path
        notes = iter_notes(vault_root)
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
        vc = resolve_single_vault(registry, vault)
        notes = iter_notes(vc.path)
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
        from .refactoring import vault_broken_links
        from .frontmatter import vault_tag_list
        from .links import vault_orphans

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


def vault_changelog(registry: VaultRegistry, days: int = 7, vault: str = "") -> str:
    """Recent changes grouped by day."""
    try:
        vc = resolve_single_vault(registry, vault)
        notes = iter_notes(vc.path)
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
        notes = iter_notes(vc.path, folder, recursive)
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
        vc = resolve_single_vault(registry, vault)
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
                connector = "\u2514\u2500\u2500 " if is_last else "\u251c\u2500\u2500 "
                if entry.is_dir():
                    count = len(list(entry.rglob("*.md")))
                    lines.append(f"{prefix}{connector}{entry.name}/ ({count})")
                    extension = "    " if is_last else "\u2502   "
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
        _, source_file = resolve(registry, source)
        if not source_file.exists():
            return f"Error: note not found: {source}"
        content = source_file.read_text(encoding="utf-8")
        return vault_write(registry, target, content)
    except Exception as e:
        return f"Error: {e}"


def vault_frontmatter_keys(registry: VaultRegistry, vault: str = "") -> str:
    """List all frontmatter keys used across the vault with frequency."""
    try:
        vc = resolve_single_vault(registry, vault)
        key_counts: dict[str, int] = defaultdict(int)

        for filepath in iter_notes(vc.path):
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


def vault_daily(registry: VaultRegistry, day: str = "", vault: str = "") -> str:
    """Create or read a daily note. Format from config."""
    try:
        vc = resolve_single_vault(registry, vault)
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
        vc = resolve_single_vault(registry, vault)
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


def vault_list_vaults(registry: VaultRegistry) -> str:
    """List all configured vaults with name, path, and note count."""
    try:
        vaults = registry.list_vaults()
        if not vaults:
            return "(no vaults configured)"
        lines = []
        for vc in vaults:
            count = len(iter_notes(vc.path))
            default = " (default)" if vc.name == registry.default_name else ""
            lines.append(f"{vc.name}{default}: {vc.path} ({count} notes)")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"
