---
name: feedback_worldcard_worktree
description: World Card（世界卡）功能开发不碰 onlychat-agg-tuning（那是 pageforge 生码测试床）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4a55234d-eb72-4301-ab04-e3fffee5d842
  modified: 2026-07-30T06:45:17.889Z
---

世界卡功能的改动**绝不动 `~/Desktop/cmm/onlychat-agg-tuning`**——那是 pageforge 生码测试床，里面的世界卡代码是工具产物，不是产品代码。这条是本记忆的不变量。

**在哪做**：接任务时 `git -C ~/Desktop/cmm/onlychat worktree list` 现查，别认历史 worktree 名。
（原写死的 `onlychat-world-book` worktree 已于 2026-07-30 核实不存在，当时的世界卡活在
`onlychat-worldcard-image-encode` 和主仓 `onlychat` 上。）认路径别认分支名；动手前 `lsof`/`ps` 确认 dev server cwd。

**细节与踩坑背景已迁入** `~/Desktop/cmm/onlychat-World-Path/04-本地启动指南.md` §十六（2026-07-06，原举证的分支名/文件路径已过期并按现状改写）。相关：[[project_onlychat]]。
