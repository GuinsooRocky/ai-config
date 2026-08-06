#!/bin/bash
# rhythm-guard —— 节律守卫（2026-08-06 依 08-04 工作模式体检立法）
# 挂在 UserPromptSubmit：stdout 注入对话上下文，无事保持沉默、零输出。
# 职责一：每周首次开工 → 报人工闸清单未销数，提醒排 2 小时档期
# 职责二：凌晨 03:00–05:59 → 熔断提醒（每个工作日夜只提一次，06:00 日界与体检口径一致）

STAMP_DIR="$HOME/.claude/cache/rhythm-guard"
GATE_FILE="$HOME/Desktop/archives/self/人工闸.md"
mkdir -p "$STAMP_DIR" 2>/dev/null

# ---- 周度人工闸提醒（ISO 周，一周只发一次）----
week="$(date +%G-W%V)"
if [ "$(cat "$STAMP_DIR/week" 2>/dev/null)" != "$week" ]; then
  echo "$week" > "$STAMP_DIR/week"
  if [ -f "$GATE_FILE" ]; then
    open_count="$(grep -c '^- \[ \]' "$GATE_FILE" 2>/dev/null)"
    [ -n "$open_count" ] || open_count=0
    if [ "$open_count" -gt 0 ]; then
      top="$(grep -m 3 '^- \[ \]' "$GATE_FILE" | sed 's/^- \[ \] /  · /')"
      printf '[人工闸·周提醒] 新的一周：只有本人能开的闸还有 %s 项未销，本周记得排一个 2 小时档期。前几项：\n%s\n完整清单：%s\n（收到请原样转达给用户，别吞。）\n' "$open_count" "$top" "$GATE_FILE"
    fi
  fi
fi

# ---- 凌晨熔断（03:00–05:59，每夜一次）----
case "$(date +%H)" in
  03|04|05)
    night="$(date -v-6H +%Y%m%d)"
    if [ "$(cat "$STAMP_DIR/night" 2>/dev/null)" != "$night" ]; then
      echo "$night" > "$STAMP_DIR/night"
      echo "[熔断·凌晨3点] 已过凌晨 3 点（体检基线：12/24 天过 3 点，30 天目标 ≤4）。建议把手头活写成交接 prompt 丢给跑批线，明天接着。（收到请原样转达给用户，别吞。）"
    fi
    ;;
esac
exit 0
