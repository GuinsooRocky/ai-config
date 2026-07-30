#!/usr/bin/env python3
"""Search the portable capability catalog bundled with ai-continuity."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path


MAX_FILE_BYTES = 500_000
SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*[^\s,;]+"),
)


def plugin_root() -> Path:
    override = os.environ.get("AI_CONTINUITY_PLUGIN_ROOT")
    if override:
        return Path(override).expanduser().resolve()
    return Path(__file__).resolve().parents[3]


def candidate_files(root: Path) -> list[Path]:
    locations = (root / "skills", root / "assets" / "capabilities")
    found: list[Path] = []
    for location in locations:
        if not location.is_dir():
            continue
        for skill_file in sorted(location.glob("*/SKILL.md")):
            if skill_file.is_file() and skill_file.stat().st_size <= MAX_FILE_BYTES:
                found.append(skill_file)
    return found


def terms_for(query: str) -> list[str]:
    terms = [
        piece.casefold()
        for piece in re.findall(r"[A-Za-z0-9_-]{2,}|[\u3400-\u9fff]{2,}", query)
    ]
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


def frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", text)
    if not match:
        return ""
    return match.group(1).strip().strip('"\'')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=8, choices=range(1, 31))
    args = parser.parse_args()

    query = args.query.casefold().strip()
    terms = terms_for(query)
    results: list[dict[str, object]] = []

    for skill_file in candidate_files(plugin_root()):
        text = skill_file.read_text(encoding="utf-8", errors="ignore")
        folded = text.casefold()
        name = frontmatter_value(text, "name") or skill_file.parent.name
        description = frontmatter_value(text, "description")
        name_folded = name.casefold()
        path_folded = str(skill_file.parent).casefold()

        score = 0
        if query and query == name_folded:
            score += 100
        elif query and query in name_folded:
            score += 40
        elif query and query in folded:
            score += 20
        score += sum(8 for term in terms if term in name_folded)
        score += sum(4 for term in terms if term in path_folded)
        score += sum(min(folded.count(term), 5) for term in terms)
        if score == 0:
            continue

        matches: list[str] = []
        for number, line in enumerate(text.splitlines(), start=1):
            line_folded = line.casefold()
            if query in line_folded or any(term in line_folded for term in terms):
                matches.append(f"{number}: {redact(line.strip())[:240]}")
            if len(matches) == 3:
                break

        results.append(
            {
                "name": name,
                "description": description,
                "path": str(skill_file.parent),
                "score": score,
                "matches": matches,
            }
        )

    results.sort(key=lambda item: (-int(item["score"]), str(item["name"])))
    print(
        json.dumps(
            {"query": args.query, "matches": results[: args.limit]},
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
