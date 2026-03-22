"""MCP wiring for vault tools — register all tools with the MCP server."""

from __future__ import annotations

from .registry import VaultRegistry
from . import tools


def register(mcp, config: dict) -> None:
    """Register vault tools as MCP tools."""
    registry = VaultRegistry(config)

    # --- CRUD Primitives ---

    @mcp.tool()
    def vault_read(path: str) -> str:
        """Read a note from the vault (returns frontmatter + body)."""
        return tools.vault_read(registry, path)

    @mcp.tool()
    def vault_write(path: str, content: str) -> str:
        """Write or overwrite a note in the vault."""
        return tools.vault_write(registry, path, content)

    @mcp.tool()
    def vault_append(path: str, content: str) -> str:
        """Append text to an existing note."""
        return tools.vault_append(registry, path, content)

    @mcp.tool()
    def vault_prepend(path: str, content: str) -> str:
        """Prepend text to a note's body (after frontmatter, before existing content)."""
        return tools.vault_prepend(registry, path, content)

    @mcp.tool()
    def vault_delete(path: str) -> str:
        """Delete a note from the vault."""
        return tools.vault_delete(registry, path)

    @mcp.tool()
    def vault_list(path: str = "", recursive: bool = False) -> str:
        """List notes in a folder. Use prefix for vault (e.g. 'arbeit:projects/')."""
        return tools.vault_list(registry, path, recursive)

    @mcp.tool()
    def vault_exists(path: str) -> str:
        """Check if a note exists."""
        return tools.vault_exists(registry, path)

    @mcp.tool()
    def vault_headings(path: str) -> str:
        """List all headings in a note. Useful before vault_insert_at or vault_split."""
        return tools.vault_headings(registry, path)

    # --- Search ---

    @mcp.tool()
    def vault_search(query: str, vault: str = "", limit: int = 0,
                     regex: bool = False, ignore_case: bool = True) -> str:
        """Full-text search across notes. Use vault='*' for all vaults. regex=True for regex patterns."""
        return tools.vault_search(registry, query, vault, limit, regex, ignore_case)

    @mcp.tool()
    def vault_search_tag(tag: str, vault: str = "") -> str:
        """Find notes with a specific tag."""
        return tools.vault_search_tag(registry, tag, vault)

    @mcp.tool()
    def vault_search_frontmatter(key: str, value: str, vault: str = "") -> str:
        """Find notes by frontmatter field value."""
        return tools.vault_search_frontmatter(registry, key, value, vault)

    # --- Links ---

    @mcp.tool()
    def vault_links(path: str) -> str:
        """Get all outgoing links and embeds from a note."""
        return tools.vault_links(registry, path)

    @mcp.tool()
    def vault_backlinks(path: str) -> str:
        """Find all notes that link to a given note (supports aliases)."""
        return tools.vault_backlinks(registry, path)

    @mcp.tool()
    def vault_related(path: str, depth: int = 1) -> str:
        """Find related notes via link traversal."""
        return tools.vault_related(registry, path, depth)

    @mcp.tool()
    def vault_orphans(vault: str = "") -> str:
        """Find notes with no incoming links."""
        return tools.vault_orphans(registry, vault)

    # --- Tags ---

    @mcp.tool()
    def vault_tag_list(vault: str = "") -> str:
        """List all tags used across the vault with counts."""
        return tools.vault_tag_list(registry, vault)

    # --- Frontmatter ---

    @mcp.tool()
    def vault_get_frontmatter(path: str) -> str:
        """Read YAML frontmatter of a note as JSON."""
        return tools.vault_get_frontmatter(registry, path)

    @mcp.tool()
    def vault_set_frontmatter(path: str, key: str, value: str) -> str:
        """Set or update a frontmatter field."""
        return tools.vault_set_frontmatter(registry, path, key, value)

    @mcp.tool()
    def vault_add_tag(path: str, tag: str) -> str:
        """Add a tag to a note's frontmatter."""
        return tools.vault_add_tag(registry, path, tag)

    @mcp.tool()
    def vault_get_types(vault: str = "") -> str:
        """Read .obsidian/types.json — Obsidian's frontmatter type definitions."""
        return tools.vault_get_types(registry, vault)

    @mcp.tool()
    def vault_set_type(key: str, type_hint: str, vault: str = "") -> str:
        """Set a frontmatter field type in types.json. Types: text, number, date, datetime, checkbox, multitext."""
        return tools.vault_set_type(registry, key, type_hint, vault)

    @mcp.tool()
    def vault_remove_tag(path: str, tag: str) -> str:
        """Remove a tag from a note's frontmatter."""
        return tools.vault_remove_tag(registry, path, tag)

    @mcp.tool()
    def vault_remove_frontmatter(path: str, key: str) -> str:
        """Remove a frontmatter field from a note."""
        return tools.vault_remove_frontmatter(registry, path, key)

    # --- Rename / Move ---

    @mcp.tool()
    def vault_rename(old_path: str, new_path: str) -> str:
        """Rename a note and update all links pointing to it."""
        return tools.vault_rename(registry, old_path, new_path)

    @mcp.tool()
    def vault_move(path: str, target_folder: str) -> str:
        """Move a note to a different folder and update all links."""
        return tools.vault_move(registry, path, target_folder)

    # --- Refactoring ---

    @mcp.tool()
    def vault_tag_rename(old_tag: str, new_tag: str, vault: str = "", dry_run: bool = False) -> str:
        """Rename a tag across the vault. dry_run=True to preview."""
        return tools.vault_tag_rename(registry, old_tag, new_tag, vault, dry_run)

    @mcp.tool()
    def vault_tag_merge(tags: list[str], target_tag: str, vault: str = "") -> str:
        """Merge multiple tags into one."""
        return tools.vault_tag_merge(registry, tags, target_tag, vault)

    @mcp.tool()
    def vault_bulk_frontmatter(key: str, value: str, filter_tag: str = "",
                               vault: str = "", dry_run: bool = False) -> str:
        """Set a frontmatter field in many notes. dry_run=True to preview."""
        return tools.vault_bulk_frontmatter(
            registry, key, value, filter_tag, vault, dry_run
        )

    @mcp.tool()
    def vault_broken_links(vault: str = "") -> str:
        """Find all broken links (targets that don't exist)."""
        return tools.vault_broken_links(registry, vault)

    # --- Analysis ---

    @mcp.tool()
    def vault_stats(vault: str = "") -> str:
        """Vault statistics: notes, tags, links, orphans."""
        return tools.vault_stats(registry, vault)

    @mcp.tool()
    def vault_recent(limit: int = 10, vault: str = "") -> str:
        """List recently modified notes."""
        return tools.vault_recent(registry, limit, vault)

    @mcp.tool()
    def vault_health(vault: str = "") -> str:
        """Vault health report: stats + orphans + broken links + tags."""
        return tools.vault_health(registry, vault)

    # --- Convenience (new) ---

    @mcp.tool()
    def vault_create(path: str, title: str = "", tags: list[str] | None = None,
                     body: str = "", extra_frontmatter: dict | None = None) -> str:
        """Create a note with structured parameters. No raw markdown needed."""
        return tools.vault_create(registry, path, title, tags, body, extra_frontmatter)

    @mcp.tool()
    def vault_find(query: str, vault: str = "", limit: int = 0) -> str:
        """Unified search. '#tag' searches tags, 'key:value' searches frontmatter, anything else searches everything."""
        return tools.vault_find(registry, query, vault, limit)

    @mcp.tool()
    def vault_summary(path: str, recursive: bool = False) -> str:
        """Quick overview: title + tags + preview. Works for single notes and folders."""
        return tools.vault_summary(registry, path, recursive)

    @mcp.tool()
    def vault_tree(vault: str = "", max_depth: int = 3) -> str:
        """Visual tree of the vault structure."""
        return tools.vault_tree(registry, vault, max_depth)

    @mcp.tool()
    def vault_copy(source: str, target: str) -> str:
        """Duplicate a note (preserves frontmatter)."""
        return tools.vault_copy(registry, source, target)

    @mcp.tool()
    def vault_frontmatter_keys(vault: str = "") -> str:
        """List all frontmatter keys used across the vault with frequency."""
        return tools.vault_frontmatter_keys(registry, vault)

    # --- Advanced Editing ---

    @mcp.tool()
    def vault_replace(query: str, replacement: str, vault: str = "",
                      dry_run: bool = False, ignore_case: bool = False, regex: bool = False) -> str:
        """Find and replace text across the vault. dry_run=True to preview. regex=True for regex patterns."""
        return tools.vault_replace(registry, query, replacement, vault, dry_run, ignore_case, regex)

    @mcp.tool()
    def vault_insert_at(path: str, heading: str, content: str, position: str = "append") -> str:
        """Insert content under a specific heading. Position: 'append', 'prepend', or 'replace'."""
        return tools.vault_insert_at(registry, path, heading, content, position)

    @mcp.tool()
    def vault_split(path: str, heading: str) -> str:
        """Split a note at a heading — extracts section into a new linked note."""
        return tools.vault_split(registry, path, heading)

    # --- Connection Discovery ---

    @mcp.tool()
    def vault_unlinked_mentions(path: str) -> str:
        """Find notes that mention this note's name but don't link to it."""
        return tools.vault_unlinked_mentions(registry, path)

    @mcp.tool()
    def vault_link_suggest(path: str, limit: int = 10) -> str:
        """Suggest notes that should be linked — based on shared tags."""
        return tools.vault_link_suggest(registry, path, limit)

    # --- Changelog ---

    @mcp.tool()
    def vault_changelog(days: int = 7, vault: str = "") -> str:
        """Recent changes grouped by day."""
        return tools.vault_changelog(registry, days, vault)

    # --- Convenience (original) ---

    @mcp.tool()
    def vault_daily(day: str = "", vault: str = "") -> str:
        """Create or read a daily note."""
        return tools.vault_daily(registry, day, vault)

    @mcp.tool()
    def vault_inbox(content: str, vault: str = "") -> str:
        """Quick-capture: append content to the inbox note."""
        return tools.vault_inbox(registry, content, vault)

    @mcp.tool()
    def vault_merge(path_a: str, path_b: str, target: str = "") -> str:
        """Merge two notes into one. Updates backlinks."""
        return tools.vault_merge(registry, path_a, path_b, target)

    @mcp.tool()
    def vault_from_template(template: str, target: str, variables: dict | None = None) -> str:
        """Create a note from a template with {{variable}} substitution."""
        return tools.vault_from_template(registry, template, target, variables)

    # --- Multi-Vault ---

    @mcp.tool()
    def vault_list_vaults() -> str:
        """List all configured vaults with name, path, and note count."""
        return tools.vault_list_vaults(registry)

    # --- Composite Operations ---

    @mcp.tool()
    def vault_link_mentions(path: str, dry_run: bool = False) -> str:
        """Auto-link all unlinked mentions of a note across the vault."""
        return tools.vault_link_mentions(registry, path, dry_run)

    @mcp.tool()
    def vault_archive(days: int = 90, archive_folder: str = "archive",
                      vault: str = "", dry_run: bool = False) -> str:
        """Move notes older than N days to archive folder. Updates links."""
        return tools.vault_archive(registry, days, archive_folder, vault, dry_run)

    @mcp.tool()
    def vault_extract_inline_tags(path: str) -> str:
        """Move inline #tags to frontmatter and remove from body."""
        return tools.vault_extract_inline_tags(registry, path)

    @mcp.tool()
    def vault_backfill_titles(vault: str = "", dry_run: bool = False) -> str:
        """Add title to frontmatter for all notes that don't have one."""
        return tools.vault_backfill_titles(registry, vault, dry_run)

    @mcp.tool()
    def vault_standardize(vault: str = "", dry_run: bool = False) -> str:
        """Standardize the vault: backfill titles, extract inline tags, register types."""
        return tools.vault_standardize(registry, vault, dry_run)

    # --- Graph Analysis ---

    @mcp.tool()
    def vault_graph(vault: str = "") -> str:
        """Complete link graph as JSON (nodes + edges)."""
        return tools.vault_graph(registry, vault)

    @mcp.tool()
    def vault_hubs(limit: int = 10, vault: str = "") -> str:
        """Notes with the most connections (the central nodes)."""
        return tools.vault_hubs(registry, limit, vault)

    @mcp.tool()
    def vault_clusters(vault: str = "") -> str:
        """Find clusters of connected notes."""
        return tools.vault_clusters(registry, vault)

    @mcp.tool()
    def vault_bridges(vault: str = "") -> str:
        """Find bridge notes — removal would disconnect clusters."""
        return tools.vault_bridges(registry, vault)

    @mcp.tool()
    def vault_dead_ends(vault: str = "") -> str:
        """Notes with outgoing links but no incoming links."""
        return tools.vault_dead_ends(registry, vault)

    @mcp.tool()
    def vault_shortest_path(source: str, target: str, vault: str = "") -> str:
        """Find the shortest link path between two notes."""
        return tools.vault_shortest_path(registry, source, target, vault)

    @mcp.tool()
    def vault_tag_graph(min_overlap: int = 2, vault: str = "") -> str:
        """Tag co-occurrence graph — which tags appear together. Shows topic clusters."""
        return tools.vault_tag_graph(registry, min_overlap, vault)

    @mcp.tool()
    def vault_isolated(vault: str = "") -> str:
        """Find truly isolated notes — no links in, no links out."""
        return tools.vault_isolated(registry, vault)

    @mcp.tool()
    def vault_tag_overlap(tag_a: str, tag_b: str, vault: str = "") -> str:
        """Find notes that have both tags — implicit relationships."""
        return tools.vault_tag_overlap(registry, tag_a, tag_b, vault)
