---
name: feedback-commit-desc-user-impact-first
description: onlychat 老板反馈——改动说明先写用户影响，再写实现
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 45ab504c-ae19-4a5c-8b6b-2ccaee3cad07
  modified: 2026-07-29T05:10:32.412Z
---

onlychat 老板（2026-07-29 review 世界卡图片压缩 commit）反馈：「之後的改動，可以產生用戶影響什麼，對結果會清晰的多」。

**Why:** 老板 review 时先看"结果对用户意味着什么"，纯实现描述（算法/线程/参数）看不出改动值不值、影响面多大。

**How to apply:** onlychat 的 commit message / PR 描述 / 给老板的汇报，第一段先写「用户影响」（更快/更小/不再出现某坏结果），实现细节放后面。首例：`50ccf75976`（用户影响 5 条在前，实现在后）。
