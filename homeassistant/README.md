        # mcp-homeassistant-tools

        Home Assistant tools for MCP — entities, services, automations, history

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-homeassistant-tools
        ```

        ## Usage

        ```bash
        mcp-homeassistant-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "homeassistant": { "command": "mcp-homeassistant-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `entity_list` | List all entities |
| `entity_state` | Get current state of an entity |
| `entity_set` | Set state of an entity |
| `service_call` | Call a Home Assistant service |
| `automation_list` | List all automations |
| `automation_trigger` | Trigger an automation |
| `automation_enable` | Enable an automation |
| `automation_disable` | Disable an automation |
| `history` | Get state history for an entity |
| `logbook` | Get logbook entries |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
