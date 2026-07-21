# OnlyChat Tailwind Token ↔ Figma 值 对照

来源：`~/Desktop/cmm/onlychat/tailwind.config.js`。

## 主题色（theme-switching）

| Figma 变量 | light 值 | dark 值 | Tailwind |
|---|---|---|---|
| `主题色/主题色 ↔︎` | `#923EFC` | `#F75ECC` | `light3-primary` / `dark3-primary` |
| `主题色/主题色↔︎ 20%` | `#923EFC33` | `#F75ECC33` | `light3-primary/20` / `dark3-primary/20` |
| `主题色/主题色 ↔︎ 70%` | `#923EFCB2` | `#F75ECCB2` | `light3-primary/70` / `dark3-primary/70` |
| `主题色/主题色悬浮 ↔︎` | `#590FB6` | `#B60083` | `light3-primaryHover` / `dark3-primaryHover` |
| `次级色 ↔︎` | `#62D5FF` | `#A8EF30` | `light3-secondary` / `dark3-secondary` |
| `新次级色 ↔︎` | `#3BA6F3` | `#7976FF` | `light3-newSecondary` / `dark3-newSecondary` |
| `场景色/背景色 ↔︎` | `#FCFCFC` | `#202020` | `light3-bg` / `dark3-bg`（或 `white-2` / `black-3`） |

## 中性色（theme-switching 简化）

| Figma 变量 | light 值 | dark 值 | Tailwind |
|---|---|---|---|
| `中性色/白 → 黑` | `#000000` | `#FFFFFF` | `text-black` / `dark:text-white` |
| `中性色/白 → 黑 4%` | `rgba(0,0,0,0.04)` | `rgba(255,255,255,0.04)` | `bg-black-4` / `dark:bg-white-4` |
| `中性色/白 → 黑 10%` | `rgba(0,0,0,0.10)` | `rgba(255,255,255,0.10)` | `bg-black/10` / `dark:bg-white/10` |
| `中性色/白 → 黑 30%` | `rgba(0,0,0,0.30)` | `rgba(255,255,255,0.30)` | `bg-black-10` / `dark:bg-white-6`（注意命名反常） |
| `中性色/中灰 → 深灰` | `#707070` | `#9E9E9E` | `text-gray-1` / `dark:text-gray-2` |
| `中性色/深灰 → 浅灰` | `#5D5D5D` | `#C7C7C7` | 需查项目具体 token |

## 固定色（两模式共用）

品牌三色作为 gradient stops 时使用，**不随主题切换**：

| Figma 变量 | 值 | Tailwind / 用法 |
|---|---|---|
| `Dark_Primary Colors/D_Primary 500` | `#F75ECC` | arbitrary `[#F75ECC]`（与 `dark3-primary` 同值，但语义是固定色） |
| `Light_Primary Colors/L_Primary 500` | `#923EFC` | arbitrary `[#923EFC]`（同上） |
| `Light_Secondary Colors/L_Secondary 500` | `#3BA6F3` | arbitrary `[#3BA6F3]` |

典型用法（event tag 三色渐变）：
```
bg-[linear-gradient(94deg,#F75ECC33_-5%,#923EFC33_50%,#3BA6F333_105%)]
```

## Alpha → hex 对照

写 arbitrary 值时用：

| Tailwind alpha | hex 后缀 | 0-255 |
|---|---|---|
| `/5` | `0D` | 13 |
| `/10` | `1A` | 26 |
| `/20` | `33` | 51 |
| `/30` | `4D` | 77 |
| `/40` | `66` | 102 |
| `/50` | `80` | 128 |
| `/60` | `99` | 153 |
| `/70` | `B2` | 178 |
| `/80` | `CC` | 204 |
| `/90` | `E6` | 230 |

## 注意

- `white-4` / `black-4` 命名误导：都是 `rgba(*,0.04)` 透明蒙层，不是 4 号色
- `gray-1 (#707070)` 在 light mode 是次要文字，在 dark mode 反而是按钮底色——**跨模式复用时查 tailwind.config.js 注释**
- 品牌三色（`#F75ECC` / `#923EFC` / `#3BA6F3`）作为渐变 stops 时 MCP 返回是 `D_Primary / L_Primary / L_Secondary`，名字像是 dark/light 但实际是**固定色**
