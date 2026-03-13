"""Pure tool logic for git — no MCP dependency."""

from __future__ import annotations

def git_status(path: str = ".") -> str:
    """Show working tree status"""
    # TODO: implement
    raise NotImplementedError("git_status")


def git_log(count: int = 10, oneline: bool = True, path: str = ".") -> str:
    """Show commit log"""
    # TODO: implement
    raise NotImplementedError("git_log")


def git_diff(staged: bool = False, file: str = "", path: str = ".") -> str:
    """Show changes"""
    # TODO: implement
    raise NotImplementedError("git_diff")


def git_blame(file: str, start_line: int = 0, end_line: int = 0, path: str = ".") -> str:
    """Show line-by-line authorship"""
    # TODO: implement
    raise NotImplementedError("git_blame")


def git_add(files: str, path: str = ".") -> str:
    """Stage files for commit"""
    # TODO: implement
    raise NotImplementedError("git_add")


def git_commit(message: str, path: str = ".") -> str:
    """Create a commit"""
    # TODO: implement
    raise NotImplementedError("git_commit")


def git_reset(files: str = "", path: str = ".") -> str:
    """Unstage files"""
    # TODO: implement
    raise NotImplementedError("git_reset")


def git_branch_list(remote: bool = False, path: str = ".") -> str:
    """List branches"""
    # TODO: implement
    raise NotImplementedError("git_branch_list")


def git_branch_create(name: str, checkout: bool = True, path: str = ".") -> str:
    """Create a new branch"""
    # TODO: implement
    raise NotImplementedError("git_branch_create")


def git_checkout(target: str, path: str = ".") -> str:
    """Switch branch or restore files"""
    # TODO: implement
    raise NotImplementedError("git_checkout")


def git_merge(branch: str, path: str = ".") -> str:
    """Merge a branch into current"""
    # TODO: implement
    raise NotImplementedError("git_merge")


def git_stash(message: str = "", path: str = ".") -> str:
    """Stash working changes"""
    # TODO: implement
    raise NotImplementedError("git_stash")


def git_stash_list(path: str = ".") -> str:
    """List stashes"""
    # TODO: implement
    raise NotImplementedError("git_stash_list")


def git_stash_pop(path: str = ".") -> str:
    """Apply and drop top stash"""
    # TODO: implement
    raise NotImplementedError("git_stash_pop")


def git_remote_list(path: str = ".") -> str:
    """List remotes"""
    # TODO: implement
    raise NotImplementedError("git_remote_list")


def git_pull(remote: str = "origin", path: str = ".") -> str:
    """Pull from remote"""
    # TODO: implement
    raise NotImplementedError("git_pull")


def git_tag_list(path: str = ".") -> str:
    """List tags"""
    # TODO: implement
    raise NotImplementedError("git_tag_list")

