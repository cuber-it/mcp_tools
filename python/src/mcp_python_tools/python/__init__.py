"""Python — MCP plugin.

Python environment tools for MCP — venvs, pip, packages, interpreter info
"""

from __future__ import annotations

from . import tools


def register(mcp, config: dict) -> None:
    """Register python tools as MCP tools."""
    @mcp.tool()
    def py_version() -> str:
        """Show Python version and path"""
        return tools.py_version()

    @mcp.tool()
    def py_pip_list(filter: str = "", outdated: bool = False) -> str:
        """List installed packages"""
        return tools.py_pip_list(filter, outdated)

    @mcp.tool()
    def py_pip_install(package: str, upgrade: bool = False) -> str:
        """Install a package"""
        return tools.py_pip_install(package, upgrade)

    @mcp.tool()
    def py_pip_show(package: str) -> str:
        """Show package details"""
        return tools.py_pip_show(package)

    @mcp.tool()
    def py_pip_uninstall(package: str) -> str:
        """Uninstall a package"""
        return tools.py_pip_uninstall(package)

    @mcp.tool()
    def py_venv_create(path: str = ".venv", python: str = "python3") -> str:
        """Create a virtual environment"""
        return tools.py_venv_create(path, python)

    @mcp.tool()
    def py_venv_info(path: str = ".venv") -> str:
        """Show venv info (path, Python version, packages count)"""
        return tools.py_venv_info(path)

    @mcp.tool()
    def py_run(code: str, timeout: int = 30) -> str:
        """Run a Python expression and return result"""
        return tools.py_run(code, timeout)
