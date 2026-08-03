---
name: write-a-skill
description: 新建或大改一个 agent skill——按官方 frontmatter 字段表写 SKILL.md、切分 reference 文件、配套脚本，写完必须跑 meta-check-skill 自审到 ≥85 才算交付。触发词："写个 skill"、"新建 skill"、"做一个 skill"、"把这个流程做成 skill"、"改一下这个 skill"、"create a skill"、"/write-a-skill"。不用于：审已有 skill 的质量打分（归 meta-check-skill）、从对话记录里挖 skill 候选（归 meta-skill-mining）、写给别的 session 执行的一次性 prompt（归 write-a-prompt）、建 agent 或 workflow（skill 只管 skill）。
---

# 写 Skill

把一个反复做的流程固化成 skill。产出必须过量具（`meta-check-skill`），不是写完就算。

## 何时使用

- 用户说「写个 skill」「新建 skill」「把这个流程做成 skill」「改一下这个 skill」
- 某个流程你已经重复手动跑过三次以上，值得固化
- **不**用于：给已有 skill 打分（`meta-check-skill`）、从对话记录挖候选（`meta-skill-mining`）、写一次性 prompt（`write-a-prompt`）

## 步骤 1 — 问清楚

先拿到这四项，缺哪项补哪项，别自己脑补：

- 覆盖什么任务/领域？边界在哪（什么情况**不**该用它）？
- 用户会怎么开口叫它？至少收集 3 种真实说法。
- 需要确定性脚本，还是纯指令就够？
- 有没有现成参考材料要打包进去？

## 步骤 2 — 先查有没有重复

`ls ~/.claude/skills/` 扫一遍。跟现有 skill 重叠就长在它上面（加一节），别新建第二个。新能力优先扩现有 skill。

## 步骤 3 — 写 SKILL.md

照下面的模板和字段表。

## 步骤 4 — 自审

跑量具，`< 85` 就改到过线：

```bash
python3 ~/.claude/skills/meta-check-skill/ref/audit.py <skill-name>
```

## 步骤 5 — 交回用户

报路径 + 分数 + 还剩哪些扣分项没修（如果有）。

## Frontmatter 字段表

官方支持 15 个字段，**任何不在表里的字段都算非法**：

`name` `description` `when_to_use` `argument-hint` `arguments` `disable-model-invocation` `user-invocable` `allowed-tools` `model` `effort` `context` `agent` `hooks` `paths` `shell`

日常只需要三个：

| 字段 | 何时写 |
|---|---|
| `name` | 必填，**必须跟目录名完全一致** |
| `description` | 必填，见下节 |
| `disable-model-invocation: true` | 只想手动 `/xxx` 调用、不许模型自动选中时 |

## description 是唯一的入口

模型选 skill 时**只看得到 description**，正文一个字都看不到。写砸了这个 skill 就永远不会被触发。

硬约束：

- **必须单行**。frontmatter 解析是简化版 YAML，`description: >` 多行写法会丢内容。
- **堆触发词**，列 ≥3 种真实说法（中英文都列），别指望模型自己泛化。
- **必须有负面边界**——「不用于 X（归 <another-skill>）」。这是防误触发的唯一手段，也是本机所有自有 skill 的统一惯例。
- 长度：单字段不死卡，但 `description + when_to_use` 合计 >1536 字会被官方 listing 截断。太短（<40 字）则触发词堆不够，也会扣分。

**正例**（能做什么 + 怎么叫它 + 什么时候别用它，三段齐全）：

```
把本地 HTML/Markdown 发布到内网 Pages 服务，返回可分享 URL。触发词："发布到内网页面"、"用 pages 发布这个 html"、"更新已发布的页面"。不用于：发公网页面（归 Artifact）、纯文件传输。
```

**反例**：`Helps with documents.` —— 模型没法把它跟其它文档类 skill 区分开。

## SKILL.md 模板

```md
---
name: skill-name
description: 做什么。触发词："..."、"..."、"..."。不用于：X（归 other-skill）。
---

# Skill Name

## 何时使用
[前置触发场景，和不该用的边界]

## 执行步骤
[分步骤，每步可验证]

## 输出约束
[格式硬要求]

## 反模式
[已知会做错的地方，逐条写清"错在哪 → 该怎么做"]
```

## 目录结构

```
skill-name/
├── SKILL.md        # 主指令（必需）
├── ref/            # 按需加载的细则、词典、样例
└── scripts/        # 确定性脚本
```

**渐进披露**：SKILL.md 只放每次都要读的东西；细则塞 `ref/`，在正文里写清「什么情况下才 Read 它」。引用只下钻一层，别套娃。

## 拆分与脚本的判据

**拆到 ref/**：SKILL.md 超 500 行；内容分属不同域（各自独立使用）；高级用法极少触发。

**写脚本**：操作是确定性的（校验、格式化、统计）；同样的代码会被反复生成；错误需要显式处理。脚本比让模型现场生成代码更省 token、更可靠。

## 反模式

1. **写完不跑量具**——`meta-check-skill` 是交付门槛，不是可选项。本机铁律：新建/大改必须自审到 ≥85。
2. **description 不写边界**——只写「能干什么」不写「什么时候别用」，结果跟邻近 skill 抢触发。
3. **触发词只写一种说法**——用户实际会换十种词，只列一种等于没列。
4. **重复造**——已有 skill 能覆盖就去扩它。新建前必须先 `ls ~/.claude/skills/`。
5. **写时效性内容**——「目前最新版本是 X」这类句子几个月后就是错的，别写进 skill。
6. **术语不统一**——同一个概念在文档里换三个叫法，模型会当成三件事。
