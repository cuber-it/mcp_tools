# mcp-wekan-tools

Wekan Kanban board tools as a standalone MCP server — boards, lists, cards, checklists, labels, custom fields.

Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

## Installation

```bash
pip install mcp-wekan-tools
```

## Usage

```bash
mcp-wekan-tools    # stdio (default)
```

### Claude Code / Claude Desktop

```json
{
  "mcpServers": {
    "wekan": { "command": "mcp-wekan-tools" }
  }
}
```

## Configuration

```yaml
server_name: "Wekan Tools"
transport: stdio
url: "https://wekan.example.com"
username: "${WEKAN_USER}"
password: "${WEKAN_PASS}"
default_board: "optional-board-id"
```

## License

MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
