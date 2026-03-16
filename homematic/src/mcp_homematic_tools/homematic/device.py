"""Device and Channel tools for HomeMatic CCU."""

from __future__ import annotations

import json
from typing import Any

from .client import CCUClient


# ---------------------------------------------------------------------------
# Device tools
# ---------------------------------------------------------------------------

def device_list(client: CCUClient, detail: bool = False) -> str:
    """List all configured devices."""
    if detail:
        devices = client.call("Device.listAllDetail")
    else:
        devices = client.call("Device.listAll")
    return json.dumps(devices, indent=2, ensure_ascii=False)


def device_get(client: CCUClient, id: str) -> str:
    """Get detail info for a single device."""
    result = client.call("Device.get", {"id": id})
    return json.dumps(result, indent=2, ensure_ascii=False)


def device_status(client: CCUClient, id: str) -> str:
    """Get status info for a device (RSSI, battery, unreach, etc.).

    Resolves address and interface automatically from the device ID.
    """
    dev = client.call("Device.get", {"id": id})
    result = client.call("Device.listStatus", {
        "id": id,
        "address": dev["address"],
        "interface": dev["interface"],
    })
    return json.dumps(result, indent=2, ensure_ascii=False)


def device_set_name(client: CCUClient, id: str, name: str) -> str:
    """Set the name of a device."""
    client.call("Device.setName", {"id": id, "name": name})
    return f"Device {id} renamed to '{name}'"


def device_set_visibility(
    client: CCUClient,
    id: str,
    visibility: str = "",
    operate_group_only: str = "",
    enabled_service_msg: str = "",
) -> str:
    """Set visibility, operability, and service message settings."""
    results = []
    if visibility:
        client.call("Device.setVisibility", {"id": id, "isVisible": visibility == "true"})
        results.append(f"visibility={visibility}")
    if operate_group_only:
        client.call("Device.setOperateGroupOnly", {"id": id, "isOperateGroupOnly": operate_group_only == "true"})
        results.append(f"operateGroupOnly={operate_group_only}")
    if enabled_service_msg:
        client.call("Device.setEnabledServiceMsg", {"id": id, "isEnabled": enabled_service_msg == "true"})
        results.append(f"enabledServiceMsg={enabled_service_msg}")
    if not results:
        return "No settings changed (all parameters empty)"
    return f"Device {id}: {', '.join(results)}"


def device_comtest(client: CCUClient, id: str, action: str = "start") -> str:
    """Start or poll a communication test.

    start returns a testId, poll requires that testId.
    """
    if action == "start":
        result = client.call("Device.startComTest", {"id": id})
        return json.dumps({"testStarted": True, "testId": result}, indent=2)
    elif action == "poll":
        # id here is the testId returned from start
        result = client.call("Device.pollComTest", {"testId": id})
        return json.dumps(result, indent=2, ensure_ascii=False)
    return f"Unknown action '{action}' (use: start, poll)"


# ---------------------------------------------------------------------------
# Channel tools
# ---------------------------------------------------------------------------

def channel_value(client: CCUClient, id: str) -> str:
    """Get the value of a channel."""
    result = client.call("Channel.getValue", {"id": id})
    return json.dumps(result, indent=2, ensure_ascii=False)


def channel_info(client: CCUClient, id: str) -> str:
    """Get name and type of a channel.

    Channel.getName uses 'address' param, Channel.getChannelType uses 'id'.
    We query both using the appropriate parameter for each.
    """
    ch_type = client.call("Channel.getChannelType", {"id": id})
    # getName needs the address — try with id first (some CCU versions accept it)
    try:
        name = client.call("Channel.getName", {"id": id})
    except Exception:
        name = "unknown"
    return json.dumps({"id": id, "name": name, "type": ch_type}, indent=2, ensure_ascii=False)


def channel_set_name(client: CCUClient, id: str, name: str) -> str:
    """Set the name of a channel."""
    client.call("Channel.setName", {"id": id, "name": name})
    return f"Channel {id} renamed to '{name}'"


def channel_config(
    client: CCUClient,
    id: str,
    logging: str = "",
    mode: str = "",
    visibility: str = "",
    usability: str = "",
) -> str:
    """Set channel configuration."""
    results = []
    if logging:
        client.call("Channel.setLogging", {"id": id, "isLogged": logging == "true"})
        results.append(f"logging={logging}")
    if mode:
        client.call("Channel.setMode", {"id": id, "mode": mode})
        results.append(f"mode={mode}")
    if visibility:
        client.call("Channel.setVisibility", {"id": id, "isVisible": visibility == "true"})
        results.append(f"visibility={visibility}")
    if usability:
        client.call("Channel.setUsability", {"id": id, "isUsable": usability == "true"})
        results.append(f"usability={usability}")
    if not results:
        return "No settings changed (all parameters empty)"
    return f"Channel {id}: {', '.join(results)}"


def channel_programs(client: CCUClient, id: str) -> str:
    """List programs using this channel."""
    has = client.call("Channel.hasProgramIds", {"id": id})
    if not has:
        return f"Channel {id}: not used in any programs"
    ids = client.call("Channel.listProgramIds", {"id": id})
    return json.dumps({"channelId": id, "programIds": ids}, indent=2, ensure_ascii=False)
