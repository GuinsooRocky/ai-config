---
name: feedback_check_requirement_owner_before_figma_impl
description: onlychat 里 owner 甩 Figma 链接 + 「Implement this design」时，先确认画板属于哪条需求、开发是不是他；是别人的需求就停，不实现
metadata:
  node_type: memory
  type: feedback
  originSessionId: e6d5e5ee-2c95-454b-a11d-8ef5bf5e1be8
  modified: 2026-10-13T05:07:13.619Z
---

owner 甩 Figma 链接配「Implement this design from Figma / 利用 mcp 检查 UI 新改动」，不等于这块画板就是他的活。

2026-10-13：他甩的是设计师文件里「GIF 标签」整块画板，我查到排期表里这条（6.36.0 付费图片增加 GIF 标签）Web 前端挂的是傅晓杰，却仍打算照做、只在结尾提一句，被纠正「gif 貌似不是我的需求」。他的本意是看这份设计稿里有没有画到他自己那条需求（付费图定价）的新改动。

**Why:** 同一份设计稿会混着好几个人的需求；照着画板实现别人的需求会和对方撞文件、白干一场。

**How to apply:**
- 画板名或 PRD 跟手上的需求对不上时，先查排期表这条需求的开发人员（飞书 bitable「crushonai排期表（新付费版）」，用 social-proxy 的 get_bitable 按需求标题过滤）。
- 开发不是 owner → 不写代码，转成「这份稿里有没有画到 owner 自己需求的部分」去对，并直接报结论。
- 开发是 owner 或排期表查不到 → 照常实现。相关 [[feedback_fix_within_reported_scope]]。
