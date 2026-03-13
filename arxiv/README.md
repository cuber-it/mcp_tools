        # mcp-arxiv-tools

        ArXiv paper search and retrieval tools for MCP

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-arxiv-tools
        ```

        ## Usage

        ```bash
        mcp-arxiv-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "arxiv": { "command": "mcp-arxiv-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `search` | Search arXiv papers by query |
| `abstract` | Get paper abstract by arXiv ID |
| `paper` | Get full paper metadata — title, authors, abstract, categories, dates |
| `download` | Download paper PDF to local path |
| `authors` | List authors of a paper |
| `recent` | List recent papers in a category |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
