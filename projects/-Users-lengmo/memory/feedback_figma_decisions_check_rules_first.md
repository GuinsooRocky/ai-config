---
name: figma-decisions-check-rules-first
description: Figma 对齐任务列「待拍」前先查项目 rules 已定口径（文案跟 PRD / 颜色跟 Figma / 多帧=多态）；09-03 三条全是已定案被顶「都这么明显了」
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 62600d65-981b-4ac0-a916-2f35573ec280
  modified: 2026-09-03T03:26:28.338Z
---

Figma 对齐任务里别把项目已定案的口径再列成「待拍」。2026-09-03 付费开关改版我列了三条待拍：PC 三张稿三选一、稿子文案要不要加、选中色跟不跟主题色——owner 回「又待拍 都这么明显了」：三张稿是同一稿的**多种状态**不是备选；文案**跟 PRD**；颜色**跟 Figma**。后两条 onlychat 的 `.claude/rules/figma-mcp.md`「样式对齐边界」早写死了（只动样式不动文案；Figma token 照抄）。

**Why:** 待拍清单每一条都在消耗 owner 注意力；已有 rule 答过的问题再问 = 没读 rule。同一 Figma section 里 ID 相近的多个 frame 默认是状态枚举，不是方案备选。

**How to apply:** 列待拍前先 grep 项目 `.claude/rules/` 与 CLAUDE.md 有没有现成口径；命中就按口径直接做并在报告里写「按 rule X」。多个相邻 frame 先当多态实现，只有稿子明确标「方案 A/B」才算备选。关联 [[feedback_owner_decision_interaction]] [[ideas-need-no-owner-signoff]]。
