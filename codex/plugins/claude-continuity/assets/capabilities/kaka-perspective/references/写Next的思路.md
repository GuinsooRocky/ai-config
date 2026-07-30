# 写 Next.js 的思路 — yangbo 的全栈工程取舍

做 Next.js 相关决策时，按这些立场走。每条都是「主张 X 而不是 Y，因为 Z」。

## 1. Next 只做渲染层，API 交给 Hono
不要用 Next Route Handler 自己扛 API。
理由：Route Handler 没有路由级中间件链、没有 RPC 类型推导、运行时受限。
「Next.js 专注渲染框架，Hono 专注 API 框架……这是大多数严肃项目的选择」。

## 2. 集成两种模式，没有哪个更对
- **模式 A**（推荐）：Hono 独立部署 Cloudflare Workers，前端用 RPC 调用。
- **模式 B**：Hono 嵌进 `app/api/[[...route]]/route.ts`。

选型决策树：要 Cloudflare binding / 要多端复用 / 团队 >3 人 → A；否则 B。
演进路径：先 B 起步，需求增长再拆 A——因为「Hono app 是纯函数，换导出方式就能换环境」。

## 3. 一份 Zod schema 作 SSOT，反对前后端各写类型
同一份 schema 同时吃多个角色：
- 前端表单校验（`zodResolver`）
- 后端入口校验（`zValidator`）
- RPC 入参类型
- LLM structured output 指令（`zodToJsonSchema`）
- 出口校验

「改 maxTokens 上限只改一行，全链路跟上」。

## 4. 类型用推导，反对「类型转悠一圈」
用 `hc<AppType>` + `InferResponseType / InferRequestType` 直接推导。
反模式：调 Hono 拿到类型后，又手写一个前端类型。
前端只 `type-only` 导入 `AppType`，不把后端运行时代码打进 bundle——
为此单独建 `packages/server-types`，或把 `AppType` 放进 shared 包 re-export。

## 5. `z.input` vs `z.infer` 要分清
- 前端表单 / 入参类型 → `z.input`（带默认值的字段可省略）
- 后端业务函数 → `z.infer` / output（默认值已填充）

## 6. 数据请求分四层，职责不重叠
```
contracts        数据形状
  ↓
http / client.ts 统一请求入口（怎么发）
  ↓
api/*.ts         接口语义映射，一个接口一个文件
  ↓
TanStack Query   客户端状态（什么时候发、loading/error/缓存/失效）
  ↓
页面             只展示
```
「请求怎么发还是走 http，TanStack Query 只管什么时候发」。

## 7. 服务端状态用 TanStack Query，反对 useEffect + useState 手撸
loading / error / 缓存 / 重试 / mutation 后失效重拉「本质不属于业务」。
TanStack Query 是**叠加**而非推翻请求层——接入后原 http 层不动。

## 8. QueryClient 用 useState 工厂创建
```ts
const [client] = useState(() => new QueryClient())
```
反模式：建在服务端组件里、或建成模块级单例（RSC 环境下会共享运行时实例出问题）。

## 9. 对 RSC / 流式 UI：知道但不用（克制）
承认 `ai/rsc`（`streamUI` / `createStreamableUI`）在 Generative UI、Dashboard 问答场景是降维打击，
但主线产品坚持 `useChat + UIMessageStream`。四条理由：
1. 多轮对话实现复杂
2. 要跨端（RSC 只能在 Next 跑）
3. 后端在 Workers 上 RSC 不顺滑
4. 不希望 LLM 越俎代庖选组件——UI 该由前端工程师决定

## 10. 样式决策下沉到 token + 共享组件
三层：基础令牌（原始色阶/字号）→ 语义令牌（surface/content/border/brand/state）→ 组件约束。
硬约束：
- 页面代码不准直接写 `#xxxxxx` / `rgba()`
- 颜色走 `content-*` / `surface-*` / `state-*`
- 按钮只从 Button 变体选
- 新增颜色先改 `theme.css`
