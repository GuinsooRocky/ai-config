---
name: feedback-writing-comments-rules
description: 写注释明确边界 — 简易逻辑/UI 样式/Figma 节点号/过程性决策溯源(PM拍板·待确认·文案值)不加；PRD 章节号可保留；只为非直觉的 why 才加
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5dbe88c8-7418-4ccf-a475-d831b5de17a6
---

写注释的明确边界：

## 不要加注释（机械跳过，别犹豫）
- **简易逻辑**：一层 if / `||` 默认值 / 三元 / 简单 map filter — 代码已经说清楚
- **UI 样式/布局**：CSS 值、间距、颜色、z-index、flex 方向 — Figma 是 ground truth，注释翻一遍只会过时
- **Figma 度量清单复述**（2026-06-12 点名"这种注释不要有 本次工作区都不要有 UI 的注释"）：`// Figma X:Y — icon(30px rounded-8 中性色白→黑) + 名(14 medium) + 计数(右 白→黑50%)` 这种把设计稿规格逐项罗列的行，连同色 token 名（白→黑/深灰→中灰）一律不写；交互机制类 why（如 pointer-events 浮层为何要 auto、padding 恒定防文字位移）可留但砍掉数值与 token 细节
- **Figma 节点号**：禁带 `Figma 14983:208113` / `Figma 36754:102948` 这种 hex 节点 id（图层会改、节点 id 会飘）
- **把代码翻成中文**：例 `const name = ... || 'Untitled'` 上面不要写 `// 默认名 Untitled，避免空名`
- **过程性 / 决策溯源**（2026-06-10 点名）：禁写「PM 已拍板 / 待确认 / 待补充 / Maureen 决策 / PRD 未规定」这类决策来源与状态；也别在 `t('xx_key')` 上注释复述 i18n 文案值（如 `// no_permission = "No permission"`）——文案值在 i18n json，过程性事实属聊天/PR 不属代码。保留「行为是什么 + 非直觉的 why」即可（如「粘贴整段当单条 keyword，区别于打字逐键的逗号分隔」OK；「按 PM 决策粘贴…」不 OK）
- **QA-doc 项号 / loop 任务号 / issue 追踪标**（2026-07-08 soliloquy 点名"（QA 02 项4）这种注释不要写"）：`// 作者露出（QA 02 项4）`、`（补-2）`、`（bug-review #3）`、`（裁决 #3）`、`（QA 01 §#7）` 这类把注释当追踪表用的章节-号标一律不写——**即使现有代码里到处是也别跟着抄**（soliloquy 仓自己写满了，是坏习惯不是规范）。保留纯 why 散文即可（`// 官方=官方标；用户卡=@username，未设回落社区创作` OK；同句尾加 `（QA 02 项4）` 不 OK）。追溯归 fix_plan/dev-log/git，不进代码注释。⚠ 与下方"PRD §X.X 可留"区分：稳定 PRD 锚点用于 drift 校验才留，QA-doc 的"项4""§#7"是易飘的施工清单号，不留
- **多行规则复述块**（2026-06-11 点名"这些注释都不要 没人会好好读"）：文件头/函数头把行为规范整段复述（「粘贴与打字同规范按逗号切分；每段 trim 截断 100、空段跳过、重复不增、12 上限…」）不要写——规则语义进测试用例钉住，不进注释。一个函数最多留 1 行非直觉 why（如 stale-props 批量落定原因）

## 才加注释（这种才有信息量）
- **Why**：为什么这么写、为什么不那么写
- **非直觉取舍**：性能 vs 可读性、绕过 lib bug、和某个隐藏 invariant 对齐
- **踩过的坑**：「不能用 X 因为 Y 场景会炸」
- **隐藏约束**：调用方/上下游的强假设
- **PRD 章节号引用**（如 `// PRD §3.3.3.2 ...`）：可以保留作为追溯锚点，章节号比 Figma 节点稳定

## 路过同文件顺手清同模式老注释（onlychat 尤其）
- 整删「显而易见 + Figma 编号」型（如 `// 删除（…Figma X:Y 垃圾桶）`）
- 不要为清注释跨文件批量改；只清当前任务正在动的文件

**Why**：用户多次点名（2026-05-20 NoteEditor.pc Figma 14983:208113；2026-05-27 WorldCard Figma 35641:385267；2026-06-10 `// no_permission = "No permission"（PM 已拍板）"这种文案都不要"；"这种垃圾注释就算了"；改逻辑后老注释变错例多次）。Figma 节点 id / 简易逻辑 / 决策溯源的注释会在代码演进或决策变动时烂掉；PRD 章节号相对稳定可留。

相关：[[feedback-comments-not-ground-truth]]（这条管"读"——别信注释当事实）
