---
name: workflow-pageforge-accept-pipeline
description: "Run the migrated Claude pageforge-accept-pipeline workflow in Codex. pageforge 生码验收三步全自动：mock-data-builder 造数据 → visual-qa 四象限走查（免确认）→ pageforge-acceptance-judge 打 100 分 Use when the user names pageforge-accept-pipeline or asks for its described end-to-end flow."
---

# pageforge-accept-pipeline Workflow

Read `references/workflow.js` completely. Treat it as the authoritative orchestration specification, not as JavaScript to execute blindly.

Reproduce its phases, role isolation, inputs, intermediate artifacts, verification gates and final output with current Codex tools. Resolve referenced Claude agents through the migrated `agent-*` skills. Use independent sub-agents only when requested and available. Preserve the workflow's stopping conditions.
