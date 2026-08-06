---
name: project-auto-clicker-daily
description: auto-clicker 抓取跑法：launchd 自动任务已不在（纯手动起）；--headless 2026-08-06 复测已恢复可用；选 ID 段前先查 state 别烧额度在老卡上
metadata: 
  node_type: memory
  type: project
  originSessionId: 6598c861-bd0c-4cf2-b70f-d7f3e4c18a4e
  modified: 2026-08-06T05:07:13.452Z
---

`~/Desktop/loop_project/auto-clicker`（crushon 图集卡自动抓取）2026-07-22 起改自动跑，用户不用再每天开口。

- ⚠ **2026-08-01 复核：定时任务已经没了**。`~/Library/LaunchAgents` 里没有 `com.lengmo.auto-clicker.daily`，`launchctl list` 也查不到 → 现在是**纯手动起**，别默认"它自己在跑"。（原设计：每天 13:30 本地触发 `run-daily-cron.sh`；13:30 安全是因为额度按 **UTC 零点**重置，本机 JST 即 09:00 已重置完。要重装照这个时间。）
- ✅ **`--headless` 2026-08-06 复测已恢复可用**（登录态秒过、跑满 215 额度）。08-01 记的"headless 登不上必须有头跑"当天真实，但已不成立——别再按那条改成有头跑。codex 侧 `AGENTS.md` 也要求 headless（`--background` 会闪屏）。
- 「从小到大、解锁了就跳下一个」的跑法有两种，08-06 用的是 **ID 升序版**：
  `env ROUND_CAP=150 STALL_ROUNDS=10 CHECK_EVERY=1 node crushon-album-farm.mjs --headless --ids=<起>-582`
  （并发 3，`CHECK_EVERY=1` 不能省否则 stall 判定延迟）。另一种是 `--album-asc` 按图集总数升序。两种都不走 `plan-next.mjs`。
- ⚠ **选 ID 段前必须先查 `runtime/state.json`**：`ROUND_CAP=150` 只让**已满 150 轮**的卡秒跳过；跑到 120–148 轮的老卡（#9/#10/#15/#16/#18/#21）会真跑起来，每张空烧约 10 轮额度且大概率零产出。08-06 就是中途发现后杀掉重起、用 `--ids=5,8,24-582` 绕开，救回约 44 额度。
- 📈 **新卡远比老卡值钱**（08-06 实测）：#5–#8 四张全空白卡平均 42 轮拿 21 张图；#9–#23 那批跑满 120–150 轮的老卡才 17–28 张。同额度产出差 3–4 倍 → 优先喂 rounds=0 的卡（清单里还有 474 张）。
- ⏱ **STALL_ROUNDS=10 验证有效**（默认 20）：08-06 四张卡全是"表层图放完就断供"形态（#8 前 12 轮 13 张、后 10 轮零），没出现代码注释担心的"第 11–20 轮才回血"。10 轮撤退比 20 轮每张省 10 额度。
- 挑卡：`plan-next.mjs` 每跑完一张重算——未 done 且 rounds<150 的卡里，先续在跑的（unlocked 多的优先），再按清单顺序开新卡；单卡单日 +43 轮；额度 215/天，剩 <10 收工。日志全进 `farm-run.log`。
- 旧的手工指定版 `run-until-quota.sh` 保留没删。
- ⚠ **TCC 卡点**：launchd 起的进程默认碰不了 `~/Desktop`（exit 126 / EX_CONFIG）。解法=给 `/bin/bash` 开「完全磁盘访问权限」（2026-07-22 用户拍板选这条）。launchd 自己的 stdout 也不能指向 Desktop，已改到 `~/Library/Logs/auto-clicker-launchd.log`。
- 手动起长跑：**Bash 工具的 run_in_background 现在够用**（08-01 一趟跑到额度耗尽、exit 0，07-22 记的"10 分钟被 SIGTERM"已不复现）+ Monitor tail 日志报进度。
- ⚠ `run-daily.sh` 正在跑时**别编辑它**（bash 按字节偏移续读，会执行错位）——要改逻辑等它收工，或改 `plan-next.mjs`（node 一次性读完，安全）。

**Why:** 用户连着 5 天手动说"可以开始跑了"，这活本身没有每日决策成分。
**How to apply:** 再被问起先看 `farm-run.log` 尾部和 launchd 状态，别默认没在跑；要临时插队直接 `bash run-daily.sh`。
