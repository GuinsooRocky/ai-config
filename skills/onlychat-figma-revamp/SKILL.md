---
name: onlychat-figma-revamp
description: OnlyChat 项目 Figma UI 改版专用流程 — 严格照 MCP 返回值还原，V2 新组件 + useGradualRollout AB 灰度，V1 零改动。触发词："Implement this design from Figma"、"按 Figma 改版 UI"、"TagListV2/TagBoxV2/XxxV2"、"home_ui_revamp_ab"
---

# OnlyChat Figma UI 改版

仅用于 onlychat（`~/Desktop/cmm/onlychat*`）。改版 = 像素级还原 Figma + 可选 AB 灰度，**不动业务逻辑**。

## 何时用

- 用户粘贴 Figma URL + `Implement this design from Figma`
- 用户说「按 Figma 改 XX」「改版 UI」
- 新建 `XxxV2.tsx`（V1 保留）
- 改造已有 V2 对齐新设计稿

## 何时不用

- 纯逻辑 bug、状态/数据流改造 → 普通开发流程
- 非 Figma 驱动的 UI（比如跟着设计师口头描述改）→ 先把意图落成截图/Figma 再走本流程

## 核心原则

1. **Figma MCP 值照抄** — rgba/hex/stops/px 一字不改。详情见 memory `feedback_figma_mcp_strict.md`
2. **双模式必须全** — 项目 `darkMode: 'class'`，light 默认、dark 走 `dark:`。Figma 只给一个模式 → 停下来问另一个节点 ID，不要自己推
3. **V2 新文件，V1 不动** — 同目录新建 `XxxV2.tsx`，接口是 V1 props 的超集
4. **AB 挂在消费端，不在 V2 内部** — `isNew ? <V2/> : <V1/>`
5. **逻辑 100% 搬运** — hooks、store 写入、tracking、empty state、特殊 slug 分发、i18n fallback，逐条搬过来

---

## 标准流程

### 0. 环境（大改版才做）

- worktree：`git worktree add ../onlychat-<slug> lengmo_YYYYMMDD_feat_<slug>`
- 进 worktree 先 `pnpm install`（node_modules 不共享）
- `cp ~/Desktop/cmm/onlychat/.env .env`（gitignored，worktree 不会自动带）
- 端口 3000 被占：`lsof -ti:3000 | xargs kill`，**不要切 3001**（避免多个 next-router-worker 互相干扰）

### 1. 抓 Figma 设计稿

并行调三个 MCP 工具（同一个 nodeId）：
```
mcp__figma__get_design_context(nodeId)
mcp__figma__get_variable_defs(nodeId)
mcp__figma__get_screenshot(nodeId)
```

**读取规则**：
- `get_design_context` 返回的代码里 `var(--xxx, #fallback)` 的 **fallback 不可信** — 通常只是默认模式的值
- `get_variable_defs` 返回当前节点实际渲染用的值 → **以它为准**
- 变量名带 `↔︎` / `→` = 主题切换 token（light/dark 值不同），两个模式都要抓
- 变量名不带 `↔︎` = 固定色（如 `D_Primary 500`、`L_Primary 500` 作为三色品牌渐变的 stops），两模式共用

### 2. 映射到项目 token

**优先命名 token，arbitrary `[#xxx]` 只在项目没对应 token 时才用**。
完整对照表见 `references/tokens.md`；最常用的：

| Figma 值 | 项目 token | 含义 |
|---|---|---|
| `#923EFC` | `light3-primary` | light 主题色 |
| `#F75ECC` | `dark3-primary` | dark 主题色 |
| `rgba(0,0,0,0.04)` | `black-4` | light 半透蒙层底 |
| `rgba(255,255,255,0.04)` | `white-4` | dark 半透蒙层底 |
| `#707070` | `gray-1` | light 次要文字 |
| `#9E9E9E` | `gray-2` | dark 次要文字 |
| `#FCFCFC` | `white-2` / `light3-bg` | light 页面底 |
| `#202020` | `black-3` / `dark3-bg` | dark 页面底 |

Alpha 后缀：`/20`→`33`、`/70`→`b2`、`/80`→`cc`、`/10`→`1a`。

### 3. 写 V2

**接口**：V1 所有 props 都保留；新增的只允许是可选的 UI 控制位（如 `hideImageSlug`、`emptyClassName`）。

**逻辑搬运 checklist**（对 V1 逐项核对）：
- [ ] 所有 `use*` hook 调用（`useAsyncBlockTags`、`useTranslations`、`useLocale`、`usePathname`…）
- [ ] store 写入（如 `setHomeExpanded` 只在 pathname 是首页时调用——漏了会导致 GoTop/useCheckPageScroll 滚动错乱）
- [ ] Tracking 埋点（`TrackWithParams('cus.click_home_tag', ...)`）
- [ ] Empty state（`tagsData.length === 0` 时的占位 div，`emptyClassName` 要继续接）
- [ ] 特殊 slug 分发（target/image/event 单独渲染路径）
- [ ] i18n fallback（`getTagLabel` 对 `image`、`crushon_*` 返回空串，用 `||` 兜底，**不要用 `??`**）
- [ ] blockStore 过滤（屏蔽词功能）

**样式**：每一条颜色类都写双模式 `bg-X dark:bg-Y text-A dark:text-B`。不确定 light 值 → 回 step 1 抓。

### 4. 挂 AB（可选）

非 AB 场景直接改消费端引用即可。要 AB 时三步。

**先判断：新 topic 还是复用？**
- 这次改版是**整体实验**的一部分（对照组=全旧、实验组=全新，共享同一组用户）→ 复用同一 topic，避免用户看到新旧拼接的割裂体验
- 这次改版是**独立实验**（有独立观测指标 + 分配比例）→ 开新 topic
- 现有 topic：`home_ui_revamp`（首页整体 UI 升级：顶栏 + 筛选 + 全站 Tag），`home_card`（首页卡片尺寸实验）

**4.1 注册 topic** — `src/hooks/useGradualRollout.ts`：
```ts
export enum ROLLOUT_TOPIC {
  home_ui_revamp = 'home_ui_revamp_ab',
  // 新 topic 加在这里；命名要覆盖实验全部范围，别用 home_tag_refactor 这种只暗示一部分的名字
}
```

**4.2 消费端三元切换**：
```tsx
const isNew = useGradualRollout(ROLLOUT_TOPIC.xxx, true);
return isNew ? <V2 {...props} /> : <V1 {...props} />;
```

**4.3 埋分组曝光**（只在 AB 容器挂载时调一次）：
```tsx
TrackWithParams('cus.home_abtest_xxx', { category: isNew ? 'a' : 'b' });
```

**AB 开关来源**：
- 纯前端 → Growthbook
- 后端驱动 → 接口返回
- ❌ **不要用 env var**（要发版、无法灰度；测试期间可以临时加但合并前必须回滚）

**URL 调试参数 `?__ab__=100/0` 是全局的**，会同时切换页面里所有 topic 的 rollout。看到「只改了 A 但 B 也坏了」先查这个。

### 5. 验收

- `pnpm exec tsc --noEmit -p tsconfig.json` 过
- `pnpm run dev` 起 3000，**浏览器 light/dark 两种模式都目视**（切 OS theme 或在 DevTools 里 `html.dark` 开关）
- Tailwind arbitrary `[rgba(...)]` / `[linear-gradient(...)]` **JIT 可能静默失败**，tsc 过 ≠ UI 对
- 对比 Figma 截图做最后一次色值对齐

### 6. 提交

- **不要自动 commit**，等用户说「commit」再提（见 memory `feedback_commit_policy.md`）
- message：`feat: <页面> UI 改版（AB <topic>）` 或 `feat: add XxxV2 component`

---

## 常见坑（每一条都真的踩过）

### CSS transition 白闪
两态 `border-width` 必须一致。`border-0 ↔ border-transparent` 过渡动画 width `0→1` 会露出浏览器默认 border-color（浅灰/白）。
- ❌ 选中 `border-0`、未选中 `border-transparent`
- ✅ 两态都 `border-transparent`（或都 `border-0`）

### 渐变圆角端点硬色带
`linear-gradient(94deg, A 0%, B 50%, C 100%)` 在 rounded-full 两端会看到 A/C 的纯色边带。
- ✅ 扩展起止：`A -5%, B 50%, C 105%`

### Arbitrary 双 background JIT 失败
`bg-[linear-gradient()_padding-box,linear-gradient()_border-box]` 这种双 bg + box 技巧在 Tailwind JIT 常跑不起来。
- ✅ 退回 `bg-[linear-gradient(...)]` 单层 + `border-transparent`

### i18n 空串 fallback
`getTagLabel` 对 slug `image`、`crushon_*` 返回 `''`（不是 null）。
- ❌ `label ?? slug`（`??` 只兜 null/undefined，空串照样渲染出空 tag）
- ✅ `label || fallback`，并加 explicit 分支：`rawLabel || (slug === 'image' ? t('image') : slug)`

### SVG 不跟主题色
`text-*` 影响 SVG 的前提是 `fill="currentColor"` / `stroke="currentColor"`。有些图标 path 写死了 hex 就不跟。
- ✅ 用之前先 `Read` SVG 源文件确认 currentColor

### 图标不该只在选中态显示
target/image 这类 slug 的专属图标，未选中也要渲染（用户反馈：「tag 的 svg 无论选不选中都要有」）。
- ❌ `{item.selected && item.slug === 'target' && <TargetIcon />}`
- ✅ `{(item.slug === 'target' || item.slug === 'image') && <Icon />}`

### homeExpanded store 同步漏
展开/收起切换时，若 pathname 是首页（`/` 或 `/${locale}`），必须调 `setHomeExpanded(next)`。这个 store 被 `HomeContent`、`useCheckPageScroll`、`GoTop` 消费，漏了会导致滚动定位/吸顶错乱。

### Event tag 选中 bg 渐变透明
Figma 给的「20% alpha 三色渐变」stops 用固定品牌色 + 20% alpha（`#F75ECC33` → `#923EFC33` → `#3BA6F333`），两个模式**共用**（品牌色不随主题切换）。

---

## References

- `references/tokens.md` — Figma 值 ↔ onlychat Tailwind token 完整对照表
- `references/ab-pattern.md` — V2 + useGradualRollout 完整代码模板（TagListV2 实战）
- `references/figma-mcp-flow.md` — MCP 三工具返回值解读 + 双模式节点抓取

## 相关 memory

- `feedback_figma_mcp_strict.md` — Figma MCP 严格值原则
- `feedback_skill_design_pattern.md` — 本 skill 自身遵循的结构
- `feedback_commit_policy.md` — 不自动 commit
- `feedback_transparent_header.md` — 顶栏透明规则（改版时别把它改没了）
