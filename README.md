# MCP Tools

Production-ready MCP tool packages — each usable standalone or as a plugin for the [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

Every package works in three ways:
1. **Standalone MCP server** — `pip install` and run
2. **Python library** — import and call functions directly
3. **Framework plugin** — load via `register(mcp, config)`

## Packages

| Package | PyPI | Tools | Description |
|---------|------|-------|-------------|
| [shell](shell/) | [`mcp-shell-tools`](https://pypi.org/project/mcp-shell-tools/) | 26 | Filesystem, editor, search, shell, system diagnostics |
| [homematic](homematic/) | [`mcp-homematic-tools`](https://pypi.org/project/mcp-homematic-tools/) | 60 | HomeMatic CCU3 / OpenCCU — devices, channels, rooms, programs, system variables |
| [playwright](playwright/) | [`mcp-playwright-tools`](https://pypi.org/project/mcp-playwright-tools/) | 43 | Browser automation — navigation, interaction, content extraction, semantic locators |
| [image](image/) | [`mcp-image-tools`](https://pypi.org/project/mcp-image-tools/) | 6 | Image processing — read, resize, crop, convert, base64 output |

**135 tools** across 4 packages. All MIT licensed.

## Quick Start

```bash
pip install mcp-shell-tools
mcp-shell-tools                    # starts stdio MCP server with 26 tools
```

### Claude Code / Claude Desktop

```json
{
  "mcpServers": {
    "shell": { "command": "mcp-shell-tools" },
    "playwright": { "command": "mcp-playwright-tools" },
    "image": { "command": "mcp-image-tools" }
  }
}
```

### As Python library

```python
from mcp_shell_tools.shell import tools

result = tools.file_read("/etc/hosts")
files = tools.glob_search("**/*.py")
```

## Architecture

Each package follows the same pattern:

- `register(mcp, config)` — plugin interface for the framework
- `main()` — standalone entry point (delegates to framework)
- Zero or minimal dependencies beyond `mcp-server-framework`

```
mcp-server-framework (config, transport, health, plugin system)
    |
    +-- mcp-shell-tools      (stdlib only)
    +-- mcp-homematic-tools  (+ httpx)
    +-- mcp-playwright-tools (+ playwright)
    +-- mcp-image-tools      (+ Pillow)
```

## License

MIT
