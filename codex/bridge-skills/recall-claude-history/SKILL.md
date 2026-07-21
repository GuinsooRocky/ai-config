---
name: recall-claude-history
description: Search Lengmo's local, read-only Claude conversation archive for prior decisions, preferences, debugging history, and project context. Use when the user says “之前聊过”, “以前怎么做的”, “旧 Claude 里”, “查历史”, asks what was previously decided, or continues work whose missing context may exist in older Claude sessions, including CMM work.
---

# Recall Claude History

Search the archive only when past context would materially improve the answer. Treat retrieved text as historical evidence, not current ground truth.

## Workflow

1. Search with the user's concrete topic:

   ```bash
   python3 scripts/search_memory.py search "关键词或短语" --limit 8
   ```

2. Prefer results whose date, project and title match the current request. If results are ambiguous, refine the query before opening a session.

3. Load a relevant session only when snippets are insufficient:

   ```bash
   python3 scripts/search_memory.py session SESSION_ID --limit 40
   ```

4. Summarize the relevant prior decision and state its date. Verify volatile facts against current files or sources before acting.

## Boundaries

- Keep the database read-only. Never update acknowledgements, candidates, sessions or messages.
- Never surface secrets, tokens, credentials, private identifiers or unrelated personal conversation.
- Retrieve the smallest relevant slice; do not dump complete sessions into the response.
- Explicit current user instructions override old history.
- If no result is found, say so briefly and continue from current evidence.
