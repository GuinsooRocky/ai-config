---
name: project-onlychat-shared-component-env-split
description: onlychat 改共用组件要顾两条环境轴 — PC/mobile（z-index/布局）+ dark/light（颜色/背景）
metadata: 
  node_type: memory
  type: project
  originSessionId: 3b3ea1c7-ced1-4474-84aa-d82100f7fb7c
---

改 onlychat 共用组件（带 `.pc`/`.mobile` 兄弟文件或双侧引用的）要同时顾两条正交轴，改完两套都自己点一遍再 ship：
1. **PC vs Mobile**：z-index / sticky / 滚动 / 布局——想"改了会不会顶坏另一侧"
2. **Dark vs Light**：颜色 / 背景 / 边框——用主题 token 或 `dark:` 前缀，别写死 hex

**具体 z-index 数值/组件案例/踩坑实录已迁入** `~/Desktop/cmm/onlychat-World-Path/04-本地启动指南.md` §十五（2026-07-06）。
