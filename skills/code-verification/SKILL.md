---
name: code-verification
description: 功能完成或 bug 修复后的代码验证流程（纯静态代码查证，默认只读，不启动 dev server）。Use when the user says 需要验证、校验一下、验证一下、检查修复、帮我验一下、verify this change、validate the fix，或要求确认一次刚完成的实现/修复。按改动范围自适应选择验证维度（全面 / 深度 / 正反面 / 对抗 / 穷举 / React 生命周期 / 数据流 / 状态流 / 样式契约），强制输出「无回归 + 净正向」结论。纯静态读代码、自身从不启动服务器；实际渲染输出 / 后端实际取值标「跨边界」作为下一步，三方/native/标准源码可深读。与 code-planning 区分：那是写前规划，本 skill 是写后验行为正确性。
argument-hint: "[--mode=light|full] [验证对象 / diff 描述]"
---

# Code Verification — drama-agent

## Goal

在功能完成或 bug 修复之后，针对「本次 diff + 目标行为」给出有证据的验证结论，而不是只说「看起来没问题」。

**本 skill 是纯静态代码查证：每条结论落到读全的代码（file:line），自身从不启动 dev server、不跑 preview。** 渲染是代码的确定函数——样式契约、自适应稳健性、执行时序、状态流、性能反模式，全在代码里，靠**读透代码**得出。

代码读不到的只有「实际输出 / 内容 / 取值」（LLM 的真实返回内容、模型是否真的拒绝某段尺度、真像素）——这才标「跨边界」；**三方 / 标准 / 运行时「行为」不算跨边界**，库源码 / 官方 spec / 状态流转都可往下读（标「可深读」）。

两层结构：
- **方法层（D1–D9）**：按改动范围自适应选「怎么看」。
- **结论层（C1 没有副作用 / C2 全正向）**：每次必出「看完签核什么」，独立于选了哪些维度。

小改动保持轻量（`--mode=light`）；高风险改动深挖链路、反例与外部内容残留标记（`--mode=full`）。默认只读——除非用户同时要求修复，发现缺陷先报告，不直接改。

## 验证深度（--mode）

| mode | 何时用 | 做什么 |
|---|---|---|
| **light**（默认） | 纯文案/常量、单行配置、低风险样式，只命中「小型改动」 | diff + 引用点 grep + 类型风险；方法层只取 D1（轻量）；**结论层 C1/C2 仍必出** |
| **full** | 命中任一域行（见下）、bug fix、共享 export、schema/契约改动，或用户要求深验 | 按维度路由取全部相关维度 + 必要命令（typecheck/build）+ 可深读 / 跨边界残留显式标出 + 结论层 |

**drama-agent 域行（命中即升 full，即便看着像小改）**：
- LLM 调用 / OpenRouter 选路 / Worker 代理（`openrouter.ts`、出站，另受 `.claude/rules/outbound-fetch.md`）
- schema 改动 / 阶段 I/O 契约（`schemas/**`、另受 `.claude/rules/schema-backward-compat.md`）
- 重试 / 错误分类（`core.ts`、`retry.ts`、`LlmError`）
- 分档 tier 逻辑（action/clip/drama 的上下限、if/then）
- 方言注入 / 内容尺度 policy（`dialects/**`、`policy.ts`）
- promptkit → 装配代码契约（`assembly-spec.md`）

## First Pass

1. 明确验证对象：读当前 diff、最近改动文件、用户描述的目标行为和已知 bug 根因。基准是 diff + 目标行为。
2. 读入口规范 + 命中的领域规则（横切，喂给所有维度）：先读根 `README.md` / `.claude/README.md`；再列本次 diff 命中的 `.claude/rules/`（`outbound-fetch` → D4/跨边界、`schema-backward-compat` → D4/D7、`html-sink-sanitize` → D4/D9、`worker-logging` → D4）。规则按域落到哪个维度就在哪个维度报。
3. 建影响面：直接改的文件、被改 export 的调用点、相关 stage / 组件、相邻 state。
4. 定 mode + 选维度：逐一过 D1–D9 动态判断；命中域行或 bug fix 升 full，否则 light。拿不准多选、按风险排序，说明跳过项理由。
5. 先验证假设再跑命令。**本 skill 自身不跑 app**——样式/时序/状态/性能在代码里读；只有「LLM 实际返回 / 真像素」代码读不到才标「跨边界」。
6. 结论层 C1/C2 每次必出。

## 维度路由（动态判断 + 护栏）

**① 逐一过 D1–D9 动态判断。** 每个维度问「本次 diff 碰了它覆盖的东西吗」——碰了选、没碰标不适用。完整性来自「过完 9 个」，不来自「匹配到对的行」。

**② 固定层（不参与判断）：** C1 / C2 每次必出（含 light）；D4 对抗 full 默认跑（除非纯文案/常量/类型）。

**③ 非显而易见触发（最易漏选，逐条核对）：**

| 信号 | 别漏 | 为什么 |
|---|---|---|
| bug fix | D2 深度 + D3 正反面 + 原 bug 复现/等价证据 | 确认命中根因，非遮症状 |
| LLM 调用 / 选路 / 出站 | 升 full + D4 + 跨边界（真实返回） | 域行高风险；OpenRouter/Worker 代理选路错了看着像小改 |
| schema / 阶段契约 | + D7 + 调用方/fixture 兼容性 | 老 `examples/**` fixture 会不会不再校验（见 backward-compat 规则） |
| 重试 / 错误分类 | + D3 反面 + D8 状态流 | 瞬时 vs 永久错分类错 → 无限重试或该重试不重试 |
| 分档 tier 逻辑 | + D5 穷举（action/clip/drama 三档） | 某档上下限失守 = 逼模型现编 |
| 新 effect / async | + D4 + D6 | stale closure、abort 缺失、重复触发 |
| 共享 util/hook/组件 export | D1 全面 + 调用点传播 | 改一处波及全调用链 |
| 动画 / 大列表 / 高频 handler | + 性能反模式静态扫（标疑虑） | 反模式是代码可读的「因」 |

**④ 路由规则：** fail-safe（拿不准宁可多选一维）；无明显信号（build/config、纯类型）→ D1 全面 + 类型/构建风险；light 默认，命中域行或 bug fix 升 full。

## Verification Dimensions（方法层 D1–D9）

> **证据纪律：每条结论必须落到实际读过的代码（file:line），不从 diff、命名、「通常这样写」推断。** 断言 cleanup 取消了 timer → 读 cleanup 本体；断言调用点都改了 → grep 全部逐个看；断言默认值变了 → 并排读旧/新实现。只能推断、读不到实证的 → 标 `可深读`（点明源在哪）/ `跨边界`，绝不写成已验证。「读不全代码」不是「要跑起来才知道」的理由。

### D1. 全面验证
- 看完整 diff，不只用户提到的文件。grep 被改名称、export、类型、schema 字段的所有调用点。
- 检查是否遗漏同域入口：image/text 模式、action/clip/drama 三档、dev 直连 / prod 代理两条选路。
- 对共享 API 变更，列调用点标 `已验 / 待验 / 不适用`。

### D2. 深度验证
- 从入口追到最终副作用：用户输入 → stage 组装 → core（LLM 调用 + ajv + 重试）→ 产出解析 → 展示。多入口先点明追的是哪个。
- bug fix：确认根因仍在当前代码路径、修复命中根因，不是遮表象。
- async 时序：await 顺序、race、abort、超时回落、错误兜底、重复触发。
- 契约：input/output schema、optional/required、默认值、单位、enum 值、tier 约束。

### D3. 正反面验证
- 正面：happy path 完整达成，成功态写对位置、展示对 UI。
- 反面：失败、取消、空数据、超时、模型拒绝（`LlmError.kind='empty'`）、网络瞬时错、重复点击、快速切换是否安全。
- bug fix：验「修复前会失败的路径现在不失败」+「相邻正常路径没被破坏」。

### D4. 对抗验证
- 假设当前实现是错的，主动找反例：旧调用点、stale closure、abort 未接、缓存/上一次产出残留、选路分支翻转。
- **对被搬动/替换的调用**（换 helper、挪分支）：并排 diff 旧/新的默认值/入参/输出，明确写出「变了什么」，别假设搬动后语义不变。
- 检查「复制来的逻辑」是否真适用新场景（数据来源、作用域、生命周期一致吗）。
- 检查「复用已有函数」是否引入不需要的副作用。
- 命中安全规则时在此并报：出站目标 host 是否仍是常量（outbound-fetch）、Worker 日志有没有落 key/正文（worker-logging）、用户内容有没有进 raw HTML sink（html-sink-sanitize）。

### D5. 穷举验证
- 只对有限状态/高风险矩阵穷举；无限输入用等价类和边界值。
- drama-agent 常见维度：tier（action/clip/drama）、mode（image/text）、intensity（sfw/suggestive/explicit/max）、选路（dev/prod）、loading/error/empty、`LlmError.kind`（http/timeout/network/empty）。
- 输出矩阵标明覆盖组合，不声称覆盖未验证组合。

### D6. React 生命周期流转验证
- mount → update → unmount → remount；尤其快速重跑、切换模式/档位、组件卸载时正在跑的请求。
- `useEffect` deps 是否完整稳定，cleanup 是否取消 timer / abort 请求 / 移除 listener。
- async 副作用里 `await` 之后读的值是不是当下最新（别读 closure 快照；本仓无 store，用 `useRef` / 重取）。

### D7. 数据流转验证
- 画数据链：用户输入 → stage 组装 → LLM → ajv 校验 → 解析 → 下一 stage / 展示。
- 确认 stage I/O 类型与 `schemas/**` 同源，别手写漂移的 type。
- promptkit → 装配代码：字段读写点是否一致，改产出端有没有同步改消费端。

### D8. 状态流转验证
- 列状态机：idle / running（第几 stage）/ 人工检查点 / compiling / success / error / empty，及合法转移（不能跳过人工检查点直接 compile）。
- reset 条件：换输入、切模式/档位、请求失败、重试、重新开始。
- boolean flag 组合是否出现不可能状态；互斥 flag 应考虑 union。

### D9. 样式契约 + 渲染态完整性（纯静态，读全样式上下文）
- **自适应稳健性**：结果表格/长 prompt 正文的溢出/换行——`flex`/`min-w-0`/`break-words`/antd `Table` 的列宽与 `ellipsis` 是否按意图声明；窄视口是否兜得住。判的是「这套约束对任意内容兜不兜得住」（代码属性），不是「某串具体断在哪」（内容，不归本维度）。
- **样式符合需求**：暗色/亮色分支（本仓 antd `theme` 切换）成对；disabled/loading/空/错误态分支齐；Modal/复制反馈层级正确。
- **渲染态完整性**：状态驱动的渲染分支都接对（与 D6/D8 联动，同一检查只报一次）。
- **外部内容残留（唯一标「跨边界」）**：LLM 实际返回文本的**长度/内容**会不会溢出（约束兜住的前提下属内容问题）、模型是否真的接受/拒绝某段尺度——这些不在代码里，标「跨边界」作为下一步。约束本体正确性仍在本维度静态查完。

### 性能反模式（横切静态扫，非独立维度；命中标「性能疑虑」+ 引导下一步）
- 命中（render 内重计算 / 大列表缺虚拟化 / 未节流 handler / 缺 memo 的昂贵子树）时：标「性能疑虑」+ file:line + 影响推断，问「要不要代码深查？」；非交互无人应答时默认列入「剩余风险」，不阻塞。静态命中 ≠ 真机一定慢。

## 结论层（每次必出）

### C1. 没有副作用（回归 + 副作用扫描）
- 本次改动是否对没碰到的相邻路径造成回归：被改 export 的所有调用点、共享 util/hook 的其他消费方、同域其他入口（image/text、三档、dev/prod 选路）。
- 是否引入非预期副作用：新增 effect/timer、多余重试/LLM 调用、状态残留、性能反模式。
- 判定：✅ 无回归 ｜ ⚠️ 有疑点/部分可深读或跨边界（列出）｜ ❌ 确有回归（列出）。

### C2. 全正向改动（净正向判定）
- 聚合 D1–D9 与 C1，一句话回答：本次改动是否「严格只把事情变好」——目标达成，且没把任何原本正常行为变差。
- 任一维度发现 P0/P1，或 C1 非 ✅，则净正向不成立，降为 ⚠️/❌ 并说明。
- 判定：✅ 净正向 ｜ ⚠️ 有已知 trade-off / 可深读或跨边界项 ｜ ❌ 非净正向。

## Commands

优先用项目已有脚本，不臆造：
- `npm run typecheck`（`tsc`）：类型面被波及时跑。
- `npm run build`（`tsc && vite build`）：改动影响构建/配置/类型面大时跑。
- 用 `examples/*.json` 当 fixture 手动过一遍 ajv（改 schema 时）。
- **本 skill 不启动 dev server、不跑 preview。** `可深读` / `跨边界` 判定见状态枚举。

不默认新增/改测试；需要补时先说明为什么验证风险必须靠测试覆盖。

## Output Format

结论开头，且结论行同时回答三件事：无阻塞 + 无回归（C1）+ 净正向（C2）。

```markdown
## 验证结论
[mode: light|full] 无阻塞 / 发现 N 个问题 / 有可深读·跨边界待办；回归(C1)：✅/⚠️/❌；净正向(C2)：✅/⚠️/❌。

## 覆盖范围
- 已读 diff：
- 已追调用点：
- 已运行命令：（无则写「未运行命令（静态验证）」）

## 维度结果（跑过的给证据；护栏/域行预期却跳过的附一句理由；明显不适用的不必列）
| 维度 | 状态 | 证据 |
|---|---|---|
| D2 深度验证 | 已验 / 跳过(理由) / 不适用 / 可深读 / 跨边界 | file:line 或深读位置 / 跨边界原因 |

## 结论判定
- C1 没有副作用：✅/⚠️/❌ + 证据
- C2 全正向改动：✅/⚠️/❌ + 证据

## 发现
- P0/P1/P2：问题、证据、影响、建议。
- 性能疑虑（如有）：反模式 + file:line + 影响推断 +「要不要代码深查？」

## 剩余风险
- 未覆盖项 / 可深读（点明深读在哪 + 值不值）/ 跨边界项 与原因。
```

状态枚举（**`可深读` / `跨边界` 判定以本表为唯一权威**）：
- **已验**：有 file:line 证据（含往下读进库源码 / 官方 spec 后给出的证据）。
- **跳过**：本维度与本次风险无关，**必须写理由**。
- **不适用**：改动类型天然不涉及该维度。
- **可深读**：决定结论的行为在**可读但本次没读全的源**里——一方代码未读透、`node_modules/<lib>` 源码、官方 spec（draft-07 JSON Schema / MDN / OpenRouter 文档）。这不是推给运行时，是「还有静态可读」：点明深读在哪 + 值不值。**没读就标 = 偷懒，违反证据纪律。**
- **跨边界（真·需要下一步）**：任何可读源里都没有的东西——① LLM 的**实际返回内容**（真文本下的真结果 / 模型是否真的拒绝某尺度）；② 真实渲染的真像素。只有这一档才真要「跑起来 / 拿到返回」，**必须显式标出，不能并进 ✅**。
- **fail-safe（仅限已读全手头可及的源后）**：拿不准 → 不标 ✅；疑点是「还有没有可读的源」→ 默认 `可深读`，别急着判 `跨边界`。

## Worked Example（bug fix：OpenRouter 选路改成 prod 走代理）

改动：`openrouter.ts` 把 `chatJSON` 的目标从「永远直连 OpenRouter + 带 Authorization」改成 `resolveTarget`（`import.meta.env.PROD || key==='' ` 走 Worker 代理 `/api/llm` 不带 key；否则直连带 key）。

- mode：full（命中「LLM 调用 / 选路 / 出站」域行）
- 路由命中：bug fix + 出站/选路 + 安全规则(outbound-fetch/worker-logging) → D2,D3,D4,D5,D8 + D9

```markdown
## 验证结论
[mode: full] 发现 1 个问题；回归(C1)：⚠️；净正向(C2)：⚠️。

## 维度结果
| 维度 | 状态 | 证据 |
|---|---|---|
| D2 深度验证 | 已验 | resolveTarget 选路 openrouter.ts:31-41；prod 分支不带 Authorization、走 PROXY_PATH |
| D3 正反面 | 已验 | 正：dev 有 key 直连带 Authorization；反：prod/空 key 走代理不带 key，key 不进 bundle |
| D4 对抗 | 已验(发现) | 判据 `import.meta.env.PROD || key.trim()===''`——dev 环境下用户清空 key 会静默切代理，但 dev 无 Worker → /api/llm 404；与「dev 直连」预期冲突 |
| D5 穷举 | 已验 | 选路矩阵：{dev,prod}×{有key,空key} 四格已覆盖，见 :38 |
| D8 状态流 | 已验 | 错误分类 LlmError.kind 未变（http/timeout/network/empty），重试判据不受选路影响 |
| D9 样式契约 | 不适用 | 本次纯网络层，无 UI 改动 |
| 安全规则 | 已验 | outbound-fetch：转发目标是常量 host，未引入 body 可控 host（跨边界：Worker 侧转发实现另需在 worker/** 验）；worker-logging：本 diff 在 web/**，不涉 Worker 日志 |

## 结论判定
- C1 没有副作用：⚠️ —— dev 下空 key 会切到不存在的代理路径，属边界回归风险
- C2 全正向改动：⚠️ —— 达成「prod 不泄露 key」目标，但引入 dev 空 key 的 404 边界，未净正向

## 发现
- P2：dev + 空 key → 走 /api/llm 但本地无 Worker → 404，错误文案不明确。证据 openrouter.ts:38。建议 dev 空 key 时给「填 VITE_OPENROUTER_KEY」的明确提示，而非静默走代理。
```
