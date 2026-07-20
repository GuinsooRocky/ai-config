---
name: feedback-fix-within-reported-scope
description: 修 bug 别超出报告的场景边界 — 报的是 A 别顺手把 guard/拦截/兜底推广到 B/C；多覆盖的那条路常是下一个 bug
metadata:
  node_type: memory
  type: feedback
  originSessionId: ac55a93d-5e97-4c28-bdc8-2879a13bec40
---

修一个报告的 bug 时，改动范围严格收在"报告里出现过的现象"内。别因为"顺手一起覆盖"把 guard / 拦截 / 兜底推广到报告里没提过的相邻场景。

**Why:** 2026-06-09 onlychat discover+tag：报的 bug 是"GrowthBook 异步 flag resolve 后排序被静默翻成 discover→配 tag 出空列表"。修的时候自作主张把 guard 从这个场景推广到"运行时手动点 tag 也弹回 recent-hits"（加了 slugList 进 effect 依赖）。报告里根本没有"手动点 tag"这一步。结果这条多推广出来的路径，17 天后（2026-06-26）被用户当新 bug 报上来。

**How to apply:**
- 每行改动都要能追溯到报告里出现过的现象；追溯不到 = 越界，删掉或单独拎出来问。
- "顺手把 B/C 一起覆盖了"是危险信号不是周到 —— 多覆盖那条路你没验证过，常成下一个 bug。
- 想扩范围时显式拆出来："报告只有 A，我打算同时防 B，要不要？"让用户拍，别静默扩。
- 同源：CLAUDE.md Karpathy "Surgical Changes"；相关 [[feedback_runtime_bug_dont_loop_static]]、[[feedback-comments-not-ground-truth]]、[[feedback-frontend-empty-vs-blank]]
