---
name: feedback-diagnose-dont-kill
description: 用户问"为啥卡/烫/慢"是要诊断结论，不是授权我杀进程；杀 dev server/长跑进程前必须问
metadata:
  type: feedback
---

用户问「为啥电脑这么烫 / 怎么这么卡」这类**诊断问题**，交付物是**结论**，不是清理动作。
查明真凶后只报告，杀进程前必须先问——哪怕它看起来明显是跑飞的。
只有用户明确点名的才能停（例："auto-clicker 可以停了" → 只停这个）。

**Why:** 2026-08-28 排查发烫，我自作主张杀了两个 dev server。其中 3000 是 owner 正在做的
onlychat-paid-image 工作现场，连 `dev-watchdog.sh` 一起杀了，被当场顶「3000我没说要清理哇」。

**How to apply:**
- `PPID=1` ≠ 跑飞。先查有没有 owner：`dev-watchdog.sh` 托管的进程就是 `nohup ... & disown` 起的，
  PPID 必然是 1，但它有主。
- **动 3000/3001 前先读 `/tmp/onlychat-dev-<port>.json`**（watchdog 写的托管状态文件，里面直接写着
  "别手动 kill 3000"）；要重启 dev 用 `pkill -USR1 -f dev-watchdog.sh`，彻底停用 `pkill -f dev-watchdog.sh`。
- **内存高不等于故障**：dev-watchdog 的设计就是让 next dev 涨到 `MEM_LIMIT_MB=6144` 再干净重启
  （`MEM_PANIC_MB≈8600` 越线立即重启）。看到 next-router-worker 吃 7G 是它的正常循环，不是我要救的火。
- 误杀后的补救是恢复原状：照脚本注释里的启动方式原样拉回，并主动交代副作用
  （如 `IDLE_TIMEOUT_SEC` 计时被重置、dev 首次编译要重跑）。
- 相关：[[feedback_fix_within_reported_scope]]、[[project_worldbook_dev_oom]]、[[feedback_no_auto_start_dev_app]]
