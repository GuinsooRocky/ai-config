---
name: project_pageforge_inspiration_inbox
description: pageforge/agg 新的 agent/生码灵感文章 → 先进 agg/V0.0.6/参考与灵感.md inbox，成熟才抽进 README
metadata: 
  node_type: memory
  type: project
  originSessionId: 0590145b-3152-430f-9bd9-892656e6b45f
---

用户分享 agent / 生码（codegen）类文章或项目当 pageforge 灵感时，**默认流程**：

1. 先落进 `~/Desktop/cmm/agg/V0.0.6/参考与灵感.md`（inbox），状态标 📥；每条用统一格式：标题/出处 · 核心论点 · 拿走 · 避开 · 在 pageforge 的位置 · 状态。
2. 评估成熟 → **抽进 `V0.0.6/README.md`**（§1 参照系新增一条 + §3/§5 落点下沉具体补丁），inbox 里改标 ✅ 并指到 README §x。
3. 不适用 → 标 ❌ 并写明否决理由（留教训，防未来手贱再加回来）。

**Why**：README §1「六个参照系」是奠基期调研、已织进设计；inbox 是它之后的持续进料口，避免每来一条都撑大 README。

**How to apply**：① 别再一上来就直接往 README 写；先进 inbox。② V0.0.6 的设计文档（README + 参考与灵感.md）是**可编辑**的——这跟 [[feedback_agg_readonly]]（agg 只读、只收 evolution/落档、不反向同步 worktree 代码）不冲突：那条管的是 worktree 的 agent/skill 代码改动，不是 pageforge 自己的设计文档。

样例已建：防幻觉文章（代码随想录）走完了完整生命周期 = README §1.7 + §3.4/§3.6/§3.8 三补丁 + 一条否决（失败样本回灌回归集→会膨胀/腐烂/过拟合）。

相关：[[project_pageforge_v006]]
