"""Vault tool implementations — headless Obsidian-compatible vault operations.

Split into modules by domain. All public functions are re-exported here
so that `from mcp_vault_tools.vault import tools; tools.vault_read(...)` keeps working.
"""

from .crud import (
    vault_append,
    vault_create,
    vault_delete,
    vault_exists,
    vault_headings,
    vault_list,
    vault_prepend,
    vault_read,
    vault_write,
)
from .search import (
    vault_find,
    vault_query,
    vault_search,
    vault_search_frontmatter,
    vault_search_tag,
)
from .links import (
    vault_backlinks,
    vault_links,
    vault_orphans,
    vault_related,
)
from .frontmatter import (
    vault_add_tag,
    vault_get_frontmatter,
    vault_get_types,
    vault_remove_frontmatter,
    vault_remove_tag,
    vault_set_frontmatter,
    vault_set_type,
    vault_tag_list,
)
from .refactoring import (
    vault_broken_links,
    vault_bulk_frontmatter,
    vault_move,
    vault_rename,
    vault_replace,
    vault_tag_merge,
    vault_tag_rename,
)
from .editing import (
    vault_insert_at,
    vault_merge,
    vault_split,
)
from .analysis import (
    vault_changelog,
    vault_copy,
    vault_daily,
    vault_from_template,
    vault_frontmatter_keys,
    vault_health,
    vault_inbox,
    vault_list_vaults,
    vault_recent,
    vault_stats,
    vault_summary,
    vault_tree,
)
from .graph import (
    vault_bridges,
    vault_clusters,
    vault_dead_ends,
    vault_graph,
    vault_hubs,
    vault_isolated,
    vault_shortest_path,
    vault_tag_graph,
    vault_tag_overlap,
)
from .composites import (
    vault_archive,
    vault_backfill_titles,
    vault_extract_inline_tags,
    vault_link_mentions,
    vault_link_suggest,
    vault_standardize,
    vault_unlinked_mentions,
)

__all__ = [
    # CRUD
    "vault_read", "vault_write", "vault_create", "vault_append", "vault_prepend",
    "vault_delete", "vault_list", "vault_exists", "vault_headings",
    # Search
    "vault_search", "vault_search_tag", "vault_search_frontmatter", "vault_find", "vault_query",
    # Links
    "vault_links", "vault_backlinks", "vault_related", "vault_orphans",
    # Frontmatter & Tags
    "vault_tag_list", "vault_get_frontmatter", "vault_set_frontmatter",
    "vault_add_tag", "vault_remove_tag", "vault_remove_frontmatter",
    "vault_get_types", "vault_set_type",
    # Editing & Refactoring
    "vault_rename", "vault_move", "vault_replace", "vault_insert_at", "vault_split",
    "vault_tag_rename", "vault_tag_merge", "vault_bulk_frontmatter",
    "vault_broken_links", "vault_merge",
    # Analysis & Convenience
    "vault_stats", "vault_recent", "vault_health", "vault_changelog",
    "vault_summary", "vault_tree", "vault_copy", "vault_frontmatter_keys",
    "vault_daily", "vault_inbox", "vault_from_template", "vault_list_vaults",
    # Connection Discovery & Composites
    "vault_unlinked_mentions", "vault_link_suggest",
    "vault_link_mentions", "vault_archive", "vault_extract_inline_tags",
    "vault_backfill_titles", "vault_standardize",
    # Graph
    "vault_graph", "vault_hubs", "vault_clusters", "vault_bridges",
    "vault_dead_ends", "vault_isolated", "vault_shortest_path",
    "vault_tag_graph", "vault_tag_overlap",
]
