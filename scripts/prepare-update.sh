#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
part="${1:-patch}"

case "$part" in
  major|minor|patch) ;;
  *)
    echo "Usage: prepare-update.sh [major|minor|patch]" >&2
    exit 2
    ;;
esac

changed_files="$({
  git -C "$repo_root" diff --name-only HEAD
  git -C "$repo_root" ls-files --others --exclude-standard
} | sort -u)"

if [[ -z "$changed_files" ]]; then
  echo "没有需要发布的修改。"
  exit 0
fi

if printf '%s\n' "$changed_files" | grep -Eq \
  '^(agents|commands|design-spec|hooks|skills|workflows)/|^RTK\.md$|^codex/(bridge-skills|capabilities\.json)|^codex/plugins/claude-continuity/scripts/migrate_claude_assets\.rb$'; then
  CONTINUITY_CLAUDE_SOURCE="$repo_root" \
    "$repo_root/codex/scripts/rebuild-codex-plugin.sh"
elif printf '%s\n' "$changed_files" | grep -q '^codex/plugins/claude-continuity/'; then
  cachebuster_helper="$HOME/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py"
  if [[ ! -f "$cachebuster_helper" ]]; then
    echo "Codex plugin cachebuster helper not found: $cachebuster_helper" >&2
    exit 1
  fi
  python3 "$cachebuster_helper" "$repo_root/codex/plugins/claude-continuity"
fi

"$repo_root/scripts/bump-version.sh" "$part"
git -C "$repo_root" diff --check
"$repo_root/codex/scripts/verify-no-secrets.sh"
ruby "$repo_root/codex/scripts/verify-codex-profile.rb"
"$repo_root/scripts/status.sh"

echo
echo "待发布文件如下；脚本没有 stage、commit 或 push："
git -C "$repo_root" status --short
