#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
profile="${1:-}"
shift || true

case "$profile" in
  claude|codex|all) ;;
  *)
    echo "Usage: update-ai-config.sh <claude|codex|all> [installer options]" >&2
    exit 2
    ;;
esac

if ! git -C "$repo_root" diff --quiet || ! git -C "$repo_root" diff --cached --quiet; then
  echo "ai-config 有未提交的已跟踪修改，未执行 pull。请先处理这些修改。" >&2
  exit 1
fi

git -C "$repo_root" pull --rebase
"$repo_root/scripts/status.sh" "$profile"
"$repo_root/scripts/install-$profile.sh" "$@"
