# Claude 全局工作指南

## Git 偏好

- Git 同步分支用 rebase（详见 memory: feedback_rebase_over_merge.md）

---

## 删除/清理

- 帮删文件一律 `mv` 到 `~/.Trash`，**绝不 `rm`**（即使用户已批准）——保持可逆（详见 memory: feedback_cleanup_use_trash_not_rm.md）

---

## 笔记存放约定

- **触发词**：用户说"存学习笔记"/"记一下"/"保存笔记" → 写到 `/Users/lengmo/Desktop/archives/技术总结/`
- **文件名**：`MM.DD-<简短标题>.md`（例：`04.20-Agent-Loop-四框架设计.md`）
- **写完告知**：报路径 + 提醒"可拖入有道云笔记 技术总结 文件夹"
- **理由**：有道云笔记数据加密封闭，无法自动导入，约定本地暂存后手动拖拽
- **别跟"落档"混**：触发词"落档"= 真实需求落档 → `~/Desktop/cmm/agg/真实需求落档/`（详见 memory: feedback_real_requirement_archive.md）

---

## PRD 路由（说"PRD"先分诊，别赌触发词）

- 审 PRD 本身（矛盾/缺文案/反讲）→ `onlychat-prd-reflection`
- 查代码注释跟 PRD 同没同步（§X.X anchor）→ `cmm-drift-prd`
- 拿方案对照 PRD 逐点拷问 → `/grill-with-prd`（手动）；无 PRD → `grill-me`
- 生码成品验收打分 → 全链路（含造数据+走查）用 `pageforge-accept-pipeline`；报告已齐只打分用 `pageforge-acceptance-judge`
- 裸"对一下 PRD/看下 PRD"意图不明 → 先反问 a审本身 / b查drift / c拷问方案，别乱选

---

## Andrej Karpathy Coding Guidelines

Behavioral guidelines to reduce common LLM coding mistakes.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- When presenting interpretations: lead with ONE recommendation and proceed; only stop and ask if the fork is irreversible.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

@RTK.md
