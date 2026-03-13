"""Tests for jupyter tools."""

import pytest

from mcp_jupyter_tools.jupyter import register
from mcp_jupyter_tools.jupyter.client import JupyterClient


class TestImport:
    def test_register_exists(self):
        assert callable(register)

    def test_client_class_exists(self):
        assert JupyterClient is not None


class TestTools:
    def test_notebook_list_exists(self):
        from mcp_jupyter_tools.jupyter import tools
        assert hasattr(tools, "notebook_list")
        assert callable(tools.notebook_list)

    def test_notebook_read_exists(self):
        from mcp_jupyter_tools.jupyter import tools
        assert hasattr(tools, "notebook_read")
        assert callable(tools.notebook_read)

    def test_notebook_create_exists(self):
        from mcp_jupyter_tools.jupyter import tools
        assert hasattr(tools, "notebook_create")
        assert callable(tools.notebook_create)

    def test_notebook_add_cell_exists(self):
        from mcp_jupyter_tools.jupyter import tools
        assert hasattr(tools, "notebook_add_cell")
        assert callable(tools.notebook_add_cell)

    def test_notebook_execute_exists(self):
        from mcp_jupyter_tools.jupyter import tools
        assert hasattr(tools, "notebook_execute")
        assert callable(tools.notebook_execute)

    def test_notebook_export_exists(self):
        from mcp_jupyter_tools.jupyter import tools
        assert hasattr(tools, "notebook_export")
        assert callable(tools.notebook_export)

    def test_kernel_list_exists(self):
        from mcp_jupyter_tools.jupyter import tools
        assert hasattr(tools, "kernel_list")
        assert callable(tools.kernel_list)

    def test_kernel_start_exists(self):
        from mcp_jupyter_tools.jupyter import tools
        assert hasattr(tools, "kernel_start")
        assert callable(tools.kernel_start)

    def test_kernel_interrupt_exists(self):
        from mcp_jupyter_tools.jupyter import tools
        assert hasattr(tools, "kernel_interrupt")
        assert callable(tools.kernel_interrupt)

    def test_kernel_restart_exists(self):
        from mcp_jupyter_tools.jupyter import tools
        assert hasattr(tools, "kernel_restart")
        assert callable(tools.kernel_restart)

    def test_hub_user_list_exists(self):
        from mcp_jupyter_tools.jupyter import tools
        assert hasattr(tools, "hub_user_list")
        assert callable(tools.hub_user_list)

    def test_hub_user_info_exists(self):
        from mcp_jupyter_tools.jupyter import tools
        assert hasattr(tools, "hub_user_info")
        assert callable(tools.hub_user_info)

    def test_hub_server_start_exists(self):
        from mcp_jupyter_tools.jupyter import tools
        assert hasattr(tools, "hub_server_start")
        assert callable(tools.hub_server_start)

    def test_hub_server_stop_exists(self):
        from mcp_jupyter_tools.jupyter import tools
        assert hasattr(tools, "hub_server_stop")
        assert callable(tools.hub_server_stop)


# TODO: add functional tests
