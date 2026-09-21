#!/usr/bin/env bash
# 每日把 memory 目录的改动落一笔本地 commit。只 commit memory 路径（别人预先 stage 的文件不扫走），不 push。
# 其余目录（skills/agents/hooks…）仍走 prepare-update.sh 手工流程，因为那条要重建 codex 插件 + 升版本号。
set -euo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
repo="$HOME/.claude"
mem="projects/-Users-lengmo/memory"
cd "$repo"
git add -- "$mem"
if git diff --cached --quiet -- "$mem"; then
  echo "$(date '+%F %T') memory 无改动，跳过"
  exit 0
fi
git commit -q -m "memory 自动快照 $(date +%F)" -- "$mem"
echo "$(date '+%F %T') 已提交 $(git log -1 --format=%h) ($(git show --stat --format= HEAD | tail -1))"
