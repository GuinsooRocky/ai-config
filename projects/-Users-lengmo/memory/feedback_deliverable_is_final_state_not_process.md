---
name: feedback-deliverable-is-final-state-not-process
description: 交付物只写最终状态，别把复核过程/自我更正/版本演进写进去
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c2226484-50b2-42d2-b0be-e98a29fe5b2b
  modified: 2026-07-30T13:05:41.193Z
---

交付的文档（HTML 报告、方案、PRD）**只写「现在是什么、该做什么」**。我的复核过程、"上一版我判错了"、"这是第几次同类错误"、逐轮 audit 章节——一律不进正文。

**Why:** 用户原话「我理解 html 应该是最终结果 但是你很喜欢把过程放进去」。过程记录对我有意义（可追溯、显得诚实），但读者要的是拍板依据；混在一起会让 700 字能讲清的卡片胀到 1000+ 字，还把真正要看的警告淹掉。2026-07-30 六类卡顿源报告改到 v3.2 时，决策台 13909 字里堆了三轮复验章节和一堆 `.corr` 撤回段。

**How to apply:**
- 区分两类信息：**「这条结论还没验证 / 照抄会出事故」= 最终状态，留**；**「我先前算错了 37.2KB 其实是 21.6KB」= 过程，删**
- 版本间差异最多留一张紧凑对照表（给看过旧版的人），只写「改成什么」不写「谁错了」
- 过程记录要留就单独落一个文件，别塞进交付物
- 判据：删掉这段，读者做决定会不会做错？不会 → 删

相关：[[feedback_prd_clean_no_process_narrative]]（PRD 同理，拍板结果直接写成正文，拷问实录/翻案痕迹清掉）、[[feedback_writing_taste_umbrella]]
