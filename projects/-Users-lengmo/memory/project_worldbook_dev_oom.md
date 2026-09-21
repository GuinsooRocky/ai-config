---
name: project_worldbook_dev_oom
description: onlychat dev watchdog 的设计原理 + 三条通用监控教训（footprint 别用 ps rss / kill_port 连 3001 / ${var} 定界）；脚本细节见 cmm-go skill 的 references/watchdog.md
metadata: 
  node_type: memory
  type: project
  originSessionId: 3b3ea1c7-ced1-4474-84aa-d82100f7fb7c
---

**本条的标的 worktree `onlychat-world-book` 已回收**（无 world-book 分支；onlychat 现存 worktree 现查 `git worktree list` 别认历史名，09-21 核只剩 onlychat / onlychat-recmodel）。**留着是因为下面那套东西跨 worktree 通用**：onlychat `pnpm dev`（`next dev`, package.json 内联 `--max-old-space-size=6144`）的内存泄漏机制，以及写任何监控脚本都会栽的三条坑。watchdog 现在服务的是通用 onlychat dev（见 [[feedback_diagnose_dont_kill]] 的 `/tmp/onlychat-dev-3000.json`）。

**操作细节（启停命令、状态文件、pgrep 检测）见 cmm-go skill 的 `references/watchdog.md`**（仍在）；本 memory 只记**为什么这么设计 + 踩过的非直觉坑**。

## 为什么需要 watchdog（OOM 触发机制）

- 约 **31 分钟** uptime 后 heap OOM 崩（`FATAL ERROR: Reached heap limit`）
- 泄漏特征：`register SIGUSR1` listener 累加 + `MaxListenersExceededWarning: 11 SIGUSR1 listeners` + WebSocket(3001) 反复 restart
- 堆已 6G 还崩 → 抬堆这条路走死，**只能靠重启**
- 时间帽别当主力、别设 ≥31min（比崩还晚=没用）；footprint 阈值（≥6G）+ 崩了自愈足够

## 关键教训（写监控脚本时务必想起）

- ⭐ **测内存别用 `ps rss`** —— macOS swap/压缩下它会瘪到几十 MB（实测同进程 rss=57MB 而真实 4298MB，**偏 75 倍**），卡 RSS 阈值永远不触发。用 macOS `footprint <pid>` 的 `phys_footprint`（含压缩页，不瘪）
- ⭐ **kill_port 必须连 WS 端口 3001 (PORT+1) 一起清** —— dev server 同占 3000(HTTP)+3001(WS)，只杀 3000 残留 3001 让新 server 绑时 `EADDRINUSE: :::3001` uncaughtException 启动即崩，90s 一轮打死循环（症状：dev log 全是 EADDRINUSE，watchdog log 反复"端口无监听→重启"，**但系统内存其实充足、非 OOM**）
- start() 里别用 `( cmd & )` 子壳起 pnpm —— 会复制出第二个 watchdog 抢端口，直接 `cd && nohup pnpm dev &`
- **shell 字符串里变量紧贴中文要用 `${var}` 花括号定界** —— 写成 `pid=$opid（…` 时 nohup 的非 UTF-8 locale 下 bash 把全角"（"首字节并进变量名 → `opid�: unbound variable`（`set -u`）启动即崩，且自替换块崩前已杀旧 watchdog → 全变孤儿

## 物理约束

- dev worker 会涨到 4-6G，24G 机器同时开多 Claude session + Chrome/Figma/Lark/VSCode 会撑爆内存吃 swap → 发烫；**降温靠关并发，不是调 watchdog**
- 抗 OOM 的替代手段：`pnpm devx`（32GB heap）能撑久但在 24G 机器上会 swap，**不推荐**

相关：[[project_onlychat]] [[feedback_diagnose_dont_kill]]。
