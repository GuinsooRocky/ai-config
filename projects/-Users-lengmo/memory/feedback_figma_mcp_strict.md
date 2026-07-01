---
name: Figma MCP strict values
description: Figma MCP 给出具体 css/token 值时必须原样照抄，不得估算或替换等价物
type: feedback
originSessionId: 8ee76bda-9231-4378-8bf1-f2a6c4ddd15d
---
用 Figma MCP 做设计还原时，**严格使用 MCP 返回的具体值**：rgba/hex/opacity/px/stops/design tokens 一个字都不改。

**Why:** 用户踩过一次 —— Figma spec 写着 `background: rgba(247,94,204,0.20)`，我没查 MCP 变量表、直接用了 `bg-dark3-primary` 实色，走了一轮返工。

**How to apply:**
1. 看到 "Implement this design from Figma" + URL 或 node 时，先 `get_design_context` / `get_variable_defs` / `get_screenshot` 拿具体值
2. 色值优先用 MCP 返回的 `rgba()` / hex — 别用「差不多的 token」替换
3. alpha 比例、font-weight、border-width、gradient stops、line-height 这些数值直接照抄 spec
4. 只有 MCP 没明确给值时才推断，并告知用户推断依据
