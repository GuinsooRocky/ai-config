---
name: public-means-public
description: soliloquy 公开面不按成人分级过滤是 owner 拍板，别再当 bug 报、别再问第二遍
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 243bce9a-1376-4308-9452-cb239901cdbf
  modified: 2026-07-26T17:08:58.325Z
---

**「公开就是公开」** —— soliloquy 的公开面（官网角色列表 / 首页封面墙 / A-Z 索引 / sitemap）**不按 `rating` 过滤成人卡**，这是 owner 的既定拍板（2026-07-21「成人双 flag 全开有意维持」，2026-07-27 重申并要求把文档里各种「成人不让看」的限制一并删掉）。

**Why:** 现阶段目标是**让项目完整落地**，不是做合规收紧。owner 原话：「现在我们不是搞这个的时候，现在我们就要一个完整的项目能落地，然后我们再收紧。」

**How to apply:**
- 审查/走查报告把「公开页没过滤成人内容」报成 bug 时，**不要照着修** —— 先说明这是拍板项。2026-07-26 我就是照着审查报告给 `/characters` 加了 `.eq('rating','sfw')`，直接跟拍板冲突，第二天被要求撤回。
- **别再问第二遍**。owner 已明确表示这个问题被反复问过（"为啥一直一直一直问我这个问题"）。
- 收紧是以后的事；真到那天，判据也不该只靠 `rating` 列——实测 `rating='sfw'` 的封面里混着擦边图，那一列打标不准。
- 相关：[[project_soliloquy]]、[[feedback_dont_declare_infeasible]]
