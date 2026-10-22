---
name: feedback-research-must-writeback
description: 调研/ultracode 的产出必须回写已有资产，不要只产新清单新报告
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9513f580-1b7b-453b-9235-c4e9274897a5
  modified: 2026-10-22T12:46:30.112Z
---

用户抱怨（2026-06-11）：两轮 ultracode 烧了大量 token，产出的是新 agent 清单和新体系设计，"甚至对原有能力都没有优化"——当时 analyzer 审计仅 55/D、事故红线（sf-reader ≤2 并发、内容校验）只活在 memory 不在 SKILL.md 里。

**Why:** 他的核心诉求是"更轻松"，资产变强 > 报告变多；新建议的默认归宿应该是长在现有资产上。**当年的两个缺口都已按这条兑现（2026-09-01 复核）**：学习体系最终没建新 skill，落成了 analyzer 的多源调研模式 + `~/.claude/skills/analyzer/references/research-mode.md`（文件在）；sf-reader 并发红线也已从 memory 搬进 `analyzer/SKILL.md:40`「多 URL 必须串行或 ≤2 并发」和 `:171`「绝不 >2 并发」。这条现在是有判例撑着的规则，不是空口号。

**How to apply:** 调研类 workflow（ultracode/deep-research/agent 选型）收尾必须包含"对已有 skill/agent 的回写清单"；推荐新建任何东西之前先问"能不能并进现有资产"；落地后跑对应审计（meta-check-skill ≥85）。

**边界（2026-09-14 被判「这么改很草率」）：回写清单 ≠ 直接改 PRD / 规格 / 协议文档。** 那次拿一轮论文精读的结论（子 agent 卡片），当场改了 eval-arena PRD01/04/10 并提交 main，结果全部撤回。草率在四处：①依据是论文自造考卷的数字，项目自己的考卷（T158）不在本机、没核就改；②给 PRD10 的 K 组又加了一个变量，违背它「只隔离一个变量」的原则；③新定义里「连续多少次」给不出数，名义上机械判定、实际判不了；④跨期协议文档没读 CONTEXT/ADR、没过开工三问。外部论文的发现一律先写成**候选**，标证据强弱和「动手前先核什么」，核完项目数据再改。skill 文件这类自有工具资产照旧直接回写。

**项目里多路调研 / 子 agent 报告的归宿（2026-10-22 perf-lab 归因层）：** owner 原话「到时候我肯定是根据 docs 里的内容思考如何发展，并不一定是在这个 session 里」。scratchpad 会随会话清掉，所以报告不能只交路径：收尾时把结论写进项目 `docs/` 的总结（含「下一步候选」：价值 / 代价 / 是否换尺子 / 锚点），原始报告按项目证据规则放 `docs/<主题>/evidence/` 并写明来源，待拍板的登记进项目自己的台账（如 open-questions），被改动影响到的活文档（README / PRD / 字典）同步改成现状。文档落在未提交的 worktree 里，别的会话一样看不到，要提醒 owner 提交。相关：[[feedback_inline_over_background_workflow]]、[[feedback_skill_design_pattern]]（meta-check ≥85 那条现居此文件）。
