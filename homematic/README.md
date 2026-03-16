# mcp-homematic-tools

**60 MCP tools for HomeMatic CCU3 / OpenCCU** — full JSON-RPC API coverage.

Control your HomeMatic smart home through the [Model Context Protocol](https://modelcontextprotocol.io/).
Works standalone or as a plugin for [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

## What you get

| Category | Tools | What they do |
|---|---|---|
| **Device** | 6 | List, inspect, rename, test devices |
| **Channel** | 5 | Read values, configure channels |
| **Interface — Values** | 6 | Read/write individual values and parameter sets |
| **Interface — Diagnostics** | 6 | RSSI, DutyCycle, service messages, device descriptions |
| **Interface — Pairing** | 6 | Teach-in, delete, replace devices; manage links |
| **Interface — Misc** | 4 | BidCoS assignment, metadata, config cache, thermostat party mode |
| **Room** | 3 | List rooms, manage channel assignments |
| **Function** | 3 | List Gewerke, manage channel assignments |
| **System Variables** | 5 | List, read, write, create, delete system variables |
| **Programs** | 3 | List, inspect, execute CCU programs |
| **Events** | 2 | Subscribe and poll for device events |
| **CCU System** | 4 | System info, configuration, service restart, heating groups |
| **ReGa** | 3 | Logic engine status, script execution, datapoints |
| **Firewall** | 1 | Read/write CCU firewall config |
| **Convenience** | 3 | Climate overview, window status, firmware management |

## Supported hardware

- **CCU3** (original eQ-3 hardware)
- **OpenCCU** (Raspberry Pi with RPI-RF-MOD)
- **RaspberryMatic**
- Any system exposing the HomeMatic JSON-RPC API at `/api/homematic.cgi`

## Installation

```bash
pip install mcp-homematic-tools
```

## Dual use: MCP server + Python library

This package works in two ways:

- **As an MCP server** — usable by any MCP client (AI agents, IDE plugins, custom integrations)
- **As a Python library** — import the functions directly, no MCP required

```python
from mcp_homematic_tools.homematic.client import CCUClient
from mcp_homematic_tools.homematic.device import device_list
from mcp_homematic_tools.homematic.convenience import climate_overview

client = CCUClient("http://192.168.178.53", "Admin", "secret")
print(device_list(client))
print(climate_overview(client))
```

The MCP layer is a thin wrapper around plain Python functions. Use them in scripts, dashboards, monitoring jobs, or any application — no protocol overhead needed.

## Standalone usage

```bash
mcp-homematic-tools --url http://192.168.178.53 --username Admin --password secret
```

Or with a config file:

```yaml
# config.yaml
url: "http://192.168.178.53"
username: "Admin"
password: "your-password"
```

```bash
mcp-homematic-tools --config config.yaml
```

## Plugin usage

Register as a plugin in [mcp-server-proxy](https://pypi.org/project/mcp-server-proxy/):

```yaml
# autoload in proxy config
autoload:
  - mcp_homematic_tools.homematic
```

With plugin config in your plugin directory:

```yaml
# homematic/config.yaml
description: "HomeMatic CCU"
url: "http://192.168.178.53"
username: "Admin"
password: "your-password"
```

## Tool reference

### Device tools

| Tool | Parameters | Returns | Description |
|---|---|---|---|
| `ccu_device_list` | `detail: bool = false` | JSON array of device IDs or full device objects with channels | List all configured devices |
| `ccu_device_get` | `id: str` | JSON object with device details (name, address, type, interface, channels) | Get detail info for a single device |
| `ccu_device_status` | `id: str` | JSON object with status (connectivity, battery, config pending) | Get status info for a device |
| `ccu_device_set_name` | `id: str, name: str` | Confirmation string | Set the name of a device |
| `ccu_device_set_visibility` | `id: str, visibility?: str, operate_group_only?: str, enabled_service_msg?: str` | Confirmation with applied settings | Set visibility, operability, service messages (each "true"/"false" or empty to skip) |
| `ccu_device_comtest` | `id: str, action: str = "start"` | Status message or JSON test result | Start or poll a communication test. action: `start`, `poll` |

### Channel tools

| Tool | Parameters | Returns | Description |
|---|---|---|---|
| `ccu_channel_value` | `id: str` | JSON with channel value | Get the current value of a channel |
| `ccu_channel_info` | `id: str` | JSON `{id, name, type}` | Get name and type of a channel |
| `ccu_channel_set_name` | `id: str, name: str` | Confirmation string | Set the name of a channel |
| `ccu_channel_config` | `id: str, logging?: str, mode?: str, visibility?: str, usability?: str` | Confirmation with applied settings | Set logging, transmission mode (STANDARD/SECURED), visibility, usability |
| `ccu_channel_programs` | `id: str` | JSON with program IDs or "not used" message | List programs using this channel |

### Interface — Values

| Tool | Parameters | Returns | Description |
|---|---|---|---|
| `ccu_get_value` | `interface: str, address: str, value_key: str` | JSON `{interface, address, key, value}` | Read a single value. Example: `interface="HmIP-RF", address="SERIAL:1", value_key="ACTUAL_TEMPERATURE"` |
| `ccu_set_value` | `interface: str, address: str, value_key: str, value: str, value_type: str = "double"` | Confirmation string | Set a value. value_type: `double`, `bool`, `int`, `string` |
| `ccu_get_paramset` | `interface: str, address: str, paramset_key: str = "VALUES"` | JSON object with all parameters | Read a complete parameter set. paramset_key: `VALUES` (live data), `MASTER` (config) |
| `ccu_get_paramset_desc` | `interface: str, address: str, paramset_key: str = "VALUES"` | JSON with parameter descriptions, types, min/max values | Describe available parameters and their types |
| `ccu_put_paramset` | `interface: str, address: str, paramset_key: str, values: str` | Confirmation string | Write a complete parameter set. values: JSON object |
| `ccu_get_master_value` | `interface: str, address: str, value_key: str` | JSON `{address, key, value}` | Read a value from the MASTER (config) parameter set |

### Interface — Diagnostics

| Tool | Parameters | Returns | Description |
|---|---|---|---|
| `ccu_list_interfaces` | — | JSON array `[{name, port, info, isPresent}]` | List interfaces (HmIP-RF, BidCos-RF, VirtualDevices) with running status |
| `ccu_list_devices_raw` | `interface: str = "HmIP-RF"` | JSON array of raw device descriptors from the interface layer | List all learned devices on an interface |
| `ccu_device_description` | `interface: str, address: str` | JSON with device/channel descriptor (type, firmware, paramsets) | Get device or channel description from interface |
| `ccu_rssi` | `interface: str = ""` | JSON object mapping addresses to RSSI values | Get signal strength of all devices. Empty = all interfaces |
| `ccu_duty_cycle` | — | JSON array of gateway DutyCycle values | Get DutyCycle of all gateways (max 1% per hour rule) |
| `ccu_service_messages` | `action: str = "count", interface?: str, address?: str, parameter_id?: str` | JSON count, suppressed list, or confirmation | action: `count`, `list_suppressed`, `suppress` |

### Interface — Pairing / Links

| Tool | Parameters | Returns | Description |
|---|---|---|---|
| `ccu_add_device` | `action: str = "status", interface: str = "HmIP-RF", serial?: str, mode_duration: int = 60` | JSON status or confirmation | action: `add` (teach-in by serial), `enable_mode` (start pairing), `status` (check timer) |
| `ccu_delete_device` | `interface: str, address: str, flags: int = 0` | Confirmation string | Delete a device from the CCU |
| `ccu_change_device` | `interface: str, old_address: str, new_address: str` | Confirmation string | Replace a device (keeps config and links) |
| `ccu_links` | `interface: str, address: str, flags: int = 0` | JSON array of direct links | List all direct links for a device or channel |
| `ccu_add_link` | `interface: str, sender: str, receiver: str, name?: str, description?: str` | Confirmation string | Create a direct link between two channels |
| `ccu_remove_link` | `interface: str, sender: str, receiver: str` | Confirmation string | Remove a direct link |

### Interface — Misc

| Tool | Parameters | Returns | Description |
|---|---|---|---|
| `ccu_set_bidcos_interface` | `action: str = "list", address?: str, interface_id?: str` | JSON interface list or confirmation | action: `list` (show BidCoS interfaces), `set` (assign device) |
| `ccu_metadata` | `action: str = "get", object_id: str, key: str, value?: str` | JSON value or confirmation | action: `get`, `set`, `remove` — read/write metadata on objects |
| `ccu_config_cache` | `action: str = "clear", interface: str, address: str` | Confirmation string | action: `clear` (delete cached config), `restore` (re-send config to device) |
| `ccu_thermostat_party` | `interface: str, address: str, values: str` | Confirmation string | Set party mode. values: JSON with party mode parameters |

### Room tools

| Tool | Parameters | Returns | Description |
|---|---|---|---|
| `ccu_room_list` | — | JSON array `[{id, name, description, channelIds}]` | List all rooms with assigned channels |
| `ccu_room_get` | `id: str` | JSON room object with programIds | Get room details and associated programs |
| `ccu_room_channel` | `action: str, room_id: str, channel_id: str` | Confirmation string | action: `add`, `remove` — manage channel-room assignments |

### Function (Gewerk) tools

| Tool | Parameters | Returns | Description |
|---|---|---|---|
| `ccu_function_list` | — | JSON array `[{id, name, description, channelIds}]` | List all functions with assigned channels |
| `ccu_function_get` | `id: str` | JSON function object with programIds | Get function details and associated programs |
| `ccu_function_channel` | `action: str, function_id: str, channel_id: str` | Confirmation string | action: `add`, `remove` — manage channel-function assignments |

### System variable tools

| Tool | Parameters | Returns | Description |
|---|---|---|---|
| `ccu_sysvar_list` | — | JSON array with all variables (id, name, type, value, min/max) | List all system variables |
| `ccu_sysvar_get` | `id?: str, name?: str` | JSON variable detail with currentValue | Get variable by ID or name |
| `ccu_sysvar_set` | `id: str, value: str` | Confirmation string | Set a variable (type auto-detected: bool/float/enum) |
| `ccu_sysvar_create` | `name: str, var_type: str, init_value?: str, min_value?: str, max_value?: str, enum_values?: str` | Confirmation string | Create a variable. var_type: `bool`, `float`, `enum`. enum_values: semicolon-separated |
| `ccu_sysvar_delete` | `name: str` | Confirmation string | Delete a system variable by name |

### Program tools

| Tool | Parameters | Returns | Description |
|---|---|---|---|
| `ccu_program_list` | — | JSON array of programs or "No programs" | List all CCU programs |
| `ccu_program_get` | `id: str` | JSON program details (name, active, conditions, last execute) | Get program details |
| `ccu_program_execute` | `action: str = "execute", id?: str, name?: str` | Confirmation string | action: `execute` (needs id), `delete` (needs name) |

### Event tools

| Tool | Parameters | Returns | Description |
|---|---|---|---|
| `ccu_event_subscribe` | `action: str = "subscribe"` | JSON `{subscribed: bool}` | action: `subscribe`, `unsubscribe` — manage event subscription |
| `ccu_event_poll` | — | JSON array of events or "No events" | Poll for events (requires prior subscription) |

### CCU system tools

| Tool | Parameters | Returns | Description |
|---|---|---|---|
| `ccu_system_info` | — | JSON `{version, serial, address, hmipAddress, addonVersions, language, securityLevel, sshState, authEnabled}` | Get CCU system information |
| `ccu_system_config` | `setting: str, value: str` | Confirmation string | Settings: `auth`, `ssh`, `ssh_password`, `https_redirect`, `snmp`, `security_level`, `language`, `info_led`, `firewall_configured` |
| `ccu_system_restart` | `service: str` | Confirmation string | service: `rega`, `ssh` |
| `ccu_heating_groups` | — | JSON array of heating groups | List heating groups |

### ReGa tools

| Tool | Parameters | Returns | Description |
|---|---|---|---|
| `ccu_rega_status` | — | JSON `{regaPresent: bool}` | Check if the logic engine is running |
| `ccu_rega_script` | `script: str` | Script output (string or JSON) | Execute a HomeMatic script — full system access, use with care |
| `ccu_rega_datapoints` | — | JSON array of all datapoints with names | List all datapoints from the logic engine |

### Firewall

| Tool | Parameters | Returns | Description |
|---|---|---|---|
| `ccu_firewall` | `action: str = "get", config?: str` | JSON config or confirmation | action: `get` (read config), `set` (write JSON config) |

### Convenience tools

| Tool | Parameters | Returns | Description |
|---|---|---|---|
| `ccu_climate` | `room: str = ""` | JSON array `[{room, devices: [{device, type, temperature, humidity, setPoint, valveLevel, boostMode}]}]` | Climate overview for all rooms. Filter by room name |
| `ccu_windows` | `room: str = ""` | JSON array `[{room, contacts: [{device, state: "open"/"closed", rawState}]}]` | Window/door contact status. Filter by room name |
| `ccu_firmware` | `action: str = "refresh", interface: str = "HmIP-RF", addresses?: str` | Confirmation string | action: `refresh` (update firmware list), `update` (flash devices, comma-separated addresses) |

## Common value keys

| Device type | Channel | Key | Type | Description |
|---|---|---|---|---|
| HmIP-eTRV-B-2 | :1 | ACTUAL_TEMPERATURE | double | Current temperature |
| HmIP-eTRV-B-2 | :1 | SET_POINT_TEMPERATURE | double | Target temperature |
| HmIP-eTRV-B-2 | :1 | LEVEL | double | Valve opening (0.0-1.0) |
| HmIP-eTRV-B-2 | :1 | BOOST_MODE | bool | Boost active |
| HmIP-STHD | :1 | ACTUAL_TEMPERATURE | double | Current temperature |
| HmIP-STHD | :1 | HUMIDITY | int | Relative humidity % |
| HmIP-SWDO-2 | :1 | STATE | bool | Contact state (false=closed) |
| any | :0 | LOW_BAT | bool | Battery low |
| any | :0 | OPERATING_VOLTAGE | double | Battery voltage |
| any | :0 | RSSI_DEVICE | int | Signal strength |
| any | :0 | UNREACH | bool | Device unreachable |

## API coverage

This package wraps the complete HomeMatic JSON-RPC API (minus destructive system operations like SafeMode/RecoveryMode and low-level RF key management). Session handling (login, renew, logout) is managed automatically by the client.

## Security

Credentials are passed via config file or command line, never hardcoded. The CCU JSON-RPC API uses session-based authentication. Sessions are renewed automatically and cleaned up on exit.

For production deployments, restrict network access to the CCU and use a dedicated API user if your CCU firmware supports it.

## License

MIT
