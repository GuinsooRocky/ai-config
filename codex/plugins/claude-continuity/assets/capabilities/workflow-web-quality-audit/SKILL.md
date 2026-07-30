---
name: workflow-web-quality-audit
description: "Run the migrated Claude web-quality-audit workflow in Codex. 四维 Web 质量运行时审计：性能 / 无障碍 / SEO / 最佳实践 各派一个浏览器 agent 并行跑，对抗验证，出 P0/P1/P2 报告 Use when the user names web-quality-audit or asks for its described end-to-end flow."
---

# web-quality-audit Workflow

Read `references/workflow.js` completely. Treat it as the authoritative orchestration specification, not as JavaScript to execute blindly.

Reproduce its phases, role isolation, inputs, intermediate artifacts, verification gates and final output with current Codex tools. Resolve referenced Claude agents through the migrated `agent-*` skills. Use independent sub-agents only when requested and available. Preserve the workflow's stopping conditions.
