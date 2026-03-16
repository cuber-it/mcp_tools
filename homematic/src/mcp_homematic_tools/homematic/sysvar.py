"""System variable tools for HomeMatic CCU."""

from __future__ import annotations

import json

from .client import CCUClient


def sysvar_list(client: CCUClient) -> str:
    """List all system variables."""
    result = client.call("SysVar.getAll")
    return json.dumps(result, indent=2, ensure_ascii=False)


def sysvar_get(client: CCUClient, id: str = "", name: str = "") -> str:
    """Get a system variable value by ID or name."""
    if name:
        result = client.call("SysVar.getValueByName", {"name": name})
        return json.dumps({"name": name, "value": result}, indent=2, ensure_ascii=False)
    if id:
        detail = client.call("SysVar.get", {"id": id})
        value = client.call("SysVar.getValue", {"id": id})
        detail["currentValue"] = value
        return json.dumps(detail, indent=2, ensure_ascii=False)
    return "Error: provide either id or name"


def sysvar_set(client: CCUClient, id: str, value: str) -> str:
    """Set a system variable value.

    Determines the correct API method (setBool/setFloat/setEnum)
    by querying the variable type first.
    """
    detail = client.call("SysVar.get", {"id": id})
    var_type = detail.get("type", "").upper()

    if var_type in ("LOGIC", "ALARM", "BOOL"):
        bool_val = value.lower() in ("true", "1", "yes")
        client.call("SysVar.setBool", {"id": id, "value": bool_val})
    elif var_type in ("NUMBER", "FLOAT"):
        client.call("SysVar.setFloat", {"id": id, "value": float(value)})
    elif var_type == "ENUM":
        client.call("SysVar.setEnum", {"id": id, "value": value})
    else:
        return f"Unknown variable type '{var_type}' for variable {id}"

    return f"SysVar {id} ({detail.get('name', '?')}) set to {value}"


def sysvar_create(
    client: CCUClient,
    name: str,
    var_type: str,
    init_value: str = "",
    min_value: str = "",
    max_value: str = "",
    enum_values: str = "",
) -> str:
    """Create a new system variable."""
    vt = var_type.lower()
    if vt == "bool":
        params = {"name": name, "init_val": init_value.lower() in ("true", "1") if init_value else False}
        client.call("SysVar.createBool", params)
    elif vt == "float":
        params: dict = {"name": name}
        if init_value:
            params["init_val"] = float(init_value)
        if min_value:
            params["minValue"] = float(min_value)
        if max_value:
            params["maxValue"] = float(max_value)
        client.call("SysVar.createFloat", params)
    elif vt == "enum":
        params = {"name": name, "init_val": init_value or "0"}
        if enum_values:
            params["valueList"] = enum_values
        client.call("SysVar.createEnum", params)
    else:
        return f"Unknown type '{var_type}' (use: bool, float, enum)"

    return f"SysVar '{name}' ({var_type}) created"


def sysvar_delete(client: CCUClient, name: str) -> str:
    """Delete a system variable by name."""
    client.call("SysVar.deleteSysVarByName", {"name": name})
    return f"SysVar '{name}' deleted"
