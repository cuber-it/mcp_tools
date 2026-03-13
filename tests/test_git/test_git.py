"""Tests for git tools."""

import pytest

from mcp_git_tools.git import register


class TestImport:
    def test_register_exists(self):
        assert callable(register)


class TestTools:
    def test_git_status_exists(self):
        from mcp_git_tools.git import tools
        assert hasattr(tools, "git_status")
        assert callable(tools.git_status)

    def test_git_log_exists(self):
        from mcp_git_tools.git import tools
        assert hasattr(tools, "git_log")
        assert callable(tools.git_log)

    def test_git_diff_exists(self):
        from mcp_git_tools.git import tools
        assert hasattr(tools, "git_diff")
        assert callable(tools.git_diff)

    def test_git_blame_exists(self):
        from mcp_git_tools.git import tools
        assert hasattr(tools, "git_blame")
        assert callable(tools.git_blame)

    def test_git_add_exists(self):
        from mcp_git_tools.git import tools
        assert hasattr(tools, "git_add")
        assert callable(tools.git_add)

    def test_git_commit_exists(self):
        from mcp_git_tools.git import tools
        assert hasattr(tools, "git_commit")
        assert callable(tools.git_commit)

    def test_git_reset_exists(self):
        from mcp_git_tools.git import tools
        assert hasattr(tools, "git_reset")
        assert callable(tools.git_reset)

    def test_git_branch_list_exists(self):
        from mcp_git_tools.git import tools
        assert hasattr(tools, "git_branch_list")
        assert callable(tools.git_branch_list)

    def test_git_branch_create_exists(self):
        from mcp_git_tools.git import tools
        assert hasattr(tools, "git_branch_create")
        assert callable(tools.git_branch_create)

    def test_git_checkout_exists(self):
        from mcp_git_tools.git import tools
        assert hasattr(tools, "git_checkout")
        assert callable(tools.git_checkout)

    def test_git_merge_exists(self):
        from mcp_git_tools.git import tools
        assert hasattr(tools, "git_merge")
        assert callable(tools.git_merge)

    def test_git_stash_exists(self):
        from mcp_git_tools.git import tools
        assert hasattr(tools, "git_stash")
        assert callable(tools.git_stash)

    def test_git_stash_list_exists(self):
        from mcp_git_tools.git import tools
        assert hasattr(tools, "git_stash_list")
        assert callable(tools.git_stash_list)

    def test_git_stash_pop_exists(self):
        from mcp_git_tools.git import tools
        assert hasattr(tools, "git_stash_pop")
        assert callable(tools.git_stash_pop)

    def test_git_remote_list_exists(self):
        from mcp_git_tools.git import tools
        assert hasattr(tools, "git_remote_list")
        assert callable(tools.git_remote_list)

    def test_git_pull_exists(self):
        from mcp_git_tools.git import tools
        assert hasattr(tools, "git_pull")
        assert callable(tools.git_pull)

    def test_git_tag_list_exists(self):
        from mcp_git_tools.git import tools
        assert hasattr(tools, "git_tag_list")
        assert callable(tools.git_tag_list)


# TODO: add functional tests
