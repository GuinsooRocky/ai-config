---
name: feedback-task-execution-cadence
description: 任务执行节奏 — 开始前对齐方案、过程中自动推进只在真岔路停、调研与验证力度按改动规模分级（trivial 轻量路径 / 大改动 tsc 增量自查）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5dbe88c8-7418-4ccf-a475-d831b5de17a6
  modified: 2026-07-31T13:24:12.984Z
---

## 开始前：对齐方案（停等确认才动 Edit/Write）

实现型任务（加功能 / 改交互 / 重构）动手写代码前，**先讲清：改哪些文件、关键决策点、不改什么**，等用户确认才动 Edit/Write。调研 / 读代码定位可以先做不用问。trivial 小改或用户明说"直接做"才跳过。

**聊产品/竞品时的「要，这个一定要」= 立待办，不是开工令**（2026-07-31 soliloquy 详情页 hero 轮播）：正在对照竞品聊某个效果，用户拍「要」，我直接改起了 `OcDetail.tsx` + `App.css`，被打断"你怎么写上代码了…放待办里说清楚做什么怎么做就行"。**产品语境里的拍板是给需求定性，落点是 BACKLOG 条目**（做什么 / 怎么做 / 图源与边界 / 不含什么 / 验收），施工要单独发起。判据：这轮对话在聊产品还是在施工——聊产品就别碰 Edit/Write。

**用户说"等我详细说"= 需求还没给完，停下听**（2026-07-11 自动点击脚本）：用户答了"等我详细说了你在做"，我仍抢跑搭了骨架 + 甩 TODO 模板让用户填，被纠正"先了解需求"。正确姿势：需求没讲完时不写码、不发结构化选择题让用户套我的猜测，等用户把需求描述完再动。"骨架无害可逆"不构成抢跑理由——用户要的是先被倾听。

## 过程中：自动推进，里程碑汇报

多 step 流程（fe-workflow / pageforge / dream-run / 审计 / 演进改造 / 长任务）：
- ✅ 每步完成出简短总结（耗时 / 产物 / 关键发现）
- ✅ 探针 + 调查 + 确定性修复连着做完再汇报，按里程碑
- ❌ 不要停下问"要不要继续下一步"—— 用户原话"很没有自动化的感觉"

## 何时该停（真决策岔路才停）

- scope 歧义 / cut vs wire / 动用户定的设计边界
- 改用户可感知行为（排序被改、被重定向、默认值变、跳转）的方案，实现前对齐 ——"用户说怎么改"≠"我可以随便改 + 扩范围"（2026-06-09 修 bug 顺手把排序静默改掉，制造新 bug）
- socket 中断后"续跑 vs 重跑"
- 写代码前的方案对齐（见第 1 段）
- 不要把 AskUserQuestion 用在"step 完成确认"上

## 调研与验证力度：按改动规模分级（2026-06-12 "改个 icon 花多少 token"）

**Trivial 档（单 icon / 单色 / 单行 className）→ 轻量路径**：拿 spec → 定位文件 → 改 → 只跑相关测试（或不跑）。不做矢量逆向工程、不全量 tsc、调研 grep 合并成最少次数。仓库硬规则（Figma MCP 三件套、icon 复用穷举）仍走，但执行收紧到一发查完。

**大改动档（动 type/接口、公共组件、一大块逻辑、提 PR 前）→ 跑 `tsc --noEmit --incremental`**（onlychat/世界卡系列）。
- Why：dev（SWC/Turbopack）只转译不查类型；pre-commit 只跑 eslint+prettier 也不查；唯一强制关卡是 `next build`（CI），离得远。**用户不开 VS Code/Cursor，没有编辑器红线**——我这次手动 tsc 是 build 前唯一类型防线，大改动后务必跑。`--incremental` 落 `.tsbuildinfo`，二次起只查改动。
- 曾评估 `tsc --watch` 常驻（吃内存，与防 OOM 冲突）和本地 git hook（husky 占了 `core.hooksPath`，加了又脏又碎），都放弃——「记 memory + 我自觉跑」最轻。
- 是我的工作节奏偏好，**不要**往 package.json 加 typecheck script、不进 git、不强加给团队。内存高占用主犯是常驻 dev server（见 [[project_worldbook_dev_oom]]），不是一次性 tsc。

**Why**：fe-workflow 原版要求每 step 确认，2026-05-15 用户覆盖为全自动跑、中途只看总结；"先出方案"来自用户原话。2026-06-12 用户质问"改个 icon 到底花了多少时间多少 token"——小活的调研/验证 overhead 一半是浪费（矢量逆向、重复 grep、全量 tsc），故加分级档。配合 CLAUDE.md Karpathy "Think Before Coding"，但 LLM 默认会过度验证 — 这条做力度闸。

相关：[[project_onlychat]]、[[feedback_worldcard_worktree]]、[[feedback_just_do_no_stop_suggestions]]
