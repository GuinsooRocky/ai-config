---
name: feedback_cmm_pr_rebase_hooks_off
description: onlychat 提交/rebase 提速铁律的 why 与速记：rebase 全程关钩子 + 时间熔断，别磨 14min；操作细节全量在 cmm-pr skill
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f31d1194-df1f-4339-b936-57ac2c703b79
---

> **操作细节已全量落 `~/.claude/skills/cmm-pr/SKILL.md`**：时间熔断在 `:12`「⏱ 时间熔断（硬规则，最高优先级）」，`-c core.hooksPath=/dev/null` 在 `:186`/`:194`/`:456`，同一次 14min 事故的根因与处置在 `references/troubleshooting.md:18` 与 `references/conflict-resolution.md:44`；tsc 按档跑、别刷屏、预检落后量也都在 SKILL.md `:22–24`。**走 cmm-pr 就够，别来这里找口径**——本文件只留 why 与非 cmm-pr 场景的速记。

**Why（2026-06-01 的根因）**：一次 commit+push+PR 烧了 ~20min，用户明确不接受。分支落后 46 commit → 必须 rebase；rebase `--continue` 时 Husky→lint-staged 在**链接式 git worktree** 里把一份陈旧 stash 内容灌进工作区（凭空冒出别处分支的 `noteImageUploadAtom`、一个测不存在 atom 的测试、`world/create/page.tsx` 的 WIP）。我没敢碰共享状态文件，深度取证→abort→重跑，14min 蒸发。

**How to apply（速记，任何仓的 rebase 都适用）**：
- **rebase 全程关钩子**：`git -c core.hooksPath=/dev/null rebase ...` 和 `... rebase --continue`。这是那次坑的根治。
- **时间熔断（最高优先级）**：同一段连续 2 次失败、或出现「不在任何 commit、也不是用户改的」幽灵内容 → 立即 abort 回安全态 + 一句话报 + 问用户。**禁止取证上瘾**（status→reflog→逐版本 grep 连环查）：深挖 ≤ 1 次，挖不明白就 abort + 问。
- 残留 untracked 幽灵文件挪 `~/.Trash`（[[feedback_cleanup_use_trash_not_rm]]），别 rm。

时间预期：普通 commit+push+PR ~3–5min；带必要 rebase ~6–8min；未知意外被熔断压到「几分钟内停下问你」。

相关：[[feedback_worldcard_worktree]]（世界卡绝不碰 agg-tuning）、[[reference_rtk_smart_gateway]]、[[feedback_rebase_over_merge]]。
