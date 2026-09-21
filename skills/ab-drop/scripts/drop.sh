#!/bin/zsh
# 把 Claude 会话加进 peekaboo-ab 的 drop_sessions（不上报）。用法：drop.sh [uuid]，缺省取当前会话
set -e
sid="${1:-$CLAUDE_CODE_SESSION_ID}"
[[ "$sid" =~ '^[0-9a-f-]{36}$' ]] || { echo "拿不到合法 session uuid: '$sid'" >&2; exit 1; }
rules=~/.agentboard/privacy-rules.json
python3 - "$rules" "$sid" <<'PY'
import json, os, sys
path, sid = sys.argv[1], sys.argv[2]
data = json.load(open(path))
lst = data.setdefault("drop_sessions", [])
KEEP = 7  # 只留最近 7 个会话；"codex:" 这类前缀规则不算数、永远保留
perm = lambda x: x.endswith(":") or x == "-"  # 前缀规则与全局规则 "-" 不参与轮换
prefixes = [x for x in lst if perm(x)]
sessions = [x for x in lst if not perm(x) and x != sid] + [sid]
removed = sessions[:-KEEP]
data["drop_sessions"] = prefixes + sessions[-KEEP:]
if data["drop_sessions"] != lst:
    tmp = path + ".tmp"
    json.dump(data, open(tmp, "w"), ensure_ascii=False, indent=2)
    os.replace(tmp, path)
print(f"已加白: {sid}" + (f"（剔除最早 {len(removed)} 条）" if removed else ""))
PY
node ~/.agentboard/privacy-patch.mjs check
