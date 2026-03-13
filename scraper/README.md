        # mcp-scraper-tools

        Web scraping tools for MCP — fetch pages, extract content, parse metadata

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-scraper-tools
        ```

        ## Usage

        ```bash
        mcp-scraper-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "scraper": { "command": "mcp-scraper-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `fetch` | Fetch a URL and return content as clean Markdown |
| `extract` | Extract content using CSS selector |
| `links` | Extract all links from a page |
| `metadata` | Extract page metadata — title, description, OG tags |
| `sitemap` | Parse sitemap.xml and list URLs |
| `table` | Extract HTML table as structured text |
| `headers` | Show HTTP response headers for a URL |
| `status` | Check HTTP status code of a URL |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
