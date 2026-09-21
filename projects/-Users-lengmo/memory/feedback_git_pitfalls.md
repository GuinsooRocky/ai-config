---
name: feedback_git_pitfalls
description: git 三坑：逐路径 add 挡不住 commit、--contains 查不出 cherry-pick、rebase 必须关钩子 + 时间熔断
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fef34f95-7dcd-414f-a190-b108cc5f63ef
  modified: 2026-09-21T07:28:06.873Z
---

# git 三坑

## 逐路径 git add 挡不住 commit——commit 提交的是整个索引

**逐路径 `git add <file>` 只控制"我加了什么"，控制不了"commit 提交什么"**——`git commit` 提交的是**整个索引**。并发会话里，如果别人已经把文件 stage 了（哪怕你一个字节没碰），你的 commit 会把它一起扫进去。

**Why**：多会话并发写同一个仓是本机常态（codex 跑批线、别的 Claude session、迁移 agent 同时在动 soliloquy/eval-arena）。"我只 add 了自己的文件"是安全错觉——2026-08-17 迁移批 6 返修时，一次 commit 就把另一个会话预先 stage 的 `lab-oc-content-snapshot.ts` 扫了进去。

**How to apply**：
- 并发仓里提交前先看 `git diff --cached --name-only`，不是只看自己 add 了什么
- 只想提交自己那几个文件：`git commit -- <path>...`（pathspec 形式，绕过索引其余部分），或先 `git stash push --staged` 挪走别人的
- 扫进去了怎么复原：`git rm --cached <file>` 撤回 + **原样重新 stage**（别人的 status 要完全复位，磁盘零改动）
- 相关：[[feedback_delegate_impl_to_opus_subagent]]（闸别在混着别的会话改动的主目录跑）

## 判「改动在不在某分支」禁用 git branch --contains——cherry-pick 换了 hash

判断「某个改动有没有落到另一条分支」，**不能用 `git branch -r --contains <hash>`**——cherry-pick 会生成新 commit 对象、新 hash，`--contains` 只认对象身份，同内容照样报「不在」。

按内容查：
```bash
git log --oneline --format='%h %ci %an %s' origin/<branch> --grep="<commit message 关键词>"
git log --oneline origin/<branch> -5 -- <改动的文件路径>
diff <(git show A -- f | grep -E '^[+-][^+-]') <(git show B -- f | grep -E '^[+-][^+-]')
```

**Why**：2026-07-17 开 onlychat banner 7/17 期，用 `--contains` 判定叶昶的 HtmlRichText fix「只在 release-v6.27.0、没进 develop」，据此向 owner 报「banner 包会夹带别人未发布的改动」的假警报，差点卡住发布。owner 说「yechang 说 cp 到 develop 了，他这没检查出来啊」——按内容重查坐实：develop 上 `da98b3c35e` 14:28 在前，release 上 `e89b0a073e` 14:30 在后，标准 cherry-pick 顺序。**是我的检查方法有缺陷，不是人说错。**

**How to apply**：cherry-pick 密集的仓（onlychat 三条 release 线每周互相 cp）里，任何「这 commit 在不在 X 分支」的判断一律按内容验。人给的口头事实（「我已经发上线了」「已经 cp 过了」）跟工具结论打架时，先怀疑工具用法——尤其在拿它当理由去阻拦 owner 的时候。同源原则见 [[feedback_not_ground_truth]]（按内容特征校验、别凭状态码下结论）、[[feedback_dont_declare_infeasible]]（别急着替 owner 判死刑）。

## rebase 全程关钩子 + 时间熔断，别磨 14min

> **操作细节已全量落 `~/.claude/skills/cmm-pr/SKILL.md`**：时间熔断在 `:12`「⏱ 时间熔断（硬规则，最高优先级）」，`-c core.hooksPath=/dev/null` 在 `:186`/`:194`/`:456`，同一次 14min 事故的根因与处置在 `references/troubleshooting.md:18` 与 `references/conflict-resolution.md:44`；tsc 按档跑、别刷屏、预检落后量也都在 SKILL.md `:22–24`。**走 cmm-pr 就够，别来这里找口径**——本节只留 why 与非 cmm-pr 场景的速记。

**Why（2026-06-01 的根因）**：一次 commit+push+PR 烧了 ~20min，用户明确不接受。分支落后 46 commit → 必须 rebase；rebase `--continue` 时 Husky→lint-staged 在**链接式 git worktree** 里把一份陈旧 stash 内容灌进工作区（凭空冒出别处分支的 `noteImageUploadAtom`、一个测不存在 atom 的测试、`world/create/page.tsx` 的 WIP）。我没敢碰共享状态文件，深度取证→abort→重跑，14min 蒸发。

**How to apply（速记，任何仓的 rebase 都适用）**：
- **rebase 全程关钩子**：`git -c core.hooksPath=/dev/null rebase ...` 和 `... rebase --continue`。这是那次坑的根治。
- **时间熔断（最高优先级）**：同一段连续 2 次失败、或出现「不在任何 commit、也不是用户改的」幽灵内容 → 立即 abort 回安全态 + 一句话报 + 问用户。**禁止取证上瘾**（status→reflog→逐版本 grep 连环查）：深挖 ≤ 1 次，挖不明白就 abort + 问。
- 残留 untracked 幽灵文件挪 `~/.Trash`（[[feedback_cleanup_use_trash_not_rm]]），别 rm。

时间预期：普通 commit+push+PR ~3–5min；带必要 rebase ~6–8min；未知意外被熔断压到「几分钟内停下问你」。

相关：[[feedback_worldcard_worktree]]（世界卡绝不碰 agg-tuning）、[[reference_rtk_smart_gateway]]、[[feedback_rebase_over_merge]]。
