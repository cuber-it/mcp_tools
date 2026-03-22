# Tool Reference — mcp-vault-tools

Complete reference for all 63 tools. Each tool works as an MCP tool and as a Python function.

## Path Syntax

All tools that accept a `path` parameter support the multi-vault prefix:

```
"note.md"              → default vault
"work:meeting.md"      → vault named 'work'
"memory:facts/proxy"   → subfolder in 'memory' vault
```

The `.md` extension is optional — `vault_read("note")` works the same as `vault_read("note.md")`.

Tools that accept a `vault` parameter for filtering:

```
vault=""     → default vault only
vault="work" → specific vault
vault="*"    → all vaults (search tools only)
```

---

## CRUD

### vault_read(path) → str

Read a note. Returns JSON with `frontmatter` (dict) and `body` (string).

```python
result = vault_read(registry, "meeting")
# {"frontmatter": {"title": "Sprint Review", "tags": ["meeting"]}, "body": "..."}
```

### vault_write(path, content) → str

Write raw markdown content to a note. Creates parent directories if needed.

### vault_create(path, title?, tags?, body?, extra_frontmatter?) → str

Create a note with structured parameters. No raw markdown needed.

```python
vault_create(registry, "meeting", title="Sprint Review", tags=["meeting", "q1"],
             body="## Agenda\n\n## Notes\n")
```

Auto-registers new frontmatter keys in `types.json`.

### vault_append(path, content) → str

Append text to the end of a note.

### vault_prepend(path, content) → str

Insert text at the start of the body (after frontmatter, before existing content).

### vault_delete(path) → str

Delete a note.

### vault_list(path?, recursive?) → str

List markdown files. Default: non-recursive, default vault root.

```python
vault_list(registry, "projects/", recursive=True)
```

Respects `.obsidianignore` and skips `.obsidian/`.

### vault_exists(path) → str

Returns `"true"` or `"false"`.

---

## Navigation

### vault_headings(path) → str

List all headings with indentation showing hierarchy.

```
# Top Level
  ## Section A
    ### Subsection
  ## Section B
```

### vault_tree(vault?, max_depth?) → str

Visual tree of the vault directory structure.

```
notes/
├── daily/
│   ├── 2026-03-19.md
│   └── 2026-03-20.md
├── projects/ (3)
└── inbox.md
```

---

## Search

### vault_search(query, vault?, limit?, regex?, ignore_case?) → str

Full-text search. Searches note content and aliases.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `regex` | `False` | Treat query as regular expression |
| `ignore_case` | `True` | Case-insensitive matching |
| `vault` | `""` | `"*"` for cross-vault search |
| `limit` | `0` | 0 = use vault's `max_results` |

### vault_search_tag(tag, vault?) → str

Find notes with a specific tag. Supports hierarchical expansion: searching for `food` also finds notes tagged `food/recipe`.

### vault_search_frontmatter(key, value, vault?) → str

Find notes where a frontmatter field equals a value.

```python
vault_search_frontmatter(registry, "type", "fact")
```

### vault_find(query, vault?, limit?) → str

Unified search with auto-detection:

- `"#tag"` → searches tags
- `"key:value"` → searches frontmatter
- anything else → searches title, tags, aliases, frontmatter, body

---

## Links

### vault_links(path) → str

All outgoing links and embeds, with type info:

```
[[simple]]
[[simple#section-one]]
[[simple#^block-123]]
![[image.png]]
```

### vault_backlinks(path) → str

Notes linking to this note. Alias-aware: if the note has `aliases: [Foo]`, notes linking to `[[Foo]]` are found.

### vault_related(path, depth?) → str

Notes reachable via link traversal. `depth=1` = direct links, `depth=2` = links of links.

### vault_orphans(vault?) → str

Notes with no incoming links from any other note.

---

## Tags

### vault_tag_list(vault?) → str

All tags with occurrence counts, sorted alphabetically.

---

## Frontmatter

### vault_get_frontmatter(path) → str

Frontmatter as JSON.

### vault_set_frontmatter(path, key, value) → str

Set a single field. Auto-registers the key in `.obsidian/types.json`.

### vault_add_tag(path, tag) → str

Add a tag to the `tags` list in frontmatter.

### vault_remove_tag(path, tag) → str

Remove a tag from frontmatter.

### vault_remove_frontmatter(path, key) → str

Remove a frontmatter field entirely.

---

## Properties

### vault_get_types(vault?) → str

Read `.obsidian/types.json` — Obsidian's type hints for frontmatter fields.

### vault_set_type(key, type_hint, vault?) → str

Set a type. Valid types: `text`, `number`, `date`, `datetime`, `checkbox`, `multitext`, `aliases`, `tags`.

---

## Rename / Move

### vault_rename(old_path, new_path) → str

Rename a note. Automatically updates all `[[WikiLinks]]` pointing to it across the entire vault.

### vault_move(path, target_folder) → str

Move to a different folder. Same link-update behavior as rename.

---

## Advanced Editing

### vault_replace(query, replacement, vault?, dry_run?, ignore_case?, regex?) → str

Find and replace across the vault.

```python
# Preview changes
vault_replace(registry, "old term", "new term", dry_run=True)

# Case-insensitive regex replace
vault_replace(registry, r"v\d+\.\d+", "v2.0", regex=True, ignore_case=True)
```

### vault_insert_at(path, heading, content, position?) → str

Insert content relative to a heading.

| Position | Behavior |
|----------|----------|
| `"append"` | End of the section (before next heading) |
| `"prepend"` | Right after the heading line |
| `"replace"` | Replace the entire section content |

Use `vault_headings()` first to see available headings.

### vault_split(path, heading) → str

Extract a heading section into a new note. The original gets a `[[link]]` where the section was. Tags are copied from the parent.

---

## Refactoring

### vault_tag_rename(old_tag, new_tag, vault?, dry_run?) → str

Rename a tag everywhere — in frontmatter `tags` lists and inline `#tags`.

### vault_tag_merge(tags, target_tag, vault?) → str

Merge multiple tags into one.

```python
vault_tag_merge(registry, ["js", "javascript", "node"], "javascript")
```

### vault_bulk_frontmatter(key, value, filter_tag?, vault?, dry_run?) → str

Set a frontmatter field in many notes. Optional tag filter.

```python
vault_bulk_frontmatter(registry, "status", "archived", filter_tag="old", dry_run=True)
```

### vault_broken_links(vault?) → str

Find all `[[links]]` pointing to notes that don't exist.

---

## Connection Discovery

### vault_unlinked_mentions(path) → str

Find notes that mention this note's name (or aliases) in plain text without `[[linking]]` it. Obsidian's core feature, available headless.

### vault_link_suggest(path, limit?) → str

Suggest notes that should be linked, based on shared tags.

---

## Analysis

### vault_stats(vault?) → str

JSON with note count, tag count, link count, orphan count.

### vault_recent(limit?, vault?) → str

Most recently modified notes with timestamps.

### vault_health(vault?) → str

Combined report: stats + broken links + orphans + tag distribution.

### vault_changelog(days?, vault?) → str

Changes grouped by day. Default: last 7 days.

---

## Convenience

### vault_summary(path, recursive?) → str

For a single note: JSON with title, tags, preview.
For a folder path (ending in `/`): table of all notes with title, tags, preview.

### vault_copy(source, target) → str

Duplicate a note including frontmatter.

### vault_frontmatter_keys(vault?) → str

All frontmatter keys used across the vault, ranked by frequency.

### vault_daily(day?, vault?) → str

Create or read a daily note. Date format from config (`daily_format`).

### vault_inbox(content, vault?) → str

Quick-capture: appends timestamped content to the inbox note.

---

## Note Operations

### vault_merge(path_a, path_b, target?) → str

Merge two notes. Frontmatter is combined (A wins conflicts, tags are merged). Body B is appended with a separator. Backlinks to B are updated to point to the target.

### vault_from_template(template, target, variables?) → str

Create a note from a template file. Supports `{{variable}}` substitution plus built-in `{{date}}`, `{{time}}`, `{{datetime}}`.

### vault_list_vaults() → str

Show all configured vaults with name, path, and note count.

---

## Composite Operations

### vault_link_mentions(path, dry_run?) → str

Find all unlinked mentions and convert them to `[[WikiLinks]]`. Handles aliases.

### vault_archive(days?, archive_folder?, vault?, dry_run?) → str

Move notes not modified in N days to an archive folder. Updates links.

### vault_extract_inline_tags(path) → str

Find inline `#tags` in the body, add them to frontmatter, remove from body.

### vault_backfill_titles(vault?, dry_run?) → str

Notes without a `title` in frontmatter get their filename as title.

### vault_standardize(vault?, dry_run?) → str

One-button cleanup: backfill titles + extract inline tags + update types.json.

---

## Graph Analysis

### vault_graph(vault?) → str

Complete link graph as JSON: `{"nodes": [...], "edges": [...]}`. Each node has path, title, tags.

### vault_hubs(limit?, vault?) → str

Most connected notes ranked by total connections (in + out).

### vault_clusters(vault?) → str

Connected components — groups of notes linked together. Sorted by size.

### vault_bridges(vault?) → str

Notes whose removal would split a cluster into two. These are the connective tissue of your knowledge.

### vault_dead_ends(vault?) → str

Notes that link to other notes but have no incoming links themselves.

### vault_isolated(vault?) → str

Notes with zero links — no outgoing, no incoming. Complete islands.

### vault_shortest_path(source, target, vault?) → str

The shortest chain of links between two notes.

```python
vault_shortest_path(registry, "kubernetes", "monitoring")
# "kubernetes -> infrastructure -> observability -> monitoring"
```

### vault_tag_graph(min_overlap?, vault?) → str

Tag co-occurrence: which tags appear together on the same notes, and how often. Reveals implicit topic clusters.

### vault_tag_overlap(tag_a, tag_b, vault?) → str

Notes that have both tags — a specific cross-section.
