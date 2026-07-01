---
name: feedback-research-must-writeback
description: 调研/ultracode 的产出必须回写已有资产，不要只产新清单新报告
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9513f580-1b7b-453b-9235-c4e9274897a5
---

用户抱怨（2026-06-11）：两轮 ultracode 烧了大量 token，产出的是新 agent 清单和新体系设计，"甚至对原有能力都没有优化"——当时 analyzer 审计仅 55/D、事故红线（sf-reader ≤2 并发、内容校验）只活在 memory 不在 SKILL.md 里。

**Why:** 他的核心诉求是"更轻松"，资产变强 > 报告变多；新建议的默认归宿应该是长在现有资产上（先例：学习体系最终没建新 skill，落成了 analyzer 的多源调研模式 + references/research-mode.md）。

**How to apply:** 调研类 workflow（ultracode/deep-research/agent 选型）收尾必须包含"对已有 skill/agent 的回写清单"；推荐新建任何东西之前先问"能不能并进现有资产"；落地后跑对应审计（meta-check-skill ≥85）。相关：[[feedback-inline-over-background-workflow]]、[[feedback-skill-dogfood-metacheck]]。
