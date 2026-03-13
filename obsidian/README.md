        # mcp-obsidian-tools

        Obsidian vault tools for MCP — read, write, search, links, tags, frontmatter

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-obsidian-tools
        ```

        ## Usage

        ```bash
        mcp-obsidian-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "obsidian": { "command": "mcp-obsidian-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `note_read` | Read a note from the vault |
| `note_write` | Write or overwrite a note |
| `note_append` | Append text to an existing note |
| `note_list` | List notes in a folder |
| `search` | Full-text search across vault |
| `search_by_tag` | Find notes with a specific tag |
| `backlinks` | Find all notes linking to a given note |
| `outgoing_links` | List all links from a note |
| `tag_list` | List all tags used in the vault |
| `frontmatter_read` | Read YAML frontmatter of a note |
| `frontmatter_update` | Update frontmatter fields of a note |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
