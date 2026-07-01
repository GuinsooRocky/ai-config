---
name: agg 目录只读规则
description: agg/ 只用于记录和查看，不要把 worktree 的改动反向同步回 agg/
type: feedback
originSessionId: 3ab28d87-c5e3-4feb-b32e-aa067280ae34
---
`~/Desktop/cmm/agg/` 是只读参考目录，只接受：
- `agg/evolution/` 下的 evolution 记录（用户说"记录"/"落 evolution"时写）
- `agg/真实需求落档/` 下的需求落档（用户说"落档"时写）

**不要把 worktree 里的 agent / skill 改动同步回 agg/**。worktree 是实验工作区，改动不自动升格到 agg 源。

**Why:** 2026-04-28 用户明确纠正——"agg 只用来做记录跟查看"。

**How to apply:**
- 改了 `.claude/agents/` 或 `.claude/skills/` 里的文件 → 不 cp 到 agg/
- 只有用户显式说"同步到 agg"/"固化进 agg"才操作
