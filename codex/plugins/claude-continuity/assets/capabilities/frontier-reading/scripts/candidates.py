#!/usr/bin/env python3
"""捞近期候选读物：HuggingFace 每日论文（按 upvotes）+ arXiv RSS（按标题关键词）。

只产候选清单，不做筛选判断——筛选归 SKILL.md 的四问 rubric。
"""
import argparse
import datetime as dt
import json
import urllib.request
import xml.etree.ElementTree as ET

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

REPORT_KEYS = ["technical report", "system card", "model card"]
SAFETY_KEYS = [
    "safety", "alignment", "deception", "deceptive", "scheming", "sandbagging",
    "dangerous capabilit", "red team", "oversight", "monitorab", "jailbreak",
    "sabotage", "situational awareness",
]


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def hf_papers(days, min_up):
    try:
        data = json.loads(fetch("https://huggingface.co/api/daily_papers?limit=100"))
    except Exception as e:
        print(f"  [HF 拉取失败：{e}]")
        return
    cutoff = (dt.date.today() - dt.timedelta(days=days)).isoformat()
    rows = []
    for it in data:
        p = it.get("paper", {}) or {}
        pub = (p.get("publishedAt") or "")[:10]
        up = p.get("upvotes") or 0
        if pub >= cutoff and up >= min_up:
            rows.append((up, pub, (p.get("title") or "").strip(), p.get("id") or ""))
    rows.sort(reverse=True)
    if not rows:
        print(f"  （近 {days} 天内没有 ≥{min_up} 赞的）")
    for up, pub, title, aid in rows:
        print(f"  {up:>4}↑  {pub}  {title}")
        print(f"        https://arxiv.org/abs/{aid}")


def arxiv_rss(feeds):
    hits = {"报告类": [], "安全/对齐线": []}
    for feed in feeds:
        try:
            raw = fetch(f"https://rss.arxiv.org/rss/{feed}")
        except Exception as e:
            print(f"  [{feed} 拉取失败：{e}]")
            continue
        try:
            root = ET.fromstring(raw)
        except ET.ParseError as e:
            print(f"  [{feed} 解析失败：{e}]")
            continue
        for item in root.iter("item"):
            title = (item.findtext("title") or "").strip().replace("\n", " ")
            link = (item.findtext("link") or "").strip()
            low = title.lower()
            if any(k in low for k in REPORT_KEYS):
                hits["报告类"].append((title, link, feed))
            elif any(k in low for k in SAFETY_KEYS):
                hits["安全/对齐线"].append((title, link, feed))
    for group, rows in hits.items():
        print(f"\n  --- {group} ---")
        if not rows:
            print("  （本次 feed 无命中）")
        seen = set()
        for title, link, feed in rows:
            if link in seen:
                continue
            seen.add(link)
            print(f"  [{feed}] {title}")
            print(f"        {link}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7, help="时间窗口，默认 7 天")
    ap.add_argument("--min-upvotes", type=int, default=20, help="HF 赞数门槛，默认 20")
    ap.add_argument("--feeds", default="cs.CL,cs.AI", help="arXiv feed，逗号分隔")
    a = ap.parse_args()

    print(f"== HuggingFace 每日论文（近 {a.days} 天，≥{a.min_upvotes} 赞）==")
    hf_papers(a.days, a.min_upvotes)
    print(f"\n== arXiv RSS 标题命中（feed 只含当日最新一批，与 --days 无关）==")
    arxiv_rss([f.strip() for f in a.feeds.split(",") if f.strip()])
    print("\n注：以上只是候选。必须按 SKILL.md 四问 rubric 筛，且推荐前要真读过正文。")


if __name__ == "__main__":
    main()
