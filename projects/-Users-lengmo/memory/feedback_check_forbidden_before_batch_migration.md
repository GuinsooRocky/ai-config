---
name: check-forbidden-before-batch-migration
description: 批量跑迁移前必须先查拍板箱有没有被 owner 判死的迁移，只验技术前置不够
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 243bce9a-1376-4308-9452-cb239901cdbf
  modified: 2026-07-26T18:22:17.143Z
---

**批量跑迁移前，除了技术前置，必须先查「产品前置」——拍板箱里有没有哪条迁移被 owner 明令禁跑。**

**事故**（2026-07-27，soliloquy）：跑 48 条待跑迁移前，我核了 pgcrypto 可用、修了 slug parity（两个都是技术前置），**没查 `loop/decisions.md`**。结果第 1 条 `20260723010000_points_membership_renewal.sql` 正是 owner 07-26 拍板推翻 T121 时标明「继续保持不执行」的那条。它往库里装了一个 **每天 0:15 自动用点数给到期会员续卡的 pg_cron 任务**——正是被废掉的行为。发现时距首次触发约 6 小时，0 条流水，没扣到任何人。已 `cron.unschedule` + `drop function` + 迁移文件移废纸篓。

**Why:** `run-migration.ts` 只认「跑没跑过」，**不认「该不该跑」**——被废弃的迁移在它眼里跟正常待跑的一模一样。而「该不该跑」这个信息活在 `loop/decisions.md` / BACKLOG 里，脚本读不到。

**How to apply:**
- 批量跑迁移前，拿待跑清单去 grep 拍板箱与 BACKLOG：`for f in $(cat pending); do grep -l "${f%.sql}" loop/decisions.md docs/prd/*.md; done`，命中的逐条读完再决定
- 一条一条跑、失败即停（`run-migration.ts` 本来就一次一个文件），别写成"全跑完再看结果"
- 跑完立刻查副作用：**特别是 `cron.job`**——定时任务是唯一会「自己再次发生」的东西，其它 DDL 至少是静止的
- owner 的删除偏好：文件走 `~/.Trash` 不 `rm`；删库对象前先 `pg_get_functiondef` 备份一份
- 相关：[[project_soliloquy]]、[[feedback_cleanup_use_trash_not_rm]]
