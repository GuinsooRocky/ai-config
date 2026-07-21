# cmm-pr §8 — PR mergeable 检测 + 解冲突子流程（完整版）

> 从 SKILL.md 拆出的按需加载细节。编号沿用 §8.x，主文件与故障排查里的交叉引用仍然有效。
> 前置上下文：§2 高敏感扫描、§2.2 前置 rebase、$target/$branch/$repo 变量均来自主文件。

### 8. PR mergeable 检测 + 解冲突子流程

PR 创建后**自动查 mergeable**，不是 advisory 而是 actionable。

> ⚠ §2.2 已在 push 前前置 rebase 到 target，所以多数 PR 创建时**本就 mergeable**，本节多数情况一次通过即退出。§8 降级为**兜底**：覆盖前置 rebase 与 PR 创建之间的竞态窗口（target 又被别人推进），以及 §2.2 重冲突时用户选了"退回旧行为"的场景。

#### 8.1. 查 mergeable

```bash
# 优先 tea pr show；不行就直接打 gitea API
pr_num=$(echo "$pr_url" | grep -oE '[0-9]+$')
mergeable=$(tea pr show "$pr_num" --login peekaboo --repo "$repo" --output simple 2>/dev/null \
  | grep -iE '^mergeable' | awk '{print $NF}')

# 或者 tea pr create 的 stdout 已经包含 "Conflicting files" → 直接当 mergeable=false
grep -qi 'conflicting files' /tmp/tea-pr-create.log && mergeable=false
```

`mergeable=false` 或检出 "Conflicting files" 字样 → **先分诊冲突量级，再决定弹不弹菜单**（爆冲档别一律弹，菜单是人工往返，轻冲突直接解更快）：

```bash
# 数真实冲突文件（merge-tree 纯预演，不动工作区）。注意：只用来「计数」决定走哪条，
# 别据此编「N 个语义冲突在打架」的叙事——rebase 实际会跳过已合入 commit，真冲突常更少。
conflict_n=$(git merge-tree --write-tree --name-only "origin/$target" HEAD 2>/dev/null | grep -ic 'CONFLICT')
```

- **轻冲突（`conflict_n` ≤ 2，且都是 import 行 / lockfile / 明显并集）→ 不弹菜单**，打印一行 `🛑 PR #N 与 <target> 有 ${conflict_n} 处冲突（轻），直接 rebase 解` → **直接进 §8.2 当场解 + §8.3 push**，解完在 §8.4 一句话报「解了哪几处」。这是爆冲的默认延续，不为它多要一次人工确认。
- **重冲突（`conflict_n` ≥ 3 / 含 i18n·generated 批量 / 一眼看不出该留谁的语义纠缠）→ 才打印 `🛑` 行 + 弹 `AskUserQuestion`**：
  - header: "解冲突方式"
  - question: "PR 与 target 有 N 处冲突，怎么处理？"
  - options：`"现在 rebase 解 (Recommended)"`（进 §8.2）/ `"改走 merge"`（`git merge origin/<target>` 留 merge commit）/ `"留着回头处理"`（汇报 PR URL 后退出）

> 反面教材（2026-06-01 PR #1158→#1159）：merge-tree 预演报 8 个 CONFLICT，我弹了菜单 + 编了「双实现打架」叙事，实际 rebase 自动跳过 2 个已合入 commit，**真冲突只有 1 文件 1 行 import**。轻冲突该直接解，把 12min 压回 5min。

#### 8.2. rebase 解冲突子流程

```bash
git fetch origin "$target"
# 硬规则：rebase 全程关钩子（-c core.hooksPath=/dev/null）。否则 rebase --continue
# 触发 Husky→lint-staged，在「链接式 worktree」里把陈旧 stash 灌进工作区（凭空冒出
# 别处分支的 atom/测试/WIP），逼出 abort+重跑+诊断，单次坑 ~14min（2026-06-01 PR #1155）。
git -c core.hooksPath=/dev/null rebase "origin/$target" 2>&1 | tee /tmp/rebase.log
```

rebase 完成无冲突 → 跳到 §8.3 push。有冲突 → 逐文件处理：

```bash
conflicts=$(git diff --name-only --diff-filter=U)
for f in $conflicts; do
  # 1. 定位冲突区
  grep -n '<<<<<<<\|=======\|>>>>>>>' "$f"
  # 2. Read 给用户看
done
```

对每个冲突文件，**用人话标注上下侧**（rebase 视角下 `ours/theirs` 跟 merge 是反的，新手 100% 踩）：

```
冲突: src/i18n/en.json
  上半段（HEAD / ours，rebase 下=target 侧）：
    target 分支 feature/lorebook 上别人后加的内容
  下半段（incoming / theirs，rebase 下=你 commit 这侧）：
    你这次 commit 9484cc0c5 想加的内容

[a] 全收 target 侧                          # git checkout --ours <file>（rebase 下）
[b] 全收你 commit 这侧                      # git checkout --theirs <file>（rebase 下）
[c] 我手动 Edit（用 Read+Edit 解，常见做法是两边都要）
```

**关键易踩**：rebase 中 `git checkout --ours` 是接受 **target** 的，不是你写的；`--theirs` 才是你的 commit。skill 用人话呈现，不直接暴露 ours/theirs 让用户死记。

解完一个 → `git add <file>` → 下一个。全部解完：

```bash
GIT_EDITOR=true git -c core.hooksPath=/dev/null rebase --continue   # 关钩子(见 §8.2 顶) + 防 vim 弹窗
```

**rebase --continue 后必须重新跑一遍 §2 高敏感扫描** —— rebase 把整个 commit replay，submodule pointer / lockfile / generated 又会出现在 staged 区。这是踩过的坑（proto sha 漂移在 rebase 后又跳出来）。

#### 8.3. 解完后 push

push 前**必须打印一行明示**，让用户理解为什么这次是强推（本仓用户踩过——看到 Gitea 事件"从 X 强制推送至 Y"会问"为什么要强推"）：

```
↻ rebase 重写了 N 个 commit 的 hash（<old_sha7> → <new_sha7>）
   远端旧 hash 已无效，需 force-with-lease 覆盖
   （lease 会校验：若远端有别人 commit 会被拒，不是裸 --force）
```

`<old_sha7>` = rebase 前 `git rev-parse origin/$branch | cut -c1-7`，`<new_sha7>` = rebase 后 `git rev-parse HEAD | cut -c1-7`；N = `git rev-list --count origin/$branch..HEAD` 之类。打印完直接执行：

```bash
git push --force-with-lease origin "$branch"
```

**硬规则**：rebase 重写历史后 push **必须 `--force-with-lease`，绝不裸 `--force`**。lease 检查失败（远端有别人 commit）→ 停下报：

```
⚠ force-with-lease 拒绝：远端 <branch> 有别人未拉取的 commit
   可能是你另一个 worktree 已经 push 过、或多人共用此分支
   先 git fetch origin <branch> + git log 看看，再决定是否真的 --force
```

不要自动升级到 `--force`。

#### 8.4. 汇报

```
✓ rebase 完成（解了 N 个冲突文件: src/i18n/en.json, ...）
✓ force-with-lease push 成功
✓ PR #1234 已自动重新检测
  <pr_url>
```
