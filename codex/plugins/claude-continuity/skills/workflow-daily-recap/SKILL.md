---
name: workflow-daily-recap
description: "Run the migrated Claude daily-recap workflow in Codex. 每日复盘：侦察需补写日期 → 并行摘要各天 → 按序 upsert 进单文件 Use when the user names daily-recap or asks for its described end-to-end flow."
---

# daily-recap Workflow

Read `references/workflow.js` completely. Treat it as the authoritative orchestration specification, not as JavaScript to execute blindly.

Reproduce its phases, role isolation, inputs, intermediate artifacts, verification gates and final output with current Codex tools. Resolve referenced Claude agents through the migrated `agent-*` skills. Use independent sub-agents only when requested and available. Preserve the workflow's stopping conditions.
