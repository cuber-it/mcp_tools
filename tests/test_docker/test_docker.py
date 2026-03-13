"""Tests for docker tools."""

import pytest

from mcp_docker_tools.docker import register
from mcp_docker_tools.docker.client import DockerClient


class TestImport:
    def test_register_exists(self):
        assert callable(register)

    def test_client_class_exists(self):
        assert DockerClient is not None


class TestTools:
    def test_container_list_exists(self):
        from mcp_docker_tools.docker import tools
        assert hasattr(tools, "container_list")
        assert callable(tools.container_list)

    def test_container_start_exists(self):
        from mcp_docker_tools.docker import tools
        assert hasattr(tools, "container_start")
        assert callable(tools.container_start)

    def test_container_stop_exists(self):
        from mcp_docker_tools.docker import tools
        assert hasattr(tools, "container_stop")
        assert callable(tools.container_stop)

    def test_container_restart_exists(self):
        from mcp_docker_tools.docker import tools
        assert hasattr(tools, "container_restart")
        assert callable(tools.container_restart)

    def test_container_remove_exists(self):
        from mcp_docker_tools.docker import tools
        assert hasattr(tools, "container_remove")
        assert callable(tools.container_remove)

    def test_container_logs_exists(self):
        from mcp_docker_tools.docker import tools
        assert hasattr(tools, "container_logs")
        assert callable(tools.container_logs)

    def test_container_inspect_exists(self):
        from mcp_docker_tools.docker import tools
        assert hasattr(tools, "container_inspect")
        assert callable(tools.container_inspect)

    def test_image_list_exists(self):
        from mcp_docker_tools.docker import tools
        assert hasattr(tools, "image_list")
        assert callable(tools.image_list)

    def test_image_pull_exists(self):
        from mcp_docker_tools.docker import tools
        assert hasattr(tools, "image_pull")
        assert callable(tools.image_pull)

    def test_image_remove_exists(self):
        from mcp_docker_tools.docker import tools
        assert hasattr(tools, "image_remove")
        assert callable(tools.image_remove)

    def test_volume_list_exists(self):
        from mcp_docker_tools.docker import tools
        assert hasattr(tools, "volume_list")
        assert callable(tools.volume_list)

    def test_network_list_exists(self):
        from mcp_docker_tools.docker import tools
        assert hasattr(tools, "network_list")
        assert callable(tools.network_list)

    def test_compose_up_exists(self):
        from mcp_docker_tools.docker import tools
        assert hasattr(tools, "compose_up")
        assert callable(tools.compose_up)

    def test_compose_down_exists(self):
        from mcp_docker_tools.docker import tools
        assert hasattr(tools, "compose_down")
        assert callable(tools.compose_down)

    def test_compose_ps_exists(self):
        from mcp_docker_tools.docker import tools
        assert hasattr(tools, "compose_ps")
        assert callable(tools.compose_ps)


# TODO: add functional tests
