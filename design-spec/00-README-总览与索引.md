# 设计规范 · 总览与索引

> 一套**通用设计系统规范**。分类按产品无关的设计系统概念组织（基础 / 组件 / 布局模式 / 决策），
> 具体规格全部从 onlychat（world-book 分支）真实代码逐文件抽取，onlychat 的组件/数值/`file:line` 作为「📍示例 / 参考实现」保留——换技术栈时把示例替换成本系统的等价物即可。
> 轴：🌗 暗/亮主题（含双值） · 📱 PC/移动 · 🆕 取最新版为准。所有数值/类名/DOM 可溯源到 `相对路径:行号`。

## 概览

它解决三个问题：

1. **取值不靠猜** —— 色/字/距/圆角/断点全是真实 hex/px；自定义 token 都标了它映射的真值。
2. **版本不踩坑** —— 同一功能存在 V1/V2/V3 多版本时，正文只写「当前实际在用」的那版，旧版仅一句话标注；判定依据是真实 import 计数（见下方版本权威表）。
3. **选型有依据** —— 每类组件给「何时用 / 何时别用」，跨组件的选型集中在决策指南。

## 文件索引（5 份）

| 文件 | 一句话 |
|---|---|
| [01-基础-Foundations.md](./01-基础-Foundations.md) | 底层令牌库 + 主题机制：调色板/语义令牌、字体排版、间距圆角阴影、断点、不透明度/模糊/渐变、运动令牌、z-index、暗黑模式（`darkMode:'class'`、`light3/dark3` 语义令牌、双值成对铁律）。**先看这份。** |
| [02-组件-Components.md](./02-组件-Components.md) | 通用组件库，6 个子节：① 控件 ② 浮层 ③ 卡片 ④ 标签徽章指示器 ⑤ 反馈动效空态 ⑥ 图标。每个组件含视觉规格/DOM/状态/暗亮/版本/何时用。 |
| [03-布局模式-Patterns.md](./03-布局模式-Patterns.md) | 布局与交互模式：页面骨架（顶/侧/底栏）、响应式容器与断点、安全区/sticky、`.pc/.mobile` 端拆分约定、编辑器双栏布局、选择/管理模式、标签页与同级切换。 |
| [04-决策指南-Decision-Guide.md](./04-决策指南-Decision-Guide.md) | 跨组件选型速查：场景→选哪个→为什么→✅该用/❌别用。卡片选型、浮层判定流程、按钮变体、tag·badge·红点·星级、骨架vs spinner、Toast vs Banner、表单控件、移动vs PC 与拆分判据。 |

> 「02-组件」是一份大文件（~2300 行），开头有子节目录，按 `§ 一~六` 跳转。

**推荐阅读顺序**：先 01（令牌+主题）建立底座 → 按需查 02/03 → 落地时查 04 决策指南；写新组件前先扫 02§六（图标复用）与对应条目的「版本说明」。

---

## 全局约定

### 三条轴

| 轴 | 含义 | 落地机制 |
|---|---|---|
| 🌗 **暗/亮主题** | 同一组件在 dark/light 两种环境分别长什么样 | `darkMode:'class'`。亮色写裸类（`bg-white text-black`），暗色写 `dark:` 前缀类。开关 = `<html class="dark">`，**不走系统偏好**。 |
| 📱 **PC/移动** | 同一组件在桌面/手机的布局或交互差异 | 多数靠断点（`sm/md/lg`）。仅当 PC 与移动**交互模型本质不同**才做 `.pc.tsx/.mobile.tsx` 文件级拆分（见 03§5）。 |
| 🆕 **取最新版为准** | 同功能多版本时只认当前在用那版 | 判定依据是真实 import 计数（见下表）。**反直觉**：不是所有 V2/V3 都比 V1 新且主流；机械「取最新」会写错。 |

### 版本权威表（精简版，判定「最新/在用」用这张）

> ⚠️ 标「反直觉」的，机械取最新会写错。完整证据见各组件「版本说明」。

| 功能族 | ✅ canonical（在用） | 弃用/次要 | 备注 |
|---|---|---|---|
| 基础弹窗 Modal | `Modal`（**V1**，274 import） | `ModalV2`（1 import） | ⚠️ 反直觉：V1 才是底座 |
| 开关 Switch | `Switch2`（纯 div 自绘） | `Switch`（V1, Mantine） | |
| Tooltip | `TooltipV2` | `Tooltip`（V1，未弃用并存） | 两版并存 |
| Dropdown | `DropdownV2` | `Dropdown`（V1，0 业务引用） | |
| 多步引导弹窗 | `StepModalV2` | `StepModal`（V1） | 业务 `StepModalV3` 非升级链 |
| Form Radio | `Radio`（**V1**，16 处主流） | `RadioV3`（胶囊）/`RadioV2` | ⚠️ 反直觉：V3 最新但未取代 V1 |
| 通用 Tag 渲染 | `TagV2`（revamp 主流） | `Tag`（V1，A/B 对照组） | A/B 双轨并存，非替代 |
| 卡片 Tag 集合 | `TagBoxV2`（8 >> 1） | `TagBox`（V1） | |
| 移动底部横幅 | `MobileBottomBannerV3` | `MobileBottomBanner`（0 引用） | |
| 登录弹层 | `LoginPopoverNew` | `LoginPopover/`（0 引用） | |

> **命名陷阱**：grep `*ModalV2` 会大量命中业务弹窗（`ChangeModelModalV2` 等），它们与基础组件升级链无关。判定基础组件版本必须按精确 import 路径计数。
> **A/B 双轨**：首页改版 `TagV2/TagBoxV2/...` 来自灰度实验，V1 零改动 → 双轨并存不是替代。

### `.pc`/`.mobile` 拆分约定（详见 03§5）

- **拆**：PC 与移动**交互模型本质不同**（如 PC 双栏 + 拖拽 vs 移动单列整页跳转）。
- **不拆**：仅 light/dark、间距、字号差异 → 单文件内 `dark:`/`md:` 断点解决。
- **双值成对铁律**：写了亮色裸类就要补对应 `dark:` 类；渐变背景 `-light` + `-dark` 两条都引。

---

## 令牌速查（一页）

> 浓缩自 01-基础，全部真实值。自定义色/断点整段覆盖了 Tailwind 默认。

### 色 · 主题语义令牌（写双值优先用这对）

| 角色 | 🌗 light (`light3-*`) | 🌗 dark (`dark3-*`) |
|---|---|---|
| 背景 `bg` | `#FCFCFC` | `#202020` |
| 主题色 `primary` | `#923EFC`（紫） | `#F75ECC`（粉） |
| 主题色悬浮 `primaryHover` | `#590FB6` | `#B60083` |
| 次级色 `secondary` | `#62D5FF`（蓝） | `#A8EF30`（绿） |
| 新次级 `newSecondary`（新代码优先） | `#3BA6F3` | `#7976FF` |

> 记忆点：暗主色=粉 `#F75ECC`，亮主色=紫 `#923EFC`——主题切换换**色相**不是简单明暗。标准写法 `text-light3-primary dark:text-dark3-primary`。

### 色 · 常用通用色阶

| token | 真实值 | 用途 |
|---|---|---|
| `black-2` / `black-6` / `black-9` | `#363234` / `#202126` / `#292929` | 卡片面 / Modal 暗底 / 卡片暗底 |
| `black-4` / `white-4` | `rgba(0,0,0,.04)` / `rgba(255,255,255,.04)` | 透明蒙层（亮/暗） |
| `black-10` / `white-6` | `rgba(0,0,0,.30)` / `rgba(255,255,255,.30)` | 边框（亮/暗对称半透明） |
| `gray-1/2/3` | `#707070` / `#9E9E9E` / `#C7C7C7` | 深/中/浅灰 |
| `purple-2/3/4` | `#D7D6FF` / `#F3F3FF` / `#7976FF` | 卡亮边 / 卡亮底 / 重点紫 |
| `red-3` | `#E4221A` | 警告色（替旧 `red-1`） |
| `blue-4` / `yellow-2` / `green-3` | `#4DAAFF` / `#FFA133` / `#00FFD1` | 链接 / 评分黄 / 重点绿 |

### 字号 / 间距 / 圆角（Tailwind v3 默认刻度，config 未覆盖）

- 字号：`xs`12 / `sm`14 / `base`16 / `lg`18 / `xl`20 / `2xl`24（px）；字重 400/500/600/700。
- 间距：每单位 4px（`p-2`=8 / `p-4`=16 / `p-6`=24）。
- 圆角：`md`6 / `lg`8 / `xl`12 / `2xl`16 / `full`9999；常见 arbitrary `rounded-[14px]`（卡/条）、`rounded-[25px]`（胶囊钮）。
- ⚠️ 组件里 `text-[14px]`/`w-[78px]` 是**硬编码字面值不是 token**。

### 断点（全自定义，覆盖 Tailwind 默认）

| token | min-width | | token | min-width |
|---|---|---|---|---|
| `xs` | 420px | | `sxl` | 1280px（项目专属，双侧栏分界） |
| `sm` | 640px | | `xl` | 1536px |
| `md` | 768px（常作 PC/移动分界） | | `2xl` | 1920px |
| `lg` | 1024px | | | |

### 运动令牌（framer-motion 单一真相源；CSS 写等值 preset 类）

| DURATION | 值 | Tailwind | 用途 |
|---|---|---|---|
| `fast` | 100ms | `duration-100` | hover/press/focus |
| `base` | 200ms | `duration-200` | 多数 enter/exit/状态切换 |
| `slow` | 300ms | `duration-300` | 较大空间移动 |
| `deliberate` | 500ms | `duration-500` | 注意/庆祝/揭示 |

进场 `ease-out` / 退场 `ease-in` / 屏内 `ease-in-out` / 旋转 `linear`。装饰循环动效配 `motion-reduce:animate-none`。

### z-index 速记

| 值 | 用途 |
|---|---|
| `useZIndex`（≥100 自增） | Modal/Drawer/Popover/ImagePreview——后开的比先开的高 1 |
| `z-[9999]` | Toast / 全屏 Loading（盖一切） |
| `z-50/51` / `z-40` / `z-10` | 桌面左侧栏 / 顶栏 / 浮层内部小元素 |

> ⚠️ 浮层用 `useZIndex` 是 inline style（优先级高），在 className 上写 `z-*` 无效；调层级靠打开顺序。

---

## 目录树

```
design-spec/
├── 00-README-总览与索引.md       ← 本文件
├── 01-基础-Foundations.md         设计令牌 + 主题暗黑机制
├── 02-组件-Components.md          控件/浮层/卡片/标签徽章/反馈动效/图标（6 子节）
├── 03-布局模式-Patterns.md        页面骨架/响应式/端拆分/编辑器/选择模式
└── 04-决策指南-Decision-Guide.md  跨组件选型速查（什么情况用什么）
```
