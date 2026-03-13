"""Tests for prometheus tools."""

import pytest

from mcp_prometheus_tools.prometheus import register
from mcp_prometheus_tools.prometheus.client import PrometheusClient


class TestImport:
    def test_register_exists(self):
        assert callable(register)

    def test_client_class_exists(self):
        assert PrometheusClient is not None


class TestTools:
    def test_query_exists(self):
        from mcp_prometheus_tools.prometheus import tools
        assert hasattr(tools, "query")
        assert callable(tools.query)

    def test_query_range_exists(self):
        from mcp_prometheus_tools.prometheus import tools
        assert hasattr(tools, "query_range")
        assert callable(tools.query_range)

    def test_series_exists(self):
        from mcp_prometheus_tools.prometheus import tools
        assert hasattr(tools, "series")
        assert callable(tools.series)

    def test_labels_exists(self):
        from mcp_prometheus_tools.prometheus import tools
        assert hasattr(tools, "labels")
        assert callable(tools.labels)

    def test_alert_list_exists(self):
        from mcp_prometheus_tools.prometheus import tools
        assert hasattr(tools, "alert_list")
        assert callable(tools.alert_list)

    def test_alert_rules_exists(self):
        from mcp_prometheus_tools.prometheus import tools
        assert hasattr(tools, "alert_rules")
        assert callable(tools.alert_rules)

    def test_target_list_exists(self):
        from mcp_prometheus_tools.prometheus import tools
        assert hasattr(tools, "target_list")
        assert callable(tools.target_list)

    def test_target_health_exists(self):
        from mcp_prometheus_tools.prometheus import tools
        assert hasattr(tools, "target_health")
        assert callable(tools.target_health)


# TODO: add functional tests
