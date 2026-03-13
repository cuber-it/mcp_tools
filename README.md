# MCP Tools

MCP tool plugins — each usable standalone or via the [mcp-server-framework](https://pypi.org/project/mcp-server-framework/) proxy.

## Packages

### Production

Implemented, tested, ready to use.

| Package | PyPI | Tools | Description |
|---------|------|-------|-------------|
| [shell](shell/) | `mcp-shell-tools` | 36 | Filesystem, editor, search, shell, git, systemd, HTTP, packages |
| [wekan](wekan/) | `mcp-wekan-tools` | 18 | Wekan Kanban REST API — boards, lists, cards, checklists, labels |
| [mattermost](mattermost/) | `mcp-mattermost-tools` | 5 | Mattermost REST API — messages, channels, search |
| [wikipedia](wikipedia/) | `mcp-wikipedia-tools` | 6 | Wikipedia REST + MediaWiki API — search, articles, summaries, multilingual |

### Planned

Scaffolded from [story files](stories/), ready for implementation.

| Package | PyPI | Tools | Description |
|---------|------|-------|-------------|
| [jupyter](jupyter/) | `mcp-jupyter-tools` | 14 | Notebooks, kernels, JupyterHub users and servers |
| [finance](finance/) | `mcp-finance-tools` | 11 | Market data via yfinance — quotes, history, fundamentals, news |
| [docker](docker/) | `mcp-docker-tools` | 15 | Containers, images, volumes, compose |
| [browser](browser/) | `mcp-browser-tools` | 12 | Playwright — navigate, extract, screenshot, interact |
| [database](database/) | `mcp-database-tools` | 8 | SQLite and PostgreSQL — query, schema, export |
| [email](email/) | `mcp-email-tools` | 9 | IMAP inbox, search, send via SMTP |
| [paperless](paperless/) | `mcp-paperless-tools` | 12 | Paperless-ngx document management |
| [obsidian](obsidian/) | `mcp-obsidian-tools` | 11 | Vault read, write, search, links, tags, frontmatter |
| [scraper](scraper/) | `mcp-scraper-tools` | 8 | Fetch pages, extract content, parse metadata |
| [arxiv](arxiv/) | `mcp-arxiv-tools` | 6 | ArXiv paper search and retrieval |
| [rss](rss/) | `mcp-rss-tools` | 8 | RSS/Atom feed reader |
| [systemd](systemd/) | `mcp-systemd-tools` | 10 | Service management, journal, timers |
| [traefik](traefik/) | `mcp-traefik-tools` | 9 | Routers, services, middlewares, certs |
| [prometheus](prometheus/) | `mcp-prometheus-tools` | 8 | PromQL queries, alerts, targets |
| [mqtt](mqtt/) | `mcp-mqtt-tools` | 6 | Publish, subscribe, topics |
| [homeassistant](homeassistant/) | `mcp-homeassistant-tools` | 10 | Entities, services, automations, history |

## Installation

Each package installs independently:

```bash
pip install mcp-shell-tools
pip install mcp-wekan-tools
pip install mcp-mattermost-tools
```

## Usage

### Standalone MCP server

```bash
mcp-shell-tools                    # starts stdio MCP server with 33 tools
mcp-wekan-tools                    # starts stdio MCP server with Wekan tools
mcp-mattermost-tools               # starts stdio MCP server with Mattermost tools
```

### Claude Code / Claude Desktop

```json
{
  "mcpServers": {
    "shell": { "command": "mcp-shell-tools" },
    "wekan": { "command": "mcp-wekan-tools" },
    "mattermost": { "command": "mcp-mattermost-tools" }
  }
}
```

### As proxy plugins

```yaml
# proxy.yaml
autoload:
  - mcp_shell_tools.shell
  - mcp_wekan_tools.wekan
  - mcp_mattermost_tools.mattermost
```

## Creating new tools

New packages are generated from YAML story files in `stories/`:

```bash
python scripts/new-tool.py stories/docker.yaml          # generate package
python scripts/new-tool.py stories/docker.yaml --dry-run # preview only
```

### Claude Code Skill

For Claude Code users there's a ready-made skill in `claude-tools/new-tool.md`:

```bash
# Symlink into your .claude/commands/
ln -s "$(pwd)/claude-tools/new-tool.md" .claude/commands/new-tool.md

# Then use it as:
# /new-tool stories/docker.yaml
```

The skill reads the story, shows a plan, waits for confirmation, generates the scaffold, installs it, and runs the tests.

## Architecture

Each package follows the same pattern:

- `register(mcp, config)` — plugin interface for the proxy
- `main()` — standalone entry point (6 lines, delegates to framework)
- Zero or minimal dependencies beyond `mcp-server-framework`

```
mcp-server-framework (config, transport, health, OAuth)
    ↑
    ├── mcp-shell-tools      (stdlib only)
    ├── mcp-wekan-tools      (+ httpx)
    └── mcp-mattermost-tools (+ httpx)
```

## License

MIT
