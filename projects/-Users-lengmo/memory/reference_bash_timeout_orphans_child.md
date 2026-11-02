---
name: reference_bash_timeout_orphans_child
description: Bash 工具超时只杀 wrapper shell，heredoc 起的 python/node 子进程会被 launchd 收养继续空烧——报 exit 144 ≠ 进程已死；Mac 发烫且 donotdisturbd 单核跑满 → 真因是通知中心对堆积的 osascript 桌面通知死循环，修法 killall NotificationCenter，别只杀 donotdisturbd
metadata: 
  node_type: memory
  type: reference
  originSessionId: febeeee0-6ded-4a89-badc-2832baaafe63
  modified: 2026-11-02T07:52:55.051Z
---

Claude Code 的 Bash 工具超时（默认 2min）**只终止 wrapper shell，不杀它的子进程**。用 `python3 - <<'PY' … PY` / `node -e` 这类 heredoc 起的活会变成 PPID=1 的孤儿，被 launchd 收养后**无限期继续跑**，而 harness 那边已经写下 `failed with exit code 144` 并当它结束了。

**Why**：这条不是"后台任务没句柄"（那是 [[feedback-inline-over-background-workflow]] 的 nohup 场景），是**前台任务也会漏**——两边都以为对方收尸，实际没人收。2026-08-15 20:47 soliloquy 一个 subagent 跑 import-graph 闭包脚本（cycle 导致 stack 无限增长），超时报 144，**孤儿又跑了 32 小时**：CPU time 23h、内存足迹 92G、24G 内存机器 swap 吃到 43.5/45G、kernel_task 常驻 60% 做内存压缩 → 整机发烫、load 5.0。owner 只感知到"电脑好烫"，从没人告诉他有个进程还活着。

**How to apply**：
- 电脑发烫/变卡先查孤儿：`ps -axo pid,ppid,etime,time,rss | awk '$2==1'` 找 PPID=1 且 TIME 巨大的；配 `sysctl vm.swapusage`（swap 快满 + kernel_task 高 = 内存压缩在烧 CPU，不是真的算力占用）
- 认领用 `lsof -p <pid>` 看 cwd 和 fd 1（会指向 `/private/tmp/claude-501/…/tasks/<taskid>.output`），再拿 taskid grep session jsonl 反查是哪个 subagent 干的
- 写一次性分析脚本时给自己加终止条件（visited set 必须单调，别写"条件满足就重新展开"的 revisit 逻辑）
- 见到 `exit code 144` 别当结束，顺手 `ps -p` 确认真死了


补充：08-15 一个跑飞 32h、swap 43.5G、机器发烫

## donotdisturbd 跑满=通知中心死循环

**现象**：机器发烫，`ps -r` 顶上是 `donotdisturbd`（专注模式守护进程）96% CPU 跑了 23 小时；swap 0、无 PPID=1 孤儿。`killall donotdisturbd` 无效，重启后 5 秒内又回 97%。

**真因（2026-09-12 查明）**：调用方是 NotificationCenter.app（clientIdentifier `com.apple.nc.donotdisturb.user-toggles.preload`），它在 ContextRepository 队列里对通知中心里堆积的 100 条「脚本编辑器」通知逐条问勿扰服务，每秒 300 次不停。「脚本编辑器」= 任何 `osascript -e 'display notification'` 发的通知的挂名；这 100 条来自 Claude Code 钩子 `~/.claude/hooks/subagent-stop-notify.sh`（前一晚 21:39–22:08 一个会话派了一堆子 agent）。

**修法**：`killall NotificationCenter`（系统秒拉起，通知记录不丢）→ donotdisturbd 立刻 0%。顺手把通知中心里「脚本编辑器」那组清掉更保险。

**彻底清理（09-12 已做）**：这 100 条 presented=0、`displayed` 表为空，通知中心面板上根本看不到、UI 清不了；只能 `killall usernoted NotificationCenter` 后用 `sqlite3 -cmd ".timeout 8000"` 删 record/delivered/displayed 里该 app 的行（usernoted 秒拉起并持锁，不带 timeout 会报 database is locked），再 killall 一次让它读干净的库，最后发一条测试通知验能落库。删前整库备份曾在 ~/.Trash/usernoted-db-backup-20260912/，废纸篓已清空、不可恢复。

**预防（已落地）**：`subagent-stop-notify.sh` 加了 20 秒合并限流（状态文件 /tmp/claude-subagent-notify.state），一个并行工作流不再攒几十条。

**查法速记**：`/usr/bin/log stream --process donotdisturbd --level debug` 6 秒看 bundleIdentifier 和 clientIdentifier；`sample <pid> 3` 看热帧。注意 Bash 工具里 `log` 被 shell 函数遮住，要写 `/usr/bin/log`；`#raw` 注释会吞掉同一行后面的所有命令，只能放最后。通知库在 `~/Library/Group Containers/group.com.apple.usernoted/db2/db`，app identifier 全小写。

相关：本文件上文（发烫另一常见因）、[[feedback_diagnose_dont_kill]]
