#!/usr/bin/env python3
"""OnlyChat 埋点工具 —— 静态自测 + 归属 + 气泡数据。

子命令（在 OnlyChat 仓库根目录跑）：
  owner-split <prefix> <email>   git blame registry，把 <prefix> 事件按作者分「你的 / 别人的」
  orphan <prefix>                列出 <prefix> 里有 registry key 但代码无 call-site 的（未用键）
  audit <input.tsv> <prefix>     静态自测：缺口/多余/参数缺失/字面值不符/prefix错位/PII/翻译文本
  tips <prefix>                  抓每个事件的 call-site → 输出 HTML 气泡 TIPS 骨架（file:line + fn）

audit 的 input.tsv（无表头，Tab 分隔）：
  col1 = cus.* 事件名（必填）
  col2 = 该事件 PM 要求的参数名，逗号分隔（可空）
  col3 = 期望字面值，分号分隔的 key=val（可空，只校验代码里写死的字面量）
例：
  cus.click_nav_create_world\tsource\tsource=home_plus_dialog

约定：registry 在 src/tracking/registry/{click,view,logic}.ts；call-site 扫 src/。
"""
import os
import re
import subprocess
import sys

REG_DIR = "src/tracking/registry"
REG_FILES = {"click": "click.ts", "view": "view.ts", "logic": "logic.ts"}
SRC_DIRS = ["src/components", "src/app", "src/hooks", "src/lib"]
KEY_RE = re.compile(r"'([a-z0-9][a-z0-9-]*)'\s*:\s*'(cus\.[A-Za-z0-9_.]+)'")
CALL_RE_T = r"\b(tc|tv|tl|useTv)\(\s*'%s'"
PII_RE = re.compile(r"\b[\w.]+@[\w.]+\.\w+\b|\b1[3-9]\d{9}\b")


def sh(args):
    return subprocess.run(args, capture_output=True, text=True).stdout


def load_registry():
    """return {kebab: (cus, table)} ，table ∈ click/view/logic"""
    reg = {}
    for table, fname in REG_FILES.items():
        path = os.path.join(REG_DIR, fname)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            for line in f:
                m = KEY_RE.search(line)
                if m:
                    reg[m.group(1)] = (m.group(2), table)
    return reg


def grep_callsites():
    """return {kebab: [(file, lineno)]}"""
    out = {}
    pat = r"\b(tc|tv|tl|useTv)\(\s*'(worldcard-[a-z0-9-]+|[a-z0-9][a-z0-9-]*)'"
    for d in SRC_DIRS:
        if not os.path.isdir(d):
            continue
        res = sh(["grep", "-rEn", pat, d])
        for ln in res.splitlines():
            mm = re.match(r"(.+?):(\d+):", ln)
            km = re.search(r"\b(?:tc|tv|tl|useTv)\(\s*'([a-z0-9][a-z0-9-]*)'", ln)
            if mm and km:
                out.setdefault(km.group(1), []).append((mm.group(1), int(mm.group(2))))
    return out


def read_call(path, lineno):
    """从 call 起读到括号配平，返回整段表达式文本（best-effort 提参数用）"""
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
    except OSError:
        return ""
    buf, depth, started = [], 0, False
    for i in range(lineno - 1, min(lineno + 30, len(lines))):
        s = lines[i]
        buf.append(s)
        for ch in s:
            if ch == "(":
                depth += 1
                started = True
            elif ch == ")":
                depth -= 1
        if started and depth <= 0:
            break
    return "".join(buf)


def extract_params(call_text):
    """从 call 文本里抠 params 对象的 key + 字面量 value（best-effort）"""
    m = re.search(r"params\s*:\s*\{", call_text)
    if not m:
        return set(), {}
    i = m.end() - 1
    depth, end = 0, len(call_text)
    for j in range(i, len(call_text)):
        if call_text[j] == "{":
            depth += 1
        elif call_text[j] == "}":
            depth -= 1
            if depth == 0:
                end = j
                break
    body = call_text[i + 1:end]
    keys = set(re.findall(r"(\w+)\s*:", body))
    lits = dict(re.findall(r"(\w+)\s*:\s*'([^']*)'", body))
    return keys, lits


# ---------- owner-split ----------
def cmd_owner_split(prefix, email):
    reg = load_registry()
    keys = sorted(k for k in reg if k.startswith(prefix))
    blame = {}
    for table, fname in REG_FILES.items():
        path = os.path.join(REG_DIR, fname)
        if not os.path.exists(path):
            continue
        out = sh(["git", "blame", "-e", "--line-porcelain", path])
        cur_mail = None
        for ln in out.splitlines():
            if ln.startswith("author-mail "):
                cur_mail = ln.split(" ", 1)[1].strip("<>")
            elif ln.startswith("\t"):
                for k in keys:
                    if "'%s'" % k in ln:
                        blame[k] = cur_mail
    mine = [k for k in keys if blame.get(k) == email]
    other = [(k, blame.get(k)) for k in keys if blame.get(k) != email]
    print("== 归属分组（registry blame，前缀 %s）==" % prefix)
    print("\n✅ 你的（%s，%d）：" % (email, len(mine)))
    for k in mine:
        print("  %s  %s" % (k, reg[k][0]))
    print("\n❌ 别人的（不碰代码，%d）：" % len(other))
    for k, m in other:
        print("  %s  %s  ← %s" % (k, reg[k][0], m))


# ---------- orphan ----------
def cmd_orphan(prefix):
    reg = load_registry()
    calls = grep_callsites()
    keys = sorted(k for k in reg if k.startswith(prefix))
    orphans = [k for k in keys if k not in calls]
    print("== 未用 registry key（前缀 %s，无 call-site）==" % prefix)
    if not orphans:
        print("✅ 全部有 call-site")
        return
    for k in orphans:
        print("  %s  %s" % (k, reg[k][0]))
    print("\n（确认确实不要 → 删 registry；否则补 call-site。chat-* 等别人的先 owner-split 排除）")
    sys.exit(1)


# ---------- audit ----------
def cmd_audit(tsv, prefix):
    reg = load_registry()
    cus2kebab = {v[0]: k for k, v in reg.items()}
    calls = grep_callsites()
    rows = []
    with open(tsv, encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#"):
                continue
            parts = (line.rstrip("\n").split("\t") + ["", ""])[:3]
            cus = parts[0].strip()
            need = [p.strip() for p in parts[1].split(",") if p.strip()]
            want = dict(
                kv.split("=", 1) for kv in parts[2].split(";") if "=" in kv
            )
            rows.append((cus, need, want))
    want_cus = {r[0] for r in rows}
    problems = []

    for cus, need, want in rows:
        kebab = cus2kebab.get(cus)
        if not kebab:
            problems.append("缺口·无 registry：%s" % cus)
            continue
        sites = calls.get(kebab, [])
        if not sites:
            problems.append("缺口·无 call-site：%s (%s)" % (cus, kebab))
            continue
        # 参数 + 字面值（合并所有 call-site 的 params）
        keys, lits = set(), {}
        for path, ln in sites:
            k, l = extract_params(read_call(path, ln))
            keys |= k
            lits.update(l)
        miss = [p for p in need if p not in keys]
        if miss:
            problems.append("缺参数：%s 少 %s（call 现有 %s）" % (cus, miss, sorted(keys) or "无"))
        for k, v in want.items():
            if k in lits and lits[k] != v:
                problems.append("取值不符：%s 的 %s 代码='%s' ≠ PM='%s'" % (cus, k, lits[k], v))
        # PII / 翻译
        for path, ln in sites:
            txt = read_call(path, ln)
            pm = re.search(r"params\s*:\s*\{", txt)
            if pm:
                body = txt[pm.end():]
                if "t(" in body:
                    problems.append("参数疑似翻译文本(t(...))：%s @ %s:%d" % (cus, path, ln))
                if PII_RE.search(body):
                    problems.append("参数疑似 PII：%s @ %s:%d" % (cus, path, ln))

    # prefix 错位
    table_prefix = {"click": "cus.click_", "view": "cus.view_", "logic": None}
    for k, (cus, table) in reg.items():
        if not k.startswith(prefix):
            continue
        exp = table_prefix[table]
        if exp and not cus.startswith(exp):
            problems.append("prefix错位：%s 在 %s.ts 但值是 %s" % (k, table, cus))

    # 多余：registry 该前缀事件不在清单
    extra = [
        reg[k][0] for k in reg if k.startswith(prefix) and reg[k][0] not in want_cus and k in calls
    ]
    for cus in sorted(extra):
        problems.append("多余·清单无（实现有 call-site）：%s" % cus)

    print("== 埋点静态自测（前缀 %s，清单 %d 条）==" % (prefix, len(rows)))
    if not problems:
        print("✅ 零残留：覆盖/参数/取值/prefix/PII/多余 全通过")
        return
    for p in problems:
        print("  ✗ " + p)
    print("\n共 %d 处。修完再跑；运行时再验「会不会真触发 + 动态值」。" % len(problems))
    sys.exit(1)


# ---------- tips ----------
def cmd_tips(prefix):
    reg = load_registry()
    calls = grep_callsites()
    print("// HTML 气泡 TIPS 骨架（file:line + fn 已填，tier/位置/路径 你补）")
    print("// tier: 浅 / 弹 / 深 / 系")
    for k in sorted(k for k in reg if k.startswith(prefix)):
        cus = reg[k][0]
        site = calls.get(k, [("?", 0)])[0]
        f = site[0].split("/")[-1] + ":" + str(site[1]) if site[1] else "?"
        print("  '%s':['', '', '', '%s']," % (cus, f))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    cmd = sys.argv[1]
    a = sys.argv[2:]
    if cmd == "owner-split" and len(a) == 2:
        cmd_owner_split(a[0], a[1])
    elif cmd == "orphan" and len(a) == 1:
        cmd_orphan(a[0])
    elif cmd == "audit" and len(a) == 2:
        cmd_audit(a[0], a[1])
    elif cmd == "tips" and len(a) == 1:
        cmd_tips(a[0])
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
