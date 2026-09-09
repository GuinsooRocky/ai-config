---
name: onlychat-jank-sample-rate-release
description: "onlychat 抽样率类改动的惯例：单独走一次发版、上线后把生效时间发给数据同学、数几天条数再决定回不回调"
metadata: 
  node_type: memory
  type: project
  originSessionId: eb2479e1-72ea-468f-9aa2-d1fcc471751c
  modified: 2026-09-01T00:00:00.000Z
---

**规则（owner 2026-07-27 拍板，此后按此办）**：onlychat 埋点抽样率（`jankMonitor/aggregation.ts` 里那几个 `*_RATE`）的改动——

1. **单独走一次发版**，不跟常规版本车合并发布；
2. 上线后**把「生效时间」发给数据同学**，文案里带上「按 `scene` 分开还原量级」的口径警告；
3. 上线后**跑一两天去神策数该 scene 的实际条数**，够用就把倍率往回调（这些是独立常量，改一行）；A/B 定案后按代码里的 `CLEANUP:` 注释调回基础 `RATE`。

**Why**：抽样率变更会让数仓同一事件里不同 scene 的量级不再可比（能差 50 倍）。混在大版本里发，数据同学没法把「量涨了」归因到具体哪次上线。

**首例已走完**：搜索动效 `search_transition` 0.1%→5%（`9f94668efe`，PR #1274）已进 develop，随后被 `0bde4c6ca0 chore(tracking): 搜索动效 ab 推全量后清理实验侧埋点` 清掉，`SEARCH_TRANSITION_RATE` 现已不存在，两件跟进事随之消化。

**同一套打法正在世界卡上复用**：`src/utils/performance/jankMonitor/aggregation.ts:95-96` 是 `// CLEANUP: 世界卡首页转场 A/B 拍板后回落 RATE。` + `WORLDCARD_TRANSITION_RATE = 1`（2026-09-01 从 5% 提到全量，因为首页世界卡入口 PV 本就低、5% 再砍一刀 A/B 两组都不够判）；施工 worktree `cmm/onlychat-jank-rate`（2026-09-09 核：现 checkout 的是 `lengmo_20260903_chore_worldcard_jank_compare_caveat`，09-01 那条 sample_rate 分支还在但已不是当前施工面）。**全量后世界卡的 freeze 会优先吃掉 `MAX_FREEZE_PER_SESSION` 那 10 条全局额度，其它 scene 的 freeze 条数会被动变少——不是那些场景变好了**，回调时记得这条。

相关：[[onlychat-project-context]]、[[project_onlychat_search_open_timing]]
