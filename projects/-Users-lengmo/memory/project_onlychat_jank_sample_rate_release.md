---
name: onlychat-jank-sample-rate-release
description: "搜索动效抽样率 5% 那个 PR（#1274）必须单独走发版，不能跟着常规版本车走"
metadata: 
  node_type: memory
  type: project
  originSessionId: eb2479e1-72ea-468f-9aa2-d1fcc471751c
  modified: 2026-07-27T12:38:57.374Z
---

onlychat 的 `search_transition` 掉帧抽样率 0.1%→5%（为搜索浮层 AB 放量攒样本），
owner 2026-07-27 拍板：**这个 commit 要单独走一次发版**，不跟常规版本车合并发布。

- PR：https://gitea.peekaboo.tech/peekaboo/onlychat/pulls/1274（develop ← `lengmo_20260727_chore_search_jank_sample_rate`）
- commit：`9f94668efe`，4 文件 / +35 -9，核心是 `aggregation.ts` 新增 `SEARCH_TRANSITION_RATE = 0.05`
- 影响事件：`cus.perf_jank_summary` 与 `cus.perf_jank_freeze`，**仅 `scene=search_transition`**；曝光事件 `cus.logic_search_overlay_abtest` 一直全量、没动

**Why**: 抽样率变更会让数仓同一事件里不同 scene 的量级不再可比（差 50 倍），
混在大版本里发，数据同学没法把「量涨了」归因到具体哪次上线。

**How to apply**: 发版时把它单独拎出来；上线后两件跟进事——
① 补「生效时间」发给数据同学（文案已拟，含「按 scene 分开还原量级」的口径警告）；
② 跑一两天去神策数 `scene=search_transition` 实际条数，够用就把 5% 往回调
（`SEARCH_TRANSITION_RATE` 是独立常量，改一行）。AB 定案后按 `CLEANUP:` 注释调回 `RATE`。

相关：[[onlychat-project-context]]、[[feedback-branch-naming]]
