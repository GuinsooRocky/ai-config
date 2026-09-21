#!/usr/bin/env bash
# Fires a macOS notification when a Claude Code subagent completes.
# Shows agent_type as title and the first line of last_assistant_message as body.

STDIN=$(cat)
printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$STDIN" >> /tmp/claude-subagent-stop.log

NAME=$(printf '%s' "$STDIN" | jq -r '.agent_type // "subagent"' 2>/dev/null)
case "$NAME" in ""|null) NAME="subagent" ;; esac

MSG=$(printf '%s' "$STDIN" | jq -r '.last_assistant_message // ""' 2>/dev/null \
  | head -1 \
  | cut -c1-80)

NAME_SAFE=$(printf '%s' "$NAME" | tr -d '"\\')
MSG_SAFE=$(printf '%s' "$MSG"   | tr -d '"\\')

# 合并限流：20 秒内多个子 agent 收工只弹一条，其余计数并入下一条。
# 2026-09-12 教训：一晚攒了 100 条通知，通知中心对着它们死循环，donotdisturbd 跑满一颗核 23 小时。
STATE=/tmp/claude-subagent-notify.state
NOW=$(date +%s); LAST=0; PENDING=0
[ -f "$STATE" ] && read -r LAST PENDING < "$STATE"
case "$LAST$PENDING" in *[!0-9]*) LAST=0; PENDING=0 ;; esac
if [ $((NOW - LAST)) -lt 20 ]; then
  printf '%s %s\n' "$LAST" "$((PENDING + 1))" > "$STATE"
  exit 0
fi
[ "$PENDING" -gt 0 ] && MSG_SAFE="(+${PENDING} 个已合并) ${MSG_SAFE}"
printf '%s 0\n' "$NOW" > "$STATE"

# 用 osascript（弹完即退）替代 terminal-notifier：
# terminal-notifier 弹完会驻留等通知中心确认、不自退，子 agent 跑多了会攒成上千个僵尸进程。
# osascript display notification 弹完立刻退出，永不堆积。仍后台 + disown，保证绝不阻塞 hook 返回。
nohup osascript -e "display notification \"${MSG_SAFE}\" with title \"Claude Code\" subtitle \"${NAME_SAFE}\" sound name \"Glass\"" \
  >/dev/null 2>&1 &
disown 2>/dev/null || true

exit 0
