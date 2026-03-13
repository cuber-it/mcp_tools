"""Prometheus — MCP plugin.

Prometheus monitoring tools for MCP — query metrics, alerts, targets

Config keys:
    url: (required)
"""

from __future__ import annotations

from .client import PrometheusClient
from . import tools


def register(mcp, config: dict) -> None:
    """Register prometheus tools as MCP tools."""
    client = PrometheusClient(config)

    @mcp.tool()
    def query(promql: str) -> str:
        """Execute an instant PromQL query"""
        return tools.query(client, promql)

    @mcp.tool()
    def query_range(promql: str, start: str = "1h", step: str = "15s") -> str:
        """Execute a range PromQL query"""
        return tools.query_range(client, promql, start, step)

    @mcp.tool()
    def series(match: str) -> str:
        """List time series matching a label set"""
        return tools.series(client, match)

    @mcp.tool()
    def labels(label: str = "") -> str:
        """List all label names or values"""
        return tools.labels(client, label)

    @mcp.tool()
    def alert_list() -> str:
        """List active alerts"""
        return tools.alert_list(client)

    @mcp.tool()
    def alert_rules() -> str:
        """List alerting rules"""
        return tools.alert_rules(client)

    @mcp.tool()
    def target_list() -> str:
        """List scrape targets and their health"""
        return tools.target_list(client)

    @mcp.tool()
    def target_health(job: str) -> str:
        """Check health of a specific target"""
        return tools.target_health(client, job)
