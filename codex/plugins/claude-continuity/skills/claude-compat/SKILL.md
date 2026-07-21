---
name: claude-compat
description: >-
  Compatibility bridge for Lengmo's live Claude setup. Resolve and reuse existing Claude skills, agents, workflows, commands, project conventions, and remembered shorthand inside Codex. Use when the user references an old Claude capability, custom agent, workflow, slash-command behavior, personal shorthand, says “像 Claude 一样”, “以前那个能力”, “无缝衔接”, or gives an unfamiliar phrase that may be defined in ~/.claude. Also use before creating a one-off replacement skill for an example, including CMM capabilities.
---

# Claude Compatibility Bridge

Preserve behavior, triggers, roles and evidence discipline without mechanically copying Claude-specific runtime code. Use the live `~/.claude` tree as the source of truth; use `~/Desktop/cc-memory/cc-防丢失` only as a fallback.

## Resolve a capability

1. Extract one to three distinctive terms from the user's wording. Search the live setup:

   ```bash
   python3 scripts/discover_capability.py "distinctive phrase" --limit 10
   ```

2. Read only the strongest matching definitions in this order:
   - `~/.claude/skills/*/SKILL.md`
   - `~/.claude/agents/*.md`
   - `~/.claude/workflows/*.js` and `~/.claude/commands/`
   - `~/.claude/projects/-Users-lengmo/memory/MEMORY.md` and its linked memory files
   - `recall-claude-history` for older conversation evidence
3. Resolve conflicts by precedence: current user instruction, current project files, live Claude definition, current memory, backup, old conversation.
4. State the resolved meaning briefly only when ambiguity remains. Otherwise continue the task directly.

## Adapt to Codex

- Claude skill: follow its domain workflow, translating tool names to available Codex tools. Do not duplicate it unless durable Codex-specific changes are genuinely required.
- Claude agent: read the role definition and give that role to an independent Codex sub-agent when the user requested agent, panel, parallel or delegated work and the runtime permits it. Respect current concurrency limits; do not hard-code Claude model names.
- Claude workflow: treat the JavaScript as an orchestration specification. Reproduce its phases, inputs, isolation and acceptance criteria with current tools; do not blindly execute product-specific workflow code.
- Claude command: preserve the command's user-facing intent and workflow even if the slash command itself does not exist in Codex.
- Claude hook or lifecycle automation: do not claim it is active. Explain the missing lifecycle surface only if it materially affects the requested result.
- Memory: retrieve the smallest relevant slice. Historical notes are context, not current truth; verify volatile facts and code claims.

## Guardrails

- Never import settings, OAuth state, API keys, MCP secrets, caches or session credentials.
- Do not create one skill per user example. Add a dedicated Codex skill only when the user asks for one or when the workflow needs stable Codex-specific scripts/assets that the bridge cannot supply.
- Be transparent when a Claude runtime feature has no Codex equivalent; preserve the outcome using the closest current mechanism.
