"""Interface tools for HomeMatic CCU — values, diagnostics, pairing, links."""

from __future__ import annotations

import json
from typing import Any

from .client import CCUClient


# ---------------------------------------------------------------------------
# Values
# ---------------------------------------------------------------------------

def get_value(client: CCUClient, interface: str, address: str, value_key: str) -> str:
    """Read a single value from a device channel."""
    result = client.call_interface("getValue", interface, address, valueKey=value_key)
    return json.dumps({"interface": interface, "address": address, "key": value_key, "value": result}, indent=2)


def set_value(
    client: CCUClient,
    interface: str,
    address: str,
    value_key: str,
    value: str,
    value_type: str = "double",
) -> str:
    """Set a single value on a device channel."""
    typed_value: Any
    if value_type == "double":
        typed_value = float(value)
    elif value_type == "bool":
        typed_value = value.lower() in ("true", "1", "yes")
    elif value_type == "int":
        typed_value = int(value)
    else:
        typed_value = value

    client.call_interface(
        "setValue", interface, address,
        valueKey=value_key, type=value_type, value=typed_value,
    )
    return f"Set {address} {value_key}={typed_value} ({value_type})"


def get_paramset(
    client: CCUClient,
    interface: str,
    address: str,
    paramset_key: str = "VALUES",
) -> str:
    """Read a complete parameter set."""
    result = client.call_interface("getParamset", interface, address, paramsetKey=paramset_key)
    return json.dumps(result, indent=2, ensure_ascii=False)


def get_paramset_desc(
    client: CCUClient,
    interface: str,
    address: str,
    paramset_key: str = "VALUES",
) -> str:
    """Get the description of a parameter set."""
    result = client.call_interface("getParamsetDescription", interface, address, paramsetKey=paramset_key)
    return json.dumps(result, indent=2, ensure_ascii=False)


def put_paramset(
    client: CCUClient,
    interface: str,
    address: str,
    paramset_key: str,
    values: str,
) -> str:
    """Write a complete parameter set."""
    parsed = json.loads(values)
    client.call_interface("putParamset", interface, address, paramsetKey=paramset_key, set=parsed)
    return f"Paramset {paramset_key} written to {address}"


def get_master_value(client: CCUClient, interface: str, address: str, value_key: str) -> str:
    """Read a value from the MASTER parameter set."""
    result = client.call_interface("getMasterValue", interface, address, valueKey=value_key)
    return json.dumps({"address": address, "key": value_key, "value": result}, indent=2)


# ---------------------------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------------------------

def list_interfaces(client: CCUClient) -> str:
    """List available interfaces and check if running."""
    interfaces = client.call("Interface.listInterfaces")
    for iface in interfaces:
        try:
            present = client.call("Interface.isPresent", {"interface": iface["name"]})
            iface["isPresent"] = present
        except Exception:
            iface["isPresent"] = "unknown"
    return json.dumps(interfaces, indent=2, ensure_ascii=False)


def list_devices_raw(client: CCUClient, interface: str = "HmIP-RF") -> str:
    """List all learned devices on an interface (raw)."""
    result = client.call_interface("listDevices", interface)
    return json.dumps(result, indent=2, ensure_ascii=False)


def device_description(client: CCUClient, interface: str, address: str) -> str:
    """Get device/channel description from interface."""
    result = client.call_interface("getDeviceDescription", interface, address)
    return json.dumps(result, indent=2, ensure_ascii=False)


def rssi(client: CCUClient, interface: str = "") -> str:
    """Get signal strength (RSSI) of all devices.

    Interface parameter is required by the CCU API. If empty, queries all known interfaces.
    """
    if not interface:
        # Query all interfaces and merge results
        interfaces = client.call("Interface.listInterfaces")
        all_rssi: dict = {}
        for iface in interfaces:
            try:
                data = client.call("Interface.rssiInfo", {"interface": iface["name"]})
                if isinstance(data, dict):
                    all_rssi[iface["name"]] = data
                elif isinstance(data, list):
                    all_rssi[iface["name"]] = data
            except Exception:
                pass
        return json.dumps(all_rssi, indent=2, ensure_ascii=False)
    result = client.call("Interface.rssiInfo", {"interface": interface})
    return json.dumps(result, indent=2, ensure_ascii=False)


def duty_cycle(client: CCUClient) -> str:
    """Get DutyCycle values of all gateways."""
    result = client.call("Interface.getDutyCycle")
    return json.dumps(result, indent=2, ensure_ascii=False)


def service_messages(
    client: CCUClient,
    action: str = "count",
    interface: str = "",
    address: str = "",
    parameter_id: str = "",
) -> str:
    """Get or suppress service messages.

    All actions require the interface parameter. If empty, queries all interfaces.
    """
    if action == "count":
        if interface:
            result = client.call("Interface.getServiceMessageCount", {"interface": interface})
            return json.dumps({"interface": interface, "serviceMessageCount": result}, indent=2)
        # Query all interfaces
        interfaces = client.call("Interface.listInterfaces")
        counts = {}
        for iface in interfaces:
            try:
                c = client.call("Interface.getServiceMessageCount", {"interface": iface["name"]})
                counts[iface["name"]] = c
            except Exception:
                pass
        return json.dumps(counts, indent=2, ensure_ascii=False)
    elif action == "list_suppressed":
        iface = interface or "HmIP-RF"
        result = client.call("Interface.getSuppressedServiceMessages", {
            "interface": iface, "channelAddress": address,
        })
        return json.dumps(result, indent=2, ensure_ascii=False)
    elif action == "suppress":
        if not interface or not address:
            return "Error: interface and address required for suppress"
        client.call_interface(
            "suppressServiceMessages", interface, address,
            parameterId=parameter_id,
        )
        return f"Service messages suppressed for {address}"
    return f"Unknown action '{action}' (use: count, list_suppressed, suppress)"


# ---------------------------------------------------------------------------
# Pairing / Links
# ---------------------------------------------------------------------------

def add_device(
    client: CCUClient,
    action: str = "status",
    interface: str = "HmIP-RF",
    serial: str = "",
    mode_duration: int = 60,
) -> str:
    """Teach-in a device or manage install mode."""
    if action == "add" and serial:
        result = client.call_interface("addDevice", interface, serial_number=serial)
        return json.dumps(result, indent=2, ensure_ascii=False)
    elif action == "enable_mode":
        client.call("Interface.setInstallModeHMIP", {
            "interface": interface, "on": True, "time": mode_duration,
        })
        return f"Install mode enabled for {mode_duration}s on {interface}"
    elif action == "status":
        result = client.call("Interface.getInstallMode", {"interface": interface})
        return json.dumps({"interface": interface, "installModeSecondsLeft": result}, indent=2)
    return f"Unknown action '{action}' (use: add, enable_mode, status)"


def delete_device(client: CCUClient, interface: str, address: str, flags: int = 0) -> str:
    """Delete a device."""
    client.call_interface("deleteDevice", interface, address, flags=flags)
    return f"Device {address} deleted from {interface}"


def change_device(client: CCUClient, interface: str, old_address: str, new_address: str) -> str:
    """Replace a device with another."""
    client.call_interface("changeDevice", interface, addressOld=old_address, addressNew=new_address)
    return f"Device {old_address} replaced with {new_address}"


def links(client: CCUClient, interface: str, address: str, flags: int = 0) -> str:
    """List direct links for a device/channel."""
    result = client.call_interface("getLinks", interface, address, flags=flags)
    return json.dumps(result, indent=2, ensure_ascii=False)


def add_link(
    client: CCUClient,
    interface: str,
    sender: str,
    receiver: str,
    name: str = "",
    description: str = "",
) -> str:
    """Create a direct link between channels."""
    client.call_interface("addLink", interface, sender=sender, receiver=receiver)
    if name or description:
        client.call_interface(
            "setLinkInfo", interface,
            senderAddress=sender, receiverAddress=receiver,
            name=name, description=description,
        )
    return f"Link created: {sender} -> {receiver}"


def remove_link(client: CCUClient, interface: str, sender: str, receiver: str) -> str:
    """Remove a direct link."""
    client.call_interface("removeLink", interface, sender=sender, receiver=receiver)
    return f"Link removed: {sender} -> {receiver}"


# ---------------------------------------------------------------------------
# Misc Interface tools
# ---------------------------------------------------------------------------

def set_bidcos_interface(
    client: CCUClient,
    action: str = "list",
    address: str = "",
    interface_id: str = "",
) -> str:
    """Assign device to BidCoS interface or list interfaces."""
    if action == "list":
        result = client.call("Interface.listBidcosInterfaces", {"interface": "BidCos-RF"})
        return json.dumps(result, indent=2, ensure_ascii=False)
    elif action == "set" and address and interface_id:
        client.call("Interface.setBidcosInterface", {
            "deviceAddress": address, "interfaceId": interface_id,
        })
        return f"Device {address} assigned to interface {interface_id}"
    return "Usage: action=list or action=set with address + interface_id"


def metadata(
    client: CCUClient,
    action: str = "get",
    object_id: str = "",
    key: str = "",
    value: str = "",
) -> str:
    """Read, write or delete metadata on an object."""
    if action == "get":
        result = client.call("Interface.getMetadata", {"objectId": object_id, "dataId": key})
        return json.dumps({"objectId": object_id, "key": key, "value": result}, indent=2)
    elif action == "set":
        client.call("Interface.setMetadata", {"objectId": object_id, "dataId": key, "value": value})
        return f"Metadata set: {object_id}.{key} = {value}"
    elif action == "remove":
        client.call("Interface.removeMetadata", {"objectId": object_id, "dataId": key})
        return f"Metadata removed: {object_id}.{key}"
    return f"Unknown action '{action}' (use: get, set, remove)"


def config_cache(client: CCUClient, action: str = "clear", interface: str = "", address: str = "") -> str:
    """Clear config cache or restore config to device."""
    if action == "clear":
        client.call_interface("clearConfigCache", interface, address)
        return f"Config cache cleared for {address}"
    elif action == "restore":
        client.call_interface("restoreConfigToDevice", interface, address)
        return f"Config restored to {address}"
    return f"Unknown action '{action}' (use: clear, restore)"


def thermostat_party(client: CCUClient, interface: str, address: str, values: str) -> str:
    """Set party mode for a thermostat."""
    parsed = json.loads(values)
    client.call_interface("putThermParamset", interface, address, set=parsed)
    return f"Party mode set on {address}"
