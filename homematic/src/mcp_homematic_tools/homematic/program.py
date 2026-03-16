"""Program tools for HomeMatic CCU."""

from __future__ import annotations

import json

from .client import CCUClient


def program_list(client: CCUClient) -> str:
    """List all programs."""
    result = client.call("Program.getAll")
    if not result:
        return "No programs configured"
    return json.dumps(result, indent=2, ensure_ascii=False)


def program_get(client: CCUClient, id: str) -> str:
    """Get program details."""
    result = client.call("Program.get", {"id": id})
    return json.dumps(result, indent=2, ensure_ascii=False)


def program_execute(
    client: CCUClient,
    action: str = "execute",
    id: str = "",
    name: str = "",
) -> str:
    """Execute or delete a program."""
    if action == "execute":
        if not id:
            return "Error: program ID required for execute"
        client.call("Program.execute", {"id": id})
        return f"Program {id} executed"
    elif action == "delete":
        if not name:
            return "Error: program name required for delete"
        client.call("Program.deleteProgramByName", {"name": name})
        return f"Program '{name}' deleted"
    return f"Unknown action '{action}' (use: execute, delete)"
