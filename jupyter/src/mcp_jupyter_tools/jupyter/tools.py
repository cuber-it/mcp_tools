"""Pure tool logic for jupyter — no MCP dependency."""

from __future__ import annotations

from .client import JupyterClient

def notebook_list(client: JupyterClient, path: str = "") -> str:
    """List notebooks in a directory"""
    # TODO: implement
    raise NotImplementedError("notebook_list")


def notebook_read(client: JupyterClient, path: str) -> str:
    """Read a notebook (cells with outputs)"""
    # TODO: implement
    raise NotImplementedError("notebook_read")


def notebook_create(client: JupyterClient, path: str, kernel: str = "python3") -> str:
    """Create a new notebook"""
    # TODO: implement
    raise NotImplementedError("notebook_create")


def notebook_add_cell(client: JupyterClient, path: str, source: str, cell_type: str = "code", position: int = -1) -> str:
    """Add a cell to a notebook"""
    # TODO: implement
    raise NotImplementedError("notebook_add_cell")


def notebook_execute(client: JupyterClient, path: str, cell_index: int = -1) -> str:
    """Execute a notebook or specific cell"""
    # TODO: implement
    raise NotImplementedError("notebook_execute")


def notebook_export(client: JupyterClient, path: str, format: str = "html") -> str:
    """Export notebook to another format"""
    # TODO: implement
    raise NotImplementedError("notebook_export")


def kernel_list(client: JupyterClient) -> str:
    """List running kernels"""
    # TODO: implement
    raise NotImplementedError("kernel_list")


def kernel_start(client: JupyterClient, kernel_name: str = "python3") -> str:
    """Start a new kernel"""
    # TODO: implement
    raise NotImplementedError("kernel_start")


def kernel_interrupt(client: JupyterClient, kernel_id: str) -> str:
    """Interrupt a running kernel"""
    # TODO: implement
    raise NotImplementedError("kernel_interrupt")


def kernel_restart(client: JupyterClient, kernel_id: str) -> str:
    """Restart a kernel"""
    # TODO: implement
    raise NotImplementedError("kernel_restart")


def hub_user_list(client: JupyterClient) -> str:
    """List JupyterHub users"""
    # TODO: implement
    raise NotImplementedError("hub_user_list")


def hub_user_info(client: JupyterClient, username: str) -> str:
    """Get info about a JupyterHub user"""
    # TODO: implement
    raise NotImplementedError("hub_user_info")


def hub_server_start(client: JupyterClient, username: str) -> str:
    """Start a user's JupyterHub server"""
    # TODO: implement
    raise NotImplementedError("hub_server_start")


def hub_server_stop(client: JupyterClient, username: str) -> str:
    """Stop a user's JupyterHub server"""
    # TODO: implement
    raise NotImplementedError("hub_server_stop")

