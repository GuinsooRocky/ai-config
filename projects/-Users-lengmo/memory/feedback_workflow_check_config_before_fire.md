---
name: workflow-check-config-before-fire
description: 按名发射 workflow 前先看脚本配置块——args 不一定被脚本消费，残留写死配置会整轮跑错
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f8823aa7-2416-4667-8ff6-9cc2748500fb
  modified: 2026-07-29T08:15:58.332Z
---

按名字发射已保存的 workflow（`Workflow({name})`）前，必须先看脚本头部的配置块：很多脚本的目标（仓库路径/scope）写死在常量里、约定由上游 skill 发射前 Edit，`args` 只是给评审员的补充文本，**不会自动覆盖配置**。

**Why:** 2026-07-29 按名发射 pr-audit 审 onlychat PR #1275，脚本残留上次 mk 的写死配置，22 个 agent、139 万 token 全烧在错误仓库上，用户质问"这算你浪费我的 token 吗"。

**How to apply:** 发射前 grep 脚本的 `const` 配置块核对目标；pr-audit 已加 args 保险丝（args 带绝对路径即覆盖，claude-config 57ebe3f），其他 workflow 未必有。相关：[[feedback_inline_over_background_workflow]]
