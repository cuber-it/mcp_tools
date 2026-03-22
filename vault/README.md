# mcp-vault-tools

Headless Obsidian-compatible Markdown vault management for MCP. 63 tools for reading, writing, searching, linking, refactoring, and analyzing vaults — without Obsidian.

Works as a standalone MCP server, as a framework plugin, and as a plain Python library.

## Why

Every existing Obsidian MCP integration requires a running Obsidian instance (via the Local REST API plugin). This package works directly on the filesystem. No Electron, no desktop app, runs on servers.

Obsidian-compatible means: Markdown files, `[[WikiLinks]]`, YAML frontmatter, `#tags`. Open your vault in Obsidian and everything looks right. Open it with these tools and everything works headless.

## Installation

```bash
pip install mcp-vault-tools
```

## Quick Start

### As MCP server (Claude Desktop / Claude Code)

```json
{
  "mcpServers": {
    "vault": {
      "command": "mcp-vault-tools",
      "env": { "VAULT_PATH": "~/Obsidian/notes" }
    }
  }
}
```

### As Python library

```python
from mcp_vault_tools.vault.registry import VaultRegistry
from mcp_vault_tools.vault import tools

registry = VaultRegistry({"vault_path": "~/Obsidian/notes"})

tools.vault_create(registry, "meeting", title="Sprint Review", tags=["meeting"], body="## Notes\n\n")
tools.vault_find(registry, "#meeting")
tools.vault_insert_at(registry, "meeting", "Notes", "Discussed deployment timeline.")
tools.vault_unlinked_mentions(registry, "meeting")
```

## Multi-Vault

Named vaults with prefix syntax. No state, no switching, no confusion.

```yaml
default_vault: notes
vaults:
  notes:
    path: ~/Obsidian/notes
  work:
    path: ~/Obsidian/work
  memory:
    path: ~/agent-memory/vault
```

```python
vault_read("note.md")             # default vault
vault_read("work:meeting.md")     # explicit vault
vault_search("*:deployment")      # all vaults
vault_list_vaults()               # show configured vaults
```

Every tool accepts the prefix syntax. Cross-vault search uses `*:`.

## Tools

### CRUD (8)

| Tool | Description |
|------|-------------|
| `vault_read` | Read a note (frontmatter + body as JSON) |
| `vault_write` | Write or overwrite a note |
| `vault_create` | Create a note with structured params (title, tags, body) |
| `vault_append` | Append text to a note |
| `vault_prepend` | Prepend text after frontmatter |
| `vault_delete` | Delete a note |
| `vault_list` | List notes in a folder |
| `vault_exists` | Check if a note exists |

### Navigation (2)

| Tool | Description |
|------|-------------|
| `vault_headings` | List all headings in a note (useful before `insert_at` or `split`) |
| `vault_tree` | Visual tree of the vault structure |

### Search (4)

| Tool | Description |
|------|-------------|
| `vault_search` | Full-text search with regex and case-insensitive options |
| `vault_search_tag` | Find notes by tag (supports hierarchical tags) |
| `vault_search_frontmatter` | Find notes by frontmatter field value |
| `vault_find` | Unified search — auto-detects `#tag`, `key:value`, or free text |

All search tools include aliases in their results.

### Links (4)

| Tool | Description |
|------|-------------|
| `vault_links` | Outgoing links and embeds from a note |
| `vault_backlinks` | Notes linking to a given note (alias-aware) |
| `vault_related` | Related notes via link traversal (configurable depth) |
| `vault_orphans` | Notes with no incoming links |

Supports `[[note]]`, `[[note|alias]]`, `[[note#heading]]`, `[[note#^block-id]]`, `![[embed]]`.

### Tags (1)

| Tool | Description |
|------|-------------|
| `vault_tag_list` | All tags with counts |

### Frontmatter (5)

| Tool | Description |
|------|-------------|
| `vault_get_frontmatter` | Read frontmatter as JSON |
| `vault_set_frontmatter` | Set a field (auto-registers in types.json) |
| `vault_add_tag` | Add a tag |
| `vault_remove_tag` | Remove a tag |
| `vault_remove_frontmatter` | Remove a frontmatter field |

### Properties (2)

| Tool | Description |
|------|-------------|
| `vault_get_types` | Read Obsidian's `.obsidian/types.json` |
| `vault_set_type` | Set a frontmatter field type (text, number, date, etc.) |

### Rename / Move (2)

| Tool | Description |
|------|-------------|
| `vault_rename` | Rename a note — updates all links across the vault |
| `vault_move` | Move to another folder — updates all links |

### Advanced Editing (3)

| Tool | Description |
|------|-------------|
| `vault_replace` | Find and replace across vault (regex, case-insensitive, dry-run) |
| `vault_insert_at` | Insert content under a specific heading (append, prepend, or replace) |
| `vault_split` | Extract a heading section into a new linked note |

### Refactoring (4)

| Tool | Description |
|------|-------------|
| `vault_tag_rename` | Rename a tag vault-wide (frontmatter + inline, dry-run) |
| `vault_tag_merge` | Merge multiple tags into one |
| `vault_bulk_frontmatter` | Set a field in many notes at once (filterable, dry-run) |
| `vault_broken_links` | Find links pointing to non-existent notes |

### Connection Discovery (2)

| Tool | Description |
|------|-------------|
| `vault_unlinked_mentions` | Notes mentioning a name without linking — Obsidian's killer feature, headless |
| `vault_link_suggest` | Suggest notes to link based on shared tags |

### Analysis (4)

| Tool | Description |
|------|-------------|
| `vault_stats` | Notes, tags, links, orphans count |
| `vault_recent` | Recently modified notes |
| `vault_health` | Combined report: stats + broken links + orphans + tags |
| `vault_changelog` | Recent changes grouped by day |

### Convenience (5)

| Tool | Description |
|------|-------------|
| `vault_summary` | Title + tags + preview for a note or folder |
| `vault_copy` | Duplicate a note |
| `vault_frontmatter_keys` | All frontmatter keys used across the vault |
| `vault_daily` | Create or read a daily note |
| `vault_inbox` | Quick-capture to an inbox note with timestamp |

### Note Operations (3)

| Tool | Description |
|------|-------------|
| `vault_merge` | Merge two notes, combine frontmatter, update backlinks |
| `vault_from_template` | Create from template with `{{variable}}` substitution |
| `vault_list_vaults` | Show all configured vaults |

### Composite Operations (5)

High-level operations that replace repetitive multi-step workflows.

| Tool | Description |
|------|-------------|
| `vault_link_mentions` | Auto-link all unlinked mentions of a note (dry-run) |
| `vault_archive` | Move notes older than N days to archive (dry-run) |
| `vault_extract_inline_tags` | Move inline `#tags` to frontmatter |
| `vault_backfill_titles` | Add title from filename to all notes missing one (dry-run) |
| `vault_standardize` | One-button vault cleanup: titles + tags + types.json (dry-run) |

### Graph Analysis (9)

Knowledge graph operations inspired by the [Enzyme](https://enzyme.garden) concept.

| Tool | Description |
|------|-------------|
| `vault_graph` | Complete link graph as JSON (nodes + edges) |
| `vault_hubs` | Most connected notes — the knowledge centers |
| `vault_clusters` | Groups of connected notes (connected components) |
| `vault_bridges` | Notes whose removal would disconnect clusters |
| `vault_dead_ends` | Notes with outgoing but no incoming links |
| `vault_isolated` | Notes with no links at all |
| `vault_shortest_path` | Link chain between two notes |
| `vault_tag_graph` | Tag co-occurrence — which topics cluster together |
| `vault_tag_overlap` | Notes sharing two specific tags |

## Obsidian Compatibility

- **WikiLinks**: `[[note]]`, `[[note|alias]]`, `[[note#heading]]`, `[[note#^block-id]]`
- **Embeds**: `![[note]]`, `![[image.png]]`
- **Frontmatter**: YAML with full read/write support
- **Tags**: frontmatter + inline `#tags`, hierarchical (`#food/recipe`)
- **Aliases**: `aliases` frontmatter field, used in backlinks and search
- **types.json**: auto-registered when setting frontmatter fields
- **.obsidianignore**: respected by list, search, and analysis tools
- **.obsidian/**: always skipped

## Safety

- **Path traversal protection** — paths are resolved and validated to stay within the vault
- **Dry-run mode** — destructive operations (replace, tag_rename, bulk_frontmatter, archive, backfill_titles, standardize, link_mentions) support `dry_run=True`
- **Logging** — all write operations are logged via Python's logging module

## Configuration

```yaml
default_vault: notes
max_results: 50
daily_format: "%Y-%m-%d"
inbox_path: "inbox.md"
template_dir: "_templates"

vaults:
  notes:
    path: ~/Obsidian/notes
  work:
    path: ~/Obsidian/work
    max_results: 100
```

Per-vault settings override global defaults.

## License

MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
