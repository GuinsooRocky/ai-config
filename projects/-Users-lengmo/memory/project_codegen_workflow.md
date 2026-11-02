---
name: project-codegen-workflow
description: "前端生码工作流：统一叫 pageforge — 旧版(≤v0.0.5,批处理流水线) → 新版(v0.0.6+,中间形态=契约账本机CLM,主线)；含\"100 分\"成功判据与挂起的世界卡测试跑现场。工作名 Loom 已被用户弃用"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3b3ea1c7-ced1-4474-84aa-d82100f7fb7c
  modified: 2026-11-02T06:13:18.890Z
---

前端生码工作流统一叫 **pageforge**（工作名 Loom 已弃用 2026-05-29）：旧版 ≤v0.0.5（多 agent 切片流水线，已定性架构选型错）→ 新版 v0.0.6+（契约账本机 CLM，单 agent 串行 + 确定性闸，主线）。

- **权威设计** = `~/Desktop/cmm/agg/V0.0.6/README.md`；当前没有现成测试床，skill 正源在 agg/V0.0.6/skills/pageforge
- **⭐100 分判据**（对新旧版都适用）：① PRD 实现 ② Figma 还原 ③ 接口接通+能跑通 ④ 逻辑与正确实现对照得上；埋点/i18n 不计分；验收=真跑不是自评分
- **铁律**（2026-06-01 用户拍）：tsc 过 ≠ 需求完成；没写 = 真没做；eval 看 logicScore 当头条
- 战报/复盘细节：`agg/V0.0.6/链路水平评估-2026.07.02.md` + `archive/memory迁移-codegen_workflow-2026.07.06.md`（原 79 行 memory 全文落档处）
- **灵感 inbox**：新看到的 agent/生码灵感文章先进 `agg/V0.0.6/参考与灵感.md`（📥 待消化 / 🔬 在评估 / ✅ 已整合 / ❌ 否决 的状态约定 + 每条格式，**规则全文就写在该文件头部，照它执行**），成熟才抽进 README。V0.0.6 设计文档可编辑，与 [[feedback_agg_readonly]] 不冲突（那条管 worktree 代码回流）。⚠ 已知漂移：文件里 "✅→README §1.7/§3.4" 类锚点解析不到——现行 `V0.0.6/README.md` 只有 `## 0.`–`## 12.` 十三个二级标题，没有 § 子锚，下次动 agg 时顺手校。

## 世界卡测试跑（挂起）

- pageforge v0.0.6 世界卡真跑 07-02 被用户叫停，中断不归零。账本 62 格：39 READY / 16 OPEN / 7 SETTLED，答卷 104 文件。
- 测试床 worktree 已回收，当前没有现成测试床。现场封存在 `~/Desktop/cmm/agg/V0.0.6/worldcard-run-20260706/`（账本/progress/node-view/答卷/预览路由/PRD 输入）。
- 旧分支 `lengmo_20260427_spike_agg` 已不存在，封存目录 README 第 38 行的还原配方跑不了（agg 只读，配方留着不改）。**续跑从封存目录重建，先定一条新基线分支。**
- **单一真相** = `agg/V0.0.6/链路水平评估-2026.07.02.md`（待结账六条：62格终态/eval分数/成本/B2断言/缺陷分布/D1，全部待回填）。
- 这六条结的是机制的账，不是 onlychat 的功能交付：onlychat 上已上线的世界卡实现是本跑的 gold（标准答案，反作弊禁读），生码答卷永不进 onlychat，只当打分材料。评分器与题面在 `agg/eval/{scorer,cases}`。
- 跑批命令 `babysit.sh $PWD --no-commit`（--no-commit 硬性）；批量验收前需用户起 `claude --chrome`（D1）。
- 完整过程记录落档 `agg/V0.0.6/archive/memory迁移-testbed_run-2026.07.06.md`。

相关：[[feedback_agg_readonly]]


补充：pageforge（Loom 已弃用）：旧版≤005 → 006+ CLM 主线；权威=agg/V0.0.6/README；⭐100分判据、「tsc过≠需求完成」、灵感 inbox 规则在条目内；战报已落 archive/
