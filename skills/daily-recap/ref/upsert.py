#!/usr/bin/env python3
"""单文件日报 upsert + 22 天保鲜（确定性，幂等）。

用法：
    python3 upsert.py <每日复盘.md 路径> < section.txt

stdin 是一天的完整 section（首行为裸文本日期标题 `YY.M.D-星期` 或
周末 `YY.M.{D1}~{D2}-周末`，其后是 bullet）。脚本会：
  1. 读出已有文件，按日期标题切成若干 section
  2. 用同标题（同一天 / 同一个周末）的新 section 覆盖旧的；没有就插入
  3. 按起始日期升序（最新在最下）排好
  4. 只留最近 22 天：丢掉 起始日 < 最新 section 起始日 − 21 天 的 section
  5. 以 `\n\n---\n\n` 分隔回写

设计：prune 锚点永远取「文件里最新的 section」，与调用顺序无关——
backfill 逐天 upsert 也不会误删较新的天。
"""
import sys
import re
from datetime import date

HEADING = re.compile(r'^(\d{2})\.(\d{1,2})\.(\d{1,2})')  # 26.6.25 / 26.6.13~14
SEP = '\n\n---\n\n'


def startdate(heading_line):
    m = HEADING.match(heading_line.strip())
    if not m:
        return None
    yy, mm, dd = (int(x) for x in m.groups())
    return date(2000 + yy, mm, dd)


def split_sections(text):
    """切成 [(startdate, heading_line, full_section_text), ...]，顺序无所谓。"""
    lines = text.splitlines()
    sections = []
    cur = []
    for ln in lines:
        if HEADING.match(ln.strip()) and startdate(ln) is not None:
            if cur:
                sections.append(cur)
            cur = [ln]
        elif cur is not None and cur:
            # 跳过 section 间的 --- 分隔与多余空行（回写时统一重建）
            cur.append(ln)
    if cur:
        sections.append(cur)

    out = []
    for blk in sections:
        # 去掉块首尾空行 / 残留的 --- 分隔线
        body = [l for l in blk]
        while body and body[-1].strip() in ('', '---'):
            body.pop()
        while len(body) > 1 and body[1:] and body[-1].strip() == '':
            break
        sd = startdate(body[0])
        out.append((sd, body[0].strip(), '\n'.join(body).rstrip()))
    return out


def main():
    if len(sys.argv) != 2:
        sys.exit('usage: upsert.py <每日复盘.md> < section.txt')
    path = sys.argv[1]
    new_text = sys.stdin.read().strip()
    if not new_text:
        sys.exit('empty section on stdin')

    new_sd = startdate(new_text.splitlines()[0])
    if new_sd is None:
        sys.exit('new section 首行不是合法日期标题：' + new_text.splitlines()[0])
    new_heading = new_text.splitlines()[0].strip()

    try:
        with open(path, encoding='utf-8') as f:
            existing = f.read()
    except FileNotFoundError:
        existing = ''

    secs = split_sections(existing)
    # 同标题覆盖（同一天 / 同一个周末标题）
    secs = [s for s in secs if s[1] != new_heading]
    secs.append((new_sd, new_heading, new_text))

    # 22 天保鲜：锚点 = 最新 section 起始日
    newest = max(s[0] for s in secs)
    secs = [s for s in secs if (newest - s[0]).days <= 21]

    secs.sort(key=lambda s: s[0])  # 升序，最新在最下
    body = SEP.join(s[2] for s in secs)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(body.rstrip() + '\n')

    print(f'upsert {new_heading} → {path}（{len(secs)} 天，保鲜锚点 {newest}）')


if __name__ == '__main__':
    main()
