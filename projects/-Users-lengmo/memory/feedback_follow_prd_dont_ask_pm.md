---
name: follow-prd-dont-ask-pm
description: "PRD 写明的照写就行，别自造\"改进版\"，也别起草消息去找 PM 确认"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 805a612e-e9d5-4fbf-9c13-2abf44f337dc
  modified: 2026-08-18T09:47:46.257Z
---

PRD 已经写死的东西（文案、空态、按钮），照写。不要因为觉得体验不好就落一版自己的，
也不要起草飞书消息去问 PM——提议"发条消息问斯怡"被当场否掉（原话「忘记这个 瞎搞」），
紧接着一句「按照 prd 写的不行吗」。

**Why**：反讲里挑出的体验问题是给 PM 看的，不是给我当改动依据的。PM 看过反讲后没改这条，
就是默认保持。我自造一版 = 既没 PRD 也没设计稿撑着，PR review 必被问；替 owner 去
骚扰 PM 确认小事，更是把我的活推给别人。

**How to apply**：
- 发现 PRD 某条体验上说不通 → 在交付说明里提一句，然后**按 PRD 落**，不要停下来等答复
- 真需要 PM 拍板的，写进「待决策」清单交回 owner，由他决定问不问，不要我起草/代发消息
- 已经自造了才发现有 PRD 依据 → 直接回滚，别再问一遍

见 [[feedback_fix_within_reported_scope]]（改动别超边界）、[[project_onlychat]]。
