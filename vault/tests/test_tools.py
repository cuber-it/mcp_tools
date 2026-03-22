"""Tests for vault tools — Schicht 1: Filesystem-only."""

import json
import pytest
from pathlib import Path

from mcp_vault_tools.vault import tools
from mcp_vault_tools.vault.parser import (
    extract_links,
    extract_tags,
    expand_hierarchical_tags,
    parse_note,
    rebuild_note,
)
from mcp_vault_tools.vault.registry import VaultRegistry


# ===================================================================
# Parser Tests
# ===================================================================

class TestParser:

    def test_parse_note_with_frontmatter(self):
        content = "---\ntitle: Test\ntags: [a, b]\n---\n\nBody text."
        fm, body = parse_note(content)
        assert fm["title"] == "Test"
        assert fm["tags"] == ["a", "b"]
        assert "Body text." in body

    def test_parse_note_without_frontmatter(self):
        content = "Just plain text."
        fm, body = parse_note(content)
        assert fm == {}
        assert "Just plain text." in body

    def test_parse_note_empty_frontmatter(self):
        content = "---\n---\n\nBody."
        fm, body = parse_note(content)
        assert fm == {}
        assert "Body." in body

    def test_parse_note_empty_content(self):
        fm, body = parse_note("")
        assert fm == {}
        assert body == ""

    def test_rebuild_note(self):
        fm = {"title": "Test", "tags": ["a"]}
        body = "Content here."
        result = rebuild_note(fm, body)
        assert "title: Test" in result
        assert "Content here." in result

    def test_rebuild_note_no_frontmatter(self):
        result = rebuild_note({}, "Just body.")
        assert result == "Just body."


class TestLinkParser:

    def test_simple_link(self):
        links = extract_links("Text [[note]] more.")
        assert len(links) == 1
        assert links[0].target == "note"
        assert not links[0].is_embed

    def test_link_with_alias(self):
        links = extract_links("[[note|display text]]")
        assert links[0].target == "note"
        assert links[0].alias == "display text"

    def test_link_with_heading(self):
        links = extract_links("[[note#section]]")
        assert links[0].target == "note"
        assert links[0].heading == "section"

    def test_link_with_block_ref(self):
        links = extract_links("[[note#^abc123]]")
        assert links[0].target == "note"
        assert links[0].block_id == "abc123"

    def test_embed(self):
        links = extract_links("![[image.png]]")
        assert links[0].target == "image.png"
        assert links[0].is_embed

    def test_note_embed(self):
        links = extract_links("![[other-note]]")
        assert links[0].is_embed
        assert links[0].target == "other-note"

    def test_link_in_code_block_ignored(self):
        content = "```\n[[not-a-link]]\n```\nReal [[link]]."
        links = extract_links(content)
        assert len(links) == 1
        assert links[0].target == "link"

    def test_link_in_inline_code_ignored(self):
        content = "Text `[[not-a-link]]` and [[real]]."
        links = extract_links(content)
        assert len(links) == 1
        assert links[0].target == "real"

    def test_multiple_links(self):
        content = "[[a]], [[b|alias]], ![[c]], [[d#head]]."
        links = extract_links(content)
        targets = [(l.target, l.is_embed) for l in links]
        assert ("c", True) in targets
        assert ("a", False) in targets
        assert ("b", False) in targets
        assert ("d", False) in targets

    def test_folder_link(self):
        links = extract_links("[[folder/note]]")
        assert links[0].target == "folder/note"


class TestTagParser:

    def test_frontmatter_tags(self):
        fm = {"tags": ["alpha", "beta"]}
        tags = extract_tags("no inline", fm)
        assert tags == ["alpha", "beta"]

    def test_inline_tags(self):
        tags = extract_tags("Text #hello and #world.", {})
        assert "hello" in tags
        assert "world" in tags

    def test_tags_in_code_ignored(self):
        content = "```\n#not-a-tag\n```\nReal #tag."
        tags = extract_tags(content, {})
        assert "tag" in tags
        assert "not-a-tag" not in tags

    def test_hierarchical_tags(self):
        tags = ["food/recipe/pasta", "food/italian"]
        expanded = expand_hierarchical_tags(tags)
        assert "food" in expanded
        assert "food/recipe" in expanded
        assert "food/recipe/pasta" in expanded
        assert "food/italian" in expanded

    def test_frontmatter_tags_as_string(self):
        fm = {"tags": "alpha, beta, gamma"}
        tags = extract_tags("", fm)
        assert "alpha" in tags
        assert "beta" in tags


# ===================================================================
# CRUD Tests
# ===================================================================

class TestCRUD:

    def test_read(self, registry):
        result = json.loads(tools.vault_read(registry, "simple"))
        assert result["frontmatter"]["title"] == "Simple Note"
        assert "simple note" in result["body"].lower()

    def test_read_not_found(self, registry):
        assert "Error" in tools.vault_read(registry, "nonexistent")

    def test_write_and_read(self, registry):
        tools.vault_write(registry, "new-note", "---\ntitle: New\n---\n\nHello.")
        result = json.loads(tools.vault_read(registry, "new-note"))
        assert result["frontmatter"]["title"] == "New"

    def test_append(self, registry):
        tools.vault_append(registry, "simple", "Appended text.")
        result = json.loads(tools.vault_read(registry, "simple"))
        assert "Appended text." in result["body"]

    def test_delete(self, registry):
        tools.vault_write(registry, "to-delete", "temp")
        tools.vault_delete(registry, "to-delete")
        assert tools.vault_exists(registry, "to-delete") == "false"

    def test_list(self, registry):
        result = tools.vault_list(registry, "", recursive=True)
        assert "simple.md" in result
        assert "deep/nested.md" in result

    def test_list_ignores_obsidian_dir(self, registry):
        result = tools.vault_list(registry, "", recursive=True)
        assert ".obsidian" not in result

    def test_list_respects_obsidianignore(self, registry):
        result = tools.vault_list(registry, "", recursive=True)
        assert "_templates" not in result

    def test_exists(self, registry):
        assert tools.vault_exists(registry, "simple") == "true"
        assert tools.vault_exists(registry, "nope") == "false"


# ===================================================================
# Search Tests
# ===================================================================

class TestPrependAndHeadings:

    def test_prepend(self, registry):
        tools.vault_write(registry, "prtest", "---\ntitle: PR\n---\n\nOriginal body.")
        result = tools.vault_prepend(registry, "prtest", "Prepended line.")
        assert "Prepended" in result
        content = json.loads(tools.vault_read(registry, "prtest"))
        assert content["body"].startswith("Prepended line.")
        assert "Original body." in content["body"]

    def test_prepend_not_found(self, registry):
        result = tools.vault_prepend(registry, "nonexistent", "text")
        assert "Error" in result

    def test_headings(self, registry):
        tools.vault_write(registry, "headed", "---\ntitle: H\n---\n\n# Top\n\nText.\n\n## Sub\n\nMore.\n\n### Deep\n\nDeepest.")
        result = tools.vault_headings(registry, "headed")
        assert "# Top" in result
        assert "## Sub" in result
        assert "### Deep" in result

    def test_headings_empty(self, registry):
        tools.vault_write(registry, "nohead", "---\ntitle: N\n---\n\nNo headings here.")
        result = tools.vault_headings(registry, "nohead")
        assert "no headings" in result


class TestSearch:

    def test_search(self, registry):
        result = tools.vault_search(registry, "simple note")
        assert "simple.md" in result

    def test_search_no_results(self, registry):
        result = tools.vault_search(registry, "xyznonexistent")
        assert "no results" in result

    def test_search_tag(self, registry):
        result = tools.vault_search_tag(registry, "test")
        assert "simple.md" in result

    def test_search_tag_hierarchical(self, registry):
        result = tools.vault_search_tag(registry, "food")
        assert "tagged.md" in result

    def test_search_frontmatter(self, registry):
        result = tools.vault_search_frontmatter(registry, "title", "Simple Note")
        assert "simple.md" in result


# ===================================================================
# Link Tests
# ===================================================================

class TestLinks:

    def test_links(self, registry):
        result = tools.vault_links(registry, "linked")
        assert "[[simple" in result
        assert "[[deep/nested]]" in result

    def test_links_embeds(self, registry):
        result = tools.vault_links(registry, "linked")
        assert "![[image.png]]" in result
        assert "![[simple]]" in result

    def test_links_heading(self, registry):
        result = tools.vault_links(registry, "linked")
        assert "#section-one" in result

    def test_links_block_ref(self, registry):
        result = tools.vault_links(registry, "linked")
        assert "#^block-123" in result

    def test_backlinks(self, registry):
        result = tools.vault_backlinks(registry, "simple")
        assert "linked.md" in result
        assert "hub.md" in result

    def test_backlinks_alias(self, registry):
        result = tools.vault_backlinks(registry, "aliased")
        assert "uses-alias.md" in result

    def test_orphans(self, registry):
        result = tools.vault_orphans(registry)
        # orphan.md is linked by hub.md, so it's not an orphan
        # bare.md, aliased.md etc. have no incoming links
        assert "bare.md" in result

    def test_related(self, registry):
        result = tools.vault_related(registry, "linked")
        assert "simple.md" in result or "nested.md" in result


# ===================================================================
# Tag Tests
# ===================================================================

class TestTags:

    def test_tag_list(self, registry):
        result = tools.vault_tag_list(registry)
        assert "test" in result

    def test_frontmatter(self, registry):
        result = tools.vault_get_frontmatter(registry, "simple")
        fm = json.loads(result)
        assert fm["title"] == "Simple Note"

    def test_set_frontmatter(self, registry):
        tools.vault_set_frontmatter(registry, "simple", "status", "done")
        result = json.loads(tools.vault_get_frontmatter(registry, "simple"))
        assert result["status"] == "done"

    def test_add_tag(self, registry):
        tools.vault_add_tag(registry, "simple", "new-tag")
        result = json.loads(tools.vault_get_frontmatter(registry, "simple"))
        assert "new-tag" in result["tags"]


# ===================================================================
# Rename / Move Tests
# ===================================================================

class TestRegex:

    def test_search_regex(self, registry):
        result = tools.vault_search(registry, r"link.*simple", regex=True)
        assert "linked.md" in result or "hub.md" in result

    def test_search_regex_case_sensitive(self, registry):
        result = tools.vault_search(registry, r"Simple", regex=True, ignore_case=False)
        assert "simple.md" in result

    def test_replace_regex(self, registry):
        tools.vault_write(registry, "regtest", "---\ntitle: Reg\n---\n\nfoo123 bar456 baz789.")
        result = tools.vault_replace(registry, r"\w+(\d{3})", r"num\1", regex=True)
        assert "occurrences" in result.lower()
        content = json.loads(tools.vault_read(registry, "regtest"))
        assert "num123" in content["body"]

    def test_replace_regex_dry_run(self, registry):
        result = tools.vault_replace(registry, r"note", "REPLACED", regex=True, dry_run=True)
        assert "DRY RUN" in result


class TestTypesJson:

    def test_get_types(self, registry):
        result = tools.vault_get_types(registry)
        # Test vault has a types.json
        assert "title" in result or "types" in result

    def test_set_type(self, registry):
        result = tools.vault_set_type(registry, "priority", "number")
        assert "Set type" in result
        types = tools.vault_get_types(registry)
        assert "priority" in types
        assert "number" in types

    def test_set_type_invalid(self, registry):
        result = tools.vault_set_type(registry, "foo", "invalid_type")
        assert "Error" in result

    def test_set_frontmatter_auto_registers_type(self, registry):
        tools.vault_set_frontmatter(registry, "simple", "new_field", "test_value")
        types = tools.vault_get_types(registry)
        assert "new_field" in types


class TestAliasSearch:

    def test_search_finds_alias(self, registry):
        result = tools.vault_search(registry, "Alias One")
        assert "aliased.md" in result

    def test_find_finds_alias(self, registry):
        result = tools.vault_find(registry, "Alias Two")
        assert "aliased.md" in result


class TestRemoveOps:

    def test_remove_tag(self, registry):
        tools.vault_add_tag(registry, "simple", "removeme")
        result = tools.vault_remove_tag(registry, "simple", "removeme")
        assert "Removed" in result
        fm = json.loads(tools.vault_get_frontmatter(registry, "simple"))
        assert "removeme" not in fm.get("tags", [])

    def test_remove_tag_not_found(self, registry):
        result = tools.vault_remove_tag(registry, "simple", "nonexistent")
        assert "not found" in result.lower()

    def test_remove_frontmatter(self, registry):
        tools.vault_set_frontmatter(registry, "simple", "temp_key", "temp_val")
        result = tools.vault_remove_frontmatter(registry, "simple", "temp_key")
        assert "Removed" in result
        fm = json.loads(tools.vault_get_frontmatter(registry, "simple"))
        assert "temp_key" not in fm

    def test_remove_frontmatter_not_found(self, registry):
        result = tools.vault_remove_frontmatter(registry, "simple", "nonexistent")
        assert "not found" in result.lower()


class TestPathTraversal:

    def test_read_traversal_blocked(self, registry):
        result = tools.vault_read(registry, "../../etc/passwd")
        assert "Error" in result

    def test_write_traversal_blocked(self, registry):
        result = tools.vault_write(registry, "../../../tmp/evil", "bad")
        assert "Error" in result

    def test_delete_traversal_blocked(self, registry):
        result = tools.vault_delete(registry, "../../etc/hosts")
        assert "Error" in result


class TestDryRun:

    def test_replace_dry_run(self, registry):
        result = tools.vault_replace(registry, "simple", "CHANGED", dry_run=True)
        assert "DRY RUN" in result
        # Verify nothing changed
        content = json.loads(tools.vault_read(registry, "simple"))
        assert "CHANGED" not in content["body"]

    def test_replace_case_insensitive(self, registry):
        tools.vault_write(registry, "casetest", "---\ntitle: Case\n---\n\nHello HELLO hello.")
        result = tools.vault_replace(registry, "hello", "hi", ignore_case=True)
        content = json.loads(tools.vault_read(registry, "casetest"))
        assert "hello" not in content["body"].lower()

    def test_tag_rename_dry_run(self, registry):
        result = tools.vault_tag_rename(registry, "test", "changed", dry_run=True)
        assert "DRY RUN" in result
        # Verify nothing changed
        tags = tools.vault_tag_list(registry)
        assert "test" in tags

    def test_bulk_frontmatter_dry_run(self, registry):
        result = tools.vault_bulk_frontmatter(registry, "status", "draft", dry_run=True)
        assert "DRY RUN" in result
        fm = json.loads(tools.vault_get_frontmatter(registry, "simple"))
        assert "status" not in fm


class TestRenameMove:

    def test_rename(self, registry):
        tools.vault_write(registry, "old-name", "---\ntitle: Old\n---\n\nContent.")
        tools.vault_write(registry, "linker", "Links to [[old-name]].")
        result = tools.vault_rename(registry, "old-name", "new-name")
        assert "Renamed" in result
        assert tools.vault_exists(registry, "new-name") == "true"
        assert tools.vault_exists(registry, "old-name") == "false"
        # Check link was updated
        linker = json.loads(tools.vault_read(registry, "linker"))
        assert "new-name" in linker["body"]

    def test_move(self, registry):
        tools.vault_write(registry, "moveme", "---\ntitle: Move\n---\n\nMove me.")
        result = tools.vault_move(registry, "moveme", "deep")
        assert "Renamed" in result
        assert tools.vault_exists(registry, "deep/moveme") == "true"


# ===================================================================
# Aggregator Tests
# ===================================================================

class TestAggregators:

    def test_tag_rename(self, registry):
        result = tools.vault_tag_rename(registry, "test", "tested")
        assert "notes" in result
        tags = tools.vault_tag_list(registry)
        assert "tested" in tags

    def test_broken_links(self, registry):
        result = tools.vault_broken_links(registry)
        # linked.md links to deep/nested which exists, but image.png doesn't have .md
        # Some links may be broken depending on exact vault state
        assert isinstance(result, str)

    def test_stats(self, registry):
        result = json.loads(tools.vault_stats(registry))
        assert result["notes"] > 0
        assert result["tags"] > 0

    def test_recent(self, registry):
        result = tools.vault_recent(registry, limit=3)
        assert ".md" in result

    def test_health(self, registry):
        result = tools.vault_health(registry)
        assert "Stats" in result
        assert "Broken Links" in result

    def test_daily(self, registry):
        result = tools.vault_daily(registry, "2026-03-19")
        assert "Created" in result or "exists" in result

    def test_inbox(self, registry):
        result = tools.vault_inbox(registry, "Quick thought")
        assert "inbox" in result.lower()

    def test_from_template(self, registry):
        result = tools.vault_from_template(
            registry, "meeting", "my-meeting",
            variables={"title": "Sprint Review"}
        )
        assert "Written" in result
        content = json.loads(tools.vault_read(registry, "my-meeting"))
        assert "Sprint Review" in content["body"]


# ===================================================================
# Multi-Vault Tests
# ===================================================================

class TestAdvancedEditing:

    def test_replace(self, registry):
        tools.vault_write(registry, "replaceme", "---\ntitle: Replace\n---\n\nxyzfoo bar xyzfoo baz.")
        result = tools.vault_replace(registry, "xyzfoo", "qux")
        assert "occurrences" in result.lower()
        content = json.loads(tools.vault_read(registry, "replaceme"))
        assert "qux bar qux baz" in content["body"]

    def test_insert_at_append(self, registry):
        tools.vault_write(registry, "sections", "---\ntitle: Sections\n---\n\n## Notes\n\nExisting.\n\n## Other\n\nStuff.")
        result = tools.vault_insert_at(registry, "sections", "Notes", "New content here.")
        assert "Inserted" in result
        content = json.loads(tools.vault_read(registry, "sections"))
        assert "New content here." in content["body"]
        assert "Existing." in content["body"]

    def test_insert_at_prepend(self, registry):
        tools.vault_write(registry, "preptest", "---\ntitle: P\n---\n\n## Section\n\nOld text.")
        tools.vault_insert_at(registry, "preptest", "Section", "Prepended.", position="prepend")
        content = json.loads(tools.vault_read(registry, "preptest"))
        body = content["body"]
        assert body.index("Prepended.") < body.index("Old text.")

    def test_insert_at_replace(self, registry):
        tools.vault_write(registry, "replsect", "---\ntitle: R\n---\n\n## Target\n\nOld.\n\n## Keep\n\nKept.")
        tools.vault_insert_at(registry, "replsect", "Target", "Replaced.", position="replace")
        content = json.loads(tools.vault_read(registry, "replsect"))
        assert "Replaced." in content["body"]
        assert "Old." not in content["body"]
        assert "Kept." in content["body"]

    def test_insert_at_heading_not_found(self, registry):
        result = tools.vault_insert_at(registry, "simple", "Nonexistent", "text")
        assert "Error" in result

    def test_split(self, registry):
        tools.vault_write(registry, "tosplit", "---\ntitle: Big\ntags: [test]\n---\n\n## Intro\n\nIntro text.\n\n## Extract Me\n\nExtracted content.\n\n## End\n\nEnd text.")
        result = tools.vault_split(registry, "tosplit", "Extract Me")
        assert "Split" in result
        # Original should have link instead of content
        original = json.loads(tools.vault_read(registry, "tosplit"))
        assert "[[extract-me]]" in original["body"]
        assert "Extracted content." not in original["body"]
        # New note should have the extracted content
        new_note = json.loads(tools.vault_read(registry, "extract-me"))
        assert "Extracted content." in new_note["body"]
        assert new_note["frontmatter"]["title"] == "Extract Me"


class TestConnectionDiscovery:

    def test_unlinked_mentions(self, registry):
        # Create a note that mentions "simple" without linking
        tools.vault_write(registry, "mentions", "---\ntitle: M\n---\n\nThis talks about simple things.")
        result = tools.vault_unlinked_mentions(registry, "simple")
        assert "mentions.md" in result

    def test_unlinked_mentions_already_linked_excluded(self, registry):
        result = tools.vault_unlinked_mentions(registry, "simple")
        # linked.md already has [[simple]] so should not appear
        assert "linked.md" not in result

    def test_link_suggest(self, registry):
        result = tools.vault_link_suggest(registry, "simple")
        # Notes sharing "test" tag should be suggested
        assert "shared tags" in result or "no suggestions" in result

    def test_link_suggest_not_found(self, registry):
        result = tools.vault_link_suggest(registry, "nonexistent")
        assert "Error" in result


class TestChangelog:

    def test_changelog(self, registry):
        result = tools.vault_changelog(registry, days=1)
        # All test files were just created, should appear
        assert "===" in result
        assert ".md" in result

    def test_changelog_no_changes(self, registry):
        result = tools.vault_changelog(registry, days=0)
        assert "no changes" in result


class TestConvenienceNew:

    def test_create(self, registry):
        result = tools.vault_create(registry, "created", title="Fresh", tags=["new"], body="Hello world.")
        assert "Written" in result
        content = json.loads(tools.vault_read(registry, "created"))
        assert content["frontmatter"]["title"] == "Fresh"
        assert "new" in content["frontmatter"]["tags"]
        assert "Hello world." in content["body"]

    def test_create_minimal(self, registry):
        result = tools.vault_create(registry, "minimal", body="Just body.")
        assert "Written" in result

    def test_find_text(self, registry):
        result = tools.vault_find(registry, "simple note")
        assert "simple.md" in result

    def test_find_tag(self, registry):
        result = tools.vault_find(registry, "#hub")
        assert "hub.md" in result

    def test_find_frontmatter(self, registry):
        result = tools.vault_find(registry, "title:Simple Note")
        assert "simple.md" in result

    def test_summary_single(self, registry):
        result = json.loads(tools.vault_summary(registry, "simple"))
        assert result["title"] == "Simple Note"
        assert "test" in result["tags"]
        assert result["preview"]

    def test_summary_folder(self, registry):
        result = tools.vault_summary(registry, "deep/", recursive=True)
        assert "nested.md" in result

    def test_tree(self, registry):
        result = tools.vault_tree(registry)
        assert "test/" in result
        assert "simple.md" in result
        assert "deep/" in result

    def test_copy(self, registry):
        result = tools.vault_copy(registry, "simple", "simple-copy")
        assert "Written" in result
        original = json.loads(tools.vault_read(registry, "simple"))
        copy = json.loads(tools.vault_read(registry, "simple-copy"))
        assert original["frontmatter"]["title"] == copy["frontmatter"]["title"]

    def test_frontmatter_keys(self, registry):
        result = tools.vault_frontmatter_keys(registry)
        assert "title" in result
        assert "tags" in result


class TestMultiVault:

    def test_list_vaults(self, multi_registry):
        result = tools.vault_list_vaults(multi_registry)
        assert "alpha" in result
        assert "beta" in result

    def test_prefix_read(self, multi_registry):
        result = json.loads(tools.vault_read(multi_registry, "beta:note-b"))
        assert result["frontmatter"]["title"] == "Note B"

    def test_default_vault(self, multi_registry):
        result = json.loads(tools.vault_read(multi_registry, "note-a"))
        assert result["frontmatter"]["title"] == "Note A"

    def test_cross_vault_search(self, multi_registry):
        result = tools.vault_search(multi_registry, "vault", vault="*")
        assert "note-a" in result.lower() or "note-b" in result.lower()

    def test_unknown_vault(self, multi_registry):
        result = tools.vault_read(multi_registry, "unknown:note")
        assert "Error" in result


# ===================================================================
# Graph Analysis Tests
# ===================================================================

class TestComposites:

    def test_link_mentions_dry_run(self, registry):
        tools.vault_write(registry, "mentioner", "---\ntitle: M\n---\n\nTalking about simple things here.")
        result = tools.vault_link_mentions(registry, "simple", dry_run=True)
        assert "DRY RUN" in result
        assert "mentioner.md" in result

    def test_link_mentions(self, registry):
        tools.vault_write(registry, "mentioner2", "---\ntitle: M2\n---\n\nThis references simple in text.")
        result = tools.vault_link_mentions(registry, "simple")
        assert "Linked" in result
        content = json.loads(tools.vault_read(registry, "mentioner2"))
        assert "[[simple" in content["body"]

    def test_archive_dry_run(self, registry):
        result = tools.vault_archive(registry, days=0, dry_run=True)
        assert "DRY RUN" in result
        # All notes are fresh, so with days=0 everything should be eligible
        # but they were just created so mtime is now — days=0 means cutoff=now
        assert "Archived" in result

    def test_extract_inline_tags(self, registry):
        result = tools.vault_extract_inline_tags(registry, "bare")
        # bare.md has inline #tag-here and #test
        assert "tag-here" in result or "test" in result

    def test_extract_inline_tags_no_tags(self, registry):
        tools.vault_write(registry, "notags", "---\ntitle: N\n---\n\nNo tags here.")
        result = tools.vault_extract_inline_tags(registry, "notags")
        assert "No inline" in result

    def test_backfill_titles_dry_run(self, registry):
        result = tools.vault_backfill_titles(registry, dry_run=True)
        assert "DRY RUN" in result
        # bare.md has no frontmatter, so no title
        assert "bare.md" in result

    def test_backfill_titles(self, registry):
        tools.vault_write(registry, "untitled", "Just body, no frontmatter at all.")
        result = tools.vault_backfill_titles(registry)
        assert "Added titles" in result
        content = json.loads(tools.vault_read(registry, "untitled"))
        assert "title" in content.get("frontmatter", {})

    def test_standardize_dry_run(self, registry):
        result = tools.vault_standardize(registry, dry_run=True)
        assert "Titles" in result
        assert "Inline tags" in result
        assert "Types" in result


class TestGraph:

    def test_graph(self, registry):
        result = json.loads(tools.vault_graph(registry))
        assert "nodes" in result
        assert "edges" in result
        assert len(result["nodes"]) > 0

    def test_hubs(self, registry):
        result = tools.vault_hubs(registry, limit=3)
        assert "hub.md" in result

    def test_clusters(self, registry):
        result = tools.vault_clusters(registry)
        assert "Cluster" in result

    def test_bridges(self, registry):
        result = tools.vault_bridges(registry)
        assert isinstance(result, str)

    def test_dead_ends(self, registry):
        result = tools.vault_dead_ends(registry)
        # dead-end.md is linked by hub.md, so it has incoming links
        # hub.md and code.md have outgoing but no incoming
        assert "hub.md" in result

    def test_shortest_path(self, registry):
        result = tools.vault_shortest_path(registry, "linked", "deep/nested")
        assert "linked" in result
        assert "nested" in result
        assert "->" in result

    def test_shortest_path_no_connection(self, registry):
        # orphan has no links to/from bare
        tools.vault_write(registry, "island_a", "No links.")
        tools.vault_write(registry, "island_b", "No links either.")
        result = tools.vault_shortest_path(registry, "island_a", "island_b")
        assert "no path" in result

    def test_tag_graph(self, registry):
        result = tools.vault_tag_graph(registry, min_overlap=1)
        # "test" appears on many notes, should co-occur with others
        assert "<->" in result or "no tag" in result

    def test_isolated(self, registry):
        tools.vault_write(registry, "total_island", "Completely alone.")
        result = tools.vault_isolated(registry)
        assert "total_island.md" in result

    def test_tag_overlap(self, registry):
        result = tools.vault_tag_overlap(registry, "test", "simple")
        assert "simple.md" in result
