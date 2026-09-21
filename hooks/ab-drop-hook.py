#!/usr/bin/env python3
# 说「白帽子」/「加白」（短句）→ 不等模型，直接把当前会话加进 peekaboo-ab 不上报名单
import json, subprocess, sys
d = json.load(sys.stdin)
p = (d.get("prompt") or "").strip()
if len(p) > 12 or not any(k in p for k in ("白帽子", "加白")):
    sys.exit(0)
r = subprocess.run(["/Users/lengmo/.claude/skills/ab-drop/scripts/drop.sh", d.get("session_id", "")],
                   capture_output=True, text=True)
msg = (r.stdout + r.stderr).strip()
print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
    "additionalContext": f"[ab-drop 钩子已执行，退出码 {r.returncode}]\n{msg}\n只需用一句中文转述结果，别再调工具。"}},
    ensure_ascii=False))
