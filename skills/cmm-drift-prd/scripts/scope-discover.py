#!/usr/bin/env python3
"""scope-discover.py — find PRD-anchored comments in branch diff files.

Usage:
    scope-discover.py <target_branch>

Output (stdout, JSON):
    [
      {
        "file": "src/foo/bar.ts",
        "line": 42,
        "anchor": "PRD §3.2",
        "anchor_section": "3.2",
        "anchor_prd_alias": null,
        "line_content": "  // PRD §3.2 用户名长度限制"
      },
      ...
    ]

Determinism:
    - 纯本地：git diff + 文件读取 + regex
    - 无 LLM、无网络、无 MCP
    - 失败兜底：找不到 anchor 返回空数组而非崩

Exit codes:
    0 = OK (含空 scope)
    1 = git 状态异常（非 repo / target 分支不存在）
    2 = 参数错误
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

# ── anchor 正则（与 references/anchor-grammar.md 同步）────────────────
# 优先级从高到低，匹配第一个命中
ANCHOR_PATTERNS = [
    # PRD<alias> §X.Y
    re.compile(r"PRD\s*<\s*([A-Za-z0-9_-]+)\s*>\s*§\s*(\d+(?:\.\d+)+)"),
    # PRD: <alias> §X.Y
    re.compile(r"PRD\s*:\s*([A-Za-z0-9_-]+)\s+§\s*(\d+(?:\.\d+)+)"),
    # PRD §X.Y
    re.compile(r"PRD\s*§\s*(\d+(?:\.\d+)+)"),
]
# 弱信号：裸 §X.Y（仅在注释行且无更强 anchor 时启用）
BARE_SECTION_RE = re.compile(r"§\s*(\d+(?:\.\d+)+)")

CODE_EXT = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
    ".py", ".sh", ".bash",
    ".vue", ".svelte", ".astro",
    ".md", ".mdx",
}

# 注释起始标记按语言简化判定
COMMENT_MARKERS = {
    ".ts":   ["//", "/*", "*"],
    ".tsx":  ["//", "/*", "*", "{/*"],
    ".js":   ["//", "/*", "*"],
    ".jsx":  ["//", "/*", "*", "{/*"],
    ".mjs":  ["//", "/*", "*"],
    ".cjs":  ["//", "/*", "*"],
    ".py":   ["#", '"""', "'''"],
    ".sh":   ["#"],
    ".bash": ["#"],
    ".vue":  ["//", "/*", "*", "<!--"],
    ".svelte": ["//", "/*", "*", "<!--"],
    ".astro": ["//", "/*", "*", "<!--", "---"],
    ".md":   ["<!--", "#"],
    ".mdx":  ["<!--", "{/*", "#"],
}


def die(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    sys.exit(code)


def git(*args: str) -> str:
    try:
        out = subprocess.check_output(["git", *args], text=True, stderr=subprocess.PIPE)
        return out.strip()
    except subprocess.CalledProcessError as e:
        die(f"git {' '.join(args)} failed: {e.stderr.strip()}")
        return ""


def is_comment_line(line: str, ext: str) -> bool:
    stripped = line.lstrip()
    markers = COMMENT_MARKERS.get(ext, ["//", "#", "/*", "*"])
    return any(stripped.startswith(m) for m in markers)


def extract_anchor(line: str) -> tuple[str | None, str | None, str | None]:
    """Return (full_anchor_text, prd_alias, section_number).

    Returns (None, None, None) if no anchor.
    """
    for pat in ANCHOR_PATTERNS:
        m = pat.search(line)
        if m:
            if pat.groups == 2:
                return (m.group(0).strip(), m.group(1), m.group(2))
            return (m.group(0).strip(), None, m.group(1))
    # Fall back to bare § only after strong anchors miss
    m = BARE_SECTION_RE.search(line)
    if m:
        return (m.group(0).strip(), None, m.group(1))
    return (None, None, None)


def diff_files(target: str) -> list[str]:
    # Validate target exists (local or remote)
    try:
        subprocess.check_output(
            ["git", "rev-parse", "--verify", target],
            text=True, stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError:
        die(f"target branch not found: {target}", code=1)

    out = git("diff", f"{target}...HEAD", "--name-only", "--diff-filter=AM")
    files = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        if Path(line).suffix in CODE_EXT:
            files.append(line)
    return files


def scan_file(repo_root: Path, rel_path: str) -> list[dict]:
    full = repo_root / rel_path
    if not full.exists() or not full.is_file():
        return []
    try:
        text = full.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError):
        return []

    ext = full.suffix
    items: list[dict] = []
    for lineno, raw_line in enumerate(text.splitlines(), 1):
        if not is_comment_line(raw_line, ext):
            continue
        anchor_text, alias, section = extract_anchor(raw_line)
        if not anchor_text or not section:
            continue
        items.append({
            "file": rel_path,
            "line": lineno,
            "anchor": anchor_text,
            "anchor_section": section,
            "anchor_prd_alias": alias,
            "line_content": raw_line.rstrip()[:300],
        })
    return items


def main() -> None:
    if len(sys.argv) < 2:
        die("usage: scope-discover.py <target_branch>", code=2)
    target = sys.argv[1]

    # Verify we're in a repo
    try:
        subprocess.check_output(
            ["git", "rev-parse", "--is-inside-work-tree"],
            text=True, stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError:
        die("not inside a git repository", code=1)

    repo_root = Path(git("rev-parse", "--show-toplevel"))
    files = diff_files(target)

    all_items: list[dict] = []
    for rel in files:
        all_items.extend(scan_file(repo_root, rel))

    print(json.dumps(all_items, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
