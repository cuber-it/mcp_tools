"""CCU system, ReGa, Firewall, and Event tools for HomeMatic CCU."""

from __future__ import annotations

import json
from typing import Any

from .client import CCUClient


# ---------------------------------------------------------------------------
# CCU System
# ---------------------------------------------------------------------------

def system_info(client: CCUClient) -> str:
    """Get CCU system information."""
    info: dict[str, Any] = {}
    calls = {
        "version": "CCU.getVersion",
        "serial": "CCU.getSerial",
        "address": "CCU.getAddress",
        "hmipAddress": "CCU.getHmIPAddress",
        "addonVersions": "CCU.getAddonVersions",
        "language": "CCU.getSystemLanguage",
        "securityLevel": "CCU.getSecurityLevel",
        "sshState": "CCU.getSSHState",
        "authEnabled": "CCU.getAuthEnabled",
    }
    for key, method in calls.items():
        try:
            info[key] = client.call(method)
        except Exception as e:
            info[key] = f"error: {e}"
    return json.dumps(info, indent=2, ensure_ascii=False)


def system_config(client: CCUClient, setting: str, value: str) -> str:
    """Set CCU system configuration."""
    valid_settings = {
        "auth", "ssh", "ssh_password", "https_redirect", "snmp",
        "security_level", "language", "info_led", "firewall_configured",
    }
    if setting not in valid_settings:
        return f"Unknown setting '{setting}'. Valid: {', '.join(sorted(valid_settings))}"

    def _bool() -> bool:
        return value in ("1", "true")

    setting_map = {
        "auth": lambda: ("CCU.setAuthEnabled", {"enabled": _bool()}),
        "ssh": lambda: ("CCU.setSSH", {"mode": int(value)}),
        "ssh_password": lambda: ("CCU.setSSHPassword", {"passwd": value}),
        "https_redirect": lambda: ("CCU.setHttpsRedirectEnabled", {"enabled": _bool()}),
        "snmp": lambda: ("CCU.setSNMPEnabled", {"enabled": _bool()}),
        "security_level": lambda: ("CCU.setSecurityLevel", {"level": value}),
        "language": lambda: ("CCU.setSystemLanguage", {"language": value}),
        "info_led": lambda: ("CCU.setInfoLedConfig", {"config": value}),
        "firewall_configured": lambda: ("CCU.setFirewallConfigured", {}),
    }
    method, params = setting_map[setting]()
    client.call(method, params)
    return f"System setting '{setting}' set to '{value}'"


def system_restart(client: CCUClient, service: str) -> str:
    """Restart CCU services."""
    if service == "rega":
        client.call("CCU.restartReGa")
        return "ReGa restarted"
    elif service == "ssh":
        client.call("CCU.restartSSHDaemon")
        return "SSH daemon restarted"
    return f"Unknown service '{service}' (use: rega, ssh)"


def heating_groups(client: CCUClient) -> str:
    """List heating groups."""
    result = client.call("CCU.getHeatingGroupList")
    return json.dumps(result, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# ReGa
# ---------------------------------------------------------------------------

def rega_status(client: CCUClient) -> str:
    """Check if ReGa logic engine is running."""
    result = client.call("ReGa.isPresent")
    return json.dumps({"regaPresent": result}, indent=2)


def rega_script(client: CCUClient, script: str) -> str:
    """Execute a HomeMatic script on the CCU."""
    result = client.call("ReGa.runScript", {"script": script})
    return json.dumps(result, indent=2, ensure_ascii=False) if isinstance(result, (dict, list)) else str(result)


def rega_datapoints(client: CCUClient) -> str:
    """List all datapoints with names."""
    result = client.call("ReGa.getAllDatapoints")
    return json.dumps(result, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Firewall
# ---------------------------------------------------------------------------

def firewall(client: CCUClient, action: str = "get", config: str = "") -> str:
    """Get or set firewall configuration."""
    if action == "get":
        result = client.call("Firewall.getConfiguration")
        return json.dumps(result, indent=2, ensure_ascii=False)
    elif action == "set" and config:
        parsed = json.loads(config)
        client.call("Firewall.setConfiguration", parsed)
        return "Firewall configuration updated"
    return "Usage: action=get or action=set with config JSON"


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

def event_subscribe(client: CCUClient, action: str = "subscribe") -> str:
    """Subscribe or unsubscribe from events."""
    if action == "subscribe":
        result = client.call("Event.subscribe")
        return json.dumps({"subscribed": True, "result": result}, indent=2)
    elif action == "unsubscribe":
        result = client.call("Event.unsubscribe")
        return json.dumps({"subscribed": False, "result": result}, indent=2)
    return f"Unknown action '{action}' (use: subscribe, unsubscribe)"


def event_poll(client: CCUClient) -> str:
    """Poll for events."""
    result = client.call("Event.poll")
    if not result:
        return "No events"
    return json.dumps(result, indent=2, ensure_ascii=False)
