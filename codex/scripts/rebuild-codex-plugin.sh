#!/bin/bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
plugin_root="$repo_root/plugins/claude-continuity"
profile_name="${CONTINUITY_PROFILE:-core}"
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
CONTINUITY_CAPABILITY_CONFIG="$repo_root/capabilities.json" \
CONTINUITY_PROFILE="$profile_name" \
  ruby "$plugin_root/scripts/migrate_claude_assets.rb"

if [[ ! -d "$build_root/plugin/skills" || ! -d "$build_root/plugin/assets/capabilities" ]]; then
  echo "Plugin rebuild did not produce the exposed skills and capability catalog." >&2
  exit 1
fi

mkdir -p "$build_root/plugin/.codex-plugin"
cp "$plugin_root/.codex-plugin/plugin.json" "$build_root/plugin/.codex-plugin/plugin.json"

CONTINUITY_PROFILE="$profile_name" \
  ruby "$repo_root/scripts/verify-codex-profile.rb" "$build_root/plugin"

# Imported Claude assets occasionally contain trailing spaces or multiple
# blank lines at EOF. Normalize generated text only; source skills stay intact.
while IFS= read -r -d '' item; do
  if LC_ALL=C grep -Iq . "$item"; then
    perl -0pi -e 's/[ \t]+(?=\r?$)//mg; s/\n+\z/\n/' "$item"
  fi
done < <(find "$build_root/plugin" -type f -print0)

generated_output_changed=false
for generated_path in skills assets hooks; do
  current_path="$plugin_root/$generated_path"
  next_path="$build_root/plugin/$generated_path"
  if [[ -e "$current_path" || -e "$next_path" ]]; then
    if [[ ! -e "$current_path" || ! -e "$next_path" ]] || \
       ! diff -qr "$current_path" "$next_path" >/dev/null; then
      generated_output_changed=true
      break
    fi
  fi
done

if ! $generated_output_changed; then
  "$repo_root/scripts/verify-no-secrets.sh"
  CONTINUITY_PROFILE="$profile_name" ruby "$repo_root/scripts/verify-codex-profile.rb" "$plugin_root"
  echo "Codex generated profile is unchanged; kept the existing plugin version."
  exit 0
fi

mkdir -p "$backup_root"
if [[ -d "$plugin_root/skills" ]]; then
  /bin/mv "$plugin_root/skills" "$backup_root/skills"
fi
/bin/mv "$build_root/plugin/skills" "$plugin_root/skills"

for generated_path in assets hooks; do
  if [[ -e "$plugin_root/$generated_path" ]]; then
    /bin/mv "$plugin_root/$generated_path" "$backup_root/$generated_path"
  fi
  if [[ -e "$build_root/plugin/$generated_path" ]]; then
    /bin/mv "$build_root/plugin/$generated_path" "$plugin_root/$generated_path"
  fi
done

cachebuster_helper="$HOME/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py"
if [[ ! -f "$cachebuster_helper" ]]; then
  echo "Codex plugin cachebuster helper not found: $cachebuster_helper" >&2
  exit 1
fi
python3 "$cachebuster_helper" "$plugin_root"

"$repo_root/scripts/verify-no-secrets.sh"
CONTINUITY_PROFILE="$profile_name" ruby "$repo_root/scripts/verify-codex-profile.rb" "$plugin_root"
echo "Codex plugin rebuilt with profile $profile_name. Previous build backup: $backup_root"
