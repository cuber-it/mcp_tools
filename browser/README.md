        # mcp-browser-tools

        Browser automation tools for MCP — navigate, extract, screenshot, interact

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-browser-tools
        ```

        ## Usage

        ```bash
        mcp-browser-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "browser": { "command": "mcp-browser-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `navigate` | Navigate to a URL and wait for page load |
| `screenshot` | Take a screenshot of the current page or element |
| `click` | Click an element on the page |
| `fill` | Fill a form field with text |
| `select` | Select an option from a dropdown |
| `extract_text` | Extract text content from the page or element |
| `extract_links` | Extract all links from the page |
| `extract_table` | Extract table data as structured text |
| `pdf` | Render current page as PDF |
| `evaluate` | Execute JavaScript in the page context |
| `wait_for` | Wait for an element or condition |
| `cookies` | Get all cookies for the current page |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
