# mcp-shell-tools

26 workstation tools as a standalone MCP server or proxy plugin — filesystem, editor, search, shell, system diagnostics.

Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

> **v4.0 Breaking Change:** Git, HTTP, pip, and systemd tools have been split into dedicated packages
> (`mcp-git-tools`, `mcp-http-tools`, `mcp-python-tools`, `mcp-systemd-tools`).
> If you depend on those tools, install the corresponding package or use `mcp-devtools` (planned metapackage).

## Installation

```bash
pip install mcp-shell-tools
```

## Dual use: MCP server + Python library

This package works in two ways:

- **As an MCP server** — usable by any MCP client (AI agents, IDE plugins, custom integrations)
- **As a Python library** — import the functions directly, no MCP required

```python
from mcp_shell_tools.shell.filesystem import file_read, file_list
from mcp_shell_tools.shell.search import grep
from mcp_shell_tools.shell.system import sysinfo

print(file_list("/home/user/projects"))
print(grep("TODO", path="/home/user/projects", file_pattern="*.py"))
```

The MCP layer is a thin wrapper around plain Python functions. Use them in scripts, automation pipelines, or any application — no protocol overhead needed.

## Usage

### Standalone

```bash
mcp-shell-tools                                  # stdio (default)
mcp-shell-tools --transport http --port 12200    # HTTP with health endpoint
```

### Claude Code / Claude Desktop

```json
{
  "mcpServers": {
    "shell": { "command": "mcp-shell-tools" }
  }
}
```

### As proxy plugin

```yaml
# proxy.yaml
autoload:
  - mcp_shell_tools.shell
```

## Tools

### Filesystem (11 tools)

| Tool | Description |
|------|-------------|
| `file_read` | Read a file with optional line range (1-based, with line numbers) |
| `file_write` | Write content to a file, creates directories if needed |
| `file_append` | Append content to a file |
| `file_list` | List directory contents (recursive, hidden files) |
| `file_delete` | Delete a file or directory (with recursive flag) |
| `file_move` | Move or rename a file/directory |
| `file_copy` | Copy a file or directory |
| `file_info` | File metadata: size, permissions, owner, timestamps |
| `head` | First N lines of a file |
| `tail` | Last N lines of a file |
| `tree` | Directory tree as ASCII art (configurable depth) |

### Editor (3 tools)

| Tool | Description |
|------|-------------|
| `str_replace` | Replace an exact, unique string in a file |
| `diff_preview` | Preview a unified diff before applying changes |
| `find_replace` | Find and replace across multiple files (dry-run by default) |

### Search (2 tools)

| Tool | Description |
|------|-------------|
| `grep` | Search file contents with regex (recursive, case-insensitive, glob filter) |
| `glob_search` | Find files by glob pattern (e.g. `**/*.py`) |

### Shell (6 tools)

| Tool | Description |
|------|-------------|
| `exec` | Execute a shell command (bash) with configurable timeout |
| `cd` | Change working directory (persists across calls) |
| `cwd` | Show current working directory |
| `which` | Find the full path of a command |
| `env` | Show environment variables (all or specific) |
| `set_env` | Set or unset environment variables for shell_exec |

### System (4 tools)

| Tool | Description |
|------|-------------|
| `ps` | List running processes (filterable by name) |
| `sysinfo` | System overview: OS, CPU, memory, disk, uptime, load |
| `port_check` | Check what's listening on a port, or list all open ports |
| `disk_usage` | Disk usage of a directory and subdirectories |

## Security

The shell tools include a configurable security sandbox:

```yaml
# Restrict filesystem access to specific paths
allowed_paths:
  - /home/user/projects
  - /tmp

# Block dangerous commands
blocked_commands:
  - "sudo"
  - "rm -rf /"
  - "mkfs"
```

- **Path restriction**: When `allowed_paths` is set, all filesystem operations are confined to those directories. Symlinks pointing outside are rejected.
- **Command blocking**: `shell_exec` checks commands against the blocklist before execution. Partial matches work — blocking `sudo` also blocks `sudo rm`.
- **No restriction by default**: Without config, all paths and commands are allowed. This is intentional for development workstations. Lock it down for shared or production environments.

## Configuration

```yaml
server_name: "Shell Tools"
transport: stdio              # stdio | http
working_dir: /home/user       # initial cwd (optional)
timeout: 120                  # default shell_exec timeout in seconds

# Security (optional)
allowed_paths: ["/home/user/projects"]
blocked_commands: ["sudo", "rm -rf /"]

# HTTP mode
port: 12200
health_port: 12201
```

Environment variables override YAML config with `MCP_` prefix:

```bash
export MCP_TRANSPORT=http
export MCP_PORT=12200
```

## What moved where (v3 → v4)

| v3 tool | v4 package | PyPI |
|---------|------------|------|
| `git`, `git_status`, `git_log`, `git_diff` | mcp-git-tools | `pip install mcp-git-tools` |
| `http_request`, `json_query` | mcp-http-tools | `pip install mcp-http-tools` |
| `pip_list`, `pip_install` | mcp-python-tools | `pip install mcp-python-tools` |
| `systemctl` | mcp-systemd-tools | `pip install mcp-systemd-tools` |

This split follows the principle: when package creation costs nothing, optimal package size gets smaller. Each package does one thing well, and you only install what you need.

## Part of mcp_tools

This package is part of the [mcp_tools](https://github.com/cuber-it/mcp_tools) ecosystem — modular MCP tool packages that work standalone and as plugins.

## License

MIT
