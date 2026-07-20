---
name: project_pageforge_worldcard_testbed_run
description: pageforge 世界卡全流程生码测试在 onlychat-agg-tuning 的当前进度与续跑步骤
metadata: 
  node_type: memory
  type: project
  originSessionId: e5ac1f2a-65d5-4110-881f-3d29eb506e29
---

pageforge v0.0.6 世界卡真跑（onlychat-agg-tuning，分支 lengmo_20260427_spike_agg）：**07-02 晚用户叫停，中断不归零，待续跑**。62 格进行到第 6 格，产物在 `src/__pageforge_out__/` 隔离区。

- **单一真相** = `~/Desktop/cmm/agg/V0.0.6/链路水平评估-2026.07.02.md`（含待结账清单：62格终态/eval分数/成本/缺陷分布/D1，全部待回填）
- 续跑归 session `c75b6e56-a9db-4e91-b122-e559d74d1c80`；续跑命令：`cd ~/Desktop/cmm/onlychat-agg-tuning && /bin/sh .claude/skills/pageforge/scripts/babysit.sh $PWD --no-commit`（--no-commit 硬性）；批量验收前需用户起 `claude --chrome`（D1）
- 完整过程记录（livelock 修复批/停点/改造批 19 项）落档 `agg/V0.0.6/archive/memory迁移-testbed_run-2026.07.06.md`

相关：[[project_codegen_workflow]]
