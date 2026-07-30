#!/bin/bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
source_root="$(cd "$repo_root/.." && pwd)"
codex_root="${CODEX_HOME:-$HOME/.codex}"
backup_root="$codex_root/continuity-backups/$(date +%Y%m%d-%H%M%S)"
helper_root="$HOME/.local/share/ai-continuity"
dry_run=false
with_detected_mcp=false

usage() {
  cat <<'EOF'
Usage: install-codex.sh [--dry-run] [--with-detected-mcp]

Installs the portable core capability profile. Optional MCP setup only adds
local services whose dependencies are available on this machine.
EOF
}

for argument in "$@"; do
  case "$argument" in
    --dry-run) dry_run=true ;;
    --with-detected-mcp) with_detected_mcp=true ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $argument" >&2; usage >&2; exit 2 ;;
  esac
done

"$repo_root/scripts/verify-no-secrets.sh"
profile_summary="$(ruby "$repo_root/scripts/verify-codex-profile.rb")"

if $dry_run; then
  echo "Would back up and install shared/AGENTS.md -> $codex_root/AGENTS.md"
  echo "Would install the portable claude-continuity core plugin from $repo_root"
  if $with_detected_mcp; then
    echo "Would add only MCP servers whose local dependencies are currently available."
  else
    echo "Would leave MCP configuration unchanged."
  fi
  echo "$profile_summary"
  release_version="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$source_root/ai-config.json")"
  echo "ai-config release: $release_version"
  echo "Codex restore dry run passed."
  exit 0
fi

if [[ -f "$codex_root/AGENTS.md" ]]; then
  mkdir -p "$backup_root"
  cp "$codex_root/AGENTS.md" "$backup_root/AGENTS.md"
fi
mkdir -p "$codex_root"
cp "$repo_root/shared/AGENTS.md" "$codex_root/AGENTS.md"

if ! codex plugin marketplace list | awk '$1 == "ai-continuity" { found=1 } END { exit(found ? 0 : 1) }'; then
  codex plugin marketplace add "$repo_root"
fi
codex plugin add claude-continuity@ai-continuity

mcp_added=0
if $with_detected_mcp; then
  if curl -sS --max-time 1 -o /dev/null http://127.0.0.1:3845/mcp 2>/dev/null && \
     ! codex mcp get figma >/dev/null 2>&1; then
    codex mcp add figma --url http://127.0.0.1:3845/mcp
    mcp_added=$((mcp_added + 1))
  fi

  lich_server="$HOME/Desktop/my-code/lich/mcp/lich-tasks.mjs"
  if [[ -f "$lich_server" ]] && command -v node >/dev/null 2>&1 && \
     ! codex mcp get lich-tasks >/dev/null 2>&1; then
    codex mcp add lich-tasks -- node "$lich_server"
    mcp_added=$((mcp_added + 1))
  fi

  claude_config="$HOME/.claude.json"
  if [[ -f "$claude_config" ]] && command -v jq >/dev/null 2>&1 && command -v npx >/dev/null 2>&1 && \
     jq -e '.mcpServers.lark.args[6] and .mcpServers.lark.args[8]' "$claude_config" >/dev/null 2>&1 && \
     ! codex mcp get lark >/dev/null 2>&1; then
    mkdir -p "$helper_root"
    cp "$repo_root/plugins/claude-continuity/scripts/run-lark-mcp.sh" "$helper_root/run-lark-mcp.sh"
    chmod +x "$helper_root/run-lark-mcp.sh"
    codex mcp add lark -- bash "$helper_root/run-lark-mcp.sh"
    mcp_added=$((mcp_added + 1))
  fi
fi

python3 "$source_root/scripts/profile_state.py" record codex --install-root "$codex_root"

echo "Codex continuity core installed. Detected MCP servers added: $mcp_added. Backup: $backup_root"
echo "$profile_summary"
echo "Start a new Codex thread to load the updated capability profile."
