---
name: project_pageforge_worldcard_testbed_run
description: pageforge 世界卡生码测试跑的现场已封存进 agg，续跑要先还原 worktree
metadata: 
  node_type: memory
  type: project
  originSessionId: e5ac1f2a-65d5-4110-881f-3d29eb506e29
  modified: 2026-08-03T09:45:44.069Z
---

pageforge v0.0.6 世界卡真跑：**07-02 晚用户叫停，中断不归零，待续跑**。62 格账本 39 READY/16 OPEN/7 SETTLED，答卷 104 文件。

**2026-08-03 现场已封存**：worktree `onlychat-agg-tuning` 回收（进废纸篓 + `git worktree prune`），运行状态搬到 `~/Desktop/cmm/agg/V0.0.6/worldcard-run-20260706/`（5.7M：账本/progress/node-view/答卷/预览路由/PRD 输入）。**续跑不能直接跑了，要先照该目录 README 还原成 worktree**（`git worktree add ../onlychat-agg-tuning lengmo_20260427_spike_agg` + pnpm i + rsync 回现场），分支还在 onlychat 本地。

- **单一真相** = `agg/V0.0.6/链路水平评估-2026.07.02.md`（待结账六条：62格终态/eval分数/成本/B2断言/缺陷分布/D1，全部待回填）
- **这六条结的都是机制的账，不是 onlychat 的功能交付** —— onlychat 上已上线的世界卡实现是本跑的 gold（标准答案，反作弊禁读），生码答卷永不进 onlychat，只当打分材料。评分器与题面在 `agg/eval/{scorer,cases}`
- 续跑归 session `c75b6e56-a9db-4e91-b122-e559d74d1c80`；跑批命令 `babysit.sh $PWD --no-commit`（--no-commit 硬性）；批量验收前需用户起 `claude --chrome`（D1）
- 完整过程记录（livelock 修复批/停点/改造批 19 项）落档 `agg/V0.0.6/archive/memory迁移-testbed_run-2026.07.06.md`

相关：[[project_codegen_workflow]]
