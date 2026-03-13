        # mcp-mqtt-tools

        MQTT messaging tools for MCP — publish, subscribe, topics

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-mqtt-tools
        ```

        ## Usage

        ```bash
        mcp-mqtt-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "mqtt": { "command": "mcp-mqtt-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `publish` | Publish a message to a topic |
| `subscribe` | Subscribe to a topic and return recent messages |
| `topics` | List known topics (via $SYS or recent activity) |
| `retained_get` | Get retained message for a topic |
| `retained_clear` | Clear retained message for a topic |
| `broker_info` | Get broker information via $SYS topics |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
