"""Test fixtures — temporary vault with diverse test notes."""

import pytest
from pathlib import Path

from mcp_vault_tools.vault.registry import VaultRegistry


@pytest.fixture
def vault_dir(tmp_path):
    """Create a temporary vault with test notes."""
    vault = tmp_path / "vault"
    vault.mkdir()

    # --- Simple note ---
    (vault / "simple.md").write_text(
        "---\ntitle: Simple Note\ntags: [test, simple]\n---\n\nThis is a simple note.\n"
    )

    # --- Note with WikiLinks ---
    (vault / "linked.md").write_text(
        "---\ntitle: Linked Note\ntags: [test]\n---\n\n"
        "This links to [[simple]] and [[deep/nested]].\n"
        "Also a heading link: [[simple#section-one]].\n"
        "And a block ref: [[simple#^block-123]].\n"
        "Embed: ![[image.png]]\n"
        "Note embed: ![[simple]]\n"
    )

    # --- Nested note ---
    deep = vault / "deep"
    deep.mkdir()
    (deep / "nested.md").write_text(
        "---\ntitle: Nested Note\ntags: [test, deep/nested/tag]\n---\n\n"
        "A nested note that links back to [[linked]].\n"
    )

    # --- Orphan (no incoming links) ---
    (vault / "orphan.md").write_text(
        "---\ntitle: Orphan Note\ntags: [lonely]\n---\n\nNobody links to me.\n"
    )

    # --- Dead end (outgoing but no incoming) ---
    (vault / "dead-end.md").write_text(
        "---\ntitle: Dead End\ntags: [test]\n---\n\n"
        "I link to [[simple]] but nobody links to me.\n"
    )

    # --- Hub (many links) ---
    (vault / "hub.md").write_text(
        "---\ntitle: Hub Note\ntags: [test, hub]\n---\n\n"
        "Central note: [[simple]], [[linked]], [[deep/nested]], [[orphan]], [[dead-end]].\n"
    )

    # --- Note with aliases ---
    (vault / "aliased.md").write_text(
        "---\ntitle: Aliased Note\naliases: [Alias One, Alias Two]\ntags: [test]\n---\n\n"
        "This note has aliases.\n"
    )

    # --- Note linking by alias ---
    (vault / "uses-alias.md").write_text(
        "---\ntitle: Uses Alias\ntags: [test]\n---\n\n"
        "Links via alias: [[Alias One]].\n"
    )

    # --- No frontmatter ---
    (vault / "bare.md").write_text(
        "Just a bare note with no frontmatter.\n\nInline #tag-here and #test.\n"
    )

    # --- Empty frontmatter ---
    (vault / "empty-fm.md").write_text(
        "---\n---\n\nEmpty frontmatter.\n"
    )

    # --- Hierarchical tags ---
    (vault / "tagged.md").write_text(
        "---\ntitle: Tagged\ntags: [food/recipe/pasta, food/italian]\n---\n\n"
        "Also has inline #coding/python tag.\n"
    )

    # --- Code blocks (links/tags inside should be ignored) ---
    (vault / "code.md").write_text(
        "---\ntitle: Code Note\ntags: [test]\n---\n\n"
        "Normal text with [[simple]] link.\n\n"
        "```python\n# This [[not-a-link]] and #not-a-tag should be ignored\n```\n\n"
        "Inline `[[also-not-a-link]]` ignored too.\n"
    )

    # --- Template ---
    templates = vault / "_templates"
    templates.mkdir()
    (templates / "meeting.md").write_text(
        "---\ntitle: Meeting {{title}}\ndate: {{date}}\ntags: [meeting]\n---\n\n"
        "# {{title}}\n\n## Attendees\n\n## Notes\n\n## Action Items\n"
    )

    # --- .obsidianignore ---
    (vault / ".obsidianignore").write_text(
        "# Ignore templates in search\n_templates\n"
    )

    # --- .obsidian directory (should always be skipped) ---
    obsidian_dir = vault / ".obsidian"
    obsidian_dir.mkdir()
    (obsidian_dir / "types.json").write_text(
        '{"types": {"title": "text", "tags": "multitext", "date": "date"}}'
    )

    return vault


@pytest.fixture
def registry(vault_dir):
    """Create a VaultRegistry with the test vault."""
    return VaultRegistry({
        "default_vault": "test",
        "vaults": {
            "test": {"path": str(vault_dir)},
        },
    })


@pytest.fixture
def multi_registry(tmp_path):
    """Create a VaultRegistry with multiple vaults."""
    vault_a = tmp_path / "vault_a"
    vault_a.mkdir()
    (vault_a / "note-a.md").write_text("---\ntitle: Note A\ntags: [alpha]\n---\n\nIn vault A.\n")

    vault_b = tmp_path / "vault_b"
    vault_b.mkdir()
    (vault_b / "note-b.md").write_text("---\ntitle: Note B\ntags: [beta]\n---\n\nIn vault B.\n")

    return VaultRegistry({
        "default_vault": "alpha",
        "vaults": {
            "alpha": {"path": str(vault_a)},
            "beta": {"path": str(vault_b)},
        },
    })
