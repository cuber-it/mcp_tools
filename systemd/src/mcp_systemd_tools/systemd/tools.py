"""Pure tool logic for systemd — no MCP dependency."""

from __future__ import annotations

def service_list(state: str = "", user: bool = False) -> str:
    """List systemd services"""
    # TODO: implement
    raise NotImplementedError("service_list")


def service_status(service: str, user: bool = False) -> str:
    """Show status of a service"""
    # TODO: implement
    raise NotImplementedError("service_status")


def service_start(service: str, user: bool = False) -> str:
    """Start a service"""
    # TODO: implement
    raise NotImplementedError("service_start")


def service_stop(service: str, user: bool = False) -> str:
    """Stop a service"""
    # TODO: implement
    raise NotImplementedError("service_stop")


def service_restart(service: str, user: bool = False) -> str:
    """Restart a service"""
    # TODO: implement
    raise NotImplementedError("service_restart")


def service_enable(service: str, user: bool = False) -> str:
    """Enable a service to start on boot"""
    # TODO: implement
    raise NotImplementedError("service_enable")


def service_disable(service: str, user: bool = False) -> str:
    """Disable a service from starting on boot"""
    # TODO: implement
    raise NotImplementedError("service_disable")


def journal(service: str, lines: int = 50, since: str = "") -> str:
    """Read journal logs for a service"""
    # TODO: implement
    raise NotImplementedError("journal")


def timer_list(user: bool = False) -> str:
    """List systemd timers"""
    # TODO: implement
    raise NotImplementedError("timer_list")


def timer_info(timer: str, user: bool = False) -> str:
    """Show details of a timer"""
    # TODO: implement
    raise NotImplementedError("timer_info")

