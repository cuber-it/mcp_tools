"""Room and Subsection (Function/Gewerk) tools for HomeMatic CCU."""

from __future__ import annotations

import json

from .client import CCUClient


# ---------------------------------------------------------------------------
# Room tools
# ---------------------------------------------------------------------------

def room_list(client: CCUClient) -> str:
    """List all rooms with their channels."""
    result = client.call("Room.getAll")
    return json.dumps(result, indent=2, ensure_ascii=False)


def room_get(client: CCUClient, id: str) -> str:
    """Get room details and associated programs."""
    room = client.call("Room.get", {"id": id})
    try:
        programs = client.call("Room.listProgramIds", {"id": id})
        room["programIds"] = programs
    except Exception:
        # listProgramIds has a known bug on some CCU firmware versions
        room["programIds"] = []
    return json.dumps(room, indent=2, ensure_ascii=False)


def room_channel(client: CCUClient, action: str, room_id: str, channel_id: str) -> str:
    """Add or remove a channel from a room."""
    if action == "add":
        client.call("Room.addChannel", {"id": room_id, "channelId": channel_id})
        return f"Channel {channel_id} added to room {room_id}"
    elif action == "remove":
        client.call("Room.removeChannel", {"id": room_id, "channelId": channel_id})
        return f"Channel {channel_id} removed from room {room_id}"
    return f"Unknown action '{action}' (use: add, remove)"


# ---------------------------------------------------------------------------
# Subsection (Function/Gewerk) tools
# ---------------------------------------------------------------------------

def function_list(client: CCUClient) -> str:
    """List all functions (Gewerke) with their channels."""
    result = client.call("Subsection.getAll")
    return json.dumps(result, indent=2, ensure_ascii=False)


def function_get(client: CCUClient, id: str) -> str:
    """Get function details and associated programs."""
    func = client.call("Subsection.get", {"id": id})
    try:
        programs = client.call("Subsection.listProgramIds", {"id": id})
        func["programIds"] = programs
    except Exception:
        # listProgramIds has a known bug on some CCU firmware versions
        func["programIds"] = []
    return json.dumps(func, indent=2, ensure_ascii=False)


def function_channel(client: CCUClient, action: str, function_id: str, channel_id: str) -> str:
    """Add or remove a channel from a function."""
    if action == "add":
        client.call("Subsection.addChannel", {"id": function_id, "channelId": channel_id})
        return f"Channel {channel_id} added to function {function_id}"
    elif action == "remove":
        client.call("Subsection.removeChannel", {"id": function_id, "channelId": channel_id})
        return f"Channel {channel_id} removed from function {function_id}"
    return f"Unknown action '{action}' (use: add, remove)"
