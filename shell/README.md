# mcp-shell-tools

33 workstation tools as a standalone MCP server — filesystem, editor, search, shell, git, systemd, HTTP, packages, diagnostics.

Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

## Installation

```bash
pip install mcp-shell-tools
```

## Usage

```bash
mcp-shell-tools                                  # stdio (default)
mcp-shell-tools --transport http --port 12200    # HTTP
```

### Claude Code / Claude Desktop

```json
{
  "mcpServers": {
    "shell": { "command": "mcp-shell-tools" }
  }
}
```

## Tools

| Category | Tools | Count |
|----------|-------|-------|
| Filesystem | file_read, file_write, file_append, file_list, file_delete, file_move, file_copy, file_info, head, tail, tree | 11 |
| Editor | str_replace, diff_preview, find_replace | 3 |
| Search | grep, glob_search | 2 |
| Shell | shell_exec, cd, cwd, which, env, set_env | 6 |
| Git | git, git_status, git_log, git_diff | 4 |
| HTTP | http_request, json_query | 2 |
| System | ps, sysinfo, port_check, disk_usage | 4 |
| Services | systemctl, pip_list, pip_install | 3 |
| History | history | 1 |

## Configuration

```yaml
server_name: "Shell Tools"
transport: stdio
allowed_paths: ["/home/user/projects"]
blocked_commands: ["sudo", "rm -rf /"]
```

## License

MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
