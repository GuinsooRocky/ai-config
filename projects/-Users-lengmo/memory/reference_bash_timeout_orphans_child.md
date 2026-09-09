---
name: reference_bash_timeout_orphans_child
description: Bash 工具超时只杀 wrapper shell，heredoc 起的 python/node 子进程会被 launchd 收养继续空烧——报 exit 144 ≠ 进程已死
metadata: 
  node_type: memory
  type: reference
  originSessionId: febeeee0-6ded-4a89-badc-2832baaafe63
  modified: 2026-08-17T05:06:54.199Z
---

Claude Code 的 Bash 工具超时（默认 2min）**只终止 wrapper shell，不杀它的子进程**。用 `python3 - <<'PY' … PY` / `node -e` 这类 heredoc 起的活会变成 PPID=1 的孤儿，被 launchd 收养后**无限期继续跑**，而 harness 那边已经写下 `failed with exit code 144` 并当它结束了。

**Why**：这条不是"后台任务没句柄"（那是 [[feedback_long_run_report_to_main_chat]] 的 nohup 场景），是**前台任务也会漏**——两边都以为对方收尸，实际没人收。2026-08-15 20:47 soliloquy 一个 subagent 跑 import-graph 闭包脚本（cycle 导致 stack 无限增长），超时报 144，**孤儿又跑了 32 小时**：CPU time 23h、内存足迹 92G、24G 内存机器 swap 吃到 43.5/45G、kernel_task 常驻 60% 做内存压缩 → 整机发烫、load 5.0。owner 只感知到"电脑好烫"，从没人告诉他有个进程还活着。

**How to apply**：
- 电脑发烫/变卡先查孤儿：`ps -axo pid,ppid,etime,time,rss | awk '$2==1'` 找 PPID=1 且 TIME 巨大的；配 `sysctl vm.swapusage`（swap 快满 + kernel_task 高 = 内存压缩在烧 CPU，不是真的算力占用）
- 认领用 `lsof -p <pid>` 看 cwd 和 fd 1（会指向 `/private/tmp/claude-501/…/tasks/<taskid>.output`），再拿 taskid grep session jsonl 反查是哪个 subagent 干的
- 写一次性分析脚本时给自己加终止条件（visited set 必须单调，别写"条件满足就重新展开"的 revisit 逻辑）
- 见到 `exit code 144` 别当结束，顺手 `ps -p` 确认真死了
