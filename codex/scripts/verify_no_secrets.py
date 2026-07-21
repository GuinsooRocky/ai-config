#!/usr/bin/env python3
"""Fail when a continuity snapshot contains credentials or local data stores."""

from __future__ import annotations

import re
import sys
import hashlib
from pathlib import Path


FORBIDDEN_NAMES = {".claude.json", "mcp-servers.json", "settings.json"}
FORBIDDEN_SUFFIXES = {".db", ".sqlite", ".sqlite3", ".jsonl", ".pem", ".p12"}
SKIP_PARTS = {".git", "__pycache__"}
DIRECT_PATTERNS = (
    ("OpenAI-style key", re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Bearer token", re.compile(r"(?i)\bBearer\s+([A-Za-z0-9._~%=-]{24,})")),
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)
ASSIGNMENT = re.compile(
    r"(?i)(?:api[_-]?key|app[_-]?secret|client[_-]?secret|access[_-]?token|refresh[_-]?token|password)"
    r"\s*[\"']?\s*[:=]\s*[\"']([^\"'\s,;]{12,})"
)
PLACEHOLDER_MARKERS = ("$", "{", "<", "redacted", "example", "placeholder", "your_")
# Public guest token vendored by the MIT-licensed bird-search client. The exact
# hash is allowlisted so another Bearer token in the same file still fails.
ALLOWLISTED_BEARER_SHA256 = {
    "11d3072e6af2d409dfc2453bc83fb1bd4bacc9db302556fa1eda60241c49e12e"
}


def is_binary(path: Path) -> bool:
    try:
        return b"\0" in path.read_bytes()[:4096]
    except OSError:
        return True


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    failures: list[str] = []

    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in SKIP_PARTS for part in path.parts):
            continue
        relative = path.relative_to(root)
        lowered_name = path.name.casefold()
        if lowered_name in FORBIDDEN_NAMES or path.suffix.casefold() in FORBIDDEN_SUFFIXES:
            failures.append(f"forbidden file: {relative}")
            continue
        if is_binary(path):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in DIRECT_PATTERNS:
            matches = list(pattern.finditer(text))
            if label == "Bearer token":
                matches = [
                    match
                    for match in matches
                    if hashlib.sha256(match.group(1).encode()).hexdigest()
                    not in ALLOWLISTED_BEARER_SHA256
                ]
            if matches:
                failures.append(f"{label}: {relative}")
        for match in ASSIGNMENT.finditer(text):
            value = match.group(1).casefold()
            if not any(marker in value for marker in PLACEHOLDER_MARKERS):
                failures.append(f"credential-like assignment: {relative}")
                break

    if failures:
        print("Secret scan failed:", file=sys.stderr)
        for failure in sorted(set(failures)):
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Secret scan passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
