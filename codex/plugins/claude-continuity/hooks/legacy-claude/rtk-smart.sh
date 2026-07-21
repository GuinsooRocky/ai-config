#!/bin/bash
# rtk-smart.sh — 动态 rtk 网关 (PreToolUse / Bash)
#
# 默认 RAW(裸跑,输出完整忠实)。只有"大输出且摘要安全"的命令才喂给 rtk 省 token。
# 手动开关(写在命令尾部,当 shell 注释,无副作用):
#   <cmd> #rtk   → 强制走 rtk 摘要(任何命令)
#   <cmd> #raw   → 强制裸跑(优先级最高)
#
# 想调"哪些命令自动省" → 改下面的 SAVINGS 正则即可。
# 排错: 临时整体停用本网关 → settings.json 里把本行换回 `rtk hook claude`,或全删。

payload=$(cat)

# 1. #raw 优先级最高 → 直接裸跑
if printf '%s' "$payload" | grep -q '#raw'; then
  exit 0
fi

# 2. #rtk → 强制省
force_rtk=0
printf '%s' "$payload" | grep -q '#rtk' && force_rtk=1

# 3. 大输出 + 摘要安全的命令白名单(其余一律裸跑)
#    依赖安装 / 构建 / 测试 / 进程列表 / docker 日志 / lint —— 这些输出大且很少需要逐行精读
SAVINGS='(npm|pnpm|yarn|bun|pip3?|brew|cargo) +(install|ci|add|update|upgrade)|(npm|pnpm|yarn|bun) +(run +)?(build|test)|(next|vite|webpack|turbo) +build|\b(tsc|eslint|vitest|jest|playwright|mocha)\b|\bps +[a-zA-Z-]|docker(-compose)? +logs'

if [ "$force_rtk" = 1 ] || printf '%s' "$payload" | grep -Eq "$SAVINGS"; then
  # 把原始 payload 交给 rtk,让它自己产出改写 JSON(它没有对应过滤器时会返回空 = 裸跑)
  printf '%s' "$payload" | PATH="$HOME/.local/bin:$PATH" rtk hook claude
  exit 0
fi

# 4. 默认: 裸跑(空输出 = Claude Code 原样执行)
exit 0
