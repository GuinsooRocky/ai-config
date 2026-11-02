---
name: feedback-reuse-project-before-writing
description: 大功能派工前先盘点项目现成实现（能抄的抄），写进派工书，别等写完才对照
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7f807ba3-20be-4aa6-b2a9-f8783f54877b
  modified: 2026-11-02T12:08:52.595Z
---

大功能开工前，先派一路把「要做的每个组件 → 项目里最接近的现成实现（文件:行号）→ 直接用 / 抽共用 / 不用及理由」盘清楚，结果写进派工规格，再动手。

**Why:** 2026-11-02 创建 Agent 全流程五路并行开写后，owner 提醒「很多都可以抄项目的其他的地方，你也提前分析清楚」。派工书只点了几处复用，几路各写各的，有重复造轮子的风险，只能写完回头补盘点。

**How to apply:** 接缝、文件归属之外，把复用清单也作为派工前置。判定时先看现成组件捆了什么（写死文案、埋点、全局 atom、跳转），不能只看长得像。相关：[[feedback_delegate_impl_to_opus_subagent]]、[[project_onlychat_creation_agent]]
