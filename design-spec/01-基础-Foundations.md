# 基础 Foundations

> 通用设计系统基础层 · 可被任意项目复用的视觉令牌与主题机制
> 三条轴: 🌗 暗/亮（含双值成对）· 📱 PC/移动 · 🆕 取最新版为准
> 数值/hex/px/类名照抄不臆造；onlychat 真实值作为「📍示例」溯源到 `相对路径:行号`

## 概览

这是设计系统的最底层：颜色、字体、间距、动画、断点、主题机制都从这里取值，是「令牌 → 组件 → 页面」金字塔的地基。本文档把可复用的**令牌表**与**机制说明**抽象成通用条目，每条配上 onlychat 的真实实现作为「📍示例」参考。

通用令牌通常分布在三类来源，各司其职：

| 来源类型 | 角色 | 📍示例 |
|---|---|---|
| Tailwind 配置 (`theme.extend`) | 主令牌库：调色板、字体族、断点、不透明度、渐变、动画/keyframes | `tailwind.config.js:14-754` |
| 全局 CSS (`globals.css`) | CSS 变量、滚动条、复用按钮类、若干 keyframes、container query | `src/app/globals.css:1-815` |
| 运动令牌模块 (`motion.ts`) | duration / easing 单一真相源（供 framer-motion 读） | `src/styles/motion.ts:82-137` |

> ⚠️ 通用原则：只有在 `theme.extend` 里建了 token 的维度才有「改一处传播全站」。未覆盖的维度（如下文字号/间距/圆角）用框架默认刻度，组件里的 arbitrary 值（`text-[14px]` / `w-[78px]`）是字面值不是 token。
>
> ⚠️ 反直觉点（取色铁律）：颜色 token 名带主题前缀（`black`/`white`/`gray`）时，**实际值与名字未必对应**——📍示例 `black.4 = rgba(0,0,0,0.04)` 是透明蒙层、`white.6 = rgba(255,255,255,0.30)` 是暗色边框。取色一律以真实 hex/rgba 为准，不要凭名字猜。

---

## 1. 调色板 Palette / 语义令牌

### 1.1 ⭐ 主题语义令牌（亮/暗成对，写双值首选）

设计系统的核心是一对**主题角色色板**：亮色一套、暗色一套，命名成对（`light*-role` / `dark*-role`）。组件写 `text-light3-primary dark:text-dark3-primary` 即自动跟随主题。这是写颜色的**第一优先级**，其次才用通用色阶（§1.2），只有拿不到 token 的场景（如 Mantine `sx`）才写裸 hex。

📍示例: onlychat `light3-*` / `dark3-*` (`tailwind.config.js:107-124`)

| 角色 | 🌗 light (`light3-*`) | 🌗 dark (`dark3-*`) | 说明 |
|---|---|---|---|
| 背景 `bg` | `#FCFCFC` | `#202020` | 页面底色 |
| 主题色 `primary` | `#923EFC`（紫） | `#F75ECC`（粉） | ⚠️ **不同色相**，非同色调明暗 |
| 主题色悬浮 `primaryHover` | `#590FB6` | `#B60083` | |
| 次级色 `secondary` | `#62D5FF`（蓝） | `#A8EF30`（绿） | 旧次级色 |
| 深次级色 `darkSecondary` | `#009EC0` | `#518200` | |
| 新次级色 `newSecondary` 🆕 | `#3BA6F3` | `#7976FF`（紫） | UI 走查替换次级色，新代码用这个 |
| 小弹窗底 `smallPopupBg` | `rgb(255,255,255)` | `#2F3034` | |

> 🆕 **新旧令牌迁移**：`secondary` 正被 `newSecondary` 替代（注释「走查替换次级色」），新代码次级色优先用 `newSecondary`。
> ⚠️ **换色相提示**：主题切换时 primary 从紫变粉，不是简单明暗——做对比度/视觉评估时注意。

### 1.2 通用色阶 black / white / gray（裸类，亮暗共用一池，靠 `dark:` 选档）

这些不是「亮一套暗一套」，而是一个色阶池；组件在亮色选浅档、暗色选深档（或反过来）。同类合并成表：

📍示例: onlychat (`tailwind.config.js:23-52`)

| 黑阶 | 值 | 语义 | 白阶 | 值 | 语义 | 灰阶 | 值 | 语义 |
|---|---|---|---|---|---|---|---|---|
| `black` | `#000000` | 纯黑 | `white` | `#FFFFFF` | 纯白 | `gray.0` | `#3F3F3F` | 加深灰 |
| `black.1` | `#1F1E1E` | 不纯黑 | `white.1` | `#F5F5F5` | 不纯白 | `gray.1` | `#707070` | 深灰（按钮底常用） |
| `black.2` | `#363234` | 碳色 | `white.2` | `#FCFCFC` | Light 背景 | `gray.2` | `#9E9E9E` | 中灰 |
| `black.3` | `#202020` | Dark 背景 | `white.3` | `#F7F7FA` | — | `gray.3` | `#C7C7C7` | 浅灰（文字常用） |
| `black.4` | `rgba(0,0,0,0.04)` | 透明蒙层 | `white.4` | `rgba(255,255,255,0.04)` | 透明背景 | `gray.4` | `#E9E9E9` | — |
| `black.5` | `#2E182E` | — | `white.5` | `#F2F2F2` | — | `gray.5` | `#E2E2E2` | — |
| `black.6` | `#202126` | 暗弹窗底 | `white.6` | `rgba(255,255,255,0.30)` | 暗色边框 | | | |
| `black.7` | `#343843` | — | | | | | | |
| `black.8` | `#151315` | — | | | | | | |
| `black.9` | `#292929` | — | | | | | | |
| `black.10` | `rgba(0,0,0,0.30)` | 亮色边框 | | | | | | |

> **对称半透明约定**（藏在色阶里，通用复用价值高）：
> - 边框：亮 `black.10 rgba(0,0,0,0.30)` ↔ 暗 `white.6 rgba(255,255,255,0.30)`
> - 透明蒙层：亮 `black.4 rgba(0,0,0,0.04)` ↔ 暗 `white.4 rgba(255,255,255,0.04)`

### 1.3 功能/品牌色板

绿/粉/紫/蓝/黄/红六组品牌与功能色，节选有通用语义的档位：

📍示例: onlychat (`tailwind.config.js:53-106`)

| green 绿 | 值 | pink 粉 | 值 | purple 紫 | 值 |
|---|---|---|---|---|---|
| `green.1` | `#A8EF30`（暗次级） | `pink.1` | `#F75ECC`（暗主题） | `purple.1` | `#923EFC`（亮主题） |
| `green.2` | `#518200`（暗深次级） | `pink.hover` | `#CF2EA2` | `purple.4` | `#7976FF`（重点紫） |
| `green.3` | `#00FFD1`（重点绿） | `pink.3` | `#FFD5F1` | `purple.6` | `#B376FF` |
| `green.6` | `#15D1BB`（新辅助提示） | `pink.4` | `#FF8ADC` | `purple.hover` | `#611BBC` |

| blue 蓝 | 值 | yellow 黄 | 值 | red 红 | 值 |
|---|---|---|---|---|---|
| `blue.1` | `#62D5FF`（亮次级） | `yellow.1` | `#F7FF88`（重点黄） | `red.1` | `#FF2619`（旧警告） |
| `blue.2` | `#009EC0`（亮深次级） | `yellow.2` | `#FFA133`（评分星黄） | `red.3` 🆕 | `#E4221A`（新警告，走查替换） |
| `blue.4` | `#4DAAFF`（链接蓝） | `yellow.6` | `#E9C897`（暗作者黄） | `red.6` | `#FF4444`（强提示） |
| `blue.10` | `#0773B0`（亮作者蓝） | | | `red.2` | `#800000`（拉黑） |

> 🆕 **警告色迁移**：旧 `red.1 #FF2619` → 新 `red.3 #E4221A`。新组件用 `red.3`。

### 1.4 与主题无关的固定档位色（示例：订阅等级）

部分语义色不随暗亮变（产品里的会员/等级标识）。这是通用「状态恒定色」模式的示例：纯色用 token，多色用渐变。

📍示例: onlychat `subscription.*` (`tailwind.config.js:125-131`, 渐变 `:307-310`)

| token | 值 | 类型 |
|---|---|---|
| `subscription.free` | `#A5E2F8` | 纯色 |
| `subscription.standard` | `#00E492` | 纯色 |
| `subscription.premium` | `#C49FF2` | 纯色 |
| `subscription.deluxe` / `.luxe` | `#FFD100`（两者同值） | 纯色 |
| `subscription-elite` | `linear-gradient(90deg, #C4C4C4 0%, #8F8A92 25%, #423F43 100%)` | 银灰渐变 |
| `subscription-imperial` | `linear-gradient(90deg, #FFD680 0%, #CEA665 50%, #9B7E4E 100%)` | 金渐变 |

### 1.5 CSS 根变量与渐变文字工具

| 项 | 值 | 用途 | 📍示例 |
|---|---|---|---|
| `--foreground-rgb` | `0, 0, 0` | body 文字色 `rgb(var(--foreground-rgb))` | `globals.css:5, 19-21` |
| `text-fill-transparent` | `transparent` | 配 `bg-clip-text` 做渐变文字 | `tailwind.config.js:368-370` |

> 通用机制：渐变文字 = `background: <gradient>` + `bg-clip-text` + `text-transparent`（filltransparent token）。

---

## 2. 字体排版 Typography

### 2.1 字体族 fontFamily

字体族以 `var(--font-*)` CSS 变量为首选（构建期注入），后跟系统降级栈。通用做法：每个族一个语义名（正文/标题/装饰/多语言）。

📍示例: onlychat (`tailwind.config.js:139-154`)

| token | 主字体 | 用途 |
|---|---|---|
| `font-roboto` | `var(--font-roboto)` | 默认正文 |
| `font-metropolis` | `Metropolis`（静态名） | 品牌标题 |
| `font-crimson` | `var(--font-crimson_text)` + serif | 衬线标题 |
| `font-ja` | `var(--font-mPlus1)` + Hiragino/Meiryo | 日语 |
| `font-exo2` / `font-montserrat` / `font-poppins` / `font-poetsenOne` | 各自变量/静态名 | 装饰/活动 |

> 共用降级栈尾部：`ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"`（serif 族走 serif 降级栈）。

### 2.2 字号 / 字重 / 行高（默认刻度）

通用建议：字号/字重/行高用框架默认刻度即可，除非有强设计需求才覆盖。下表为 Tailwind v3 默认（📍示例项目未在 config 覆盖，直接依赖此基线）：

| 类名 | font-size | line-height | | 字重 | 值 |
|---|---|---|---|---|---|
| `text-xs` | 12px | 16px | | `font-normal` | 400 |
| `text-sm` | 14px | 20px | | `font-medium` | 500 |
| `text-base` | 16px | 24px | | `font-semibold` | 600 |
| `text-lg` | 18px | 28px | | `font-bold` | 700 |
| `text-xl` | 20px | 28px | | | |
| `text-2xl` | 24px | 32px | | | |

> ⚠️ 未建 token 时「改一处传播全站」不成立；`text-[14px]` 是硬编码字面值。

---

## 3. 间距 / 圆角 / 阴影 / 模糊

| 维度 | 通用做法 | 📍示例值 | 📍来源 |
|---|---|---|---|
| 间距 spacing | 用框架默认刻度（每单位 0.25rem=4px：`1`=4px / `2`=8px / `3`=12px / `4`=16px / `6`=24px / `8`=32px） | 未覆盖，arbitrary `w-[78px]` 为字面值 | Tailwind v3 默认 |
| 圆角 borderRadius | 用默认（`rounded` 4px / `-md` 6px / `-lg` 8px / `-xl` 12px / `-2xl` 16px / `-full` 9999px） | 未覆盖；富文本图固定 `border-radius: 14px` | `globals.css:564` |
| 阴影 boxShadow | 用默认 `shadow` / `shadow-md` | 未覆盖 | Tailwind v3 默认 |
| 模糊 blur（自定义补档） | 框架默认无 xs 档时补一档 | `blur-xs = 2px` | `tailwind.config.js:136-138` |
| 超大宽度 maxWidth（自定义补档） | 按需补大尺寸 | `max-w-8xl = 1524px` | `tailwind.config.js:133-135` |

---

## 4. 断点 Screens

📱 通用：断点是 PC/移动判定的唯一真相。可全覆盖框架默认，但**自定义后数值可能与框架默认不同**，用前必查。

📍示例: onlychat 全自定义断点集 (`tailwind.config.js:371-379`)

| token | min-width | 典型用途 | 是否同框架默认 |
|---|---|---|---|
| `xs` | `420px` | 超小屏（小手机） | 自定义 |
| `sm` | `640px` | 手机 | 同默认 |
| `md` | `768px` | 平板 / PC 起点（常作 PC/移动分界） | 同默认 |
| `lg` | `1024px` | 小桌面 | 同默认 |
| `sxl` | `1280px` | 中桌面（项目专属档） | ⚠️ 自定义档 |
| `xl` | `1536px` | 大桌面 | ⚠️ ≠ 默认 1280 |
| `2xl` | `1920px` | 超宽屏 | ⚠️ ≠ 默认 1536 |

> 📱 **PC/移动判定**：最常用 `sm:` / `md:` 作分界。`sxl` 是项目专属，`xl`/`2xl` 数值与 Tailwind 默认不同，迁移到别的项目时需重新核对。

---

## 5. 不透明度 / 模糊 / 渐变

### 5.1 不透明度 Opacity（补默认缺档）

通用做法：补框架默认缺失的细档（如 2/4/6/95）。

📍示例: onlychat (`tailwind.config.js:380-394`) — 补档 `opacity-2=0.02` / `-4=0.04` / `-6=0.06` / `-95=0.95`，其余 10~90 每 10 一档。

### 5.2 渐变 BackgroundImage（🌗 双值成对铁律）

**通用机制**：主题双值渐变靠**名字后缀** `-light` / `-dark`（少数 `-black-1`）区分，消费端必须**成对引用** `bg-xxx-light dark:bg-xxx-dark`，不能只写一边。这是「Figma token 名形如 `白→黑` 时」落地的标准做法。

基础渐变工具（与主题无关，通用复用）：

📍示例: onlychat (`tailwind.config.js:155-158`)

| token | 值 |
|---|---|
| `bg-gradient-radial` | `radial-gradient(var(--tw-gradient-stops))` |
| `bg-gradient-conic` | `conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))` |
| `bg-gradient-315deg` | `linear-gradient(315deg, var(--tw-gradient-stops))` |
| `bg-gradient-45deg` | `linear-gradient(45deg, var(--tw-gradient-stops))` |

主题双值渐变范式（📍示例选取代表性几对，展示「同视觉两后缀」模式，完整清单见原 config）：

📍示例: onlychat (`tailwind.config.js:163-366`)

| 用途 | 🌗 light | 🌗 dark |
|---|---|---|
| 主题渐变背景 | `gradient-primary-light` `linear-gradient(180deg, rgba(243,243,255) 0%, rgba(198,153,255) 90%)` | `gradient-primary-dark` `linear-gradient(180deg, rgba(20,20,20) 0%, rgba(171,57,139) 90%)` |
| 卡片底部渐隐 | `character-card-light`（→`#F3F3FF`） | `character-card-dark`（→`#363234`） |
| 滚动遮罩 | `pricing-scrollbar-bg-light`（→`#FCFCFC`） | `pricing-scrollbar-bg-dark`（→`#202020`） |
| 弹层背景 | `gradient-popover-light` `linear-gradient(180deg, #FFF 0%, #B1E8FF 100%)` | `gradient-popover-dark` `linear-gradient(180deg, #FFF 0%, #E1FFAF 100%)` |

> 🆕 **版本并存示例**：渐变会出现 V1/V2 并存（如活动标签底 `event-tag-bg` V1 中间 stop `#923EFC` ↔ `event-tag-bg-v2` V2 中间 stop `#B376FF`，`globals.css:661`）。新组件取最新版。
> 渐变文字工具同理成对：`imperial-text-gradient` / `elite-text-gradient` 及各自 `-mobile` 变体（📱PC/移动两套，`globals.css:741-755`）。

---

## 6. 运动令牌 Motion (duration / easing)

**通用机制**：运动设计应有**单一真相源**（一个 `motion.ts` 常量文件），定义按「视觉目的」而非「元素大小」选择的 duration 与 easing。framer-motion 场景直接读常量（改一处传播全站）；CSS/Tailwind 场景写等值 preset 类（字面值，改 token 需 grep）。

### 6.1 DURATION（按视觉目的选）

📍示例: onlychat (`motion.ts:82-87`)

| token | 值 | 对应 Tailwind 类 | 用途 |
|---|---|---|---|
| `fast` | 100ms | `duration-100` | hover / press / focus，要「瞬时」感 |
| `base` | 200ms | `duration-200` | 多数 enter / exit / 状态切换 |
| `slow` | 300ms | `duration-300` | 较大空间移动、多步过渡 |
| `deliberate` | 500ms | `duration-500` | 注意、庆祝、揭示时刻 |

LOOP_DURATION（长循环动画，与过渡令牌刻意分开，`motion.ts:91-95`）：`short` 1000ms（spin）/ `medium` 1500ms（pulse）/ `long` 2000ms。

### 6.2 EASING（方向性曲线，传达「能量从哪来到哪去」）

📍示例: onlychat (`motion.ts:102-121`)

| token | cubic-bezier | 对应 Tailwind 类 | 用途 |
|---|---|---|---|
| `decelerate` | `(0, 0, 0.2, 1)` | `ease-out` | **进场默认**（能量到达、就位） |
| `accelerate` | `(0.4, 0, 1, 1)` | `ease-in` | **退场默认**（能量聚集、离开） |
| `standard` | `(0.4, 0, 0.2, 1)` | `ease-in-out` | 屏内开始结束（状态变化、数值微调） |
| `emphasized` | `(0.2, 0, 0, 1)` | 无 preset，需 `ease-[cubic-bezier(0.2,0,0,1)]` | 高重要度时刻 |
| `linear` | `linear` | `ease-linear` | 持续旋转、shake 类注意动效 |

> 速查：进场 `duration-200 ease-out`（base+decelerate）/ 退场 `duration-200 ease-in`（base+accelerate）/ hover `duration-100`（fast）。
> a11y 约定：装饰性循环动画必须配 `motion-reduce:animate-none`，循环频率 <3Hz（WCAG 2.3.1）。

---

## 7. z-index / 层级

> 通用建议：z-index 应建立分层令牌（base / dropdown / sticky / modal / toast 等递增档），避免散落魔数。
>
> 📍示例: onlychat 当前未在 `theme.extend` 建 z-index token，组件用 Tailwind 默认 `z-10/20/30/40/50` 及 arbitrary `z-[N]` 字面值。共用组件需同时顾 🌗 暗/亮 + 📱 PC/移动两轴时，z-index 属于「移动布局」轴的一部分（见 §8 双轴铁律）。

---

## 8. 主题与暗黑机制 Theming

主题系统是设计系统的底座，决定「同一组件在暗/亮两种环境下分别长什么样」。通常由三层拼起来，各管一摊：

1. **主题状态层（Provider）** — 管「现在是 dark / light / system」状态，结果写成 `<html class="dark">`。
2. **Tailwind `dark:` 变体层（主力）** — 真正决定组件颜色：亮色写裸类，暗色写 `dark:` 前缀类。
3. **UI 库主题层（次要）** — 第三方组件库（如 Mantine）的 colorScheme 跟随主题状态同步。

> 核心心智模型：**改一个组件的主题表现 = 在亮色裸类旁补一条 `dark:` 类**。绝大多数情况不碰 Provider 也不碰 UI 库。

### 8.1 `darkMode: 'class'` —— 开关是 `<html class="dark">`

**通用机制**：暗色走 `.dark` 父类驱动（而非系统 `prefers-color-scheme`），所有暗亮差异写成 `dark:` 前缀。配置 `darkMode: 'class'`。

📍示例: onlychat (`tailwind.config.js:6`)。系统偏好媒体查询块整段注释禁用（`globals.css:11-17`）——暗色**只走 `.dark` class，不走系统偏好**。

主题状态机要点（通用 Provider 行为，📍示例 `src/components/Themes/index.tsx`）：

| 配置项 | 行为 | 📍示例 |
|---|---|---|
| `attribute` | `"class"`（暗色时 `<html class="... dark">`） | `layout.tsx:419` |
| `defaultTheme` | 读持久化值，无则 `'system'` | `layout.tsx:420-423` |
| 持久化 | cookie `color-schema`，30 天 | `Themes/index.tsx:39, 92` |
| `themes` | `['system', 'light', 'dark']` | `:34` |
| 选中后三件事 | ① resolve（system 读 `matchMedia`）② 改 `<html>` class ③ 同步 `html.style.colorScheme` 让原生控件跟随 | `:51-85` |
| 首屏防闪烁 | 挂载前内联 `<script>` 先打 class + `suppressHydrationWarning` | `:171-273`, `layout.tsx:349` |
| 跨标签同步 | 监听 `storage` 事件 | `:117-131` |

> 配套：移动端地址栏底色随主题改 `<meta name="theme-color">`（🌗 light `#FCFCFC` / dark `#202020`，正是 `light3.bg`/`dark3.bg`），📍示例 `ThemeColorController/index.tsx:18-19`。

### 8.2 语义令牌写双值（light/dark 成对）

见 §1.1 主题语义令牌表。**写颜色优先级**：① `light3-*` / `dark3-*` 语义令牌 → ② 通用色阶（§1.2） → ③ 只有拿不到 token 的场景（如 UI 库 `sx` 回调）才写裸 hex，且 hex 必须与令牌对齐。

典型写法：`text-light3-primary dark:text-dark3-primary`（亮紫 / 暗粉）。

### 8.3 🌗 双值成对铁律

**写了亮色裸类就必须补对应 `dark:` 类；双值渐变必须 `-light` + `-dark` 两条都引，不能只写一边。** 这是整个主题系统最硬的约束。

- 颜色：`bg-white dark:bg-black-6` / `text-black dark:text-gray-3`
- 渐变：`bg-xxx-light dark:bg-xxx-dark`（见 §5.2）
- Figma 只读到单 mode 时要标注、不臆造另一侧。

📍示例 — 标准弹窗双值 (`Modal.tsx:55-59`)：

| 部位 | 🌗 light | 🌗 dark |
|---|---|---|
| 容器底 | `bg-white` | `dark:bg-black-6`（`#202126`） |
| 标题 | `text-black` | `dark:text-white` |
| 正文 | `text-black` | `dark:text-gray-3`（`#C7C7C7`） |
| 遮罩 | `bg-black/50`（暗亮共用） | 同左 |

> 读法：暗色只覆盖需要变的（底色/字色），圆角/padding/遮罩暗亮共用。📱 `p-5 sm:p-10`（移动 20px → ≥640px 40px）即两轴并存示例。

### 8.4 三条消费路径（按场景分工）

| 场景 | 用哪套机制 | 📍示例 |
|---|---|---|
| 普通业务/UI 组件 / div / span | Tailwind `dark:`（主力） | `Modal.tsx`、`ThemeSelect.tsx:68` |
| 直接渲染第三方 UI 库组件（Mantine `Menu`/`Switch`/`Select`） | UI 库 `colorScheme === 'dark'` 三元写 `sx`/`styles`（拿不到 token，写裸 hex） | `ThemeDropdown.tsx:127-135` |
| 全局元素（滚动条、`<body>`、伪元素） | 全局 CSS 里 `.dark` 选择器 | `globals.css:61-66` |
| 浏览器原生控件底色 | `html.style.colorScheme`（Provider 自动同步） | `Themes/index.tsx:75-82` |

> **UI 库与 Tailwind 关系**：两套共享同一「主题状态真值」，但各管各的组件。UI 库 `colorScheme` 单向同步自主题 Provider 的 `resolvedTheme`，兜底默认 `'dark'`。主题状态统一用自研 `useTheme()`，不直接用 UI 库的 colorScheme hook（那是下游）。📍示例 `MantineThemeProvider.tsx:18, 26, 42`。

### 8.5 🌗 主题换色相（非简单明暗）

**关键约定**：`primary` 在亮暗是**不同色相**（📍示例亮紫 `#923EFC` / 暗粉 `#F75ECC`），主题切换会换色相而非同色调明暗。做对比度/视觉评估、配渐变时都要按各自色相单独验。

### 8.6 📱 共用组件两轴铁律

共用组件要**同时顾两条轴**：🌗 暗/亮（颜色/背景）+ 📱 PC/移动（布局/z-index/尺寸）。

📍示例: `redeemBtn`/`purchaseBtn` 复用按钮（`globals.css:787-815`）即两轴并存：📱 移动 32px×78px / PC（`sm:`）35px×85px；🌗 disabled 亮 `black/0.04` 底 + `gray-2` 字 / 暗 `white/0.04` 底 + `gray-1` 字。

---

## 附录 · 通用令牌速查

| 想要的效果 | 通用取法 | 📍示例值 |
|---|---|---|
| 主题色文字/按钮 | `text-{light}-primary dark:text-{dark}-primary` | 亮紫 `#923EFC` / 暗粉 `#F75ECC` |
| 次级强调色 | newSecondary（走查后） | 亮 `#3BA6F3` / 暗 `#7976FF` |
| 页面背景 | 语义 bg 令牌 | 亮 `#FCFCFC` / 暗 `#202020` |
| 边框（半透明对称） | 亮 black.10 / 暗 white.6 | `rgba(0,0,0,.30)` / `rgba(255,255,255,.30)` |
| 透明蒙层（半透明对称） | 亮 black.4 / 暗 white.4 | `rgba(0,0,0,.04)` / `rgba(255,255,255,.04)` |
| PC/移动分界 | `md:`(768) 或 `sm:`(640) | — |
| 进场 / 退场动画 | base + decelerate / accelerate | `duration-200 ease-out` / `ease-in` |
| hover 反馈 | fast + brightness | `duration-100 hover:brightness-110` |
