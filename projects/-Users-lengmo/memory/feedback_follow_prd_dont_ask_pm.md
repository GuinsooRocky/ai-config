---
name: follow-prd-dont-ask-pm
description: "PRD 写明的照写，别自造\"改进版\"，也别起草消息找 PM；PRD 没要求的文案/数字/按钮行为不顺手改，提 PR 前列多做清单交 owner"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 805a612e-e9d5-4fbf-9c13-2abf44f337dc
  modified: 2026-11-02T08:49:06.523Z
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
- PRD 没要求的改动（提示里的数字、按钮置灰这类）一样不顺手做；确实觉得该改，写进交付说明的「多做清单」交回 owner，由他同步产品、更新 PRD。不写成代码注释（Wei 口径：注释是杂讯，该进个人 checklist）
- 提 PR 前对照 PRD 过一遍 diff，列出「PRD 没写但改了」的条目（onlychat 已接进 cmm-pr §3.5，别的入口提 PR 也要做）。这条记忆没拦住相册「最多 0 张」：提示数字和满 50 张置灰都没同步产品，线上挂了约 6 周才被测出

见 [[feedback_fix_within_reported_scope]]（改动别超边界）、[[project_onlychat]]。
