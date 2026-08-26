#!/usr/bin/env python3
"""拉 anthropic.com 全量文章清单，diff 出还没蒸馏过的。

数据源是 sitemap.xml（全量，含 lastmod），不是板块索引页——索引页只服务端渲染首屏
约 26 篇，news/research 的绝大部分都在首屏之外，靠它做增量会漏掉几百篇。
sitemap 没有标题，所以再抓三个板块索引页把首屏能拿到的标题/发布日期合并进来；
拿不到标题的条目 title 为空，蒸馏子 agent 读原文时自己补。

第二个源是 claude.com/sitemap.xml 的 /blog/ 段（section="blog"）——工程实践类文章
搬去了那个域，anthropic.com 的 sitemap 里一条都没有。它的索引页是 Webflow 渲染，
抓不到标题，所以 blog 条目 title 一律为空，照样由蒸馏子 agent 读原文补。

用法:
  fetch-index.py                    列出未蒸馏的文章（默认最新 15 篇），JSON 输出
  fetch-index.py --limit 30         改取数上限
  fetch-index.py --all              不限条数
  fetch-index.py --section news     只看某板块（news/engineering/research/blog）
  fetch-index.py --commit slug ...  把这些 slug 记为已蒸馏
  fetch-index.py --skip --commit slug ...  把这些 slug 记为「有意跳过」（不写卡）
  fetch-index.py --mark-all-read    建基线：把当前全量清单记为已蒸馏
  fetch-index.py --check            自检：每条已蒸馏的 slug 都得有卡，缺卡则退出码 1
"""
import argparse
import json
import pathlib
import re
import sys
import urllib.request
from datetime import date, datetime

DATA = pathlib.Path.home() / "Desktop/archives/anthropic-distill"
STATE = DATA / "state.json"
CARDS = DATA / "cards"
SECTIONS = ["news", "engineering", "research"]
BASE = "https://www.anthropic.com"
CLAUDE_BASE = "https://claude.com"


def fetch(path, base=BASE):
    req = urllib.request.Request(
        f"{base}/{path}", headers={"User-Agent": "Mozilla/5.0 (Macintosh)"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def parse_sitemap(xml):
    """全量清单：(section, slug, lastmod)。lastmod 是最后修改时间，不是发布时间，
    只作排序兜底——索引页能给发布日期的以索引页为准。"""
    return re.findall(
        r"<loc>%s/(news|engineering|research)/([a-z0-9\-]+)</loc>\s*"
        r"<lastmod>(\d{4}-\d{2}-\d{2})" % BASE,
        xml,
    )


def parse_claude_blog_sitemap(xml):
    """claude.com 的 /blog/ 段：(slug, lastmod)。它的 lastmod 是完整 ISO 时间戳
    （2026-08-24T...），正则只吃前面的日期部分，跟 anthropic.com 那边对齐成同一种排序键。
    路径卡死 /blog/ 开头，顺带把 /ko/blog/ 这类本地化副本挡在外面。"""
    return re.findall(
        r"<loc>%s/blog/([a-z0-9\-]+)</loc>\s*<lastmod>(\d{4}-\d{2}-\d{2})" % CLAUDE_BASE,
        xml,
    )


def parse(html, section):
    """按 <article> 切块。不匹配 CSS 类名全称——它带构建 hash，会随发版变。"""
    out, seen = [], set()
    for blk in html.split("<article")[1:]:
        end = blk.find("</article>")
        if end != -1:
            blk = blk[:end]
        m_href = re.search(r'href="/%s/([a-z0-9\-]+)"' % section, blk)
        if not m_href or m_href.group(1) in seen:
            continue
        seen.add(m_href.group(1))
        m_title = re.search(r"<h3[^>]*>(.*?)</h3>", blk, re.S)
        m_date = re.search(r'__date"[^>]*>(.*?)<', blk, re.S)
        raw_date = m_date.group(1).strip() if m_date else ""
        out.append(
            {
                "slug": m_href.group(1),
                "section": section,
                "title": re.sub(r"<[^>]+>", "", m_title.group(1)).strip()
                if m_title
                else "",
                "date": raw_date,
                "sort_key": to_iso(raw_date),
                "url": f"{BASE}/{section}/{m_href.group(1)}",
            }
        )
    return out


def to_iso(raw):
    """'Jan 06, 2025' -> '2025-01-06'；解析不了返回空串（排最后）。"""
    for fmt in ("%b %d, %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return ""


def collect():
    # 站点改版会让正则静默失配。宁可炸也不能报"没有新文章"——
    # 那种假阴性会让这套机制悄悄死掉而没人发现。
    entries = parse_sitemap(fetch("sitemap.xml"))
    if len(entries) < 100:
        sys.exit(
            f"[FATAL] sitemap 只解析出 {len(entries)} 条（正常约 400+）。"
            f"sitemap 结构可能变了，先手动看一眼 {BASE}/sitemap.xml 再修 parse_sitemap()。"
        )

    # 索引页首屏的标题/发布日期，能合并多少算多少
    titled = {}
    for s in SECTIONS:
        try:
            for a in parse(fetch(s), s):
                titled[a["slug"]] = a
        except Exception as e:
            print(f"# [warn] /{s} 索引页抓取失败（{e}），该板块条目将没有标题", file=sys.stderr)

    articles = []
    for section, slug, lastmod in entries:
        t = titled.get(slug)
        articles.append(
            {
                "slug": slug,
                "section": section,
                "title": t["title"] if t else "",
                "date": t["date"] if t else "",
                "sort_key": t["sort_key"] if t and t["sort_key"] else lastmod,
                "url": f"{BASE}/{section}/{slug}",
            }
        )

    blog = parse_claude_blog_sitemap(fetch("sitemap.xml", CLAUDE_BASE))
    if len(blog) < 100:
        sys.exit(
            f"[FATAL] claude.com sitemap 只解析出 {len(blog)} 条 blog（正常约 220+）。"
            f"结构可能变了，先手动看一眼 {CLAUDE_BASE}/sitemap.xml 再修 parse_claude_blog_sitemap()。"
        )
    seen = {a["slug"] for a in articles}
    for slug, lastmod in blog:
        if slug in seen:  # 同 slug 两域都有：以 anthropic.com 那条为准
            continue
        seen.add(slug)
        articles.append(
            {
                "slug": slug,
                "section": "blog",
                "title": "",
                "date": "",
                "sort_key": lastmod,
                "url": f"{CLAUDE_BASE}/blog/{slug}",
            }
        )
    return articles


def check_cards(state):
    """已蒸馏 = state 记了账 + cards/ 里有卡。只记账没落盘的条目会被增量清单永远跳过，
    等于人间蒸发，所以要能主动查出来。skipped_at（有意跳过）和 baseline（建基线时
    批量标读，本来就没蒸馏过）不在此列。"""
    have = set()
    for p in CARDS.glob("*.md"):
        m = re.match(r"\d{4}-\d{2}-\d{2}-(.+)\.md$", p.name)
        if m:
            have.add(m.group(1))
    return [
        slug
        for slug, meta in state["distilled"].items()
        if "skipped_at" not in meta
        and meta.get("distilled_at")
        and meta["distilled_at"] != "baseline"
        and slug not in have
    ]


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"distilled": {}}


def save_state(state):
    DATA.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=15)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--section", choices=SECTIONS + ["blog"])
    ap.add_argument("--commit", nargs="+", metavar="SLUG")
    ap.add_argument("--skip", action="store_true", help="配合 --commit：记为有意跳过而非已蒸馏")
    ap.add_argument("--mark-all-read", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.skip and not args.commit:
        ap.error("--skip 只能配合 --commit 用")

    state = load_state()

    if args.check:
        missing = check_cards(state)
        if missing:
            print(f"[FAIL] {len(missing)} 条记了 distilled_at 却找不到卡片：", file=sys.stderr)
            for slug in missing:
                print(f"  - {slug}（缺 cards/*-{slug}.md）", file=sys.stderr)
            print("修法：补卡，或把它改成 skipped_at（--skip --commit <slug>）。", file=sys.stderr)
            sys.exit(1)
        print(f"OK: state 里 {len(state['distilled'])} 条，已蒸馏的每条都有卡。")
        return

    if args.commit:
        field = "skipped_at" if args.skip else "distilled_at"
        for slug in args.commit:
            state["distilled"].setdefault(slug, {})[field] = date.today().isoformat()
        save_state(state)
        verb = "跳过" if args.skip else "已蒸馏"
        print(f"已记录 {len(args.commit)} 篇为{verb}，累计 {len(state['distilled'])} 篇。")
        return

    articles = collect()

    if args.mark_all_read:
        for a in articles:
            state["distilled"].setdefault(a["slug"], {})
            state["distilled"][a["slug"]].update(
                {"section": a["section"], "date": a["date"], "distilled_at": "baseline"}
            )
        save_state(state)
        print(f"基线已建：{len(articles)} 篇标记为已读（未实际蒸馏）。")
        return

    if args.section:
        articles = [a for a in articles if a["section"] == args.section]
    fresh = [a for a in articles if a["slug"] not in state["distilled"]]
    fresh.sort(key=lambda a: a["sort_key"], reverse=True)
    shown = fresh if args.all else fresh[: args.limit]

    print(
        f"# 索引共 {len(articles)} 篇 / 已记账 {len(state['distilled'])} 篇（含跳过）/ "
        f"未蒸馏 {len(fresh)} 篇 / 本次列出 {len(shown)} 篇",
        file=sys.stderr,
    )
    if len(shown) < len(fresh):
        print(
            f"# 注意：还有 {len(fresh) - len(shown)} 篇未列出，加 --all 或 --limit N 取更多",
            file=sys.stderr,
        )
    print(json.dumps(shown, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
