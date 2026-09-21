---
name: feedback_bug_hunt_means_full_code_scan
description: owner 说「全项目查一波 bug + 补 test」= 全量代码逐文件扫（带覆盖率账本）+ 组件共用/代码优化，不是按热区/产品链路抽样
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a213dde5-737d-4efd-bc12-aec0d83f549c
  modified: 2026-09-17T15:13:07.492Z
---

owner 说「整个项目先查一波 bug 然后补 test」，指的是**所有代码逐文件扫**，并且默认包含**组件共用、重复代码、代码优化**。按提交热区 + 产品链路梳理挑出页面问题去修，会被判「没抓全」，「组件共用、代码优化都没做」也会被追问。

**Why:** 2026-09-17 eval-arena 会话，我把「开工三问」第 3 问的「更简单形态」当成缩窄范围的理由，改成先修 P0 页面问题。修了 3 批合进 main 后，owner 连着两句纠正。

**How to apply:**
- 先量源码体量（去掉测试、生成文件、文档），按约 3 万行切块。每块派一个 opus 逐文件读，覆盖账本必须写到 X/N=N。
- 另加一路专查跨进程接缝：Python、JS、TS 两侧对账，能用脚本实证的就实证。
- 另开质量扫描几路，按区域切：重复 UI 和逻辑、已经分叉的 helper 副本、死代码、巨石拆分方案。按 [[feedback_refactor_risk_tiers]] 分小、中、大三档。
- 顺序：扫描 → 对抗验证 → 修 bug（每处带回归测试）→ 再做重构（避免把重构做在带 bug 的代码上）。
- 「更简单的形态」可以说出来，但不能拿它替 owner 缩范围。
