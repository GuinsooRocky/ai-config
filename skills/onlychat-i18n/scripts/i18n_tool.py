#!/usr/bin/env python3
"""onlychat-i18n 确定性工具。从 onlychat worktree 根目录跑（读 src/i18n/*.json，扫 src/）。

子命令:
  inventory  列前缀 key 的 en值/位置 + 复用机会 + 缺en
  html       生成 HTML 清单（① 新建 ② 复用，位置去重）
  tsv        生成 key\\tEN 的 TSV，--copy 顺便进剪贴板
  reuse      给英文列表（--strings-file，每行一条），查 15/15 现成 key
  reuse-audit 【硬闸】自动扫新建前缀 key，值撞现成全语言键的 = 必须复用（出飞书清单前必跑，命中非零退出）
  snapshot   导出当前前缀 key 列表（跑 pnpm i18n 前存）
  verify     跑 pnpm i18n 后：对比 snapshot，存活/丢失 + 翻译缺口 + git diff
  gitdiff    【权威源】git diff en.json 定增删（+进飞书 -删飞书），跨前缀不漏
  baseline   接代码前拍 en.json 全量基线（配 tsv --baseline 出差集）
  dups       扫同前缀、同 en 值的 key（同值=按概念重复，逐组合并）
  plan       接代码前的审查 HTML（读 plan.tsv）
通用参数: --prefix（如 worldcard_）--scope（默认 src）--i18n-dir（默认 src/i18n）
         --exclude 别人 key 清单文件（每行一个，inventory/html/tsv/snapshot 会跳过）
"""
import argparse, re, os, json, sys, subprocess, html as H, datetime, tempfile

LOCALES = ['en','pt','ru','de','it','fr','pl','es','id','ja','ko','fil','hi','ar','zh-tw']


def copy_grid(pairs):
    """把 [(key, en), ...] 以 HTML <table> 进剪贴板（text/html flavor）。
    关键：Feishu Sheets 对纯文本 TSV 不拆格——整块塞进一个单元格；只认富文本表格。
    HTML 表格在 Feishu / Google Sheets / Excel 都会按 行/列 拆成网格。
    osascript 失败（非 macOS / 无权限）则回退纯 TSV（Google/Excel 仍可，Feishu 退化为单格）。
    返回 True=HTML 成功 / False=回退 TSV。"""
    cells = '\n'.join(
        f'<tr><td>{H.escape(k)}</td><td>{H.escape(v)}</td></tr>' for k, v in pairs
    )
    doc = f'<meta charset="utf-8"><table><tbody>\n{cells}\n</tbody></table>'
    f = tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8')
    f.write(doc)
    f.close()
    try:
        subprocess.run(
            ['osascript', '-e',
             f'set the clipboard to (read (POSIX file "{f.name}") as «class HTML»)'],
            check=True, capture_output=True)
        return True
    except Exception as e:
        tsv = '\n'.join(f'{k}\t{v}' for k, v in pairs) + '\n'
        try:
            subprocess.run(['pbcopy'], input=tsv.encode('utf-8'), check=True)
        except Exception:
            pass
        print(f"  ⚠️ HTML 剪贴板失败，已回退纯 TSV: {e}")
        return False
    finally:
        try:
            os.unlink(f.name)
        except Exception:
            pass
# lookbehind 防 format(/report( 误匹配；覆盖 t('k') t("k") t(`k`) t.rich('k'
KEY_RE = re.compile(r"(?<![A-Za-z0-9_])t(?:\.rich)?\(\s*['\"`]([a-zA-Z0-9_]+)['\"`]")


def load_locales(d):
    out = {}
    for l in LOCALES:
        p = os.path.join(d, f'{l}.json')
        out[l] = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
    return out


def fully_set(data):
    en = data['en']
    return {k for k, v in en.items()
            if isinstance(v, str) and all(data[l].get(k) for l in LOCALES)}


def scan_code(scope):
    """{key: ['relpath:line', ...]} 全部 t() key。"""
    occ = {}
    for root, dirs, files in os.walk(scope):
        dirs[:] = [d for d in dirs if d not in ('node_modules', '.next')]
        if os.path.join('src', 'i18n') in root:
            continue
        for fn in files:
            if not fn.endswith(('.ts', '.tsx')):
                continue
            fp = os.path.join(root, fn)
            rel = fp[4:] if fp.startswith('src/') else fp
            try:
                lines = open(fp, encoding='utf-8', errors='ignore').read().splitlines()
            except Exception:
                continue
            for i, line in enumerate(lines, 1):
                for m in KEY_RE.finditer(line):
                    occ.setdefault(m.group(1), []).append(f"{rel}:{i}")
    return occ


def load_exclude(p):
    return {x.strip() for x in open(p)} if p and os.path.exists(p) else set()


def split_keys(occ, prefix, exclude):
    """occ -> (新建前缀key dict, 复用非前缀key dict)"""
    new = {k: v for k, v in occ.items() if k.startswith(prefix) and k not in exclude}
    reused = {k: v for k, v in occ.items() if not k.startswith(prefix)}
    return new, reused


def cmd_inventory(a):
    data = load_locales(a.i18n_dir); en = data['en']; full = fully_set(data)
    occ = scan_code(a.scope); exclude = load_exclude(a.exclude)
    new, _ = split_keys(occ, a.prefix, exclude)
    # 反查：en value -> 现成全语言 key（非本前缀）
    val2key = {}
    for k in full:
        if not k.startswith(a.prefix):
            val2key.setdefault(en[k].strip(), []).append(k)
    print(f"== 前缀 {a.prefix} 在代码里 t() 调用的 key: {len(new)} ==")
    missing, reuse_op = [], []
    for k in sorted(new):
        v = en.get(k)
        if v is None:
            missing.append(k); continue
        cand = val2key.get(v.strip())
        if cand:
            reuse_op.append((k, v, cand))
    print(f"\n[缺 en.json（坏，必补/必查）] {len(missing)}")
    for k in missing: print("  ", k)
    print(f"\n[可复用现成 key（英文与全语言 key 字符级相同）] {len(reuse_op)}")
    for k, v, c in reuse_op:
        print(f"   {k}  \"{v}\"  → {c}")
    print(f"\n[其余=真新建] {len(new)-len(missing)-len(reuse_op)}")


def _loc_dedup(locs, primary):
    out = []
    for s in locs:
        rel, ln = s.rsplit(':', 1)
        out.append(f'L{ln}' if rel == primary else H.escape(s))
    return out


def cmd_html(a):
    data = load_locales(a.i18n_dir); en = data['en']; full = fully_set(data)
    occ = scan_code(a.scope); exclude = load_exclude(a.exclude)
    new, reused = split_keys(occ, a.prefix, exclude)
    reused = {k: v for k, v in reused.items() if k in full}  # 只留 15/15 的真复用
    groups = {}
    for k in new:
        groups.setdefault(new[k][0].rsplit(':', 1)[0], []).append(k)
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    P = [f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>i18n {a.prefix} {ts}</title><style>
body{{font-family:-apple-system,sans-serif;padding:24px;max-width:1400px;margin:0 auto;color:#222;background:#fafafa}}
h1{{font-size:21px}}h2{{font-size:16px;margin:24px 0 8px}}.meta{{color:#666;font-size:13px;margin-bottom:14px}}
.stats{{display:flex;gap:12px;margin-bottom:16px}}.stat{{background:#fff;padding:9px 15px;border-radius:8px;border:1px solid #e5e5e5}}
.stat .n{{font-size:21px;font-weight:bold}}.new .n{{color:#7976ff}}.re .n{{color:#0e9488}}.stat .l{{font-size:12px;color:#666}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid #e5e5e5;border-radius:8px;overflow:hidden;margin-bottom:20px}}
th{{background:#f0f0f0;text-align:left;padding:8px 12px;font-size:12px;border-bottom:1px solid #e5e5e5}}
td{{padding:8px 12px;vertical-align:top;border-bottom:1px solid #f3f3f3;font-size:13px}}
.key code{{background:#f5f5ff;padding:2px 6px;border-radius:4px;color:#4a3aff;font-size:12px;white-space:nowrap}}
.re .key code{{background:#ecfdf5;color:#047857}}.value{{max-width:560px;word-break:break-word}}
.sec{{font-size:13px;margin:14px 0 5px;font-family:monospace;background:#eef;padding:3px 8px;border-radius:4px;display:inline-block}}
.occ{{font-size:11px;color:#777}}</style></head><body>
<h1>i18n 落地清单 — {a.prefix}</h1>
<div class="meta">{ts} · 位置列：同文件标行号 L，跨文件标路径 · 飞书录入自理</div>
<div class="stats"><div class="stat new"><div class="n">{len(new)}</div><div class="l">本次新建（进飞书）</div></div>
<div class="stat re"><div class="n">{len(reused)}</div><div class="l">复用现成（不进飞书，全语言）</div></div></div>
<h2>① 本次新建（{len(new)}，进飞书）</h2>"""]
    for primary in sorted(groups):
        P.append(f'<div class="sec">{H.escape(primary)}</div>')
        P.append('<table><thead><tr><th>Key</th><th>English</th><th>位置</th></tr></thead><tbody>')
        for k in sorted(groups[primary]):
            locs = '<br>'.join(f'<span class="occ">{x}</span>' for x in _loc_dedup(new[k], primary))
            P.append(f'<tr><td class="key"><code>{k}</code></td><td class="value">{H.escape(en.get(k,"⚠️缺en"))}</td><td>{locs}</td></tr>')
        P.append('</tbody></table>')
    P.append(f'<h2>② 本次复用（{len(reused)}，不进飞书）</h2>')
    P.append('<table class="re"><thead><tr><th>复用 key</th><th>English</th><th>用在</th></tr></thead><tbody>')
    for k in sorted(reused):
        locs = '<br>'.join(f'<span class="occ">{H.escape(x)}</span>' for x in reused[k])
        P.append(f'<tr><td class="key"><code>{k}</code></td><td class="value">{H.escape(en.get(k,""))}</td><td>{locs}</td></tr>')
    P.append('</tbody></table></body></html>')
    open(os.path.expanduser(a.out), 'w', encoding='utf-8').write('\n'.join(P))
    print(f"✅ HTML: {a.out} — 新建 {len(new)} / 复用 {len(reused)} / 文件组 {len(groups)}")


def cmd_baseline(a):
    """接代码前拍 en.json 全量基线（所有 key，不分前缀）。接完用 tsv --baseline 做差集。"""
    en = load_locales(a.i18n_dir)['en']
    keys = sorted(en.keys())
    open(os.path.expanduser(a.out), 'w').write('\n'.join(keys) + '\n')
    print(f"✅ baseline: {a.out} — {len(keys)} 个 en key（接代码前存；接完 tsv --baseline 差集出本次新增）")


def cmd_tsv(a):
    data = load_locales(a.i18n_dir); en = data['en']
    if getattr(a, 'baseline', None) and os.path.exists(a.baseline):
        # 推荐：基线差集 → 本次所有新增 key（跨前缀，含 nav_ / 动态拼接落进 en 的）
        base = {x.strip() for x in open(a.baseline) if x.strip()}
        new = {k: None for k in en if k not in base}
        print(f"[基线差集] 本次新增 {len(new)} 个 key（跨前缀）")
    else:
        occ = scan_code(a.scope); exclude = load_exclude(a.exclude)
        new, _ = split_keys(occ, a.prefix, exclude)
        print(f"[前缀扫描] {a.prefix} {len(new)} 个 —— 注意：漏别的前缀/动态 key，优先用 --baseline")
    bad = [k for k in new if '\n' in en.get(k, '')]
    pairs = [(k, en.get(k, '')) for k in sorted(new)]
    txt = '\n'.join(f"{k}\t{v}" for k, v in pairs) + '\n'
    # 默认进剪贴板（HTML 表格，Feishu/Sheets/Excel 都拆格）；要存文件才给 --out
    ok = copy_grid(pairs)
    print(f"✅ 已进剪贴板（{'HTML 表格' if ok else '纯 TSV 回退'}）— {len(pairs)} 行（key|EN，直接粘飞书 A/B 列）")
    if getattr(a, 'out', None):
        open(os.path.expanduser(a.out), 'w', encoding='utf-8').write(txt)
        print(f"（另存文件: {a.out}）")
    if bad:
        print(f"⚠️ 含换行的值（粘贴会串行，注意）: {bad}")


def cmd_reuse(a):
    data = load_locales(a.i18n_dir); en = data['en']; full = fully_set(data)
    val2key = {}
    for k in full:
        val2key.setdefault(en[k].strip(), []).append(k)
    strings = [x.rstrip('\n') for x in open(a.strings_file) if x.strip()]
    print(f"== 复用查询：{len(strings)} 条英文 ==")
    for s in strings:
        cand = val2key.get(s.strip())
        print(f"  \"{s}\"  → {cand if cand else '（无现成 15/15 可复用，需新建）'}")


def cmd_reuse_audit(a):
    """【硬闸·出飞书清单前必跑】扫每个新建 <prefix> key，若其 en 值已有「现成全 15 语言键」字符级相同 → 必须复用、删掉这个新建 key，别进飞书。
    i18n 是扁平字符串去重：同值+全翻译 = 机械复用，前缀/功能归属/"怕耦合"都不是保留理由（key 不是模块）。
    比 reuse 强：自动扫已建 key（不用手攒 strings-file），专抓"建了重复键"这个翻车点。命中即非零退出（当 CI/闸用）。"""
    data = load_locales(a.i18n_dir); en = data['en']; full = fully_set(data)
    exclude = load_exclude(a.exclude)
    val2key = {}
    for k in full:
        if not k.startswith(a.prefix):
            val2key.setdefault(en[k].strip(), []).append(k)
    hits = []
    for k, v in en.items():
        if k.startswith(a.prefix) and k not in exclude and isinstance(v, str):
            cand = val2key.get(v.strip())
            if cand:
                hits.append((k, v, cand))
    print(f"== 复用审计（前缀 {a.prefix}，出飞书清单前硬闸）==")
    if not hits:
        print("✅ 零残留：每个新建 key 的值都没有现成全语言键，放行")
        return
    print(f"❌ {len(hits)} 个 key 的值已有现成全语言键 → 必须复用 + 删掉这些新建 key（别进飞书）：\n")
    for k, v, cand in sorted(hits):
        print(f'  {k}  ="{v}"')
        print(f'       复用成: {", ".join(cand)}（多个选最裸通用的）')
    print("\n铁律：同值+全翻译 = 机械复用。前缀/功能归属（createoc_*、bonus_btn_* 等）、'怕跨功能耦合' 都不是保留理由——key 不是模块，两处显示同一个词不是耦合。")
    print("唯一例外：该值在某语言必须翻成不同的词（语法性别/格、chip 太窄要短译）才保留两个；否则一律复用。")
    sys.exit(1)


def cmd_snapshot(a):
    data = load_locales(a.i18n_dir); en = data['en']; exclude = load_exclude(a.exclude)
    keys = sorted(k for k in en if k.startswith(a.prefix) and k not in exclude)
    open(os.path.expanduser(a.out), 'w').write('\n'.join(keys) + '\n')
    print(f"✅ snapshot: {a.out} — {len(keys)} 个 {a.prefix} key（跑 pnpm i18n 前）")


def cmd_verify(a):
    data = load_locales(a.i18n_dir); en = data['en']
    before = sorted(x.strip() for x in open(a.before) if x.strip())
    now = set(en)
    survived = [k for k in before if k in now]
    lost = [k for k in before if k not in now]
    print(f"== 覆盖后验证（{len(before)} 个 snapshot key）==")
    print(f"✅ 存活（飞书已收录）: {len(survived)}/{len(before)}")
    if lost:
        print(f"❌ 丢失（飞书漏录，需补）: {len(lost)}")
        for k in lost: print("   ", k)
    else:
        print("   无丢失，全部进了飞书 ✅")
    # 翻译覆盖：survived 里有多少在 ja/de 有值
    for l in ['ja', 'de']:
        filled = sum(1 for k in survived if data[l].get(k))
        print(f"  {l} 翻译已填: {filled}/{len(survived)}（空=待翻译）")
    try:
        out = subprocess.run(['git', 'diff', '--numstat', a.i18n_dir],
                             capture_output=True, text=True).stdout.strip()
        print("\ngit diff 概览:")
        for line in out.splitlines():
            p = line.split('\t')
            if len(p) == 3: print(f"  {p[2]}: +{p[0]} -{p[1]}")
    except Exception:
        pass


def cmd_gitdiff(a):
    """【权威源·默认】用 git diff en.json 定增删：+ 行=新增进飞书，- 行=从飞书删。
    跨前缀、跨 t()/labelKey/map/动态拼接，一个不漏。前缀扫描只是辅助参考，别拿来当飞书清单。"""
    en = load_locales(a.i18n_dir)['en']
    d = subprocess.run(['git', 'diff', '--unified=0', os.path.join(a.i18n_dir, 'en.json')],
                       capture_output=True, text=True).stdout
    add, rem = set(), set()
    for line in d.splitlines():
        m = re.match(r'^([+-])\s*"([^"]+)"\s*:', line)
        if m:
            (add if m.group(1) == '+' else rem).add(m.group(2))
    exclude = load_exclude(a.exclude)
    pure_add = sorted(k for k in add if k not in rem and k not in exclude)
    pure_del = sorted(k for k in rem if k not in add and k not in exclude)
    changed = sorted(k for k in add if k in rem)
    print("== git diff en.json（权威增删源）==")
    print(f"  + 新增进飞书: {len(pure_add)}")
    print(f"  - 从飞书删（确认无他处用再删）: {len(pure_del)}")
    for k in pure_del:
        print(f"      - {k}")
    print(f"  ~ 改值（飞书该行更新成新值）: {len(changed)}")
    pairs = [(k, en.get(k, '')) for k in pure_add]
    txt = '\n'.join(f"{k}\t{v}" for k, v in pairs) + '\n'
    if getattr(a, 'out', None):
        open(os.path.expanduser(a.out), 'w', encoding='utf-8').write(txt)
        print(f"  （另存文件 {a.out}）")
    else:
        ok = copy_grid(pairs)
        print(f"  ✅ {len(pairs)} 行新增已进剪贴板（{'HTML 表格' if ok else '纯 TSV 回退'}，直接粘飞书）")


def cmd_dups(a):
    """扫同前缀、同 en 值的 key（同值=按概念重复，该合成 1 个）。接线后、出飞书清单前跑。
    gitdiff 只抓"哪些是新增"，抓不到"两个新 key 英文一样"——这命令补这个盲区。"""
    en = load_locales(a.i18n_dir)['en']
    occ = scan_code(a.scope); exclude = load_exclude(a.exclude)
    by_val = {}
    for k, v in en.items():
        if k.startswith(a.prefix) and k not in exclude and isinstance(v, str):
            by_val.setdefault(v.strip(), []).append(k)
    dups = {v: ks for v, ks in by_val.items() if len(ks) > 1}
    print(f"== 同值 key 扫描（前缀 {a.prefix}）==")
    if not dups:
        print("✅ 无同值 key，无需合并")
        return
    save = sum(len(ks) - 1 for ks in dups.values())
    print(f"⚠️ {len(dups)} 组同值，合并后可省 {save} 个 key\n")
    for v, ks in sorted(dups.items()):
        print(f'值 "{v}":')
        for k in ks:
            locs = occ.get(k, [])
            print(f"   {k}  → {', '.join(locs) if locs else '⚠️ 代码无引用(死键?)'}")
        print()
    print("逐组：留通用名 → repoint 另一处 call site → 删冗余 key（飞书删行 + pnpm i18n 自动清 json）")
    print("例外：英文恰好相同但你预判将来要分歧（语法格/长度）才保留两个，否则一律合。")


def cmd_plan(a):
    """接代码前的审查 HTML。读 plan.tsv: status<TAB>key<TAB>en<TAB>location（status=new 或 reuse:<key>）。"""
    rows = []
    for line in open(a.plan_file, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line.strip():
            continue
        p = line.split('\t')
        if len(p) < 4:
            continue
        rows.append((p[0].strip(), p[1].strip(), p[2], p[3].strip()))
    new = [r for r in rows if r[0] == 'new']
    reuse = [r for r in rows if r[0].startswith('reuse')]
    groups = {}
    for s, k, en, loc in new:
        f = loc.rsplit(':', 1)[0] if ':' in loc else loc
        groups.setdefault(f, []).append((k, en, loc))
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    P = [f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>i18n plan {ts}</title><style>
body{{font-family:-apple-system,sans-serif;padding:24px;max-width:1400px;margin:0 auto;color:#222;background:#fafafa}}
h1{{font-size:21px}}h2{{font-size:16px;margin:22px 0 8px}}.meta{{color:#9a3412;font-size:13px;margin-bottom:14px;font-weight:600}}
.stats{{display:flex;gap:12px;margin-bottom:16px}}.stat{{background:#fff;padding:9px 15px;border-radius:8px;border:1px solid #e5e5e5}}
.stat .n{{font-size:21px;font-weight:bold}}.new .n{{color:#7976ff}}.re .n{{color:#0e9488}}.stat .l{{font-size:12px;color:#666}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid #e5e5e5;border-radius:8px;overflow:hidden;margin-bottom:20px}}
th{{background:#f0f0f0;text-align:left;padding:8px 12px;font-size:12px;border-bottom:1px solid #e5e5e5}}
td{{padding:8px 12px;vertical-align:top;border-bottom:1px solid #f3f3f3;font-size:13px}}
.key code{{background:#f5f5ff;padding:2px 6px;border-radius:4px;color:#4a3aff;font-size:12px;white-space:nowrap}}
.re .key code{{background:#ecfdf5;color:#047857}}.value{{max-width:560px;word-break:break-word}}
.sec{{font-size:13px;margin:14px 0 5px;font-family:monospace;background:#eef;padding:3px 8px;border-radius:4px;display:inline-block}}
.occ{{font-size:11px;color:#777}}</style></head><body>
<h1>i18n 计划（接代码前·待审）</h1>
<div class="meta">⚠️ 这是 plan,代码还没改。审命名/复用/新建,确认后才接 t()。</div>
<div class="stats"><div class="stat new"><div class="n">{len(new)}</div><div class="l">拟新建（进飞书）</div></div>
<div class="stat re"><div class="n">{len(reuse)}</div><div class="l">拟复用（不进飞书）</div></div></div>
<h2>① 拟新建（{len(new)}）</h2>"""]
    for f in sorted(groups):
        P.append(f'<div class="sec">{H.escape(f)}</div>')
        P.append('<table><thead><tr><th>Key</th><th>English</th><th>位置</th></tr></thead><tbody>')
        for k, en, loc in sorted(groups[f]):
            ln = loc.rsplit(':', 1)[1] if ':' in loc else ''
            P.append(f'<tr><td class="key"><code>{H.escape(k)}</code></td><td class="value">{H.escape(en)}</td><td><span class="occ">L{H.escape(ln)}</span></td></tr>')
        P.append('</tbody></table>')
    P.append(f'<h2>② 拟复用（{len(reuse)}，不进飞书）</h2>')
    P.append('<table class="re"><thead><tr><th>本处 key</th><th>English</th><th>复用 →</th><th>位置</th></tr></thead><tbody>')
    for s, k, en, loc in sorted(reuse):
        tgt = s.split(':', 1)[1] if ':' in s else ''
        P.append(f'<tr><td class="key"><code>{H.escape(k)}</code></td><td class="value">{H.escape(en)}</td><td><code>{H.escape(tgt)}</code></td><td><span class="occ">{H.escape(loc)}</span></td></tr>')
    P.append('</tbody></table></body></html>')
    open(os.path.expanduser(a.out), 'w', encoding='utf-8').write('\n'.join(P))
    print(f"✅ plan HTML: {a.out} — 拟新建 {len(new)} / 拟复用 {len(reuse)}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    for name in ('inventory', 'html', 'tsv', 'reuse', 'reuse-audit', 'snapshot', 'verify', 'plan', 'gitdiff', 'dups'):
        s = sub.add_parser(name)
        s.add_argument('--prefix', default='worldcard_')
        s.add_argument('--scope', default='src')
        s.add_argument('--i18n-dir', default='src/i18n', dest='i18n_dir')
        s.add_argument('--exclude', default=None)
        if name == 'gitdiff':
            s.add_argument('--out', default=None)  # 默认进剪贴板；给 --out 才落文件
        if name == 'plan':
            s.add_argument('--plan-file', required=True, dest='plan_file')
            s.add_argument('--out', default=os.path.expanduser('~/Desktop/i18n-plan.html'))
        if name == 'html':
            s.add_argument('--out', default=os.path.expanduser('~/Desktop/i18n-inventory.html'))
        if name == 'tsv':
            s.add_argument('--out', default=os.path.expanduser('~/Desktop/i18n-feishu.tsv'))
            s.add_argument('--copy', action='store_true')
        if name == 'reuse':
            s.add_argument('--strings-file', required=True, dest='strings_file')
        if name in ('snapshot',):
            s.add_argument('--out', default='/tmp/i18n-before.txt')
        if name == 'verify':
            s.add_argument('--before', default='/tmp/i18n-before.txt')
    a = ap.parse_args()
    {'inventory': cmd_inventory, 'html': cmd_html, 'tsv': cmd_tsv,
     'reuse': cmd_reuse, 'reuse-audit': cmd_reuse_audit, 'snapshot': cmd_snapshot,
     'verify': cmd_verify, 'plan': cmd_plan, 'gitdiff': cmd_gitdiff, 'dups': cmd_dups}[a.cmd](a)


if __name__ == '__main__':
    main()
