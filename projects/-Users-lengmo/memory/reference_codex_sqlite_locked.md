---
name: reference_codex_sqlite_locked
description: "codex 报 \"database is locked\" 的真因是有 codex 被 Ctrl+Z 挂起（ps STAT=T）攥着写事务；顺带 logs sqlite 需定期 VACUUM"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 5084dc23-930d-4a1b-ab88-9aeee2523970
  modified: 2026-11-02T06:13:33.497Z
---

codex 启动报 `database is locked (code: 5)`（`~/.codex/state_5.sqlite` / `logs_2.sqlite`）**不是"另一个 codex 在跑"**——codex 多实例本来能共存（几个 `codex mcp-server` 长期并存无事）。

真因：某个终端里的 codex TUI 被 **Ctrl+Z 挂起**了，停在写事务中间永不提交。

**诊断三步**（2026-07-30、08-09 各撞一次）：
1. `ps -eo pid,stat,etime,command | grep '[c]odex'` —— 认 **`STAT = T`**（stopped），不是看有没有 codex 在跑
2. `lsof +d ~/.codex | grep sqlite` —— 确认哪个 PID 攥着（mcp-server 通常不开这些库）
3. `sqlite3 -cmd ".timeout 3000" logs_2.sqlite "begin immediate; select 1; rollback;"` —— 锁被占会返 `database is locked (5)`；读查询不受影响（WAL），别用读来判断

**解法**：`kill -CONT` **单独用没用**——它一读 tty 就吃 SIGTTIN 再次自停。要么去 `ps -o tty` 指出的那个终端 `fg` 后正常退出，要么 `kill -CONT <pid> && kill -TERM <pid>`。

**顺带的清理**：codex 自己按约 10 天保留期删日志行，但 SQLite 删行不还盘。08-09 实测 `logs_2.sqlite` 1741 MB 里 **63% 是 freelist 空洞**，`PRAGMA wal_checkpoint(TRUNCATE); VACUUM;` 回收 1.18 GB 到 559 MB，**零行丢失**（整库 integrity ok）。要独占锁，所以必须先解上面的锁。`sessions/`(791M)、`plugins/`(350M) 是另外的大头，真删才能瘦，动它们照 [[feedback_cleanup_use_trash_not_rm]] 走废纸篓。

**2026-09-10 复跑**：logs_2 又涨回 831M / 48% 空洞，VACUUM → 348M（这是**周期性活**，数字每次不同，别记数字记动作）。`sessions/` 由 launchd `com.lengmo.codex-retention` 每天 04:15 自动清，保留 30 天，先备份到废纸篓，别再手工切；该脚本不做 VACUUM，logs_2 仍要手动。注意 `thread_history_1.sqlite`(1.7G) 是 0% 空洞的真数据，VACUUM 对它无效；1002/1230 个 rollout 已投影进该库，但**删了 jsonl 还能不能 `codex resume` 未验**。


补充：10-08 logs_2 只剩 104M，大头在 sessions 与 app-server 旧版本
