---
name: feedback_worldcard_worktree
description: World Card（世界卡）功能开发只在 onlychat-world-book worktree 做，不碰 onlychat-agg-tuning
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4a55234d-eb72-4301-ab04-e3fffee5d842
---

World Card / 世界卡功能的所有改动**只在 `~/Desktop/cmm/onlychat-world-book` worktree** 做（分支 `lengmo_20260513_feat_world_book`）。**不要动 `~/Desktop/cmm/onlychat-agg-tuning`** —— 包括不主动回退已有改动。

**Why:** dev server（端口 3000）实际跑在 `onlychat-world-book`（可用 `lsof`/`ps` 查进程 cwd 确认）。`onlychat-agg-tuning` 是另一套分叉的 spike 实现，文件名/结构都不同（如 tag 弹窗：world-book 是 `src/components/Modal/WorldCard/TagsSelectDialog.tsx`，agg-tuning 是 `src/components/WorldCard/WorldInfo/TagsModal.tsx`），改它用户在浏览器里看不到效果。曾因改错 worktree 浪费一整轮。

**How to apply:** 接到 World Card / 创建世界卡 / World Info 类任务，默认落到 `onlychat-world-book`。动手前若不确定，先 `ps`/`lsof` 确认 dev server 的 cwd。相关：[[project_onlychat]]。
