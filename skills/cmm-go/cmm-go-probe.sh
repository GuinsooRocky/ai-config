#!/bin/bash
# cmm-go-probe.sh <worktree-path>
# 一次性拿齐 branch / commits / port3000(pid+cwd) / watchdog 进程 / drift，
# 顺手把 .last-seen.json 更新好。skill 主流程只调一次本脚本，替代 4 个 Bash。

set -u

WT="${1:?usage: cmm-go-probe.sh <worktree-path>}"
LAST_SEEN="$HOME/Desktop/cc-memory/onlychat/.last-seen.json"
TODAY=$(date +%Y-%m-%d)

BRANCH=$(git -C "$WT" branch --show-current 2>/dev/null)
COMMITS=$(git -C "$WT" log -5 --oneline 2>/dev/null)

PORT_PID=$(lsof -nP -iTCP:3000 -sTCP:LISTEN 2>/dev/null | awk 'NR>1 {print $2; exit}')
if [ -n "${PORT_PID:-}" ]; then
  PORT_CWD=$(lsof -p "$PORT_PID" -a -d cwd 2>/dev/null | tail -1 | awk '{print $NF}')
else
  PORT_CWD=""
fi

WATCHDOG=$(pgrep -fl 'dev-watchdog\.sh' 2>/dev/null | grep -v terminal-notifier || true)

# 读旧 branch + 写新 ts（一次 Python 调用，保留其它 worktree 条目，不全覆盖）
PREV_BRANCH=$(python3 - "$LAST_SEEN" "$WT" "$BRANCH" "$TODAY" <<'PY'
import json, sys, os
path, wt, branch, ts = sys.argv[1:5]
try:
    with open(path) as f:
        data = json.load(f)
    if not isinstance(data, dict):
        data = {}
except Exception:
    data = {}
prev = data.get(wt, {}).get("branch", "")
data[wt] = {"branch": branch, "ts": ts}
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(prev)
PY
)

if [ -z "$PREV_BRANCH" ]; then
  DRIFT="new (no prev)"
elif [ "$PREV_BRANCH" = "$BRANCH" ]; then
  DRIFT="no"
else
  DRIFT="YES (prev: $PREV_BRANCH → now: $BRANCH)"
fi

cat <<EOF
== branch ==
$BRANCH
== commits ==
$COMMITS
== port3000 ==
pid: ${PORT_PID:-none}
cwd: ${PORT_CWD:-n/a}
== watchdog ==
${WATCHDOG:-none}
== drift ==
$DRIFT
EOF
