        # mcp-python-tools

        Python environment tools for MCP — venvs, pip, packages, interpreter info

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-python-tools
        ```

        ## Usage

        ```bash
        mcp-python-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "python": { "command": "mcp-python-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `py_version` | Show Python version and path |
| `py_pip_list` | List installed packages |
| `py_pip_install` | Install a package |
| `py_pip_show` | Show package details |
| `py_pip_uninstall` | Uninstall a package |
| `py_venv_create` | Create a virtual environment |
| `py_venv_info` | Show venv info (path, Python version, packages count) |
| `py_run` | Run a Python expression and return result |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
