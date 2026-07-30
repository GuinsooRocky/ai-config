#!/bin/bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
claude_root="${CLAUDE_HOME:-$(cd "$repo_root/.." && pwd)}"

copy_file() {
  local source="$1"
  local destination="$2"
  [[ -f "$source" ]] || return 0
  mkdir -p "$(dirname "$destination")"
  cp "$source" "$destination"
}

if [[ "${CONTINUITY_SNAPSHOT_AGENTS:-0}" == "1" ]]; then
  copy_file "$HOME/.codex/AGENTS.md" "$repo_root/shared/AGENTS.md"
fi

CONTINUITY_CLAUDE_SOURCE="$claude_root" \
CONTINUITY_PROFILE="${CONTINUITY_PROFILE:-core}" \
  "$repo_root/scripts/rebuild-codex-plugin.sh"
"$repo_root/scripts/verify-no-secrets.sh"
echo "Snapshot complete. Review git status before committing."
