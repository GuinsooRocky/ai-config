---
name: feedback_merge_without_owner_clickthrough
description: soliloquy 大批 UI 修复静态闸全绿后直接合 main，owner 不先亲点；别把「等你按清单点完再合」当默认门
metadata:
  type: feedback
---

owner 不想在合并前亲自按清单点一遍。静态闸全绿、独立审查已过的批次，直接 rebase、合进 main，汇报时附上亲点清单的路径就行，不要求他先点。

**Why:** 2026-10-13 soliloquy 全站 UI 逐行修复（PR #17，382 个文件）。我按项目「完成定义要运行时证据」开了 PR 不合，留了「照 §2 亲点后再合」给他，他回「直接合吧，我并没有想看」。

**How to apply:**
- 合并本身照项目提交约定自己做，只把真钱、不可逆迁移、首次曝光这三类留给 owner 拍。
- 亲点清单照样写进交付文档，作为发版前走查的依据，但不拿它当合并门。
- 汇报时如实写「没有运行时证据」，不要包装成已验证。
- 相关：[[feedback_done_needs_runtime_before_saying_so]]、[[feedback_owner_decision_interaction]]。
