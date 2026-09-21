---
name: anthropic-distill
description: 增量蒸馏 anthropic.com 官方文章（news/engineering/research）成固定 schema 卡片，跨篇合出「主线/口径变化/张力」，再逐条对照 soliloquy 判定已对齐·相悖·空白机会。触发词："蒸馏 anthropic"、"anthropic 蒸馏"、"anthropic 最近发了什么"、"跑一下情报蒸馏"、"anthropic 主线"、"更新主线"、"跟 anthropic 方向对齐"、"soliloquy 方向对照"、"anthropic-distill"。不用于：一次性抓某几篇给定 URL 做要点分析（归 analyzer）、单次外部信息转项目改进建议（归 project-suggest）、开放议题深挖（归 deep-research）、近 30 天全网动态盘点（归 firecrawl 搜索 / deep-research）。
---

# Anthropic 蒸馏

把 anthropic.com（news/engineering/research）和 claude.com/blog（工程实践类的现主场）
的官方文章沉淀成**可跨时间比对**的情报库，再拿它照 soliloquy 的方向。

数据目录（下称 `DATA`）：`~/Desktop/archives/anthropic-distill/`（跨项目知识资产，
落 archives 进 Obsidian 回看层；不放 soliloquy 仓——那里只放跟项目决策绑定的东西）

```
DATA/
├── state.json          已蒸馏 slug 清单（增量的依据，脚本维护，别手改）
├── cards/              一篇一张卡
├── 主线.md              跨篇合并结果，每次覆盖重写
└── 对照-YYYY-MM-DD.md   对 soliloquy 的判定，每次新建
```

## 何时使用

- 定期（建议两周一次）跑一轮增量蒸馏
- 想知道 Anthropic 反复在押什么、口径什么时候变过
- 要给 soliloquy 拍方向，想先看跟 Anthropic 的主线是否打架

不该用它的场合看 frontmatter 的负面边界。**非 soliloquy 项目不要用**——对照层的判据和落盘路径
都焊死在 soliloquy 上了。

## 三个模式

用户没指定就跑 **A → B → C 全程**。说「只更新一下」跑 A，说「看主线」跑 B，说「对照 soliloquy」跑 C。

### 模式 A — 增量蒸馏

**步骤 1** — 列出未蒸馏的文章：

```bash
python3 ~/.claude/skills/anthropic-distill/scripts/fetch-index.py --limit 15
```

首次使用且不想回溯全部历史时，先建基线：`--mark-all-read`，之后只蒸馏新增的。

**步骤 2** — 必须先按相关度粗筛一遍：soliloquy 方向之外，claude.com/blog 里的
Claude Code / harness / eval 工程实践文也算相关（owner 的工作方式资产）。合作公告、
政策表态、经济指数、客户案例这类，**用 `--skip --commit <slug> ...` 记为有意跳过**，
不深读不写卡。不筛就会把预算烧在公关稿上。

**步骤 3** — 派子 agent 蒸馏，并行扇出，每个 agent 塞 2 篇摊薄开销。
派工 prompt 只需一句：`Read ~/.claude/skills/anthropic-distill/ref/distill-prompt.md
并严格按它执行` + 逐篇给 url/slug/section/date/title（后两项可空）。
子 agent 只回状态行，主对话不收全文也不收卡片正文。

**步骤 4** — 卡片落盘后再记账：

```bash
python3 ~/.claude/skills/anthropic-distill/scripts/fetch-index.py --commit <slug> <slug> ...
python3 ~/.claude/skills/anthropic-distill/scripts/fetch-index.py --check   # 收尾必跑：抓「记了账没落卡」
```

**顺序不能反。** 先 commit 后蒸馏的话，中途失败那几篇就永久漏掉了——脚本再也不会列出它们。
`--check` 红了 = 有 slug 处于这种蒸发态，当场补卡或改记 `--skip --commit`。

### 模式 B — 一致性合并

**步骤 1** — Read `ref/synthesis.md`。
**步骤 2** — 读 `cards/` 全部卡片，覆盖重写 `主线.md`。四节必须齐：主线 / 口径变化 / 张力 / 孤点。

### 模式 C — 对照 soliloquy

**步骤 1** — Read `ref/synthesis.md`（同一份，看模式 C 那半）。
**步骤 2** — 读 `主线.md` + soliloquy 的 `docs/prd/PRODUCT.md`、`REDLINES.md`、`BACKLOG.md`。
**步骤 3** — 产出 `对照-YYYY-MM-DD.md`，每条主线判定：已对齐 / 相悖 / 空白机会 / 不适用。
判定必须引 soliloquy 里真实存在的东西，引不出来标【无依据·待查】。
细则和四条硬约束在 `ref/synthesis.md`，动笔前必须读。

## 输出约束

- 卡片 schema 一个字段都不能改。schema 漂移 = 那批卡片在后续合并里作废。
- `主线.md` 覆盖重写，不追加、不留「本次新增」之类的过程叙事。
- 对照文件每次新建带日期，保留历史——方向判断的变化本身是有价值的记录。
- 回主对话只报：新蒸馏 N 篇 / 主线有无变化 / 对照结论里最值得看的 2-3 条。全文在文件里。

## 示例输出

一张真实卡片的样子（节选自首跑产物 `cards/2026-03-24-harness-design-long-running-apps.md`）：

```md
## 主张
agent 的能力上限不在模型自己身上，而在有没有一个跟它分家、被专门调教得刻薄的评审 agent——
让干活的 agent 自评永远抬不动质量。

## 押的赌注
- 赌「主观品质可以被写成评分标准」：靠四条 criteria + few-shot 校准就能变成可反复驱动生成的信号。

## 证据类型
实验数据 / 内部实践 / 立场声明

## 复现术语
generator / evaluator / planner, context anxiety, compaction, handoff artifact, load-bearing
```

注意示例里的形状：主张是**可被反驳的断言**（不是「介绍了……」），术语是**英文原文照抄**。
新卡片长得不像这个形状就是写错了。

## 反模式

1. **硬凑可迁移点。** Anthropic 多数文章跟消费级陪伴产品无关，无关就写「无」。
   凑数会让主线库注水，几轮之后整套东西就没人信了。

2. **把「一致性」做成「模仿」。** owner 要的是方向上不打架，不是跟着 Anthropic 做。
   soliloquy 有意选的反向路线（例：公开面不按成人分级过滤，owner 已拍板）标成
   【相悖·有意为之】，不是待修的 bug。

3. **先 commit 后蒸馏。** 见模式 A 第 4 步——会造成永久漏读，且不报错。

4. **自动改 BACKLOG.md。** 只产出建议文件，进不进需求库是 owner 拍板。

5. **索引页当成全量。** 三个板块的索引页只覆盖首屏（约 26 篇），长期不跑会漏中间的。
   隔太久没跑就明说「可能有漏，中间段要补得手动翻」，别假装覆盖完整。

6. **脚本报 0 条就当没新文章。** 脚本在某板块解析出 0 条时会 FATAL 退出——那是站点改版
   打断了正则，去修 `parse()`，不是「这周没更新」。

## Codex compatibility

Preserve this workflow's intent and evidence rules. Translate Claude-specific tool names to the available Codex tools.
