---
name: workflow-five-identity
description: "Run the migrated Claude five-identity workflow in Codex. Stage-aware Boris Cherny five-identity review — routes to the right mix based on product lifecycle stage Use when the user names five-identity or asks for its described end-to-end flow."
---

# five-identity Workflow

Read `references/workflow.js` completely. Treat it as the authoritative orchestration specification, not as JavaScript to execute blindly.

Reproduce its phases, role isolation, inputs, intermediate artifacts, verification gates and final output with current Codex tools. Resolve referenced Claude agents through the migrated `agent-*` skills. Use independent sub-agents only when requested and available. Preserve the workflow's stopping conditions.
