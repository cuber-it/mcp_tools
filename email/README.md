        # mcp-email-tools

        Email tools for MCP — IMAP inbox, search, send via SMTP

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-email-tools
        ```

        ## Usage

        ```bash
        mcp-email-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "email": { "command": "mcp-email-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `inbox` | List recent messages from inbox |
| `search` | Search emails by criteria |
| `read` | Read a specific email by ID |
| `folders` | List available mail folders |
| `move` | Move a message to another folder |
| `mark` | Mark a message as read/unread/flagged |
| `send` | Send a plain text email |
| `send_html` | Send an HTML email |
| `reply` | Reply to a message |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
