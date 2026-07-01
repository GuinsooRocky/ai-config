# 布局模式 Patterns

> 通用设计系统 · 布局与交互的**可复用模式**（非具体组件清单）
> 轴: 🌗 暗/亮主题 · 📱 PC/移动 · 🆕 取最新版为准（底栏取 V3）
> onlychat 作示例：具体数值/className/file:行号【保留】，格式 📍示例: xxx (相对路径:行号)

## 概览

本章把页面骨架与编辑器交互沉淀成**通用模式**，每个模式给「何时用」+「何时不用」，再用 onlychat（产品名 Crushon AI）的真实代码做示例。

组织顺序由外到内：

1. **页面骨架** — 顶栏 / 左侧栏 / 右侧栏 / 移动底栏，外壳由谁管，透明头约定。
2. **响应式容器** — 断点、容器宽度、grid 列数、给侧栏让位机制。
3. **安全区 / sticky** — 软键盘、底栏让位、吸顶层级。
4. **不同区域不同骨架** — 路由分组各挂不同外壳的通用模式。
5. **.pc/.mobile 端拆分约定** — 何时拆文件、何时单文件断点解决。
6. **编辑器 / 双栏布局** — 双栏、双 frame、标签页 + Save 槽。
7. **选择 / 管理模式** — 批量选择态的横幅 / 顶栏 / 底栏三形态。
8. **标签页与同级切换** — Tab 切换、同级横滑切换条。

贯穿原则：

- **骨架数据驱动**：所有开合 / 全屏 / 顶栏显隐由一个 **per-route 状态中枢**集中管理，组件只读不算。
- **逻辑属性优先**：内边距用 `ps-`/`pe-`（logical），自动适配 RTL，不写死 `pl-`/`pr-`。
- **断点对位是硬约束**：sticky 层的 `top-*` 必须等于它上方固定元素的高度，差 1px 就钻缝。

---

## 1. 页面骨架模式

### 1.1 模式：单一骨架壳 + 状态中枢

**何时用**：应用有多个核心页共享同一套外壳（顶栏 / 侧栏 / 底栏），但每页对外壳的需求略有不同（有的要全屏、有的隐藏顶栏、有的双侧栏）。

**做法**：只写一个带完整 chrome 的 layout，所有可变状态（侧栏开合 / 是否全屏 / 顶栏显隐 / 双侧栏）抽到一个 **per-route 状态中枢**；进每个页面时由「路由 → 初始 props」映射注入差异，组件层只读状态、不各自判断。

**何时不用**：页面外壳彼此完全不同（详情页自带布局 / webview 透明壳）→ 见 §4 不同区域不同骨架。

📍示例: onlychat 的 Dashboard 骨架是唯一带完整 chrome 的 layout (src/app/[locale]/(dashboard)/layout.tsx)；状态中枢是 per-route zustand store，用 React Context 包裹、每进 LayoutProvider 新建实例 (src/store/layout.tsx:144-154)。

骨架默认状态字段（DEFAULT_PROPS）📍示例: src/store/layout.tsx:52-68：

| 字段 | 默认 | 含义 |
|---|---|---|
| `isFullPage` | `false` | 内容区是否全屏（去 padding） |
| `isShowHeader` | `true` | 是否显示顶栏 |
| `isSidebarMobileOpen` | `false` | 移动抽屉侧栏开合 |
| `isSidebarDesktopOpen` | `true` | 桌面左侧栏展开 |
| `isSidebarDesktopMini` | `false` | 桌面左侧栏迷你态（仅图标） |
| `isRightSidebarDesktopOpen` | `false` | 桌面右侧栏开合 |
| `isLeftRightSidebarLayout` | `false` | 是否「左+右双侧栏」布局 |

路由 → 初始 props 映射 📍示例: src/components/Layout/LayoutPropsProvider.tsx:41-78：

| 区域 | 注入的初始 props |
|---|---|
| 列表型页（chat 列表） | `isShowHeader:false` + `isSidebarDesktopMini:true` + `isFullPage:true` + 注入 `sidebarExtension` |
| 详情型页（chat 详情） | 叠加 `isLeftRightSidebarLayout:true` + `isSidebarDesktopOpen:false` |
| 全屏沉浸页（memory） | `isFullPage:true` + `isShowHeader:false` |
| 其他 | 用 DEFAULT_PROPS |

### 1.2 模式：全局 Provider 链 + 全局浮层根

**何时用**：弹窗 / toast / 登录层 / loading 这类「不属于任何页面 DOM」的浮层，需要一个全站唯一的挂载根。

**做法**：在 root 客户端壳里按「由外到内」嵌套 Provider（i18n → 主题 class → 状态库 → UI 库 → 数据层 → 业务 Provider），最内层挂命令式弹窗根 + 全局浮层。这样 `show()` 出来的弹窗都挂在同一根，不污染页面 DOM。

📍示例: onlychat Provider 嵌套 (src/app/[locale]/ClientLayout.tsx:318-388 + [locale]/layout.tsx:417-451)：`NextIntlClientProvider → NextThemesProvider(class) → jotai → Mantine ThemeProvider → TRPCProvider → 业务 Provider → ErrorBoundary → LayoutPropsProvider → NiceModalProvider(命令式弹窗根) → children`。全局浮层 `Toaster` / `GlobalLoading` / 登录层挂这一层。

> 通用要点：暗亮主题靠最外层的 `class`-mode 主题 Provider（在 `<html>` 上挂 `dark` class），而非每个组件自己读主题。

---

## 2. 响应式容器模式

### 2.1 模式：非标准断点表（一处定义，全站引用）

**何时用**：任何响应式系统。断点要集中定义，组件只引名字不写死像素。

**做法**：在样式配置里覆盖默认断点，并允许加业务专用断点（如双侧栏布局需要一个比 `lg` 更大的分界）。

📍示例: onlychat 断点 (tailwind.config.js:371-379，覆盖了 Tailwind 默认，非标准)：

| 断点 | 值 | 备注 |
|---|---|---|
| `xs` | `420px` | |
| `sm` | `640px` | |
| `md` | `768px` | PC/移动文件拆分常用分界 |
| `lg` | `1024px` | 桌面侧栏默认显隐分界 |
| `sxl` | `1280px` | 🆕 自定义断点，双侧栏布局专用 |
| `xl` | `1536px` | |
| `2xl` | `1920px` | |

宽容器上限 📍示例: `maxWidth.8xl = 1524px` (tailwind.config.js:133-135)，用于宽顶栏。

### 2.2 模式：运行时屏幕类型（SSR 预判 + 客户端校正）

**何时用**：需要根据 PC/tablet/mobile 跑不同**逻辑分支**（不只是 CSS），且要避免首屏抖动。

**做法**：① 服务端用 UA 预判设备类型，首屏注入消除偏移；② hydration 后客户端按 `window.innerWidth` 覆盖精确值；③ 不同布局可用不同的分界阈值。

📍示例: onlychat 服务端 UAParser 预判 `serverDeviceType` 首屏注入，hydration 后客户端覆盖 (src/app/[locale]/layout.tsx:335-339 + ClientLayout.tsx:159-170)。阈值随布局变 (src/components/Layout/ScreenTypeManager.tsx)：

| 场景 | mobile | tablet | pc | 出处 |
|---|---|---|---|---|
| 双侧栏布局 | ≤639 | 640–1279 | >1279 | `:33` |
| 其他页 | ≤639 | 640–1023 | >1023 | `:38` |

### 2.3 模式：fixed 侧栏 + 容器 padding 让位（不用 grid 分栏）

**何时用**：侧栏是 `fixed`/`sticky` 浮层（开合有过渡动画、要盖在内容上），而内容区需要随侧栏状态调整可用宽度。

**做法**：容器**不**用 grid/flex 分栏，而是用左右内边距（`ps-`/`pe-`）给 fixed 侧栏留白；padding 值随侧栏状态在断点处切换。好处：侧栏动画独立、内容区不重排 grid。

**何时不用**：编辑器这种「两栏都在文档流里、都要滚动」的固定双栏 → 用 grid（见 §6.1）。

📍示例: onlychat 普通页 leftLayout (src/app/[locale]/(dashboard)/layout.tsx:156-192)：

| 侧栏状态 | 左 padding |
|---|---|
| 列表展开（mini+extension） | `lg:ps-[370px]` |
| 展开 + mini 态 | `lg:ps-[69px]` |
| 展开（普通） | `lg:ps-[232px]` |
| 收起兜底 | `lg:ps-[280px]` |

右侧栏让位：开时 `lg:pe-[300px]`（双侧栏页用 `sxl:pe-[300px]`）。双侧栏页的左让位走同结构但断点换成 `sxl:`(1280px) 📍示例: :117-135。

> 关键尺寸记忆点（示例值）：侧栏展开 **232px** / mini **69px** / 列表展开 **370px** / 收起兜底 **280px** / 右侧栏 **300px**。全部用 `ps-`/`pe-` 自动 RTL。

---

## 3. 安全区 / sticky 模式

### 3.1 模式：移动端软键盘安全区

**何时用**：移动端有输入框、且底部有固定按钮（Save / 操作栏）。

**做法**：① viewport 设 `interactiveWidget='resizes-content'`，软键盘弹出时 resize 内容区；② 滚动容器底部预留安全区 `pb-[calc(N+env(safe-area-inset-bottom))]` 给 fixed 底栏让位；③ 软键盘弹起时隐藏 fixed 底部按钮、滑到底时兜底复显。

📍示例: onlychat viewport `interactiveWidget:'resizes-content'` + `userScalable=false` (src/app/[locale]/layout.tsx:208-214)；编辑器单列底部预留 `pb-[calc(96px+env(safe-area-inset-bottom))]`，软键盘弹起隐藏 Save、滑到底兜底复显 (EditNotesFrame.mobile.tsx:327, :370-376)。

### 3.2 模式：底栏让位安全区（PC）

**何时用**：PC/移动通用，内容区底部有固定横幅/底栏。

**做法**：内容区固定留底部 padding（如 `pb-[80px]`）给底部横幅让出安全区，避免最后一屏内容被遮。

📍示例: onlychat main 内容区固定 `pb-[80px]` (src/app/[locale]/(dashboard)/layout.tsx:438-466)，全屏态 `isFullPage` 则无 padding。

### 3.3 模式：sticky 层级阶梯（top 对位 + z 分层）

**何时用**：多个吸顶元素叠在一起（顶栏 → 标签条 → 板块横幅）。

**做法**：① 下层 sticky 的 `top-*` **必须等于**上层固定元素的高度，差 1px 就钻缝；② z-index 按「谁该压住谁」分配，主顶栏 z 高于次级头。

📍示例: onlychat 主顶栏 `sticky top-0 z-40`，返回式简头 `sticky top-0 z-10`——前者要压住更多内容 (DashboardHeader.tsx:120 / CommonHeader.tsx:9)。编辑器内 `EditorTabs` 用 `sticky top-11` 必须等于上方 `EditorHeader` 的 `h-11`(44px)，否则钻缝 (EditorTabs.tsx:42-43)。

---

## 4. 不同区域不同骨架模式

### 4.1 模式：路由分组各挂不同外壳

**何时用**：应用里不同区域的「外壳需求」根本不同——核心产品页要完整 chrome，详情页自带布局，文章页只要 root，App 内嵌页要透明背景。

**做法**：按区域分路由组，每组一个 layout，决定挂什么外壳：完整骨架 / 透传 children / 落到 root / 透明全屏占位。**不要**用一个 layout 内大量 if 去切外壳。

📍示例: onlychat 四路由组 chrome 差异：

| 路由组 | 外壳 | 出处 |
|---|---|---|
| `(dashboard)` | 完整：节日横幅 + 侧栏 + 顶栏 + main + 移动底栏 | `(dashboard)/layout.tsx:419-471` |
| `(chatbot)` | 无外壳，`return children`（各页自带布局） | `(chatbot)/layout.tsx:9` |
| `(web-article)` | 无自有 layout，落到 root（html/body + Provider 链） | — |
| `(webview)` | 透明全屏占位 | `(webview)/layout.tsx:16-23` |

嵌套 layout 进一步在分组内注入差异 📍示例: chat 子 layout 设 `isShowHeader:false / isSidebarDesktopMini:true / isFullPage:true` + 注入 sidebarExtension (chat/layout.tsx:119-206)；memory 子 layout 仅透传、状态交给同步控制器。

### 4.2 模式：透明头约定（嵌入 webview）

**何时用**：页面被 native/外层 webview 加载，要求背景透明让宿主内容透出。

**做法**：注入 `<style>html,body{background:transparent!important}</style>` 盖过 root 在 body 上设的背景色 + 暗色 `.dark` 选择器，占位容器用 `min-h-dvh bg-transparent`。`!important` 必要——root 的暗色背景优先级更高。

📍示例: onlychat (webview)/layout.tsx:16-23：

```html
<style>html, body { background: transparent !important; }</style>
<div class="min-h-dvh bg-transparent">{children}</div>
```

---

## 5. .pc / .mobile 端拆分约定

### 5.1 模式：交互模型分叉才拆文件

**何时用**：PC 与移动的**交互模型本质不同**（不是样式差异）时，把组件拆成 `Xxx.pc.tsx` + `Xxx.mobile.tsx`，各自 export 同名组件。

**何时不拆**：仅 light/dark、间距、字号差异 → 单文件内用 `dark:` / `md:` 断点解决（强烈默认）。乱拆会制造双份维护成本。

**判据**（拆 vs 不拆）：

| 维度 | 拆文件 | 单文件断点 |
|---|---|---|
| 布局结构 | PC 双栏 vs 移动单列 | 列宽随断点变 |
| 交互手段 | PC 拖拽/框选/右键 vs 移动点击整页跳转 | 同样点击，只是触达区不同 |
| 信息密度 | PC 瘦行 vs 移动胖卡 | 同结构换字号/间距 |
| 导航形态 | PC 浮层 vs 移动整页跳转 | — |

📍示例: onlychat 世界卡是仓内唯一大规模文件级拆分的功能域 (src/components/WorldCard/)。已拆与不拆的判定 (06-世界卡 §0)：

- **拆**：`EditNotesFrame`（PC 左右双栏 + 拖拽/框选/右键 vs mobile 单列 + 点条目整页跳转）、`NoteCategoryCard`（PC 承载拖拽落位 vs mobile 无拖拽胖卡）、`NoteEntryCard`（PC 48px 瘦行 + 双击改名 vs mobile 胖卡）、`WorldInfoFrame`（PC 双栏 vs mobile 单列 3 卡）、管理态（PC 吸顶横幅 vs mobile 顶栏头 + 底栏，见 §7）。
- **不拆（共享件）**：`DraftBadge` / `KeywordChipInput` / `PriorityLevelStars` / `ImageUploadField` / cover 系列——靠 `md:` 断点共用一份。
- **矢量定义只写一处**：勾选框 `ManageCheckedSquare`/`ManageUncheckSquare` 定义在 PC 文件 (NoteEntryCard.tsx:479/500)，mobile 从那里 import (NoteEntryCard.mobile.tsx:28)。

---

## 6. 编辑器 / 双栏布局模式

### 6.1 模式：PC 左右双栏 + 移动单列（同一编辑器两实现）

**何时用**：编辑器有「列表 + 编辑区」结构。PC 屏宽够，左列表右编辑、点列表项即时切右栏；移动屏窄，单列、点条目整页跳转到 `/edit/[id]`。

**做法**：

- PC：固定 grid 双栏，列宽用 grid 模板（小屏 320 / 大屏 400），两栏各自 `overflow-y-auto` 独立滚动（`min-h-0` 保证可滚）。右栏空态显引导。
- 移动：单列 flex-col 滚动容器，点条目整页跳转；底部 fixed Save。

📍示例: onlychat PC 双栏 (EditNotesFrame.pc.tsx:1016)：

```
<div class="grid size-full grid-cols-[320px_minmax(0,1fr)] lg:grid-cols-[400px_minmax(0,1fr)]">
  <aside class="flex h-full min-h-0 flex-col gap-3 overflow-y-auto px-10 pb-6"> ← 左列表
  <section class="h-full min-h-0 overflow-y-auto px-10 pb-6">                  ← 右编辑/空态
</div>
```

移动单列 📍示例: EditNotesFrame.mobile.tsx:315，点条目整页跳转到 `/world/[id]/edit/note/[noteId]`，无双栏。

> 列宽与编辑器顶部的标签条用同一套 grid 模板对齐 📍示例: `md:grid-cols-[320px_minmax(0,1fr)] lg:grid-cols-[400px_minmax(0,1fr)]` (EditorTabs.tsx:44) 与双栏一致，保证标签条左格压在左列表上。

### 6.2 模式：编辑器顶栏（返回 + 标题 + 入口 pill）

**何时用**：进入沉浸式编辑器/创建流，需要一个轻量返回头（区别于全站主顶栏）。

**做法**：`sticky top-0` 一条 bar：左返回箭头 + 标题（truncate）+ 右侧功能 pill（如指南入口）。**高度双端分叉是硬约束**：移动端高度必须与下方 sticky 层（标签条、选择头）对位。

📍示例: onlychat EditorHeader (EditorHeader.tsx:51)：`sticky top-0 z-10 border-b px-4`，高度 mobile `h-11`(44px) / PC `md:h-[52px]`。移动必须 44，因为 `EditorTabs`/同级切换条的 `sticky top-11` 与选择头(h-11) 都按 44 对位，52 会钻缝 (:48-50 注释)。

> 通用经验：编辑器专用返回箭头常自绘轻量版（无 drop-shadow、无 locale 旋转），与全站主返回图标分开 📍示例: EditorHeader.tsx:90 内联 BackArrowIcon。

### 6.3 模式：标签页容器内嵌 Save 槽（恒高防抖）

**何时用**：编辑器顶部既要切 Tab，又要在某些 Tab 放 Save 按钮，但不想 Save 出现/消失时整条抖动。

**做法**：标签条容器设最小高度 = Save 按钮高 + 上下 padding，保证「有 Save / 无 Save」两态恒高。

📍示例: onlychat EditorTabs (EditorTabs.tsx:42-44)：容器 `md:min-h-16`(64px) = Save 按钮 `h-10` + `py-3`，两态恒 64px 不抖。

---

## 7. 选择 / 管理模式（批量多选态）

### 7.1 模式：管理态三形态（PC 吸顶横幅 / 移动顶栏头 + 底栏）

**何时用**：列表需要进入「批量选择」态做批量删除/移动。PC 与移动的承载位置不同。

**做法**：

- **PC**：列表顶部吸顶横幅承载（Selected n + 操作下拉 + 删 + 关）。横幅 `sticky top-0`，盖在列表上滚。
- **移动**：拆成「顶栏选择头」（替换编辑器顶栏的同一 44px bar：Cancel / Selected n/M / Select All）+「底部固定操作栏」（删除栈 + 主操作按钮）。上下分置，留中间内容可滚选。

📍示例: onlychat 三件套（06-世界卡 §8）：

| 形态 | 规格 | 出处 |
|---|---|---|
| PC 吸顶横幅 ManageBanner | `sticky top-0 z-30`，内 `rounded-[14px] bg-black/4 px-3 py-2 dark:bg-white/4`；Selected `text-light3-primary dark:text-dark3-primary` | `ManageBanner.pc.tsx:86-88` |
| 移动顶栏选择头 ManageSelectionHeader | 复用 EditorHeader 同一 `sticky top-0 z-10 h-11 border-b`：Cancel(灰) / `Select n/M`(黑白) / Select All(主题色) | `ManageSelectionHeader.mobile.tsx:26` |
| 移动底部操作栏 ManageActionBar | `flex gap-5`：左 Delete 垂直栈 + 右 Move To 主按钮 `h-10 rounded-[25px] bg-light3-primary dark:bg-dark3-primary` | `ManageActionBar.mobile.tsx:27` |

> 移动选择头复用编辑器顶栏的同一 44px 位 = §6.2 高度对位约定的直接收益。

### 7.2 模式：单条目的选中态 / 勾选框（瘦行 hover 浮现 vs 胖卡常驻）

**何时用**：列表项需支持「当前编辑选中」与「批量勾选」两种态。

**做法**：

- 普通态勾选框 `opacity-0 group-hover:opacity-100`（hover 才浮现），进管理态后常显。
- 选中/勾选高亮统一用主题色 20% 底（`bg-light3-primary/20 dark:bg-dark3-primary/20`）；移动胖卡额外加 1px 主题色边框。
- 勾选框矢量「选中（实心方块+白勾）/ 未选（描边圆角方框）」两态成对。

📍示例: onlychat PC 瘦行勾选框 `absolute left-2 size-5`，普通 `opacity-0 group-hover:opacity-100`、manage 常显 (NoteEntryCard.tsx:338-348)；选中底 `bg-light3-primary/20 dark:bg-dark3-primary/20` (:319/322)。移动胖卡 checked 加边框 `border-light3-primary/50 ... border` (NoteEntryCard.mobile.tsx:151-152)。

### 7.3 模式：拖拽排序 / 跨分类移动（PC 专属）

**何时用**：PC 列表要拖拽排序或跨分类拖动条目（移动端不做，改用右键/操作栏移动）。

**做法**：用拖拽库包列表根；被拖行保槽位（`opacity:0`）、邻居 transform 让位、落位处显幽灵占位卡；拖拽预览卡用 DragOverlay 渲染，多选时叠数量徽标；松手做飞入动画。落位高亮态给分类容器换底色。

📍示例: onlychat PC 用 dnd-kit (EditNotesFrame.pc.tsx:1016-1175)：框选矩形 `fixed z-40 border border-light3-primary bg-light3-primary/10`；DragOverlay 预览卡描边 `border-2 border-light3-primary/50`，多选数量徽标 `absolute -right-2 -top-2 bg-light3-primary dark:bg-dark3-primary`；松手飞入 `transition transform 200ms cubic-bezier(0.2,0.8,0.2,1)`。分类容器落位高亮 `bg-purple-3 dark:bg-white/10` (NoteCategoryCard.tsx:190)。配套 PC 右键菜单移动 (MoveNoteContextMenu.tsx:73，portal 到 body + 视口边界 clamp)。

---

## 8. 标签页与同级切换模式

### 8.1 模式：Tab 切换（active 下划线宽随文字）

**何时用**：编辑器/页面内的少量 Tab 切换（2–3 个）。

**做法**：active 文字加粗变色 + 下方 `h-[2px]` 主题色下划线，**下划线宽度跟随文字宽**（inactive 用透明占位等高，避免布局抖）。

📍示例: onlychat EditorTabs (EditorTabs.tsx:57-70)：active `text-black dark:text-white` + 下划线 `h-[2px] w-full rounded-full bg-light3-primary dark:bg-dark3-primary`，inactive `text-gray-2 dark:text-gray-1` + 透明占位等高。

### 8.2 模式：同级横滑切换条（移动全屏编辑页）🆕

**何时用**：移动端进入「单条目全屏编辑」后，要在同类条目间快速横向切换 + 末尾新建，而不必返回列表。

**做法**：顶部一条 `sticky` 横向滚动 pill 条（`overflow-x-auto` + 隐藏滚动条），同类条目并排、当前高亮、末尾 + 新建；达上限隐藏 Add；未完成项 pill 下挂草稿徽章。`sticky top-*` 仍要对位上方编辑器顶栏高度。

📍示例: onlychat SiblingSwitcherStrip (SiblingSwitcherStrip.tsx:118-189)：容器 `flex gap-2 overflow-x-auto sticky top-11 z-10 hide-scrollbar`；pill 选中 `bg-light3-primary/20 text-light3-primary dark:bg-dark3-primary/20 dark:text-dark3-primary`、未选 `bg-black/4 dark:bg-white/4`；头像 `size-9 rounded-full`；Add `size-9 rounded-[50px] border border-black/10`；达 `WORLD_CARD_NOTES_MAX`(99) 隐藏 Add (:181)，未完成 pill 下挂 DraftBadge (:172)。

---

## 附：本章涉及的关键尺寸 / token 速查（示例值）

📍示例: onlychat (tailwind.config.js，`darkMode:'class'`)

| 项 | 值 | 语义 |
|---|---|---|
| `sxl` 断点 | `1280px` | 双侧栏布局分界 |
| `lg` 断点 | `1024px` | 普通页侧栏分界 |
| `md` 断点 | `768px` | PC/移动文件拆分分界 |
| `max-w-8xl` | `1524px` | 宽顶栏容器 |
| 侧栏展开 / mini | `232px` / `69px` | fixed 侧栏让位 |
| 右侧栏 | `300px` | 右侧栏让位 |
| 编辑器顶栏高 | mobile `44px` / PC `52px` | sticky 对位基准 |
| 标签条最小高 | `64px`(min-h-16) | Save 槽恒高防抖 |
| `light3-primary` / `dark3-primary` | `#923EFC` / `#F75ECC` | 主题色（紫/粉，永远成对） |
| `light3-bg` / `dark3-bg` | `#FCFCFC` / `#202020` | 页面背景 |
