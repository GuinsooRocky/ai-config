#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
dry_run=false
with_detected_mcp=false

for argument in "$@"; do
  case "$argument" in
    --dry-run)
      dry_run=true
      ;;
    --with-detected-mcp)
      with_detected_mcp=true
      ;;
    -h|--help)
      echo "Usage: install-all.sh [--dry-run] [--with-detected-mcp]"
      exit 0
      ;;
    *)
      echo "Unknown option: $argument" >&2
      exit 2
      ;;
  esac
done

if $dry_run; then
  "$repo_root/scripts/install-claude.sh" --dry-run
else
  "$repo_root/scripts/install-claude.sh"
fi

if $dry_run && $with_detected_mcp; then
  "$repo_root/scripts/install-codex.sh" --dry-run --with-detected-mcp
elif $dry_run; then
  "$repo_root/scripts/install-codex.sh" --dry-run
elif $with_detected_mcp; then
  "$repo_root/scripts/install-codex.sh" --with-detected-mcp
else
  "$repo_root/scripts/install-codex.sh"
fi

if ! $dry_run; then
  echo "Claude + Codex 安装完成。请分别新开会话加载配置。"
fi
