---
name: feedback-fix-within-reported-scope
description: 改动别超出被要求的边界 — 报的是 A 别把 guard 推广到 B/C；反向也算：新机制在某场景不触发，不等于该去改那个场景的既有决定
metadata:
  node_type: memory
  type: feedback
  originSessionId: ac55a93d-5e97-4c28-bdc8-2879a13bec40
  modified: 2026-08-04T12:24:14.524Z
---

修一个报告的 bug 时，改动范围严格收在"报告里出现过的现象"内。别因为"顺手一起覆盖"把 guard / 拦截 / 兜底推广到报告里没提过的相邻场景。

**Why:** 2026-06-09 onlychat discover+tag：报的 bug 是"GrowthBook 异步 flag resolve 后排序被静默翻成 discover→配 tag 出空列表"。修的时候自作主张把 guard 从这个场景推广到"运行时手动点 tag 也弹回 recent-hits"（加了 slugList 进 effect 依赖）。报告里根本没有"手动点 tag"这一步。结果这条多推广出来的路径，17 天后（2026-06-26）被用户当新 bug 报上来。

**反向同样越界（2026-08-04 世界卡静图编码）：** 出改动方案时发现「要接的新兜底（OC 的 QUALITY_LIST）在弱网停摆那类失败上不会触发」，就把它写成「停摆策略与自动降质冲突、两件事得一起定」。但停摆熔断是 develop 上既有的、修 bug 修出来的决定（`bb81e1a9a3`，防"原图上传失败静默丢原图"），有写明的理由。被顶「这是往外延伸思考了吧，为什么会动刀这里」。而且「冲突」是我造的——断网时自动降质重传一样传不上去、用户需要知道，所以判失败让人手动 Retry；S3 报错才归自动重试。那是分工不是冲突。

**How to apply:**
- 每行改动都要能追溯到报告里出现过的现象；追溯不到 = 越界，删掉或单独拎出来问。
- 新机制在某场景不触发时，默认先问「它本来就不该在那儿触发吗」，别默认是那个场景的既有处理有问题。既有决定带着 commit 理由 = 有人想过，先读理由再谈动它。
- 覆盖面要如实交代（防虚报收益），但「所以该改那边」是另一个需求，不能由本次改动带出来。
- "顺手把 B/C 一起覆盖了"是危险信号不是周到 —— 多覆盖那条路你没验证过，常成下一个 bug。
- 想扩范围时显式拆出来："报告只有 A，我打算同时防 B，要不要？"让用户拍，别静默扩。
- 同源：CLAUDE.md Karpathy "Surgical Changes"；相关 [[feedback_runtime_bug_dont_loop_static]]、[[feedback-comments-not-ground-truth]]、[[feedback-frontend-empty-vs-blank]]
