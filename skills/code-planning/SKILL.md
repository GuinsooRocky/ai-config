---
name: code-planning
description: 动键盘前的代码规划 — 状态放置（useState/useRef/React Context）、组件/模块拆分、副作用收敛、契约设计（schema/stage I/O/promptkit）、props 接口。情境触发、输出决策矩阵。触发词：「我要加一个 X」「这该放哪」「这该用 useState 还是 useRef/Context」「这组件/stage 要不要拆」「规划这段怎么写」，或 diff 出现新增 useState/useEffect、新 .tsx、新 export、新 stage、改 schema、动 App.tsx / web/pipeline/core.ts 等热点档前。不适用：纯样式、纯文案、纯常量值、不引入新抽象的 bug fix。与 code-verification（写后验）互补；reframe 是上游（先确认 frame 对不对，再进本 skill 规划实现）。
---

# Code Planning — drama-agent 代码规划顾问

## 为什么有这个 skill

**目标**：为**新代码**设立规划门槛，确保新增的 hook / 组件 / stage / utility 在诞生时就经过评估，别在这条五步流水线里再长出一个什么都塞的巨档。本 skill 规划新代码，不主动清历史债。

drama-agent 现在还小（React 18 + antd + Vite + ajv 的纯前端 SPA），但已有集中风险点：`web/App.tsx` 是单一大壳（表单/选项/流水线编排/结果展示/复制全在里面），`web/pipeline/core.ts` 是所有 stage 共用的执行器，`web/pipeline/stages/stage1-5.ts` 各自持一段 prompt 组装逻辑。**趁小把规划这一步流程化**，别等它长成 2000 行的 App.tsx 再重构。

## 何时触发

判断标准是**机械信号**（diff 上能验证），不是主观「这算大改吗」。

### 触发信号 → 维度映射

| diff 上能看到的信号 | 该过的维度 |
|---|---|
| 新增 `useState` / `useRef` ≥ 1 | Ⅱ-5, Ⅱ-6 |
| 新增 `useEffect` / `useLayoutEffect` | Ⅲ-8, Ⅲ-9 |
| 新增 `export const` / `export function` / `export default` ≥ 1 | Ⅰ-1, Ⅴ-13 |
| 新增 `.tsx` 档（不论行数） | Ⅰ-2, Ⅱ-7, Ⅵ-15 |
| 新增 / 动既有 hook（`use*.ts*`） | Ⅰ-3, Ⅲ-8 |
| 新增 stage（`web/pipeline/stages/stageN.ts`）或改 stage I/O 类型 | Ⅴ-12, Ⅴ-13, Ⅰ-3 |
| 改 `schemas/**` 或新增字段 | Ⅴ-12（并读 `.claude/rules/schema-backward-compat.md`） |
| 新增 `if/else if` 链 ≥ 3，或新增 `switch`（按 tier / model / mode / 方言分派） | Ⅳ-10 |
| Props interface 新增 ≥ 3 个 prop | Ⅱ-7 |
| 触碰热点档（见文末） | 信号命中子集 + 必查 4 条：Ⅰ-2 / Ⅰ-3 / Ⅱ-7 / Ⅳ-11 |

**只要命中任一信号，skill 触发。** 命中多条取维度子集并集。

### 机械上「不」触发

- diff **只**动 antd 样式 / inline `style=` / `styles.css`
- diff **只**改字串字面量值（不新增变量宣告、不改类型、不改控制流）
- diff **只**动 import 顺序 / 格式化
- bug fix 但 diff **不含**上方任一触发信号

不确定算不算触发时，**预设不触发**——宁可漏触发也别噪音。

## 维度（5 层框架）

> drama-agent 无 zustand / 无 tRPC / 无 server-state 缓存层，所以没有「store 作用域」「React Query key」这类维度；状态放置收敛成三选一（useState/useRef/Context）。

### Ⅰ. 结构层

**Ⅰ-1. 函数抽取 / 命名**
- 该抽吗？rule of three：同一逻辑第 3 次才抽（前 2 次允许 inline/复制；第 2 次是警觉点，评估「第 3 次可预期吗、两处差异多大」）。
- 该叫什么？动词+名词（`buildStage2Payload` 而非 `build`、`isImageMode` 而非 `check`）。
- 该住哪？stage 专属逻辑留在该 stage 文件；跨 stage 共用的进 `core.ts` 或独立 util，别塞进万能抽屉。

**Ⅰ-2. 组件拆分 / 单一职责**
- 触发拆分：JSX > 50 行、useState 合计 > 8、Props > 12、JSX 内条件分支 > 4。
- 方向：先拆「呈现组件」（纯 props in）再拆「容器组件」。
- 反模式：拆出来的子组件只被一处用且不会独立测试 → 过度拆分。
- drama-agent 现状：`App.tsx` 已把表单/编排/结果表格/复制混在一起——**加新 UI 区块前先想能不能拆呈现组件出去**，别继续往 App.tsx 堆。

**Ⅰ-3. Hook / stage 职责边界**
- god 信号：> 300 行、useState > 5、useEffect > 5、职责横跨 ≥ 3 个维度。
- stage 的拆分维度：按流水线职责（prompt 组装 / 调 core / 解析产出 / 兜底）。`core.ts` 是共用执行器（一次带 schema 的 LLM 调用 + ajv 校验 + 重试），**别把某个 stage 的特例逻辑塞进 core**——core 只该长通用能力。
- 反模式：把 god 拆成 god + 一个琐碎 hook，没减复杂度只是搬家。

**Ⅰ-4. 模块公私 API**
- `stages.ts` 是桶文件 = 契约宣告，只 re-export 消费者要用的；stage 内部 helper 不外泄。

### Ⅱ. 数据流层

**Ⅱ-5. 三段决策：useState / useRef / React Context**

开新状态前走这个决策树：
```
这个值改变需要触发 re-render 吗？
├─ 否（纯记账/定时器 id/最新值快照） → useRef
└─ 是 → 访问范围多大？
   ├─ 一个组件内 → useState
   └─ 跨多个组件 / 需 prop-drill ≥ 3 层 → React Context
```
- 流水线的**进度/中间产物**（storyline/scenes/shots…）是 App 级 state，用 useState 提在编排容器里；别为它另开影子副本。
- 长命 callback（AbortController、超时 timer）里要读的最新值放 `useRef`，别读 closure 快照。

**Ⅱ-6. Boolean flag → discriminated union**
- 同一对象上 ≥ 3 个 `is*/has*` flag，或出现「不可能同时为 true」的组合（`isRunning` + `isError` + `isDone`）→ 换 union。
```ts
// ❌ flag 爆炸（流水线运行态最容易踩）
{ isRunning: bool, isError: bool, isDone: bool, result: T | null }
// ✅ discriminated union
{ status: 'idle' } | { status: 'running', stage: number } | { status: 'error', error: E } | { status: 'done', result: T }
```

**Ⅱ-7. Props 接口设计**
> 12 props 必须触发拆分决策：该拆组件？该用 children/slot？该把相关 prop 打包成 config object？该用 Context 取代 prop drilling（≥ 3 层）？

### Ⅲ. 副作用层

**Ⅲ-8. useEffect 密度与职责**
新增 effect 前先问：
- 能不能改成派生值（直接计算 / `useMemo`）？
- 能不能改成事件处理器（`onClick` 内直接做）？
- 确实需要 effect → 写清 deps，不靠 lint 补。

**Ⅲ-9. Cleanup / abort / race**
- 任何 async 副作用（LLM 调用、多 stage 串跑）要有 abort 或 mounted guard。`openrouter.ts` 已有 `AbortController` + 超时；新增长跑逻辑照此。
- `setTimeout` / `setInterval` 必须在 cleanup clear。
- 快速重跑（用户连点「生成」）：确认前一次在跑的请求被中止或结果被丢弃，别让两次产出互相覆盖。

### Ⅳ. 控制流层

**Ⅳ-10. if-else / switch 链 → lookup table**
> 5 个 `else if`，或按同一变量不同值分派 → 换 `Record<K, handler>`：
- 按 `tier`（action/clip/drama）、`mode`（image/text）、`model` slug、方言分派参数/文案时，用注册表而非 if 链。model slug 已集中成常量（`DEEPSEEK_V4_PRO_MODEL` / `GLM_5_2_MODEL`），别在别处散落字面量。

**Ⅳ-11. 多步骤流程是否需要显式状态机**
- 流水线本身就是「storyline → scenes → shots →（人工检查点）→ compile」的多态流程。新增编排分支前，确认状态转移合法（不能跳过人工检查点直接 compile）；用一个显式的 phase 枚举/reducer，而非散落的 boolean。

**Ⅳ-12. 条件渲染深度**
- 嵌套三元 ≥ 2 层 → 拆 helper 或提早 return；JSX 内 `&&` 链 ≥ 3 → 拆变量或子组件。

### Ⅴ. 契约层

**Ⅴ-12. Schema / stage I/O 即 source of truth**
- `schemas/0N-*.schema.json` 是各阶段产出的契约。改字段前**必须**过 `.claude/rules/schema-backward-compat.md`（additive-only、别硬删/改名、`additionalProperties:false` 下加字段要同步改产出）。
- stage 之间的 I/O 类型（`Stage2Input` 等）要跟 schema 同源，别手写一份漂移的 type。
- promptkit → 装配代码（`assembly-spec.md`）是纯代码契约，改字段名同步改装配代码。

**Ⅴ-13. Magic string / enum 集中**
- 重复出现 ≥ 2 次的字串 → 提常量。
- model slug 只在 `openrouter.ts` 定义常量，UI/stage 引用常量，别硬编码 `'z-ai/glm-5.2'`。
- `tier` / `mode` / `intensity` 枚举以 schema / `policy.ts` 的类型为准，别在多处重定义。

**Ⅴ-14. 第三方/外部边界包装**
- OpenRouter 调用已包在 `openrouter.ts`（错误分类成 `LlmError`）；ajv 包在 `core.ts`。新接一个外部 provider / 校验器时同样包成独立模块——换实现时只动一处、可加 mock。

### Ⅵ. 韧性层

**Ⅵ-15. Loading / empty / error 三态**
- 任何 async 展示（生成中、各 stage 产出、编译结果）三态齐全。
- 错误要区分：网络瞬时错（可重试，`LlmError.kind='network'/'timeout'`）vs 内容被模型拒（永久，`kind='empty'`，文案应引导降尺度或手写）——别对两类用同一句文案。
- ErrorBoundary：结果展示区/编译区崩溃不该炸掉整个表单页。

## Workflow

1. **信号扫描（≤ 30 秒）**：对照信号表列出 diff（已存在或预估）命中的信号。无命中 → 不触发，直接写。
2. **抽维度子集（≤ 10 秒）**：命中信号对应维度取并集，通常 3–6 条。触碰热点档时额外加 Ⅰ-2 / Ⅰ-3 / Ⅱ-7 / Ⅳ-11。
3. **逐维度决策**：每条产出「决策 + 依据 + 替代方案（考虑过为何弃）」。被触发但不适用的维度标 `N/A` + 一句原因。
4. **输出决策矩阵**（必须表格，不是长叙述）：
```
## 规划决策
任务：{一句话}
| 维度 | 决策 | 依据 | 替代方案 |
|---|---|---|---|
| Ⅱ-5 状态放置 | useState 提在编排容器 | 只本页读写、需驱动 UI | useRef（不驱动渲染，错） |
| Ⅳ-10 分派 | tier→Record 注册表 | 3 档参数分派 | if 链（加档要回改） |
| Ⅴ-12 契约 | 新字段 optional | 老 fixture 要仍校验通过 | 直接 required（破兼容） |
## 开工
```
5. **开工后自查（10 秒）**：每条决策是否真执行了？有没有冒出该过却没过的维度？

## 反模式（主动 call out）

- **「先这样，之后再重构」**——巨档都是这么来的。要求当下做决策（「inline 不抽」也是显式决策）。
- **「先复制，之后抽」**——标准是 rule of three（第 2 次警觉、第 3 次动作），不是「第 2 次必抽」。
- **「这个 prop 加一下就好」**——prop 接口跨过 12 必须触发 Ⅱ-7。
- **「schema 加个字段而已」**——任何 schema 改动都要过 backward-compat 规则，别只改产出端不改 schema、或反之。

## drama-agent 热点档清单（动之前必跑本 skill）

- `web/App.tsx`（单一大壳：表单 + 流水线编排 + 结果表格 + 复制，最易继续膨胀）
- `web/pipeline/core.ts`（所有 stage 共用执行器：LLM 调用 + ajv 校验 + 重试；别塞 stage 特例）
- `web/pipeline/stages.ts` + `stages/stage1-5.ts`（各 stage 的 prompt 组装 + I/O 契约）
- `web/pipeline/openrouter.ts`（OpenRouter/Worker 代理选路 + 错误分类；改出站相关的另受 `.claude/rules/outbound-fetch.md` 约束）
- `schemas/**`（阶段契约；改动受 `.claude/rules/schema-backward-compat.md` 约束）

## 与其他 skill 的边界

| Skill | 时机 | 关系 |
|---|---|---|
| `reframe` | 需求 / frame 层 | 上游：先确认 frame 对不对，frame 定了本 skill 才规划实现 |
| `code-planning`（本 skill） | 动手前 | 主规划 |
| `code-verification` | 写完后 | 下游：静态验行为正确、无回归净正向 |

## 停止条件

- 无触发信号 → 直接写。
- 决策矩阵产出且勾选维度全有决策 → 进实作。
- 实作完成且自查通过 → 结束。

不需要做的事：跑全部维度（除非触及热点档）、写长篇分析、重构既有代码（除非需求要求）。
