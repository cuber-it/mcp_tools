"""Markdown + Frontmatter + WikiLink + Tag parser for vault tools.

Obsidian-compatible: WikiLinks, Heading-Links, Block-Refs, Embeds,
hierarchical tags, YAML frontmatter.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import frontmatter


# ---------------------------------------------------------------------------
# Frontmatter
# ---------------------------------------------------------------------------

def parse_note(content: str) -> tuple[dict, str]:
    """Parse a markdown note into frontmatter dict and body string.

    Handles edge cases: empty frontmatter, no frontmatter, nested structures.
    """
    if not content or not content.strip():
        return {}, ""
    try:
        post = frontmatter.loads(content)
        return dict(post.metadata), post.content
    except Exception:
        return {}, content


def rebuild_note(fm: dict, body: str) -> str:
    """Rebuild a markdown note from frontmatter dict and body string."""
    if not fm:
        return body
    post = frontmatter.Post(body, **fm)
    return frontmatter.dumps(post)


# ---------------------------------------------------------------------------
# Links
# ---------------------------------------------------------------------------

@dataclass
class VaultLink:
    """A parsed link from a markdown note."""
    target: str          # note name or path
    heading: str = ""    # #heading part
    block_id: str = ""   # ^block-id part
    alias: str = ""      # display text after |
    is_embed: bool = False  # ![[...]] vs [[...]]


_CODE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`[^`]+`")
_EMBED_RE = re.compile(r"!\[\[([^\]]+)\]\]")
_LINK_RE = re.compile(r"(?<!!)\[\[([^\]]+)\]\]")


def _strip_code(content: str) -> str:
    """Remove code blocks and inline code from content."""
    result = _CODE_BLOCK_RE.sub("", content)
    return _INLINE_CODE_RE.sub("", result)


def _parse_link_text(raw: str, is_embed: bool = False) -> VaultLink:
    """Parse raw link text into a VaultLink.

    Handles: note, note|alias, note#heading, note#^block-id,
    folder/note, folder/note#heading|alias
    """
    alias = ""
    if "|" in raw:
        raw, alias = raw.split("|", 1)
        alias = alias.strip()

    heading = ""
    block_id = ""
    target = raw.strip()

    if "#^" in target:
        target, block_id = target.split("#^", 1)
    elif "#" in target:
        target, heading = target.split("#", 1)

    return VaultLink(
        target=target.strip(),
        heading=heading.strip(),
        block_id=block_id.strip(),
        alias=alias,
        is_embed=is_embed,
    )


def extract_links(content: str) -> list[VaultLink]:
    """Extract all links and embeds from markdown content.

    Returns VaultLink objects with target, heading, block_id, alias, is_embed.
    Ignores links inside code blocks.
    """
    clean = _strip_code(content)
    links = []

    for match in _EMBED_RE.finditer(clean):
        links.append(_parse_link_text(match.group(1), is_embed=True))

    for match in _LINK_RE.finditer(clean):
        links.append(_parse_link_text(match.group(1), is_embed=False))

    return links


def extract_wikilinks(content: str) -> list[str]:
    """Extract all [[WikiLink]] targets as simple strings (no embeds)."""
    return [link.target for link in extract_links(content) if not link.is_embed]


# ---------------------------------------------------------------------------
# Tags
# ---------------------------------------------------------------------------

_INLINE_TAG_RE = re.compile(r"(?:^|\s)#([a-zA-Z][a-zA-Z0-9_/-]*)", re.MULTILINE)


def extract_tags(content: str, fm: dict) -> list[str]:
    """Extract all tags from frontmatter and inline #tags.

    Returns sorted, deduplicated list. Handles hierarchical tags.
    """
    tags = set()

    # From frontmatter
    fm_tags = fm.get("tags", [])
    if isinstance(fm_tags, list):
        tags.update(str(t).strip() for t in fm_tags if t)
    elif isinstance(fm_tags, str):
        tags.update(t.strip() for t in fm_tags.split(",") if t.strip())

    # Inline #tags (not inside code blocks)
    clean = _strip_code(content)
    for match in _INLINE_TAG_RE.finditer(clean):
        tags.add(match.group(1))

    return sorted(tags)


def expand_hierarchical_tags(tags: list[str]) -> list[str]:
    """Expand hierarchical tags: food/recipe/pasta -> food, food/recipe, food/recipe/pasta."""
    expanded = set()
    for tag in tags:
        parts = tag.split("/")
        for i in range(1, len(parts) + 1):
            expanded.add("/".join(parts[:i]))
    return sorted(expanded)


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def normalize_note_name(name: str) -> str:
    """Normalize a note name: strip .md extension."""
    name = name.strip()
    if name.lower().endswith(".md"):
        name = name[:-3]
    return name


def ensure_md_extension(path: str) -> str:
    """Ensure path ends with .md."""
    if not path.endswith(".md"):
        return path + ".md"
    return path
