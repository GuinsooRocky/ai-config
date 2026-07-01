---
name: project-onlychat-shared-component-env-split
description: onlychat 改共用组件要顾两条环境轴 — PC/mobile（z-index/布局）+ dark/light（颜色/背景）
metadata: 
  node_type: memory
  type: project
  originSessionId: 3b3ea1c7-ced1-4474-84aa-d82100f7fb7c
---

onlychat 的共用组件（如世界卡编辑器的 `NotesSearchBar` / `StickyBannerHeader` / `WorldInfoFields` 等）会在多套环境下渲染。改这些组件时要**同时顾两条正交的环境轴**，否则一侧的修法会顶坏另一侧。

## 轴 1：PC vs Mobile（影响 z-index / sticky / 滚动 / 布局）

- **PC**：编辑器在 `<main h-screen overflow-hidden>` 内，顶部 sticky `nav`（z-10），滚动发生在内层 aside/section（`overflow-y-auto`）。内容要盖过 nav → z-20
- **Mobile**：页面是窗口滚动（`min-h-screen`），sticky header + `SiblingSwitcherStrip` 都 z-10，共用横幅须 `z-[5]`（低于它们），否则会盖住 header/strip

**踩坑（2026-05-21）**：给共用组件加全局 `z-20` 修 PC 的"吸顶横幅被 nav 切 1-2px"，结果 mobile 把 Basic Info 横幅顶到切换条上面。修法：
- 共用组件用 `useScreenTypeStore().isMobile` 分流（如 `StickyBannerHeader isMobile ? 'z-[5]' : 'z-20'`）
- 或只在 `.pc` 调用处包 z-wrapper（如 `NotesSearchBar`）

## 轴 2：Dark vs Light（影响 color / background / border / opacity）

- 颜色 / 背景 / 边框 / 半透明叠色在两个主题下表现不同
- 写死的 hex / rgba 在另一个主题下可能丢对比、糊成一片、或边框消失
- 用项目的主题 token（如 `bg-background` / `text-foreground` / `border-border`）而不是裸 hex；或用 Tailwind 的 `dark:` 前缀分流（`bg-white dark:bg-zinc-900`）
- 实测要两个主题都切到看一眼，不能只看一个就 ship

## How to apply

改 onlychat **带 `.pc`/`.mobile` 兄弟文件 / 被两侧都引用**的共用组件时：
1. **z-index / sticky / overflow / 布局** → 想"PC 这套 vs Mobile 这套，改了会不会顶坏另一侧"
2. **颜色 / 背景 / 边框** → 想"dark 模式下还能看吗、对比够吗、边框还在吗"
3. 改完两套都自己点一遍再 ship
