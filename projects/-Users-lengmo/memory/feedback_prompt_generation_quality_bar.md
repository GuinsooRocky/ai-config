---
name: feedback_prompt_generation_quality_bar
description: 用户常让我生成 prompt，要成品质量稳定高——按固定 rubric 写别临场发挥
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7ba438cf-9730-4093-bf85-c4f7900dcd78
---

用户经常让我「生成一个 prompt」（回头贴给别的 session 跑）。痛点：质量不稳，取决于我当时手上有多少他的上下文。定一套固定标准，每次生成 prompt 都过一遍。

**Why:** prompt 质量不该靠运气/当时上下文，靠可复用的标准才稳。用户自己判断这是「习惯」问题不是「工具」问题。

**How to apply:** 生成任何 prompt 时逐条过：
1. 开头给角色 + 硬规则，写成「违反即失败」的失败条件，不是软建议
2. **焊进他的真实上下文/踩过的坑**——主动去 memory 捞（对称操作持久化不对称、项目情报不进全局、lockfile 为准、别用黑话、surgical/只读…）。这是「通用 prompt」和「懂他世界的 prompt」的最大差距，也是他能感知的质量主因
3. 明确输出契约：写到哪、什么结构、「对话里只回什么」、锚 `file:行号`
4. 内建优先级：P0/P1/P2，按收益×成本排，标出「哪些不值得做」
5. 可逆护栏：默认只读/先 diff，匹配他 surgical 习惯
6. 参数留 `____` 填空位，别替他猜项目/目标

意图欠缺时（缺这 4 要素之一：目标 / 谁跑它 / 成功长啥样 / 绝不做什么）先反问一句再写，别硬编。

关联 [[feedback_no_jargon_plain_product_language]] [[feedback_skill_design_pattern]]
