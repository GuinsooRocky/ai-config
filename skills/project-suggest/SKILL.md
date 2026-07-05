---
name: project-suggest
description: 把外部信息（AI 新闻 / 竞品 PR / 文章 / 痛点 / issue）转成贴合当前项目实际约定、按优先级排序的改进建议清单——每条都锚到真实文件/契约，不空谈。触发词：给改进建议、项目改进、提点建议、这篇/这个能给项目带来啥、ideas for X、suggest improvements，或直接粘一段新闻/PR/文章说"看看对项目有啥用"。常接在 analyzer 之后（analyzer 抓内容 → project-suggest 转成本项目可执行的改进项）。不用于：开新功能前的设计对齐（用 brainstorm）、把需求落档存盘（那是另一回事）。
---

# project-suggest

把外部信号转成具体的、按优先级排序的建议——每一条都扎根在**当前项目的真实约定和在途工作**里，而不是泛泛而谈。

## 何时使用

- 用户粘了一段 AI 新闻 / 竞品 PR / 博客 / issue，问「这对项目有啥用」「给点改进建议」
- 紧接 `analyzer` 抓完内容后，把抓到的要点转成本项目可执行的改进项
- 用户说「项目改进」「提点建议」「ideas for X」「suggest improvements」

不用于：开新功能前的设计对齐（用 `brainstorm`）、把需求落档存盘（另一回事）。

## Instructions

### Step 1 — 先把项目摸清楚（强制，下笔前必做）

并行读以下文件。不要跳过——忽略它们的建议会被用户直接打回：

- `CLAUDE.md` / `AGENTS.md` / 根 `README.md` —— runtime、包管理器、lint/format、架构规则、被禁工具。任何提案必须合规。
- `docs/designs/`、`docs/rfcs/`、`docs/adrs/`（若有）—— 已有或在途的设计。**不要重复提**已经设计/上线的东西；引用对应文档，只提增量（delta）。
- 项目声明的 `contracts/`、`api/` 等边界层 —— 任何会破坏它的建议都要标出来。
- `skills/**/SKILL.md` 和 `.claude/skills/**/SKILL.md` —— 如果某建议改了某个 skill 文档化的 CLI 或用户可见面，在同一条目里点出需要同步更新的 skill。

如果输入涉及某个子系统（日志、会话、provider、附件等），下笔前也顺手扫一眼源码树里对应模块。

### Step 2 — 读输入上下文

用户会粘贴或指向以下一种或多种：

- AI 新闻摘要 / Twitter weekly
- 竞品发布、PR、博客文章
- 原始想法、痛点、抱怨
- bug 报告、issue 串
- 其他任何东西

从中抽出具体的**信号（signal）**——具体引文、日期、指标或行为——而不是模糊的感觉。没有可追溯信号的建议没用。

### Step 3 — 生成建议

产出一份**按优先级排序的清单**。每条用以下固定结构：

```
## N. <简短标题> (urgency: P0 / P1 / P2)

**Signal**：<1–3 句引用来源——日期、谁说的、具体事实。尽量给链接或原文引用。>

**Project impact**：<结合本项目架构，为什么这事对本项目重要。引用它触碰的真实模块 / 文件 / 契约。>

**Action**：<具体改动。点名要动的文件或契约。多步工程就先列能解锁后续的最小第一步。提及 CLAUDE.md / AGENTS.md 里影响做法的约定。>
```

清单规则：

1. **按 urgency 排序**，不按主题。P0 = 有时限的外部压力（政策变化、安全、上游 breaking）。P1 = 明确的用户痛点或竞品差距。P2 = nice-to-have / 战略性。
2. **主清单最多 6 条**。超过用户一条都不会动。更弱的放进简短的「Secondary / watch」尾巴。
3. **不重复提已有设计文档 / RFC / ADR** —— 已覆盖就说一声，只提 delta。
4. **遵守架构规则**（包边界、被禁依赖、type-only import 等）。
5. **摆出 tradeoff**：如果某 action 有真实代价（重构面积、性能、vendor lock-in），在 Action 里一句话说清。
6. **文件要具体**：写 `src/feature/foo.ts`，别写「feature 层」。用户没确认路径时可以推测，但标注是推测。
7. **自检后再交**：每条建议过两问——点名的文件真实存在吗？和已有 RFC/设计文档重复吗？过不了的删掉或标注。

### Step 4 — 收尾给下一步指引

用一两句话收尾：从哪条开始、为什么，并主动提议深入某一条（读对应模块，给更细的改动计划）。**不要开始写代码**——本 skill 产出提案，不产出补丁。

## 示例输出

```
## 1. 把 fetch 缓存策略显式化 (urgency: P1)

**Signal**：Next.js 15（2024-10 发布）默认 fetch 不再缓存，GET Route Handler 也不再静态化。

**Project impact**：本项目 `src/app/api/feed/route.ts` 依赖旧的隐式缓存，升级后会每请求打后端，QPS 翻倍。

**Action**：给该 route 显式加 `export const dynamic = 'force-static'` 或在 fetch 上加 `next: { revalidate }`。先改 feed 这条最高频的，其余按访问量排队。tradeoff：force-static 会让数据有最长 revalidate 的延迟。

---

## 2. ...（最多 6 条）

### Secondary / watch
- <更弱的项，一行一条>

> 建议从第 1 条开始（升级会直接打挂线上）。要我读 `src/app/api/feed/route.ts` 给细化改动计划吗？
```

## Output language

跟随用户语言。用户写中文就用中文回（代码符号、文件路径、专有名词保留英文）。

## Anti-patterns to avoid

- 模糊建议（「提升性能」「加测试」）没有文件/契约锚点。
- 推荐项目 `CLAUDE.md` / `AGENTS.md` 明令禁止的工具或依赖。
- 没读就重复提已有设计文档 / RFC / ADR。
- 灌水凑条数装全面。
- 把「因为新闻是最近的」当成 urgency——recency ≠ urgency。半年前的架构债可以压过一个花哨的新发布。
