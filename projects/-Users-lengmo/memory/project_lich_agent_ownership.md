---
name: lich-agent-ownership
description: 2026-11-02 owner 定调：lich 用 Codex 是暂时的，模型要能换，主要 agent 能力放在 lich 自己；评估 lich 架构时别把 Codex 循环当长期前提
metadata:
  node_type: memory
  type: project
  originSessionId: b687fd18-4c19-41c5-8afa-b89884c7e409
  modified: 2026-11-02T14:30:25.311Z
---

lich（`~/Desktop/my-code/lich`）的助手现在由 Codex 跑循环，这只是暂时形态。owner 2026-11-02 原话：「lich 现在用codex 是暂时的哎 因为可以换模型 我觉得主要的agent能力还是要再lich里搞」。

**Why:** 模型要能换，agent 能力不能绑在某个执行后端上。

**How to apply:** 评估外部文章或方案时，按「lich 自己持有 agent 能力」判断，不要以「Codex 已经做了」为由判不用做。助手 PRD 写的就是「可替换的执行后端」。Codex 现在代管的压缩、续用、缓存、联网和套餐登录，都算迁移时要补的能力。真动工仍等 owner 明说，进度以仓内 roadmap 为准。
