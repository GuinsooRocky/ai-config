---
name: feedback-no-real-model-runs-for-verification
description: 验证改动默认不真跑模型（假模型测试+读代码即可）；只有改动明显改变模型该怎么理解输入且非跑不可时，先说一声等同意再跑
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1ffc514c-783b-4496-9455-814a5d98ec77
  modified: 2026-10-28T12:55:36.947Z
---

验证代码改动时，默认不调用真实模型（本机 Codex / 付费 API）去「看效果」，用模拟应答的测试加读代码即可。

**Why:** 2026-10-28 lich 聊天底稿验收，我连跑三轮真实模型复核，owner 问「一定要跑模型吗 模型本身没什么问题」。第一轮确实抓到了模拟测试抓不到的问题（会话备注≠对方昵称时把对方的话算成用户的），但后两轮只是改完提示词后的保险复跑，owner 认为多余。

**How to apply:** 只有当改动明显改变「模型该怎么理解输入」（提示词语义、输入字段含义），且判断非跑不可时，才先跟 owner 说清楚要跑什么、为什么，等他同意再跑；改完提示词后的确认性复跑不做。与 [[ask-before-paid-api-batch]] 互补：那条管量（>50 次先报费用），这条管要不要跑。
