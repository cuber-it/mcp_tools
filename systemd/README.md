        # mcp-systemd-tools

        Systemd service management tools for MCP — services, journal, timers

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-systemd-tools
        ```

        ## Usage

        ```bash
        mcp-systemd-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "systemd": { "command": "mcp-systemd-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `service_list` | List systemd services |
| `service_status` | Show status of a service |
| `service_start` | Start a service |
| `service_stop` | Stop a service |
| `service_restart` | Restart a service |
| `service_enable` | Enable a service to start on boot |
| `service_disable` | Disable a service from starting on boot |
| `journal` | Read journal logs for a service |
| `timer_list` | List systemd timers |
| `timer_info` | Show details of a timer |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
