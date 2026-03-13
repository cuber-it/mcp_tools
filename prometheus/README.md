        # mcp-prometheus-tools

        Prometheus monitoring tools for MCP — query metrics, alerts, targets

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-prometheus-tools
        ```

        ## Usage

        ```bash
        mcp-prometheus-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "prometheus": { "command": "mcp-prometheus-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `query` | Execute an instant PromQL query |
| `query_range` | Execute a range PromQL query |
| `series` | List time series matching a label set |
| `labels` | List all label names or values |
| `alert_list` | List active alerts |
| `alert_rules` | List alerting rules |
| `target_list` | List scrape targets and their health |
| `target_health` | Check health of a specific target |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
