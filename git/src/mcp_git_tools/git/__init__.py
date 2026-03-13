"""Git — MCP plugin.

Git version control tools for MCP — status, log, diff, commit, branch, stash, remote, blame
"""

from __future__ import annotations

from . import tools


def register(mcp, config: dict) -> None:
    """Register git tools as MCP tools."""
    @mcp.tool()
    def git_status(path: str = ".") -> str:
        """Show working tree status"""
        return tools.git_status(path)

    @mcp.tool()
    def git_log(count: int = 10, oneline: bool = True, path: str = ".") -> str:
        """Show commit log"""
        return tools.git_log(count, oneline, path)

    @mcp.tool()
    def git_diff(staged: bool = False, file: str = "", path: str = ".") -> str:
        """Show changes"""
        return tools.git_diff(staged, file, path)

    @mcp.tool()
    def git_blame(file: str, start_line: int = 0, end_line: int = 0, path: str = ".") -> str:
        """Show line-by-line authorship"""
        return tools.git_blame(file, start_line, end_line, path)

    @mcp.tool()
    def git_add(files: str, path: str = ".") -> str:
        """Stage files for commit"""
        return tools.git_add(files, path)

    @mcp.tool()
    def git_commit(message: str, path: str = ".") -> str:
        """Create a commit"""
        return tools.git_commit(message, path)

    @mcp.tool()
    def git_reset(files: str = "", path: str = ".") -> str:
        """Unstage files"""
        return tools.git_reset(files, path)

    @mcp.tool()
    def git_branch_list(remote: bool = False, path: str = ".") -> str:
        """List branches"""
        return tools.git_branch_list(remote, path)

    @mcp.tool()
    def git_branch_create(name: str, checkout: bool = True, path: str = ".") -> str:
        """Create a new branch"""
        return tools.git_branch_create(name, checkout, path)

    @mcp.tool()
    def git_checkout(target: str, path: str = ".") -> str:
        """Switch branch or restore files"""
        return tools.git_checkout(target, path)

    @mcp.tool()
    def git_merge(branch: str, path: str = ".") -> str:
        """Merge a branch into current"""
        return tools.git_merge(branch, path)

    @mcp.tool()
    def git_stash(message: str = "", path: str = ".") -> str:
        """Stash working changes"""
        return tools.git_stash(message, path)

    @mcp.tool()
    def git_stash_list(path: str = ".") -> str:
        """List stashes"""
        return tools.git_stash_list(path)

    @mcp.tool()
    def git_stash_pop(path: str = ".") -> str:
        """Apply and drop top stash"""
        return tools.git_stash_pop(path)

    @mcp.tool()
    def git_remote_list(path: str = ".") -> str:
        """List remotes"""
        return tools.git_remote_list(path)

    @mcp.tool()
    def git_pull(remote: str = "origin", path: str = ".") -> str:
        """Pull from remote"""
        return tools.git_pull(remote, path)

    @mcp.tool()
    def git_tag_list(path: str = ".") -> str:
        """List tags"""
        return tools.git_tag_list(path)
