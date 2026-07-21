#!/usr/bin/env python3
"""Find matching capabilities in Lengmo's live Claude configuration."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HOME = Path.home()
LIVE_ROOT = HOME / ".claude"
BACKUP_ROOT = HOME / "Desktop/cc-memory/cc-防丢失"
MAX_FILE_BYTES = 1_000_000
SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*[^\s,;]+"),
)


def candidate_files() -> list[tuple[str, Path]]:
    groups: list[tuple[str, list[Path]]] = [
        ("skill", sorted((LIVE_ROOT / "skills").glob("*/SKILL.md"))),
        ("agent", sorted((LIVE_ROOT / "agents").glob("*.md"))),
        ("workflow", sorted((LIVE_ROOT / "workflows").glob("*.js"))),
        ("command", sorted((LIVE_ROOT / "commands").glob("*"))),
        ("memory-index", [LIVE_ROOT / "projects/-Users-lengmo/memory/MEMORY.md"]),
        ("memory", sorted((LIVE_ROOT / "projects/-Users-lengmo/memory").glob("*.md"))),
    ]
    if not any(path.exists() for _, paths in groups for path in paths):
        groups = [
            ("skill-backup", sorted((BACKUP_ROOT / "skills").glob("*/SKILL.md"))),
            ("agent-backup", sorted((BACKUP_ROOT / "agents").glob("*.md"))),
            ("workflow-backup", sorted((BACKUP_ROOT / "workflows").glob("*.js"))),
            ("command-backup", sorted((BACKUP_ROOT / "commands").glob("*"))),
            ("memory-backup", sorted((BACKUP_ROOT / "memory").glob("*.md"))),
        ]

    found: list[tuple[str, Path]] = []
    seen: set[Path] = set()
    for kind, paths in groups:
        for path in paths:
            if not path.is_file() or path in seen:
                continue
            if path.stat().st_size > MAX_FILE_BYTES:
                continue
            seen.add(path)
            found.append((kind, path))
    return found


def terms_for(query: str) -> list[str]:
    terms = [piece.casefold() for piece in re.findall(r"[A-Za-z0-9_-]{2,}|[\u3400-\u9fff]{2,}", query)]
    expanded: list[str] = []
    for term in terms:
        expanded.append(term)
        if re.fullmatch(r"[\u3400-\u9fff]{4,}", term):
            expanded.extend(term[index : index + 2] for index in range(len(term) - 1))
    return list(dict.fromkeys(expanded))


def redact(text: str) -> str:
    for pattern in SECRET_PATTERNS:
        text = pattern.sub("[REDACTED]", text)
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=10, choices=range(1, 51))
    args = parser.parse_args()

    query = args.query.casefold().strip()
    terms = terms_for(query)
    results: list[dict[str, object]] = []
    for kind, path in candidate_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        folded = text.casefold()
        path_folded = str(path).casefold()
        score = 20 if query and query in folded else 0
        score += sum(5 for term in terms if term in path_folded)
        score += sum(min(folded.count(term), 5) for term in terms)
        if score == 0:
            continue

        previews: list[str] = []
        for number, line in enumerate(text.splitlines(), start=1):
            line_folded = line.casefold()
            if query in line_folded or any(term in line_folded for term in terms):
                previews.append(f"{number}: {redact(line.strip())[:300]}")
            if len(previews) == 3:
                break
        results.append({"kind": kind, "path": str(path), "score": score, "matches": previews})

    results.sort(key=lambda item: (-int(item["score"]), str(item["path"])))
    print(json.dumps({"query": args.query, "matches": results[: args.limit]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
