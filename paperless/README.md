        # mcp-paperless-tools

        Paperless-ngx document management tools for MCP

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-paperless-tools
        ```

        ## Usage

        ```bash
        mcp-paperless-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "paperless": { "command": "mcp-paperless-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `document_list` | List documents with optional filters |
| `document_search` | Full-text search across all documents |
| `document_get` | Get document details and content |
| `document_upload` | Upload a new document |
| `document_download` | Download a document file |
| `tag_list` | List all tags |
| `tag_assign` | Assign a tag to a document |
| `tag_remove` | Remove a tag from a document |
| `correspondent_list` | List all correspondents |
| `correspondent_assign` | Assign a correspondent to a document |
| `doctype_list` | List all document types |
| `doctype_assign` | Assign a document type to a document |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
