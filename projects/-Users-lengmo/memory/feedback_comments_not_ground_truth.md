---
name: feedback-comments-not-ground-truth
description: 代码注释别当 ground truth — 可能过时/误导/章节号抄错；当 hint 用，PRD 引用必须翻原文核对
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e4bfc843-b448-4560-aa50-f9007a67ab34
---

代码注释不是事实，是别人留下的线索。可能过时、可能抄错、可能从一开始就脑补 — 尤其是引用外部章节号 / PRD / Figma 节点 / 别处文件路径的注释。

**Why:** 实际踩过的坑：`EditNotesFrame.mobile.tsx` 注释里写"0 个有效条目时点击进 §8.10.2 二确"，把 PRD 原文翻完整份发现根本没 §8.10.2 这个章节号，是写注释那人脑补出来的。如果信了注释里的章节号，就会跟着复述错误信息给用户，错上加错。

**How to apply:**
- 注释只当 hint（"这里写注释的人当时想表达什么"），不当事实
- 任何"PRD §X.X 怎么说" / "Figma 节点 X:Y 怎么画" / "为什么这样写"必须翻原文核对，不能凭注释下结论
- 写注释断言后端行为（"后端会返回 X / 后端逻辑是 Y"，不只 PRD/Figma）：要么贴核实来源，要么明写"未核实推断"，不能把推断焊成事实（2026-06-09 "后端 discover 叠 tag 返回空集"就是未核实推断写成定论，误导了后续修复）
- 注释看起来"特别详细、特别帮你解释逻辑"时尤其警觉 — 越像解释的注释越可能是脑补
- 写新注释前问自己：3 个月后这段还会准确吗？不准确就别写（参考 [[feedback-no-obvious-comments]]）
