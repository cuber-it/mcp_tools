"""Tests for traefik tools."""

import pytest

from mcp_traefik_tools.traefik import register
from mcp_traefik_tools.traefik.client import TraefikClient


class TestImport:
    def test_register_exists(self):
        assert callable(register)

    def test_client_class_exists(self):
        assert TraefikClient is not None


class TestTools:
    def test_router_list_exists(self):
        from mcp_traefik_tools.traefik import tools
        assert hasattr(tools, "router_list")
        assert callable(tools.router_list)

    def test_router_inspect_exists(self):
        from mcp_traefik_tools.traefik import tools
        assert hasattr(tools, "router_inspect")
        assert callable(tools.router_inspect)

    def test_service_list_exists(self):
        from mcp_traefik_tools.traefik import tools
        assert hasattr(tools, "service_list")
        assert callable(tools.service_list)

    def test_service_health_exists(self):
        from mcp_traefik_tools.traefik import tools
        assert hasattr(tools, "service_health")
        assert callable(tools.service_health)

    def test_middleware_list_exists(self):
        from mcp_traefik_tools.traefik import tools
        assert hasattr(tools, "middleware_list")
        assert callable(tools.middleware_list)

    def test_entrypoint_list_exists(self):
        from mcp_traefik_tools.traefik import tools
        assert hasattr(tools, "entrypoint_list")
        assert callable(tools.entrypoint_list)

    def test_cert_list_exists(self):
        from mcp_traefik_tools.traefik import tools
        assert hasattr(tools, "cert_list")
        assert callable(tools.cert_list)

    def test_cert_expiry_exists(self):
        from mcp_traefik_tools.traefik import tools
        assert hasattr(tools, "cert_expiry")
        assert callable(tools.cert_expiry)

    def test_overview_exists(self):
        from mcp_traefik_tools.traefik import tools
        assert hasattr(tools, "overview")
        assert callable(tools.overview)


# TODO: add functional tests
