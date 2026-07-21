#!/bin/bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
plugin_root="$repo_root/plugins/claude-continuity"
claude_source="${CONTINUITY_CLAUDE_SOURCE:-}"
if [[ -z "$claude_source" ]]; then
  parent_root="$(cd "$repo_root/.." && pwd)"
  if [[ -d "$parent_root/skills" && -f "$parent_root/CLAUDE.md" ]]; then
    claude_source="$parent_root"
  else
    claude_source="$repo_root/claude"
  fi
fi
timestamp="$(date +%Y%m%d-%H%M%S)"
backup_root="$HOME/.ai-continuity-backups/plugin-refresh/$timestamp"
build_root="$(mktemp -d "${TMPDIR:-/tmp}/ai-continuity-build.XXXXXX")"
trash_root="$HOME/.Trash/ai-continuity-build-$timestamp-$$"

cleanup() {
  if [[ -d "$build_root" ]]; then
    mkdir -p "$(dirname "$trash_root")"
    /bin/mv "$build_root" "$trash_root"
  fi
}
trap cleanup EXIT

CLAUDE_SOURCE_DIR="$claude_source" \
CODEX_PLUGIN_OUTPUT="$build_root/plugin" \
CLAUDE_BRIDGE_DIR="$repo_root/bridge-skills" \
  ruby "$plugin_root/scripts/migrate_claude_assets.rb"

if [[ ! -d "$build_root/plugin/skills" ]]; then
  echo "Plugin rebuild did not produce a skills directory." >&2
  exit 1
fi

# Imported Claude assets occasionally contain trailing spaces or multiple
# blank lines at EOF. Normalize generated text only; source skills stay intact.
while IFS= read -r -d '' item; do
  if LC_ALL=C grep -Iq . "$item"; then
    perl -0pi -e 's/[ \t]+(?=\r?$)//mg; s/\n+\z/\n/' "$item"
  fi
done < <(find "$build_root/plugin" -type f -print0)

mkdir -p "$backup_root"
if [[ -d "$plugin_root/skills" ]]; then
  /bin/mv "$plugin_root/skills" "$backup_root/skills"
fi
/bin/mv "$build_root/plugin/skills" "$plugin_root/skills"

if [[ -d "$build_root/plugin/hooks" ]]; then
  mkdir -p "$plugin_root/hooks"
  rsync -a "$build_root/plugin/hooks/" "$plugin_root/hooks/"
fi
if [[ -d "$build_root/plugin/assets" ]]; then
  mkdir -p "$plugin_root/assets"
  rsync -a "$build_root/plugin/assets/" "$plugin_root/assets/"
fi

"$repo_root/scripts/verify-no-secrets.sh"
echo "Codex plugin rebuilt. Previous skills backup: $backup_root/skills"
