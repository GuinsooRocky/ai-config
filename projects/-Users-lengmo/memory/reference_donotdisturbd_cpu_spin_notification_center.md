---
name: donotdisturbd-cpu-spin-notification-center
description: Mac 发烫且 donotdisturbd 单核跑满 → 真因是通知中心对堆积的 osascript 桌面通知死循环；修法 killall NotificationCenter，别只杀 donotdisturbd
metadata:
  type: reference
---

**现象**：机器发烫，`ps -r` 顶上是 `donotdisturbd`（专注模式守护进程）96% CPU 跑了 23 小时；swap 0、无 PPID=1 孤儿。`killall donotdisturbd` 无效，重启后 5 秒内又回 97%。

**真因（2026-09-12 查明）**：调用方是 NotificationCenter.app（clientIdentifier `com.apple.nc.donotdisturb.user-toggles.preload`），它在 ContextRepository 队列里对通知中心里堆积的 100 条「脚本编辑器」通知逐条问勿扰服务，每秒 300 次不停。「脚本编辑器」= 任何 `osascript -e 'display notification'` 发的通知的挂名；这 100 条来自 Claude Code 钩子 `~/.claude/hooks/subagent-stop-notify.sh`（前一晚 21:39–22:08 一个会话派了一堆子 agent）。

**修法**：`killall NotificationCenter`（系统秒拉起，通知记录不丢）→ donotdisturbd 立刻 0%。顺手把通知中心里「脚本编辑器」那组清掉更保险。

**彻底清理（09-12 已做）**：这 100 条 presented=0、`displayed` 表为空，通知中心面板上根本看不到、UI 清不了；只能 `killall usernoted NotificationCenter` 后用 `sqlite3 -cmd ".timeout 8000"` 删 record/delivered/displayed 里该 app 的行（usernoted 秒拉起并持锁，不带 timeout 会报 database is locked），再 killall 一次让它读干净的库，最后发一条测试通知验能落库。删前整库备份在 ~/.Trash/usernoted-db-backup-20260912/。

**预防（已落地）**：`subagent-stop-notify.sh` 加了 20 秒合并限流（状态文件 /tmp/claude-subagent-notify.state），一个并行工作流不再攒几十条。

**查法速记**：`/usr/bin/log stream --process donotdisturbd --level debug` 6 秒看 bundleIdentifier 和 clientIdentifier；`sample <pid> 3` 看热帧。注意 Bash 工具里 `log` 被 shell 函数遮住，要写 `/usr/bin/log`；`#raw` 注释会吞掉同一行后面的所有命令，只能放最后。通知库在 `~/Library/Group Containers/group.com.apple.usernoted/db2/db`，app identifier 全小写。

相关：[[reference_bash_timeout_orphans_child]]（发烫另一常见因）、[[feedback_diagnose_dont_kill]]
