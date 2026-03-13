        # mcp-rss-tools

        RSS/Atom feed reader tools for MCP

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-rss-tools
        ```

        ## Usage

        ```bash
        mcp-rss-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "rss": { "command": "mcp-rss-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `feed_read` | Read a feed and return recent entries |
| `feed_add` | Add a feed to the tracked list |
| `feed_list` | List all tracked feeds |
| `feed_remove` | Remove a feed from the tracked list |
| `entries` | List entries across all tracked feeds |
| `entry_read` | Read full content of a feed entry |
| `opml_import` | Import feeds from OPML file |
| `opml_export` | Export tracked feeds as OPML |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
