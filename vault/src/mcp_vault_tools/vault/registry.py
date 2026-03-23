"""Multi-vault registry — named vaults with prefix syntax.

Path syntax:
  "note.md"           → default vault
  "arbeit:note.md"    → vault named 'arbeit'
  "*:query"           → all vaults (for search)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .index import VaultIndex


@dataclass
class VaultConfig:
    """Configuration for a single vault."""
    name: str
    path: Path
    max_results: int = 50
    daily_format: str = "%Y-%m-%d"
    inbox_path: str = "inbox.md"
    template_dir: str = "_templates"


class VaultRegistry:
    """Registry of named vaults with prefix-based routing."""

    def __init__(self, config: dict):
        self._vaults: dict[str, VaultConfig] = {}
        self._default: str = config.get("default_vault", "")
        self._global_max_results = config.get("max_results", 50)
        self._global_daily_format = config.get("daily_format", "%Y-%m-%d")
        self._global_inbox_path = config.get("inbox_path", "inbox.md")
        self._global_template_dir = config.get("template_dir", "_templates")

        vaults = config.get("vaults", {})
        if isinstance(vaults, dict):
            for name, vault_conf in vaults.items():
                if isinstance(vault_conf, str):
                    vault_conf = {"path": vault_conf}
                path = Path(vault_conf["path"]).expanduser().resolve()
                self._vaults[name] = VaultConfig(
                    name=name,
                    path=path,
                    max_results=vault_conf.get("max_results", self._global_max_results),
                    daily_format=vault_conf.get("daily_format", self._global_daily_format),
                    inbox_path=vault_conf.get("inbox_path", self._global_inbox_path),
                    template_dir=vault_conf.get("template_dir", self._global_template_dir),
                )

        # Single vault_path fallback (backward compat)
        if not self._vaults and "vault_path" in config:
            path = Path(config["vault_path"]).expanduser().resolve()
            self._vaults["default"] = VaultConfig(
                name="default",
                path=path,
                max_results=self._global_max_results,
            )
            self._default = "default"

        # Auto-set default if only one vault
        if not self._default and len(self._vaults) == 1:
            self._default = next(iter(self._vaults))

    def resolve(self, prefixed_path: str) -> tuple[VaultConfig, str]:
        """Resolve a prefixed path into (vault_config, relative_path).

        'note.md'         → (default_vault, 'note.md')
        'arbeit:note.md'  → (arbeit_vault, 'note.md')

        Raises ValueError for unknown vault names or missing default.
        """
        if ":" in prefixed_path:
            vault_name, rel_path = prefixed_path.split(":", 1)
            if vault_name == "*":
                raise ValueError("Use resolve_all() for wildcard vault queries")
            if vault_name not in self._vaults:
                available = ", ".join(sorted(self._vaults.keys()))
                raise ValueError(f"Unknown vault '{vault_name}'. Available: {available}")
            return self._vaults[vault_name], rel_path

        if not self._default:
            available = ", ".join(sorted(self._vaults.keys()))
            raise ValueError(f"No default vault configured. Use prefix: {available}")
        if self._default not in self._vaults:
            raise ValueError(f"Default vault '{self._default}' not found in config")

        return self._vaults[self._default], prefixed_path

    def resolve_all(self) -> list[VaultConfig]:
        """Return all configured vaults (for wildcard operations)."""
        return list(self._vaults.values())

    def get(self, name: str) -> VaultConfig | None:
        """Get a vault by name."""
        return self._vaults.get(name)

    def list_vaults(self) -> list[VaultConfig]:
        """List all configured vaults."""
        return list(self._vaults.values())

    def get_index(self, vault_name: str = "") -> "VaultIndex":
        """Get or create a VaultIndex for a vault. Lazy initialization."""
        from .index import VaultIndex
        name = vault_name or self._default
        vc = self._vaults.get(name)
        if not vc:
            raise ValueError(f"Unknown vault '{name}'")
        if not hasattr(vc, "_index") or vc._index is None:
            vc._index = VaultIndex(vc.path)
        return vc._index

    @property
    def default_name(self) -> str:
        return self._default
