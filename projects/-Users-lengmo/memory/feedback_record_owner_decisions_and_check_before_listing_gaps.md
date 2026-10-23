---
name: feedback-record-owner-decisions-and-check-before-listing-gaps
description: owner 在对话里拍的板当场写进项目决策账；列「薄弱处/待办/建议」前先查决策账+近期会话，别把已拍板的事当缺口重提
metadata:
  node_type: memory
  type: feedback
  originSessionId: d762bb0d-bae0-4a38-9dbe-35f72a58e5d9
  modified: 2026-10-23T08:19:43.202Z
---

10-23 perf-lab：owner 在一个会话里说过「最多存 7 份（本轮+比较用的 6 轮），不要 S3」，当时只落了「不要 S3」进决策账，「7 份」没记、清理逻辑也没改。下一个会话的汇报把「历史只留得住几轮、补法是另存中位数」当成技术薄弱处重新提，被 owner 顶回：「记在哪里了 docs里吗…这个我都说了怎么做 说了好几次」。

**Why:** owner 的拍板只活在聊天里，换个会话就丢，结果同一件事被反复当缺口提，等于让 owner 重复决策。

**How to apply:**
1. owner 在对话里定了口径/做法，当场追加进项目的决策账（perf-lab 是 docs/decisions.md），连同「实现是否已跟上」一句；不只改代码不记账，也不只记一半。
2. 汇报里列薄弱处、待办、建议之前，先 grep 决策账，再按 [[feedback-read-past-sessions-before-asking]] 搜近期会话里 owner 的原话；已定的只报「定了但实现没跟上」，不重新出方案。
3. 汇报方向时拿项目目标句逐条对：目标外的（更真实的设备条件、交互场景、函数级归因这类）明说「超出目标」，不混进待办。相关：[[feedback-think-before-escalating-gaps]]。
