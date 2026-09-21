---
name: cmm-drift-prd
description: OnlyChat 项目：查代码注释里埋的 §X.X PRD anchor 跟没跟上代码和 PRD（三方比对，只改注释，不动代码/PRD/测试）。触发词：扫一遍注释 anchor、对一下注释和 PRD、查 drift、PRD 改后查注释跟没跟、检测注释 drift、PRD drift、/cmm-drift-prd。不用于：审 PRD 本身的矛盾/缺文案（归 onlychat-prd-reflection）、非 onlychat 项目（agg、mk、kaka 等）。
---

# cmm-drift-prd

## 触发与拒绝

**触发词**：扫一遍注释 anchor / 对一下注释和 PRD / 查 drift / PRD 改后查注释跟没跟 / 检测注释 drift / PRD drift / `/cmm-drift-prd`

> ⚠️ 我查的是**代码注释里埋的 §X.X anchor** 跟代码/PRD 同不同步，不是审 PRD 本身。用户说「扫一遍 PRD / 把 PRD 过一遍 / PRD 有没有矛盾」→ 那是 `onlychat-prd-reflection`，不是我。

**强制先反问确认**，再启 pipeline：

> 准备扫：worktree = `<current>`，PRD = `<resolved>`，base = `<branch>`。继续？

**拒绝触发的情况**：

- 不在 git 仓库 → 拒绝
- worktree 名不含 `onlychat` → 拒绝（如 agg / mk / kaka，提示用户走自己流程）
- 当前在 `main` / `develop` / `release` 等非 feature 分支（无分叉）→ 提示用户切到 feature 分支

## 工作分割

- `onlychat-prd-reflection` = 开工前反讲 PRD 自身缺陷
- `cmm-drift-prd`（本 skill）= 迭代中查代码 anchor 注释的 drift
- 🔴 档（PRD 自身矛盾）顺手扫到 → 建议用户去跑 reflection，不自己处理

---

## 主流程

### Step 0 · Gate + 清理旧报告

```bash
git rev-parse --is-inside-work-tree   # 必须 true
git rev-parse --show-toplevel          # 拿仓库根
git rev-parse --abbrev-ref HEAD        # 拿当前分支名
```

worktree 名（`basename` 的结果）必须包含 `onlychat`，否则拒绝。

**清理旧 HTML 报告（>10 分钟）**：

```bash
find ~/Desktop/cmm/onlychat-World-Path/prd-drift -maxdepth 1 -name '*.html' -mmin +10 -exec mv -f {} ~/.Trash/ \; 2>/dev/null || true
```

- 用 `mv` 不用 `rm`（feedback_cleanup_use_trash_not_rm）
- 只清 HTML 报告；快照（`.git/prd-snapshots/`）NEVER 清
- 10 分钟阈值是为了「跑完留时间给用户看，下次再跑就不留旧版本」
- 失败静默（用户没装目录 / 没旧文件都正常）

### Step 1 · 解析 PRD 来源

按顺序尝试：

1. **读 features.md**：`~/Desktop/cc-memory/onlychat/features.md`
   - 详见 `references/prd-source-resolution.md`
   - 找当前 worktree 对应的 PRD URL + base 分支
2. **兜底问用户**：features.md 没命中 → 当场让用户贴 PRD URL（可多份）+ base 分支
3. **不写回 features.md**：用户约束，cc-memory 由用户自己维护

### Step 2 · Scope 圈定

```bash
python3 ~/.claude/skills/cmm-drift-prd/scripts/scope-discover.py <base_branch>
```

输出 JSON 数组：`[{file, line, anchor, anchor_section, line_content}, ...]`

向用户**第二次确认**：

> Scope：N 个文件 / M 处 anchor / K 个独立 PRD 章节。预计 P 次飞书 get_document 调用。继续？

**报空**：scope 为空（本分支无挂 anchor 的注释）→ 提示用户后退出。

### Step 3 · 拉 PRD ground truth + 快照

对每份 PRD：

1. 用 `mcp__social-proxy-documents__get_document` 拉全文
   - 输入 url 或 token；wiki URL 自动解为底层 docx
   - 大文档默认前 50000 字 + has_more；按 offset 翻页直至覆盖所有 anchor 涉及的章节
2. 按 anchor 双 key（章节号 + 标题文字）抽取对应章节内容
   - 章节号变了但标题稳定 → fuzzy match 找新位置，记 `section_drifted: true`
   - 章节号 + 标题都漂了 → 进 🔴 档
3. 写快照到 `<repo>/.git/prd-snapshots/<doc-token>-<YYYY-MM-DD>.json`
   - 快照旧版本只追加不删
   - 同日重跑：覆盖同日文件即可
4. 与最近一次旧快照（若存在）做 diff
   - 章节内容未变 → 跳过 Step 4 该 anchor 的 B 类判定（无 drift）
   - 章节内容有变 → 喂给 Step 4

### Step 4 · 三类 drift LLM 比对

对每个 `(anchor, 注释块, 代码块, PRD 章节内容)` 元组按 `references/drift-classification.md` 判定。

每条 LLM 输出严格 JSON：

```json
{
  "type": "A" | "B" | "C" | "RED",
  "confidence": 0.0,
  "file": "...",
  "line": 0,
  "anchor": "§3.2",
  "current_comment": "...",
  "current_code_excerpt": "...",
  "prd_content": "...",
  "suggestion": "...",
  "new_comment": "...",
  "code_diff_draft": null
}
```

判定参考表（来自 `references/drift-classification.md`）：

| 注释 vs 代码 | 注释 vs PRD | 代码 vs PRD | 分类 |
|---|---|---|---|
| ✅ | ✅ | ✅ | 无 drift，跳过 |
| ❌ | ✅ | ❌ | C（代码偏离） |
| ❌ | ❌ | ✅ | A（注释抄错） |
| ✅ | ❌ | ❌ | B + C（PRD 升过，代码注释都没跟） |
| ❌ | ❌ | ❌ | 三方各异，优先 🔴（PRD 自身有问题） |

### Step 5 · 分档

| 类 | confidence | 档 | 动作 |
|---|---|---|---|
| B | any | 🟢 | 自动 Edit 改注释 |
| A | ≥ 0.85 | 🟢 | 自动 Edit 改注释 |
| A | < 0.85 | 🟡 | 只标记 |
| C | any | 🟡 | 出 diff 草稿，不动代码 |
| RED | any | 🔴 | 转 onlychat-prd-reflection |

### Step 6 · 执行 + 报告

1. **执行 🟢 档**：每条单独 Edit，old_string 用原行（含原缩进），new_string 仅替换注释文字
   - 失败：单条失败不影响其余，写入报告的"未自动应用"小节
2. **生成 HTML 报告**：
   - 模板：`references/output-template.html`
   - 输出：`~/Desktop/cmm/onlychat-World-Path/prd-drift/YYYY-MM-DD-<branch>.html`
   - 路径不存在自动创建
3. **末尾提示**用户：
   - 报告路径（用户可拖到浏览器打开）
   - 自动改的注释数量（用户应 git diff review）
   - 待决策项数量（🟡 + 🔴）

### Step 7 · 自审

```
/meta-check-skill cmm-drift-prd
```

< 85 分回去改 SKILL.md / references，直到 ≥ 85 才算交付。

---

## 硬约束

- **不动代码**：所有代码改动只产出 diff 草稿，不执行 Edit/Write
- **不动 PRD**：飞书内容只读
- **不动 features.md**：cc-memory 由用户自己维护
- **不动测试**
- **不删快照**：旧快照只追加新版本

## 失败兜底

- **飞书 MCP 失败** → 报错不静默，让用户重试或手动贴 PRD 全文
- **scope 为空** → 提示「本分支无挂 PRD anchor 的注释」并退出
- **LLM 输出非 JSON** → 重试一次；再失败 → 跳过该 anchor，记入"解析失败"列表
- **大量低 confidence**（>50% 在 0.7~0.85）→ 提示 anchor 引用过松，建议补章节号 + 标题双引用
- **base 分支不存在** → 提示用户检查 features.md 或重新贴

## 参考资料（按需加载）

- `references/anchor-grammar.md` — PRD anchor 识别模式与误报防控
- `references/drift-classification.md` — A/B/C 三类判定规则 + few-shot
- `references/prd-source-resolution.md` — features.md 探测格式 + URL 兜底
- `references/output-template.html` — HTML 报告模板（占位符替换）
- `scripts/scope-discover.py` — git diff + grep anchor 脚本

## 与其它 skill 关系

- `onlychat-prd-reflection`：开工前反讲 PRD；本 skill 🔴 档转给它
- `cmm-go` / `cmm-pr`：本 skill 输出的 🟢 档改动会被 cmm-pr 一并提交（用户决定何时提）
- `meta-check-skill`：本 skill 自审用

## 反模式（NEVER 做）

- **NEVER 自动 apply C 类 diff 草稿**：C 类只在报告里出建议，不允许 Edit 代码。即使 LLM 觉得"一行就能改"也不行。
- **NEVER 删除旧 PRD 快照**：旧快照是 B 类比对的依赖；只能追加新版本。
- **NEVER 用裸 `§X.Y` 在非注释行匹配**：必须先过 `is_comment_line` 判定，否则字符串字面量、数学符号、法律条款会大量误报。
- **NEVER 在多 PRD 章节号歧义时直接选第一份**：必须标 `ambiguous: true` 进 🟡 让用户决断，不允许 LLM 替用户挑。
- **NEVER 把 anchor 解析丢给 LLM**：scope-discover.py 是确定性脚本，LLM 只做 drift 比对。anchor 抽取走脚本，可重复可调试。
- **NEVER 替用户做 PRD 自身反讲**：🔴 档只输出转介绍信息，不要在本 skill 里展开评审 PRD 的工作，那是 `onlychat-prd-reflection` 的活。
- **NEVER 自动写回 features.md**：cc-memory 由用户维护，skill 只读不写。
- **NEVER 跳过两次确认**：Step 1（PRD 来源）+ Step 2（scope 规模）必须各自反问用户，不允许直接拉满。

## 已知坑

- **大文档分页**：飞书 `get_document` 默认返前 50000 字 + has_more。anchor 涉及的章节如果在 50000 字之后，必须按 offset 翻页直到覆盖。漏翻 → 假阳性的 🔴（找不到章节误判为 PRD 漂移）。
- **章节号漂移 + 标题改写**：PRD 章节号变了**且**标题文字也大改 → fuzzy match 阈值（0.8）可能 miss。坑在于：注释还指向旧 §3.2 但 PRD 已经把这块拆成 §3.2 / §3.3 两节，单凭一个 anchor 无法对应到两个新章节。这种走 🔴 让用户人工拆。
- **JSX 注释**：`{/* ... */}` 的 `{` 容易被 lint 改格式后破坏匹配。anchor-grammar.md 的 markers 已含 `{/*`，但用户自己重排过格式的代码可能误判为非注释行。
- **快照同日重跑**：同一天多次跑 skill 会覆盖快照。这是 by-design（同日多次拉的 PRD 视为同一基准），但如果中途 PRD 在线编辑了，第二次的快照会"吃掉"中间版本。需要 B 类精确比对时建议手工备份快照。

## 示例输出

终端尾部摘要：

```
扫了 12 个 anchor，覆盖 3 份 PRD（main / config / payment）。
🟢 已自动改注释 5 条（B 类 3 + A 类高置信 2）
🟡 待决策 6 条（A 类低置信 2 + C 类代码偏离 4）
🔴 PRD 自身问题 1 条 → 建议跑 /onlychat-prd-reflection

报告：~/Desktop/cmm/onlychat-World-Path/prd-drift/2026-05-28-lengmo_20260528_feat_xxx.html

自动改的注释（请 git diff 复核）：
  src/foo/bar.ts:42      PRD §3.2 用户名长度 4-20 → 4-32      (A, conf 0.96)
  src/auth/login.ts:88   PRD §4.1 注册流程 → 注册流程（含手机验证）(B, conf 0.91)
  src/auth/login.ts:127  PRD §4.2 token TTL 30min → 60min        (B, conf 0.95)
  src/profile/page.tsx:204  PRD §5.3 头像尺寸 200px → 256px      (A, conf 0.88)
  src/payment/order.ts:55   PRD §6.1 默认币种 USD → JPY          (B, conf 0.93)

🟡 待决策 6 条已写入报告，请打开 HTML 面板查看。
```

HTML 报告结构示意：

```
┌─────────────────────────────────────────────┐
│ PRD Drift Report                            │
│ 分支 feat-xxx · 基于 develop · 2026-05-28  │
│ PRD: docxAAA, docxBBB, docxCCC              │
├──────────┬──────────┬─────────┬─────────────┤
│ 12 anchor│ 🟢 5 改  │ 🟡 6 决 │ 🔴 1 PRD    │
├─────────────────────────────────────────────┤
│ 🟢 已自动改注释                              │
│   ├ [A] src/foo/bar.ts:42 · §3.2 · conf 0.96│
│   │   旧：// PRD §3.2 用户名长度 4-20       │
│   │   新：// PRD §3.2 用户名长度 4-32       │
│   │   PRD 内容：用户名 4-32 字符...         │
│   │   建议：已改为「4-32」                  │
│   └ ...                                     │
├─────────────────────────────────────────────┤
│ 🟡 待决策（不动代码）                        │
│   ├ [C] src/payment/order.ts:88 · §6.2      │
│   │   注释：// 折扣码 5% 起                 │
│   │   代码：const MIN_DISCOUNT = 0.05       │
│   │   PRD：折扣码 8% 起                     │
│   │   diff 草稿：MIN_DISCOUNT = 0.08        │
│   └ ...                                     │
├─────────────────────────────────────────────┤
│ 🔴 PRD 自身问题 → 转 onlychat-prd-reflection│
│   └ [RED] §3.2 vs §3.3 · 注册流程定义打架   │
└─────────────────────────────────────────────┘
```

快照文件（`.git/prd-snapshots/docxAAA-2026-05-28.json`）：

```json
{
  "doc_token": "docxAAA",
  "fetched_at": "2026-05-28T14:30:00+09:00",
  "sections": {
    "3.2": { "title": "用户注册", "content": "用户名 4-32 字符..." },
    "4.1": { "title": "注册流程", "content": "需邮箱 + 手机..." }
  }
}
```
