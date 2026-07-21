---
name: workflow-prd-capability-architect
description: "Run the migrated Claude prd-capability-architect workflow in Codex. AI 架构师视角重新设计 PRD 相关能力栈：先并行测绘现状（skills/agents/workflows/数据源/触发词冲突），再用三种架构哲学并行出方案，对抗评审后合成一份可落地蓝图 Use when the user names prd-capability-architect or asks for its described end-to-end flow."
---

# prd-capability-architect Workflow

Read `references/workflow.js` completely. Treat it as the authoritative orchestration specification, not as JavaScript to execute blindly.

Reproduce its phases, role isolation, inputs, intermediate artifacts, verification gates and final output with current Codex tools. Resolve referenced Claude agents through the migrated `agent-*` skills. Use independent sub-agents only when requested and available. Preserve the workflow's stopping conditions.
