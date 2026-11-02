---
name: Figma MCP strict values
description: Figma MCP 给出具体 css/token 值时必须原样照抄，不得估算或替换等价物；onlychat 里 owner 甩 Figma 链接 + 「Implement this design」时，先确认画板属于哪条需求、开发是不是他，是别人的需求就停、不实现；Figma 对齐任务列「待拍」前先查项目 rules 已定口径（文案跟 PRD / 颜色跟 Figma / 多帧=多态），09-03 三条全是已定案被顶「都这么明显了」
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8ee76bda-9231-4378-8bf1-f2a6c4ddd15d
  modified: 2026-11-02T07:52:40.527Z
---
用 Figma MCP 做设计还原时，**严格使用 MCP 返回的具体值**：rgba/hex/opacity/px/stops/design tokens 一个字都不改。

**Why:** 用户踩过一次 —— Figma spec 写着 `background: rgba(247,94,204,0.20)`，我没查 MCP 变量表、直接用了 `bg-dark3-primary` 实色，走了一轮返工。

**How to apply:**
1. 看到 "Implement this design from Figma" + URL 或 node 时，先 `get_design_context` / `get_variable_defs` / `get_screenshot` 拿具体值
2. 色值优先用 MCP 返回的 `rgba()` / hex — 别用「差不多的 token」替换
3. alpha 比例、font-weight、border-width、gradient stops、line-height 这些数值直接照抄 spec
4. 只有 MCP 没明确给值时才推断，并告知用户推断依据

## 甩 Figma 先查需求归属

owner 甩 Figma 链接配「Implement this design from Figma / 利用 mcp 检查 UI 新改动」，不等于这块画板就是他的活。

2026-10-13：他甩的是设计师文件里「GIF 标签」整块画板，我查到排期表里这条（6.36.0 付费图片增加 GIF 标签）Web 前端挂的是傅晓杰，却仍打算照做、只在结尾提一句，被纠正「gif 貌似不是我的需求」。他的本意是看这份设计稿里有没有画到他自己那条需求（付费图定价）的新改动。

**Why:** 同一份设计稿会混着好几个人的需求；照着画板实现别人的需求会和对方撞文件、白干一场。

**How to apply:**
- 画板名或 PRD 跟手上的需求对不上时，先查排期表这条需求的开发人员（飞书 bitable「crushonai排期表（新付费版）」，用 social-proxy 的 get_bitable 按需求标题过滤）。
- 开发不是 owner → 不写代码，转成「这份稿里有没有画到 owner 自己需求的部分」去对，并直接报结论。
- 开发是 owner 或排期表查不到 → 照常实现。相关 [[feedback_fix_within_reported_scope]]。

## Figma 待拍先查 rules

Figma 对齐任务里别把项目已定案的口径再列成「待拍」。2026-09-03 付费开关改版我列了三条待拍：PC 三张稿三选一、稿子文案要不要加、选中色跟不跟主题色——owner 回「又待拍 都这么明显了」：三张稿是同一稿的**多种状态**不是备选；文案**跟 PRD**；颜色**跟 Figma**。后两条 onlychat 的 `.claude/rules/figma-mcp.md`「样式对齐边界」早写死了（只动样式不动文案；Figma token 照抄）。

**Why:** 待拍清单每一条都在消耗 owner 注意力；已有 rule 答过的问题再问 = 没读 rule。同一 Figma section 里 ID 相近的多个 frame 默认是状态枚举，不是方案备选。

**How to apply:** 列待拍前先 grep 项目 `.claude/rules/` 与 CLAUDE.md 有没有现成口径；命中就按口径直接做并在报告里写「按 rule X」。多个相邻 frame 先当多态实现，只有稿子明确标「方案 A/B」才算备选。关联 [[feedback_owner_decision_interaction]]。
