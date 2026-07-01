---
name: feedback_cmm_pr_rebase_hooks_off
description: onlychat 提交/rebase 提速铁律：rebase 全程关钩子 + 时间熔断，别磨 14min
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f31d1194-df1f-4339-b936-57ac2c703b79
---

2026-06-01：一次 commit+push+PR 烧了 ~20min，用户明确不接受。复盘后定的硬规则。

**Why（这次的根因）**：分支落后 demo/lorebook 46 commit → 必须 rebase；rebase `--continue` 时 Husky→lint-staged 在**链接式 git worktree** 里把一份陈旧 stash 内容灌进工作区（凭空冒出别处分支的 `noteImageUploadAtom`、一个测不存在 atom 的测试、`world/create/page.tsx` 的 WIP）。我没敢碰共享状态文件，深度取证→abort→重跑，14min 蒸发。

**How to apply**：
- **rebase 全程关钩子**：`git -c core.hooksPath=/dev/null rebase ...` 和 `... rebase --continue`。这是这次坑的根治（已写进 cmm-pr §8.2 + 故障排查）。
- **时间熔断（最高优先级）**：同一段连续 2 次失败、或出现「不在任何 commit、也不是用户改的」幽灵内容 → 立即 abort 回安全态 + 一句话报 + 问用户。**禁止取证上瘾**（status→reflog→逐版本 grep 连环查）：深挖 ≤ 1 次，挖不明白就 abort + 问。
- **push 前本地先 `pnpm exec tsc --noEmit`**，绿了再 push；别靠 pre-push 钩子失败-重试循环。
- **别刷屏烧 token**：大列表 `--stat`/计数，不全量打印；同一份 `git status` 别重复贴；钩子输出 `tail -8`。
- **预检落后量**：`behind_target > 10` 就建议「commit 前先 rebase」，别等 PR 建好才炸。
- 残留 untracked 幽灵文件挪 `~/.Trash`（[[feedback_cleanup_use_trash_not_rm]]），别 rm。

时间预期：普通 commit+push+PR ~3–5min；带必要 rebase ~6–8min；未知意外被熔断压到「几分钟内停下问你」。

相关：[[feedback_worldcard_worktree]]（世界卡只在 onlychat-world-book 做）、[[feedback_git_porcelain_with_rtk]]、[[feedback_rebase_over_merge]]。
