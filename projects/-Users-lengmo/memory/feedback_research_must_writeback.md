---
name: feedback-research-must-writeback
description: 调研/ultracode 的产出必须回写已有资产，不要只产新清单新报告
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9513f580-1b7b-453b-9235-c4e9274897a5
  modified: 2026-09-14T11:29:29.501Z
---

用户抱怨（2026-06-11）：两轮 ultracode 烧了大量 token，产出的是新 agent 清单和新体系设计，"甚至对原有能力都没有优化"——当时 analyzer 审计仅 55/D、事故红线（sf-reader ≤2 并发、内容校验）只活在 memory 不在 SKILL.md 里。

**Why:** 他的核心诉求是"更轻松"，资产变强 > 报告变多；新建议的默认归宿应该是长在现有资产上。**当年的两个缺口都已按这条兑现（2026-09-01 复核）**：学习体系最终没建新 skill，落成了 analyzer 的多源调研模式 + `~/.claude/skills/analyzer/references/research-mode.md`（文件在）；sf-reader 并发红线也已从 memory 搬进 `analyzer/SKILL.md:40`「多 URL 必须串行或 ≤2 并发」和 `:171`「绝不 >2 并发」。这条现在是有判例撑着的规则，不是空口号。

**How to apply:** 调研类 workflow（ultracode/deep-research/agent 选型）收尾必须包含"对已有 skill/agent 的回写清单"；推荐新建任何东西之前先问"能不能并进现有资产"；落地后跑对应审计（meta-check-skill ≥85）。

**边界（2026-09-14 被判「这么改很草率」）：回写清单 ≠ 直接改 PRD / 规格 / 协议文档。** 那次拿一轮论文精读的结论（子 agent 卡片），当场改了 eval-arena PRD01/04/10 并提交 main，结果全部撤回。草率在四处：①依据是论文自造考卷的数字，项目自己的考卷（T158）不在本机、没核就改；②给 PRD10 的 K 组又加了一个变量，违背它「只隔离一个变量」的原则；③新定义里「连续多少次」给不出数，名义上机械判定、实际判不了；④跨期协议文档没读 CONTEXT/ADR、没过开工三问。外部论文的发现一律先写成**候选**，标证据强弱和「动手前先核什么」，核完项目数据再改。skill 文件这类自有工具资产照旧直接回写。相关：[[feedback_inline_over_background_workflow]]、[[feedback_skill_design_pattern]]（meta-check ≥85 那条现居此文件）。
