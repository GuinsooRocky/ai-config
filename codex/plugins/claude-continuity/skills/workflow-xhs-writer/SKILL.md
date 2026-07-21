---
name: workflow-xhs-writer
description: "Run the migrated Claude xhs-writer workflow in Codex. 小红书 9 宫格帖三路并行生成：同一素材同时跑科普/单点/故事三种角度，去AI味，最后出对比报告让用户选 Use when the user names xhs-writer or asks for its described end-to-end flow."
---

# xhs-writer Workflow

Read `references/workflow.js` completely. Treat it as the authoritative orchestration specification, not as JavaScript to execute blindly.

Reproduce its phases, role isolation, inputs, intermediate artifacts, verification gates and final output with current Codex tools. Resolve referenced Claude agents through the migrated `agent-*` skills. Use independent sub-agents only when requested and available. Preserve the workflow's stopping conditions.
