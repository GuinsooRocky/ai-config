---
name: feedback_worldcard_worktree
description: World Card（世界卡）功能开发只在 onlychat-world-book worktree 做，不碰 onlychat-agg-tuning
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4a55234d-eb72-4301-ab04-e3fffee5d842
---

世界卡功能的所有改动**只在 `~/Desktop/cmm/onlychat-world-book` worktree 做**；不动 `onlychat-agg-tuning`（pageforge 生码测试床，里面的世界卡代码是工具产物）。认 worktree 路径别认历史分支名；动手前 `lsof`/`ps` 确认 dev server cwd。

**细节与踩坑背景已迁入** `~/Desktop/cmm/onlychat-World-Path/04-本地启动指南.md` §十六（2026-07-06，原举证的分支名/文件路径已过期并按现状改写）。相关：[[project_onlychat]]。
