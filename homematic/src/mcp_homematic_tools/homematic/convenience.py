"""Convenience tools — high-level views combining multiple API calls."""

from __future__ import annotations

import json
from typing import Any

from .client import CCUClient


def climate(client: CCUClient, room: str = "") -> str:
    """Climate overview: temperature, humidity, valve state, set point for all rooms.

    Combines Room.getAll, Device.listAllDetail and Interface.getParamset to build
    a human-readable climate summary per room.
    """
    rooms = client.call("Room.getAll")
    devices = client.call("Device.listAllDetail")

    # Build channel→device lookup
    channel_device: dict[str, dict] = {}
    for dev in devices:
        for ch in dev.get("channels", []):
            channel_device[ch["id"]] = {
                "deviceName": dev["name"],
                "deviceType": dev["type"],
                "address": ch["address"],
                "channelIndex": ch["index"],
                "interface": dev.get("interface", "HmIP-RF"),
            }

    result = []
    for r in rooms:
        if room and room.lower() not in r["name"].lower():
            continue
        if not r.get("channelIds"):
            continue

        room_data: dict[str, Any] = {"room": r["name"], "devices": []}

        for ch_id in r["channelIds"]:
            ch_info = channel_device.get(ch_id)
            if not ch_info:
                continue

            dev_type = ch_info["deviceType"]
            is_thermo = dev_type.startswith("HmIP-STHD") or dev_type.startswith("HmIP-eTRV-B")
            if not is_thermo:
                continue
            # Only channel index 1 carries climate values
            if ch_info["channelIndex"] != 1:
                continue

            try:
                values = client.call_interface(
                    "getParamset",
                    ch_info["interface"],
                    ch_info["address"],
                    paramsetKey="VALUES",
                )
            except Exception:
                continue

            entry: dict[str, Any] = {"device": ch_info["deviceName"], "type": dev_type}

            if "ACTUAL_TEMPERATURE" in values:
                entry["temperature"] = values["ACTUAL_TEMPERATURE"]
            if "HUMIDITY" in values:
                entry["humidity"] = values["HUMIDITY"]
            if "SET_POINT_TEMPERATURE" in values:
                entry["setPoint"] = values["SET_POINT_TEMPERATURE"]
            if "LEVEL" in values:
                entry["valveLevel"] = values["LEVEL"]
            if "BOOST_MODE" in values:
                entry["boostMode"] = values["BOOST_MODE"]

            if len(entry) > 2:  # has actual values beyond device/type
                room_data["devices"].append(entry)

        if room_data["devices"]:
            result.append(room_data)

    if not result:
        return "No climate data available" + (f" for room '{room}'" if room else "")
    return json.dumps(result, indent=2, ensure_ascii=False)


def windows(client: CCUClient, room: str = "") -> str:
    """Window/door contact status for all rooms.

    Reads STATE from all HmIP-SWDO-2 devices, grouped by room.
    """
    rooms = client.call("Room.getAll")
    devices = client.call("Device.listAllDetail")

    # Build channel→device lookup
    channel_device: dict[str, dict] = {}
    for dev in devices:
        for ch in dev.get("channels", []):
            channel_device[ch["id"]] = {
                "deviceName": dev["name"],
                "deviceType": dev["type"],
                "address": ch["address"],
                "channelIndex": ch["index"],
                "interface": dev.get("interface", "HmIP-RF"),
            }

    result = []
    for r in rooms:
        if room and room.lower() not in r["name"].lower():
            continue
        if not r.get("channelIds"):
            continue

        room_data: dict[str, Any] = {"room": r["name"], "contacts": []}

        for ch_id in r["channelIds"]:
            ch_info = channel_device.get(ch_id)
            if not ch_info or not ch_info["deviceType"].startswith("HmIP-SWDO"):
                continue
            if ch_info["channelIndex"] == 0:
                continue  # Skip MAINTENANCE

            try:
                values = client.call_interface(
                    "getParamset",
                    ch_info["interface"],
                    ch_info["address"],
                    paramsetKey="VALUES",
                )
            except Exception:
                continue

            state = values.get("STATE")
            is_open = str(state) in ("1", "true", "True")
            room_data["contacts"].append({
                "device": ch_info["deviceName"],
                "state": "open" if is_open else "closed",
                "rawState": state,
            })

        if room_data["contacts"]:
            result.append(room_data)

    if not result:
        return "No window contacts found" + (f" for room '{room}'" if room else "")
    return json.dumps(result, indent=2, ensure_ascii=False)


def firmware(
    client: CCUClient,
    action: str = "refresh",
    interface: str = "HmIP-RF",
    addresses: str = "",
) -> str:
    """Update device firmware or refresh firmware list."""
    if action == "refresh":
        client.call_interface("refreshDeployedDeviceFirmwareList", interface)
        return f"Firmware list refreshed for {interface}"
    elif action == "update" and addresses:
        addr_list = [a.strip() for a in addresses.split(",") if a.strip()]
        client.call("Interface.updateFirmware", {
            "interface": interface, "devices": addr_list,
        })
        return f"Firmware update started for {', '.join(addr_list)}"
    return "Usage: action=refresh or action=update with comma-separated addresses"
