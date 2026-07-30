---
name: grill-me
description: Interview the user one question at a time to resolve ambiguity in a plan
  or design. Use only when the user explicitly asks to be grilled or challenged interactively.
---

# Grill Me — 方案拷问（无 PRD 版）

## 何时使用

- 用户有一个**已成形**的计划/设计，想被拷问找漏洞、达成共识
- 触发词："grill me"、"拷问我"、"挑战这个方案"、"把这个计划问透"

## 何时不用

- 有 PRD 可对照 → `/grill-with-prd`（对照 PRD 逐点追问）
- 想法还没成形、要从 0 理清 → `brainstorm`
- 审 PRD 文档本身（矛盾/缺文案）→ `onlychat-prd-reflection`

## 执行

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.

规则：
1. **一次只问一个问题**，等回答再问下一个
2. **每问附带你的推荐答案**——用户可以直接回"按推荐"
3. 问题能靠翻代码库回答的，自己去翻，别浪费用户回合
4. 顺决策树走：先问影响后续分支的根决策，再进细节
5. 用户说"先跳过"的问题记入未决项，别缠着不放

## 收尾输出

到达共识后输出：
- **决议清单**：每条 = 问题 → 拍板结果（一行一条）
- **未决项**：跳过的问题单列
- 不写代码、不出实现方案——那是批准之后的事

## Codex compatibility

Preserve this workflow's intent and evidence rules. Translate Claude-specific tool names to the available Codex tools.
