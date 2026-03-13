"""Pure tool logic for prometheus — no MCP dependency."""

from __future__ import annotations

from .client import PrometheusClient

def query(client: PrometheusClient, promql: str) -> str:
    """Execute an instant PromQL query"""
    # TODO: implement
    raise NotImplementedError("query")


def query_range(client: PrometheusClient, promql: str, start: str = "1h", step: str = "15s") -> str:
    """Execute a range PromQL query"""
    # TODO: implement
    raise NotImplementedError("query_range")


def series(client: PrometheusClient, match: str) -> str:
    """List time series matching a label set"""
    # TODO: implement
    raise NotImplementedError("series")


def labels(client: PrometheusClient, label: str = "") -> str:
    """List all label names or values"""
    # TODO: implement
    raise NotImplementedError("labels")


def alert_list(client: PrometheusClient) -> str:
    """List active alerts"""
    # TODO: implement
    raise NotImplementedError("alert_list")


def alert_rules(client: PrometheusClient) -> str:
    """List alerting rules"""
    # TODO: implement
    raise NotImplementedError("alert_rules")


def target_list(client: PrometheusClient) -> str:
    """List scrape targets and their health"""
    # TODO: implement
    raise NotImplementedError("target_list")


def target_health(client: PrometheusClient, job: str) -> str:
    """Check health of a specific target"""
    # TODO: implement
    raise NotImplementedError("target_health")

