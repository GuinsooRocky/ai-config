---
name: skill-dogfood-metacheck
description: 新建或大改 ~/.claude/skills/ 下的 skill 后，必须立即跑 meta-check-skill 自审
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 53890fbf-af4b-498e-b50b-61bfc0ff92e2
---

新建一个 skill、或对现有 skill 做多轮编辑后，**必须立即跑一次 `meta-check-skill` 自审**（`python3 ~/.claude/skills/meta-check-skill/ref/audit.py <name>`），通过（≥85）才算交付完成。

**Why:** 2026-05-15 手写 `skill-upstream-diff` 时没用现成元 skill 流程，多轮迭代中改了「输出策略」却没回头同步「不做什么」「配套文件清单」，产生 3 处 drift（含一处自相矛盾的指令、一处指向不存在文件）。跑 meta-check-skill 在交付前抓出来了，否则会流到用户首次使用时才暴露。用户当时质疑"写这个 skill 用 write-a-skill 了吗" —— 正是这个疏漏。

**How to apply:** 写完/大改 skill 的最后一步固定是跑 meta-check-skill。多轮编辑尤其危险——改一处容易忘了同步其他处（drift）。审计重点看 Drift 维度（引用路径是否存在、章节间指令是否一致）。相关：[[feedback_skill_design_pattern]]。
