"""Tests for python tools."""

import pytest

from mcp_python_tools.python import register


class TestImport:
    def test_register_exists(self):
        assert callable(register)


class TestTools:
    def test_py_version_exists(self):
        from mcp_python_tools.python import tools
        assert hasattr(tools, "py_version")
        assert callable(tools.py_version)

    def test_py_pip_list_exists(self):
        from mcp_python_tools.python import tools
        assert hasattr(tools, "py_pip_list")
        assert callable(tools.py_pip_list)

    def test_py_pip_install_exists(self):
        from mcp_python_tools.python import tools
        assert hasattr(tools, "py_pip_install")
        assert callable(tools.py_pip_install)

    def test_py_pip_show_exists(self):
        from mcp_python_tools.python import tools
        assert hasattr(tools, "py_pip_show")
        assert callable(tools.py_pip_show)

    def test_py_pip_uninstall_exists(self):
        from mcp_python_tools.python import tools
        assert hasattr(tools, "py_pip_uninstall")
        assert callable(tools.py_pip_uninstall)

    def test_py_venv_create_exists(self):
        from mcp_python_tools.python import tools
        assert hasattr(tools, "py_venv_create")
        assert callable(tools.py_venv_create)

    def test_py_venv_info_exists(self):
        from mcp_python_tools.python import tools
        assert hasattr(tools, "py_venv_info")
        assert callable(tools.py_venv_info)

    def test_py_run_exists(self):
        from mcp_python_tools.python import tools
        assert hasattr(tools, "py_run")
        assert callable(tools.py_run)


# TODO: add functional tests
