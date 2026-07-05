# RTK - Rust Token Killer

**Usage**: Token-optimized CLI proxy (60-90% savings on dev operations)

## Meta Commands (always use rtk directly)

```bash
rtk gain              # Show token savings analytics
rtk gain --history    # Show command usage history with savings
rtk discover          # Analyze Claude Code history for missed opportunities
rtk proxy <cmd>       # Execute raw command without filtering (for debugging)
```

## Installation Verification

```bash
rtk --version         # Should show: rtk X.Y.Z
rtk gain              # Should work (not "command not found")
which rtk             # Verify correct binary
```

⚠️ **Name collision**: If `rtk gain` fails, you may have reachingforthejack/rtk (Rust Type Kit) installed instead.

## Hook-Based Usage（rtk-smart 智能网关，2026-06-26 起）

默认**裸跑**（输出完整忠实）。只有大输出且摘要安全的命令自动走 rtk：
install 类（npm/pnpm/yarn/bun/pip/brew/cargo）、build/test（tsc/eslint/vitest/jest/playwright/mocha）、ps、docker logs。

手动开关（写在命令尾部当注释）：
- `<cmd> #rtk` → 强制走 rtk 摘要
- `<cmd> #raw` → 强制裸跑（优先级最高）

git/grep/cat 等精度命令默认不改写，不需要用 `rtk proxy` 绕路。
路由逻辑见 `~/.claude/hooks/rtk-smart.sh`（改白名单就是改里面的 SAVINGS 正则）。
