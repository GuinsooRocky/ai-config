---
name: project-onlychat-search-open-timing
description: onlychat 搜索开场端到端时长线已做完躺在 worktree 待发，收场那条按 owner 拍板挂起等产品需求单
metadata: 
  node_type: memory
  type: project
  originSessionId: 47c7c44a-cba1-4de6-9879-2fb6ae84d968
  modified: 2026-08-13T12:11:37.887Z
---

**2026-08-13 完成、未提 PR、未发版。**

worktree `~/Desktop/cmm/onlychat-search-timing`，分支 `lengmo_20260813_feat_search-transition-timing`（base develop）。

做了什么：搜索转场补 `cus.logic_search_open_timing`——「点首页搜索图标 → 搜索页能用」端到端耗时，老路由组与新动效组各一条，两组同起点同源终点、差值可归因。顺带把搜索 AB 的分组从单布尔补成三档 `experiment_group` + `group_resolved`（照世界卡）。看板必须钉死 `is_mobile=true`，否则 PC 整页跳转会污染对照基线。

**挂起的那条**：收场时长线（返回 → 首页回到眼前）。卡点是老路由组没有干净的终点挂点——搜索入口横跨 dashboard 各页、返回目的地不固定，`HomeCharacterList` 又被个人页/文件夹/搜索结果页复用。owner 2026-08-13 拍板：**先放着，等产品提需求单**。

参照物是世界卡那两条同款线（`worldCardOpenTiming.ts` / `worldCardBackTiming.ts`），开场那条已在 `release-v6.30.0`、收场那条 08-13 才进 develop。相关：[[project_onlychat_jank_sample_rate_release]]、[[project_onlychat]]、[[feedback_no_jargon_plain_product_language]]。
