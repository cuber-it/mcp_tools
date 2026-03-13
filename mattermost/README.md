# mcp-mattermost-tools

Mattermost chat tools as a standalone MCP server — send messages, search, channels, posts.

Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

## Installation

```bash
pip install mcp-mattermost-tools
```

## Usage

```bash
mcp-mattermost-tools    # stdio (default)
```

### Claude Code / Claude Desktop

```json
{
  "mcpServers": {
    "mattermost": { "command": "mcp-mattermost-tools" }
  }
}
```

## Configuration

```yaml
server_name: "Mattermost Tools"
transport: stdio
url: "https://mm.example.com"
token: "${MM_TOKEN}"
```

## License

MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
