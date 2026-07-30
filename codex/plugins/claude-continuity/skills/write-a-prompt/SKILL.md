---
name: write-a-prompt
description: Create or improve a high-quality prompt for another agent or session.
  Use when the user asks to write, generate, or optimize a prompt that someone else
  will execute.
---

# Write-a-Prompt

把「我要一份 prompt」变成一份**执行方拿去就能干、且不会被过期信息带沟里**的 prompt。产出是可复制的 prompt 文本，不是替用户把活干了。

## 何时使用

- 用户说「生成 / 写个 / 帮我出个 prompt」「优化这个 prompt」「promort」，或 `/write-a-prompt`。
- 交付物**必须**是 prompt 本身（贴给别的 session / 别人跑）。

**负边界（别抢）**：对象是文章/稿子 → 归 xhs-writer；对象是 skill → 归 write-a-skill；是聊设计不是产 prompt → 归 brainstorm。区分只认一条：**对象词是不是 prompt/promort**，不认「帮我写」这种裸动词。

> 用户在任务里顺口要 prompt、没说触发词时，本 skill 不 fire —— 那种情况直接手动过下面的质量线即可，别硬唤。

## 质量线（6 条，每次逐条过，别临场发挥）

1. **角色 + 硬规则**：prompt 开头给执行方定角色，规则写成「违反即失败」的失败条件，不是软建议。
2. **焊入真实上下文**：这是「通用 prompt」和「懂用户世界的 prompt」最大的差距，也是用户能感知的质量主因。**必须**实时收（见 Step 2），绝不凭记忆脑补。
3. **输出契约**：产出写到哪、什么结构、「对话里只回什么」、锚 `文件:行号`。
4. **内建优先级**：涉及多项时给 P0/P1/P2，按收益×成本排，标出「哪些不值得做」。
5. **可逆护栏**：默认只读 / 先 diff，匹配用户 surgical 习惯；对外/不可逆动作写成需确认。
6. **填空位**：项目 / 目标等参数留 `____`，绝不替用户猜。

## 执行步骤

### Step 1 — 补齐意图（缺就先反问一句）

产 prompt 前确认 4 要素齐不齐：**目标**（干成什么）/ **谁跑它**（主 session？子 agent？有无浏览器工具）/ **成功长啥样**（输出什么、写哪、怎么算完）/ **绝不做什么**（红线）。缺任一条**必须**先反问，别硬编。

### Step 2 — 实时收三层上下文

1. **对话上下文**：本会话已聊到的意图。
2. **偏好上下文**：**实时** `Read ~/.claude/projects/-Users-lengmo/memory/MEMORY.md`，从索引挑出跟写 prompt 相关的 `feedback_*`（单行 description、别用黑话、surgical 只读、表格给结构化内容等），只读那几条正文再应用。**绝不**把偏好写死进本 skill —— memory 天天变，读索引才跟得上。
3. **代码/项目上下文**（功能类 prompt 才需要）：Grep/Read 定位相关文件、函数、契约、要对齐的现有模式。

### Step 3 — 分「耐久锚点」vs「易变细节」（放错机制）

功能类 prompt 的核心风险：现在读的代码是快照，贴过去执行时可能**已被改动或本次就查漏了**。所以：

- **耐久锚点**（哪些文件相关、架构/契约、要遵循的模式、约束）→ 直接焊进 prompt。
- **易变细节**（具体行号、当前签名）→ **禁止**当 ground truth 写死；写成「起点，执行前先核」，并让生成的 prompt **第一步**就是「重读 X/Y 确认这些假设还成立，漂了就停下重划范围」。
- **置信度**：本次查得不确定的地方一律明标「疑似在 …，请确认」，绝不把晃悠的读取伪装成确定。

核实**必须**发生在执行的 session（只有那一刻才看得到别人改没改），不在本 session。此条即用户 memory 的「注释不是 ground truth」「拿运行时真相」。

### Step 4 — 起草并交付

按 6 条质量线成文。长 prompt **必须**落到文件报路径（scratchpad 或用户指定），别糊进对话；短的直接给纯文本。交付后一句话说清：这份 prompt 谁来跑、跑前要先核实哪几点。

## 产出结构（生成的 prompt 建议骨架）

```
[角色 + 一句话目标]
## 硬规则（违反即失败）
1. …（只读/边界/不代跑）
## 上下文（耐久锚点：文件/契约/模式）
## 执行前先核实（易变细节，列为第一步）
## 任务步骤
## 输出契约（写哪 / 结构 / 对话里只回什么）
## 参数（留 ____ 待填）
```

## 示例输出

用户说「给我写个 prompt，让另一个 session 给 CharacterForm 加个字数上限校验」→ 本 skill 产出（节选）：

```
你是 onlychat 前端工程师。给 CharacterForm 的简介字段加字数上限校验。

## 硬规则（违反即失败）
1. 只改校验逻辑，绝不顺手重构相邻代码（surgical）。
2. 工作仓：不 commit、不 push。

## 上下文（耐久锚点）
- 表单组件在 src 里的 CharacterFormV2；沿用该文件现有的 zod schema 校验模式，别自造。
- 与 isDraftSame 的 dirty 判定联动，改完保存按钮态要对。

## 执行前先核实（易变，第一步做）
- 重读 CharacterFormV2，确认简介字段名 + schema 位置仍如上；若已被改动，停下重划范围。
- 上限数值去 PRD/设计确认，别写死猜测值 ____。

## 输出契约
- 只回：改了哪个文件:行号 + 一句校验规则；跑一遍空态/超长态验证。
```

注意：文件路径给的是「耐久锚点」（模式、联动关系），行号/字段名降级成「执行前先核实」，上限值留 `____`。

## 反模式

1. **偏好写死进 skill** —— 必过期；一律走 Step 2 实时读 MEMORY.md。
2. **把本次代码读取当铁律写进 prompt** —— 行号/签名会漂，必须降级为「先核实」。
3. **意图不全就硬产** —— 缺 4 要素先反问，别脑补。
4. **抢别的 skill 的活** —— 对象不是 prompt 就退给 xhs-writer / write-a-skill / brainstorm。
5. **替用户把功能做了** —— 本 skill 只产 prompt，不动业务代码。

## 自检

写完/大改后**必须**立即跑一次，≥85 才算交付：

```bash
python3 ~/.claude/skills/meta-check-skill/ref/audit.py write-a-prompt
```

## Codex compatibility

Preserve this workflow's intent and evidence rules. Translate Claude-specific tool names to the available Codex tools.
