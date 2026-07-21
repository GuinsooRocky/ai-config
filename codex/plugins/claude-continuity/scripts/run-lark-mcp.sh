#!/bin/bash
set -euo pipefail

claude_config="${CLAUDE_CONFIG_PATH:-$HOME/.claude.json}"
if [[ ! -f "$claude_config" ]]; then
  echo "Claude MCP config not found: $claude_config" >&2
  exit 1
fi

app_id="$(jq -r '.mcpServers.lark.args[6] // empty' "$claude_config")"
app_secret="$(jq -r '.mcpServers.lark.args[8] // empty' "$claude_config")"
if [[ -z "$app_id" || -z "$app_secret" ]]; then
  echo "Lark credentials are missing from the existing Claude MCP config." >&2
  exit 1
fi

exec npx -y -p @larksuiteoapi/lark-mcp lark-mcp mcp \
  --app-id "$app_id" \
  --app-secret "$app_secret" \
  --language zh \
  --token-mode auto \
  --oauth \
  --tools preset.default
