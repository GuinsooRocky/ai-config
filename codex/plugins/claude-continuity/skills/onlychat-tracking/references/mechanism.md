# OnlyChat 埋点机制（接线细节）

> SKILL.md 是流程主干；本文是 tc/tv/tl/registry/委派/新旧体系/guard/神策 的具体写法，按需查。

## 新旧两套（别混）

- **新代码用 `@/tracking`**（tc/tv/tl/useTv + registry 三表）。截至 2026-04 仍有 415 档用旧 `@/lib/track`，**不为迁移而迁移**，只在改该档核心逻辑时顺带换。
- 旧 `@/lib/track`：`TRACK(event)`（**只接事件名、不接参数**）、`TrackWithParams(event, params)`。**老组件 / 共享 nav（如 CreateNavModal、navigation.tsx）整文件是旧体系时，新增一条埋点跟着旧体系写**（别为一条 tv 把 `@/tracking` 塞进共享侧栏文件）。
  - 坑：要带参数却用了 `TRACK` → 参数发不出去（首页 CreateWorld 点击「缺 source」就是这么来的，要换 `TrackWithParams`）。

## tc / tv / tl / useTv 选型

| API | 形态 | 上报前缀 | 机制 |
|---|---|---|---|
| `{...tc('key')}` | 固定 DOM 点击（展开到元素 props） | `cus.click_*` | **全局 1 个 document click 委派** |
| `{...tv('key')}` / `useTv` | 块 mount 曝光 | `cus.view_*` | mount/进视口触发；列表用 `useTv` 默认加 `once:true` |
| `tl('key', { params })` | 弹窗曝光 / 命令式 / 系统 / 失焦 / 带计算参数 | 按语义命名 | 手动调用 |

- NiceModal 弹窗曝光：`useEffect(() => tl('xxx'), [])`，事件名用 `cus.view_*`（仿 chat-unavailable 先例：modal 走 `show()` 非声明式 mount，挂不上 tc/tv hash 委派）。
- 同一按钮按状态分流（如 SaveAndPublish vs SaveAndUpdate）→ `tl` 带参数，事件名仍 `cus.click_*`。

## tc 是「捕获阶段」委派（验证时关键）

`src/tracking/core/tc.ts`：`document.addEventListener('click', handler, true)` —— 第三参 `true` = **捕获阶段**。
- 后果：点击瞬间，**document 捕获监听先触发上报**，早于按钮自己的 React `onClick`。
- 所以即使 onClick 里 `router.push()` 跳转 / `modal.hide()` 卸载，**事件已经发了**。验证"点了好像没报"多半是跳转后 console 被清/被原生弹窗压住（见 verify-gotchas.md），不是没发。

## registry 三表

`src/tracking/registry/{click,view,logic}.ts`，每条 `'kebab-key': 'cus.{click|view|logic}_xxx'`。
- 前缀对齐：click.ts → `cus.click_*`、view.ts → `cus.view_*`、logic.ts 混（view/click/logic 名都可，按真实语义）。
- **点击事件登到 logic.ts 是踩坑**（曾把 interest-tag select 误放 LOGIC 后修）；遇到顺手修。
- call-site 用 kebab key：`tc('worldcard-xxx')`；registry 把它映射成 `cus.*`。

## transport（最终出口）

`src/tracking/core/transport.ts` → `track()` → `@/lib/track` 的 `TrackWithParams` → `window.sensors.track(event, params)`（神策）+ dataLayer(GTM) + TikTok。
- 即新旧两套**最终都进同一个神策 `sensors.track`**。
- 神策 SDK `show_log`：dev/test 开（`FE_ENV=pro` 关），开了会把每条事件打 console（**太吵，验证别靠它**，见 verify-gotchas.md 的 snippet）。

## tracking-guard（CI 防删）

`scripts/tracking-guard.ts`（`npx tsx scripts/tracking-guard.ts`）：用 TS compiler API 找所有 tc/tv/tl 调用 → 解析首参 literal type → 反查哪些 registry key **没被用**（防误删埋点）。
- 本 skill 的 `tracking_tool.py orphan <prefix>` 是它的「按前缀 scoped」轻量版。
- guard 报一堆未用 key 时先看**是不是别人前缀**（chat-* 等），别人的不归你。

## 链路参数（source / category）透传范式

「**组件 tracking-agnostic + 父级补业务参数**」：
- 子组件（ImageUploadField / KeywordChipInput）只暴露回调 `onTrackUpload(e)`，**自己不发埋点**；
- 父级在回调里 `tl('xxx', { params: { category, ... } })` 补业务参数。
- B1 编辑页首次进入的 `source`（manual_named / manual_skip / import）也走这套：create 页 seed 草稿时写 createSource，编辑页读出来发。

## 参数硬规则（再强调）

- no PII（email/phone/用户输入/token）
- no 翻译文本（`t('...')` 进参数 → 不同 locale 炸统计；用稳定英文 enum）
- 语义化参数名（不要 A/B/type）
- 能前端算别等后端：file_size_kb（File.size/1024）、note_count（数响应条目）、duration（前端 `Date.now()` 掐表）
