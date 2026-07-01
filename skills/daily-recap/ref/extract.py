#!/usr/bin/env python3
"""daily-recap 提取脚本 —— 按 SKILL.md 要求抽每个 jsonl 的真实 user 消息 + tool 统计 + 关键词标记。

用法:
    python3 extract.py <jsonl_path> [<jsonl_path> ...]
输出 JSON（stdout），字段:
    - session_id: 文件 basename 前 8 位
    - size_mb: 文件大小 MB
    - cwds: 去重后的 cwd 列表
    - user_msgs: 过滤后的真实用户消息（前 250 字）
    - tool_uses: 工具调用次数 dict（降序前 15）
    - keywords: 命中的主题关键词 dict（关键词 → 命中次数）
    - context_resets: `This session is being continued from` 出现次数（判断是否需要通读）
"""

import json
import os
import sys
import re

NOISE_MARKERS = (
    '<system-reminder>',
    '<command-name>',
    '<user-prompt-submit-hook>',
    '<task-notification>',
    '<local-command-caveat>',
    '<local-command-stdout>',
    '<local-command-',
)

KEYWORDS = [
    # 里程碑
    'issue', 'PR', 'Discussion', 'Phase',
    # 分支 / agent / skill
    'worktree', '@agent-', 'commit-cr', 'skill',
    # onlychat / UI
    '走查', 'Figma', 'TagListV2', 'TagBoxV2', 'useGradualRollout', 'home_ui_revamp',
    # CICD
    'Gitea', 'runner', '飞书', 'CI/CD',
    # 升级
    'Turbopack', 'Next 15', 'Next 14', 'Bun',
    # 模式
    'autonomous-loop', 'ScheduleWakeup',
]


def extract_user_text(msg):
    content = msg.get('content', '')
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        for c in content:
            if isinstance(c, dict) and c.get('type') == 'text':
                return c.get('text', '')
    return ''


def is_noise(txt: str) -> bool:
    if not txt:
        return True
    if any(m in txt for m in NOISE_MARKERS):
        return True
    if txt.startswith('Caveat') or txt.startswith('[Request interrupted'):
        return True
    return False


def scan_jsonl(path: str) -> dict:
    sid = os.path.basename(path)[:8]
    size_mb = round(os.path.getsize(path) / (1024 * 1024), 2)
    cwds = set()
    user_msgs = []
    tool_uses = {}
    context_resets = 0
    raw_blob = ''

    with open(path, 'r', errors='replace') as fp:
        for line in fp:
            raw_blob += line  # for keyword scan
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue

            cwd = o.get('cwd')
            if cwd:
                cwds.add(cwd)

            t = o.get('type')
            if t == 'user':
                msg = o.get('message', {})
                txt = extract_user_text(msg)
                if is_noise(txt):
                    continue
                if 'This session is being continued from' in txt:
                    context_resets += 1
                    continue
                user_msgs.append(txt[:250].replace('\n', ' ').strip())
            elif t == 'assistant':
                msg = o.get('message', {})
                content = msg.get('content', [])
                if isinstance(content, list):
                    for c in content:
                        if isinstance(c, dict) and c.get('type') == 'tool_use':
                            nm = c.get('name', '?')
                            tool_uses[nm] = tool_uses.get(nm, 0) + 1

    # Keyword scan on the raw blob (case-insensitive, except for 中文/特定大小写)
    keywords_hit = {}
    lower_blob = raw_blob.lower()
    for kw in KEYWORDS:
        if kw.isascii() and not kw[0].isupper():
            c = lower_blob.count(kw.lower())
        else:
            c = raw_blob.count(kw)
        if c > 0:
            keywords_hit[kw] = c

    top_tools = dict(sorted(tool_uses.items(), key=lambda x: -x[1])[:15])

    return {
        'session_id': sid,
        'size_mb': size_mb,
        'cwds': sorted(cwds),
        'user_msgs_count': len(user_msgs),
        'user_msgs_first5': user_msgs[:5],
        'user_msgs_last5': user_msgs[-5:] if len(user_msgs) > 5 else [],
        'tool_uses': top_tools,
        'keywords': keywords_hit,
        'context_resets': context_resets,
    }


def main():
    if len(sys.argv) < 2:
        print('usage: extract.py <jsonl_path> [...]', file=sys.stderr)
        sys.exit(1)
    results = []
    for p in sys.argv[1:]:
        if not os.path.exists(p):
            print(f'[warn] not found: {p}', file=sys.stderr)
            continue
        results.append(scan_jsonl(p))
    json.dump(results, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
