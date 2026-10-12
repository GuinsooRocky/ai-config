---
name: feedback_bug_hunt_means_full_code_scan
description: owner 说「全项目查 bug / 想想有哪些 UI 要优化」= 全量代码逐行扫（覆盖账本 X/N=N）+ 审 origin/main 基线，不是按维度抽样深读 20 个文件、也不是审落后的本地分支
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a213dde5-737d-4efd-bc12-aec0d83f549c
  modified: 2026-09-17T15:13:07.492Z
---

owner 说「整个项目先查一波 bug 然后补 test」，指的是**所有代码逐文件扫**，并且默认包含**组件共用、重复代码、代码优化**。按提交热区 + 产品链路梳理挑出页面问题去修，会被判「没抓全」，「组件共用、代码优化都没做」也会被追问。

**Why:** 2026-10-12 soliloquy UI 审查复发：按「移动/桌面/CSS/a11y/多身份」五个维度派 5 路，每路机械 grep 全量但只深读 20~35 个文件，且 4 路审的是落后 origin/main 122 提交的本地分支，被 owner 一句「你没有到每行前端代码都审 并且 本地更新到最新 要不从新来」打回重做（重做：origin/main detached worktree 当基线，10.9 万行按领域切 13 片、每片一路 opus 逐行读、覆盖表每文件已读行=总行）。更早 2026-09-17 eval-arena 会话，我把「开工三问」第 3 问的「更简单形态」当成缩窄范围的理由，改成先修 P0 页面问题。修了 3 批合进 main 后，owner 连着两句纠正。

**How to apply:**
- 先量源码体量（去掉测试、生成文件、文档），按领域聚合切块：逐文件审约 3 万行一块；**逐行审（UI/交互/CSS 这种每行都可能有问题的）约 1 万行一块**。每块派一个 opus，覆盖账本写到每文件「已读行=总行」。
- 基线先对 origin/main：本地分支落后就 `git worktree add --detach <tmp> origin/main` 审那份，别审旧树（见 [[feedback_check_main_before_product_advice]]）。
- 另加一路专查跨进程接缝：Python、JS、TS 两侧对账，能用脚本实证的就实证。
- 另开质量扫描几路，按区域切：重复 UI 和逻辑、已经分叉的 helper 副本、死代码、巨石拆分方案。按 [[feedback_refactor_risk_tiers]] 分小、中、大三档。
- 顺序：扫描 → 对抗验证 → 修 bug（每处带回归测试）→ 再做重构（避免把重构做在带 bug 的代码上）。
- 「更简单的形态」可以说出来，但不能拿它替 owner 缩范围。
