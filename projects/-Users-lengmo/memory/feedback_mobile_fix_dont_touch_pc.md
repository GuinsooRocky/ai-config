---
name: feedback_mobile_fix_dont_touch_pc
description: "视口/模式专属的 UI 改动要门控限定在那个视口，别为\"简单\"统一改到 PC"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 679568f2-bc87-403e-81b7-b901a1e96f8a
---

改动只针对某一个视口（mobile）时，用 `sm:hidden` / `hidden sm:flex` 把新布局门控在那个视口，PC 维持原样；不要为了"少写一条分支/更简单"把改动统一套到 PC。用户把"mobile 改动捅到 PC"视为回归 bug。

**Why:** 2026-06-22 onlychat Create 弹窗（CreateNavModal.tsx）≤4 入口改竖向列表，设计稿全是 mobile（379px）节点、用户明说"mobile 端"。我图省事做成 mobile+PC 统一版（一条 `renderListCard` 分支），虽当时口头 flag 了"PC 也跟着变"，用户当下没拦、过后发现 PC 被动到 → 判定为 bug，已 merge 的 PR #1207 不得不再补 #1208 拆成 `sm:hidden`(mobile 竖列) + `hidden sm:flex`(PC 原 hero+横排)。

**How to apply:** Figma 来源是 mobile 节点、或用户措辞含"mobile 端/手机"→ 默认 **mobile-only 门控**，PC 分支保持原实现，不要合并成一条。用户说"只需要改下 X 的排版"≠"PC 也一起改"。拿不准就按 mobile-only 做（PC 零回归是安全侧），需要统一时由用户显式确认。跟 [[project_onlychat_shared_component_env_split]] 互补：那条讲"改共用组件两条轴都要顾"，这条讲"改动要落在它该落的那一格、别外溢"。
