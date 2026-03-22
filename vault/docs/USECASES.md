# Use Cases — mcp-vault-tools

Real-world workflows with example prompts. Each scenario shows what you'd ask the LLM and which tools work together.

---

## Knowledge Management

### "I just had a meeting — capture it"

```
Create a meeting note for today's sprint review.
Attendees: Alice, Bob. We discussed the deployment timeline
and decided to postpone to next week.
Tag it with meeting and q1-2026.
```

Tools: `vault_create` → `vault_daily` (link from daily note)

### "What do I know about deployment?"

```
Search all my vaults for anything related to deployment.
```

Tools: `vault_find("deployment")` or `vault_search("*:deployment")`

### "Give me an overview of my projects folder"

```
Show me a summary of everything in the projects folder.
```

Tools: `vault_summary("projects/", recursive=True)`

### "Which notes should I connect?"

```
Check if there are notes that mention "kubernetes" without linking to the kubernetes note.
```

Tools: `vault_unlinked_mentions("kubernetes")` → `vault_link_mentions("kubernetes", dry_run=True)`

---

## Vault Hygiene

### "Is my vault healthy?"

```
Run a health check on my vault.
```

Tools: `vault_health()` — returns stats, broken links, orphans, tag distribution in one call.

### "Clean up my vault"

```
Standardize my vault — fill in missing titles, move inline tags to frontmatter.
Show me what would change first.
```

Tools: `vault_standardize(dry_run=True)` → review → `vault_standardize()`

### "Find broken links"

```
Which notes link to things that don't exist?
```

Tools: `vault_broken_links()`

### "Archive old stuff"

```
Move everything I haven't touched in 6 months to an archive folder.
Show me what would move first.
```

Tools: `vault_archive(days=180, dry_run=True)` → review → `vault_archive(days=180)`

---

## Refactoring

### "Rename a tag everywhere"

```
Rename the tag "js" to "javascript" across my entire vault.
Preview first.
```

Tools: `vault_tag_rename("js", "javascript", dry_run=True)` → `vault_tag_rename("js", "javascript")`

### "Merge related tags"

```
Merge the tags js, javascript, and node into just "javascript".
```

Tools: `vault_tag_merge(["js", "javascript", "node"], "javascript")`

### "This note is too long — split it"

```
Split the "Architecture" section out of my design-doc note into its own note.
```

Tools: `vault_headings("design-doc")` → `vault_split("design-doc", "Architecture")`

### "Rename a note without breaking links"

```
Rename old-project-name to new-project-name.
```

Tools: `vault_rename("old-project-name", "new-project-name")` — all links updated automatically.

### "Find and replace a term vault-wide"

```
Replace "microservice" with "service" everywhere. Case-insensitive. Show me what would change.
```

Tools: `vault_replace("microservice", "service", ignore_case=True, dry_run=True)`

---

## Research & Analysis

### "What are the central topics in my vault?"

```
Show me the hub notes — the most connected notes in my vault.
```

Tools: `vault_hubs(limit=10)`

### "How does topic A relate to topic B?"

```
How is the kubernetes note connected to the monitoring note?
```

Tools: `vault_shortest_path("kubernetes", "monitoring")`

### "What topic clusters do I have?"

```
Show me the knowledge clusters in my vault.
```

Tools: `vault_clusters()`

### "Which notes hold everything together?"

```
Which notes are bridges — if I removed them, parts of my vault would become disconnected?
```

Tools: `vault_bridges()`

### "Which tags co-occur?"

```
Show me which tags tend to appear together. I want to see my implicit topic clusters.
```

Tools: `vault_tag_graph(min_overlap=2)`

### "What's completely isolated?"

```
Find notes that have no links at all — neither in nor out.
```

Tools: `vault_isolated()`

---

## Daily Workflow

### "Start my day"

```
Create today's daily note and show me what changed yesterday.
```

Tools: `vault_daily()` → `vault_changelog(days=1)`

### "Quick thought"

```
Add to my inbox: "Look into vector databases for the memory system"
```

Tools: `vault_inbox("Look into vector databases for the memory system")`

### "What did I work on this week?"

```
Show me everything that changed in the last 7 days.
```

Tools: `vault_changelog(days=7)`

---

## Multi-Vault Workflows

### "Search across everything"

```
Search all my vaults for "authentication".
```

Tools: `vault_search("authentication", vault="*")`

### "Which vaults do I have?"

```
List all my configured vaults.
```

Tools: `vault_list_vaults()`

### "Move a note between contexts"

```
Copy the meeting note from my work vault to my personal vault.
```

Tools: `vault_copy("work:meetings/sprint-review", "notes:work/sprint-review")`

---

## Template Workflows

### "Create a project note from template"

```
Create a new project note for "vault-tools-v2" using the project template.
```

Tools: `vault_from_template("project", "projects/vault-tools-v2", variables={"title": "Vault Tools v2", "status": "active"})`

### "What frontmatter fields are common in my vault?"

```
Show me which frontmatter fields are used and how often.
```

Tools: `vault_frontmatter_keys()`

---

## Agent / Memory Use Cases

These show how a memory system would use vault-tools as its storage layer.

### "Remember a fact"

```python
vault_create(registry, "facts/proxy-port",
    title="Proxy Port Convention",
    tags=["fact", "infrastructure"],
    body="MCP proxy runs on port 12201.",
    extra_frontmatter={"type": "fact", "confidence": 0.9, "domain": "infrastructure"})
```

### "Recall by context"

```python
results = vault_find(registry, "proxy port")
# or more specific:
results = vault_search_frontmatter(registry, "type", "fact")
```

### "What do I know about a domain?"

```python
vault_search_tag(registry, "infrastructure")
vault_tag_graph(registry, min_overlap=2)  # see how infrastructure connects to other domains
```

### "Self-diagnosis"

```python
vault_health(registry)        # overall vault health
vault_orphans(registry)       # forgotten knowledge
vault_isolated(registry)      # completely disconnected facts
vault_dead_ends(registry)     # facts that reference things but nobody references them
```
