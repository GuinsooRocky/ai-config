#!/usr/bin/env python3
"""meta-check-skill · SKILL.md 审计器（对齐 2026-04 官方 skill 规格）

用法:
    python3 audit.py <name|path|--all>

输入:
    <name>  skill 目录名（如 `write-a-skill`）→ 自动拼 ~/.claude/skills/<name>/SKILL.md
    <path>  直接给 SKILL.md 的绝对路径
    --all   扫 ~/.claude/skills/*/SKILL.md + 当前 cwd 的 .claude/skills/*/SKILL.md

规格来源: https://code.claude.com/docs/en/skills （2026-04 抓取）

输出: 纯 Markdown 报告（用 bullet 不用表格，以兼容用户偏好）
"""

import os
import re
import sys
from pathlib import Path

# ==== 词典（内化自 ref/rubric.md，对齐 2026 官方 frontmatter 表）====

SUPPORTED_FRONTMATTER = {
    'name', 'description', 'when_to_use', 'argument-hint', 'arguments',
    'disable-model-invocation', 'user-invocable', 'allowed-tools',
    'model', 'effort', 'context', 'agent', 'hooks', 'paths', 'shell',
}

# description + when_to_use 合计上限（官方 listing 截断阈值）
DESC_COMBINED_CAP = 1536

ACTION_MARKERS = [
    r'\bMUST\b', r'\bMUST NOT\b', r'\bNEVER\b', r'\bDO NOT\b',
    r'必须', r'永远不', r'永远', r'不要', r'禁止', r'一定要', r'绝对不',
]

HEDGE_MARKERS = [
    r'\bmaybe\b', r'\bprobably\b', r'\bmight\b', r'\bcould\b',
    r'可能', r'或许', r'大概', r'差不多', r'将来', r'\bTODO\b', r'也许',
]

STEP_MARKERS = [
    r'Step\s*\d', r'步骤\s*\d', r'Phase\s*\d', r'阶段\s*\d',
    r'^###?\s+\d+[\.、]',
]

TRIGGER_SECTION = [
    r'use this skill when', r'when to use', r'何时使用', r'何时调用',
    r'触发词', r'触发场景', r'适用', r'\btrigger', r'触发[:：]',
]

# 负面边界：description 里"什么时候不要用本 skill / 该归谁"的指向，防过度触发
NEGATIVE_BOUNDARY = [
    r'\bdo\s+not\s+use\b', r"\bdon'?t\s+use\b", r'\bnot\s+for\b', r'\bnot\s+intended\b',
    r'\binstead\b', r'不触发', r'不归', r'不适用', r'不要用', r'不用于', r'不属于',
    r'不处理', r'不负责', r'不执行', r'别用本',
    r'归\s*[A-Za-z][\w./-]+',  # "开放议题研究归 deep-research" 式路由
]

VERIFY_SECTION = [
    r'verification', r'验证', r'自检', r'反模式', r'已知坑',
    r'known issue', r'gotcha', r'anti.?pattern', r'\bexamples?\b',
    r'示例', r'样例', r'坑',
]

OUTPUT_SECTION = [
    r'\boutput\b', r'输出', r'硬约束', r'格式', r'\bformat\b',
]


# ==== Parsing ====

SPEC_LEAK = {
    '章节号引用': r'§\s*\d',
    '档位符号': r'[🟢🟡🔴🔵⚪]',
    '数值阈值': r'(?:≥|≤|>=|<=|>|<)\s*\d',
    '内部步骤名': r'(?:Step|Phase|步骤)\s*\d',
}


def parse_skill(path: Path):
    text = path.read_text(encoding='utf-8', errors='replace')
    lines = text.splitlines()
    fm = {}
    body_start = 0
    if lines and lines[0].strip() == '---':
        for i, l in enumerate(lines[1:], 1):
            if l.strip() == '---':
                body_start = i + 1
                break
            m = re.match(r'^([\w-]+):\s*(.*)$', l)
            if m:
                fm[m.group(1)] = m.group(2).strip()
    body = '\n'.join(lines[body_start:])
    return {
        'path': str(path),
        'name_folder': path.parent.name,
        'total_lines': len(lines),
        'body_lines': len(lines) - body_start,
        'frontmatter': fm,
        'body': body,
    }


def count_matches(text, patterns):
    total = 0
    for p in patterns:
        total += len(re.findall(p, text, re.IGNORECASE | re.MULTILINE))
    return total


# ==== Scorers（每个返回 (score, issues[])）====

def score_frontmatter(parsed):
    fm = parsed['frontmatter']
    issues, pts = [], 0
    name = fm.get('name', '')
    if name:
        pts += 2
        if name == parsed['name_folder']:
            pts += 3
        else:
            issues.append(f"name `{name}` 与目录 `{parsed['name_folder']}` 不一致 → 改成一致")
    else:
        issues.append("缺 `name` 字段 → frontmatter 加 `name: <目录名>`")

    desc = fm.get('description', '')
    when = fm.get('when_to_use', '')
    combined_len = len(desc) + len(when)
    if desc:
        pts += 3
        L = len(desc)
        if L < 80:
            issues.append(f"description 过短 ({L} 字) → 扩到 ≥80 字，加触发词和具体文件/概念")
        elif L <= 320:
            pts += 3
        elif L <= 600:
            pts += 2
            issues.append(f"description 偏长 ({L} 字) → 压到 ≤320 字。它每轮都占 context，且 skill 一多会被 listing 截断，看到的字反而更少")
        else:
            issues.append(f"description 过长 ({L} 字) → 压到 ≤320 字。超长 description 会互相挤占、被截断，模型更难选对 skill")
        if combined_len > DESC_COMBINED_CAP:
            issues.append(f"description+when_to_use 合计 {combined_len} 字 > 官方 1536 字上限 → 会被 skill listing 截断")
        if count_matches(desc + ' ' + when, TRIGGER_SECTION):
            pts += 2
        else:
            issues.append("description 缺 `使用场景/触发` 类指向 → 加一句 `Use when...` 或 `触发词:`（或用 `when_to_use:` 字段）")
        if re.search(r'`[^`]+`', desc) or '触发词' in desc or re.search(r'\.(md|ts|tsx|py|json|sh|yaml)\b', desc):
            pts += 3
        else:
            issues.append("description 无具体锚点 → 用反引号标出关键文件/触发词")
        leaks = [n for n, pat in SPEC_LEAK.items() if re.search(pat, desc)]
        if leaks:
            pts -= 1
            issues.append(
                f"description 里混了运行时规格（{'、'.join(leaks)}）→ 搬进 body。"
                "选不选这个 skill 不需要知道它内部怎么分档/什么阈值/哪些子步骤")
    else:
        issues.append("缺 `description` 字段 → 这是 skill 自动触发的唯一依据")

    unknown = set(fm) - SUPPORTED_FRONTMATTER
    if not unknown:
        pts += 4
    else:
        issues.append(f"frontmatter 含非官方字段 {sorted(unknown)} → 删掉（否则被静默忽略；官方 15 字段表见 https://code.claude.com/docs/en/skills）")
    return pts, issues


def score_triggering(parsed):
    body = parsed['body']
    desc = parsed['frontmatter'].get('description', '')
    when = parsed['frontmatter'].get('when_to_use', '')
    combined = desc + '\n' + when + '\n' + body
    issues, pts = [], 0

    if re.search(r'触发词[:：]|trigger(?:s|\s+words?)[:：]', combined, re.IGNORECASE):
        pts += 8
    else:
        issues.append("没显式列触发词 → 在 description / when_to_use / body 加 `触发词: xxx、yyy、zzz`")

    # 触发变体：先抓引号内短语，再补 `触发词: a、b、c` / `Examples: "x", "y"` 这种散文形式
    text_for_variants = desc + '\n' + when
    variants = re.findall(r'["""\'`]([^"""\'`\n]{2,30})["""\'`]', text_for_variants)
    # 散文式：触发词 / trigger 后面到下一个段落终止符之间，按中英标点切
    prose_match = re.search(
        r'(?:触发词|trigger(?:s|\s+words?)?)[:：]\s*([^\n。.]{2,200})',
        text_for_variants, re.IGNORECASE)
    if prose_match:
        chunk = prose_match.group(1)
        for piece in re.split(r'[、,，/／|｜；;]', chunk):
            piece = piece.strip(' \t"""\'`*-')
            if 2 <= len(piece) <= 30:
                variants.append(piece)
    unique_variants = set(v.strip() for v in variants if v.strip())
    if len(unique_variants) >= 3:
        pts += 8
    elif len(unique_variants) >= 1:
        pts += 4
        issues.append(f"触发变体偏少 ({len(unique_variants)}) → 补到 ≥3 种（中英混合、口语+书面）")
    else:
        issues.append("description 一个加引号的触发词都没有 → 加 3-5 个变体")

    # 负面边界只看 desc + when_to_use（自动触发的判断依据），body 里的不算
    if len(unique_variants) >= 6:
        vs = sorted(unique_variants)

        def _shares(a, b):
            # 共享一段 >=3 字的连续片段 = 同一意图的同义变体
            return any(a[i:i + 3] in b for i in range(len(a) - 2))

        dup = sum(1 for a in vs if any(a != b and _shares(a, b) for b in vs))
        if dup / len(vs) > 0.5:
            pts -= 2
            issues.append(
                f"触发词冗余：{len(vs)} 个里 {dup} 个共享同一词根（同一意图的同义变体）"
                " → 每个意图留 1-2 个最典型的，召回不会掉，省下的字给负面边界")

    if count_matches(desc + '\n' + when, NEGATIVE_BOUNDARY):
        pts += 4
    else:
        issues.append("description 缺负面边界 → 加一句『X 不归本 skill / 开放议题归 <other-skill> / Do NOT use for X』防过度触发")
    return pts, issues


def score_structure(parsed):
    body = parsed['body']
    issues, pts = [], 0

    lead = body[:600]
    if count_matches(lead, TRIGGER_SECTION):
        pts += 5
    else:
        issues.append("body 前 600 字缺前置触发场景段 → 开头加 `## 何时使用` 段")

    step_count = count_matches(body, STEP_MARKERS)
    if step_count >= 3:
        pts += 5
    elif step_count >= 1:
        pts += 2
        issues.append(f"步骤偏少 ({step_count}) → 拆成 ≥3 步（`Step 1 / Step 2 / Step 3`）")
    else:
        issues.append("没有分步骤 → 加 `Step 1 / 步骤 1 / Phase 1` 分段")

    if count_matches(body, OUTPUT_SECTION):
        pts += 5
    else:
        issues.append("没有输出格式段 → 加 `## 输出格式` 说明硬约束")

    if count_matches(body, VERIFY_SECTION):
        pts += 5
    else:
        issues.append("没有验证/反模式段 → 加 `## 反模式` 或 `## 已知坑`")
    return pts, issues


def score_simplicity(parsed):
    body = parsed['body']
    issues, pts = [], 0

    if parsed['total_lines'] <= 500:
        pts += 5
    else:
        issues.append(f"SKILL.md {parsed['total_lines']} 行 > 500 → 拆到 `ref/` 按需加载")

    hedge = count_matches(body, HEDGE_MARKERS)
    if hedge <= 3:
        pts += 5
    else:
        issues.append(f"犹豫词 {hedge} 处 (maybe/可能/或许/TODO 等) → 精简到 ≤3")

    action = count_matches(body, ACTION_MARKERS)
    if action >= 5:
        pts += 5
    elif action >= 2:
        pts += 3
        issues.append(f"硬约束词 {action} 处 → 至少 5 处 MUST/必须/不要/NEVER（否则 skill 变软建议）")
    else:
        issues.append(f"硬约束词 {action} 处 → 必须 ≥5 处 MUST/必须/不要/NEVER")

    if re.search(r'AbstractFactory|Helper.*Helper|Manager.*Manager|BaseBase', body):
        issues.append("body 出现空壳抽象命名 → 删掉")
    else:
        pts += 5
    return pts, issues


def score_drift(parsed):
    body = parsed['body']
    fm = parsed['frontmatter']
    issues, pts = [], 0

    unknown = set(fm) - SUPPORTED_FRONTMATTER
    if not unknown:
        pts += 10
    else:
        issues.append(f"非官方字段 {sorted(unknown)} → 删掉（二次扣分，看第 1 维建议）")

    # 路径存在性：只对 /... 或 ~/... 且看起来像文件的
    path_pattern = re.compile(r'(?:^|[\s`(])(/Users/[\w./-]+|~/[\w./-]+)')
    cand = set(path_pattern.findall(body))
    missing = []
    for p in cand:
        expanded = os.path.expanduser(p)
        if '<' in expanded or '*' in expanded or expanded.startswith('/tmp'):
            continue
        if not re.search(r'\.(md|py|sh|tsx?|jsx?|jsonl?|yaml|html|css|mdx)$', expanded):
            # 目录或无扩展名 —— 跳过
            continue
        if not os.path.exists(expanded):
            missing.append(p)
    if not missing:
        pts += 5
    else:
        shown = missing[:3]
        suffix = f" ... 共 {len(missing)} 处" if len(missing) > 3 else ''
        issues.append(f"引用了不存在的路径 {shown}{suffix} → 删掉或修正")

    if count_matches(body, [r'示例', r'样例', r'参考输出', r'dogfood', r'example', r'reference output']):
        pts += 5
    else:
        issues.append("缺示例/参考输出段 → 加一段 `## 示例输出` 贴一份真实产物")
    return pts, issues


# ==== Grade & Report ====

def grade(score):
    if score >= 90:
        return 'A (高质量)'
    if score >= 75:
        return 'B (能用，小瑕疵)'
    if score >= 60:
        return 'C (能触发但行为不稳)'
    return 'D (返工)'


def audit_one(path: Path):
    parsed = parse_skill(path)
    categories = {
        'Frontmatter': score_frontmatter(parsed),
        'Triggering': score_triggering(parsed),
        'Structure': score_structure(parsed),
        'Simplicity': score_simplicity(parsed),
        'Drift': score_drift(parsed),
    }
    total = sum(s[0] for s in categories.values())
    return {
        'path': str(path),
        'name': parsed['frontmatter'].get('name', '(缺 name)'),
        'total': total,
        'grade': grade(total),
        'lines': parsed['total_lines'],
        'categories': categories,
    }


def prioritize(categories):
    """按单项能补多少分排 Top 3 修复。"""
    gaps = []
    for cat, (score, issues) in categories.items():
        deficit = 20 - score
        if deficit > 0 and issues:
            for iss in issues:
                gaps.append((deficit, cat, iss))
    gaps.sort(key=lambda x: -x[0])
    prios = []
    for deficit, cat, iss in gaps[:3]:
        if deficit >= 5:
            tag = '高'
        elif deficit >= 3:
            tag = '中'
        else:
            tag = '低'
        prios.append((tag, cat, iss))
    return prios


def format_one(result):
    out = []
    out.append(f"## {result['name']} — {result['total']}/100 · {result['grade']}")
    out.append(f"- 路径: `{result['path']}`  ·  {result['lines']} 行")
    out.append('')
    for cat, (score, issues) in result['categories'].items():
        out.append(f"### {cat}: {score}/20")
        if issues:
            for i in issues:
                out.append(f"- ⚠️ {i}")
        else:
            out.append("- ✅ 满分")
        out.append('')
    prios = prioritize(result['categories'])
    if prios:
        out.append("### Top 3 修复优先级")
        for tag, cat, iss in prios:
            out.append(f"- [{tag}] **{cat}**: {iss}")
    return '\n'.join(out)


def format_summary(results):
    out = ['# Meta-Check Skill · 批量审计']
    out.append('')
    out.append('## 汇总排名')
    for r in sorted(results, key=lambda x: -x['total']):
        out.append(f"- **{r['name']}** — {r['total']}/100 · {r['grade']} · {r['lines']} 行")
    out.append('')
    out.append('---')
    out.append('')
    for r in sorted(results, key=lambda x: -x['total']):
        out.append(format_one(r))
        out.append('')
    return '\n'.join(out)


# ==== CLI ====

def resolve_input(arg):
    if arg == '--all':
        # 同时扫 personal (~/.claude/skills/) 和当前 cwd 的 project (./.claude/skills/)
        # 官方 2026 规格 4 种存放位置：enterprise / personal / project / plugin
        personal = Path.home() / '.claude' / 'skills'
        project = Path.cwd() / '.claude' / 'skills'
        found = list(personal.glob('*/SKILL.md'))
        if project.exists() and project != personal:
            found += list(project.glob('*/SKILL.md'))
        return sorted(found)
    p = Path(arg)
    if p.is_file():
        return [p]
    # 名字搜索：先看 personal，再看 cwd 的 project skills
    for base in (Path.home() / '.claude' / 'skills', Path.cwd() / '.claude' / 'skills'):
        cand = base / arg / 'SKILL.md'
        if cand.is_file():
            return [cand]
    print(f'[error] 无法解析输入: {arg}', file=sys.stderr)
    print('  - skill 目录名 (~/.claude/skills/<name>/SKILL.md 或 ./.claude/skills/<name>/SKILL.md)', file=sys.stderr)
    print('  - 绝对路径到 SKILL.md', file=sys.stderr)
    print('  - --all (扫 personal + 当前 cwd 的 project skills)', file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print('usage: audit.py <name|path|--all>', file=sys.stderr)
        sys.exit(1)
    targets = resolve_input(sys.argv[1])
    results = [audit_one(p) for p in targets]
    if len(results) == 1:
        print(format_one(results[0]))
    else:
        print(format_summary(results))


if __name__ == '__main__':
    main()
