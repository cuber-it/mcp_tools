"""Graph analysis operations for vault link structure."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from ..parser import (
    ensure_md_extension,
    extract_tags,
    extract_wikilinks,
    normalize_note_name,
    parse_note,
)
from ..registry import VaultRegistry
from ._helpers import iter_notes, resolve_single_vault


def _build_graph(vault_root: Path) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """Build outgoing and incoming link maps for the vault.

    Returns (outgoing, incoming) where both are dict[path, set[path]].
    """
    outgoing: dict[str, set[str]] = defaultdict(set)
    incoming: dict[str, set[str]] = defaultdict(set)
    all_notes = {str(f.relative_to(vault_root)): f for f in iter_notes(vault_root)}
    note_names = {normalize_note_name(p).lower(): p for p in all_notes}

    for rel_path, filepath in all_notes.items():
        content = filepath.read_text(encoding="utf-8")
        for link in extract_wikilinks(content):
            target_name = normalize_note_name(link).lower()
            target_path = note_names.get(target_name)
            if target_path:
                outgoing[rel_path].add(target_path)
                incoming[target_path].add(rel_path)

    # Ensure all notes are in the maps
    for p in all_notes:
        outgoing.setdefault(p, set())
        incoming.setdefault(p, set())

    return dict(outgoing), dict(incoming)


def vault_graph(registry: VaultRegistry, vault: str = "") -> str:
    """Complete link graph as JSON (nodes + edges)."""
    try:
        vc = resolve_single_vault(registry, vault)
        vault_root = vc.path
        outgoing, _ = _build_graph(vault_root)

        nodes = []
        edges = []
        for filepath in iter_notes(vault_root):
            rel = str(filepath.relative_to(vault_root))
            content = filepath.read_text(encoding="utf-8")
            fm, _ = parse_note(content)
            tags = extract_tags(content, fm)
            title = fm.get("title", normalize_note_name(Path(rel).name))
            nodes.append({"path": rel, "title": title, "tags": tags})

        for source, targets in outgoing.items():
            for target in targets:
                edges.append({"source": source, "target": target})

        return json.dumps({"nodes": nodes, "edges": edges}, indent=2, default=str)
    except Exception as e:
        return f"Error: {e}"


def vault_hubs(registry: VaultRegistry, limit: int = 10, vault: str = "") -> str:
    """Notes with the most incoming + outgoing links (the central nodes)."""
    try:
        vc = resolve_single_vault(registry, vault)
        outgoing, incoming = _build_graph(vc.path)

        scores = {}
        for path in set(list(outgoing.keys()) + list(incoming.keys())):
            scores[path] = len(outgoing.get(path, set())) + len(incoming.get(path, set()))

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        lines = [f"{path} ({score} connections)" for path, score in ranked if score > 0]
        return "\n".join(lines) if lines else "(no hubs)"
    except Exception as e:
        return f"Error: {e}"


def vault_clusters(registry: VaultRegistry, vault: str = "") -> str:
    """Find clusters of connected notes (connected components)."""
    try:
        vc = resolve_single_vault(registry, vault)
        outgoing, incoming = _build_graph(vc.path)

        all_nodes = set(outgoing.keys()) | set(incoming.keys())
        visited = set()
        clusters = []

        for node in all_nodes:
            if node in visited:
                continue
            # BFS
            cluster = set()
            queue = [node]
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                cluster.add(current)
                for neighbor in outgoing.get(current, set()):
                    if neighbor not in visited:
                        queue.append(neighbor)
                for neighbor in incoming.get(current, set()):
                    if neighbor not in visited:
                        queue.append(neighbor)
            clusters.append(sorted(cluster))

        # Sort clusters by size, largest first
        clusters.sort(key=len, reverse=True)
        lines = []
        for i, cluster in enumerate(clusters):
            summary = f"Cluster {i+1} ({len(cluster)} notes): {', '.join(cluster[:5])}"
            if len(cluster) > 5:
                summary += f" ... +{len(cluster) - 5}"
            lines.append(summary)

        return "\n".join(lines) if lines else "(no clusters)"
    except Exception as e:
        return f"Error: {e}"


def vault_bridges(registry: VaultRegistry, vault: str = "") -> str:
    """Find bridge notes -- removal would disconnect clusters."""
    try:
        vc = resolve_single_vault(registry, vault)
        outgoing, incoming = _build_graph(vc.path)

        # Build undirected adjacency
        adj: dict[str, set[str]] = defaultdict(set)
        for node, targets in outgoing.items():
            for t in targets:
                adj[node].add(t)
                adj[t].add(node)

        all_nodes = list(adj.keys())
        if not all_nodes:
            return "(no bridges)"

        # Count connected components
        def count_components(skip: str) -> int:
            visited = set()
            components = 0
            for start in all_nodes:
                if start == skip or start in visited:
                    continue
                components += 1
                queue = [start]
                while queue:
                    current = queue.pop(0)
                    if current in visited or current == skip:
                        continue
                    visited.add(current)
                    for n in adj.get(current, set()):
                        if n not in visited and n != skip:
                            queue.append(n)
            return components

        base_components = count_components("")
        bridges = []
        for node in all_nodes:
            if len(adj[node]) < 2:
                continue
            if count_components(node) > base_components:
                bridges.append(node)

        return "\n".join(sorted(bridges)) if bridges else "(no bridges)"
    except Exception as e:
        return f"Error: {e}"


def vault_dead_ends(registry: VaultRegistry, vault: str = "") -> str:
    """Notes with outgoing links but no incoming links (not orphans -- those have no links at all)."""
    try:
        vc = resolve_single_vault(registry, vault)
        outgoing, incoming = _build_graph(vc.path)

        dead_ends = []
        for path in outgoing:
            if outgoing[path] and not incoming.get(path, set()):
                dead_ends.append(path)

        return "\n".join(sorted(dead_ends)) if dead_ends else "(no dead ends)"
    except Exception as e:
        return f"Error: {e}"


def vault_isolated(registry: VaultRegistry, vault: str = "") -> str:
    """Find truly isolated notes -- no links in, no links out, no embeds. Complete islands."""
    try:
        vc = resolve_single_vault(registry, vault)
        outgoing, incoming = _build_graph(vc.path)

        isolated = []
        for path in outgoing:
            if not outgoing[path] and not incoming.get(path, set()):
                isolated.append(path)

        return "\n".join(sorted(isolated)) if isolated else "(no isolated notes)"
    except Exception as e:
        return f"Error: {e}"


def vault_shortest_path(registry: VaultRegistry, source: str, target: str, vault: str = "") -> str:
    """Find the shortest link path between two notes. Shows how knowledge connects."""
    try:
        vc_s, rel_s = registry.resolve(source)
        vc_t, rel_t = registry.resolve(target)
        if vc_s.name != vc_t.name:
            return "Error: both notes must be in the same vault"

        vault_root = vc_s.path
        source_path = ensure_md_extension(rel_s)
        target_path = ensure_md_extension(rel_t)

        if not (vault_root / source_path).exists():
            return f"Error: note not found: {source}"
        if not (vault_root / target_path).exists():
            return f"Error: note not found: {target}"

        outgoing, incoming = _build_graph(vault_root)

        # BFS for shortest path (undirected)
        adj: dict[str, set[str]] = defaultdict(set)
        for node, targets in outgoing.items():
            for t in targets:
                adj[node].add(t)
                adj[t].add(node)

        visited = {source_path}
        queue = [(source_path, [source_path])]
        target_normalized = normalize_note_name(target_path).lower()

        while queue:
            current, path = queue.pop(0)
            if normalize_note_name(current).lower() == target_normalized:
                return " -> ".join(normalize_note_name(p) for p in path)
            for neighbor in adj.get(current, set()):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return f"(no path between {source} and {target})"
    except Exception as e:
        return f"Error: {e}"


def vault_tag_graph(registry: VaultRegistry, min_overlap: int = 2, vault: str = "") -> str:
    """Tag co-occurrence graph -- which tags appear together and how often.

    Shows implicit topic clusters. min_overlap filters weak connections.
    """
    try:
        vc = resolve_single_vault(registry, vault)
        # Collect tags per note
        note_tags: list[set[str]] = []
        for filepath in iter_notes(vc.path):
            content = filepath.read_text(encoding="utf-8")
            fm, _ = parse_note(content)
            tags = set(extract_tags(content, fm))
            if len(tags) >= 2:
                note_tags.append(tags)

        # Count co-occurrences
        cooccurrence: dict[tuple[str, str], int] = defaultdict(int)
        for tags in note_tags:
            tag_list = sorted(tags)
            for i in range(len(tag_list)):
                for j in range(i + 1, len(tag_list)):
                    cooccurrence[(tag_list[i], tag_list[j])] += 1

        # Filter and format
        pairs = [(a, b, count) for (a, b), count in cooccurrence.items() if count >= min_overlap]
        pairs.sort(key=lambda x: x[2], reverse=True)

        if not pairs:
            return "(no tag co-occurrences found)"

        lines = [f"{a} <-> {b} ({count} notes)" for a, b, count in pairs]
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


def vault_tag_overlap(registry: VaultRegistry, tag_a: str, tag_b: str, vault: str = "") -> str:
    """Find notes that have both tags -- implicit relationships."""
    try:
        vc = resolve_single_vault(registry, vault)
        a_clean = tag_a.lstrip("#")
        b_clean = tag_b.lstrip("#")
        results = []

        for filepath in iter_notes(vc.path):
            content = filepath.read_text(encoding="utf-8")
            fm, _ = parse_note(content)
            tags = extract_tags(content, fm)
            if a_clean in tags and b_clean in tags:
                results.append(str(filepath.relative_to(vc.path)))

        return "\n".join(sorted(results)) if results else "(no overlap)"
    except Exception as e:
        return f"Error: {e}"
