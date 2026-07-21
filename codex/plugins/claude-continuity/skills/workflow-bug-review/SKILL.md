---
name: workflow-bug-review
description: "Run the migrated Claude bug-review workflow in Codex. bug-hunter → adversary → judge 三件套一条命令：扫描 → 对抗 → 裁决 Use when the user names bug-review or asks for its described end-to-end flow."
---

# bug-review Workflow

Read `references/workflow.js` completely. Treat it as the authoritative orchestration specification, not as JavaScript to execute blindly.

Reproduce its phases, role isolation, inputs, intermediate artifacts, verification gates and final output with current Codex tools. Resolve referenced Claude agents through the migrated `agent-*` skills. Use independent sub-agents only when requested and available. Preserve the workflow's stopping conditions.
