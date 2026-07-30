---
name: ai-capability-router
description: Find and run a less-common capability bundled with this plugin. Use when
  the user names an unfamiliar custom skill, agent, workflow, command, shorthand,
  or asks whether an existing capability can handle a task.
---

# AI Capability Router

Use the bundled capability catalog as the source of truth for workflows that are not exposed in Codex's initial skill list.

## Resolve a capability

1. Extract one to three distinctive terms from the user's wording.
2. Search the installed catalog:

   ```bash
   python3 scripts/discover_capability.py "distinctive phrase" --limit 8
   ```

3. Read the strongest matching `SKILL.md` completely. Follow any directly referenced role, workflow, command, script, or reference needed for the task.
4. If several matches remain plausible, prefer the match whose trigger and scope most closely fit the request. Briefly state the mapping only when ambiguity remains.

## Run it in Codex

- Preserve the capability's intent, evidence requirements, stopping conditions, and output contract.
- Translate runtime-specific tool names to tools that are actually available in the current Codex session.
- Use an independent sub-agent only when the user or current repository instructions request delegation and the runtime permits it.
- Treat historical notes and generated reports as leads, not current truth. Verify changing facts and code claims.
- If a dependency is unavailable on this machine, use the documented fallback or report the missing dependency once; do not repeatedly retry a service that is not configured.

## Boundaries

- Do not read credentials, OAuth state, raw session logs, caches, or local databases through this router.
- Do not claim that a hook, connector, MCP server, or external application is active unless the current session exposes it.
- Do not copy a catalog capability into the exposed skill list merely because it was used once. Promotion into the core profile requires a repeated-use reason and an updated capability profile.
