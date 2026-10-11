---
name: project_soliloquy_bugscan_20261011
description: 2026-10-11 soliloquy 全仓捉虫（28 路猎手 + 27 路对抗）结果位置、结论要点与下一步；修复尚未开始、5 件待 owner 拍板
metadata:
  type: project
---

**位置**：`~/Desktop/loop_project/soliloquy-bugscan-20261011/`——`FINAL.md`（结论，唯一真相）、`reports/<分区>.md` + `.adv.md`（逐条原文）、`reports/DIGEST*.md`（裁决用摘要，三份）、`reports/QUALITY.md`（质量备注汇总）、`reports/AGGREGATE.md`（机器合并表，`tools/aggregate.py` 生成）、`BRIEF.md` / `ADV_BRIEF.md` / `SEAMS.md`（可复用的简报）。扫描基线 `origin/main 71c3c21e0`；只读 worktree `repo/` 在分支 `lengmo_20261011_fix_bugscan`（无 upstream，依赖已离线装好），**修复就在这个 worktree 上做**。

**结论要点**：150 条经对抗；P0 无；P1 19 条 = 18 个根因（13 个生产现在就能碰到），P2 126，推翻 5。最先修：卡审核守卫 `search_tsv`（db2-1）、删卡两条后果（seamA-1 + db1-2）、Telegram 付费档失败（seamB-1）、BYOK Anthropic 失败（server2-1）；修政策文本前先修 db1-1 / db1-ADV-1。

**下一步（owner 还没拍）**：是否按 eval-arena 那套三波并行修（每路独立审查）；FINAL §F 列了 5 件先拍板的事（政策暂停发版、无 OC 会话分级、截断扣不扣点、R2 改投聊天图、清卡脚本去留）。修复顺序按 §G 同根组排，修完要做 §F 的盘点。

**Why:** owner 10-11 要求「对整个 soliloquy 做代码捉虫，无论前后端，多路并行」。
**How to apply:** 接到「修 soliloquy 的 bug / 继续捉虫后续」先读 FINAL.md §结论 + §F，别重扫。画布分支扫描期间已合进 main（e5ec727b9），canvas1 的发现现在 main 上也有。相关：[[parallel-subagent-fix-pipeline]]、[[project_soliloquy]]
