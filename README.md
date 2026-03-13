# MCP Tools

Production-ready MCP tool plugins — each usable standalone or via the [mcp-server-framework](https://pypi.org/project/mcp-server-framework/) proxy.

## Packages

| Package | PyPI | Tools | Description |
|---------|------|-------|-------------|
| [shell](shell/) | `mcp-shell-tools` | 33 | Filesystem, editor, search, shell, git, systemd, HTTP, packages |
| [wekan](wekan/) | `mcp-wekan-tools` | 18+ | Wekan Kanban REST API — boards, lists, cards, checklists, labels |
| [mattermost](mattermost/) | `mcp-mattermost-tools` | 5 | Mattermost REST API — messages, channels, search |

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
