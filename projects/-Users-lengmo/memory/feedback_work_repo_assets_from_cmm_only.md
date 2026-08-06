---
name: feedback_work_repo_assets_from_cmm_only
description: 工作仓（cmm）要图片/素材只能从 ~/Desktop/cmm 里取，绝不去个人项目或个人归档翻
metadata: 
  node_type: memory
  type: feedback
  originSessionId: de30072a-86a5-43f2-9a0b-3b065db79b31
  modified: 2026-08-05T06:45:25.307Z
---

给 onlychat 等工作仓（`~/Desktop/cmm/**`）造测试素材、fixtures、走查用图时，**素材来源只能是 `~/Desktop/cmm` 目录内**。

绝不去这些地方翻：
- `~/Desktop/loop_project/**`（soliloquy / drama-agent / eval-arena 等个人项目）
- `~/Desktop/archives/**`（个人归档、技术总结、剪藏）
- 其他任何 cmm 以外的个人目录

**Why:** 2026-08-05 世界卡静态图编码走查，我需要"细节多的大照片"当测试图，图省事从 `loop_project/fl/` 和 `archives/` 各拷了一张进工作仓的 `tests/browser/fixtures/`。虽然最后没进提交也没出网，但个人素材混进工作仓的任何环节（哪怕是未追踪的临时文件）都是越界——owner 当场发火（"你为什么要用非 /Users/lengmo/Desktop/cmm 以外的图！！！！"）。

**How to apply:** 工作仓需要素材时，先在 `~/Desktop/cmm` 内找（`相册/` 这类目录是合法来源）；找不到合适的就**自己合成**（当时那两张平涂图/透明 PNG 就是手写 PNG 编码器生成的，完全没问题），或者直接问 owner 要。不要拿"只是临时文件、反正会删"当理由。

相关：[[feedback_agg_readonly]]、[[feedback_project_intel_stays_in_project_docs]]
