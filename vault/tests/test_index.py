"""Tests for VaultIndex and vault_query."""

import json
from pathlib import Path

from mcp_vault_tools.vault import tools
from mcp_vault_tools.vault.index import VaultIndex


class TestVaultIndex:

    def test_build(self, vault_dir):
        idx = VaultIndex(vault_dir)
        count = idx.build()
        assert count > 0

    def test_get_entry(self, vault_dir):
        idx = VaultIndex(vault_dir)
        idx.build()
        entry = idx.get("simple.md")
        assert entry is not None
        assert entry.frontmatter["title"] == "Simple Note"
        assert "test" in entry.tags

    def test_outgoing_links(self, vault_dir):
        idx = VaultIndex(vault_dir)
        idx.build()
        entry = idx.get("linked.md")
        assert "simple" in entry.outgoing_links

    def test_incoming_links(self, vault_dir):
        idx = VaultIndex(vault_dir)
        idx.build()
        entry = idx.get("simple.md")
        assert any("linked" in p for p in entry.incoming_links)

    def test_refresh_no_changes(self, vault_dir):
        idx = VaultIndex(vault_dir)
        idx.build()
        updated = idx.refresh()
        assert updated == 0

    def test_refresh_detects_change(self, vault_dir):
        idx = VaultIndex(vault_dir)
        idx.build()
        # Modify a file
        (vault_dir / "simple.md").write_text(
            "---\ntitle: Changed\ntags: [modified]\n---\n\nNew body."
        )
        updated = idx.refresh()
        assert updated >= 1
        entry = idx.get("simple.md")
        assert entry.frontmatter["title"] == "Changed"

    def test_refresh_detects_new_file(self, vault_dir):
        idx = VaultIndex(vault_dir)
        idx.build()
        count_before = idx.note_count
        (vault_dir / "brand-new.md").write_text("---\ntitle: New\n---\n\nFresh.")
        idx.refresh()
        assert idx.note_count == count_before + 1

    def test_refresh_detects_deleted(self, vault_dir):
        idx = VaultIndex(vault_dir)
        idx.build()
        count_before = idx.note_count
        (vault_dir / "simple.md").unlink()
        idx.refresh()
        assert idx.note_count == count_before - 1

    def test_outgoing_map(self, vault_dir):
        idx = VaultIndex(vault_dir)
        idx.build()
        out = idx.outgoing_map
        assert "linked.md" in out
        assert "simple" in out["linked.md"]

    def test_incoming_map(self, vault_dir):
        idx = VaultIndex(vault_dir)
        idx.build()
        inc = idx.incoming_map
        assert "simple.md" in inc

    def test_tag_index(self, vault_dir):
        idx = VaultIndex(vault_dir)
        idx.build()
        ti = idx.tag_index
        assert "test" in ti
        assert len(ti["test"]) > 0

    def test_query_basic(self, vault_dir):
        idx = VaultIndex(vault_dir)
        idx.build()
        results = idx.query()
        assert len(results) > 0

    def test_query_where(self, vault_dir):
        idx = VaultIndex(vault_dir)
        idx.build()
        results = idx.query(where={"title": "Simple Note"})
        assert len(results) == 1
        assert results[0]["path"] == "simple.md"

    def test_query_tags(self, vault_dir):
        idx = VaultIndex(vault_dir)
        idx.build()
        results = idx.query(tags=["hub"])
        assert len(results) == 1
        assert results[0]["path"] == "hub.md"

    def test_query_folder(self, vault_dir):
        idx = VaultIndex(vault_dir)
        idx.build()
        results = idx.query(from_folder="deep/")
        assert len(results) == 1

    def test_query_fields(self, vault_dir):
        idx = VaultIndex(vault_dir)
        idx.build()
        results = idx.query(where={"title": "Simple Note"}, fields=["title", "tags"])
        assert results[0]["title"] == "Simple Note"

    def test_query_sort(self, vault_dir):
        idx = VaultIndex(vault_dir)
        idx.build()
        results = idx.query(sort="name")
        paths = [r["path"] for r in results]
        assert paths == sorted(paths)

    def test_query_limit(self, vault_dir):
        idx = VaultIndex(vault_dir)
        idx.build()
        results = idx.query(limit=3)
        assert len(results) == 3


class TestVaultQueryTool:

    def test_query_via_tool(self, registry):
        result = tools.vault_query(registry, where={"title": "Simple Note"}, fields=["title"])
        parsed = json.loads(result)
        assert len(parsed) == 1
        assert parsed[0]["title"] == "Simple Note"

    def test_query_tags(self, registry):
        result = tools.vault_query(registry, tags=["test"], limit=5, fields=["title"])
        parsed = json.loads(result)
        assert len(parsed) > 0

    def test_query_no_results(self, registry):
        result = tools.vault_query(registry, where={"title": "Nonexistent XYZ"})
        assert "no results" in result or "[]" in result

    def test_query_cross_vault(self, multi_registry):
        result = tools.vault_query(multi_registry, vault="*", limit=10)
        parsed = json.loads(result)
        assert len(parsed) >= 2
        vaults = {r["vault"] for r in parsed}
        assert "alpha" in vaults
        assert "beta" in vaults
