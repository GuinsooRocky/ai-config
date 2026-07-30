---
name: project-auto-clicker-daily
description: auto-clicker 抓取已自动化：launchd 每天 13:30 跑 run-daily-cron.sh，自动挑卡+自动定 ROUND_CAP
metadata: 
  node_type: memory
  type: project
  originSessionId: 6598c861-bd0c-4cf2-b70f-d7f3e4c18a4e
  modified: 2026-07-22T06:25:24.633Z
---

`~/Desktop/loop_project/auto-clicker`（crushon 图集卡自动抓取）2026-07-22 起改自动跑，用户不用再每天开口。

- 定时：LaunchAgent `com.lengmo.auto-clicker.daily`（plist 在 ~/Library/LaunchAgents），每天 **13:30 本地**触发 `run-daily-cron.sh`（单实例守卫 → `run-daily.sh`）。13:30 安全是因为额度按 **UTC 零点**重置，本机 JST 即 09:00 已重置完。
- 挑卡：`plan-next.mjs` 每跑完一张重算——未 done 且 rounds<150 的卡里，先续在跑的（unlocked 多的优先），再按清单顺序开新卡；单卡单日 +43 轮；额度 215/天，剩 <10 收工。日志全进 `farm-run.log`。
- 旧的手工指定版 `run-until-quota.sh` 保留没删。
- ⚠ **TCC 卡点**：launchd 起的进程默认碰不了 `~/Desktop`（exit 126 / EX_CONFIG）。解法=给 `/bin/bash` 开「完全磁盘访问权限」（2026-07-22 用户拍板选这条）。launchd 自己的 stdout 也不能指向 Desktop，已改到 `~/Library/Logs/auto-clicker-launchd.log`。
- ⚠ 手动起长跑**别用 Bash 工具的 run_in_background**：harness timeout 上限 10 分钟，到点 SIGTERM 掐掉（07-22 栽过一次）。用 `nohup ... & disown` + Monitor tail 日志报进度。
- ⚠ `run-daily.sh` 正在跑时**别编辑它**（bash 按字节偏移续读，会执行错位）——要改逻辑等它收工，或改 `plan-next.mjs`（node 一次性读完，安全）。

**Why:** 用户连着 5 天手动说"可以开始跑了"，这活本身没有每日决策成分。
**How to apply:** 再被问起先看 `farm-run.log` 尾部和 launchd 状态，别默认没在跑；要临时插队直接 `bash run-daily.sh`。
