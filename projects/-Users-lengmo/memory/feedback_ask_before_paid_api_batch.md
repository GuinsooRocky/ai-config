---
name: ask-before-paid-api-batch
description: 批量烧付费 API（LLM 评分/翻译/生成等一跑几百上千次调用）前先说清要花钱并确认，别默认开跑
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 998263a4-2788-4658-ab2e-253318a62c8a
---

批量消耗付费 API 的操作（如全量 LLM 打分 980 张卡）开跑前要说清"这会烧 OpenRouter/API 额度"，让用户确认。

**Why:** 2026-07-16 优秀度评分全量跑完，用户才说"其实我本意是不想花钱的 但是花了就算了"——事前没意识到这是付费操作。试跑小样本（≤20 次调用）可以直接跑，全量要过一句确认。

**How to apply:** 涉及按量计费的外部 API 且调用量 >50 次时，报预估调用量+说明会产生费用，等用户点头再跑。用户追问成本细节时再查，别主动翻账（[[feedback_owner_decision_interaction]] 的例外：花别人钱的事就是要停下问）。
