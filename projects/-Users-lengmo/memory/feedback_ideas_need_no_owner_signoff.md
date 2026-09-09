---
name: feedback-ideas-need-no-owner-signoff
description: 落灵感/低风险文档不许挂「待 owner 确认所指」——按最合理理解写完，理解写在抬头就行
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 51bfa63e-cdb4-40fe-9746-9857881dac46
  modified: 2026-08-28T06:54:31.054Z
---

写灵感稿（soliloquy `docs/prd/ideas/` 这类）时，遇到用户一句话没展开的题目，**按最合理的理解直接写完**，
不要在文档里立「⚠ 这词有两种所指，待 owner 确认，不然本篇作废」这种门，也不要在回复里把它当待拍项抛回去。

**Why:** 2026-08-28 落「公告系统」灵感，我摆了「平台公告 vs 创作者公告」两种所指让他选，被顶：
「你觉得一个灵感要我自己确认什么吗」。灵感本来就是未定形的东西，它的价值在于**把想法接地到仓里的实况**
（现有代码有什么、跟哪条红线撞、坑在哪），不在于口径精确。要确认所指，等它升格成 PRD 再确认也不迟；
在灵感阶段设门，等于用一件不可逆的事的规格去要求一件完全可逆的事。

**How to apply:** 理解写在抬头一行（「按 XX 这层意思写的」）就够了，正文照写不设条件。
真正该停下来问的门槛不变：对外承诺变更、不可逆迁移、花钱——灵感稿一个都不沾。
用户补充所指之后直接重写，别再追问第二轮。

相关：[[feedback_no_pending_verification_lists]]、[[feedback_just_do_no_stop_suggestions]]、
[[feedback_dont_declare_infeasible]]
