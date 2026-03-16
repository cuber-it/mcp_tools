"""HomeMatic/OpenCCU adapter — MCP plugin for CCU3 JSON-RPC API.

55 tools covering devices, channels, interfaces, rooms, functions,
system variables, programs, events, and system management.

Config keys:
    url: CCU base URL (required, e.g. http://192.168.178.53)
    username: Login username (required)
    password: Login password (required)
"""

from __future__ import annotations

from .client import CCUClient
from . import tools


def register(mcp, config: dict) -> None:
    """Register all HomeMatic tools as MCP tools."""
    url = config.get("url")
    if not url:
        raise ValueError("HomeMatic plugin requires 'url' in config")

    client = CCUClient(
        url=url,
        username=config.get("username", ""),
        password=config.get("password", ""),
    )

    # --- Device (6) ---

    @mcp.tool()
    def ccu_device_list(detail: bool = False) -> str:
        """List all configured devices. Set detail=true for full info including channels."""
        return tools.device_list(client, detail)

    @mcp.tool()
    def ccu_device_get(id: str) -> str:
        """Get detail info for a single device by ID."""
        return tools.device_get(client, id)

    @mcp.tool()
    def ccu_device_status(id: str) -> str:
        """Get status info for a device (battery, connectivity, etc.)."""
        return tools.device_status(client, id)

    @mcp.tool()
    def ccu_device_set_name(id: str, name: str) -> str:
        """Set the name of a device."""
        return tools.device_set_name(client, id, name)

    @mcp.tool()
    def ccu_device_set_visibility(
        id: str,
        visibility: str = "",
        operate_group_only: str = "",
        enabled_service_msg: str = "",
    ) -> str:
        """Set visibility, operability, and service message settings for a device."""
        return tools.device_set_visibility(client, id, visibility, operate_group_only, enabled_service_msg)

    @mcp.tool()
    def ccu_device_comtest(id: str, action: str = "start") -> str:
        """Start or poll a communication test for a device. action: start, poll"""
        return tools.device_comtest(client, id, action)

    # --- Channel (5) ---

    @mcp.tool()
    def ccu_channel_value(id: str) -> str:
        """Get the current value of a channel."""
        return tools.channel_value(client, id)

    @mcp.tool()
    def ccu_channel_info(id: str) -> str:
        """Get name and type of a channel."""
        return tools.channel_info(client, id)

    @mcp.tool()
    def ccu_channel_set_name(id: str, name: str) -> str:
        """Set the name of a channel."""
        return tools.channel_set_name(client, id, name)

    @mcp.tool()
    def ccu_channel_config(
        id: str,
        logging: str = "",
        mode: str = "",
        visibility: str = "",
        usability: str = "",
    ) -> str:
        """Set channel config: logging, transmission mode, visibility, usability."""
        return tools.channel_config(client, id, logging, mode, visibility, usability)

    @mcp.tool()
    def ccu_channel_programs(id: str) -> str:
        """List programs using this channel."""
        return tools.channel_programs(client, id)

    # --- Interface — Values (6) ---

    @mcp.tool()
    def ccu_get_value(interface: str, address: str, value_key: str) -> str:
        """Read a single value from a device channel. Example: interface=HmIP-RF, address=SERIAL:1, value_key=ACTUAL_TEMPERATURE"""
        return tools.get_value(client, interface, address, value_key)

    @mcp.tool()
    def ccu_set_value(
        interface: str,
        address: str,
        value_key: str,
        value: str,
        value_type: str = "double",
    ) -> str:
        """Set a single value on a device channel. value_type: double, bool, int, string"""
        return tools.set_value(client, interface, address, value_key, value, value_type)

    @mcp.tool()
    def ccu_get_paramset(
        interface: str,
        address: str,
        paramset_key: str = "VALUES",
    ) -> str:
        """Read a complete parameter set (VALUES or MASTER) from a channel."""
        return tools.get_paramset(client, interface, address, paramset_key)

    @mcp.tool()
    def ccu_get_paramset_desc(
        interface: str,
        address: str,
        paramset_key: str = "VALUES",
    ) -> str:
        """Get the description of a parameter set — shows available parameters and their types."""
        return tools.get_paramset_desc(client, interface, address, paramset_key)

    @mcp.tool()
    def ccu_put_paramset(
        interface: str,
        address: str,
        paramset_key: str,
        values: str,
    ) -> str:
        """Write a complete parameter set. values: JSON object with key-value pairs."""
        return tools.put_paramset(client, interface, address, paramset_key, values)

    @mcp.tool()
    def ccu_get_master_value(interface: str, address: str, value_key: str) -> str:
        """Read a value from the MASTER parameter set (device configuration)."""
        return tools.get_master_value(client, interface, address, value_key)

    # --- Interface — Diagnostics (6) ---

    @mcp.tool()
    def ccu_list_interfaces() -> str:
        """List available interfaces (HmIP-RF, BidCos-RF, VirtualDevices) and check status."""
        return tools.list_interfaces(client)

    @mcp.tool()
    def ccu_list_devices_raw(interface: str = "HmIP-RF") -> str:
        """List all learned devices on an interface (raw interface-level data)."""
        return tools.list_devices_raw(client, interface)

    @mcp.tool()
    def ccu_device_description(interface: str, address: str) -> str:
        """Get device or channel description from interface layer."""
        return tools.device_description(client, interface, address)

    @mcp.tool()
    def ccu_rssi(interface: str = "") -> str:
        """Get signal strength (RSSI) of all devices. Empty interface = all."""
        return tools.rssi(client, interface)

    @mcp.tool()
    def ccu_duty_cycle() -> str:
        """Get DutyCycle values of all gateways/interfaces."""
        return tools.duty_cycle(client)

    @mcp.tool()
    def ccu_service_messages(
        action: str = "count",
        interface: str = "",
        address: str = "",
        parameter_id: str = "",
    ) -> str:
        """Get or suppress service messages. action: count, list_suppressed, suppress"""
        return tools.service_messages(client, action, interface, address, parameter_id)

    # --- Interface — Pairing/Links (6) ---

    @mcp.tool()
    def ccu_add_device(
        action: str = "status",
        interface: str = "HmIP-RF",
        serial: str = "",
        mode_duration: int = 60,
    ) -> str:
        """Teach-in a device or manage install mode. action: add, enable_mode, status"""
        return tools.add_device(client, action, interface, serial, mode_duration)

    @mcp.tool()
    def ccu_delete_device(interface: str, address: str, flags: int = 0) -> str:
        """Delete a device from the CCU."""
        return tools.delete_device(client, interface, address, flags)

    @mcp.tool()
    def ccu_change_device(interface: str, old_address: str, new_address: str) -> str:
        """Replace a device with another (keeps configuration)."""
        return tools.change_device(client, interface, old_address, new_address)

    @mcp.tool()
    def ccu_links(interface: str, address: str, flags: int = 0) -> str:
        """List all direct links for a device or channel."""
        return tools.links(client, interface, address, flags)

    @mcp.tool()
    def ccu_add_link(
        interface: str,
        sender: str,
        receiver: str,
        name: str = "",
        description: str = "",
    ) -> str:
        """Create a direct link between two channels."""
        return tools.add_link(client, interface, sender, receiver, name, description)

    @mcp.tool()
    def ccu_remove_link(interface: str, sender: str, receiver: str) -> str:
        """Remove a direct link between two channels."""
        return tools.remove_link(client, interface, sender, receiver)

    # --- Interface — Misc (4) ---

    @mcp.tool()
    def ccu_set_bidcos_interface(
        action: str = "list",
        address: str = "",
        interface_id: str = "",
    ) -> str:
        """List BidCoS interfaces or assign a device to one. action: list, set"""
        return tools.set_bidcos_interface(client, action, address, interface_id)

    @mcp.tool()
    def ccu_metadata(
        action: str = "get",
        object_id: str = "",
        key: str = "",
        value: str = "",
    ) -> str:
        """Read, write or delete metadata on an object. action: get, set, remove"""
        return tools.metadata(client, action, object_id, key, value)

    @mcp.tool()
    def ccu_config_cache(
        action: str = "clear",
        interface: str = "",
        address: str = "",
    ) -> str:
        """Clear config cache or restore config to device. action: clear, restore"""
        return tools.config_cache(client, action, interface, address)

    @mcp.tool()
    def ccu_thermostat_party(interface: str, address: str, values: str) -> str:
        """Set party mode for a thermostat. values: JSON with party mode parameters."""
        return tools.thermostat_party(client, interface, address, values)

    # --- Room (3) ---

    @mcp.tool()
    def ccu_room_list() -> str:
        """List all rooms with their assigned channel IDs."""
        return tools.room_list(client)

    @mcp.tool()
    def ccu_room_get(id: str) -> str:
        """Get room details and associated programs."""
        return tools.room_get(client, id)

    @mcp.tool()
    def ccu_room_channel(action: str, room_id: str, channel_id: str) -> str:
        """Add or remove a channel from a room. action: add, remove"""
        return tools.room_channel(client, action, room_id, channel_id)

    # --- Function/Gewerk (3) ---

    @mcp.tool()
    def ccu_function_list() -> str:
        """List all functions (Gewerke) with their assigned channel IDs."""
        return tools.function_list(client)

    @mcp.tool()
    def ccu_function_get(id: str) -> str:
        """Get function details and associated programs."""
        return tools.function_get(client, id)

    @mcp.tool()
    def ccu_function_channel(action: str, function_id: str, channel_id: str) -> str:
        """Add or remove a channel from a function. action: add, remove"""
        return tools.function_channel(client, action, function_id, channel_id)

    # --- SysVar (5) ---

    @mcp.tool()
    def ccu_sysvar_list() -> str:
        """List all system variables with current values."""
        return tools.sysvar_list(client)

    @mcp.tool()
    def ccu_sysvar_get(id: str = "", name: str = "") -> str:
        """Get a system variable value by ID or name."""
        return tools.sysvar_get(client, id, name)

    @mcp.tool()
    def ccu_sysvar_set(id: str, value: str) -> str:
        """Set a system variable value. Type is detected automatically."""
        return tools.sysvar_set(client, id, value)

    @mcp.tool()
    def ccu_sysvar_create(
        name: str,
        var_type: str,
        init_value: str = "",
        min_value: str = "",
        max_value: str = "",
        enum_values: str = "",
    ) -> str:
        """Create a new system variable. var_type: bool, float, enum"""
        return tools.sysvar_create(client, name, var_type, init_value, min_value, max_value, enum_values)

    @mcp.tool()
    def ccu_sysvar_delete(name: str) -> str:
        """Delete a system variable by name."""
        return tools.sysvar_delete(client, name)

    # --- Program (3) ---

    @mcp.tool()
    def ccu_program_list() -> str:
        """List all programs on the CCU."""
        return tools.program_list(client)

    @mcp.tool()
    def ccu_program_get(id: str) -> str:
        """Get program details."""
        return tools.program_get(client, id)

    @mcp.tool()
    def ccu_program_execute(
        action: str = "execute",
        id: str = "",
        name: str = "",
    ) -> str:
        """Execute or delete a program. action: execute (needs id), delete (needs name)"""
        return tools.program_execute(client, action, id, name)

    # --- Events (2) ---

    @mcp.tool()
    def ccu_event_subscribe(action: str = "subscribe") -> str:
        """Subscribe or unsubscribe from CCU events. action: subscribe, unsubscribe"""
        return tools.event_subscribe(client, action)

    @mcp.tool()
    def ccu_event_poll() -> str:
        """Poll for CCU events (requires prior subscription)."""
        return tools.event_poll(client)

    # --- CCU System (4) ---

    @mcp.tool()
    def ccu_system_info() -> str:
        """Get CCU system information: version, serial, addresses, addons, language, security."""
        return tools.system_info(client)

    @mcp.tool()
    def ccu_system_config(setting: str, value: str) -> str:
        """Set CCU system config. setting: auth, ssh, ssh_password, https_redirect, snmp, security_level, language, info_led, firewall_configured"""
        return tools.system_config(client, setting, value)

    @mcp.tool()
    def ccu_system_restart(service: str) -> str:
        """Restart a CCU service. service: rega, ssh"""
        return tools.system_restart(client, service)

    @mcp.tool()
    def ccu_heating_groups() -> str:
        """List heating groups configured on the CCU."""
        return tools.heating_groups(client)

    # --- ReGa (3) ---

    @mcp.tool()
    def ccu_rega_status() -> str:
        """Check if the ReGa logic engine is running."""
        return tools.rega_status(client)

    @mcp.tool()
    def ccu_rega_script(script: str) -> str:
        """Execute a HomeMatic script on the CCU. Use with care — scripts have full system access."""
        return tools.rega_script(client, script)

    @mcp.tool()
    def ccu_rega_datapoints() -> str:
        """List all datapoints with names from the ReGa logic engine."""
        return tools.rega_datapoints(client)

    # --- Firewall (1) ---

    @mcp.tool()
    def ccu_firewall(action: str = "get", config: str = "") -> str:
        """Get or set the CCU firewall configuration. action: get, set (with JSON config)"""
        return tools.firewall(client, action, config)

    # --- Convenience (3) ---

    @mcp.tool()
    def ccu_climate(room: str = "") -> str:
        """Climate overview: temperature, humidity, valve state, set point per room. Filter by room name."""
        return tools.climate(client, room)

    @mcp.tool()
    def ccu_windows(room: str = "") -> str:
        """Window/door contact status for all rooms. Filter by room name."""
        return tools.windows(client, room)

    @mcp.tool()
    def ccu_firmware(
        action: str = "refresh",
        interface: str = "HmIP-RF",
        addresses: str = "",
    ) -> str:
        """Refresh firmware list or update device firmware. action: refresh, update (with comma-separated addresses)"""
        return tools.firmware(client, action, interface, addresses)
