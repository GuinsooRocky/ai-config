---
name: cmm-pr
description: 用 tea CLI 给 onlychat 系列 worktree 做 commit→push→PR 一条龙编排（默认非草稿，要草稿显式说），支持三档：快冲(low) 单次 Enter 一键梭、轻检(med，默认) 跑 code-review、重检(high) 建 PR 先报 URL 后，后台跑 pr-audit 审查(非阻塞)。commit msg 草稿必给用户审一眼，subject 强制全小写避免 commitlint 翻车。同步默认走 rebase，显式说 merge 才用 merge。commit 后 push 前自动把 target 最新代码前置 rebase 过来（干净无感 / 轻冲突当场解 / 重冲突弹菜单），让 PR 创建即 mergeable。submodule / lockfile / generated 等高敏感路径单独分组高亮。PR 建好后仍自动查 mergeable，§8 降级为竞态兜底。触发词：提pr、cmm-pr、/cmm-pr、commit并PR、提交并PR、提交代码、提交、commit、一把梭、快冲pr、轻检pr、重检pr、开 PR、解冲突rebase、rebase到target。不用于：非 onlychat 项目、agg/agg-tuning worktree、main/master/release 分支。
---

# cmm-pr · OnlyChat commit + push + PR 一条龙

把当前 worktree 的改动一气呵成提成 Gitea PR。**commit msg 草稿永远给你审一眼**，**默认走 rebase**，**默认非草稿**（普通 open PR、标题干净；要草稿显式说"草稿提pr"），**快冲档全程只需 1 次 Enter**。

数据源：`~/Desktop/cc-memory/onlychat/features.md`（与 cmm-go 共用；`pr_target` 字段定每个 worktree 的默认 PR 目标分支）。

## ⏱ 时间熔断（硬规则，最高优先级）

正常路径 1–2 次交互、几分钟完事。一旦偏离，**主动熔断、停下问用户，别闷头磨**：

- **慢的真凶是「每轮推理 + 啰嗦输出」延迟，不是 git（2026-06-10 实测：一次爆冲 19min，git 操作全是秒级，时间全耗在工具结果→下一步之间 90~250s 的推理/生成间隙 × ~10 轮）**。三条对策：
  1. **跑前降 effort**：提交是机械流程，高 effort（xhigh）让每轮深度推理 90~250s，是最大时间黑洞。若当前 effort 偏高，**第一句先建议用户 `/effort low` 再提**（一句话提示，不强制）。
  2. **合并工具调用，少绕推理轮**：commit→push（med/high 中间夹一次 tsc）串进**单个 `set -e` 脚本一把跑**，别拆成 5~7 个独立 bash（每个都触发一整轮昂贵推理）。状态扫描也一次抓全（§2），别 scan→重验→diffstat 三步走。⚠ 脚本里 `git push` 这种关键步若被拒，`set -e` 只在它不被管道包裹时才拦得住 —— 见对策 3。
  3. **关键命令退出码一次抓对，绝不塞 `| tail`**：`tsc`（med/high）、`git push`、`git commit` 等都用 `cmd > /tmp/x.log 2>&1; echo "exit=$?"` 抓真实退出码 —— `cmd | tail` 会把退出码换成 `tail` 的 0，`set -e` / PIPESTATUS 全失效，**失败被吞还往下走**（2026-06-18 踩过：`git push … | tail` 把"被拒"吞了，脚本继续把 PR 建到过期分支，多 2 轮恢复 +3min）。面板/解释压到一两行。
- **失败/意外计数 ≥ 2 → 立即停**：同一段（commit/push/rebase）连续 2 次失败，或工作区出现「不在任何 commit、也不是用户改的」幽灵内容 → 恢复到已知安全态（`git rebase --abort` / `git reset` 回上个好 commit），一句话报「卡在哪 + 打算怎么恢复」，等用户拍板。
- **禁止取证上瘾**：状态诡异时走最短恢复路径（abort + 关钩子重跑），不要 status→reflog→逐版本 grep 连环查。深挖 ≤ 1 次，挖不明白就 abort + 问。
- **tsc 按档跑**：med/high push 前本地 `pnpm exec tsc --noEmit` 一次（绿了再 push，别靠 pre-push 钩子失败-重试循环 ~1min/次）；**爆冲(low) 不跑显式全量 tsc**（用户 2026-06-18 拍板）—— pre-commit 的 lint-staged 已对 staged 文件做 tsc-check，且开发期一直在跑 tsc，再来一次全量 ~90s 是重复劳动。代价：low 跳过跨文件全量校验、rebase replay 引入的类型错不拦 —— 爆冲档接受此风险换速度。
- **别刷屏烧 token**：大列表用 `--stat`/计数，不全量打印；同一份 `git status` 别重复贴；commit 钩子输出 `tail -8` 够了，别带 pnpm 进度噪音。
- **预检落后量**：§2 若 `behind_target > 10` → 面板标红，建议「commit 前先 rebase 到 target」，把大 rebase 变成可控前置步，而不是 PR 创建后才炸（§8）。⚠ **落后量 ≠ 冲突量**：behind 大常常只是 target 推进快，真冲突可能就 1 行（rebase 会自动跳过已合入的 commit）；别拿 behind 数去编「N 个语义冲突」的吓人叙事。但 **behind 异常大（>15）在一条本该是 feature 集成分支上 = base 可能配错的信号**，先回 §1 核对 `pr_target` 指对没有（2026-06-01 踩过：features.md 误填 `demo/lorebook` 部署快照，把一次 1 行 import 冲突拖成 12min）。
- **爆冲(low) 时间预算 ≈ 3min**：commit→push→（轻冲突当场 rebase 解）→建 PR 整条**目标 3 分钟内** —— 全是秒级 git + 1 次 AskUserQuestion，**不含全量 tsc**（见上条「tsc 按档跑」，low 去掉 ~90s 地板后预算从 5min 收到 3min）。只有**重冲突**（≥3 文件 / 含 i18n·generated 批量 / 语义纠缠）才允许超时；**轻冲突**（1-2 文件 / import 行 / lockfile / 明显并集）必须当场解完仍压在预算内，别按重冲突的排场跑（菜单+预演+反复确认）。

意义：把「未知意外」的代价从「自动磨 14min」压到「几分钟内停下问你」；正常爆冲（含轻冲突）压在 5min。

## 交互方式硬规则

**选择菜单一律用 `AskUserQuestion` 工具，不要打印 `[Enter] / [m] / [l]` 这种文本伪装菜单。**

- 文本伪菜单的问题：用户得手敲 "Enter"/"m" 回我，多一轮 token，且超 3 个选项就乱
- `AskUserQuestion` 提供真 UI：2-4 个互斥 option + 自动 "Other" 兜底输入
- 仍照常打印的：**信息**类内容（commit msg 草稿、文件分组、面板状态、PR 汇报）。这些是给用户**看**的，不是给用户**选**的

转换映射（贯穿全文）：

| 旧文本菜单 | 新 AskUserQuestion 用法 |
|---|---|
| `[Enter] / [n] 取消` | options 第一个是动作（推荐项标 "(Recommended)"），最后一个是 "取消" |
| `[Enter] / [e] 改 msg / [s] 反选高敏感 / [n]` | 4 个 options：一把梭(R) / 改 commit msg / 反选高敏感 / 取消 |
| `[Enter] / [m] merge / [l] 留着` | 3 个 options：rebase(R) / 改走 merge / 留着回头处理 |
| `[Enter] 接受 / 输入其他分支名:` | 2 个 options：接受默认(R) / 其他分支名（用户走 "Other" 输入自定义） |

如果选项 ≤ 2 且推荐项极强（比如纯 Y/n 确认），可省 AskUserQuestion 直接干，给后悔机制（汇报里说"如要回滚跑 git reset"）。

## 何时使用

- **通用触发词**：`提pr` / `cmm-pr` / `/cmm-pr` / `提单` / `开 PR` / `提个 PR` / `commit并PR` / `提交并PR` / `一把梭`
- **快冲档(low)**：`快冲pr` / `/cmm-pr low` / `快速提pr` / `一键提pr`
- **中档(med)**（默认）：`轻检pr` / `/cmm-pr med` / `检一下提pr`
- **高档(high)**：`重检pr` / `/cmm-pr high` / `深审提pr`
- **不触发**：
  - 用户在 onlychat 主仓 develop / main 分支上（先切 feat 分支）
  - 在 `~/Desktop/cmm/agg` 或 `~/Desktop/cmm/onlychat-agg-tuning`（agg 只读，不产交付，见 memory: feedback_agg_readonly）

## 三档语义速查

| 档 | 关键词 | 流程 | 交互次数 |
|---|---|---|---|
| **快冲(low)** | 快冲pr / 一把梭 / low | 一把抓状态 → 草稿 → **Enter 一键梭**（commit + 同步 + push + PR）| **1 次** |
| **中档(med)**(默认) | 提pr / 轻检pr / med | code-review(low) → 报告 → 草稿 → **Enter 梭剩下** | 2 次 |
| **高档(high)** | 重检pr / 深审pr / high | 同快冲建 PR(先报 URL) → 选审查 → **后台 pr-audit**(不阻塞) | 2 次 |

> 三档**任何一档**走完到 PR 创建后，都会自动跑 §8 mergeable 检测；有冲突弹解冲突菜单（这是 actionable，不是 advisory）。
> 解冲突子流程 §8.2 单独可触发：用户说"rebase 到 target / 解冲突 rebase / 这 PR 有冲突解一下"时直接 Read `references/conflict-resolution.md` 进 §8.2，不必从头跑 §0。

## 主流程

### 0. 前置检查（所有档共用）

按序跑，任何一步失败立即拦下并报原因。**用 `--porcelain` / `rtk proxy git` 拿真相**（memory: feedback_git_porcelain_with_rtk，rtk 摘要会藏文件）。

```bash
# tea 装了 + 登录了
tea login list | grep -q peekaboo || { echo "tea 未登录 peekaboo，先跑 tea login add"; exit 1; }

# 在 git worktree 里
worktree=$(git rev-parse --show-toplevel) || { echo "不在 git repo 里"; exit 1; }

# 不是 agg
case "$worktree" in
  */agg|*/onlychat-agg-tuning) echo "agg 系列不产交付，不提 PR"; exit 1 ;;
esac

# 当前分支符合命名规范
branch=$(git branch --show-current)
echo "$branch" | grep -qE '^lengmo_[0-9]{8}_(feat|fix|refactor|spike|chore|docs)(_[a-z0-9_-]+)?$' \
  || { echo "分支 $branch 不符合 lengmo_YYYYMMDD_<type>[_<slug>] 命名"; exit 1; }

case "$branch" in
  main|master|develop|release/*) echo "禁止从 $branch 提 PR"; exit 1 ;;
esac
```

### 0.5. 解析档位 & 模式

```
1. 触发词含 "快冲" / "一把梭" / "一键" / "low"   → tier=low
2. 触发词含 "重检" / "深审" / "high"             → tier=high
3. 都没匹配                                       → tier=med（默认）
4. 触发词含 "merge"                              → sync_mode=merge；否则 rebase（默认；memory: feedback_rebase_over_merge）
5. 触发词含 "草稿" / "draft" / "wip"              → draft=true；否则 false（**默认非草稿**，普通 open PR，标题无 WIP:）
```

在面板顶部显示：`📍 档位: <tier> ／ 同步: <rebase|merge> ／ 草稿: <yes|no>`，并提示「改档位说『快冲pr/重检pr』；要 merge 加『merge』；非草稿加『非草稿』」。

### 1. 解析 PR target

```
1. 读 features.md，找包含 `worktree: <当前 worktree 路径>` 的 section
2. 在该 section 找 `pr_target: xxx`
3. 找到 → 取该值
   特殊值 `pr_target: none` → 该项目已暂停 PR 流程，直接拦下：
     "📍 <项目名> 标记为 pr_target: none —— 只 push 到自己远端，不提 PR。
      要恢复提 PR，去 features.md 改掉这个字段。"
4. 没找到 → 默认 develop，**必问一次**。先打印信息面板：

      📍 worktree: onlychat-world-book
      features.md 里没找到 pr_target 字段。
      默认建议: develop

   再用 `AskUserQuestion`：
   - header: "PR target"
   - question: "用 develop 作为 PR target 吗？"
   - options: ["用 develop (Recommended)", "其他分支名"]
   - 用户选第 2 项或 "Other" → 走输入自定义分支名

5. 用户答 → patch features.md（在该 section 的 worktree 行下面插入 `- pr_target: <值>`）
6. 校验 target ≠ main/master/release/* —— 是的话再问一次确认
```

patch features.md 示例：用 Edit 一次把 `worktree: <路径>\n- 需求一句话:` 替换成 `worktree: <路径>\n- pr_target: <target>\n- 需求一句话:`。

### 2. 一把抓工作区状态（所有档共用）

**一次性拿全，不再反复 status/diff/log**——上次因为反复探查浪费了 5min。

```bash
dirty=$(git status --porcelain)
git fetch origin "$branch" "$target" 2>/dev/null
behind_branch=$(git rev-list --count "HEAD..origin/$branch" 2>/dev/null || echo 0)
behind_target=$(git rev-list --count "HEAD..origin/$target" 2>/dev/null || echo 0)
ahead_list=$(git log "origin/$branch..HEAD" --pretty=format:'%h %s' 2>/dev/null)
diff_stat=$(git diff --stat HEAD)

# 高敏感路径扫描（submodule / lockfile / generated / proto / package.json / i18n batch）
# 这些不是普通业务文件，要单独高亮让用户专门确认，防 `git add -A` 静默带入
sensitive=$(printf '%s\n' "$dirty" | awk '
  $2 ~ /^proto$/                            {print "submodule  " $0; next}
  $2 ~ /(^|\/)(pnpm-lock\.yaml|package-lock\.json|yarn\.lock|bun\.lock|Cargo\.lock|go\.sum)$/  {print "lockfile   " $0; next}
  $2 ~ /(^|\/)package\.json$/               {print "pkg-json   " $0; next}
  $2 ~ /^src\/generated\//                  {print "generated  " $0; next}
  $2 ~ /^src\/i18n\/.*\.json$/              {print "i18n       " $0; next}
')
i18n_count=$(printf '%s\n' "$sensitive" | grep -c '^i18n')
```

- 落后 `origin/$branch`（user 在别处 commit 了同分支）→ 后续会自动 `git pull --rebase`（或 `git pull` 若 merge 模式）
- 落后 `origin/$target`（PR target 比分支新）→ **commit 后、push 前自动前置 rebase 到 target**（§2.2），把"PR 创建后才发现冲突"提前到 push 前。干净 replay 无感、白捡一个 mergeable PR；冲突按量级分流（轻=当场解 / 重=弹菜单或退回旧行为）
- 高敏感路径命中 → 面板**单独分组**展示（见 §4-low），并在 commit 前**专门弹一次确认**（要带 / 反选不带 / 撤回到 HEAD），尤其 `proto` submodule pointer 漂移最容易被 `git add -A` 静默带入

### 2.1. 文件分组（面板渲染用）

把 `$dirty` 切成三档展示，**别全堆成一个长 list 让用户淹没**：

| 档 | 路径模式 | 处置 |
|---|---|---|
| 🟢 业务 | 其余 | 总数 + 抽样 5 个，` ... (+ N more)` 折叠 |
| 🟡 i18n / 多文件批量 | `src/i18n/*.json` 命中 ≥3 → 视作批量 | 一行汇总：`i18n: 14 国 (+M -N lines)` |
| 🔴 高敏感 | submodule / lockfile / package.json / generated / proto | **逐个列**，附带 `before → after` 信息（lockfile 写依赖名版本，submodule 写 sha 短哈希） |

### 2.2. 前置 rebase 到 target（commit 后 / push 前）

新增核心步骤。目标：把"PR 创建后才发现与 target 冲突"提前到 push 之前，常见情况下白捡一个 mergeable PR，省掉 §8 那套创建后往返。

**仅当 `behind_target > 0` 才跑**；`behind_target == 0`（已坐在 target tip 上）直接跳过、原样 push。

```bash
# 1. 先纯预演数真实冲突量（merge-tree 不动工作区）。计数 ≠ 语义冲突叙事（见 §8.1 反例：别拿 N 编"打架"故事）
conflict_n=$(git merge-tree --write-tree --name-only "origin/$target" HEAD 2>/dev/null | grep -ic 'CONFLICT')

# 2. 关钩子 rebase（硬规则：链接式 worktree 不关钩子会被 Husky 灌陈旧 stash，§8.2 踩过 14min）
git fetch origin "$target"
git -c core.hooksPath=/dev/null rebase "origin/$target" 2>&1 | tee /tmp/rebase.log
rebased_to_target=1
```

按 rebase 结果分流：

- **干净 replay（无冲突，最常见）** → 无感继续。rebase 后**必重扫 §2 高敏感**（commit replay 把 proto/lockfile/generated 重新带回 staged），再 push。
- **轻冲突（`conflict_n` ≤ 2 且都是 import 行 / lockfile / 明显并集）** → 不弹菜单，打印一行 `🛑 与 <target> 有 ${conflict_n} 处轻冲突，直接解` → 进 §8.2 逐文件解（Read `references/conflict-resolution.md`） → 重扫高敏感 → push。这是一键梭的默认延续，不为它多要一次确认。
- **重冲突（`conflict_n` ≥ 3 / 含 i18n·generated 批量 / 一眼看不出留谁的语义纠缠）** → 先 `git -c core.hooksPath=/dev/null rebase --abort` 回到安全态，打印 `🛑` 行，弹 `AskUserQuestion`：
  - header: "重冲突处理"
  - question: "前置 rebase 到 <target> 撞上 N 处重冲突，怎么办？"
  - options:
    - `"现在 rebase 解 (Recommended)"` — 重新跑上面的 rebase，进 §8.2 逐文件解（Read `references/conflict-resolution.md`）
    - `"退回旧行为：先建 PR，留 §8"` — 跳过前置 rebase（`rebased_to_target=0`），直接 push 当前 commit 建 PR，冲突交给 §8 post-PR 流程
    - `"取消"`

**push 规则（关键）**：

```bash
# 前置 rebase 实际 replay 过（rebased_to_target=1）且分支已在远端 → 历史被重写，必须 --force-with-lease
if [ "$rebased_to_target" = 1 ] && git rev-parse --verify --quiet "origin/$branch" >/dev/null; then
  # 先打印 §8.3（references/conflict-resolution.md）的「↻ rebase 重写了 hash」明示，再推
  git push --force-with-lease origin "$branch"
else
  git push -u origin "$branch"   # 首次 push / 没做 target rebase
fi
```

时间预算：干净 replay 几秒；轻冲突当场解仍压在爆冲 5min 内；只有重冲突（用户选"现在解"）才允许超。

### 3. 生成 commit msg 草稿（仅 dirty 时）

工作区**干净**（`dirty` 空）→ 跳过本节，直接走 §5 简化 push 路径。
有 dirty → 按 conventional commit 拼草稿：

- **scope**：从 dirty 文件路径推断主导业务模块（如 `src/screens/WorldCard/...` → `worldcard`）；多模块时留空
- **type**：新增文件占多 → `feat`；纯样式 → `style`；只动测试 → `test`；其余看主导
- **subject**：抓主要变更摘要，≤60 字
- **格式**：`type(scope): subject` 或 `type: subject`
- **强制全小写**（避免 commitlint 拒 PascalCase——上次 `Figma` 翻车浪费 2min）
  - `Figma` → `figma` 或拆 scope `feat(figma-revamp): ...`
  - `NotesSearchBar` → `notes-search-bar` 或 `notessearchbar`，或用 scope `feat(notes-search): z-index`

### 4. 三档分流

#### 4-low. 快冲（low）—— 单次交互

展示一个综合面板，**[Enter] 一键梭到底**。文件按 §2.1 分组渲染，**高敏感单独亮**：

```
📍 worktree: onlychat-world-book
   branch:   lengmo_20260522_feat_world_book_ui → origin/develop
   档位:     快冲(low) / rebase / draft

✏️ 待 commit (40 个文件 / +314 -152)
   🟢 业务 (24)
      M  src/components/WorldCard/Editor.tsx
      M  src/components/NotesSearchBar/index.tsx
      ?? src/components/NotesSearchBar/styles.ts
      ... (+ 21 more)
   🟡 i18n: 14 国 (+14 -3 lines)        # ≥3 个 i18n json 视作批量，折叠成一行
   🔴 高敏感（要专门确认）
      submodule  M  proto                7f3c6ee → a728682（前进 N commits）
      lockfile   M  pnpm-lock.yaml       依赖 X 升 1.2.3 → 1.2.4
      generated  M  src/generated/grpc/world_card_pb.ts
      pkg-json   M  package.json

✏️ commit msg 草稿
   feat(worldcard): notessearchbar z-index + 编辑器布局

📤 push 还会带上已有 commits (2)
   ab12cd3 fix: 旧的 commit 1
   ef45gh6 feat: 旧的 commit 2

↻ 落后 origin/develop 3 commits → push 前自动 rebase 到 develop（干净则无感；冲突按量级分流，见 §2.2）
```

打印完面板，用 `AskUserQuestion`：
- header: "执行确认"
- question: "确认提交并一把梭到 PR 吗？"
- options（动态裁剪）：
  - `"一把梭 (Recommended)"` — commit + pull --rebase + push + PR
  - `"改 commit msg"` — 用户输入新 msg，回到面板
  - `"反选高敏感"` — 仅当 `$sensitive` 非空时显示；选择后高敏感不进 commit，重新展示面板
  - `"取消"`

用户选"一把梭"后顺序执行（任意一步失败立即停下报原因，不继续）：

```bash
# 默认 git add -A；若用户选 [s]，先把高敏感路径 git restore --staged 后再 -A
git add -A
git commit -m "$msg"
[ "$behind_branch" -gt 0 ] && git pull --rebase   # merge 模式: git pull
# 落后 target → 前置 rebase（§2.2：干净无感 / 轻冲突当场解 / 重冲突弹菜单），并决定本次 push 是否 --force-with-lease
# push 命令见 §2.2 末尾（push 规则）；tea flag 探测 + repo/head 默认带见 §7
```

**关键硬规则**：高敏感分组**非空时不要静默 -A**。即使快冲档，也要让用户用眼睛扫一遍那 4-6 行 —— `proto` submodule pointer 偏移最容易这样溜进 commit（本仓踩过，评审追问"为什么这个 PR 顺手升 proto"）。

**全程 1 次交互（高敏感为空时）/ 2 次交互（要反选时）。** 报 PR URL 完事。

#### 4-med. 中档（med，默认）

**先跑 code-review**，再走 4-low 的单次面板。

```
📍 跑 code-review effort=low ...
```

**直接调起** `code-review` skill（effort=low），**不要先去探测它是否注册**。调用失败两种处理：

- skill 不存在 / 调用报错 → 打一行 advisory `⚠ code-review 不可用，自动降级到 low 档`，直接进 §4-low 面板，不卡用户
- skill 跑出来但只是 inconclusive → 当 ✅ 处理

成功跑出报告时三类处理：

- ✅ 无 critical → 直接进 §4-low 的 Enter 面板
- ⚠️ minor 问题 → 列出来 + Enter 面板（用户决定继续 or 修）
- 🛑 P0 bug → 停下报告，建议「修完再来」，**不进 commit**（避免把 bug 钉进 git history）

通过后流程同 §4-low。**共 2 次交互**：审 review + Enter 一键梭。

> **反模式**：不要在面板上写"中档默认要跑 code-review，建议跳过直接走快冲档"让用户拍板降级 —— 这把 skill 的决策成本转嫁给用户。本 skill 的设计就是档位选好之后自动跑通。降级是 skill 的内部 fallback，不是用户的待选项。

#### 4-high. 重检（high）—— 非阻塞后台审查

PR **照常一气呵成建好并先报 URL**，再后台 fire pr-audit 审查，全程不阻塞（**流程优先**：用户会自己合，少量 P0 用 fix commit 补，不挡 push）。

```
1. 同 §4-low 完成：commit → 前置 rebase(§2.2) → push → §6/§7 建 PR。
   **立即按 §7 汇报 PR URL**（不等审查）。

2. PR 建好后，用 AskUserQuestion 问后台跑哪些审查（交互在 skill 里做，workflow 不能中途问）：
   - header: "后台审查"
   - question: "PR 已建好（URL 上方）。后台跑哪些审查？不阻塞，报告回来再看。"
   - options:
     - "代码评审 (Recommended)"   — RUN_CR=true RUN_WQA=false
     - "代码评审 + 质量体检"       — RUN_CR=true RUN_WQA=true（质量体检只对网页代码有意义；非 web 项目别选）
     - "都不跑"                   — 直接结束

3. 选了要审 → 后台 fire pr-audit：
   a. Edit ~/.claude/workflows/pr-audit.js 顶部配置：
      REPO='<worktree>'  SCOPE='<target>'  RUN_CR=true  RUN_WQA=<按上面选择>（质量体检仅 web 项目开）
   b. 用 Workflow 工具 run_in_background 跑 ~/.claude/workflows/pr-audit.js
   c. 一行汇报：🔍 pr-audit 后台审查中，报告回来再看；要改补个 fix commit（不必重跑）

4. 本次结束（PR URL 第 1 步已给）。
```

**共 2 次交互**：草稿审 + 审查选择。

### 5. 简化 push 路径（工作区开头就干净）

`dirty` 空、纯粹想把已有 commits 提 PR → 跳过 commit 流程，沿用旧版逻辑：

```
要 push 的 commits:
  ab12cd3 fix: NotesSearchBar z-index
  ef45gh6 feat: 加 worldCard 编辑器

push 到 origin/<branch>？[Y/n]
```

用户 Y → `git push -u origin "$branch"` → 直接进 §6。用户 N → 停。

### 6. PR title / body

```bash
title=$(git log -1 --pretty=format:'%s')                     # HEAD commit subject
body=$(git log "origin/$target..HEAD" --pretty=format:'- %s') # 本分支相对 target 的全部 commits
```

- 快冲档/中档：PR title = 上面审过的 commit msg，不再单独问
- 高档：同快冲/中档，title = 审过的 commit msg（重检的 pr-audit 审查在 PR 建好后才后台跑，不参与 title）

#### 6.1. 自动 Notes 段（评审"扫读 vs 细审"分流）

扫 `origin/$target..HEAD` 的 diff 文件特征，命中即在 `body` 末尾追加 `### Notes` 段，让评审一眼分清哪些是机生 / 哪些值得细审：

```bash
notes=""
# submodule
if git diff --diff-filter=M "origin/$target..HEAD" --name-only | grep -qE '^proto$'; then
  before=$(git ls-tree "origin/$target" proto | awk '{print substr($3,1,7)}')
  after=$(git ls-tree HEAD proto | awk '{print substr($3,1,7)}')
  notes="${notes}- proto submodule 升级 ${before} → ${after}（业务接口同步，generated/ 跟随重生成，无手写）\n"
fi
# i18n 批量
i18n_files=$(git diff "origin/$target..HEAD" --name-only | grep -c '^src/i18n/.*\.json$')
if [ "$i18n_files" -ge 3 ]; then
  added=$(git diff "origin/$target..HEAD" -- src/i18n/en.json | grep -cE '^\+\s+"[^"]+":')
  changed=$(git diff "origin/$target..HEAD" -- src/i18n/en.json | grep -cE '^-\s+"[^"]+":')
  notes="${notes}- i18n：新增 ~${added} key / 改 ~${changed} key，其余 ${i18n_files}-1 国 placeholder 待 localizely 回译\n"
fi
# lockfile
if git diff "origin/$target..HEAD" --name-only | grep -qE '(pnpm-lock|yarn\.lock|package-lock|Cargo\.lock|go\.sum|bun\.lock)'; then
  notes="${notes}- lockfile：依赖变更，PR 评审主要看 package.json，lockfile 改动属机生\n"
fi
# generated
if git diff "origin/$target..HEAD" --name-only | grep -qE '^src/generated/'; then
  notes="${notes}- generated/：跟随 proto 重生成，无手写代码\n"
fi
[ -n "$notes" ] && body="${body}\n\n### Notes\n${notes}"
```

理由：本仓踩过 —— 40 文件 PR 评审看到 14 国 i18n + proto submodule 不附说明，往往会反问"为什么动这么多"。Notes 段提前回答。

### 7. tea pr create

**别按"备忘"硬拼命令** —— tea CLI flag 在不同版本会漂（如 `--head`）。运行时探测。**注意 `--draft` 不是版本漂移、是 Gitea 根本没有这个 flag** —— 草稿走标题 `WIP:` 前缀（见下）：

```bash
# 只探测 --head（会因版本漂移）；--draft 不探测——Gitea 没这 flag（见下方草稿处理）
tea_help=$(tea pr create --help 2>&1)
echo "$tea_help" | grep -qE '(^|\s)--head(\s|$)' && supports_head=1 || supports_head=0

# 草稿 = 标题带 WIP 前缀（Gitea 原生机制，与 tea 版本无关，永久解）。
# Gitea 把标题以 "WIP:" 开头的 PR 自动标记 draft + 禁止 merge；网页 "Convert to draft"
# 按钮干的就是加/去这个前缀。peekaboo 实例用默认前缀 "WIP:"（2026-06-30 PATCH title 验证 → draft:true）。
# 转正式：去掉标题 WIP: 前缀（网页点 "Start review"，或改标题走 API；tea 无 pr edit 子命令）。
[ "$draft" = "true" ] && title="WIP: $title"

# 从 origin remote 解析 owner/repo（兼容 SSH + HTTPS）
# SSH:  git@gitea.peekaboo.tech:peekaboo/onlychat.git
# HTTPS: https://gitea.peekaboo.tech/peekaboo/onlychat.git
repo=$(git config remote.origin.url | sed -E 's|.*[:/]([^/:]+/[^/.]+)(\.git)?$|\1|')

cmd=(tea pr create
  --login peekaboo
  --repo "$repo"
  --base "$target"
  --title "$title"
  --description "$body"
)
[ "$supports_head" = 1 ] && cmd+=(--head "$branch")

"${cmd[@]}" 2>&1 | tee /tmp/tea-pr-create.log
pr_url=$(grep -oE 'https://gitea\.peekaboo\.tech/[^[:space:]]+/pulls/[0-9]+' /tmp/tea-pr-create.log | head -1)

# URL 拷贝到剪贴板（终端不可点 cmd+click 时的兜底）
[ -n "$pr_url" ] && printf '%s' "$pr_url" | pbcopy
```

**硬规则**：
- 默认带 `--repo`（SSH remote tea 解析不出 owner/repo，本仓踩过 `path segment [0] is empty`）
- 默认带 `--head`（若该版本支持），不依赖"head 自动取当前分支"行为
- `--description` 不是 `--body`
- **草稿用标题 `WIP:` 前缀实现，别找 `--draft` flag**（Gitea 没有）。`$draft=true` 时 `title="WIP: $title"`，PR 建出来**即原生 draft**，不需要事后手动 Convert。要转正式：去掉标题 `WIP:` 前缀

成功 → 报（含 mergeable 状态，见 §8）：

```
✓ PR 已开（draft=true → 标题带 WIP: 前缀=草稿；draft=false 则普通 open）
  https://gitea.peekaboo.tech/peekaboo/onlychat/pulls/1234
  📋 URL 已复制到剪贴板（终端不可点时用 cmd+v）
  base: feature/lorebook  ←  head: lengmo_20260522_feat_world_book_ui
  commits: N      档位: low/med/high
  mergeable: <见 §8>
```

**URL 渲染规则**：单独成行、不要套进 markdown code block 反引号（部分终端 hyperlink 不识别），让 iTerm/Warp 等可以 cmd+click 直接打开。同时 `pbcopy` 兜底，应对不支持的终端。

### 8. PR mergeable 检测 + 解冲突子流程（细节按需加载）

PR 创建后**自动查 mergeable**。§2.2 已在 push 前前置 rebase，本节多数情况一次通过即退出，只兜「前置 rebase 与 PR 创建之间的竞态」和「§2.2 重冲突用户选退回」两种场景。

- mergeable=true → 直接汇报 PR URL，本节结束
- mergeable=false / stdout 出现 "Conflicting files" → **Read `references/conflict-resolution.md`，按其中 §8.1-8.4 执行**。速记硬规则（细节以该文件为准）：
  - 轻冲突（≤2 处、import/lockfile 类）不弹菜单直接解；重冲突才弹 AskUserQuestion
  - rebase 全程 `-c core.hooksPath=/dev/null`（Husky 灌陈旧 stash 的 14min 坑）
  - rebase 重写历史后 push 一律 `--force-with-lease`，绝不裸 `--force`
  - `rebase --continue` 后必须重跑 §2 高敏感扫描（submodule/lockfile 会再次冒出）

## 同步策略

- **默认 rebase**（memory: feedback_rebase_over_merge）：落后自己远端时 `git pull --rebase`
- 用户触发词含 `merge` → `git pull`（生成 merge commit），仅当用户显式声明
- 落后 `origin/$target` → **commit 后、push 前自动前置 rebase 到 target**（§2.2）；§8 降级为兜底（前置 rebase 与 PR 创建间的竞态窗口，或 §2.2 重冲突时用户选择退回旧行为）
- **rebase 重写历史后 push 一律 `--force-with-lease`**，绝不裸 `--force`（见 references/conflict-resolution.md §8.3）

## 边界

- commit msg 草稿**永远给用户审一眼**（[Enter] / [e] / [n]），不静默 commit
  - 快冲档：审 msg 的同一个面板也包含 push 确认，[Enter] 一键
  - 中/高档：分两/三次确认
- agg / agg-tuning 永远不提（memory: feedback_agg_readonly）
- **默认非草稿**（普通 open PR，标题无 WIP:，可直接合）；要草稿显式加 `草稿` / `draft` / `wip`（Gitea 草稿 = 标题 `WIP:` 前缀）
- target 默认 develop；features.md 显式 `pr_target` 优先；`pr_target: none` 直接拦下
- 改这个 skill 默认只自用（memory: feedback_skill_personal_only）

## 故障排查（细节按需加载）

遇到任何报错/异常 → **Read `references/troubleshooting.md`**（12 条：tea CLI flag 漂移 / 401 / commitlint 拒 subject / rebase 幽灵内容 / force-with-lease 拒绝 / staged 区复现高敏感路径等）。

## Codex compatibility

Preserve this workflow's intent and evidence rules. Translate Claude-specific tool names to the available Codex tools.
