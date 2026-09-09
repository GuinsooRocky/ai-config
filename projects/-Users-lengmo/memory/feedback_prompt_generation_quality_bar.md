---
name: feedback_prompt_generation_quality_bar
description: 指针——生成 prompt 的 6 条 rubric 已实体化进 write-a-prompt skill「质量线」节，按它逐条过别临场发挥
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7ba438cf-9730-4093-bf85-c4f7900dcd78
---

> **6 条 rubric 已逐字实体化进 `~/.claude/skills/write-a-prompt/SKILL.md`「质量线（6 条，每次逐条过，别临场发挥）」节**——角色+硬规则（违反即失败）/ 焊入真实上下文（实时收，不凭记忆脑补）/ 输出契约 / 内建优先级 P0P1P2 / 可逆护栏 surgical / 参数留 `____` 填空位；「意图四要素（目标 / 谁跑它 / 成功长啥样 / 绝不做什么）缺一先反问」也在该 skill 的 Step 1。**生成 prompt 一律照那份走，别在这里找口径。**

**Why:** 用户经常让我「生成一个 prompt」（回头贴给别的 session 跑），痛点是质量不稳、取决于我当时手上有多少他的上下文。他自己判断这是「习惯」问题不是「工具」问题——所以答案是固定标准，不是更聪明的临场发挥。

**How to apply:** 触发词没命中、skill 没 fire 的场合（用户在别的任务里顺口要一段 prompt），手动把那 6 条过一遍即可。关联 [[feedback_no_jargon_plain_product_language]] [[feedback_skill_design_pattern]]
