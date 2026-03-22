# Vault Tools — Usage Guide for LLMs

You have access to 63 vault tools for managing Obsidian-compatible Markdown vaults. Here's how to use them effectively.

## Core Concepts

**Multi-Vault**: Paths use prefix syntax. `"note.md"` = default vault. `"work:note.md"` = specific vault. `"*:query"` = all vaults. The `.md` extension is optional.

**Dual output**: Most tools return plain text. `vault_read`, `vault_stats`, `vault_summary`, `vault_graph` return JSON.

**Dry-run**: Destructive operations (replace, tag_rename, bulk_frontmatter, archive, backfill_titles, standardize, link_mentions) support `dry_run=True`. Always preview first for vault-wide changes.

## Decision Guide

### Creating notes

- **Structured content** → `vault_create(path, title=, tags=, body=)` — the default choice
- **Raw markdown** → `vault_write(path, content)` — when you have pre-formatted content
- **From template** → `vault_from_template(template, target, variables=)` — for recurring note types
- **Quick capture** → `vault_inbox(content)` — timestamped entry to inbox
- **Daily note** → `vault_daily()` — date-based note

### Finding notes

- **General search** → `vault_find(query)` — start here, auto-detects query type
- **By tag** → `vault_find("#tag")` or `vault_search_tag(tag)`
- **By field** → `vault_find("type:fact")` or `vault_search_frontmatter(key, value)`
- **Regex** → `vault_search(pattern, regex=True)`
- **Cross-vault** → any search with `vault="*"`

### Reading notes

- **Full content** → `vault_read(path)` — returns frontmatter + body as JSON
- **Quick overview** → `vault_summary(path)` — title + tags + preview
- **Folder overview** → `vault_summary("folder/", recursive=True)`
- **Structure** → `vault_headings(path)` — before insert_at or split
- **Vault overview** → `vault_tree()` — directory structure

### Editing notes

- **Add to end** → `vault_append(path, content)`
- **Add to start** → `vault_prepend(path, content)`
- **Under a heading** → `vault_insert_at(path, heading, content)` — use vault_headings first
- **Replace section** → `vault_insert_at(path, heading, content, position="replace")`
- **Find & replace** → `vault_replace(query, replacement, dry_run=True)`

### Organizing notes

- **Rename** → `vault_rename(old, new)` — updates all links
- **Move** → `vault_move(path, folder)` — updates all links
- **Copy** → `vault_copy(source, target)`
- **Merge** → `vault_merge(a, b)` — combines content + frontmatter
- **Split** → `vault_split(path, heading)` — extract section to new note

### Understanding connections

- **What links here?** → `vault_backlinks(path)`
- **What does this link to?** → `vault_links(path)`
- **Related notes** → `vault_related(path, depth=2)`
- **Unlinked mentions** → `vault_unlinked_mentions(path)` — the discovery tool
- **Link suggestions** → `vault_link_suggest(path)`
- **Path between notes** → `vault_shortest_path(a, b)`

### Analyzing the vault

- **Quick stats** → `vault_stats()`
- **Full health** → `vault_health()` — stats + broken links + orphans + tags
- **Recent changes** → `vault_changelog(days=7)`
- **Knowledge centers** → `vault_hubs(limit=10)`
- **Topic clusters** → `vault_clusters()`
- **Critical connectors** → `vault_bridges()`
- **Tag relationships** → `vault_tag_graph()`

### Vault maintenance

- **Preview first** → always use `dry_run=True` for vault-wide changes
- **One-button cleanup** → `vault_standardize(dry_run=True)` then `vault_standardize()`
- **Archive old notes** → `vault_archive(days=90, dry_run=True)`
- **Fix broken links** → `vault_broken_links()` then fix or delete
- **Auto-link mentions** → `vault_link_mentions(path, dry_run=True)`

## Patterns

### Create then enrich

```
vault_create → vault_add_tag → vault_set_frontmatter → vault_insert_at
```

### Explore then refactor

```
vault_health → vault_broken_links → vault_orphans → vault_tag_rename / vault_archive
```

### Discover then connect

```
vault_unlinked_mentions → vault_link_mentions (dry_run) → vault_link_mentions
```

### Analyze then navigate

```
vault_hubs → vault_clusters → vault_shortest_path → vault_related
```

## Anti-Patterns

- Don't use `vault_write` when `vault_create` works — you'll miss types.json registration
- Don't use `vault_search` for tags — use `vault_find("#tag")` or `vault_search_tag`
- Don't do vault-wide replace without `dry_run=True` first
- Don't call `vault_insert_at` without checking `vault_headings` first
- Don't build paths manually — always use the prefix syntax
