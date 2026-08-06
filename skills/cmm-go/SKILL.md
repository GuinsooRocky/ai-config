---
name: cmm-go
description: OnlyChat 开工编排——报项目昵称即落到正确 worktree 并出控制面板。触发词：世界卡项目/world-book、next项目/next15、生码项目/agg、onlychat/原项目、开工、上班、继续昨天的活、继续干、/cmm-go。Use when 用户从 home 开 session、只甩一句 onlychat 项目昵称或开工口令时——解析昵称→worktree（读 `~/Desktop/cc-memory/onlychat/features.md`），出控制面板（实时分支/上次进度/watchdog 状态/分支漂移告警/按需资产菜单），管 dev-watchdog 生命周期，按需拉 PRD/Figma/后端文档。不用于：非 onlychat 项目、纯写代码实现任务（直接干）。
---

# cmm-go · OnlyChat 开工编排

用户从 home 开 session，只甩一句项目昵称，本 skill 替他：落对 worktree → 出控制面板 → 管 dev-watchdog → 按需端资产。

核心铁律：**只读稳定指针，动态信息现查；落地前必须先对齐，绝不写错 worktree。**

## 何时使用

- 触发词（口语+书面+英文变体）：`世界卡项目`、`世界卡`、`world-book`、`next 项目`、`next15`、`生码项目`、`agg`、`onlychat`、`原项目`、`开工`、`上班`、`继续昨天的活`、`继续干`、`/cmm-go`
- 典型场景：用户从 `~` 起 `claude`，第一句就报一个 onlychat 项目昵称，想直接落到对应 worktree 接着干。
- 不触发：非 onlychat 的活；已经在 worktree 里、直接让你写代码/修 bug（那就正常干，别硬套面板）。

数据源：`~/Desktop/cc-memory/onlychat/features.md`（手维护映射表）
状态文件：`~/Desktop/cc-memory/onlychat/.last-seen.json`（本 skill 自动读写，记每个 worktree 上次见到的分支，用于漂移检测）

## 主流程（每次触发按序走）

### 1. 解析昵称 → worktree（顺带吃 PRD 范围）
- 读 `features.md`，把用户的话跟各条 `aliases` 模糊匹配。
- 命中 → 拿 worktree 路径，进第 2 步。
- 没命中 → 跑 `git -C ~/Desktop/cmm/onlychat worktree list`，编号列出让用户选。**绝不瞎猜**，必须等用户选定再继续。
- **顺手解析 PRD 范围**：开工口令同句若含 `prd范围 <spec>` / `prd <spec>` / `PRD scope <spec>`，把 `<spec>` 当本 session 的 PRD scope 暂存（覆盖表里默认）。格式与示例见 `references/assets.md` §PRD 范围。比如 "世界卡 prd 3.1 3.4 4.1 8" / "world-book prd范围 all"。没带就静默，等第 4 步真要拉 PRD 时再走默认/兜底问。

### 2. 渲染控制面板
格式与漂移逻辑见 `references/control-panel.md`。

**一把现查**：跑 `bash ~/.claude/skills/cmm-go/cmm-go-probe.sh <worktree>`。
脚本一次输出 `branch / commits / port3000(pid+cwd) / watchdog / drift` 五段，
并在内部把 `.last-seen.json` 更新好（用 python 合并，保留其它 worktree 条目）。
**别再单独跑 4 个 Bash + Write/Edit**——那样会触发 Write 的 read-first 限制并往屏幕上贴一堆细节。

字段取值：
- **worktree**：第 1 步的路径
- **分支**：probe `== branch ==` 段（永远实时，不写进表）
- **需求一句话**：读表
- **上次干到哪**：probe `== commits ==` 段第一行
- **watchdog**：probe `== port3000 ==` + `== watchdog ==` 段，按第 3 步判定
- **漂移告警**：probe `== drift ==` 段。`no` / `new (no prev)` 不展示；`YES (...)` → 标 ⚠ 问"换活了吗"
- **可拉缓存菜单**：读表，有指针标 ●、低档(埋点/i18n)标 ○、坑给 memory 条目名

### 3. dev-watchdog 生命周期
判定见 `references/watchdog.md`。**以 3000 监听进程的 cwd 为准**（动态真相），不以 watchdog 进程启动参数为准（启动时快照、会被手动 kill+起 dev 绕过）。三种情况：
- 3000 没人监听 → **直接起 watchdog**（报昵称=开工信号，别再问"要不要起"）。唯一例外：用户明说"先别起 / 只看不跑 / 收工"就不起
- 3000 cwd = 本 worktree → 标 `● 已运行（本 session 跳过）`，不动它
- 3000 cwd ≠ 本 worktree → ⚠ 提示一行 `3000 实际跑 <X>，不是本项目`，**啥都不动**（见 memory: feedback_watchdog_user_switches_self）。若 watchdog 进程参数跟 3000 cwd 又不一致，再加一行 advisory："dev 挂会被重启回 <watchdog 参数>"

### 4. 按需拉资产
面板出完就停，等用户点菜。用户说"看 PRD / 看设计 / 看后端文档"时，按 `references/assets.md` 现拉。**飞书是真相源，顺指针实时取，不缓存正文。**

PRD 特殊：拉之前先确定**范围**（避免 50000 字塞爆）。解析顺序——
1. 本 session 暂存（第 1 步从口令吃下来的）
2. features.md 这条的 `PRD范围默认:`（非 `<待填>`）
3. 都没有 → 问一次（"PRD 范围？回 all / 章节号空格分隔 / skip"），**用户答完写回 features.md 的 `PRD范围默认:`**
切片算法见 `assets.md` §PRD 范围。

## 反应式：链接落档（细节见 ref）

用户贴 URL 时，**全部满足**才加载 `references/link-archive.md` 走 a/b/c 流程：
- 本 session 已落定活跃项目（主流程第 1 步过了）
- URL 是 `*.feishu.cn/docx/{token}` 或 `figma.com/(file|design)/...`（**无 `?node-id=`**）
- 本 session 还没问过这个 URL

其它形态（`/sheets/` `/base/` `/wiki/`、飞书群 deep link、figma 节点级链接）→ 不主动落，静默。
"参考一下"语境 / 没活跃项目 → 静默。

## 示例输出

```
📍 onlychat · 世界卡项目
────────────────────────────────
worktree   onlychat-world-book                    ✓
分支       lengmo_20260522_feat_world_book_ui
需求       世界卡（World Book）编辑器 UI
上次干到   37954c4 fix: NotesSearchBar z-index
watchdog   ● 已自动启动（首次开工自起）

可拉缓存
  PRD     ○ 表里没指针，现搜飞书
  Figma   ○ 现搜
  后端文档 ●
  ─ 低档，干到那步再拉 ─
  埋点 / i18n / 接口     ○按需
  坑      worldcard_editor_env_split, feedback_worldcard_worktree
```

## 边界
- 只管 onlychat。用户要直接写代码/修 bug，落到 worktree 后交给正常流程。
- **绝不**替用户 commit / push（memory: feedback_commit_policy）；**生码/agg worktree 永远不要提交**（它只读别处代码做总结，自己不产交付）。
- 改这张表/这个 skill 默认只自用。
- 自动停 watchdog（最后一个 session 关掉就自杀）是 **phase 2**（见 `references/watchdog.md` 末尾），v1 先手动停。

## 跨 skill 跳板

- 用户在 onlychat worktree 里说"**提交代码 / 提交 / commit / 提 pr / 开 PR / 一把梭 / 解冲突**"等任一意图 → **直接转 `cmm-pr` skill**，别自己起草 commit msg / 跑 git status。
  本 skill 只负责把人落到正确 worktree + 出控制面板，commit→push→PR→冲突这整条链路是 `cmm-pr` 的职责。
