#!/bin/bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
codex_root="${CODEX_HOME:-$HOME/.codex}"
backup_root="$codex_root/continuity-backups/$(date +%Y%m%d-%H%M%S)"
helper_root="$HOME/.local/share/ai-continuity"
dry_run=false
[[ "${1:-}" == "--dry-run" ]] && dry_run=true

"$repo_root/scripts/verify-no-secrets.sh"

if $dry_run; then
  echo "Would back up and install shared/AGENTS.md -> $codex_root/AGENTS.md"
  echo "Would install the Lark credential bridge -> $helper_root/run-lark-mcp.sh"
  echo "Would add marketplace $repo_root and install claude-continuity@ai-continuity"
  echo "Codex restore dry run passed."
  exit 0
fi

if [[ -f "$codex_root/AGENTS.md" ]]; then
  mkdir -p "$backup_root"
  cp "$codex_root/AGENTS.md" "$backup_root/AGENTS.md"
fi
mkdir -p "$codex_root" "$helper_root"
cp "$repo_root/shared/AGENTS.md" "$codex_root/AGENTS.md"
cp "$repo_root/plugins/claude-continuity/scripts/run-lark-mcp.sh" "$helper_root/run-lark-mcp.sh"
chmod +x "$helper_root/run-lark-mcp.sh"

codex plugin marketplace add "$repo_root"
codex plugin add claude-continuity@ai-continuity
echo "Codex continuity plugin installed. Backup: $backup_root"
