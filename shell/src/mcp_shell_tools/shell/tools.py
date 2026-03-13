"""Shell tools — re-export facade.

Imports all tool functions from submodules so that
``from . import tools`` in __init__.py keeps working.

v4.0: Git, HTTP, systemd, pip removed — see mcp-git-tools, mcp-http-tools,
mcp-python-tools, mcp-systemd-tools.
"""

from ._history import record as _record
from ._state import (
    check_command as _check_command,
    check_command as _check_command_allowed,
    check_path as _check_path,
    format_size as _format_size,
    read_text as _read_text,
    resolve_path,
    run as _run,
    set_security_boundaries,
    set_working_dir,
)
from .editor import diff_preview, find_replace, str_replace
from .filesystem import (
    file_append,
    file_copy,
    file_delete,
    file_info,
    file_list,
    file_move,
    file_read,
    file_write,
    head,
    tail,
    tree,
)
from .search import glob_search, grep
from .shell import cd, cwd, env, set_env, shell_exec, which
from .system import disk_usage, port_check, ps, sysinfo

__all__ = [
    # state
    "set_working_dir", "set_security_boundaries", "resolve_path",
    # filesystem
    "file_read", "file_write", "file_append", "file_list",
    "file_delete", "file_move", "file_copy", "file_info",
    "head", "tail", "tree",
    # editor
    "str_replace", "diff_preview", "find_replace",
    # search
    "grep", "glob_search",
    # shell
    "shell_exec", "cd", "cwd", "which", "env", "set_env",
    # system
    "ps", "sysinfo", "port_check", "disk_usage",
]
