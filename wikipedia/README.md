        # mcp-wikipedia-tools

        Wikipedia tools for MCP — search, articles, summaries, multilingual

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-wikipedia-tools
        ```

        ## Usage

        ```bash
        mcp-wikipedia-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "wikipedia": { "command": "mcp-wikipedia-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `search` | Search Wikipedia articles |
| `article` | Get full article content as Markdown |
| `summary` | Get article summary (first section) |
| `links` | List all links from an article |
| `categories` | List categories of an article |
| `random` | Get a random article summary |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
