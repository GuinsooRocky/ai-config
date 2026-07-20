---
name: project-codegen-workflow
description: "前端生码工作流：统一叫 pageforge — 旧版(≤v0.0.5,批处理流水线) → 新版(v0.0.6+,中间形态=契约账本机CLM,主线)；含\"100 分\"成功判据。工作名 Loom 已被用户弃用"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3b3ea1c7-ced1-4474-84aa-d82100f7fb7c
---

前端生码工作流统一叫 **pageforge**（工作名 Loom 已弃用 2026-05-29）：旧版 ≤v0.0.5（多 agent 切片流水线，已定性架构选型错）→ 新版 v0.0.6+（契约账本机 CLM，单 agent 串行 + 确定性闸，主线）。

- **权威设计** = `~/Desktop/cmm/agg/V0.0.6/README.md`；测试床 = onlychat-agg-tuning（快照会漂移，正源在 agg/V0.0.6/skills/pageforge）
- **⭐100 分判据**（对新旧版都适用）：① PRD 实现 ② Figma 还原 ③ 接口接通+能跑通 ④ 逻辑与正确实现对照得上；埋点/i18n 不计分；验收=真跑不是自评分
- **铁律**（2026-06-01 用户拍）：tsc 过 ≠ 需求完成；没写 = 真没做；eval 看 logicScore 当头条
- 战报/复盘细节：`agg/V0.0.6/链路水平评估-2026.07.02.md` + `archive/memory迁移-codegen_workflow-2026.07.06.md`（原 79 行 memory 全文落档处）

相关：[[feedback_agg_readonly]] / [[project_pageforge_inspiration_inbox]]
