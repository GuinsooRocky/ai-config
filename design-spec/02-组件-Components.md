# 组件 Components

> 设计规范 · 通用组件库。分类按通用设计系统概念组织，onlychat 的具体组件/数值/`file:line` 作为「📍示例 / 参考实现」保留。
> 轴：🌗 暗/亮主题（含双值） · 📱 PC/移动 · 🆕 取最新版为准
> 令牌/主题见 `01-基础-Foundations.md`；布局/响应式/编辑器/选择模式见 `03-布局模式-Patterns.md`；选型速查见 `04-决策指南-Decision-Guide.md`。

## 本章目录

| § | 子节 | 内容 |
|---|---|---|
| 一 | [控件 Controls](#一控件-controls) | 按钮 / 开关 / 标签页 / 选择器下拉 / 输入框多行文本 / 字数计数 / 图片上传位 / 滑块 / Radio·Checkbox / 标签输入 |
| 二 | [浮层 Overlays](#二浮层-overlays) | Modal 弹窗 / Drawer 抽屉 / Popover 气泡 / Tooltip / Toast / 上下文菜单 / 图片预览 / 多步引导 |
| 三 | [卡片 Cards](#三卡片-cards) | 封面卡 / 列表条目卡 / 分类分组卡 / 用户实体 Icon / 空态占位卡 / 推荐胶囊 + 选卡决策 |
| 四 | [标签 · 徽章 · 指示器](#四标签--徽章--指示器-tags--badges) | Tag/Pill / Chip / Badge / 门控标签 / 红点·计数 / 星级 / 进度字数指示器 |
| 五 | [反馈 · 动效 · 空态](#五反馈--动效--空态-feedback--motion) | 加载态 / 空态 / Toast / Banner 横幅 / 装饰动效 |
| 六 | [图标 Icons](#六图标-icons) | 按功能分类的 canonical 图标库 + viewBox/尺寸/着色 + 已废弃对照 + 使用规范 |

---

## 一、控件 Controls

> 通用设计系统 · 控件层（原子交互件）
> 三轴贯穿全章：🌗 暗/亮（成对双值）· 📱 PC/移动 · 🆕 取最新版为准
> 数值/hex/px/类名均照抄实现，可溯源：📍示例 给出参考实现的 `相对路径:行号`

本章收口所有「原子交互控件」——无业务语义、被弹窗/页面/卡片层层复用的最小积木。每个控件给出：视觉规格 · DOM 结构 · 状态 · 🌗暗亮 · 📱端差异 · 🆕版本说明。

排序：按钮 → 开关 → 标签页 → 选择器/下拉 → 输入框/多行自适应文本 → 字数计数 → 图片上传位 → 滑块 → Radio/Checkbox → 标签输入。

### 0. 配色 token 速查（控件高频引用）

颜色走 Tailwind 自定义 token（`darkMode: 'class'`，`dark:` 分支生效）。控件里出现的成对 token 已映射真实 hex：

| token（亮 / 暗） | 亮值 | 暗值 | 语义 |
|---|---|---|---|
| `light3-primary` / `dark3-primary` | `#923EFC`(紫) | `#F75ECC`(粉) | 主题色（成对铁律：light 紫、dark 粉，永远成对写）|
| `light3-secondary` / `dark3-secondary` | `#62D5FF`(蓝) | `#A8EF30`(绿) | 次级色 |
| `light3-newSecondary` / `dark3-newSecondary` | `#3BA6F3` | `#7976FF` | 新次级色 |
| `light3-smallPopupBg` / `dark3-smallPopupBg` | `rgb(255,255,255)` | `#2F3034` | 小浮层底 |
| `gray-1` | `#707070` | 同 | 深灰（控件底 / placeholder 暗 / disabled 文字）|
| `gray-2` | `#9E9E9E` | 同 | 中灰（placeholder 亮 / 弱文字）|
| `gray-3` | `#C7C7C7` | 同 | 浅灰文字 |
| `red-1` | `#FF2619` | 同 | 警告（旧）|
| `red-2` | `#800000` | 同 | 错误正文字色 |
| `red-5` | `#F77872` | 同 | 错误提示底色（红底块）|
| `red-6` | `#FF4444` | 同 | 字段 error 强提示（半透明红框/底）|
| `black-2` | `#363234` | 同 | 碳色（暗色卡/输入底）|

> 透明蒙层惯例：`bg-black/4`（亮填充底 `rgba(0,0,0,0.04)`）↔ `bg-white/4`（暗填充底 `rgba(255,255,255,0.04)`）。控件普遍用 `black/4` `white/4` 的不透明度语法成对写。

---

### 1. 按钮 Button

#### 1.1 设计哲学：配色与几何分离

基础按钮**只负责配色 + 一组通用过渡/禁用样式**；**几何（圆角、padding、字号覆盖）由调用方通过 `className` 注入**。`twMerge(基础类, className)`，调用方类排最后可覆盖。典型调用方补 `rounded-full px-6 py-3`。

📍示例: `src/components/CoUI/Button.tsx`（基础类 :38-40；调用方几何 Button.stories.tsx:22）

#### 1.2 基础态规格（所有变体共享）

| 项 | 值 | 📍出处 |
|---|---|---|
| 字号 | `text-base`（16px） | Button.tsx:39 |
| 字重 | `font-bold` | :39 |
| 行高 | `leading-none`（1） | :39 |
| 文字色 | `text-white dark:text-white`（默认白字） | :39 |
| 过渡 | `transition-all duration-200 ease-in-out` | :39 |
| 默认 `type` | `"button"`（非 submit） | :36 |
| 圆角/padding/尺寸 | **无**，由调用方决定（典型 `rounded-full px-6 py-3`） | Button.stories.tsx:22 |

#### 1.3 变体 color（5 种）

| color | 类名 | 配色（亮 → 暗） |
|---|---|---|
| `primary`（默认） | `bg-light3-primary dark:bg-dark3-primary` | 紫 `#923EFC` → 粉 `#F75ECC`，白字 |
| `secondary` | `bg-light3-secondary dark:bg-dark3-secondary` | 蓝 `#62D5FF` → 绿 `#A8EF30`，白字 |
| `new-secondary` | `bg-light3-newSecondary dark:bg-dark3-newSecondary` | `#3BA6F3` → `#7976FF`，白字 |
| `gray` | `text-black bg-gray-3 dark:text-gray-3 dark:bg-gray-1` | 浅灰底黑字 → 深灰底浅灰字 |
| `tertiary` | `text-black bg-white dark:text-white dark:bg-[rgba(255,255,255,0.10)]` | 白底黑字 → 10% 白蒙层底白字 |

📍示例: Button.tsx:11、:23-30

#### 1.4 尺寸 size

组件本身**不带尺寸**，由调用方几何类决定。两档常见尺寸示例：

| 档 | 几何类 | 用途 | 📍示例 |
|---|---|---|---|
| 标准（实色填充） | `rounded-full px-6 py-3` | 表单提交 / 弹窗主操作 | Button.stories.tsx:22 |
| 大主按钮（满宽/固定宽） | `h-10 w-full rounded-[25px]` 或 `h-10 w-[100px] rounded-[25px]` | 底部固定 Save / Retry 等 | 上传 Retry 按钮 ImageUploadField.tsx:781 |

#### 1.5 状态

| 状态 | 表现 | 📍出处 |
|---|---|---|
| default | 见变体配色 | — |
| hover/active | **未内置**（依赖 `transition-all`，调用方自加 hover 类或品牌 hover token `*-primaryHover`） | Button.tsx:39 |
| **disabled** | `cursor-default` + 底色 `bg-black/10`(亮)/`dark:bg-white/10`(暗) + 文字 `text-gray-1`(`#707070`) | Button.tsx:39 |
| disabled（大主按钮另一套） | `disabled:bg-gray-3 disabled:text-black dark:disabled:bg-gray-1 dark:disabled:text-gray-3` | ImageUploadField/底部 Save 类 |
| loading | **无内置**（业务层自包 spinner） | — |

#### 1.6 DOM 结构

```
<button type="button"
  class="text-base font-bold leading-none text-white
         transition-all duration-200 ease-in-out
         disabled:cursor-default disabled:bg-black/10 disabled:text-gray-1
         dark:text-white dark:disabled:bg-white/10 disabled:dark:text-gray-1
         {colorVariants[color]} {className}">
  {children}
</button>
```

#### 1.7 🌗暗亮 / 📱端差异

- 🌗：每个变体都成对写 `dark:` 分支（见 1.3）；主题色亮紫暗粉、次级色亮蓝暗绿是全站规律。
- 📱：组件本身无端差异，由调用方 className 控制。

#### 1.8 衍生模式（可复用，非完整控件）

两种 hover 灰底交互模式，可直接复用：

- **图标方块按钮**：`h-11 rounded-[14px] border border-black/2 dark:border-white/2 backdrop-blur-sm`，未激活底 `bg-black/4 dark:bg-white/4`，hover `md:hover:bg-black/10 md:dark:hover:bg-white/10`。图标激活态可走颜色翻转 `text-white dark:text-black`（激活）↔ `text-black dark:text-white`（未激活）。📍示例: CharacterActionButtons.tsx:71-81
- **图标圆/方钮（删除/裁剪等）**：`size-6 rounded-full`（或 `rounded-[19px]`），底 `bg-white/80 dark:bg-black/20` 或 `bg-gray-5 dark:bg-lp_bg2`，内嵌 `size-4` 图标。📍示例: NoteEntryCard.tsx:409-411、ImageUploadField.tsx:724

---

### 2. 开关 Switch 🆕

> 🆕 版本判定：**Switch2 > Switch**。Switch2（纯 div+span 自绘，13 处引用）为当前标准；Switch（基于 Mantine，5 处旧调用）被取代，仅留要点。

#### 2.1 Switch2（当前标准）视觉规格

| 项 | 值 | 📍出处 |
|---|---|---|
| 轨道宽 | `w-[28px]` | Switch2.tsx:23 |
| 轨道 padding | `p-0.5`（2px，决定 knob 间距） | :23 |
| 轨道圆角 | `rounded-3xl` | :23 |
| 轨道默认底 | `bg-gray-1`(`#707070`) | :23 |
| 轨道开启底 | `bg-light3-primary dark:bg-dark3-primary`（紫/粉） | :27 |
| 滑块尺寸 | `h-3 w-3`（12×12） | :38 |
| 滑块圆角 | `rounded-full` | :38 |
| 滑块默认色 | `bg-white` | :45 |
| 滑块禁用色 | `bg-gray-2`(`#9E9E9E`) | :45 |
| 滑块过渡 | `transition-transform` | :38 |
| 开启位移 | `ltr:translate-x-full rtl:-translate-x-full`（按读写方向） | :41 |

📍示例: `src/components/CoUI/Switch2.tsx:20-49`

#### 2.2 状态

| 状态 | 表现 |
|---|---|
| default（关） | 灰轨 `bg-gray-1`，`cursor-pointer`，滑块靠左 |
| checked（开） | 主题色轨 `bg-light3-primary dark:bg-dark3-primary`，滑块右移满格 |
| disabled | `cursor-not-allowed bg-gray-1`，滑块 `bg-gray-2`（不论开关都灰） |

#### 2.3 DOM 结构

```
<div onClick class="pointer flex w-[28px] items-center rounded-3xl bg-gray-1 p-0.5
     {disabled? cursor-not-allowed bg-gray-1
      : checked? cursor-pointer bg-light3-primary dark:bg-dark3-primary
      : cursor-pointer}">
  <span class="block h-3 w-3 rounded-full transition-transform
       {checked? ltr:translate-x-full rtl:-translate-x-full : ''}
       {disabled? bg-gray-2 : bg-white}"></span>
</div>
```

> `onClick` 同时触发 `onClick?.()` 与 `onChange?.(!checked)`（Switch2.tsx:31-34）。

#### 2.4 🌗暗亮 / 📱端差异

仅开启态轨道色有 `dark:` 分支（紫→粉）；灰轨/白滑块两态共用。PC/移动无差异；窄轨（28px）适合密集列表行尾。

#### 2.5 旧版（Switch，简记，被取代）

封装 Mantine `<MSwitch>`：开启 track `dark:!bg-lp_primary !border-light3-primary !bg-light3-primary`，关闭 `!bg-gray-1`；`isDisable` =「禁用样式但仍可点」与原生 `disabled` 区分；`disabled` 时 `grayscale`。仅需 Mantine 受控/label 能力的极少数旧场景保留。📍示例: Switch.tsx:24-30

---

### 3. 标签页 Tabs

两个导出：`Tabs`（默认）+ `TabsWithIndicator`（带滑动下划线）。两种 `type`：`default`(下划线) / `button`(胶囊)。

📍示例: `src/components/CoUI/Tabs.tsx`

#### 3.1 type=default（下划线式）

| 部位 | 类名 | 📍出处 |
|---|---|---|
| wrapper | `font-bold text-sm flex justify-between` | Tabs.tsx:39 |
| item 通用 | `w-[50%] inline-flex h-7 items-center justify-center text-black dark:text-white`（每项占半宽，高 28px） | :39-47 |
| item 激活 | `border-b-2 border-light3-primary text-light3-primary dark:border-dark3-primary dark:text-dark3-primary`（2px 主题色下边框 + 主题色字） | :39-47 |

#### 3.2 type=button（胶囊式）

| 部位 | 类名 | 📍出处 |
|---|---|---|
| wrapper | `font-bold text-xs border rounded-full border-light3-primary dark:border-gray-1 border-2` | Tabs.tsx:48-58 |
| item 通用 | `w-[120px] h-[26px] rounded-full text-black dark:text-white` | :48-58 |
| item 激活 | `text-white bg-light3-primary dark:text-black dark:bg-dark3-primary`（主题色实色填充） | :48-58 |

#### 3.3 红点 / 额外内容

- 标签外层 `<span class="capitalize">`（:133）。
- `reddot` 为真时加伪元素红点：`before:absolute before:-right-3 before:-top-1 before:h-2 before:w-2 before:rounded-full before:bg-red-1 dark:before:bg-green-3`（亮红暗绿，:137）。
- `item.extra` 渲染在标签后（:142）。

#### 3.4 TabsWithIndicator（带滑动下划线）

在 default/button 基础上额外渲染绝对定位下划线：`absolute bottom-0 h-[3px] w-4 rounded-full bg-light3-primary dark:bg-dark3-primary transition-all duration-300`（:231-234），用 ref 测当前 tab 居中位置动态设 `left`（:170-182）。

#### 3.5 DOM 结构（default）

```
<div class="font-bold text-sm flex justify-between {className}">
  <button|Link class="w-[50%] inline-flex h-7 items-center justify-center text-black dark:text-white
        {active? border-b-2 border-light3-primary text-light3-primary
                 dark:border-dark3-primary dark:text-dark3-primary}">
    <span class="capitalize {reddot? relative before:...红点}">{label}{extra}</span>
  </button|Link>
  ...
</div>
```

> item 可是 `button` 或 `link`（`as:'link'` 时渲染 `<Link>`，默认 `replace=true`，:72-96）。

#### 3.6 衍生：分段切换 pill 条（轻量 Tab 变体）

横向 pill 条做同类切换（如全屏页同级切换、筛选维度），常与下拉/筛选共用 chip 风格：

| 部位 | 类名 | 📍示例 |
|---|---|---|
| 容器 | `flex gap-2 overflow-x-auto hide-scrollbar`，可 `sticky top-11 z-10` | SiblingSwitcherStrip.tsx:124-126 |
| pill 选中 | `bg-light3-primary/20 text-light3-primary dark:bg-dark3-primary/20 dark:text-dark3-primary` | :147-148 |
| pill 未选 | `bg-black/4 text-black dark:bg-white/4 dark:text-white` | :149 |
| pill 几何 | `rounded-[50px]`，文字 `text-[12px] font-bold truncate` | :146、:168 |

#### 3.7 状态 / 🌗暗亮 / 📱端

active 见上；非 active 为黑/白字（`text-black dark:text-white`）。激活色亮紫暗粉。`default`（各占 50% 宽）适合 2 个对等分类；`button`（固定 120px）适合需边框强调的少量切换；`TabsWithIndicator` 适合需平滑过渡反馈。`reddot` 用于「该 tab 下有未读/新内容」。

---

### 4. 选择器 / 下拉 Select & Dropdown

> 🆕 版本判定：轻量选择器 **CommonSelectV2 > commonSelect**；菜单式 **DropdownV2 > Dropdown**（V1 业务 0 引用，仅 stories）。重型主入口 `Select` 唯一。三类按用途分：

| 类型 | 定位 | 何时用 |
|---|---|---|
| **Select**（4 套配色主题 + 搜索 + 移动端转抽屉） | 重型 | 选项多、需主题配色、可能要搜索 |
| **CommonSelectV2** 🆕（轻量 popover） | 轻量首选 | 选项不多、popover 风格小下拉（排序/筛选）|
| **Dropdown / DropdownV2** | 菜单 | 「更多操作」式菜单（含可点链接项），字号更小 |

#### 4.1 Select（带配色主题的下拉，主入口）

📍示例: `src/components/CoUI/Select/index.tsx` + `config.ts`

| 项 | 值 | 📍出处 |
|---|---|---|
| 外壳 | `relative w-36 cursor-pointer justify-center border text-xs`（144px 默认） | index.tsx:237-238 |
| 闭合圆角 | `rounded-full` | :243 |
| 展开圆角 | `rounded-tl-xl rounded-tr-xl`（上圆下方，与展开菜单拼一体） | :243 |
| `noBorder` 且未展开 | `border-transparent dark:border-transparent` | :240-242 |
| 触发行 | `relative flex items-center justify-between whitespace-nowrap px-2 font-bold capitalize` | :251-252 |
| 箭头 | `ChevronUpIcon h-6 w-6 shrink-0`，闭合态 `rotate-180`（默认朝下） | :266-272 |
| 下拉面板 | `absolute -left-px -right-px top-full z-[50] overflow-hidden rounded-bl-xl rounded-br-xl border border-t-0 capitalize` | :277-278 |
| 选项行 | `flex h-6 cursor-pointer items-center px-2 transition duration-300` + 选中态 `config.selectedClass` | :214-221 |
| 占位 | 单行省略 `line-clamp-1` | :93-97 |

**4 套配色主题**（`ISelectType`，每种含 light/dark 全套 background/font/border/select/hover 七项，config.ts:23-95）：

| type | 亮底 → 暗底 | 选中态 | 备注 |
|---|---|---|---|
| `secondary`(默认) | `bg-blue-3` → `bg-black` | 黑底白字 → `bg-dark3-secondary` 黑字 | 蓝/绿系 |
| `black` | (借用 secondary light) → `bg-black` | → `bg-gray-3` 黑字 | — |
| `pure` | `bg-light3-bg` → `bg-black` | 黑底白字 → `bg-gray-3` 黑字 | 纯黑白 |
| `transaction` | `bg-transparent` 两态 | 选中字 `text-light3-primary` / `text-dark3-primary` | hover `rounded-[4px]` |

**搜索框（hasFilter）**：`h-10 w-full rounded-lg`，亮 `bg-black/10` 暗 `dark:bg-white/10`，桌面 `sm:h-[30px]`；右侧空串 `SearchIcon`、有值 `CloseIcon` 清除（:175-206）。

**📱移动端**：`hasFilter && isMobile` 时下拉隐藏，改用底部抽屉 `MobileDrawer`，高度 `visualViewportHeight * 0.8 - offsetY`（:282、:293-318）。

#### 4.2 CommonSelectV2（轻量 popover 选择器）🆕

> 🆕 取代 commonSelect（V1，仅 2 处）。基于 `Popover` 而非自绘绝对定位。

📍示例: `src/components/CoUI/Select/commonSelectV2.tsx`

| 部位 | 类名 | 📍出处 |
|---|---|---|
| 触发器 | `flex items-center justify-between whitespace-nowrap rounded-lg border border-black/5 px-3 py-2 font-bold capitalize dark:border-white/5 sm:px-4` | :161-166 |
| 触发器文字 | `truncate text-xs font-medium text-black dark:text-white` | :167 |
| 箭头 | `ChevronUpIcon size-4 text-gray-3 dark:text-gray-1`，闭合 `rotate-180` | :170-176 |
| 弹层 | `z-[999] rounded-[14px] border border-black/5 bg-light3-smallPopupBg dark:border-white/5 dark:bg-dark3-smallPopupBg` | :180-185 |
| 弹层滚动 | `max-h-[60vh]`，内 `flex flex-col gap-1 px-2 py-3` | :191-195 |
| option 行 | `flex h-[30px] min-w-[130px] items-center rounded-lg px-2 text-xs font-medium transition duration-300 sm:hover:bg-black/10 dark:sm:hover:bg-white/10` | :108-115 |
| option 选中色 | `text-light3-primary dark:text-dark3-primary`，未选 `text-black dark:text-gray-3` | :112-114 |
| option 禁用 | `cursor-not-allowed` | :100-102 |

> 弹层默认 `autoPlacement`（bottom-start/end、top-start/end，:130-138）；移动端 pointerdown 关闭后 500ms 防抖避免重开（:72-84）。

#### 4.3 Dropdown / DropdownV2（菜单式，更小字号）

> 🆕 DropdownV2（基于 Mantine Menu）现役；V1（自绘 popover-菜单）仅作样板，业务 0 引用。

**DropdownV2** 📍示例: `src/components/CoUI/DropdownV2.tsx`

| 部位 | 类名 | 📍出处 |
|---|---|---|
| 容器 | `!rounded-lg border !border-black/4 bg-white !py-3 !px-2 !shadow-[0_4px_20px_0_rgba(0,0,0,0.10)] dark:!border-white/4 dark:bg-dark3-smallPopupBg` | :91 |
| item | `text-gray-0 dark:text-gray-3 font-medium !rounded-lg !p-2`，hover `[&[data-hovered]]:bg-black/4 [&[data-hovered]]:text-purple-1 dark:[&[data-hovered]]:bg-white/4 dark:[&[data-hovered]]:text-pink-1` | :94-100 |
| itemIcon / itemLabel | `size-4` / `text-xs` | :101-102 |

> 大量 `!important` 用于对抗 Mantine 内部样式；点外部/滚动自动关闭（:41-67）。

**Dropdown V1（样板，简记）**：触发标签 `flex items-center justify-between gap-1 whitespace-nowrap`，文字 `text-[8px] text-gray-1`；弹层 `z-[999] rounded-lg border border-black/5 bg-light3-smallPopupBg dark:border-white/5 dark:bg-dark3-smallPopupBg`；item `flex max-w-[178px] items-center rounded-sm px-1 text-[10px] transition duration-300 sm:hover:bg-black/10 dark:sm:hover:bg-white/20 text-black dark:text-gray-3`；支持 `href` item 渲染 `<Link>`，空菜单显示 `no_options_available`。📍示例: Dropdown.tsx:114-169

#### 4.4 衍生：右键 / 上下文菜单（弹层菜单模式）

portal 到 body、视口边界 clamp 的浮层菜单，可复用同套小浮层底色：

| 部位 | 类名 | 📍示例 |
|---|---|---|
| 菜单容器 | `fixed z-[1000] min-w-[160px] rounded-lg border border-black/5 bg-light3-smallPopupBg p-1 text-sm shadow-lg dark:border-white/5 dark:bg-dark3-smallPopupBg` | MoveNoteContextMenu.tsx:73 |
| 菜单项 | `rounded-md px-3 py-2 hover:bg-black/5 dark:hover:bg-white/10` | :73 |
| 危险项 | `text-red-500 hover:bg-red-500/10` | :140 |

---

### 5. 输入框 / 多行自适应文本 Input & Textarea

> 🆕 版本判定：CoUI `Textarea` V1 与 `TextareaV2`(4 处) 并存，V1 仍现役为主体。单行输入框无单一 canonical，三套并行按场景选。

#### 5.1 单行输入框（药丸形带边框）

最轻量原子输入框，`<label>` 包 `<input>`，支持 `prefix` 插槽。

| 项 | 值 | 📍出处 |
|---|---|---|
| 外壳 | `flex items-center gap-2.5 rounded-3xl border border-black bg-white px-4 py-1.5 dark:border-white` | Input.tsx:19-20 |
| 聚焦边框 | `focus-within:border-light3-primary dark:focus-within:border-dark3-primary` | :20 |
| input 本体 | `flex-1 border-none bg-transparent px-0 py-1 text-sm leading-6 placeholder-gray-1 outline-0 focus:ring-0` | :28-29 |
| autoComplete | `off`（硬写） | :31 |

📍示例: `src/components/CoUI/Form/Input.tsx`

```
<label class="flex items-center gap-2.5 rounded-3xl border border-black bg-white px-4 py-1.5
              focus-within:border-light3-primary dark:border-white dark:focus-within:border-dark3-primary">
  {prefix}
  <input class="flex-1 border-none bg-transparent px-0 py-1 text-sm leading-6
                placeholder-gray-1 outline-0 focus:ring-0" autocomplete="off" />
</label>
```

> 🌗 亮：白底黑边；暗：白边（透出页面背景）。focus 切主题色边框。原生药丸样式适合搜索/筛选行内输入；卡片化表单里常被覆盖成 5.2 的扁平样式。

#### 5.2 扁平半透明灰底输入（卡片表单内，可复用）

卡片化表单里输入框统一「无边框 + 半透明灰底 + 大圆角」。可复用片段（`FLAT_INPUT_CN`）：

```
h-[44px] rounded-[12px] border-0 bg-black/4 px-4 py-0 text-black
placeholder:text-gray-2 dark:bg-white/4 dark:text-white dark:placeholder:text-gray-1
```

📍示例: BasicInfoSection.tsx:41-42（另：圆角档 `rounded-xl`，蒙层 `bg-opacity-5` 变体见 NameField.tsx:72）

> 🌗 亮：黑 4%~5% 蒙层底；暗：白 4%~5% 蒙层底。📱 PC/移动同款扁平（卡片背景才分端）。

**统一错误态输入框**（不用红警告色描边，而是「半透明红框 + 红底蒙层」）：

```
border border-red-6/50 bg-red-6/20 dark:border-red-6/50 dark:bg-red-6/15
```

📍示例: BasicInfoSection.tsx:276、NameField.tsx:74（`red-6=#FF4444`；个别场景例外用 `ring-1 ring-red-1`）

#### 5.3 多行文本域 Textarea（受控截断 + 内置计数）

固定样式 + 内置 maxLength 截断 + 可选计数/错误行。

| 项 | 值 | 📍出处 |
|---|---|---|
| 本体 | `rounded-3xl border border-black p-4 text-sm leading-tight placeholder-gray-1 outline-0 focus:border-light3-primary focus:ring-0 dark:border-white dark:focus:border-dark3-primary` | Textarea.tsx:42 |
| error 边 | `errText` 时叠 `!border-red-1` | :43 |
| 截断逻辑 | onChange 内 `length >= maxLength` 即 `slice(0,maxLength)`；`emojiSplit` 时按 code point 截 | :24-39 |
| 计数/错误行 | `mt-2 flex justify-between text-sm`，左 `text-red-1` 错误、右 `text-gray-1` 计数 `{len} / {max}` | :47-57 |

📍示例: `src/components/CoUI/Form/Textarea.tsx`

```
<textarea class="rounded-3xl border border-black p-4 text-sm leading-tight placeholder-gray-1
                 outline-0 focus:border-light3-primary focus:ring-0
                 dark:border-white dark:focus:border-dark3-primary" />
<div class="mt-2 flex justify-between text-sm">   // showLength || errText
  <span class="self-start text-red-1">{errText}</span>
  <span class="self-end text-gray-1">{len} / {max}</span>
</div>
```

**🆕 TextareaV2（扁平变体，并存）**：更圆润扁平、无内置字数条：`resize-none rounded-lg border border-gray-3 bg-white px-4 py-3 text-sm leading-tight tracking-[.015rem] text-black outline-0 focus:ring-0 dark:border-black-2 dark:bg-black-2 dark:text-gray-3`。暗态背景 `bg-black-2`(`#363234`)。📍示例: TextareaV2.tsx:16-17

#### 5.4 自适应高度文本域（Auto-resize）

按机制分三种实现，按场景选：

| 机制 | 行为要点 | 📍示例 |
|---|---|---|
| **隐藏镜像测高** | `hiddenRef` 隐藏 textarea 写入相同 value，读 `scrollHeight` 反推高度；支持 `showLength`/`emojiSplit`/`errText`/`longpressSelectAll`(长按 800ms 全选)。本体 `w-full resize-none focus:ring-0` | AutoTextarea.tsx:55-69、:88-107、:132 |
| **行数测量库式** | `calculateNodeHeight`+`getSizingData`，按 `minRows/maxRows` 钳行数；`setProperty('height',...,'important')` 强写；监听 resize+字体加载重测 | AutosizeTextarea/index.tsx:80、:113-114 |
| **行高换算式** | `minRows=2 / maxRows=4 / defaultHeight=20`；rAF 内先 `height:auto` 重置再读 `scrollHeight`，按 `lineHeight`+padding+border 钳 min/max | TextareaAutoLine.tsx:16 |

> 用途：聊天输入框、动态高度长文本输入用自增高；标签输入（见 §10）内部即复用「行高换算式」。

---

### 6. 字数计数 Char Counter

结构高度雷同的轻量计数器，按归属选用。

| 文案格式 | 样式 | 📍示例 |
|---|---|---|
| `{count} / {maxCount} {t('chars')}` | `flex text-xs leading-tight text-gray-2` | CharCount.tsx:16-22 |
| `{count}/{maxCount}` 或 `t('x_chars',{count})` | `text-xs text-black-2 dark:text-gray-1` | CreateModelV2/CharCount.tsx:15-19 |
| `{len}/{max} {t('base_characters')}` | `mt-1 text-sm text-gray-1` | BaseInput.tsx:113-118 |

**通用约定**：

- 位置一律右对齐（外层 `flex justify-end` 或 `text-right`）。
- 文字尺寸普遍 `text-xs`(12) 或 `text-[10px]`（卡片表单计数更小）。
- **满额/分阶段标红**：到顶时计数变 `text-red-6`，普通态 `text-gray-2 dark:text-gray-1`。📍示例: BasicInfoSection.tsx:668-670
- **三阶段色**（按字数阈值，如 ≥4000 danger / ≥3700 warning / else normal）：normal `text-[#7976ff]` / warning `text-[#fff1a7]` / danger `text-[#f44]`。容器 `flex items-center gap-1 text-[10px]`。📍示例: CharCountIndicator.tsx:26、:40-41

---

### 7. 图片上传位 Image Upload

> 🆕 版本判定：比例自适应矩形位 **ImageUploadField（四态机）** 为最完整新版；圆形头像上传为老通用版，按形状需求各取其一。

#### 7.1 比例自适应矩形封面（四态机）🆕

**四状态**：`empty` / `loading` / `uploaded` / `error`，比例 prop 决定框尺寸。

📍示例: `src/components/WorldCard/ImageUploadField.tsx:592`

**外框**：

```
relative isolate flex w-full items-center justify-center overflow-hidden
rounded-[14px] border bg-black/4 transition-colors dark:bg-white/4
```

**比例占位用 padding-bottom 百分比**（不用 `aspect-ratio`——flex+绝对定位下 aspect 会塌成 0）：

| 比例 | 框宽 | padding-bottom（撑高） | 📍出处 |
|---|---|---|---|
| 3:4 | `w-[150px]` | `pb-[133.3333%]` | :122/132 |
| 9:16 | `w-[180px]` | `pb-[177.7778%]` | :124/133 |
| 2:1 | `w-[400px]` | `pb-[50%]` | :126/134 |
| 1:1 | `w-[200px]` | `pb-[100%]` | :127/135 |

**四态视觉**：

| 态 | 表现 | 📍出处 |
|---|---|---|
| empty | 虚线框 `border-dashed`，中央 50×50 加号 SVG（`text-gray-2 dark:text-white`）+ prompt 文字（仅 PC，`hidden md:flex`） | :628-667 |
| loading | 立即回显本地 blob 图 + 底部黑渐变蒙层 `bg-gradient-to-b from-transparent to-black/50` + 右下白色 spinner `size-6 fill-white text-white/50` | :670-688 |
| uploaded | `object-cover` 满铺 + 右下 `size-6` 裁剪圆钮（`bg-gray-5 text-gray-0 dark:bg-lp_bg2 dark:text-gray-3` + `CropFrameIcon size-4`）+ 右上 `size-6` 删除（`CloseCircleIcon`，`text-gray-3 dark:text-gray-1`） | :690-739 |
| error | 图 + 黑渐变 + 底部「上传中断」白字 `text-base font-semibold capitalize text-white` + Retry 药丸 `h-10 w-[100px] rounded-[25px] bg-light3-primary text-white dark:bg-dark3-primary` + 右上删除 | :741-787 |

**拖拽态边框**（`dragBorder`，:585-590）：normal `border-black/4 dark:border-white/4` / valid `border-light3-primary dark:border-dark3-primary` / invalid `border-red-6/50 bg-red-6/15`。

> 📱 PC 支持拖拽 + 框内大字 prompt；移动端空态只留加号图标（拖拽是桌面语义）。加载失败回退占位图。

#### 7.2 圆形头像上传（老通用版）

圆形头像预览 + 文件选择按钮。

| 项 | 值 | 📍出处 |
|---|---|---|
| 头像图 | `h-32 w-32 cursor-pointer rounded-full object-cover` + `border-0 dark:border-2 dark:border-white` | BaseImageUpload.tsx:83 |
| 占位默认图 | 默认图 + 中央 50×50 刷新 SVG（白）+ 右下相机 SVG（`text-light3-primary dark:text-dark3-secondary`） | :89-133 |
| 上传按钮 | `ml-4 flex cursor-pointer items-center rounded-3xl bg-light3-primary px-8 py-2 text-sm font-semibold text-white shadow-sm group-hover:brightness-110 dark:bg-dark3-primary dark:text-black`；loading 叠 `bg-pink-1/80` | :136-137 |
| 隐藏 file input | `absolute left-0 top-0 ... opacity-0 cursor-pointer`，`accept="image/*"` | :155-158 |

📍示例: `src/components/BaseComponents/BaseImageUpload.tsx`

> 文件校验：用 magic number 确认是图片，否则 toast 报错（:177-200）。🌗 暗色头像加 2px 白边；按钮亮紫底白字 / 暗粉底黑字。
> 选型：固定圆形位（用户/角色头像）用圆形头像版；按场景比例自动裁剪的矩形封面用 7.1 四态机。

---

### 8. 滑块 Slider

基于 Mantine `createStyles`，两个 variant：`default`（带可拖拽 thumb 的通用滑块）/ `volume`（无 thumb 的纯填充进度条）。

📍示例: `src/components/CommonStyles/slider.ts`

#### 8.1 default（通用滑块）

| 部位 | 值 | 📍出处 |
|---|---|---|
| thumb | `1.25rem × 1.25rem` 圆，无边，背景 = `defaultColor` | slider.ts:34-40 |
| defaultColor | disabled `#707070` / 暗 `#FF8ADC` / 亮 `#D7D6FF` | :18 |
| track 高 | `0.25rem`，`:before` 轨道 `#707070` opacity 0.5 | :45、:56-60 |
| bar | 背景 `defaultColor` | :74-77 |

#### 8.2 volume（音量专用，无 thumb）

| 部位 | 值 | 📍出处 |
|---|---|---|
| thumb | 尺寸全归零、`opacity:0`（无 thumb） | :25-33 |
| track 高 | `0.75rem`（12px）+ `borderRadius:10px` | :46-48 |
| 轨道 `:before` | 暗 `rgba(255,255,255,0.10)` / 亮 `rgba(0,0,0,0.10)`，`borderRadius:10px` | :49-56 |
| bar | volumeColor + `borderRadius:'40px 0 0 40px'`（左圆右直） | :69-74 |
| volumeColor | 暗 `#FF8ADC` / 亮 `#B376FF` | :21 |
| label | `color:#000` 背景 defaultColor，`fontWeight:500 fontSize:0.875rem padding:0.25rem 0.5rem` | :62-68 |

> 🌗 颜色直接按 `theme.colorScheme === 'dark'` 切（:16）。`volume` 给纯填充进度条样式；其它进度型滑块用 `default`。

---

### 9. Radio / Checkbox

> 🆕 版本判定：Radio **V1（16 处，主流）> RadioV3（6 处，胶囊新版）> RadioV2（2 处）**。规范主体写 V1，V3 作「分段选择器」外观备选。
> 实现套路统一：隐藏原生 `<input class="peer hidden">` + `peer-[:checked]` 切换两个图标 span。

#### 9.1 Radio（单选，圆点式）

| 项 | 值 | 📍出处 |
|---|---|---|
| 包裹 label | `group flex w-full items-center gap-5`；`cursor-pointer` / disabled `cursor-not-allowed` | Radio.tsx:45-49 |
| 图标 span 尺寸 | `h-5 w-5 shrink-0`（20px） | :41 |
| 选中色 | `text-light3-primary dark:text-dark3-primary`（disabled→`text-gray-500`，未选→`text-gray-1`） | :41 |
| 选中态 | `peer-[:checked]:block` 显示 `CheckCircleIcon`，内嵌白色圆点 `size-4/5 rounded-full bg-white` | :65-74 |
| 未选态 | `peer-[:checked]:hidden` 显示 `UncheckCircleIcon` | :75-86 |
| label 文字 | `leading-6 text-sm text-gray-900 dark:text-gray-100` | :87-96 |

📍示例: `src/components/CoUI/Form/Radio.tsx`

> `onValueChange?.(value)` + `stopPropagation` 防 label→input 冒泡双触发（:59-63）。

**🆕 RadioV3（胶囊/分段选择器外观）**：不画圆点，整个 label 变胶囊。

```
h-8 rounded-3xl px-4 py-2 min-w-[100px] sm:min-w-[120px]
选中: bg-light3-primary/20 text-light3-primary dark:bg-dark3-primary/20 dark:text-dark3-primary
未选: bg-black/4 text-gray-1 dark:bg-white/4 dark:text-gray-2
```

label 文字 `font-roboto text-sm font-medium`。📍示例: RadioV3.tsx:42-50、:84

#### 9.2 Checkbox（多选）

同 peer 模式，支持 `type:'circle'|'square'`（默认 circle）和 `theme:'primary'|'secondary'`（默认 secondary）。

| 项 | 值 | 📍出处 |
|---|---|---|
| 图标尺寸 | `size-5 shrink-0`（20px） | Checkbox.tsx:74-76 |
| theme primary | `text-light3-primary dark:text-dark3-primary` | :28 |
| theme secondary（默认） | `text-light3-secondary dark:text-dark3-secondary`，disabled→`text-gray-1` | :30-31 |
| circle 选中/未选 | `CheckCircleIcon` / `UncheckCircleIcon` | :84/103 |
| square 选中/未选 | `CheckSquareIcon` / `UncheckSquareIcon`（disabled→`DisableCheckSquareIcon`） | :82/96-99 |
| label | `leading-6 text-sm text-gray-900 dark:text-gray-100`，有 label 时 `ml-2.5` | :106-115 |

📍示例: `src/components/CoUI/Form/Checkbox.tsx`

#### 9.3 衍生：多选勾选框矢量（列表多选用）

列表 manage 多选的方块勾选矢量，PC/mobile 共用：

- 选中：`viewBox 0 0 20 20`，主题色填充方块（`fill currentColor`）+ 白描边勾（`stroke #FFFFFF strokeWidth 2.08333`），`size-5 text-light3-primary dark:text-dark3-primary`。
- 未选：描边圆角方框（`stroke currentColor strokeWidth 1.5`），`size-5 text-gray-2 dark:text-gray-1`。

📍示例: NoteEntryCard.tsx:479（选中）/ :500（未选）

---

### 10. 标签输入 Tag / Chip Input 🆕

外框灰底 + 框内 chips 流式排列 + 框内自适应高 textarea 输入。

📍示例: `src/components/WorldCard/KeywordChipInput.tsx:182`

| 部位 | 样式 | 📍出处 |
|---|---|---|
| 外框 | `flex min-h-[44px] w-full cursor-text flex-col justify-center gap-2 rounded-[12px] bg-black/4 p-[9px] dark:bg-white/4`（空态对齐 44px） | :186 |
| error 态 | 叠 `border border-red-6/50 bg-red-6/20 dark:border-red-6/50 dark:bg-red-6/15` | :188-189 |
| chips 容器 | `flex flex-wrap gap-2`（chips.length>0 时渲染） | :203 |
| chip | `inline-flex min-h-[30px] max-w-full items-center gap-1 rounded-full bg-black/4 px-3 py-1 text-xs font-medium text-gray-1 dark:bg-white/4 dark:text-gray-2` | :199 |
| chip 删除 | `size-3 text-gray-1 dark:text-gray-2` + `CloseIcon size-3` | :212-214 |
| 输入 textarea | `w-full resize-none overflow-hidden border-0 bg-transparent p-0 text-sm leading-[23px] text-black outline-0 placeholder:text-gray-2 focus:ring-0 dark:text-white dark:placeholder:text-gray-1`（自适应高，复用 §5.4 行高换算式） | :254 |
| footer 计数 | `text-[10px] font-medium text-light3-primary dark:text-dark3-primary`（`{n}/12 keywords` 等格式） | :263 |

**DOM 结构**：

```
<div class="flex flex-col gap-1 md:gap-3">
  <div class="flex min-h-[44px] flex-col justify-center gap-2 rounded-[12px] bg-black/4 p-[9px] dark:bg-white/4">  ← 外框
    {chips.length>0 && <div class="flex flex-wrap gap-2">{chips}</div>}
    {!满上限 && <textarea ... />}                      ← 输入框(自适应高)
  </div>
  <div class="flex justify-between">
    <span class="text-[10px] font-medium text-light3-primary dark:text-dark3-primary">{n}/12 keywords</span>
  </div>
</div>
```

**行为约定**（可复用）：逗号(半/全角)/回车 提交 chip；单条上限 100 字、最多 N 条、重复不新增（大小写不敏感）；达上限隐藏输入框；支持 IME 组合输入保护。长 tag 在 chip 内 `break-all` 断行不撑破框。

> 🌗 框/ chip 走 `black/4 ↔ white/4` 成对蒙层。📱 PC/移动同款框样式。

---

### 附：版本判定汇总（🆕 取最新版）

| 控件族 | canonical（本章主体） | 弃用/局部新版 |
|---|---|---|
| 按钮 | 基础 Button（配色与几何分离，唯一） | — |
| 开关 | **Switch2**（13 处） | Switch V1（Mantine，5 处旧调用）|
| 标签页 | Tabs（default/button）+ TabsWithIndicator | — |
| 选择器（重型） | Select（4 套配色主题 + 搜索 + 移动抽屉，主入口） | — |
| 选择器（轻量） | **CommonSelectV2** | commonSelect V1（2 处）|
| 下拉菜单 | **DropdownV2**（Mantine Menu，现役） | Dropdown V1（自绘样板，业务 0 引用）|
| 多行文本（CoUI） | Textarea V1（受控截断 + 内置计数） | TextareaV2（4 处，扁平变体，并存）|
| Radio | **Radio V1**（16 处，圆点） | RadioV3（6 处，胶囊）/ RadioV2（2 处）|
| 图片上传 | **ImageUploadField**（四态比例自适应） | 圆形头像上传（老通用，仍在用）|
## 二、浮层 Overlays

「悬浮在常规文档流之上」的一切容器。它们共享一条**统一的 z-index 递增机制**（下文 §2.0），但在「锚点、定位、遮罩、动画、移动端形态」上分七类，各有不同语义。轴：🌗 暗/亮（双值）· 📱 PC/移动 · 🆕 取最新版为准。

### 概览选型

| 类别 | 何时用（一句话语义） | 锚点 | 遮罩 | 进出动画 | 移动端 | 最新版 |
|---|---|---|---|---|---|---|
| **Modal 弹窗** | 打断用户、必须做决策（确认/表单/选择） | 屏幕居中 | 有 `bg-black/50` | zoom + fade | 可退化成底部抽屉 | V1 canonical 🆕 |
| **Drawer 抽屉** | 侧边长内容 / 移动端从底滑出 | 屏幕某一边 | 有 `bg-black/50` | 平移 slide | 边可配 bottom（bottom-sheet） | 单版本 |
| **Popover 气泡** | 点/悬浮触发的轻量补充信息（可含可点元素） | 触发元素 | 无 | opacity 过渡 | 同 PC | 单 canonical（floating-ui） |
| **Tooltip 提示** | 单条文字/简短引导气泡 | 触发元素 | 无 | opacity 过渡 | tap 触发（非 hover） | TooltipV2 🆕 |
| **Toast 轻提示** | 操作结果反馈、不打断 | 顶部居中 / 锚点 | 无 `pointer-events-none` | 上滑进出（CSS class） | 同 PC | 单版本 |
| **PopupMenu 上下文菜单** | 右键 / 「更多」按钮触发的操作列表 | 触发元素 / 坐标 | 无 | 无 / scale | 同 PC | Menu v2 🆕 |
| **ImagePreview 图片预览** | 全屏沉浸式图集浏览 | 全屏铺黑 | 整屏黑底（即遮罩） | swiper 横滑 | 完整触摸手势 | 单版本 |

---

### 2.0 z-index 层级机制（全局统一）

所有浮层的层级**不写死** tailwind `z-*`，而由一个全局自增计数器分配——是读懂「谁压谁」的前提。

**机制**：
- store：zustand，`zIndex` 初始值 **100**，`increaseZIndex()` 每次 +1。
- hook（`useZIndex`）：组件传入 `isOpen`；当 false→true 时把当前 `zIndex+1` 锁进本组件的 `currentZIndex`，并推高全局计数。
- 效果：后打开的浮层 z-index 永远比先打开的高 1。Modal / Drawer / Popover / ImagePreview 都走这套。
- 写入方式：作为 **inline style** 写到浮层根节点（`style={{ zIndex }}`），不是 class。

> ⚠️ **重要后果**：因为走 inline style 且 ≥100 起步，在 `floatingClassName` 上写 tailwind `z-*` **无效**（inline style 优先级更高会覆盖）。要调浮层层级只能靠**打开顺序**，不能靠 class。

**写死的 z-index（少数特例，绕过 useZIndex 直接用 tailwind `z-[...]`）**：

| z 值 | 用途 |
|---|---|
| `z-[9999]` | Toast 容器（要盖一切）；图片预览的拖拽跟手图层 |
| `z-[1000]` | portal 到 body 的右键上下文菜单 |
| `z-[999]` | 「更多」菜单气泡容器 |
| `z-[700]` | 菜单项内 tooltip |
| `z-10` | 浮层内部相对层（关闭按钮等） |

📍示例: store 初始值 100 / 每次 +1 (`src/store/zIndex.ts:7-12`)；hook (`src/hooks/useZIndex.tsx:7-30`)；inline style 无效说明 (`WorldCard/FieldInfoPopover.tsx:14-17`)；Toast/跟手图 `z-[9999]` (`CoUI/Toast/ToastProvider.tsx:187`、`CoUI/ImagePreviewModal/ImagePreviewModal.tsx:517`)。

---

### 2.1 Modal 弹窗（基础底座）🆕

**何时用**：需要用户明确决策（删除确认、年龄确认、登录）、承载表单、聚焦的中等内容。不该用：纯信息反馈（→ Toast）、依附按钮的轻提示（→ Popover/Tooltip）、移动端从底滑出的长列表（→ Drawer 或给 Modal 开 `mobileDrawer`）。

🆕 **版本结论**：canonical 是**基础 Modal（V1，default export）**，全站大量 import。基础 `ModalV2` 仅 1 处使用、近乎弃用，规范只写 V1。（注意 grep `*ModalV2` 命中的 `ChangeModelModalV2` 等是业务弹窗命名，与 CoUI 基础 ModalV2 无关。）

底层基于 `rc-dialog`；命令式 `show()` 唤起为主流写法。

**视觉规格（DefaultClassNames 默认槽位）**：

| 槽位 | 类名（真实） | 关键规格 |
|---|---|---|
| `dialog`（外层） | `relative -mt-[30px] max-w-[calc(100vw_-_32px)] sm:mx-auto px-0` | 视口宽减 32px 上限；上移 30px |
| `wrapper`（定位） | `fixed inset-0 flex items-center justify-center` | 全屏 fixed + flex 居中 |
| `content`（卡片） | `relative mx-auto flex flex-col max-h-[80vh] w-full max-w-full rounded-2xl border border-white/10 bg-white p-5 supports-[max-height:100dvh]:max-h-[90dvh] dark:bg-black-6 sm:p-10` | 圆角 16px；最大高 80vh（支持 dvh 则 90dvh）；padding 移动 20px / PC 40px |
| `header`（标题） | `flex-shrink-0 text-center text-base font-bold leading-5 text-black dark:text-white` | 居中、16px 粗体 |
| `mask`（遮罩） | `fixed inset-0 bg-black/50` | 黑 50% |
| `body`（内容） | `overflow-x-hidden overflow-y-auto text-black dark:text-gray-3 mt-3 sm:mt-5 flex-1 flex items-stretch` | 纵向滚动；上间距移动 12px / PC 20px（无 title 时归 0） |
| `footer`（按钮区） | `flex gap-x-2 sm:gap-x-4 flex-shrink-0 justify-center` | 按钮居中，间距移动 8px / PC 16px |

- **关闭按钮**：`absolute right-3 top-3 z-10 h-6 w-6 text-gray-1 sm:right-4 sm:top-4`（24×24，移动 12px / PC 16px）。
- **宽度**：默认 `DEFAULT_WIDTH = 600`；`width` 直传，或 `size` 枚举（已 `@deprecated`，建议用 `width`）映射 `xs:80 sm:96 md:448 lg:512 xl:576 2xl:672 3xl:768 5xl:1100`。
- **Footer 容器**：`mt-6 flex w-full flex-col gap-y-2 sm:mt-10 sm:gap-y-3`，支持 `footerBefore`/`footerAfter`（字符串渲染成 `text-[10px] leading-none text-gray-1` 居中小字）。

**DOM 结构**：
```
rc-dialog-root
└─ wrapper  (fixed inset-0 flex items-center justify-center)
   └─ dialog  (relative -mt-[30px] max-w-[calc(100vw-32px)])
      └─ content  (rounded-2xl border border-white/10 bg-white dark:bg-black-6 p-5 sm:p-10)
         ├─ CloseIcon  (absolute right-3 top-3 h-6 w-6)
         ├─ header  (text-center text-base font-bold)        ← title
         ├─ body  (overflow-y-auto flex-1)
         │  └─ <div class="w-full">{children}</div>
         └─ footer  (flex gap-x-2 sm:gap-x-4 justify-center)  ← 取消/确认
mask  (fixed inset-0 bg-black/50)
```

**进出动画**：
- 卡片 `transitionName="zoom"` — `antZoomIn`（scale 0.2→1 + opacity 0→1，0.3s）/ `antZoomOut`，缓动 `cubic-bezier(0.08,0.82,0.17,1)`。
- 遮罩 `maskTransitionName="fade"` — `FadeIn`/`FadeOut`，0.2s linear。

**🌗 暗/亮**：卡片底 `bg-white` → `dark:bg-black-6`；标题 `text-black` → `dark:text-white`；正文 `text-black` → `dark:text-gray-3`；遮罩两模式同为 `bg-black/50`。

**📱 PC / 移动**：
1. padding/间距用 `sm:` 加大（content `p-10`、body `mt-5`、footer gap 16px）。
2. **退化成抽屉**：传 `mobileDrawer` 时，移动端整个 Modal 改渲染成底部抽屉（默认 `drawerPlacement='bottom'`，bottom-sheet）；按钮变 ok flex-1 basis-2/3 + cancel basis-1/4 横排，header `p-5 pb-2`、body `px-5`、footer `p-5 pt-6`。

**显隐 / 唯一性**：默认 `autoNice=true`（绑 NiceModal，`mergedOpen = niceModal.visible`）；`uniqueKey` 防同 key 重复弹出（含 1 小时未用 key 的定期清理）；open 时全局遮罩广播（emit `ADD_GLOBAL_MASK_IDS`，卸载 emit `REMOVE`）。

**命令式 helper（Confirm 家族，无需 `create()` 包裹）**：
- `Modal.confirm` / `Modal.asyncConfirm` — 普通二次确认（async 版 resolve `true/false/undefined`）。
- `Modal.dangerConfirm` / `Modal.asyncDangerConfirm` — **红色警示**二次确认（危险/破坏性，如删除）。
- `Modal.destroyAll()` — 销毁所有。
- `contentAlign: 'left'|'center'`、`footerDirection: 'row'|'column'|'column-mobile'`。

📍示例: 默认类名 (`CoUI/Modal/Modal.tsx:50-74`)；关闭按钮 (`Modal.tsx:191-201`)；宽度/size 映射 (`Modal.tsx:63-74`)；Footer 容器 (`Modal/shared.tsx:91-99`)；动画 (`Modal/style.css` + `Modal.tsx:350-351`)；mobileDrawer 退化 (`Modal.tsx:131-333`)；uniqueKey/清理 (`Modal.tsx:134-172`)；遮罩广播 (`Modal.tsx:215-224`)；Confirm 家族 (`Modal/index.tsx:67-86`、`interface.ts:171-172`)。

---

### 2.2 Drawer 抽屉

**何时用**：左右侧栏面板、移动端底部操作面板/长列表（bottom-sheet）、需侧滑手势关闭、需保留部分主页面上下文的内容。不该用：强决策小弹窗（→ Modal.confirm）、轻提示（→ Toast）。

🆕 无版本分歧，单一 canonical。底层基于 `rc-drawer`，prefixCls `co-drawer`。`MobileDrawer`（Modal 的移动退化态）就是对它的封装。

**视觉规格**：

| 槽位 | 类名（真实） |
|---|---|
| `mask` | `absolute inset-0 bg-black/50 pointer-events-auto` |
| `content` | `flex flex-col w-full h-full overflow-auto pointer-events-auto dark:bg-black-3 bg-white-2` |
| `wrapper`（按 placement 贴边） | `absolute` + `left-0 top-0 bottom-0`(left) / `right-0 top-0 bottom-0`(right) / `left-0 right-0 top-0`(top) / `left-0 right-0 bottom-0`(bottom) |
| `rootClassName` | `pointer-events-none fixed inset-x-0 top-0 h-screen supports-[height:100dvh]:h-dvh` |

**Panel 内部**：
- header `relative flex items-center justify-center p-4 pb-0`，title `text-black dark:text-white font-bold`。
- 关闭按钮 `absolute top-4 ltr:right-4 rtl:left-4`，按钮本体 `text-gray-2`。
- 侧滑手柄（仅 `swipeToClose`）：`mx-auto mt-2 h-1 w-9 shrink-0 rounded-full bg-black/10 dark:bg-white/20`。

**进出动画**：遮罩 `mask-motion` opacity 0↔1（`transition: all 0.3s`）；面板 `panel-motion-{left|right|top|bottom}` 平移 `translateX/Y(±100%) ↔ none` + opacity 0.7↔1（`all 0.3s`）。

**移动端 bottom-sheet（MobileDrawer 封装）**：`placement='bottom'` 时 content 加 `rounded-t-[20px]`（顶部圆角 20px，其余边对应圆角）；最大高 `max-h-[90vh]`（支持 dvh 则 90dvh）；header `sticky top-0`、footer `sticky bottom-0 bg-light3-bg dark:bg-dark3-bg`。

**手势与边界**：
- `swipeToClose`：仅 `placement==='bottom'` 生效；下滑超阈值（`clientHeight*0.25`，clamp 100~180px）即关闭，收尾动画对齐 rc-drawer 的 300ms leave。
- `preventMaskScroll`：iOS 橡皮筋滚动修复，给 mask 加非 passive touchmove 监听。
- RTL：方向为 rtl 时加 `.rtl` class。

**🌗 暗/亮**：content 底 `bg-white-2` → `dark:bg-black-3`（注意与 Modal 的 `black-6` 不同）；title `text-black` → `dark:text-white`；MobileDrawer footer `bg-light3-bg` → `dark:bg-dark3-bg`。

📍示例: 默认类名 (`CoUI/Drawer/index.tsx:364-386`)；Panel (`CoUI/Drawer/DrawerPanel.tsx:94,110,153`)；动画 (`Drawer/style.css`)；bottom-sheet (`Modal/MobileDrawer.tsx:70-92`)；swipeToClose (`Drawer/index.tsx:195-337`)；preventMaskScroll (`index.tsx:158-193`)；RTL (`index.tsx:83`)。

---

### 2.3 Popover 气泡

**何时用**：字段 ⓘ 说明气泡、「更多」下拉菜单、需要箭头指向触发源的补充信息（比 Tooltip 能放更多内容、含可点元素）。无遮罩，点外部自动关（`useDismiss`）。不该用：纯 hover 单行文字（→ TooltipV2 更轻）、需遮罩的决策（→ Modal）。

🆕 canonical 是基于 `@floating-ui/react` 的 **CoUI Popover**。另有两个**底层不同**的同名物，勿混为版本：彩色提示气泡（§2.3.1，再封装本组件）、PopupMenu（基于 `@mantine/core`，见 §2.6）。

**视觉规格（默认气泡体）**：
```
break-words rounded border border-white bg-purple-2 p-2 text-xs leading-normal
text-black dark:border-gray-1 dark:bg-black-2 dark:text-gray-3
```
（圆角 4px、padding 8px、12px）

**箭头**：`absolute h-2 w-2 rotate-45 border bg-purple-2 dark:bg-black-2`（8×8 旋转 45° 方块），按 placement 给三面透明/两面着色的边框，底色默认 `border-t-white dark:border-t-gray-1` 等。

**定位机制（floating-ui middleware）**：
- `offset({ mainAxis: gap=8, crossAxis })` — 与触发元素间距默认 8px。
- `shift({ padding: 8 })` — 防贴边。
- `size(...)` — 可选 `autoWidth`（同宽触发元素）+ 自动 maxWidth/maxHeight（可视区减 8px padding）。
- `autoPlacement`（可选）— 自动选最佳方向。
- `arrow({ element, padding })`。

**交互**：`useClick`（默认开）/ `useHover`（`hoverable`，带 `safePolygon()` 防误关）/ `useDismiss`（pointerdown 点外关）/ `useRole`；`initialFocus=-1` 可让 input 触发时不抢焦点。

**DOM 结构**：
```
FloatingPortal
└─ FloatingFocusManager (returnFocus=false)
   └─ <div style={{...floatingStyles, zIndex}}>          ← 定位层（zIndex 来自 useZIndex）
      └─ <div style={transitionStyles} class="...rounded border bg-purple-2 p-2 text-xs...">
         ├─ {children}
         └─ <span ref=arrowRef class="absolute h-2 w-2 rotate-45 border bg-purple-2">  ← 箭头
```

**进出动画**：`useTransitionStyles` — floating-ui 默认 opacity 过渡。

**🌗 暗/亮**：气泡底 `bg-purple-2` → `dark:bg-black-2`；边 `border-white` → `dark:border-gray-1`；文字 `text-black` → `dark:text-gray-3`。

📍示例: 气泡体 (`CoUI/Popover.tsx:378-403`)；箭头着色 (`Popover.tsx:240-284`)；定位 middleware (`Popover.tsx:101-151`)；交互/initialFocus (`Popover.tsx:54-64`)；动画 (`Popover.tsx:307`)。

#### 2.3.1 彩色提示气泡（强调色变体）

基于 CoUI Popover 再封装的**红/绿强调色提示气泡**，自带 SVG 三角箭头（viewBox `0 0 15 10`，`fill=currentColor`）。

**何时用**：带强调色/需引导注意的提示（错误、新功能引导），区别于中性紫底的基础 Popover。

- 气泡体：`break-normal border-none bg-[#E4221A] p-1 font-bold text-white dark:bg-green-3 dark:text-black`（红底白字 → 暗绿底黑字）。
- 箭头着色：`text-[#E4221A] dark:text-green-3`，按 placement 旋转。
- 支持 `autoClose`（5s 自动关）、`delayOpen`（延时打开）。
- 配色枚举 3 套：A=`bg-yellow-2 text-white`、B=`bg-purple-4 text-yellow-1`、C=`bg-green-3 text-black-3`。

📍示例: 封装体/箭头/autoClose (`components/Popover/index.tsx:96-98,142-158`)；配色枚举 (`components/Popover/style.ts:15-40`)。

---

### 2.4 Tooltip 提示

🆕 **版本结论**：两版并存且用量相当，**新基准取 TooltipV2**（较新、有独立测试、tracking 以它为准）。V1 旧调用点保留、**未弃用**（一句话标注见下）。`ToolTipClickClose` 是 V2 的「带关闭按钮」变体。

#### 2.4.1 TooltipV2（canonical）🆕

**何时用**：单条文字/简短内容的引导气泡，但比朴素 tooltip 强——支持只弹一次（onceKey 记 localStorage）、自动关（duration）、受控（control）、被更高浮层占场时压住并退回 onceKey（suppressed）、进入视口才弹（IntersectionObserver）、曝光埋点。本质是**基于 CoUI Popover 封装的「一次性新功能引导气泡」**。

- 该用：新功能首次引导、定时消失的轻提示、需曝光埋点的气泡。
- **📱 PC = hover 触发；移动端 = tap 触发**。

**视觉规格（气泡体 override）**：
```
flex max-w-80 flex-col gap-2 rounded-lg border-black bg-gradient-popover-light px-3
dark:border-black dark:bg-gradient-popover-dark dark:text-black
```
- 圆角 8px、最大宽 320px、横向 padding 12px、文字 `whitespace-pre-wrap`（保留换行）。
- **底色用渐变 token**（真实值）：
  - `bg-gradient-popover-light` = `linear-gradient(180deg, #FFF 0%, #B1E8FF 100%)`（白→浅蓝）
  - `dark:bg-gradient-popover-dark` = `linear-gradient(180deg, #FFF 0%, #E1FFAF 100%)`（白→浅绿）

**箭头**（按 placement 四套）：left/right `bg-gradient-popover-light dark:bg-gradient-popover-dark`、top `bg-blue-5/90 dark:bg-green-5`、bottom `bg-white dark:bg-gradient-popover-dark`，配黑边。触发器 `cursor-pointer text-gray-1`。

**状态与机制**：
- `onceKey` + store atom：只弹一次。
- `duration`：定时器自动关。
- `suppressed`：被更高优先级浮层挡住时关闭并退回 onceKey，浮层关后补弹（含 race 处理）。
- 曝光埋点：首次开时打点（`logName`）。

**🌗 暗/亮**：底色 light=白→浅蓝 / dark=白→浅绿；文字暗模式强制 `dark:text-black`（暗底其实是浅色渐变）。

📍示例: 气泡体 (`CoUI/TooltipV2.tsx:253-267`)；渐变 token 真实值 (`tailwind.config.js:199-202`)；箭头四套 (`TooltipV2.tsx:208-228`)；hover/tap 分流 (`TooltipV2.tsx:182-198`)；onceKey/duration/suppressed/埋点 (`TooltipV2.tsx:87-180`)。

#### 2.4.2 Tooltip V1（旧版，未弃用）

> 🆕 旧版，少量调用仍在用。与 V2 不同：直接基于 floating-ui（非封装 Popover），是更朴素的「hover/focus 单行提示」。气泡体 `z-10 rounded bg-gray-3 p-1 text-xs font-bold shadow-md`、箭头 `FloatingArrow fill-gray-3`、`flip` 自动翻面、`FloatingDelayGroup` 延迟组。**新代码用 V2**；V1 主要遗留在菜单项的 `TooltipLabel` 等旧调用点。📍示例: `CoUI/Tooltip.tsx:197,257`。

#### 2.4.3 ToolTipClickClose（V2 带 X 变体）

包一层 TooltipV2、强制 `control`，文案右侧加 `CloseIcon`（`ml-2 size-4 cursor-pointer`），点 X 设 `open=false`。用于**需要用户手动关闭、不自动消失的引导气泡**。📍示例: `CoUI/ToolTipClickClose.tsx`。

---

### 2.5 PopupMenu 上下文菜单

「操作列表浮层」，无遮罩，点项即执行。多套实现按场景选：

**怎么选**：
- 锚在「⋮ / 更多」按钮上的操作列表 → 「更多」菜单（基于 CoUI Popover 封装，可跨页复用）。
- 右键 / 长按某条目唤起 → 坐标定位 + portal 的上下文菜单。
- 字段旁 ⓘ 纯说明气泡 → 字段信息气泡（CoUI Popover `hoverable`）。
- 需按坐标精确定位、自带方向/边界回收的通用菜单 → CoUI Menu（v2）。

#### 2.5.1 CoUI Menu（坐标定位菜单）🆕

🆕 同文件内 v1 / v2 两套样式，**v2 是新版**（更精致小弹层），以 v2 为准。按绝对坐标 `position{left,top}` 定位，`direction` 控制展开方向（left/right/top/top-left/top-right），含视口边界 clamp（量 rect 回收进可视区）。

**v2 容器**：
```
gap-1 rounded-lg border-black/5 bg-light3-smallPopupBg/95 px-2 py-3
shadow-[0_5px_10px_0_rgba(0,0,0,0.20)] backdrop-blur-md
dark:border-white/5 dark:bg-dark3-smallPopupBg/95 dark:shadow-none
```
**v2 菜单项**：`font-medium px-2 rounded-lg whitespace-nowrap text-black dark:text-gray-3 hover:bg-black/10 dark:hover:bg-white/10`。

> v1 旧样式：`w-[95px] rounded-md border-black-1 bg-white p-2 shadow-[0px_4px_4px_0px_rgba(0,0,0,0.25)] dark:border-gray-3 dark:bg-black`，项带下划线分隔。新代码传 `version='v2'`。

`smallPopupBg` token 真实值：light=`rgb(255,255,255)`、dark=`#2F3034`。

📍示例: clamp (`CoUI/Menu.tsx:92-174`)；v2 容器 (`Menu.tsx:180-182`)；v2 项 (`Menu.tsx:197`)；v1 (`Menu.tsx:182`)；token (`tailwind.config.js:114,123`)。

#### 2.5.2 PopupMenu（mantine 封装）

> ⚠️ **独立技术栈**：基于 `@mantine/core` 的 `Popover`，与 CoUI Popover（floating-ui）完全不同底层。dropdown 样式（inline）：`transform: scale(0.8)`、`borderRadius: 6`、`border: 1px solid black`、`boxShadow: 0px 4px 12px rgba(108,108,108,0.25)`、`padding: 8px 6px`、`fontWeight: 700`，底色 `dark? 'black' : '#F3F3FF'`，`withinPortal` 渲染到 portal。📍示例: `CoUI/PopupMenu/index.tsx:25-37`。

#### 2.5.3 上下文菜单的三种业务形态

**「更多 ⋮」菜单**（CoUI Popover 封装，跨页复用，触发外观靠 `triggerClassName`/`triggerIcon` 注入差异、菜单结构共享）：
- 气泡容器：`z-[999] min-w-[120px] rounded-lg border border-black/5 bg-light3-smallPopupBg p-1 shadow-lg dark:border-white/5 dark:bg-dark3-smallPopupBg`。
- 菜单项：`flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm`，危险项 `text-red-500 hover:bg-red-500/10`，普通项 `text-black hover:bg-black/5 dark:text-white dark:hover:bg-white/10`。
- `showArrow={false}`，默认 `placement='bottom-end'`、`gap=4`。

**右键上下文菜单**（`createPortal` 到 `document.body`）：
- 容器：`fixed z-[1000] min-w-[160px] rounded-lg border border-black/5 bg-light3-smallPopupBg p-1 text-sm shadow-lg dark:border-white/5 dark:bg-dark3-smallPopupBg`。
- 视口 clamp（PAD=8px，量 rect 回收）；二级子菜单默认 `left-full` 向右展开，贴右边时翻 `right-full`。
- 点外部 / 滚动自动关。

**字段 ⓘ 信息气泡**（CoUI Popover `hoverable`）：
- 气泡体：`max-w-[260px] rounded-lg border-0 bg-[linear-gradient(180deg,#FFFFFF_0%,#B6B4FF_123.33%)] p-0 text-black shadow-[0px_6px_8px_0px_rgba(0,0,0,0.36)] dark:text-black`（白→紫 #B6B4FF 渐变，light/dark 同款）。
- 箭头：`overrideArrowClassName="border-0 bg-[#C6C5FF] dark:bg-[#C6C5FF]"`；内文 `whitespace-normal px-3 py-2 text-xs leading-[normal]`；触发 InfoIcon `size-3 text-gray-1`。
- 因 useZIndex inline style ≥100 已盖过 sidebar/其他业务气泡，**不要在 floatingClassName 写 z-***。

📍示例: 「更多」菜单 (`WorldCard/MoreMenuButton.tsx:126,139-144`)；右键菜单 (`WorldCard/MoveNoteContextMenu.tsx:47-78`)；字段气泡 (`WorldCard/FieldInfoPopover.tsx:46`)。

---

### 2.6 Toast 轻提示

**何时用**：保存成功/失败、复制成功、网络错误、loading 等一次性反馈——顶部居中（或锚定某元素）短暂浮现一条带图标提示，几秒后自动消失。容器 `pointer-events-none`（不挡交互）。不该用：需用户决策（→ Modal）、依附按钮的持续说明（→ Popover）。

🆕 单一 canonical，无版本分歧。

**调用方式**：
- 命令式全局 API：`toast.success/info/warning/error/loading/show/hide/removeAll(...)`（全局单例，无需 Provider 内）。
- Hook：`useToast()` → `showToast/showInfo/.../hideToast/removeAll`。

> ⚠️ **复用陷阱**：要反复 show/hide 同一条必须指定固定 `id`；同 id 在显示中 show 是 no-op；hide→show 有 320ms 竞态，provider 用 `cancelledHides` 处理，勿自己 setTimeout 绕。

**视觉规格**：按 `type` 切换底色 + 边色 + 图标（全写死 hex）：

| type | 底色 | 边色 | 图标 |
|---|---|---|---|
| info | `bg-[#E2F4FF]` | `border-[#3BA6F3]` | ToastInfoIcon |
| warning | `bg-[#FFF2E4]` | `border-[#FFA133]` | ToastWaringIcon |
| error | `bg-[#F8E3E3]` | `border-[#E4221A]` | ToastErrorIcon |
| success | `bg-[#E7F7F5]` | `border-[#07BC7B]` | ToastSuccessIcon |
| loading / default | `bg-[#F5F5F5]` | `border-[#707070]` | ToastLoading / ToastDefault |

- 卡片：`rounded-md p-4 shadow-lg text-white {border} pointer-events-auto`（圆角 6px、padding 16px）。
- 标题 `text-base font-bold text-black`（16px 粗黑）；描述 `text-sm text-gray-1`。
- 图标统一 `size={20}`；关闭按钮 `ToastXIcon size={20}`（`text-white hover:text-gray-200`）。
- 默认 `duration=3000`ms、`autoClose=true`。

**定位与 DOM**：
- 容器：`pointer-events-none fixed left-0 top-0 z-[9999] size-full`（全屏 fixed、z-9999 盖一切、自身不挡点）。
- 非锚点 Toast（顶部居中）：
  ```
  <div class="mt-14 flex w-full justify-center sm:mt-10">      ← 移动顶距 56px / PC 40px
    <div class="w-full px-4 md:px-10 lg:px-52 {animationClass} max-w-[1190px]">
      <Toast .../>
  ```
- 锚点 Toast（`positionEl`）：量目标 rect，定位到其上方 80px（`rect.top - 80`），`<div class="absolute" style={position}>`。

**进出动画**：CSS class 切换——进入 `toast-enter` / 退出 `toast-exit`（退出延迟 320ms 后真正卸载）。

**🌗 暗/亮**：⚠️ Toast 底色/边色**写死 hex、不随主题切换**（无 dark: 分支）；卡片整体 `text-white` 但标题强制 `text-black`、描述 `text-gray-1`，即两模式下外观一致（浅底深字）。

📍示例: 全局 API (`CoUI/Toast/toast.ts:18-75`)；Hook (`Toast/ToastProvider.tsx:238-244`)；复用 no-op (`ToastProvider.tsx:56-58`)；type 配色 (`Toast/index.tsx:78-110,166`)；容器 (`ToastProvider.tsx:187`)；非锚点 (`ToastProvider.tsx:193-201`)；锚点 (`Toast/index.tsx:43-59,132-160`)；动画/卸载 (`ToastProvider.tsx:111-121,190`)。

---

### 2.7 ImagePreview 图片预览

**何时用**：角色相册/图集的沉浸式查看——全屏铺黑 + swiper 横滑浏览图集，支持手势下拉关闭、跟手拖拽、举报/审核蒙版。区别于普通 Modal：无圆角卡片，整屏黑底铺满。

🆕 单一 canonical。是**全屏沉浸式图片浏览器**（非普通 Modal），基于 `nice-modal` + `swiper`，zIndex 走 useZIndex。

**视觉规格**：
- 根容器：`double-click-filter fixed inset-0 bg-black backdrop-blur-md sm:bg-black/80`，`style={{ zIndex }}`。移动端纯黑、PC 黑 80% + 模糊。
- 图片：`absolute left-0 top-0 size-full touch-none select-none object-contain`。
- 文字说明条：`max-w-[750px] rounded-lg bg-black/30 p-3 text-center text-sm text-white backdrop-blur-md sm:bg-black/50 sm:backdrop-blur-sm`（底部居中）。
- 关闭按钮：`absolute end-4 top-3 z-10 rounded-full text-white sm:end-5 sm:top-5 sm:bg-white/10 sm:p-2`，内 `CloseIcon size-6`。
- 跟手拖拽图层：`position: fixed; zIndex: 9999`。

**📱 PC / 移动**：移动端有完整触摸手势（下拉关闭 + 水平滑动切图，touchState/followImage 状态机）；PC 用 swiper 的 prev/next 按钮 + 分页。

📍示例: 根容器 (`CoUI/ImagePreviewModal/ImagePreviewModal.tsx:385-393`)；图片 (`:447`)；说明条 (`:460`)；关闭按钮 (`:503-506`)；跟手图层 (`:512-517`)。

---

### 2.8 StepModal 多步引导弹窗 🆕

**何时用**：新功能多步教学——基于 Modal 底座的「横向轮播多步引导」，每步一张图（区分 light/dark × mobile/pc 四套）+ markdown 文案 + Back/Next/Done 按钮。

🆕 **版本结论**：通用多步弹窗取 **StepModalV2**。`StepModal`（V1）仅 1 处 import。注意业务层另有基于 Modal 自建的 `StepModalV3` 封装，**不是 CoUI 升级链第三代**，勿混入。

**视觉规格**：
- 复用 Modal 底座：`classNames={{ content: 'flex flex-col pb-8', body: 'mt-2.5 mb-0 mx-4 px-0 overflow-x-hidden' }}`、`footer={null}`、`autoNice={false}`。
- 关闭按钮：`absolute right-4 top-4 z-10 size-6 text-light3-primary dark:text-dark3-primary`。
- 轮播：`motion.div animate={{ translateX: -currentIndex*100% }}`（framer-motion，type tween）；每步 `flex w-full shrink-0 flex-col gap-2`。
- 图片：四套条件渲染（`step.image.{light,dark}.{mobile,pc}`），用 `padding-bottom: ratio%` 撑比例 + `<Image fill object-cover>`。
- 文案：`MarkdownText text-sm text-black dark:text-gray-3`。
- 按钮：Back `color="gray" h-10 w-36 rounded-3xl sm:w-[200px]`；Next/Done `color="primary" h-10 rounded-3xl`，有 Back 时 `w-36 sm:w-[200px]` 否则 `w-full sm:w-[300px]`。

**状态**：`hasBack`（非首步且多步）/ `hasNext`（多步且非末步）/ `hasDone`（单步或末步）由 `currentIndex` 推导；steps 变化时重置到第 0 步。

**🌗 / 📱**：图片按 `light/dark` × `mobile/pc` 四套切换（dark:hidden / sm:hidden / sm:dark:block 组合）；文案/按钮宽度走 `sm:` 断点。

📍示例: 底座/关闭/图片/文案 (`CoUI/StepModalV2.tsx:95-249`)；按钮 (`:214-248`)；状态推导/重置 (`:68-78`)。
## 三、卡片 Cards

> 卡片按**通用形态**分类，不按产品功能命名。onlychat 的具体数值 / className / `file:行号` 作为示例（📍示例）保留，数值照抄。
> 三轴：🌗 暗/亮（双值）· 📱 PC/移动（grid 列数 / list）· 🆕 取最新版为准。

### 0. 卡片的本质拆解（先看这个）

卡片 = **可点击的实体容器**。无论封面卡还是条目卡，都由这几层组合：

| 层 | 职责 | 常见取舍 |
|---|---|---|
| 外框 | 圆角 + 边框 + 卡底 + 阴影 + hover/selected 态 | 竖卡走整卡 `<Link>` 跳转；条目行走 role=button |
| 视觉区 | 封面图 / 头像 / 默认占位 / 裂图兜底 | 封面卡放大图（比例撑高）；条目卡放小头像 |
| 文字区 | 标题 + 副标(作者/meta) + 标签 + 数据指标 | 竖排（封面卡）或右侧横排（条目卡）|
| 操作层 | 收藏 / 编辑 / 更多 / 删除 / 勾选框 | overlay 在封面右上，或 inline 在 meta 行 |
| 状态蒙版 | 审核中 / 失效 / 选中 / 申诉 | 居中蒙版或全卡覆盖 |

**两条选型主轴**：
1. **比例**：封面 1:1 正方 → 头像型实体（角色）；封面 3:4 竖向 + 左侧书脊 → 文档型实体（世界卡）；横条卡 → 详情页/挂载区列出。
2. **交互密度**：网格平铺看 → 封面竖卡；密集列表逐条编辑 → 瘦行条目卡；横滑只看头像 → 圆形 Icon。

---

### 1. 封面卡（Cover Card）

竖向「封面图 + 文字区」是平铺网格的标准载体。两种封面比例决定两套实现。

#### 1.1 视觉规格

| 部位 | 规格 | 何处取值 |
|---|---|---|
| 外框 | `flex flex-col overflow-hidden rounded-lg border`，卡底 `bg-purple-3 dark:bg-black-9`，边框 `border-purple-2 dark:border-black-2`，`shadow-sm` | 📍示例: OCCard `CardBox.tsx:29` |
| 外框（无边框变体）| `group relative flex w-full flex-col overflow-hidden rounded-lg`，卡底同上 | 📍示例: 世界卡竖卡 `WorldCard.tsx:922` |
| 封面区（头像型 1:1）| `relative pb-[100%]` 正方撑高 | 📍示例: `TopImage.tsx:92` |
| 封面区（文档型 3:4）| `relative aspect-[174/232] w-full overflow-hidden rounded-br-lg`，占位底 `bg-black/4 dark:bg-white/4` | 📍示例: `WorldCard.tsx:938` |
| 封面图 | `absolute inset-0 size-full object-cover object-top`，淡入 `transition-opacity duration-700`，loading 时 `opacity-0` | 📍示例: `TopImage.tsx:135` |
| 封面底渐变蒙层 | `absolute -bottom-px h-[50px] w-full`，往卡底 fade（亮往 `#F3F3FF` / 暗往 `#292929`）| 📍示例: `top/BottomBox.tsx:23`（token `oc-detail-card-light/dark`）|
| 标题 | 头像型 `text-xs font-bold truncate`；文档型 `font-exo2 text-base font-bold italic leading-[18px]`；色 `text-black dark:text-white` | 📍示例: `NameBox.tsx:119` / `WorldCard.tsx:910` |
| 数据指标条 | `text-[.625rem]`(10px) `backdrop-blur-xs`，半透底 `bg-purple-3/50 dark:bg-black/50`；或行内 `MessageIcon size-[14px] + text-xs text-gray-1 dark:gray-2` | 📍示例: `top/BottomBox.tsx:25` / `WorldCard.tsx:1123` |
| 圆角 | `rounded-lg`(8px) 主流；放大/横条变体 `rounded-[14px]` | — |

**封面书脊 spine（文档型专属视觉签名）**：左侧一条带顶/底内凹弧的渐变竖条，把卡视觉化成「一本书」。

| 规格 | 值 | 何处取值 |
|---|---|---|
| 容器 | `absolute inset-y-0 left-0 h-full`，宽度按场景：竖卡 `w-2`(8px) / 横条 `w-1.5`(6px) / 详情大卡 `w-5`(20px) | 📍示例: `WorldCardSpine.tsx:13` |
| 绘制 | SVG `viewBox 0 0 20 400 preserveAspectRatio=none`，渐变 `#7976FF` 0.6→0.3（从右往左）| 📍示例: `WorldCardSpine.tsx:36` |
| 让位 | 图区跟着 `ml-2` 给书脊腾位 | 📍示例: `WorldCard.tsx:946` |
| 🌗 | 书脊**不变色**（两主题同 `#7976FF`）| — |

**默认封面 / 裂图兜底**（封面缺失或加载失败的两层 fallback）：

| 态 | 表现 | 何处取值 |
|---|---|---|
| 无封面默认占位 | `bg-white-2 dark:bg-dark3-bg`，dark 叠 `bg-white/10`，居中半透插图 `text-black/[0.08] dark:text-white/[0.08]` | 📍示例: `WorldCardDefaultCover.tsx:11` |
| 加载失败裂图 | 本地 public 双图 dark: 切换（`/worldcard-default-light.png` `dark:hidden` / `-dark.png` `hidden dark:block`），`unoptimized object-cover` | 📍示例: `WorldCardBrokenCover.tsx:13` |

> ⚠️ 本地 dev 下静态图走 `next/image` 会裂，默认/裂图占位一律用本地 public 双图或 inline `backgroundImage` 切换。

#### 1.2 DOM 锚点结构

```
<外框 rounded-lg border bg-purple-3 dark:bg-black-9>
  <Link stretched-link absolute inset-0>      ← 整卡跳详情（竖卡惯例）
  <封面区 pb-[100%] | aspect-[174/232]>
    [<spine w-2>]                              ← 文档型才有
    <封面图 | DefaultCover/BrokenCover>
    <顶栏 absolute top-0>  左: 排名/置顶/题材chip  右: 收藏星 | 编辑 | 更多
    <居中蒙版>            审核态 / 失效 Expired
    <底渐变蒙层 -bottom-px h-50>  数据指标条
  <文字区 flex-1 flex-col justify-between px-* pb-*>
    <标题 truncate + 更多按钮>
    <副标 简介>
    <标签组>
    <meta 行 justify-between>  [💬数 + 📝数] + (Draft 徽章 | inline 更多)
  [<selected overlay border-2>]               ← 多选/管理场景
```
📍示例: 头像型 `OCCard.tsx:137`；文档型 `WorldCard.tsx:913`

#### 1.3 状态

| 状态 | 表现 | 何处取值 |
|---|---|---|
| hover (PC) | `lg:hover:shadow-lg`（头像型）/ `md:group-hover:border-black/20 dark:md:group-hover:border-white/20`（文档型）| `CardBox.tsx:29` / `WorldCard.tsx:1176` |
| selected | `border-2 border-light3-primary dark:border-dark3-primary` overlay；或全卡覆盖 `absolute z-[9] bg-black/50`（多选）| `WorldCard.tsx:1175` / `FolderCard.tsx:113` |
| 收藏激活 | 星 `text-pink-1`；未收藏 `text-gray-3` | `WorldCard.tsx:1006` |
| owner 主态 | 显编辑按钮、隐藏收藏星，footer 走 Owner 区 | `WorldCard.tsx:976` |
| 草稿 | 隐藏数据指标，显紫色 Draft 徽章（`border-purple-4 text-purple-4` + `size-1` 圆点）| `FooterCard.tsx:31` / `WorldCard.tsx:1141` |
| 审核异常 | 封面居中蒙版 | `top/CenterBox.tsx` / `WorldCard.tsx:1051` |
| 失效 | 竖卡 + 居中 `⚠ Expired` 蒙版（`bg-black/30 backdrop-blur-xs`），本人态留 Remove 按钮 | 📍示例: `WorldCardExpiredCard.tsx:80` |
| 预览（非交互）| 外层 `pointer-events-none`，强制未收藏态；角标纯装饰 | `FeedPreview/PreviewCard.tsx:24` |

#### 1.4 🌗 暗亮 / 📱 PC移动 / 🆕

- 🌗：卡底 `bg-purple-3 → dark:bg-black-9`；边框 `border-purple-2 → dark:border-black-2`；标题 `text-black → dark:text-white`；封面占位底 `bg-black/4 → dark:bg-white/4`；@作者 `blue-10 → yellow-6`；指标 `gray-1 → gray-2`；**书脊不变色**。
- 📱：自适应网格。头像型目标卡宽 `BASE_CARD_WIDTH=180px`，列数随容器算、窄屏 clamp ≥2 列（`InfiniteScroll/config.ts:3`）；文档型 `repeat(auto-fill, minmax(min(180px, calc(50% - 6px)), 1fr))`、窄屏 ≥2 列（`HomeWorldCardList.tsx:48`），gap `gap-2 sm:gap-3`。hover 阴影仅 `lg:` 生效。
- 🆕：标签组按 `useHomeUiRevamp()` A/B 分流 `TagBoxV2`(revamp) / `TagBox`(对照)；排名条同有 revamp 粉条渐变 `from-light3-primary dark:from-dark3-primary`。

#### 1.5 封面卡的横条 / 放大 / 预览衍生形态

同一封面卡，换布局/尺寸即衍生出别的用途：

| 衍生形态 | 与竖卡的差异 | 何处取值 |
|---|---|---|
| **横条卡（左封面+右文字）** | `flex items-center gap-2 rounded-[14px] bg-black-4 dark:bg-white-4 p-4`；封面 mobile `88×72` / PC `140×111`；PC 额外展示简介+tags（`items-start gap-3`）| 📍示例: longStrip `WorldCard.tsx:746`（角色详情页列出挂载项）|
| **中长条卡（挂载区块）** | `border bg-black-4 backdrop-blur-[50px]`；封面 `104×78 rounded-[10px]`；右上切换/删除按钮 `size-7` | 📍示例: mediumStrip `WorldCard.tsx:618`（新建会话/创建页已挂载世界卡）|
| **详情图卡（主视觉大封面）** | 书脊 `w-5` + 大封面 `aspect-[380/534]`，默认 `w-[460px] rounded-r-[14px]`；点击放大看图 | 📍示例: `world/[world_id]/components/WorldCard.tsx:20` |
| **预览卡（编辑器实时预览）** | 放大竖卡（封面 `aspect-[320/400] rounded-[14px]`）；底色层用 SVG clipPath 照搬书脊斜边像素级齐平；收藏角标**纯装饰不可点**（`StarFullIcon size-6 text-white/80`）；标题 `font-exo2 text-2xl italic` | 📍示例: `WorldCardPreviewCard.tsx:49` |

#### 1.6 何时用封面卡

网格里平铺、点进去消费一个实体（聊天角色 / 看世界卡详情）时——封面卡是标准载体。
头像型（1:1，无书脊）= 角色这类「人/头像」实体；文档型（3:4 + 书脊 + 艺术字标题）= 世界卡这类「文档/设定」实体。要在详情页里横向列出用横条卡，要做编辑实时预览用预览卡。

---

### 2. 列表条目卡（List Entry Card）

密集列表里逐条展示/编辑的卡。两套交互模型，PC/移动本质不同时拆文件实现。

#### 2.1 瘦行型（PC·密集编辑）🆕

48px 高的瘦行：紫点 + 标题 + 审核 icon + 优先级星 + 删除，hover 浮现勾选框，双击改名。

| 部位 | 规格 | 何处取值 |
|---|---|---|
| 基底 | `group relative flex w-full rounded-[14px] py-3 pl-9 pr-3 gap-4 select-none overflow-hidden transition-[background-color,color] duration-200` | 📍示例: `NoteEntryCard.tsx:315` |
| 标题 | `min-w-0 truncate text-base font-bold leading-[18px]` | `:256` |
| 未完成标记 | 标题前 `size-2 rounded-full bg-[#7976ff]` 紫点 | `:360` |
| 操作区 | 右侧 `flex shrink-0 items-center gap-2`：优先级实心星（仅展示已选颗数 `size-4`）+ 删除 `size-6 rounded-[19px] bg-white/80 dark:bg-black/20` + `TrashOutlineIcon size-4` | `:259` / `:409` |
| 勾选框 | `absolute left-2 top-1/2 size-5 -translate-y-1/2`；常态 `opacity-0 group-hover:opacity-100`，manage 态常显 | `:338` |

#### 2.2 胖卡型（移动 / 信息密度高）📱

头像 + 标题 + 徽章 + 关键词行 + 描述两行的胖卡，点整卡跳转。

| 部位 | 规格 | 何处取值 |
|---|---|---|
| 基底 | `flex w-full flex-col gap-1 overflow-hidden rounded-[14px] border p-3 transition-colors` | 📍示例: `NoteEntryCard.mobile.tsx:146` |
| 头像 | `size-9 rounded-full bg-black/4 dark:bg-white/4`，图 `sizes="36px" object-cover`；无图回退默认插图 | `:171` |
| 标题 | `truncate text-base font-bold leading-[18px]`；空名 `text-black/30 dark:text-white/30` | `:187` |
| 删除 | `size-6 rounded-full bg-white-2 dark:bg-[#212121]` + `TrashOutlineIcon size-4` | `:216` |
| 关键词行 | `truncate text-sm font-medium leading-[14px] text-black dark:text-white`（无关键词显 "Always on"）| `:229` |
| 描述行 | `line-clamp-2 text-xs leading-normal text-gray-1 dark:text-gray-2`，缩进 `pl-11` 对齐头像右 | `:240` |

#### 2.3 头像横排型（搜索结果 / list 行）

整行展示一个实体，左头像 + 中名字/统计/简介 + 右操作。

| 部位 | 规格 | 何处取值 |
|---|---|---|
| 外框 | `my-1 flex w-full rounded-lg bg-white-1 px-4 py-2 dark:bg-black` | 📍示例: SearchUserCard `SearchUserCard.tsx:44` |
| 头像 | `size-14`(56px)，带 frame | `:49` |
| 名字 | `text-sm font-bold` | — |
| 统计 | `text-xs text-light3-primary dark:text-dark3-secondary` | — |
| 简介 | `line-clamp-3 text-xs` | `:73` |
| 右操作 | FollowButton 等 | — |
| 骨架版 | `bg-gray-3 dark:bg-black-2` + `animate-pulse` | `SearchUserLoadingCard.tsx:112` |

#### 2.4 DOM 锚点结构

```
瘦行型（PC）：
<div role=button data-note-id rounded-[14px] py-3 pl-9 pr-3>
  [<勾选框 absolute left-2 size-5>]
  <name 组 flex-1>  紫点? + 标题truncate + 审核icon
  <操作区 shrink-0>  优先级星 + 删除
  [<改名浮层条 absolute>]                    ← 双击改名（PC 独有）

胖卡型（移动）：
<div role=button rounded-[14px] border p-3>
  <行 items-center gap-2>  [勾选框] + 头像size-9 + (标题+徽章+审核icon) + [删除]
  <信息块 pl-11>  关键词行 + 描述两行
```
📍示例: `NoteEntryCard.tsx:288` / `NoteEntryCard.mobile.tsx:135`

#### 2.5 状态

| 状态 | 表现 | 何处取值 |
|---|---|---|
| default | `bg-black/4 hover:bg-black/10 dark:bg-white/4 dark:hover:bg-white/10` | `NoteEntryCard.tsx:320` |
| selected（当前编辑）| `bg-light3-primary/20 dark:bg-dark3-primary/20`，标题转主题色 | `:322` / `:372` |
| 多选 checked | 瘦行 `bg-light3-primary/20`（无边框）；胖卡 `border-light3-primary/50 bg-light3-primary/20`（🆕 mobile 有 1px 边框）| `:319` / `mobile:151` |
| 改名中（PC）| 浮层条 `absolute left-9 right-3 h-[23px] rounded border border-black/10 bg-white/80 backdrop-blur-[10px]` + input + 计数 | `:423` |
| 空名 | 标题色 `text-[#707070]`（瘦行）/ `text-black/30 dark:text-white/30`（胖卡）| `:374` |

> 🆕 删除统一用描边垃圾桶 `TrashOutlineIcon`（非通用 DeleteIcon）；勾选框矢量 PC/mobile 共用：选中 `ManageCheckedSquare`(主题色填充+白勾) / 未选 `ManageUncheckSquare`(描边圆角方框)，`NoteEntryCard.tsx:479/500`。

#### 2.6 🌗 / 📱 / 何时用

- 🌗：底 `bg-black/4 → dark:bg-white/4`；标题/关键词 `text-black → dark:text-white`；描述 `gray-1 → gray-2`；选中态主题色成对 `light3-primary ↔ dark3-primary`。
- 📱：交互模型本质不同 → 拆文件。瘦行（PC）双击改名 + hover 勾选 + 拖拽排序；胖卡（移动）点整卡跳转、**无持续选中高亮**、靠头像/关键词/描述提供信息密度。
- 何时用：密集列表逐条管理（编辑/删除/多选/排序）→ 瘦行型；移动端或需要每条带头像+预览信息 → 胖卡型；搜索结果/关注列表这类整行实体 → 头像横排型。

---

### 3. 分类 / 分组卡（Category / Group Card）

把一组同类条目折叠在一个可展开容器里：标题行（图标 + 名 + 计数 + 添加）+ 条目列表。

| 部位 | 规格 | 何处取值 |
|---|---|---|
| 容器（PC）| `flex flex-col gap-4 rounded-[14px] border border-transparent p-1`；落位高亮 `bg-purple-3 dark:bg-white/10`；过渡 `transition-[background-color] duration-200` | 📍示例: `NoteCategoryCard.tsx:189` |
| 容器（移动）| `flex flex-col gap-4`（无背景），分类间距更大 | `NoteCategoryCard.mobile.tsx:130` |
| 标题文字 | `font-exo2 text-base font-semibold leading-5 text-black dark:text-white` | `:203` |
| 计数 (N) | `text-sm text-black/50 dark:text-white/50`（manage 态切灰）| `:213` |
| 折叠箭头 | `ChevronDownIcon size-4 text-black/50 dark:text-white/50`，折叠 `-rotate-90` | `:206` |
| 添加按钮 | PC `size-7 text-gray-2 dark:text-gray-1`（字面 `＋`）；移动内联 12px 描边十字 | `:224` / `mobile:165` |
| 条目列表 | PC `flex min-h-[2px] flex-col gap-3`；移动 `flex flex-col gap-2` | `:236` / `mobile:174` |
| 落位幽灵卡（PC 拖拽）| `absolute inset-x-0 top-0 rounded-[14px] bg-black/[0.04] dark:bg-white/[0.04]` + translateY | `:291` |

**DOM 锚点结构**：
```
<div data-cat rounded-[14px] border p-1 gap-4>
  <标题行 justify-between>
    <button flex-1>  chevron + 名 + ( N )
    [<添加按钮 size-7>]                        ← 未达上限 & 非 manage
  {expanded && <条目列表 gap-3>
    {items.map(<列表条目卡 §2>)}
    [<落位幽灵卡 absolute>]                     ← PC 拖拽落位
  }
</div>
```
📍示例: `NoteCategoryCard.tsx:182`

**状态**：折叠/展开（chevron 旋转）；拖拽落位高亮（容器变色 + 幽灵卡占位，PC 独有）；达上限隐藏添加按钮。
**🌗**：容器落位高亮 `bg-purple-3(#F3F3FF) → dark:bg-white/10`；标题 `text-black → dark:text-white`；计数/箭头 `black/50 → white/50`。
**📱**：PC 容器带边框 + 拖拽落位（droppable/让位 transform/幽灵卡）；移动无拖拽、无容器背景、条目卡更胖、分类间距更大。
**何时用**：一屏内分组管理多类条目，每组可独立折叠/计数/新增——比纯标题分隔更强（带交互边界 + 拖拽落位区）。

---

### 4. 用户 / 实体 Icon（圆形头像型）

非整卡：只展示头像 + 名，横滑列表里点进去看实体。

| 部位 | 规格 | 何处取值 |
|---|---|---|
| 头像 | `h-12 w-12 sm:h-[60px] sm:w-[60px] rounded-full object-top` | 📍示例: CircleCharacterIcon `CharacterIcon.tsx:55` |
| 自有标记 | 加 `border border-light3-primary dark:border-dark3-primary` | `:57` |
| 名字 | `text-[10px] sm:text-xs sm:font-bold truncate` | `:67` |
| 创建入口变体 | `size-12 sm:size-[60px] rounded-full border` + 加号 SVG | `:90` |

**🌗**：自有边框主题色成对 `light3-primary ↔ dark3-primary`。
**📱**：尺寸 `48 → 60px`（sm 断点）。
**何时用**：横滑列表里只需展示「头像 + 名」、点进去看实体时——比封面卡轻，不承载简介/数据/操作。

---

### 5. 空态 / 占位 / 骨架卡（Empty / Placeholder / Skeleton）

列表为空、加载中、或槽位占位时的填充卡。

| 形态 | 表现 | 何处取值 |
|---|---|---|
| **通用空态**（图标+提示+加按钮）| 居中图标 `text-[#B376FF] dark:text-pink-4` + 加按钮 `h-[40px] w-[200px] rounded-[8px] border border-black/10`（前置 `+`）| 📍示例: `CardEmptyView/index.tsx:29` |
| **空槽占位**（网格末尾）| `min-h-[295px]` 渐变底 `linear-gradient(180deg, rgba(146,62,252,0.12) 0%, ...)` + 居中图标 + 渐变文字 | 📍示例: EmptyCard `EmptyCard.tsx:20` |
| **加载骨架** | 封面 spinner + 三条 `bg-black/5 dark:bg-white/5` 占位，`animate-pulse` | 📍示例: LoadingCard `LoadingCard.tsx:14` |
| **编辑器右栏空态**（引导）| Hero `font-exo2 text-[50px] italic` + 渐变 `bg-clip-text`（light 橙→紫 / dark 黄→粉）+ 副标 `text-sm text-gray-1` + 引导卡组 | 📍示例: `NoteEditorEmptyState.tsx:26` |
| **引导卡 StarterCard** | `min-w-[180px] flex-1 rounded-[14px] bg-black/4 p-4 dark:bg-white/4`：标题 `text-sm font-bold` + 描述 `text-xs text-gray-1` + 右下 `size-[68px]` 多层矢量图标 | 📍示例: `StarterCard.tsx:206` |

**StarterCard 角标**（推荐项）：`absolute left-0 top-0 h-3 rounded-br-[8px] rounded-tl-[8px] bg-green-3 px-2 text-[10px] font-bold text-black`（`:249`）。
**🌗**：骨架/卡底 `bg-black/4 → dark:bg-white/4`，占位条 `black/5 → white/5`；空态图标/渐变各兜主题对应色。
**何时用**：列表无数据时——纯空态用通用空态卡（带"去创建"按钮）；网格补齐尾部空槽用空槽占位；首次加载用骨架；需要引导用户操作时用引导卡组。

---

### 6. 推荐胶囊（Recommendation Pill）

非卡：圆角 pill，内联在底栏/工具条，激活态高亮。

| 部位 | 规格 | 何处取值 |
|---|---|---|
| 容器 | `rounded-full px-2 py-1 text-[10px]`，PC 加 `sm:border sm:border-black/10 sm:px-4` | 📍示例: RecommendModelBottomV2 `RecommendModelBottomV2.tsx:126` |
| 激活态 | `bg-light3-primary/20 text-light3-primary dark:bg-dark3-primary/20 dark:text-dark3-primary` | `:127` |
| 未激活 | `bg-gray-5/40 dark:bg-black-2/60 sm:bg-white/60` | `:129` |

**🌗**：激活态主题色成对；未激活底色暗亮各兜。
**📱**：移动纯 pill 无边框；PC（sm+）加描边 + 横向内距。
**何时用**：工具条/底栏里的轻量入口（推荐项/快捷动作），激活态要明显但不抢卡片视觉——用主题色 20% 底。🆕 V2 取代 V1（V1 已弃用）。

---

### 7. 选卡决策（小结）

```
要平铺网格、点进去消费一个实体？        → 封面卡（§1）
  ├ 实体是「人/头像」（1:1 正方，无书脊） → 头像型竖卡   📍OCCard
  ├ 实体是「文档/设定」(3:4+书脊+艺术字)  → 文档型竖卡   📍WorldCard vertical
  ├ 详情页里横向列出                      → 横条卡       📍longStrip
  ├ 挂载区块/已选列表（可切换/删除）       → 中长条卡     📍mediumStrip
  ├ 详情页主视觉大封面                     → 详情图卡
  ├ 编辑器实时预览                        → 预览卡       📍WorldCardPreviewCard
  └ 失效                                  → 失效卡 + Expired 蒙版

要密集列表里逐条管理？                  → 列表条目卡（§2）
  ├ 高频编辑/多选/排序（PC）              → 瘦行型（48px，双击改名+hover勾选）
  ├ 移动 / 每条要头像+预览                → 胖卡型
  └ 搜索结果 / 关注列表（整行实体）       → 头像横排型   📍SearchUserCard

要把一组同类条目折叠分组？              → 分类/分组卡（§3）  📍NoteCategoryCard
要横滑只看头像、点进去？                → 圆形 Icon（§4）   📍CircleCharacterIcon
列表空 / 加载 / 占位 / 引导？           → 空态卡族（§5）
工具条/底栏轻量入口？                    → 推荐胶囊（§6，非卡）
```

**三个核心判别**：
1. **比例 + 书脊** 决定封面卡子型：1:1 无书脊 = 头像实体；3:4 + 左侧紫书脊 + Exo2 斜体标题 = 文档实体（书脊是最强视觉签名）。
2. **交互密度** 决定条目卡子型：瘦行（编辑密集）vs 胖卡（信息密集）vs 横排（整行实体）。
3. **PC/移动交互模型是否本质不同**（不是单纯样式）才拆文件——拖拽/双击改名 vs 整页跳转就是本质不同；只有 light/dark/间距差异用 `dark:`/`md:` 单文件解决。
## 四、标签 · 徽章 · 指示器 Tags & Badges

> 三轴：🌗 暗/亮（双值）· 📱 PC/移动 · 🆕 取最新版
> 数值/类名照抄自 onlychat world-book 分支，作通用形态的真实示例（📍示例: …）

「小块状信息载体」统称。它们都很小（多在 14–30px 高），靠**形状 + 配色 + 是否可交互**区分语义。本节按通用形态从「纯展示」到「带交互」到「状态/提醒」组织。

---

### 4.0 怎么选：Tag / Chip / Badge / 红点 / 计数（语义速查）

判断顺序：先问「表达的是分类、状态还是数量」，再问「能不能点」。

| 你要表达 | 用什么形态 | 可交互 | 数据来源 |
|---|---|---|---|
| 这条内容属于哪一类（可点筛选） | **Tag / Pill** | 点选/筛选 | 分类数据 |
| 用户可增删的关键词集合 | **可删 Chip**（带 ×） | 删除 | 用户输入产物 |
| 在固定几个视图选项里切换 | **可选 Chip**（互斥单选） | 切换 | 预设选项 |
| 这个对象的身份 / 付费等级 / 草稿状态 | **Badge** | 通常不可点 | 对象属性 |
| 这个对象正在审核 / 被限制 / 被封 | **状态 Badge**（颜色语义化） | 不可点 | 合规状态字段 |
| 需要更高权限才能用 | **门控标签**（锁/会员） | 不可点 | 权限判定 |
| 有没有未读 / 新内容（布尔提醒） | **红点** | 不可点 | 未读 store |
| 一个数值的剩余量 / 超限警告 | **计数指示器** | 不可点 | 当前值/上限 |
| 1–5 级的程度选择 | **星级** | 点选 | 程度值 |

三条铁律（最容易混）：
- **Tag vs Badge**：Tag 是「内容的分类」（可点去筛选），Badge 是「对象的身份/状态」（贴在对象上、通常不可点）。
- **红点 vs 计数**：红点只表达「有/无」布尔提醒，不传达精确数量（即便后台有 count）；要给精确数字用计数 badge，别用红点凑。
- **可删 Chip vs 可选 Chip**：前者是用户造出来的（每个带 ×），后者是预设的视图过滤项（互斥单选 + 计数）。

---

### 4.1 Tag / Pill（展示标签）

胶囊形，表达「这条内容属于哪一类」。可纯展示，也可点选作筛选器。

**底座规格（裸态）** 📍示例: CoUI/Tag (src/components/CoUI/Tag/Tag.tsx:86-90)

| 项 | 值 | 类名 |
|---|---|---|
| 高度 | 20px | `h-5` |
| 圆角 | 全圆 | `rounded-full` |
| 边框 | 1px | `border` |
| 横内距 | 6px | `px-1.5` |
| 字号 | 12px | `text-xs` |
| 过渡 | all 200ms | `transition-all duration-200` |
| 布局 | flex 居中 | `box-border flex items-center justify-center` |

特性：传 `onClick` 自动加 `cursor-pointer`；支持前缀 icon、`closable`（× 关闭，点击 `stopPropagation`）。📍示例: (Tag.tsx:50-80)
⚠️ 渐变背景的 tag 必须 `border-0`，不能 `border-transparent`——否则全圆端会漏出页面底色。📍示例: (TagV2.tsx:105-107)

**Size 三档**（统一渲染器 TagV2）📍示例: (src/components/CoUI/Tag/TagV2.tsx:18-29)

| size | 高 | 内距 | 字号 | icon 容器 | 类名 | 适用 |
|---|---|---|---|---|---|---|
| sm | 16px | px6/py4 | 10px | 12px | `h-4 px-1.5 py-1 text-[10px]` | 卡片小角标 |
| md | 22px | px8/py4 | 12px | 12px | `h-[22px] px-2 py-1 text-[12px]` | 详情页胶囊 |
| lg（默认） | 30px | px12 | 12px medium | 16px | `h-[30px] px-3 text-xs font-medium` | 筛选/选择栏 |

**选中态配色**（中性底 ↔ 主题色 20% 底）📍示例: (TagV2.tsx:31-37)

| 状态 | bg + text | 🌗 类名（成对） |
|---|---|---|
| 未选中 | 中性 4% 底 + 灰字 | `bg-black-4 text-gray-1 dark:bg-white-4 dark:text-gray-2` |
| 选中 | 主题色 20% 底 + 主题色字 | `bg-light3-primary/20 text-light3-primary dark:bg-dark3-primary/20 dark:text-dark3-primary` |
| 未选中 hover（仅桌面） | 中性 10% 底（字色不变） | `md:hover:bg-black/10 md:hover:dark:bg-white/10` |

> 选中态恒无 hover 变化；hover 限 `md:` 桌面断点，避免移动端 tap 闪一下 hover 色。

**高亮/品牌渐变变体**：用于「活动/特殊」类 tag，3 色渐变底 + 渐变字（`bg-clip-text` 透明填充），渐变 stop 延到 `-5%/105%` 防全圆端漏色；其 icon 用品牌固定色，light/dark 共用一套。📍示例: event 渐变 `linear-gradient(94deg,#F75ECC33 -5%,#923EFC33 50%,#3BA6F333 105%)` (TagV2.tsx:38-42,82-133)

**卡片标签条**（一行多 tag + 自动溢出 +N）📍示例: TagBoxV2 (src/components/CoUI/TagBox/TagBoxV2.tsx)

- 子 tag 统一基底：`h-4 px-1.5 py-1 rounded-full text-[10px]`（16px 高 / 全圆 / 10px 字）。📍示例: (:27-28)
- 中性常规 tag 8% 底，`+N` 溢出 tag 4% 底（更弱）。📍示例: (:31-33)
- 前缀状态徽（带语义 icon `size-3 shrink-0`）排在普通 tag 前。
- 容器固定高（`h-9`=36px）+ `overflow-hidden`，超出折叠成 `+N`。📍示例: (:155)

---

### 4.2 Chip（可删 / 可选）

Chip 比 tag 多一层交互：**可删**（用户增删的集合）或**可选**（视图过滤的互斥切换）。

#### A. 可删 Chip（用户输入产物，每个带 ×）

📍示例: KeywordChipInput 内 chip (src/components/WorldCard/KeywordChipInput.tsx:199)

| 项 | 值 | 类名 |
|---|---|---|
| 高 | 30px | `min-h-[30px]` |
| 圆角 | 全圆 | `rounded-full` |
| 内距 | px12/py4 | `px-3 py-1` |
| 字 | 12px medium 灰 | `text-xs font-medium text-gray-1 dark:text-gray-2` |
| 底（🌗） | 白→黑 4% | `bg-black/4 dark:bg-white/4` |
| 删除按钮 | `size-3` 的 × | `CloseIcon size-3`，`-mr-1` 贴边，点击 `stopPropagation` |

- chip 内文字 `min-w-0 whitespace-normal break-all`：长内容在 chip 内断行，不撑破外框。📍示例: (:201-203)
- 外框容器 `min-h-[44px] rounded-[12px] bg-black/4 p-[9px] dark:bg-white/4`；error 态叠红框 `border border-red-6/50 bg-red-6/20`。📍示例: (:185-190)
- 配套 footer 计数 `{n}/{max}`（见 §4.6 计数）。

> 通用形态：可删 chip = 用户造出来的标签集合（关键词/触发词）。和「可选 chip」的区别是它是输入产物、不是预设项，每个都能删。

#### B. 可选 Chip（互斥单选 + 计数的视图过滤器）

📍示例: NotesFilterChips PC (src/components/WorldCard/NotesFilterChips.tsx:65-69) / 📱 mobile (.mobile.tsx:52-56)

| 项 | PC 值 | 📱 mobile 值 |
|---|---|---|
| 高 | 30px (`h-[30px]`) | 32px (`h-8`) |
| 圆角 | 全圆 (`rounded-full`) | 25px (`rounded-[25px]`) |
| 内距 | px12/py4 (`px-3 py-1`) | 同 |
| 字 | 12px medium (`text-xs font-medium`) | 同 |
| 选中（🌗） | 主题色 20% 底 + 主题色字 `bg-light3-primary/20 text-light3-primary dark:bg-dark3-primary/20 dark:text-dark3-primary` | 同 |
| 未选（🌗） | 白→黑 4% 底 + 中灰字 `bg-black/4 text-gray-2 dark:bg-white/4` | 同 |

- 选中态配色与 Tag 选中态一致（主题色 20% 底）——这是全系统「被激活」的统一信号。
- 可挂状态圆点前缀：`size-2 rounded-full bg-[#7976ff]`（仅某状态项显示）。📍示例: 📱 (:58-63)
- 可挂尾部入口键（如管理齿轮）：`size-[30px] rounded-full border border-black/4 bg-black/4` + 图标 `size-5`。📍示例: PC (:76-86)

> 通用形态：互斥单选的视图过滤器（固定 2–N 个选项 + 计数）。和数据驱动的分类 Tag 区别：它是页面内固定视图开关，不随内容变。

---

### 4.3 Badge（身份 / 付费 / 草稿 / 新）

贴在对象上的资格/状态角标。形状偏**小矩形圆角**（区别于 tag 的全圆胶囊），通常不可点。付费类常用品牌渐变底（light/dark 共用），状态类用描边 + 主题色。

| Badge 类型 | 高 | 圆角 | 底 | 字色 | 语义 | 📍示例 |
|---|---|---|---|---|---|---|
| 付费 A（Pro 档） | 18px | 4px | 金黄渐变 `from-[#FFF4AC] to-[#FFB87A]` | 黑 | 较低付费档 | (src/components/CoUI/ProTag.tsx:6-13) |
| 付费 B（顶配档） | 14px | 4px (`rounded`) | 5 色彩虹渐变 | 紫 `#5900ff` | 最高付费档 | (src/components/CoUI/UltraBadge.tsx:7-31) |
| 草稿 | 16px | 4px | 中性 4% + 模糊 `backdrop-blur-[10px]` | `purple-4 #7976ff` | 未发布 | (src/components/WorldCard/DraftBadge.tsx:31-37) |

**付费 A（Pro）** `bg-gradient-to-r from-[#FFF4AC] to-[#FFB87A]`，黑色重体字，`px-1.5`。
**付费 B（顶配）** `linear-gradient(90deg, rgb(255,205,236) 0%, rgb(252,255,215) 25%, rgb(178,255,235) 50%, rgb(149,165,255) 75%, rgb(170,134,255) 100%)`，10px 黑体紫字 `#5900ff`，`px-1.5 py-px`；加 `whitespace-nowrap shrink-0` 防文字被断行。light/dark 共用一套品牌渐变。
**草稿** `border border-purple-4 bg-black/4 text-purple-4 backdrop-blur-[10px] dark:bg-white/4`，前缀小圆点 `size-1 rounded-full bg-purple-4`，内容 `● Draft`。`purple-4 #7976ff` 两主题同值。

> ⚠️ 共用基底铁律：被多处调用的 badge，基础样式是契约。单点对齐用调用处 `className` override，**禁止改基础样式**（历史踩坑：改基底导致 8 处调用同时变形）。

**状态 Badge（合规/审核态，颜色语义化）**

表达「正在审核 / 被限制 / 被封 / 已通过」，颜色即语义，不是分级 tag。两种贴法：行内（inline，icon `size-4`）或封面蒙版（overlay，`bg-black/30 backdrop-blur-xs rounded-lg px-1 py-0.5`）。📍示例: (src/components/ReviewIcon/WorldCardNoteReviewBadge.tsx:73-92)

| 状态 | 容器色（light 示例） | 语义色 |
|---|---|---|
| 封禁/移除 | `border-[rgba(255,68,68,0.20)] bg-[rgba(255,12,12,0.04)]` | 红 = 禁 |
| 限制展示 | `border-[rgba(255,161,51,0.30)] bg-[rgba(247,255,136,0.20)]` | 黄 = 限 |
| 已通过 | `border-[rgba(0,255,209,0.20)] bg-[rgba(0,255,209,0.04)]` | 绿 = 通过 |
| 改级 | `border-[rgba(247,94,204,0.20)] bg-[rgba(247,94,204,0.04)]` | 粉 = 调整 |

横条容器 `rounded-lg border px-3 py-2`，icon `size-6`。📍示例: AuditResultBadge (src/components/ReviewIcon/AuditResultBadge.tsx:39-48)
多态同时命中时按优先级取一个：限制 > 审核中 > 封禁。📍示例: (WorldCardNoteReviewBadge.tsx:53-59)

> 通用形态：状态 Badge 的颜色必须语义化（红=禁/黄=限/绿=通过），caller 不传 `text-*`，色由各状态自带。

---

### 4.4 门控标签（锁 / 会员）

表达「需要更高权限/会员才能用」的胶囊。通用形态是「锁/会员提示标签」——保留这个形态，**不保留具体的会员档位判定逻辑**（那是业务规则）。

📍示例: VipGateTag (src/components/WorldCard/VipGateTag.tsx:11-19)

| 项 | 值 | 类名 |
|---|---|---|
| 高 | 21px | `h-[21px]` |
| 圆角 | 6px | `rounded-md` |
| 内距 | px8 | `px-2` |
| 圆点前缀 | `size-1 rounded-full bg-current`（跟随文字色） | — |
| 字 | 12px bold | `font-roboto text-xs font-bold leading-none` |

> 🌗 **暗亮差异显著（非简单反色）**：light 用主题紫 `border-light3-primary text-light3-primary`（`#923EFC`）/ dark 用重点黄 `border-yellow-1 text-yellow-1`（`#F7FF88`）。这是少数刻意 light=紫 / dark=黄 的 swap，目的是在区块里足够醒目。普通组件仍走 `text-x dark:text-x` 成对反色，门控这类需要「抢注意」的才单独配色。

**门控类 badge 横向对比**

| 类型 | 圆角 | 底 | 字色 | 是否品牌渐变 |
|---|---|---|---|---|
| 付费档（Pro/顶配） | 4px | 金黄 / 彩虹渐变 | 黑 / 紫 | 是（light/dark 共用） |
| 草稿 | 4px | 中性 4% + 模糊 | purple-4 | 否 |
| 门控（会员锁） | 6px | 透明描边 | 紫(L)/黄(D) | 否（描边 + 反 swap） |

---

### 4.5 红点 / 计数（提醒）

#### 红点（布尔提醒）

红点只表达「有/无新内容」，是布尔提醒，**不传达精确数量**。
驱动逻辑（拉未读 count、写 store）与红点视觉是分离的：驱动组件可以 `return null` 无 DOM，红点的 px 样式由各消费点按 store count 自行渲染。📍示例: GlobalRedDot 是纯驱动 (src/components/GlobalRedDot/index.tsx:43)

> 要展示精确数量，用计数 badge，别用红点凑。红点的价值就是「轻、只说有没有」。

#### 计数指示器（剩余量 / 超限警告）

数值 + 三阶段语义色（正常 / 警告 / 超限），表达「还剩多少 / 是否超额」。

📍示例: CharCountIndicator 三阶段 (src/components/WorldCard/CharCountIndicator.tsx:33-44)

| level | 阈值（示例） | 色 |
|---|---|---|
| normal | 未近上限 | 蓝紫 `text-[#7976ff]` |
| warning | 接近上限 | 黄 `text-[#fff1a7]` |
| danger | ≥上限 | 红 `text-[#f44]` |

容器 `flex items-center gap-1 text-[10px]`，格式 `{cur} / {max} chars`。阈值由派生函数算 level，组件只管按 level 上色。

简版计数（不分阶段，仅超额变红）：常态 `text-gray-2 dark:text-gray-1`，超额 `text-red-6`，10px。📍示例: 字段计数 (src/components/WorldCard/BasicInfoSection.tsx:668-670)

---

### 4.6 星级（程度选择）

1–N 颗可点星，表达「程度/优先级」，常配一行随值变化的提示文案。

📍示例: PriorityLevelStars 5 星 (src/components/WorldCard/PriorityLevelStars.tsx:43-94)

| 元素 | 值 | 类名 |
|---|---|---|
| 单星 | 24px | `size-6` |
| 星间距 / 组内距 | gap8 / py12 | `gap-2 py-3` |
| filled | 实心 | `fill currentColor` |
| outline | 空心描边 | `fill none` + `stroke=currentColor strokeWidth=1.2` |
| 星色（🌗） | 黑/白 | `text-black dark:text-white` |
| 提示文案（🌗） | 14px medium，随星级切换 | `text-sm font-medium text-light3-newSecondary dark:text-green-1`（绿） |

实现要点：SVG 用**双层 inset**（`inset-[12.5%]` + `inset-[-5%]`）防 stroke 被容器裁掉。颜色靠 `currentColor` 从父级继承，filled/outline 共用一套 path。

> ⚠️ 注释不是 ground truth：该组件注释标 filled=主题色，但**真实代码是 `text-black dark:text-white`**，以代码为准。仅展示态（如条目行）用同 path 但只渲染已选颗数、无置灰占位，`size-4`。📍示例: (NoteEntryCard.tsx:517-545)

---

### 4.7 进度 / 字数指示器（程度可视化）

#### 进度条（rate/limit 可视化）

📍示例: Achievement/Progress (src/components/Achievement/Progress.tsx:18-34)

| 元素 | 值 | 类名（🌗） |
|---|---|---|
| 轨 | 20px 高全圆 | `h-5 w-full rounded-full bg-black/5 p-0.5 dark:bg-white/5` |
| 填充 | 全圆，宽=rate/limit | `inset-y-0.5 left-0.5 min-w-4 rounded-full bg-purple-1 dark:bg-pink-1` |
| 标签 | 12px bold | `text-xs font-bold`；>60% 时白字压在填充上，否则黑字 |

> 填充设 `min-w-4`：0% 也留一截可见头，避免「空轨看起来像坏了」。标签随进度反色保证可读。

#### 字数/字段标识吸顶条（三阶段变色）

板块标题随内容字数变色，复用 §4.5 的三阶段语义（normal/warning/danger）但作用在容器底色 + 标题色上。📍示例: StickyBannerHeader (src/components/WorldCard/StickyBannerHeader.tsx:41-50)

| level | bg（🌗） | text |
|---|---|---|
| normal | `bg-light3-newSecondary/20 dark:bg-dark3-newSecondary/20`（蓝/紫蓝） | 同色 |
| warning | `bg-yellow-2/10 dark:bg-yellow-7/10`（橙/浅黄） | `text-yellow-2 dark:text-yellow-7` |
| danger | `bg-red-6/20` | `text-red-6` |

> 通用规律：「接近上限」的反馈用 蓝/紫(正常) → 黄(警告) → 红(超限) 三阶语义色，全系统统一（计数文字、进度、吸顶条都遵守），用户一眼认出危险等级。

---

### 4.8 本节图标语义区分（易混）

| 图标 | 语义 | 区别于 |
|---|---|---|
| 实心五角星 | **收藏** | 点赞（心形，不同语义） |
| 描边垃圾桶 | 删除（条目级统一描边变体） | 实心垃圾桶（另一套调用） |
| × | chip/弹窗关闭（`size-3`/`size-4`） | — |

> 收藏星与「程度星级」用的是不同 SVG：星级是独立 inline path（`viewBox 0 0 13.2024 13.2012`），不是收藏图标。
## 五、反馈 · 动效 · 空态 Feedback & Motion

> 覆盖一切「告诉用户系统正在做什么 / 这里没有内容 / 刚发生了什么」的反馈层。三轴：🌗 暗/亮（双值）· 📱 PC/移动 · 🆕 取最新版为准。数值/className 照抄真实代码，📍示例标注 onlychat 出处（`相对路径:行号`）。

### 5.0 一图选型（先看这张表，再翻细则）

| 你遇到的情况 | 选哪种形态 | 理由 |
|---|---|---|
| 列表/网格/卡片首屏拉数据，**布局形状已知** | **骨架屏** | 占位 = 未来内容形状，无跳变，体感比转圈更快 |
| 局部容器/弹窗内拉数据，**布局未知** | **圆环 spinner** | 轻量居中，不必画骨架 |
| 操作型阻塞（提交中/跳转中/整页等待） | **全屏遮罩 spinner** | 盖满 + 半透明遮罩，禁止误操作 |
| 有明确**百分比**的长任务（上传/导入/克隆） | **环形进度** | 圆环 + 中心 % 数字 |
| 等对方/AI 回消息（气泡内） | **打字点** | 聊天专属「正在输入」 |
| 文本逐词吐出（流式/伪流式） | **打字机** | 按分词逐段揭示 |
| 文字旁的小装饰（「生成中」氛围） | **小尺寸 Lottie** | 装饰性，随主题换配色 |
| 滚动到底自动加载下一页 | **触底哨兵 + spinner** | IntersectionObserver 触底拉取 |
| **一次性、自动消失**的操作结果反馈 | **Toast** | 短促、不占版面、不阻断；移动端可叠上滑关闭 |
| 需要**用户继续看见** + 带操作按钮的状态提示 | **Banner 横幅** | 常驻内容流，带 CTA（管理/清除/折叠） |
| 整片区域无数据，**且要引导创建** | **空态 + 新建按钮** | 图标 + 文案 + 「+ 新建」 |
| 整片区域无数据，**引导去别处发现** | **空态 + 跳转按钮** | 图标 + 文案 + 「去逛逛」 |
| 路由命中不存在 | **404 整页** | 主题插画 + 单一回首页 CTA |

核心三问：
1. **加载用骨架还是 spinner？** 布局形状已知 → 骨架（每种卡自己画一份，几何贴合真实卡）；布局未知/弹窗内零散等待 → spinner。有真实百分比 → 环形进度；只是「在转」→ 不定式 spinner。
2. **用 Toast 还是 Banner？** 看完即走、不需操作 → Toast；要用户主动消费 + 带按钮 + 常驻 → Banner。
3. **空态怎么摆？** 居中：图标 → 文案（1–2 行）→ 引导按钮。按动作意图分两种：在此创建（带「+ 新建」）vs 去别处发现（带「去逛逛」跳转）。重型引导（从零搭建）可升级为渐变 hero + 多张入口卡。

---

### 5.1 加载态 Loading

#### 5.1.1 圆环 spinner（局部加载 canonical）

局部加载的标准旋转圆环，可选半透明遮罩 + tip 文案。**局部等待首选**：弹窗内、卡片内、按钮触发后的短暂等待。已知布局形状的列表首屏优先用骨架屏（5.1.3），需盖满整页禁操作时升级为全屏遮罩 spinner（5.1.8）。

| 项 | 通用规格 |
|---|---|
| spinner 尺寸 | 40×40px（`h-10 w-10`） |
| 动画 | `animate-spin`（`spin 1s linear infinite`，0→360°） |
| 圆环色（🌗双值） | 主题色双层：底环用残量灰（亮 `gray-200` / 暗 `gray-600`），高亮弧用 primary（亮紫 / 暗粉） |
| z-index | spinner / tip 同层置顶 |
| tip 文字 | spinner 下 `mt-1`，居中 primary 色 |
| a11y | wrapper `aria-live="polite" aria-busy`；`sr-only` 读 loading 文案 |
| 遮罩态（可选） | `absolute inset-0` 盖满父容器，半透明底（亮白 75% / 暗深灰 75%）+ `blur-xs` |

`visible=false` 渲染 `null`（不占位）。遮罩默认关，开启时盖满**父容器**（非全屏）。

📍示例: onlychat `CoUI/Loading`，圆环色亮 `fill-light3-primary`=`#923EFC` / 暗 `dark:fill-dark3-primary`=`#F75ECC`；遮罩亮 `bg-[rgba(255,255,255,0.75)]` / 暗 `dark:bg-[rgba(44,46,51,0.75)]`，z-`[2000]`（`src/components/CoUI/Loading/index.tsx:21-81`、`LoadingIcon.tsx:1-22`）

#### 5.1.2 环形进度（带百分比）

有明确进度数值时用的圆环进度，中心显示整数百分比。**只在有真实百分比的长任务用**（上传/导入/克隆）；没有可量化进度就退回不定式 spinner。

| 项 | 通用规格 |
|---|---|
| 默认尺寸 | 90px（inline style 控宽高） |
| SVG | viewBox `0 0 100 100`，整体 `-rotate-90`（让 0% 起点在顶部） |
| 进度环 | `r=45`，周长 `2π·45`；`strokeWidth=10`、`strokeLinecap=round` |
| 底环色（🌗双值） | 浅灰（亮）/ 中灰（暗） |
| 进度环色 | primary（紫/粉） |
| 进度过渡 | `transition-all duration-300 ease-out`（strokeDashoffset 平滑动） |
| 中心数字 | 加粗 primary 色，`{round(progress)}%` |
| progress 钳制 | `Math.max(0, Math.min(100, progress))` |
| 底部 tip | `mt-3` 居中小字 |

📍示例: onlychat `ProgressLoading`，底环亮 `text-gray-3`=`#C7C7C7` / 暗 `text-gray-1`=`#707070`，进度环 `text-light3-primary dark:text-dark3-primary`（`src/components/CoUI/Loading/ProgressLoading.tsx:17-94`）

#### 5.1.3 骨架屏 Skeleton

灰块占位 = 未来内容形状，消除首屏跳变。**列表/网格/卡片首屏且布局形状已知**时用：每种卡自己画一份骨架，几何尽量贴合真实卡片（高度、圆角、头像位置）。布局未知或弹窗内零散等待 → 回 spinner。

| 项 | 通用规格 |
|---|---|
| 卡片外框 | 圆角 + 1px 边 + 浅底（🌗双值：亮浅色边/底，暗白边/纯黑底） |
| 占位块底色 | 统一中灰；圆角按形状（文本条 `rounded-sm`、头像 `rounded-full`、气泡 `rounded-[10px]`） |
| 气泡仿真 | 对话气泡尖角处理：右气泡 `rounded-tr-none` / 左气泡 `rounded-tl-none`（缺角仿真实） |
| 动画 | **默认无 shimmer/pulse**（纯静态灰块即可占位）；如需脉动叠 `animate-pulse`（见 5.5 token） |

实现路线：本仓骨架是逐场景手写，**不抽通用 Skeleton 组件**——每种卡自己画。

📍示例: onlychat `MemoryCardSkeleton`，外框亮 `border-purple-2 bg-purple-3` / 暗 `dark:border-white dark:bg-black`，占位块 `bg-gray-1`=`#707070`，预览区 `bg-light3-bg dark:bg-dark3-bg`（`src/components/Skeletons/MemoryCardSkeleton.tsx:3-48`）

#### 5.1.4 打字点（「正在输入」三点）

聊天气泡里对方/AI 还没出字时的三点跳动。**只用于聊天「正在输入」**，不要拿它做通用 loading。

| 项 | 通用规格 |
|---|---|
| 单点 | 8×8px 圆（`w-2 h-2 rounded-full`） |
| 点距 | `gap-x-1` |
| 动画 | `typing 1.2s ease-in-out infinite`（关键帧：15% 透明度.5+上跳 -35% → 30% 透明度1+落回） |
| 错峰 | 第 2 点 delay `.15s`、第 3 点 `.25s`（inline style） |

⚠️ 点色常硬编码深灰、**未做暗色分支**（暗色下仍同一深灰，属可改进点）。

📍示例: onlychat `TypingDot`，单点 `bg-gray-800`（Tailwind 内建灰，非项目 token），动画 `animate-typing-dot`（`src/components/TypingDot/TypingDot.tsx:1-11`、关键帧 `tailwind.config.js:603-614`）

#### 5.1.5 打字机（逐词揭示）

文本逐段揭示（**按分词推进，非逐字符**）。**AI 流式/伪流式文本**用；与打字点配合：先点点点（等待），开始吐字换打字机。纯静态文本不要套。

| 项 | 通用机制 |
|---|---|
| 揭示粒度 | 按空格推进，一次揭示到下一个空格 |
| 节奏 | `setInterval(..., speed)`，speed 由调用方按场景定（聊天快、引导慢，ms/词） |
| 断点续打 | 已揭示前缀命中开头时直接从末尾续，不重打 |
| 收尾 | 揭完触发回调 + 清定时器 |
| 渲染 | 透传给 Markdown 渲染器（支持关键词点击等），无自身视觉样式 |

📍示例: onlychat `TypewriterText`（底层走 `MarkdownText`，`memo` 包裹），`src/components/TypewriterText/TypewriterText.tsx:7-91`

#### 5.1.6 小尺寸装饰 Lottie

文字旁的小尺寸 Lottie（如「灵感生成中」氛围），暗亮各一份 JSON 按主题切。小尺寸、装饰性、循环播放。

| 项 | 通用规格 |
|---|---|
| 容器 | 小尺寸（约 20×40px） |
| 数据源（🌗双值） | 暗/亮各一份 JSON，按 resolvedTheme 切 |
| 配置 | `loop:true autoplay:true`，`preserveAspectRatio:'xMidYMid slice'`，点击不暂停 |

🆕 接入规范：装饰 Lottie 应走项目统一 Lottie 入口（见 5.4.2，带 cloneDeep + unmount destroy 防护），**不要裸用 react-lottie**。

📍示例: onlychat `CoUI/TextLoadingAnimation`（暗 `linggan_dark.json` / 亮 `linggan_light.json`），用在 ChatFooter / 世界卡轮播文案旁。⚠️ 此文件仍裸 `import Lottie from 'react-lottie'` + 顶层 static import JSON，是尚未迁移到统一入口的历史写法（记录现状，非推荐）（`src/components/CoUI/TextLoadingAnimation/index.tsx:7-26`）

#### 5.1.7 触底加载哨兵 & 三态分发器（编排器，非视觉件）

这两个管逻辑不管样式，视觉（骨架/spinner/空态）由你传进去的 fallback 决定。统一用它们能让列表页三态逻辑一致。

| 编排器 | 职责 | 实现 |
|---|---|---|
| 触底哨兵 | 「滚到底拉更多」 | `IntersectionObserver` 监听一个无样式 div，进视口即触发 `onVisible()`（拉下一页）；`children` 由调用方塞 spinner/文案；不支持 observer 时降级为不触发 |
| 三态分发器 | 「loading / 空 / 有数据」三态切换 | 按优先级：loading → loadingFallback；否则 empty → emptyFallback；否则 children。纯条件分发，无样式 |

📍示例: onlychat `LoadingMore`（`src/components/LoadingMore/LoadingMore.tsx:3-34`）+ `LoadingRenderer`（`src/components/LoadingRenderer/LoadingRenderer.tsx:50-66`）

#### 5.1.8 全屏遮罩 loading（整页阻塞）

整页阻塞等待（跳转/全局操作）时盖满全屏的 spinner。**整页阻塞专用**（盖住全站）；局部等待不要用它（会黑全屏），那是 5.1.1 的活。

| 项 | 通用规格 |
|---|---|
| 实现 | 包圆环 spinner，开遮罩，容器 `fixed` 全屏 + 最高 z-index |
| 状态源 | 全局 store 开关 |
| 自动关闭 | 路由变化时自动复位（防卡死） |

📍示例: onlychat `GlobalLoading`（包 `CoUI/Loading`，`withOverlay=true`，`containerClassName="z-[9999] fixed"`，状态走 `useGlobalLoadingStore`，pathname 变化自动 `setLoading(false)`）（`src/components/GlobalLoading/index.tsx:14-49`）

---

### 5.2 空态 Empty State

通用摆法：**居中竖排，图标 → 文案 → 引导按钮**。按引导意图分两类，重型场景可升级为 hero 引导。

#### 5.2.1 列表空态 · 引导创建（带「+ 新建」）

某个 Tab / 空间无内容时：图标 + 文案 + 一颗「+ 新建」按钮。特征是「空 + 引导在此创建」。

| 项 | 通用规格 |
|---|---|
| 外层 | `flex flex-col items-center justify-center gap-3` |
| 图标 | 主题色（🌗双值：亮一色 / 暗一色） |
| 文案 | 浅灰小字，`mt-3` |
| 新建按钮 | 固定尺寸圆角块（如 `h-[40px] w-[200px] rounded-[8px]` + 1px 边），内容 `+` + 文案 |
| 多类型 | 同一组件按 type 切图标 + 文案（不同 Tab 复用一套结构） |

📍示例: onlychat `CardEmptyView`，图标亮 `#B376FF`=purple-6 / 暗 `pink-4`=`#FF8ADC`，文案 `text-gray-0 dark:text-gray-2`，type 含 oc/memory/likes/favorites/profile_card/scene_card/models（`src/components/CardEmptyView/index.tsx:12-42`、`MobileEmptySpaceTip.tsx`）

#### 5.2.2 列表/编辑器空态 · 引导发现（带「去逛逛」）

通用「这里还没内容，去逛逛」：图标 + 双行说明 + 一颗跳转按钮。与 5.2.1 的区别——这个引导「去别处发现」（导向热门/探索），那个引导「在此创建」。

| 项 | 通用规格 |
|---|---|
| 外层 | 上留白居中（如 `mt-[100px] flex flex-col items-center`） |
| 图标 | 64×64（`size-16`，可覆盖） |
| 文案（×2 行） | 标题 + 说明，浅灰小字，`mt-3` |
| 跳转按钮 | 宽胶囊（如 `h-10 w-[300px] rounded-3xl`），导向热门/探索 |

📍示例: onlychat `CoUI/EditorEmptyState`，文案色 `text-gray-2`=`#9E9E9E`，按钮文案默认导向 trending（`src/components/CoUI/EditorEmptyState/EditorEmptyState.tsx:16-43`）

#### 5.2.3 编辑器 Hero 空态 · 从零搭建（渐变标题 + 入口卡）

重型引导空态，比通用空态隆重得多：用大号**渐变 hero 标题**制造仪式感 + 副标 + **多张分类入口卡**。只用在「从零搭建」的编辑器初始无内容场景。

| 项 | 通用规格 |
|---|---|
| 外层 | `flex flex-col items-center gap-5 px-4 py-12` |
| Hero 标题 | 大号加粗斜体（如 `text-[50px] font-bold italic`），`bg-clip-text text-transparent` + 渐变上色 |
| Hero 渐变（🌗双值） | 两套渐变：亮一组、暗一组（暖→冷过渡） |
| Hero 收尾 | italic 末字母右倾，渐变末端留 `pr-2` 余量，防 bg-clip-text 方形裁切 |
| 副标题 | 限宽居中浅灰小字，可分两段 |
| 入口卡区 | 等宽横排 `flex-wrap gap-3`，窄屏换行；每张卡是一个分类入口，可挂推荐角标 |
| 入口卡图标 | 走 inline SVG（非 `<img>`，才能由 className 控亮暗）：结构色黑↔白、装饰色 primary 紫↔粉随主题翻转 |

📍示例: onlychat `WorldCard/NoteEditorEmptyState`（世界卡 PC 编辑页右栏空态，🆕 world-book 分支，Figma `14977:193686`）：Hero 渐变亮 `from-[#ffa133] to-[#b376ff]`（橙→紫）/ 暗 `dark:from-[#fff1a7] dark:to-[#f75ecc]`（黄→粉），副标 `text-gray-1`=`#707070`，3 张入口卡 character（带 Most Start Here 角标）/ location / rule（`src/components/WorldCard/NoteEditorEmptyState.tsx:20-55`、`StarterCard.tsx:35-39`）

#### 5.2.4 路由级 404 兜底

整页接管的 404：主题插画 + 标题 + 单一回首页 CTA。

| 项 | 通用规格 |
|---|---|
| 全屏容器 | `flex h-screen w-screen items-center justify-center` + 页面背景（🌗双值） |
| 插画（🌗双值） | 亮/暗整张换图 |
| 标题 | 居中限宽 |
| 回首页按钮 | primary 底胶囊 + hover `brightness-110` |
| 副作用 | mount 时上报监控（404 计数） |

行为：webview 内走原生返回关 webview；纯 web `router.push` 回首页（可带 cache-buster）。

📍示例: onlychat `NotFound`，背景亮 `light3-bg`=`#FCFCFC` / 暗 `dark3-bg`=`#202020`，插画 `/404-light.png` / `/404-dark.png`，mount 时 `Sentry.captureException`（`src/components/NotFound/index.tsx:12-63`）

---

### 5.3 Toast / 消息条

**Toast = 一次性、自动消失、不阻断**的操作结果反馈。本体样式/底色由 Toast 库（如 `react-hot-toast`）+ 项目 Toast provider 配置决定。这里只收一个可复用增强：**移动端上滑关闭**。

#### 5.3.1 可上滑关闭的 Toast 容器

包在 Toast 内的容器，移动端上滑超阈值即关闭。无自身视觉（透传 Toast 内容），只加滑动手势。PC 无触屏不生效。

| 项 | 通用规格 |
|---|---|
| 关闭阈值 | 向上滑 > 20px |
| 关闭动作 | `toast.dismiss(id)` |
| 回弹 | 未过阈值复位回 0 |
| 跟手位移 | `transform: translateY(${moveY}px)`，`transition: transform 0.2s ease-out` |
| 监听 | touchstart/move/end（仅触屏） |

📍示例: onlychat `SwipeableToastContent`，`src/components/SwipeableToastContent/SwipeableToastContent.tsx:5-63`

---

### 5.4 Banner 横幅

**Banner = 常驻内容流、要用户主动消费、带 CTA** 的状态提示。比 Toast 重（Toast 看完即走，Banner 要操作 + 持续可见）。三种通用形态：信息型（轻提示 + 撤销）、结果型（操作结果 + 入口按钮）、sticky 结构型（板块标识 + 状态语义 + 吸顶）。

#### 5.4.1 信息型横幅（轻提示 + 撤销入口）

低存在感的状态提示 + 一颗操作按钮（如「已恢复草稿」+ 清除）。特征：透明度极低的底色蒙层、随用户后续动作自动消失。

| 项 | 通用规格 |
|---|---|
| 外层 | 圆角 + 小内距 + 极淡蒙层底（🌗双值：亮黑 4% / 暗白 4%） |
| 文字 | 主文字色（🌗双值 黑↔白） |
| 操作按钮 | 小圆角块，次级色底（🌗双值，可反相：亮一色白字 / 暗一色黑字） |
| 显隐 | 触发态显示；用户后续动作（改字段/提交/点撤销）即自动消失 |
| 📱差异 | 移动留边 `mx-4` → PC 贴边 `md:mx-0`；圆角/内距/字号按断点放大 |

📍示例: onlychat `WorldCard/DraftRestoredBanner`（草稿恢复提示，PRD §8.11.3），底 `bg-black/4 dark:bg-white/4`，Clear 按钮亮 `bg-light3-newSecondary`=`#3BA6F3` 白字 / 暗 `dark:bg-dark3-secondary`=`#A8EF30` 黑字；改任意字段（dirtyFields 非空）/ 提交 / 点 Clear 即消失（`src/components/WorldCard/DraftRestoredBanner.tsx:13-33`）

#### 5.4.2 结果型横幅（操作结果 + 入口按钮）

操作完成后告诉用户结果 + 给后续入口（如导入完成 + 「去管理」）。带标题、关闭叉、说明、CTA 按钮。比 Toast 重（要用户主动消费 + 操作），常驻内容流。

| 项 | 通用规格 |
|---|---|
| 外层 | 圆角 + 内距 + 渐变底（如品牌色左浓右淡 30%→10%） |
| 布局 | 竖排：标题行（标题 + 关闭叉）+ 正文行（说明 + CTA 按钮） |
| 标题 | 加粗主文字色（🌗双值 黑↔白） |
| 关闭叉 | 小尺寸 inline SVG 十字（如 12px 容器内 7px 叉，`strokeLinecap=round`） |
| 说明 | 浅灰小字 |
| CTA 按钮 | 胶囊，品牌色底白字加粗 |

📍示例: onlychat `WorldCard/ImportResultBanner`（导入结果，Figma `14991:202018`），渐变 `from-purple-4/30 to-purple-4/10`（`purple-4`=`#7976FF`），Manage 按钮 `bg-purple-4` 白字；仅移动端导入后展示、初始 hidden（`src/components/WorldCard/ImportResultBanner.tsx:19-78`）

#### 5.4.3 sticky 结构型横幅（板块标识 + 状态语义 + 吸顶）

长表单/编辑器各板块的标题条，三合一：① 板块标题（吸顶常驻分隔）② 随进度变色的状态语义（如字数预算蓝→黄→红）③ 移动端可折叠收纳长板块。是「带状态语义的结构化 Banner」，不是临时提示。

| 项 | 通用规格 |
|---|---|
| 外层 | `w-full` + 页面背景底 + `sticky`（top 默认 0，可配） |
| z-index（📱差异） | 移动低层（不压住更高的导航条）/ PC 高层（盖过 nav） |
| 内层 banner | `rounded-[12px] overflow-hidden p-3`；tone 色走 `absolute inset-0` 半透明蒙层，外层不透明 page bg 做挡板（否则圆角透明像素会让下方内容透出） |
| 标题 | `text-base font-bold` + tone.text |
| 折叠 chevron（📱差异） | **仅移动端**：展开朝下 / 收起 `-rotate-90` 朝右；PC 无 chevron、点击不折叠（始终展开） |
| 状态计数 | 小字（如 `text-[10px]`）+ tone.text，右对齐 |

状态三阶配色（以字数预算为例，🌗每阶都带暗色分支）：

| 阶段 | 触发 | bg / text 思路 |
|---|---|---|
| normal | 常态 | 次级色 20% 底 + 同色字 |
| warning | 接近上限 | 黄系 10% 底 + 黄字 |
| danger | 超限 | 红系 20% 底 + 红字 |

📍示例: onlychat `WorldCard/StickyBannerHeader`（板块标题 + 实时字数预算，Figma mobile `14870:136763` / web `14983:195468`），z-index 移动 `z-[5]` / PC `z-20`；三阶 normal `bg-light3-newSecondary/20 dark:bg-dark3-newSecondary/20`（亮 `#3BA6F3` / 暗 `#7976FF`）→ warning `bg-yellow-2/10 dark:bg-yellow-7/10`（亮 `#FFA133` / 暗 `#FFF1A7`）→ danger `bg-red-6/20`（`#FF4444`）（`src/components/WorldCard/StickyBannerHeader.tsx:36-140`）

---

### 5.5 装饰动效 Motion

#### 5.5.1 全屏粒子装饰（节日/氛围彩蛋）

全屏覆盖的粒子动效（如落雪），多重门控显示。通用形态——具体节日（圣诞等）只是触发条件之一，复用的是「全屏粒子 + 门控 + 可开关 + 避开专注场景」这套结构。

| 项 | 通用规格 |
|---|---|
| 容器 | `fixed inset-0` + 最高 z-index（盖顶） |
| 粒子数 | 按视口宽度算（resize 防抖） |
| 运动参数 | 下落速度/横向风/半径/颜色按效果调（如雪：speed `[0.5,1]`、wind `[0,0]`、radius `[0.5,2.5]`、淡蓝白色） |
| 门控（全真才显示） | ① 触发条件（节日配置）② 用户开关 ③ 路由白名单——**避开聊天/创建等专注场景** |

📍示例: onlychat `Snowfall`（圣诞落雪，`react-snowfall`），雪花数 `floor(bodyWidth/6.5)`，色 `#dee4fd`；门控：`isChristmas` && 开关 store && 路由不在 `/create`、`/chat`、`/memory`（`src/components/Snowfall/Snowfall.tsx:12-58`）

#### 5.5.2 Lottie 统一入口

项目内 Lottie 动画的 canonical 封装。所有 Lottie（庆祝、解锁、点赞、灵感闪烁等）统一走它，由它兜底内存安全。

| 项 | 通用规格 |
|---|---|
| 入口 | 透传 Lottie 库选项 + width/height/deepClone |
| 默认配置 | `loop:false autoplay:true`（可被 props 覆盖） |
| 防内存膨胀 | `deepClone=true` → `cloneDeep(animationData)` |
| 生命周期 | unmount 时 `destroy()` |
| 命令式控制 | 同时提供 `play / stop`（hook 形态） |

🆕 规范：**新代码唯一允许的 Lottie 入口**。禁止裸用 `react-lottie`/`lottie-react`/`lottie-web`（绕过 cloneDeep + destroy 防护）。JSON 体积大时按需 dynamic import。

📍示例: onlychat `CoUI/Lottie`（三 surface：声明式 `<Lottie>` / 命令式 `useLottie` / 点按 `useLottieSwitch`）（`src/components/CoUI/Lottie/index.tsx:1-9`、`hooks/useLottie.tsx:10-38`）

#### 5.5.3 动效 token（动画/关键帧）

反馈/动效相关的可复用动画 class，统一收在 tailwind 配置。

| class | 定义 | 用途 |
|---|---|---|
| `animate-spin` | `spin 1s linear infinite`（0→360°） | 圆环 spinner |
| `animate-pulse` | `pulse 1.5s ease-in-out infinite`（opacity 1→.5→1） | 骨架/呼吸（如需） |
| `animate-typing-dot` | `typing 1.2s ease-in-out infinite`（15% 上跳淡出 → 30% 落回） | 打字点三点 |
| `animate-loading-ellipsis` | `loadingEllipsis 1.2s steps(3, jump-start) infinite`（宽 0→0.9em） | 省略号 `. / .. / ...` 步进 |
| `animate-float-up` | `floatUp 2s ease-in-out forwards`（translateY 0→-5rem + 淡出） | 数值飘字上浮 |
| `animate-fade-in-up` | `fadeInUp 200ms cubic-bezier(0,0,0.2,1) both` | 区块进场淡入+上移 |
| `animate-fade-slide-left` | `fadeSlideLeft 300ms cubic-bezier(0,0,0.2,1) both` | 内容切换右→左滑入 |
| `animate-value-increase/decrease` | `valueIncrease/Decrease 1s` | 数值增减强调 |
| `animate-sparkle-twinkle / breath` | 3s / 4s ease-in-out infinite | 装饰 sparkle 闪烁/呼吸 |

a11y 守护：显式保留 `animation.none` 以支持 `motion-reduce:animate-none`。**装饰型/循环动效**（脉动、sparkle、sheen 等）按规范必须配 `motion-reduce:animate-none` 兜底。

> 打字点 vs 省略号点的区别：打字点是聊天气泡三个圆点跳动；省略号点是「文字后 . → .. → ...」的步进揭示（`steps(3, jump-start)`，内层宽 0→0.9em），消费端需外层预留 `0.9em` 防居中抖动，`motion-reduce` 时静态显示 `...`。

📍示例: onlychat `tailwind.config.js:406-470`（animation）/ `471-648+`（keyframes）
## 六、图标 Icons

> 分类按【功能语义】，与具体工程实现解耦。每个功能取**最新/在用版**作 canonical（权威示例），给出 viewBox / 默认尺寸 / 着色方式 + 已废弃旧版对照。
> onlychat 真实文件路径（`相对路径:行号`）作为「推荐文件」示例与最新版权威保留；🆕 标记最新版判定结论。数值照抄源码，未列出的不臆造。
> 轴：🌗 暗/亮主题 · 📱 PC/移动 · 🆕 取最新版为准。

### 6.1 概览与通用约定

图标全部是**手写内联 SVG 的 React 组件**（无 sprite、无 iconfont、无第三方 icon 库），分三类来源：

| 来源 | 角色 |
|---|---|
| 业务通用图标主库（`src/components/CoUI/icon/`，251 个 `.tsx`，另有 `nav/`、`CreateModal/` 子目录） | 绝大多数功能取这里 |
| 独立图标目录（`src/components/Icon/`，16 个） | 少量独立图标；多与主库重复，主库版使用量更高为准；唯一例外 `BackArrowIcon` 只在这里 |
| 角色卡复合组件（`src/components/CharacterIcon/`） | 带审核态/限制态逻辑的视觉组件，**不是纯图标**，不在 icon 清单内 |

**全库统一约定（几乎所有图标都遵守）：**

- 组件签名 `function XxxIcon(props: HTMLProps<SVGSVGElement>)`，`{...props}` 透传给根 `<svg>` → **尺寸/颜色全由调用处 `className` 控制**（`size-*` / `h-* w-*` / `text-*`）。
- 着色：路径 `fill="currentColor"`（实心款）或 `stroke="currentColor"`（描边款）→ 颜色继承 CSS `color`。**故图标本身无暗/亮分支，🌗 差异完全靠调用处 `text-*` token + `dark:` 解决**（见 6.4）。
- SVG 上写死的 `width`/`height` 是「该图标默认/Figma 导出尺寸」，**不是固定尺寸**——调用处可用 `className` 覆盖（`size-6` 等）。
- 极少数图标硬编码 hex（属历史遗留），下文逐个标注。
- ⚠️ 铁律：图标的「最新改动」≠「采纳最广」。canonical 按**使用量**判定，新版/描边款作备选标注（典型：`CheckV3Icon` 是 2026-05-19 最新描边款但仅 1 处用，canonical 仍是 `CheckIcon`）。

### 6.2 功能 → 推荐（最新）图标 总表

每行：功能语义 → 推荐文件（示例）→ viewBox / 默认尺寸 / 着色 → 出处。**推荐版按使用量 canonical**，同功能旧版见 6.3。

| 功能 | 推荐文件 | export | viewBox | 默认尺寸 | 着色 | 出处 |
|---|---|---|---|---|---|---|
| 删除/垃圾桶 | `CoUI/icon/DeleteIcon.tsx` | default `DeleteIcon` | `0 0 16 16` | 16×16 | `fill=currentColor`（实心垃圾桶，含两条竖纹） | `CoUI/icon/DeleteIcon.tsx:5-16` |
| 返回（back） | `Icon/BackArrowIcon.tsx` | default `BackArrowIcon` | `0 0 24 27` | 24×24 | `stroke=currentColor` `strokeWidth=2.2` `strokeLinecap=round`（描边折线「‹」，带 drop-shadow，locale=ar 自动 `rotate-180`） | `Icon/BackArrowIcon.tsx:8-27` |
| 向上收起（chevron up） | `CoUI/icon/ChevronUpIcon.tsx` | default `ChevronUpIcon` | `0 0 24 24` | 24×24 | `fill=currentColor`（实心三角朝上，`id=Icon/arrow`） | `CoUI/icon/ChevronUpIcon.tsx:5-19` |
| 向下展开（chevron down） | `CoUI/icon/ChevronDownIcon.tsx` | default `ChevronDownIcon` | `0 0 20 20` | 20×20 | `fill=currentColor`（实心三角） | `CoUI/icon/ChevronDownIcon.tsx:5-15` |
| 列表项进入（chevron right） | `CoUI/icon/ChevronRightIcon.tsx` | default `ChevronRightIcon` | `0 0 20 20` | 20×20 | `fill=currentColor`（实心小三角，**实为下三角**，名不副实历史遗留） | `CoUI/icon/ChevronRightIcon.tsx:5-17` |
| 通用三角指示（下拉） | `CoUI/icon/TriangleIcon.tsx` | default `TriangleIcon` | `0 0 12 12` | 12×12 | `fill=currentColor`（实心下三角，下拉指示） | `CoUI/icon/TriangleIcon.tsx:5-14` |
| 双向箭头/展开收起 | `CoUI/icon/DoubleArrowIcon.tsx` | named `DoubleArrowIcon` | `0 0 24 24` | 24×24 | `fill=currentColor`（两个朝左 V 形「«」） | `CoUI/icon/DoubleArrowIcon.tsx:4-21` |
| 关闭/X | `CoUI/icon/CloseIcon.tsx` | default `CloseIcon` | 默认 `0 0 24 25`（withShadow 时 `0 0 24 24`） | 默认 24×25（withShadow 24×24） | `fill=currentColor`；`withShadow` prop 加 drop-shadow；另导出 `LightCloseIcon`（圆形带叉 18×18） | `CoUI/icon/CloseIcon.tsx:5-143` |
| 添加/加号 | `CoUI/icon/PlusIcon.tsx` | default `PlusIcon` | `0 0 16 16` | 16×16 | `fill=currentColor`（十字加号，`id=Icon/general_chatplus_16`）；另导出 `PlusIconWithNoMargin`（20×20 两条 rounded rect） | `CoUI/icon/PlusIcon.tsx:5-46` |
| 复制 | `CoUI/icon/CopyIcon.tsx` | default `CopyIcon` | `0 0 16 16` | 16×16 | `fill=currentColor`（双层方框） | `CoUI/icon/CopyIcon.tsx:5-17` |
| 分享 | `CoUI/icon/ShareIcon.tsx` | default `ShareIcon` | `0 0 12 12` | 12×12 | `fill=currentColor`（描边箭头+曲线，`id=Icon/general_share_12_xian`） | `CoUI/icon/ShareIcon.tsx:5-21` |
| 编辑/铅笔 | `CoUI/icon/EditIcon.tsx` | default `EditIcon` | `0 0 24 24` | 24×24 | `fill=currentColor` `fillRule=evenodd`（铅笔+下划线） | `CoUI/icon/EditIcon.tsx:5-19` |
| 更多（竖排三点） | `CoUI/icon/ThreeDotsVerticalIcon.tsx` | default `ThreeDotsVerticalIcon` | `0 0 16 16` | 16×16 | `fill=currentColor` `fillRule=evenodd`（三个圆点，`id=Icon/main`） | `CoUI/icon/ThreeDotsVerticalIcon.tsx:5-22` |
| 菜单（列表/汉堡） | `CoUI/icon/MenuLineIcon.tsx` ⚠️见下注 | default `MenuLineIcon` | `0 0 24 24` | 24×24 | `fill=currentColor`（圆点+横线交替的列表菜单） | `CoUI/icon/MenuLineIcon.tsx:3-25` |
| 收藏（星） | `CoUI/icon/FavoriteIcon.tsx` | default `FavoriteIcon` | `0 0 12 13` | 12×13 | `fill=currentColor`（实心五角星，收藏语义） | `CoUI/icon/FavoriteIcon.tsx:4-17` |
| 点赞/喜欢（拇指） | `CoUI/icon/LikeIcon.tsx` | default `LikeIcon`（带 `active` prop） | active `0.5 0.5 16 16` / 非 active `0 0 24 24` | active 16×16 / 非 active 24×24 | `fill=currentColor`（拇指，active 实心 / 非 active 描边轮廓） | `CoUI/icon/LikeIcon.tsx:6-43` |
| 搜索 | `CoUI/icon/SearchIcon.tsx` | default `SearchIcon` | `0 0 24 24` | 24×24 | `fill=currentColor`（放大镜，`id=Icon/search`） | `CoUI/icon/SearchIcon.tsx:5-21` |
| 设置/齿轮 | `CoUI/icon/SettingIcon.tsx` | default `SettingIcon` | `0 0 24 24` | 24×24 | `fill=currentColor`（齿轮+中心圆） | `CoUI/icon/SettingIcon.tsx:5-17` |
| 对勾（纯勾） | `CoUI/icon/CheckIcon.tsx` | default `CheckIcon` | `0 0 20 20` | 20×20 | `fill=currentColor`（实心对勾，`id=Icon/duicuo`） | `CoUI/icon/CheckIcon.tsx:5-20` |
| 对勾（圆框选中） | `CoUI/icon/CheckCircleIcon.tsx` | default `CheckCircleIcon` | `0 0 24 24` | **16×16**（width/height 写 16，viewBox 24） | `fill=currentColor`（圆框内对勾） | `CoUI/icon/CheckCircleIcon.tsx:5-18` |
| 锁/基础锁 | `CoUI/icon/LockIcon.tsx` | default `LockIcon` | `0 0 16 16` | 16×16 | `fill=currentColor` `fillRule=evenodd`（挂锁带钥匙孔） | `CoUI/icon/LockIcon.tsx:5-19` |
| 发送 | `CoUI/icon/SendIcon.tsx` | **named** `SendIcon` | `0 0 20 20` | 20×20 | `fill=currentColor`（纸飞机/箭头） | `CoUI/icon/SendIcon.tsx:3-18` |

> ⚠️ **「菜单/更多」命名陷阱（recon 标签纠正）**：recon 表把 `CoUI/icon/MenuIcon.tsx` 标为「汉堡菜单 canonical」，但**读源码发现 `MenuIcon.tsx` 渲染的是三个竖排圆点**（3 个 `<path>`，圆心 x=12，y=5/12/19，r=2，`0 0 24 24`，`CoUI/icon/MenuIcon.tsx:13-24`）——视觉上是「更多」三点而非汉堡。真正的列表/菜单图标是 `MenuLineIcon.tsx`（圆点+横线交替）。**竖排三点「更多」首选 `ThreeDotsVerticalIcon`（16×16，使用量更高）**；`MenuIcon`（24×24 三点）是同语义的另一尺寸版本。本表「菜单」行因此改推 `MenuLineIcon`，与 recon 标签不一致之处以源码为准。

### 6.3 各功能 DOM 骨架与已废弃版对照

> 逐功能给出推荐版的 SVG 结构骨架（仅保留结构性属性）+ 同功能「已废弃 / 旧版 / 边界」对照表。

#### 删除 / 垃圾桶

推荐 `DeleteIcon`（实心）。

```svg
<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
  <path d="M4.99997 3.2V2H11V3.2H14V4.4H12.8V13.4 ... 8.59997 6.2H9.79997V11H8.59997V6.2Z" fill="currentColor" />
</svg>
```

| 文件 | 视觉 | 状态 | 出处 |
|---|---|---|---|
| `DeleteIcon` 🆕 | 实心垃圾桶含两竖纹，16×16 fill | ✅ canonical（21 处） | `CoUI/icon/DeleteIcon.tsx` |
| `TrashOutlineIcon` | 描边垃圾桶（盖+把手+桶身+两竖线），`stroke=currentColor` `strokeWidth=1.4` `0 0 16 16`，自带 `aria-hidden` | ⚠️ 描边场景专用（7 处），与实心 DeleteIcon 视觉不同，**不是版本关系**——要描边款才用 | `CoUI/icon/TrashOutlineIcon.tsx:6-30` |
| `RemoveIcon` | 视觉几乎等同 DeleteIcon（实心垃圾桶 16×16），但**语义=移除**而非删除 | ⚠️ 语义不同（6 处），别当 DeleteIcon 替身用 | `CoUI/icon/RemoveIcon.tsx:3-18` |

> `DeleteIcon` 与 `RemoveIcon` 路径几乎一致（都是垃圾桶），但约定 `DeleteIcon`=删除、`RemoveIcon`=移除（减号语义）。选用按语义，不按视觉。

#### 箭头家族（返回 / chevron / 三角 / 双向）

箭头按「形态 + 方向」拆成多个独立图标，没有统一旋转的单一箭头。各取最新/最高频版：

| 用途 | 推荐 | viewBox | 默认尺寸 | 形态 | 出处 |
|---|---|---|---|---|---|
| 返回（页面级） | `Icon/BackArrowIcon` 🆕 | `0 0 24 27` | 24×24 | 描边「‹」+ drop-shadow，ar 语言 `rotate-180`，`strokeWidth=2.2` | `Icon/BackArrowIcon.tsx:8-27` |
| 收起（向上） | `CoUI/icon/ChevronUpIcon` 🆕 | `0 0 24 24` | 24×24 | 实心上三角（41 处，最高频箭头），`id=Icon/arrow` | `CoUI/icon/ChevronUpIcon.tsx` |
| 展开（向下） | `CoUI/icon/ChevronDownIcon` | `0 0 20 20` | 20×20 | 实心三角（5 处） | `CoUI/icon/ChevronDownIcon.tsx` |
| 列表进入 | `CoUI/icon/ChevronRightIcon` | `0 0 20 20` | 20×20 | 实心三角（10 处，路径实为下三角，历史遗留） | `CoUI/icon/ChevronRightIcon.tsx` |
| 下拉三角 | `CoUI/icon/TriangleIcon` | `0 0 12 12` | 12×12 | 实心下三角（13 处） | `CoUI/icon/TriangleIcon.tsx` |
| 双向展开 | `CoUI/icon/DoubleArrowIcon` | `0 0 24 24` | 24×24 | 双 V 形（11 处） | `CoUI/icon/DoubleArrowIcon.tsx` |

**已废弃 / 边界版：**

| 文件 | 状态 | 说明 | 出处 |
|---|---|---|---|
| `CoUI/icon/ChevronLeftIcon` | 备选 | 实心左三角 20×20，左向版 | `CoUI/icon/ChevronLeftIcon.tsx:5-17` |
| `CoUI/icon/ChevronRightOutlineIcon` | 描边备选（2 处） | 真正的「›」描边右箭头 `strokeWidth=2.2` `0 0 16 16`；代码注释明确「`ChevronRightIcon` 画的是实心下三角名不副实勿改」 | `CoUI/icon/ChevronRightOutlineIcon.tsx:4-24` |
| `CoUI/icon/ArrowTriangleIcon` | 边界（1 处） | 圆角实心上三角 24×24，使用面窄 | `CoUI/icon/ArrowTriangleIcon.tsx:3-18` |
| `CoUI/icon/ArrowUpIcon` | 边界 | 上箭头柄（非三角，12×12 `↑` 形） | `CoUI/icon/ArrowUpIcon.tsx:3-18` |
| `Icon/ArrowIcon` | ⚠️ Icon 目录旧版 | 实心下三角 `0 0 21 20`，与 CoUI Chevron 重复，新代码用 CoUI 版 | `Icon/ArrowIcon.tsx:3-8` |

#### 关闭 / X

推荐 `CoUI/icon/CloseIcon`（全站最高频，92 处）。一个文件含 3 个 export：

```svg
<!-- 默认 CloseIcon：viewBox 0 0 24 25, 24×25, id=Icon/general_delete_24 -->
<svg width="24" height="25" viewBox="0 0 24 25" fill="none">
  <g id="Icon/general_delete_24"><path id="Vector" d="M11.9997 10.7039 ..." fill="currentColor" /></g>
  <!-- defs 内含 filter0_d（drop-shadow，仅 withShadow 分支用）+ clipPath -->
</svg>
<!-- withShadow=true：viewBox 0 0 24 24, 24×24, 路径外包 filter0_d 投影 -->
```

| export | viewBox / 尺寸 | 用途 | 出处 |
|---|---|---|---|
| `CloseIcon`（default，`withShadow=false`） | `0 0 24 25` / 24×25 | 普通弹窗关闭 X | `CoUI/icon/CloseIcon.tsx:67-124` |
| `CloseIcon`（`withShadow={true}`） | `0 0 24 24` / 24×24，带 `filter0_d` drop-shadow | 图片/深色背景上的关闭 X（需投影描边） | `CoUI/icon/CloseIcon.tsx:9-66` |
| `LightCloseIcon`（named） | `0 0 18 18` / 18×18 | 圆形带叉的小关闭按钮 | `CoUI/icon/CloseIcon.tsx:127-143` |

**已废弃 / 重复版：**

| 文件 | 状态 | 说明 | 出处 |
|---|---|---|---|
| `Icon/CloseIcon`（`CloseIcon` named） | ⚠️ Icon 目录重复版（24 处） | 24×24 实心 X，CoUI 版使用量更高（92），新代码优先 CoUI | `Icon/CloseIcon.tsx:3-20` |
| `Icon/CloseIcon`（`SmallCloseIcon` named） | ⚠️ 硬编码色 | 12×13，**fill 写死 `#707070`**（不跟 currentColor），慎用 | `Icon/CloseIcon.tsx:22-42` |
| `CoUI/icon/CloseCircleIcon`（default） | 圆形变体（9 处） | 圆框带叉 24×24 `viewBox 2 2 22 22` | `CoUI/icon/CloseCircleIcon.tsx:5-21` |
| `CoUI/icon/CloseCircleIcon`（`CloseCircleIconV2` named） | 圆形小号变体 | 16×16 实心圆带叉 | `CoUI/icon/CloseCircleIcon.tsx:23-46` |

#### 添加 / 加号

推荐 `CoUI/icon/PlusIcon`（39 处）。

```svg
<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
  <g id="Icon/general_chatplus_16"><path id="Vector" d="M7.33337 7.33337V3.33337 ... " fill="currentColor" /></g>
</svg>
```

| 文件 / export | 状态 | 说明 | 出处 |
|---|---|---|---|
| `PlusIcon`（default） 🆕 | ✅ canonical（39 处） | 十字加号 16×16 | `CoUI/icon/PlusIcon.tsx:3-22` |
| `PlusIconWithNoMargin`（named） | 备选 | 20×20，两条 rounded `<rect>`（无内边距版） | `CoUI/icon/PlusIcon.tsx:24-46` |
| `CoUI/icon/CirclePlusIcon` | 大尺寸专用（6 处） | **79×80**（`0 0 79 80`），圆框内加号，用于大号「创建」入口，不是通用小加号 | `CoUI/icon/CirclePlusIcon.tsx:2-24` |
| `Icon/AddIcon` | ⚠️ Icon 目录旧版 | **31×31**（`0 0 31 31`）十字加号，与 PlusIcon 重复，新代码用 CoUI `PlusIcon` | `Icon/AddIcon.tsx:3-9` |

#### 复制

推荐 `CoUI/icon/CopyIcon`（8 处，CoUI 唯一）。

```svg
<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
  <path d="M4.66667 3.99992V1.99992 ..." fill="currentColor" /> <!-- 双层方框 -->
</svg>
```

| 文件 | 状态 | 说明 | 出处 |
|---|---|---|---|
| `CoUI/icon/CopyIcon` 🆕 | ✅ canonical（8 处） | 双层方框 16×16 | `CoUI/icon/CopyIcon.tsx:3-19` |
| `Icon/CopyIcon` | ⚠️ Icon 目录重复版 | 同为双层方框 16×16（路径略不同），CoUI 版优先 | `Icon/CopyIcon.tsx:3-20` |

#### 分享

推荐 `CoUI/icon/ShareIcon`（12 处）。

```svg
<svg width="12" height="12" viewBox="0 0 12 12" fill="none">
  <g id="Icon/general_share_12_xian"><path id="Vector" d="M6.5 7H5.5 ..." fill="currentColor" /></g>
</svg>
```

| 文件 | 状态 | 说明 | 出处 |
|---|---|---|---|
| `CoUI/icon/ShareIcon` 🆕 | ✅ canonical（12 处） | 描边箭头+曲线 12×12 | `CoUI/icon/ShareIcon.tsx:3-21` |
| `ShareFillIcon` | 备选（5 处） | 实心分享变体 | `CoUI/icon/ShareFillIcon.tsx` |
| `ShareOutlineIcon` | 备选（3 处） | 描边变体 | `CoUI/icon/ShareOutlineIcon.tsx` |
| `ShareFillIconV2` | 边界新版（2 处） | 实心新款 **20×20**（`0 0 20 20`），使用面窄 | `CoUI/icon/ShareFillIconV2.tsx:3-19` |

#### 编辑 / 铅笔

推荐 `CoUI/icon/EditIcon`（34 处）。

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path fillRule="evenodd" clipRule="evenodd" d="M13.4091 3.70108 ..." fill="currentColor" /> <!-- 铅笔+下划线 -->
</svg>
```

唯一 canonical。`WorldEditIcon` 在库中存在但 0 处引用，不用。

#### 更多（三点） / 菜单

| 语义 | 推荐 | 形态 | 出处 |
|---|---|---|---|
| 更多（竖排三点，弹菜单） | `ThreeDotsVerticalIcon` 🆕 | 16×16 三圆点 `fillRule=evenodd`，`id=Icon/main`（12 处） | `CoUI/icon/ThreeDotsVerticalIcon.tsx:5-22` |
| 更多（同语义大号） | `MenuIcon` | **24×24 三竖排圆点**（非汉堡！3 个 `<path>` 圆心 x=12 y=5/12/19 r=2） | `CoUI/icon/MenuIcon.tsx:5-25` |
| 列表 / 菜单（行+点） | `MenuLineIcon` | 24×24，圆点+横线交替的列表样式 | `CoUI/icon/MenuLineIcon.tsx:3-25` |

```svg
<!-- ThreeDotsVerticalIcon：三个独立圆点路径 -->
<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
  <g id="Icon/main"><path id="Shape" fillRule="evenodd" clipRule="evenodd"
    d="M8.00001 5.33341C8.73334 ... 7.26667 10.6667Z" fill="currentColor" /></g>
</svg>
```

> 语义区分铁律：竖排三点（`ThreeDotsVerticalIcon` / `MenuIcon`）= **更多**；列表横线（`MenuLineIcon`）= **菜单/列表**。⚠️ recon 把 `MenuIcon` 标为「汉堡」是误判——`MenuIcon` 源码是三竖排圆点，不是汉堡横线。

#### 收藏（星） vs 点赞（拇指）

两者**不同语义，不可互换**：

```svg
<!-- FavoriteIcon 收藏：实心五角星 -->
<svg width="12" height="13" viewBox="0 0 12 13" fill="none">
  <path d="M5.25855 2.71993C5.60014 ... 4.69716 4.06966L5.25855 2.71993Z" fill="currentColor" />
</svg>
```

| 语义 | 推荐 | viewBox / 尺寸 | 形态 | 出处 |
|---|---|---|---|---|
| 收藏 | `CoUI/icon/FavoriteIcon` 🆕 | `0 0 12 13` / 12×13 | 实心五角星（14 处） | `CoUI/icon/FavoriteIcon.tsx:4-17` |
| 点赞/喜欢 | `CoUI/icon/LikeIcon`（带 `active` prop） | active `0.5 0.5 16 16` 16×16 / 非 active `0 0 24 24` 24×24 | 拇指，active 实心 / 非 active 描边（10 处） | `CoUI/icon/LikeIcon.tsx:6-43` |

**已废弃 / 重复 / 专用版：**

| 文件 | 状态 | 说明 | 出处 |
|---|---|---|---|
| `HeartIcon` | 边界（2 处） | 心形「喜欢」变体，使用面窄 | `CoUI/icon/HeartIcon.tsx` |
| `Icon/LikeIcon`（named `LikeIcon`） | ⚠️ Icon 目录重复版 | 20×20 描边拇指 `strokeWidth=1.49954`，CoUI 版优先 | `Icon/LikeIcon.tsx:3-36` |
| `FavModelIcon` / `FavModelFillIcon` | 专用（各 3 处） | 模型收藏专用，非通用收藏星 | `CoUI/icon/FavModel*.tsx` |

> `LikeIcon`（CoUI）是**有状态图标**：必传 `active: boolean`，active 时渲染 16×16 实心拇指，否则 24×24 描边拇指——是同图标内置选中/未选中两套 SVG 的范例。

#### 搜索

推荐 `CoUI/icon/SearchIcon`（13 处，CoUI 唯一）。

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <g id="Icon/search"><path id="Vector" d="M18.031 16.617L22.314 20.899 ..." fill="currentColor" /></g>
</svg>
```

唯一 canonical，无废弃版。

#### 设置 / 齿轮

推荐 `CoUI/icon/SettingIcon`（10 处）。

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M10.2774 19.8299C11.4131 ... 10.6877 9.85292 11.3301 9.60012 12 9.60012Z" fill="currentColor" /> <!-- 齿轮+中心圆 -->
</svg>
```

| 文件 | 状态 | 说明 |
|---|---|---|
| `SettingIcon` 🆕 | ✅ canonical（10 处） | 齿轮+中心圆 24×24 |
| `SettingIconLarge` | 备选（4 处） | 同款大尺寸变体 |
| `HexSettingIcon` / `ShineSetting*` | 边界 | 六边形 / 闪光设置专用 |

#### 对勾 / 选中

按形态分两条线：

```svg
<!-- CheckIcon 纯勾（无圆框）：实心 -->
<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
  <g id="Icon/duicuo"><path id="Vector" d="M7.99988 12.4122L16.666 4L18 5.2939L7.99988 15L2 9.17652L3.3331 7.88262L7.99988 12.4122Z" fill="currentColor" /></g>
</svg>
```

| 语义 | 推荐 | viewBox / 尺寸 | 形态 | 出处 |
|---|---|---|---|---|
| 纯对勾（无圆） | `CheckIcon` 🆕（按使用量 canonical，8 处） | `0 0 20 20` / 20×20 | 实心勾 `id=Icon/duicuo` | `CoUI/icon/CheckIcon.tsx:5-20` |
| 圆框内选中 | `CheckCircleIcon`（11 处，最高频 check） | `0 0 24 24` / **写 16×16** | 实心圆框+勾 | `CoUI/icon/CheckCircleIcon.tsx:5-18` |

**已废弃 / 描边新版：**

| 文件 | 状态 | 说明 | 出处 |
|---|---|---|---|
| `CheckV3Icon` | ⚠️ 最新描边款（2026-05-19）但仅 1 处用 | **`0 0 12 11` 12×11，`stroke=currentColor` `strokeWidth=1.8` `strokeLinecap/join=round`**（描边勾）——「改动最新 ≠ 采纳广」典型，描边场景备选 | `CoUI/icon/CheckV3Icon.tsx:3-21` |
| `CheckV2Icon` | 边界（2 处） | 12×12 实心勾 `fillRule=evenodd` | `CoUI/icon/CheckV2Icon.tsx:3-21` |
| `CheckCircleSolidIcon` / `CheckDoubleIcon` / `CheckSquareIcon` | 专用变体 | 实心圆 / 双勾（已读）/ 方框勾，各自场景 | `CoUI/icon/Check*.tsx` |

> ⚠️ `CheckCircleIcon` 是规格陷阱：`viewBox="0 0 24 24"` 但 `width="16" height="16"`（`CoUI/icon/CheckCircleIcon.tsx:7-9`）——默认渲染 16px，但坐标系是 24。调用处覆盖尺寸时按 viewBox 24 推比例。

#### 锁 / 会员锁

推荐基础锁 `CoUI/icon/LockIcon`（17 处）。

```svg
<svg width="16" height="16" viewBox="0 0 16 16" fill="none">
  <path fillRule="evenodd" clipRule="evenodd" d="M4.17713 4.52664C4.17713 ... 7.41313 11.1975 7.92063 11.4008Z" fill="currentColor" /> <!-- 挂锁带钥匙孔 -->
</svg>
```

| 语义 | 文件 | 状态 | 说明 |
|---|---|---|---|
| 基础锁 | `LockIcon` 🆕 | ✅ canonical（17 处） | 挂锁带钥匙孔 16×16 `fillRule=evenodd` |
| 会员/付费锁 | `ShineLockIcon` / `ShineLockFillIcon` | 专用 | 闪光会员锁 24×24（`ShineLockIcon.tsx:3-12`） |
| 会员/付费锁 | `StarLockIcon` / `StarLockFillIcon` | 专用 | 星标付费锁 |
| 场景锁 | `ProfileCardLockIcon` / `...FillIcon`、`ThumbUpLockIcon` / `...FillIcon` | 专用 | 个人页卡 / 点赞锁，各场景 |
| VIP 徽标 | `VIPIcon` | 专用 | VIP 徽标（非锁） |

> 语义铁律：基础锁（`LockIcon`）用于普通「锁定/不可用」；`ShineLock` / `StarLock` / `ProfileCardLock` / `ThumbUpLock` 是会员付费专用锁，**不是 LockIcon 的版本**，按场景选。

#### 发送

推荐 `CoUI/icon/SendIcon`（6 处，CoUI 唯一）。注意是 **named export**（`export function SendIcon`）。

```svg
<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
  <path d="M2.5 10.8327H7.5V9.16602H2.5V1.53769 ..." fill="currentColor" /> <!-- 纸飞机/箭头 -->
</svg>
```

唯一 canonical，无废弃版。

### 6.4 图标使用规范

#### 尺寸档位

图标 SVG 上写死的 width/height 只是默认/Figma 导出值，**统一由调用处覆盖**。常见档位：

| 档位 | 用法 | 典型图标 |
|---|---|---|
| 12px | 行内小标记（分享、收藏星、三角） | `ShareIcon` 12×12、`FavoriteIcon` 12×13、`TriangleIcon` 12×12 |
| 16px | 表单/列表行内操作 | `PlusIcon`、`CopyIcon`、`DeleteIcon`、`LockIcon`、`ThreeDotsVerticalIcon`（均 16×16） |
| 20px | 中号交互按钮 | `CheckIcon`、`SendIcon`、`Chevron*`（20×20） |
| 24px | 头部/导航/弹窗级 | `CloseIcon`(25)、`EditIcon`、`SearchIcon`、`SettingIcon`、`ChevronUpIcon`、`MenuLineIcon`、`BackArrowIcon`（24 量级） |
| 大号（≥31） | 大入口/空态 | `CirclePlusIcon` 79×80、`Icon/AddIcon` 31×31 |

落地写法：调用处用 `className="size-4"`（16px）/ `size-5`（20px）/ `size-6`（24px）等控制；**不要在 icon 组件内把业务尺寸写死**（与 Figma MCP 规范一致）。

#### 着色（🌗 暗/亮）

- 全库图标用 `fill="currentColor"` / `stroke="currentColor"`，**颜色 = CSS `color`**，所以暗/亮切换不改图标本身，只改调用处的 `text-*` token。
- 暗/亮分支统一走 Tailwind `dark:`（`darkMode: 'class'`），如 `className="text-light3-primary dark:text-dark3-primary"`。
- ⚠️ 项目 Tailwind 自定义色阶覆盖了默认色，用色前查 `tailwind.config.js`。
- ⚠️ 例外：`SmallCloseIcon` 写死 `#707070`、`BackArrowIcon` 自带 drop-shadow filter、`CloseIcon withShadow` 自带投影——这些不纯跟 currentColor，慎用并注意暗/亮下投影对比。
- 多 class 拼接用 `twJoin` / `twMerge`，不用 `classNames()`。

#### 与文字对齐

- 图标与文字并排时，容器用 `inline-flex items-center gap-*`，图标尺寸取相邻文字行高的同档位（16px 文字配 16px 图标）。
- 带状态的图标（`LikeIcon` 的 `active`、`CloseIcon` 的 `withShadow`）通过 prop 切换内部 SVG，不靠调用处换组件。

#### 复用优先 / 不新增重复

- 新功能先 grep 图标主库，有语义相近的优先复用（Figma MCP rule 硬性要求）。
- 同功能在主库与独立目录都有时（Close/Copy/Like/Add），**一律用主库版**（使用量更高、维护集中）；唯一例外 `BackArrowIcon` 只在独立目录，无主库对应。
- 尺寸/颜色/暗亮差异由 `className` / token 解决，**className 控制尺寸不写死、不为差异复制新 SVG**。

#### 版本说明（🆕 汇总）

- 删除：`DeleteIcon`（实心）为 canonical；`TrashOutlineIcon` 是描边款（非旧版，要描边才用）；`RemoveIcon` 语义=移除（别替代删除）。
- 对勾：按使用量 `CheckIcon`（纯勾）/ `CheckCircleIcon`（圆框）为 canonical；`CheckV3Icon`（2026-05-19 最新描边款）仅 1 处用，描边场景备选——「改动新 ≠ 采纳广」。
- 关闭：`CoUI/icon/CloseIcon`（92 处）为 canonical，`Icon/CloseIcon`（24 处）是重复旧版。
- 添加：`PlusIcon`（16×16）canonical；`CirclePlusIcon`（79×80）大入口专用；`Icon/AddIcon`（31×31）旧版。
- 菜单/更多：`ThreeDotsVerticalIcon`=更多（竖三点）；`MenuLineIcon`=列表菜单；`MenuIcon` 源码实为三竖排圆点（recon「汉堡」标签误判）。
- 收藏 vs 点赞：`FavoriteIcon`（星）=收藏；`LikeIcon`（拇指）=点赞，不可互换。
- 锁：`LockIcon`=基础锁；`ShineLock`/`StarLock`/`ProfileCardLock`/`ThumbUpLock`=会员付费专用锁。
