"""Re-export all tool functions for direct use."""

from .device import (
    device_list,
    device_get,
    device_status,
    device_set_name,
    device_set_visibility,
    device_comtest,
    channel_value,
    channel_info,
    channel_set_name,
    channel_config,
    channel_programs,
)
from .interface import (
    get_value,
    set_value,
    get_paramset,
    get_paramset_desc,
    put_paramset,
    get_master_value,
    list_interfaces,
    list_devices_raw,
    device_description,
    rssi,
    duty_cycle,
    service_messages,
    add_device,
    delete_device,
    change_device,
    links,
    add_link,
    remove_link,
    set_bidcos_interface,
    metadata,
    config_cache,
    thermostat_party,
)
from .room import (
    room_list,
    room_get,
    room_channel,
    function_list,
    function_get,
    function_channel,
)
from .sysvar import (
    sysvar_list,
    sysvar_get,
    sysvar_set,
    sysvar_create,
    sysvar_delete,
)
from .program import (
    program_list,
    program_get,
    program_execute,
)
from .system import (
    system_info,
    system_config,
    system_restart,
    heating_groups,
    rega_status,
    rega_script,
    rega_datapoints,
    firewall,
    event_subscribe,
    event_poll,
)
from .convenience import (
    climate,
    windows,
    firmware,
)

__all__ = [
    # Device (6)
    "device_list", "device_get", "device_status",
    "device_set_name", "device_set_visibility", "device_comtest",
    # Channel (5)
    "channel_value", "channel_info", "channel_set_name",
    "channel_config", "channel_programs",
    # Interface — Values (6)
    "get_value", "set_value", "get_paramset",
    "get_paramset_desc", "put_paramset", "get_master_value",
    # Interface — Diagnostics (6)
    "list_interfaces", "list_devices_raw", "device_description",
    "rssi", "duty_cycle", "service_messages",
    # Interface — Pairing/Links (6)
    "add_device", "delete_device", "change_device",
    "links", "add_link", "remove_link",
    # Interface — Misc (4)
    "set_bidcos_interface", "metadata", "config_cache", "thermostat_party",
    # Room (3)
    "room_list", "room_get", "room_channel",
    # Function/Gewerk (3)
    "function_list", "function_get", "function_channel",
    # SysVar (5)
    "sysvar_list", "sysvar_get", "sysvar_set",
    "sysvar_create", "sysvar_delete",
    # Program (3)
    "program_list", "program_get", "program_execute",
    # System (4)
    "system_info", "system_config", "system_restart", "heating_groups",
    # ReGa (3)
    "rega_status", "rega_script", "rega_datapoints",
    # Firewall (1)
    "firewall",
    # Events (2)
    "event_subscribe", "event_poll",
    # Convenience (3)
    "climate", "windows", "firmware",
]
