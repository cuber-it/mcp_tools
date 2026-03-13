        # mcp-jupyter-tools

        Jupyter tools for MCP — notebooks, kernels, JupyterHub users and servers

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-jupyter-tools
        ```

        ## Usage

        ```bash
        mcp-jupyter-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "jupyter": { "command": "mcp-jupyter-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `notebook_list` | List notebooks in a directory |
| `notebook_read` | Read a notebook (cells with outputs) |
| `notebook_create` | Create a new notebook |
| `notebook_add_cell` | Add a cell to a notebook |
| `notebook_execute` | Execute a notebook or specific cell |
| `notebook_export` | Export notebook to another format |
| `kernel_list` | List running kernels |
| `kernel_start` | Start a new kernel |
| `kernel_interrupt` | Interrupt a running kernel |
| `kernel_restart` | Restart a kernel |
| `hub_user_list` | List JupyterHub users |
| `hub_user_info` | Get info about a JupyterHub user |
| `hub_server_start` | Start a user's JupyterHub server |
| `hub_server_stop` | Stop a user's JupyterHub server |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
