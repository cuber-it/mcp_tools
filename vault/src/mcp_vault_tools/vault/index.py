"""In-memory vault index — caches frontmatter, tags, and links per note.

Rebuilt on first access, refreshed via mtime check on subsequent calls.
No persistence, no SQLite, no sync problems. Dies with the process.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

from .parser import extract_links, extract_tags, extract_wikilinks, normalize_note_name, parse_note

logger = logging.getLogger(__name__)


@dataclass
class NoteEntry:
    """Cached metadata for a single note."""
    path: str
    mtime: float
    size: int
    frontmatter: dict
    tags: list[str]
    outgoing_links: list[str]
    incoming_links: list[str] = field(default_factory=list)


class VaultIndex:
    """In-memory index over a vault directory.

    Caches frontmatter, tags, and link structure.
    Refreshes automatically via mtime comparison.
    """

    def __init__(self, vault_root: Path):
        self._root = vault_root
        self._entries: dict[str, NoteEntry] = {}
        self._built = False

    def _scan_note(self, filepath: Path) -> NoteEntry:
        """Parse a single note and return its cached entry."""
        stat = filepath.stat()
        content = filepath.read_text(encoding="utf-8")
        fm, body = parse_note(content)
        tags = extract_tags(content, fm)
        links = [normalize_note_name(lnk).lower() for lnk in extract_wikilinks(content)]
        return NoteEntry(
            path=str(filepath.relative_to(self._root)),
            mtime=stat.st_mtime,
            size=stat.st_size,
            frontmatter=fm,
            tags=tags,
            outgoing_links=links,
        )

    def _rebuild_incoming(self) -> None:
        """Rebuild incoming link index from outgoing links."""
        note_names = {normalize_note_name(p).lower(): p for p in self._entries}
        for entry in self._entries.values():
            entry.incoming_links = []
        for entry in self._entries.values():
            for link in entry.outgoing_links:
                target = note_names.get(link)
                if target and target in self._entries:
                    self._entries[target].incoming_links.append(entry.path)

    def build(self) -> int:
        """Full rebuild of the index. Returns number of notes indexed."""
        self._entries.clear()
        for filepath in sorted(self._root.rglob("*.md")):
            if filepath.name.startswith("."):
                continue
            try:
                filepath.relative_to(self._root / ".obsidian")
                continue
            except ValueError:
                pass
            try:
                entry = self._scan_note(filepath)
                self._entries[entry.path] = entry
            except Exception as e:
                logger.warning("Index skip %s: %s", filepath, e)
        self._rebuild_incoming()
        self._built = True
        logger.info("VaultIndex built: %d notes", len(self._entries))
        return len(self._entries)

    def refresh(self) -> int:
        """Delta refresh — only re-parse changed/new files, remove deleted.

        Returns number of notes updated.
        """
        if not self._built:
            return self.build()

        current_files = {}
        for filepath in self._root.rglob("*.md"):
            if filepath.name.startswith("."):
                continue
            try:
                filepath.relative_to(self._root / ".obsidian")
                continue
            except ValueError:
                pass
            rel = str(filepath.relative_to(self._root))
            current_files[rel] = filepath

        updated = 0

        # Remove deleted
        deleted = set(self._entries.keys()) - set(current_files.keys())
        for path in deleted:
            del self._entries[path]
            updated += 1

        # Add new / update changed
        for rel, filepath in current_files.items():
            stat = filepath.stat()
            existing = self._entries.get(rel)
            if existing and existing.mtime == stat.st_mtime and existing.size == stat.st_size:
                continue
            try:
                entry = self._scan_note(filepath)
                self._entries[entry.path] = entry
                updated += 1
            except Exception as e:
                logger.warning("Index refresh skip %s: %s", filepath, e)

        if updated > 0:
            self._rebuild_incoming()
            logger.info("VaultIndex refreshed: %d updates", updated)

        return updated

    def ensure_fresh(self) -> None:
        """Ensure index is built and up to date."""
        if not self._built:
            self.build()
        else:
            self.refresh()

    def get(self, path: str) -> NoteEntry | None:
        """Get cached entry for a note path."""
        self.ensure_fresh()
        return self._entries.get(path)

    def all_entries(self) -> list[NoteEntry]:
        """All cached entries, refreshed."""
        self.ensure_fresh()
        return list(self._entries.values())

    def query(
        self,
        from_folder: str = "",
        where: dict | None = None,
        tags: list[str] | None = None,
        sort: str = "",
        fields: list[str] | None = None,
        limit: int = 0,
        descending: bool = False,
    ) -> list[dict]:
        """Query the index with combined filters.

        from_folder: restrict to a subfolder
        where: frontmatter key-value filters (AND)
        tags: all must be present
        sort: frontmatter field or 'name'/'modified'
        fields: which frontmatter fields to return (empty = path only)
        """
        self.ensure_fresh()
        results = []

        for entry in self._entries.values():
            # Folder filter
            if from_folder and not entry.path.startswith(from_folder):
                continue

            # Frontmatter filter
            if where:
                match = True
                for key, value in where.items():
                    fm_val = entry.frontmatter.get(key)
                    if fm_val is None or str(fm_val) != str(value):
                        match = False
                        break
                if not match:
                    continue

            # Tag filter
            if tags:
                if not all(t.lstrip("#") in entry.tags for t in tags):
                    continue

            results.append(entry)

        # Sort
        if sort:
            if sort == "modified":
                results.sort(key=lambda e: e.mtime, reverse=descending)
            elif sort == "name":
                results.sort(key=lambda e: e.path, reverse=descending)
            else:
                def sort_key(e):
                    val = e.frontmatter.get(sort, "")
                    return str(val) if val is not None else ""
                results.sort(key=sort_key, reverse=descending)

        # Limit
        if limit:
            results = results[:limit]

        # Format output
        if fields:
            return [
                {"path": e.path, **{f: e.frontmatter.get(f, "") for f in fields}}
                for e in results
            ]
        return [{"path": e.path} for e in results]

    @property
    def note_count(self) -> int:
        return len(self._entries)

    @property
    def outgoing_map(self) -> dict[str, list[str]]:
        """Outgoing links per note — for graph tools."""
        self.ensure_fresh()
        return {e.path: e.outgoing_links for e in self._entries.values()}

    @property
    def incoming_map(self) -> dict[str, list[str]]:
        """Incoming links per note — for graph tools."""
        self.ensure_fresh()
        return {e.path: e.incoming_links for e in self._entries.values()}

    @property
    def tag_index(self) -> dict[str, list[str]]:
        """Tag to note paths mapping."""
        self.ensure_fresh()
        result: dict[str, list[str]] = {}
        for entry in self._entries.values():
            for tag in entry.tags:
                result.setdefault(tag, []).append(entry.path)
        return result
