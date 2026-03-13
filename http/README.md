        # mcp-http-tools

        HTTP client tools for MCP — requests, JSON, downloads, headers, status checks

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-http-tools
        ```

        ## Usage

        ```bash
        mcp-http-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "http": { "command": "mcp-http-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `http_request` | Make an HTTP request |
| `http_json` | GET a URL and parse JSON response |
| `http_download` | Download a file from URL |
| `http_head` | Get HTTP headers without body |
| `http_status` | Check if a URL is reachable (status code) |
| `http_form_post` | Submit a form (multipart/form-data) |
| `json_query` | Query a local JSON file |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
