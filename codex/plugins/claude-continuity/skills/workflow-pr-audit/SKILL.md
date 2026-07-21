---
name: workflow-pr-audit
description: "Run the migrated Claude pr-audit workflow in Codex. PR 审查引擎(可选 代码评审/质量体检)：对一组改动并行扇出多路评审 → 逐条独立对抗验证 → 汇总 P0/P1/P2。非阻塞，建 PR 后后台跑。 Use when the user names pr-audit or asks for its described end-to-end flow."
---

# pr-audit Workflow

Read `references/workflow.js` completely. Treat it as the authoritative orchestration specification, not as JavaScript to execute blindly.

Reproduce its phases, role isolation, inputs, intermediate artifacts, verification gates and final output with current Codex tools. Resolve referenced Claude agents through the migrated `agent-*` skills. Use independent sub-agents only when requested and available. Preserve the workflow's stopping conditions.
