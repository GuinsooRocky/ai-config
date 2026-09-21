#!/usr/bin/env python3
"""Publish a local HTML/Markdown file to the internal Pages service.

Wraps the `pages` MCP server (HTTP / JSON-RPC) so the file content is read and
uploaded entirely in code — no need for the model to inline / transcribe large
base64-heavy HTML into a tool call.

Config resolution (first hit wins):
  1. env PAGES_MCP_URL / PAGES_MCP_TOKEN
  2. parsed from `claude mcp get pages`

Usage:
  pages_publish.py publish  <file.html> [--slug SLUG] [--title TITLE]
  pages_publish.py markdown <file.md>   [--slug SLUG] [--title TITLE]
  pages_publish.py list     [--limit N]

Notes:
  - Passing an existing --slug overwrites that page (URL unchanged, 90d TTL reset).
  - Omitting --slug creates a new page with a random slug.
  - --title defaults to the HTML <title> tag, else the file stem.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path


def resolve_config():
    url = os.environ.get("PAGES_MCP_URL")
    tok = os.environ.get("PAGES_MCP_TOKEN")
    if url and tok:
        return url, tok if tok.lower().startswith("bearer ") else f"Bearer {tok}"
    try:
        out = subprocess.run(
            ["claude", "mcp", "get", "pages"],
            capture_output=True, text=True, timeout=30,
        ).stdout
    except Exception as e:
        sys.exit(f"[pages-publish] cannot read config from `claude mcp get pages`: {e}")
    m_url = re.search(r"URL:\s*(\S+)", out)
    m_auth = re.search(r"Authorization:\s*(.+)", out)
    if not (m_url and m_auth):
        sys.exit("[pages-publish] failed to parse URL/Authorization from `claude mcp get pages`. "
                 "Set PAGES_MCP_URL and PAGES_MCP_TOKEN env vars instead.")
    return m_url.group(1).strip(), m_auth.group(1).strip()


def rpc(url, auth, method, params, rid=1):
    body = json.dumps({"jsonrpc": "2.0", "id": rid, "method": method, "params": params}).encode()
    req = urllib.request.Request(
        url, data=body, method="POST",
        headers={
            "Authorization": auth,
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            # Cloudflare (error 1010) bans the default urllib UA; mimic curl.
            "User-Agent": "curl/8.4.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            ctype = resp.headers.get("Content-Type", "")
            raw = resp.read().decode()
    except urllib.error.HTTPError as e:
        sys.exit(f"[pages-publish] HTTP {e.code}: {e.read().decode(errors='replace')[:500]}")
    except urllib.error.URLError as e:
        sys.exit(f"[pages-publish] network error: {e}")

    # Streamable HTTP may answer as SSE; grab the last JSON `data:` frame.
    if "text/event-stream" in ctype:
        payload = None
        for line in raw.splitlines():
            if line.startswith("data:"):
                payload = line[5:].strip()
        raw = payload or "{}"
    data = json.loads(raw)
    if "error" in data:
        sys.exit(f"[pages-publish] MCP error: {data['error']}")
    return data.get("result", {})


def extract_text(result):
    sc = result.get("structuredContent") or {}
    if isinstance(sc, dict) and sc.get("result"):
        return sc["result"]
    for item in result.get("content", []):
        if item.get("type") == "text":
            return item["text"]
    return json.dumps(result, ensure_ascii=False)


def guess_title(html, fallback):
    m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    return (m.group(1).strip() if m else fallback) or fallback


def cmd_publish(args, url, auth, tool, is_md):
    path = Path(args.file).expanduser()
    if not path.is_file():
        sys.exit(f"[pages-publish] file not found: {path}")
    content = path.read_text(encoding="utf-8")
    kb = round(len(content.encode()) / 1024, 1)
    key = "markdown" if is_md else "html"
    arguments = {key: content}
    if args.slug:
        arguments["slug"] = args.slug
    arguments["title"] = args.title or (path.stem if is_md else guess_title(content, path.stem))
    print(f"[pages-publish] uploading {path.name} ({kb} KB) via {tool} ...", file=sys.stderr)
    result = rpc(url, auth, "tools/call", {"name": tool, "arguments": arguments}, rid=2)
    print(extract_text(result))


def cmd_share(args, url, auth):
    arguments = {"slug": args.slug, "description": args.desc}
    # 目标三选一：webhook（自定义机器人）/ email / open_id（P2P，需服务端配应用凭证）
    for k in ("webhook", "email", "open_id"):
        v = getattr(args, k)
        if v:
            arguments[k] = v
    result = rpc(url, auth, "tools/call", {"name": "share_page", "arguments": arguments}, rid=5)
    print(extract_text(result))


def cmd_list(args, url, auth):
    result = rpc(url, auth, "tools/call",
                 {"name": "list_pages", "arguments": {"limit": args.limit}}, rid=3)
    print(extract_text(result))


def cmd_delete(args, url, auth):
    result = rpc(url, auth, "tools/call",
                 {"name": "delete_page", "arguments": {"slug": args.slug}}, rid=4)
    print(extract_text(result))


def main():
    p = argparse.ArgumentParser(prog="pages_publish")
    sub = p.add_subparsers(dest="cmd", required=True)

    pub = sub.add_parser("publish", help="publish a self-contained HTML file")
    pub.add_argument("file")
    pub.add_argument("--slug", default="")
    pub.add_argument("--title", default="")

    md = sub.add_parser("markdown", help="publish a Markdown file (server-side template)")
    md.add_argument("file")
    md.add_argument("--slug", default="")
    md.add_argument("--title", default="")

    sh = sub.add_parser("share", help="send a Feishu card for a published page")
    sh.add_argument("slug")
    sh.add_argument("--desc", default="")
    sh.add_argument("--webhook", default="")
    sh.add_argument("--email", default="")
    sh.add_argument("--open-id", dest="open_id", default="")

    ls = sub.add_parser("list", help="list published pages")
    ls.add_argument("--limit", type=int, default=50)

    dl = sub.add_parser("delete", help="delete a published page by slug")
    dl.add_argument("slug")

    args = p.parse_args()
    url, auth = resolve_config()
    if args.cmd == "publish":
        cmd_publish(args, url, auth, "publish_page", is_md=False)
    elif args.cmd == "markdown":
        cmd_publish(args, url, auth, "publish_markdown", is_md=True)
    elif args.cmd == "share":
        cmd_share(args, url, auth)
    elif args.cmd == "list":
        cmd_list(args, url, auth)
    elif args.cmd == "delete":
        cmd_delete(args, url, auth)


if __name__ == "__main__":
    main()
