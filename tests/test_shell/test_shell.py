"""Tests for mcp-shell-tools v4 — filesystem, editor, search, shell, system."""

import os
import json
import pytest

from mcp_shell_tools.shell import register
from mcp_shell_tools.shell import tools


# ---------------------------------------------------------------------------
# Import & Registration
# ---------------------------------------------------------------------------

class TestImport:
    def test_register_callable(self):
        assert callable(register)

    def test_register_tools(self):
        from mcp.server.fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp, {})
        registered = list(mcp._tool_manager._tools.keys())
        assert len(registered) == 26

    def test_v4_no_git_tools(self):
        """Git tools were removed in v4."""
        from mcp.server.fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp, {})
        registered = list(mcp._tool_manager._tools.keys())
        for removed in ["shell_git", "shell_git_status", "shell_git_log", "shell_git_diff"]:
            assert removed not in registered

    def test_v4_no_http_tools(self):
        """HTTP tools were removed in v4."""
        from mcp.server.fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp, {})
        registered = list(mcp._tool_manager._tools.keys())
        for removed in ["shell_http_request", "shell_json_query"]:
            assert removed not in registered


# ---------------------------------------------------------------------------
# Filesystem
# ---------------------------------------------------------------------------

class TestFilesystem:
    def test_file_write_and_read(self, tmp_path):
        f = str(tmp_path / "test.txt")
        result = tools.file_write(f, "hello world")
        assert "written" in result.lower()
        content = tools.file_read(f)
        assert "hello world" in content

    def test_file_append(self, tmp_path):
        f = str(tmp_path / "append.txt")
        tools.file_write(f, "line1\n")
        tools.file_append(f, "line2\n")
        content = tools.file_read(f)
        assert "line1" in content
        assert "line2" in content

    def test_file_list(self, tmp_path):
        (tmp_path / "a.txt").write_text("a")
        (tmp_path / "b.txt").write_text("b")
        result = tools.file_list(str(tmp_path))
        assert "a.txt" in result
        assert "b.txt" in result

    def test_file_copy(self, tmp_path):
        src = str(tmp_path / "src.txt")
        dst = str(tmp_path / "dst.txt")
        tools.file_write(src, "copy me")
        tools.file_copy(src, dst)
        assert "copy me" in tools.file_read(dst)

    def test_file_move(self, tmp_path):
        src = str(tmp_path / "old.txt")
        dst = str(tmp_path / "new.txt")
        tools.file_write(src, "move me")
        tools.file_move(src, dst)
        assert not os.path.exists(src)
        assert "move me" in tools.file_read(dst)

    def test_file_delete(self, tmp_path):
        f = str(tmp_path / "del.txt")
        tools.file_write(f, "delete me")
        tools.file_delete(f)
        assert not os.path.exists(f)

    def test_file_info(self, tmp_path):
        f = str(tmp_path / "info.txt")
        tools.file_write(f, "x" * 100)
        result = tools.file_info(f)
        assert "100" in result or "bytes" in result.lower()

    def test_head(self, tmp_path):
        f = str(tmp_path / "lines.txt")
        tools.file_write(f, "\n".join(f"line{i}" for i in range(50)))
        result = tools.head(f, 5)
        assert "line0" in result
        assert "line4" in result

    def test_tail(self, tmp_path):
        f = str(tmp_path / "lines.txt")
        tools.file_write(f, "\n".join(f"line{i}" for i in range(50)))
        result = tools.tail(f, 5)
        assert "line49" in result

    def test_tree(self, tmp_path):
        (tmp_path / "sub").mkdir()
        (tmp_path / "sub" / "file.py").write_text("x")
        result = tools.tree(str(tmp_path), max_depth=2)
        assert "sub" in result
        assert "file.py" in result

    def test_file_read_nonexistent(self, tmp_path):
        result = tools.file_read(str(tmp_path / "nope.txt"))
        assert "error" in result.lower() or "not found" in result.lower() or "no such" in result.lower()


# ---------------------------------------------------------------------------
# Editor
# ---------------------------------------------------------------------------

class TestEditor:
    def test_str_replace(self, tmp_path):
        f = str(tmp_path / "edit.txt")
        tools.file_write(f, "hello world")
        result = tools.str_replace(f, "world", "python")
        content = tools.file_read(f)
        assert "python" in content

    def test_diff_preview(self, tmp_path):
        f = str(tmp_path / "diff.txt")
        tools.file_write(f, "old text here")
        result = tools.diff_preview(f, "old", "new")
        assert "old" in result or "new" in result or "-" in result

    def test_find_replace_dry_run(self, tmp_path):
        f = tmp_path / "fr.txt"
        f.write_text("foo bar foo")
        result = tools.find_replace("foo", "baz", str(tmp_path), "*.txt", dry_run=True)
        # dry run should not change the file
        assert f.read_text() == "foo bar foo"


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

class TestSearch:
    def test_grep(self, tmp_path):
        (tmp_path / "a.py").write_text("def hello():\n    pass\n")
        (tmp_path / "b.py").write_text("def world():\n    pass\n")
        result = tools.grep("hello", str(tmp_path))
        assert "hello" in result

    def test_glob_search(self, tmp_path):
        (tmp_path / "one.py").write_text("")
        (tmp_path / "two.txt").write_text("")
        result = tools.glob_search("*.py", str(tmp_path))
        assert "one.py" in result
        assert "two.txt" not in result


# ---------------------------------------------------------------------------
# Shell
# ---------------------------------------------------------------------------

class TestShell:
    def test_cwd(self):
        result = tools.cwd()
        assert "/" in result

    def test_cd_and_cwd(self, tmp_path):
        tools.cd(str(tmp_path))
        result = tools.cwd()
        assert str(tmp_path) in result

    def test_which(self):
        result = tools.which("python3")
        assert "python3" in result or "/bin/" in result or "/usr/" in result

    def test_env(self):
        result = tools.env("HOME")
        assert "/" in result

    def test_set_env_and_read(self):
        tools.set_env("MCP_TEST_VAR", "test_value_42")
        result = tools.env("MCP_TEST_VAR")
        assert "test_value_42" in result
        # cleanup
        tools.set_env("MCP_TEST_VAR", "")


# ---------------------------------------------------------------------------
# System
# ---------------------------------------------------------------------------

class TestSystem:
    def test_sysinfo(self):
        result = tools.sysinfo()
        assert len(result) > 50  # should have substantial content

    def test_ps(self):
        result = tools.ps()
        assert "python" in result.lower() or "PID" in result or len(result) > 20

    def test_ps_filter(self):
        result = tools.ps("python")
        # might or might not find python, but should not error
        assert isinstance(result, str)

    def test_disk_usage(self, tmp_path):
        result = tools.disk_usage(str(tmp_path))
        assert isinstance(result, str)

    def test_port_check(self):
        # port 0 = list all, should not crash
        result = tools.port_check(0)
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------

class TestSecurity:
    def test_allowed_paths_blocks(self, tmp_path):
        tools.set_security_boundaries(
            allowed_paths=[str(tmp_path / "allowed")],
            blocked_commands=None,
        )
        (tmp_path / "allowed").mkdir()
        (tmp_path / "forbidden").mkdir()
        (tmp_path / "forbidden" / "secret.txt").write_text("nope")

        result = tools.file_read(str(tmp_path / "forbidden" / "secret.txt"))
        assert "denied" in result.lower() or "not allowed" in result.lower() or "blocked" in result.lower() or "error" in result.lower()

        # cleanup — remove restrictions
        tools.set_security_boundaries(allowed_paths=None, blocked_commands=None)

    def test_allowed_paths_allows(self, tmp_path):
        allowed = tmp_path / "ok"
        allowed.mkdir()
        (allowed / "file.txt").write_text("fine")

        tools.set_security_boundaries(
            allowed_paths=[str(allowed)],
            blocked_commands=None,
        )
        result = tools.file_read(str(allowed / "file.txt"))
        assert "fine" in result

        # cleanup
        tools.set_security_boundaries(allowed_paths=None, blocked_commands=None)
