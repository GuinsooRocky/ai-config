# CLAUDE.md 路由提案（人工过目后自行粘贴，贴完可删本文件）

> 来源：2026-07-06 Fable 5 立法 session。按约定不碰 CLAUDE.md 本体，只出提案。

## 建议粘贴的内容（原样抄，5 行）

建议位置：CLAUDE.md 的「PRD 路由」段之后、「Andrej Karpathy Coding Guidelines」之前。

```markdown
## 模型调度与判断（制度文件，2026-07-06 Fable 立法）

- 派子 agent / 选 model / 验收升降级 → 先读 `~/.claude/model-dispatch.md`
- 拿不准"算不算完成 / 该不该问用户 / 该不该换路" → 查 `~/.claude/judgment-rubrics.md`
- 派工 prompt 直接套 `~/.claude/delegation-templates.md` 的模板（T1 搜索 / T2 实作 / T3 重构 / T4 研究 / T5 审查）
- 改以上制度文件前，先读 `~/.claude/harness-maintenance.md` 的权限分层
```

## 为什么只加这 5 行

- 固定 ~5 行的每 session 开销，换 4 份制度文件的确定性可达（不靠概率性 memory 召回）
- 全文不进 CLAUDE.md：防规则通胀（退化分析见 harness-maintenance.md）

## 不贴的后果

制度文件仍在磁盘上，但未来 session 不知道它们存在——整套立法变死文件。这 5 行是唯一的激活开关。
