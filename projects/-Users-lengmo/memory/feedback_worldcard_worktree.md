---
name: feedback_worldcard_worktree
description: World Card（世界卡）功能开发不碰 onlychat-agg-tuning（那是 pageforge 生码测试床）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4a55234d-eb72-4301-ab04-e3fffee5d842
  modified: 2026-11-02T08:07:39.898Z
---

世界卡功能的改动**绝不动 `~/Desktop/cmm/onlychat-agg-tuning`**——那是 pageforge 生码测试床，里面的世界卡代码是工具产物，不是产品代码。这条是本记忆的不变量。

（worktree 已回收，分支已不存在，现场见 [[project_codegen_workflow]]「世界卡测试跑」。若重建测试床，里面的世界卡代码同样不是产品代码。）

**在哪做**：接任务时 `git -C ~/Desktop/cmm/onlychat worktree list` 现查，别认历史 worktree 名。认路径别认分支名；动手前 `lsof`/`ps` 确认 dev server cwd。

**踩坑背景** 在 `~/Desktop/cmm/onlychat-World-Path/04-本地启动指南.md` §十六。相关：[[project_onlychat]]。
