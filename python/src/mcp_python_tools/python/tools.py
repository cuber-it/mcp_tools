"""Pure tool logic for python — no MCP dependency."""

from __future__ import annotations

def py_version() -> str:
    """Show Python version and path"""
    # TODO: implement
    raise NotImplementedError("py_version")


def py_pip_list(filter: str = "", outdated: bool = False) -> str:
    """List installed packages"""
    # TODO: implement
    raise NotImplementedError("py_pip_list")


def py_pip_install(package: str, upgrade: bool = False) -> str:
    """Install a package"""
    # TODO: implement
    raise NotImplementedError("py_pip_install")


def py_pip_show(package: str) -> str:
    """Show package details"""
    # TODO: implement
    raise NotImplementedError("py_pip_show")


def py_pip_uninstall(package: str) -> str:
    """Uninstall a package"""
    # TODO: implement
    raise NotImplementedError("py_pip_uninstall")


def py_venv_create(path: str = ".venv", python: str = "python3") -> str:
    """Create a virtual environment"""
    # TODO: implement
    raise NotImplementedError("py_venv_create")


def py_venv_info(path: str = ".venv") -> str:
    """Show venv info (path, Python version, packages count)"""
    # TODO: implement
    raise NotImplementedError("py_venv_info")


def py_run(code: str, timeout: int = 30) -> str:
    """Run a Python expression and return result"""
    # TODO: implement
    raise NotImplementedError("py_run")

