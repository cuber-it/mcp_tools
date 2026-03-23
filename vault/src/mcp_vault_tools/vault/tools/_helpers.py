"""Shared helpers for vault tools — resolution, iteration, safety."""

from __future__ import annotations

import logging
import re
from pathlib import Path

from ..parser import ensure_md_extension
from ..registry import VaultConfig, VaultRegistry

logger = logging.getLogger(__name__)


def safe_resolve(vault_root: Path, rel_path: str) -> Path:
    """Resolve a relative path and ensure it stays within the vault.

    Raises ValueError on path traversal attempts.
    """
    resolved = (vault_root / rel_path).resolve()
    vault_resolved = vault_root.resolve()
    if not str(resolved).startswith(str(vault_resolved) + "/") and resolved != vault_resolved:
        raise ValueError(f"Path traversal blocked: '{rel_path}' escapes vault")
    return resolved


def resolve(registry: VaultRegistry, path: str) -> tuple[Path, Path]:
    """Resolve prefixed path to (vault_root, full_filepath)."""
    vc, rel = registry.resolve(path)
    return vc.path, safe_resolve(vc.path, ensure_md_extension(rel))


def resolve_vaults(registry: VaultRegistry, vault: str = "") -> list[VaultConfig]:
    """Resolve vault parameter to list of VaultConfigs.

    '' = default vault, 'name' = specific vault, '*' = all vaults.
    """
    if vault == "*":
        return registry.resolve_all()
    if vault:
        vc = registry.get(vault)
        if not vc:
            raise ValueError(f"Unknown vault '{vault}'")
        return [vc]
    vc, _ = registry.resolve("")
    return [vc]


def resolve_single_vault(registry: VaultRegistry, vault: str = "") -> VaultConfig:
    """Resolve to a single VaultConfig (for non-search operations)."""
    vc, _ = registry.resolve(vault + ":_" if vault else "_")
    return vc


def load_obsidianignore(vault_root: Path) -> list[str]:
    """Load .obsidianignore patterns if present."""
    ignore_file = vault_root / ".obsidianignore"
    if ignore_file.exists():
        return [
            line.strip() for line in ignore_file.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
    return []


def is_ignored(path: Path, vault_root: Path, patterns: list[str]) -> bool:
    """Check if a path matches any .obsidianignore pattern."""
    rel = str(path.relative_to(vault_root))
    for pattern in patterns:
        if re.match(pattern.replace("*", ".*"), rel):
            return True
        if rel.startswith(pattern):
            return True
    return False


def iter_notes(vault_root: Path, folder: str = "", recursive: bool = True) -> list[Path]:
    """Iterate over markdown files in a vault, respecting .obsidianignore."""
    base = vault_root / folder if folder else vault_root
    if not base.exists():
        return []
    ignore = load_obsidianignore(vault_root)
    glob_fn = base.rglob if recursive else base.glob
    files = []
    for f in sorted(glob_fn("*.md")):
        if f.name.startswith("."):
            continue
        if ignore and is_ignored(f, vault_root, ignore):
            continue
        try:
            f.relative_to(vault_root / ".obsidian")
            continue
        except ValueError:
            pass
        files.append(f)
    return files
