"""Pure tool logic for traefik — no MCP dependency."""

from __future__ import annotations

from .client import TraefikClient

def router_list(client: TraefikClient) -> str:
    """List all Traefik routers"""
    # TODO: implement
    raise NotImplementedError("router_list")


def router_inspect(client: TraefikClient, name: str) -> str:
    """Show details of a router"""
    # TODO: implement
    raise NotImplementedError("router_inspect")


def service_list(client: TraefikClient) -> str:
    """List all Traefik services"""
    # TODO: implement
    raise NotImplementedError("service_list")


def service_health(client: TraefikClient, name: str) -> str:
    """Show health status of a service"""
    # TODO: implement
    raise NotImplementedError("service_health")


def middleware_list(client: TraefikClient) -> str:
    """List all middlewares"""
    # TODO: implement
    raise NotImplementedError("middleware_list")


def entrypoint_list(client: TraefikClient) -> str:
    """List all entrypoints"""
    # TODO: implement
    raise NotImplementedError("entrypoint_list")


def cert_list(client: TraefikClient) -> str:
    """List TLS certificates"""
    # TODO: implement
    raise NotImplementedError("cert_list")


def cert_expiry(client: TraefikClient, domain: str = "") -> str:
    """Check certificate expiry dates"""
    # TODO: implement
    raise NotImplementedError("cert_expiry")


def overview(client: TraefikClient) -> str:
    """Traefik dashboard overview — routers, services, middlewares counts"""
    # TODO: implement
    raise NotImplementedError("overview")

