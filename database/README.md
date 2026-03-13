        # mcp-database-tools

        Database tools for MCP — query, schema, export for SQLite and PostgreSQL

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-database-tools
        ```

        ## Usage

        ```bash
        mcp-database-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "database": { "command": "mcp-database-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `query` | Execute a read-only SQL query and return results |
| `execute` | Execute a write SQL statement (INSERT/UPDATE/DELETE, requires write_enabled config) |
| `schema` | Show database schema — tables, columns, types, indices |
| `tables` | List all tables in the database |
| `describe` | Describe a table — columns, types, constraints |
| `export_csv` | Export query results as CSV |
| `export_json` | Export query results as JSON |
| `explain` | Show query execution plan |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
