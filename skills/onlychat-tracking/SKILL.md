---
name: onlychat-tracking
description: OnlyChat 埋点（tracking / 神策 cus.* 事件）的接线 + 核对 + 验证全流程。触发词：接埋点、核对埋点、埋点对照 PM 清单、验证埋点、埋点 verify、tracking guard、tc/tv/tl、生成埋点核对 HTML。从零接线与核对已有埋点都覆盖；含静态 audit 自测 + 运行时验证手册 + 踩坑库 + 可勾选核对 HTML 生成。
---

# OnlyChat 埋点 skill

把「接埋点 / 核对埋点 / 验证埋点」收成一条流程。**重心是核对 + 验证**（接线是基础，验证才是痛点）。配套 i18n skill 用同一范式（SKILL 主干 + references 按需 + script 自测）。

## 何时使用

- 接新功能的埋点（从零）／核对 PM 清单 vs 已实现埋点／逐条验证某事件有没有真上报
- 用户说：接埋点、核对埋点、埋点对照清单、验证埋点、tracking guard、生成埋点核对 HTML、tc/tv/tl 怎么选
- 看到 PM 给的「埋点需求清单」（列：流程/模块/事件/元素/参数/版本/负责人/产品）

## 心智锚（先读）

1. **PM 清单 = 唯一真相源**。所有动作都围绕「清单 ↔ 代码」对齐。
2. **「必须手动验」比你以为的小得多** —— 这次落地的 bug（缺 source / 多余键 / 取值错）**全是静态能抓的**，没用上神策。先跑静态 `audit` 挡掉 80%，运行时只验「会不会真触发 + 动态算的值」。
3. **神策 `show_log` 太吵别用**；运行时验证用 console snippet（见 references/verify-gotchas.md）。
4. **只动自己的代码**：事件归你不代表代码归你（`git blame` 别人写的 call-site 不碰）。

## 入口分流（一个 skill 全包）

```
PM 清单（事件/元素/参数 必给；负责人/版本/产品 可选）
        │  有没有现成埋点？
        ├─ 没有  → 从零接线（§4）→ 验证（§6）→ HTML（§7）
        ├─ 全做  → 双向核对（§5）→ 验证 → HTML
        └─ 部分  → 核对 + 补缺 → 验证 → HTML
```

## §1 归属两层（没负责人列也能跑）

- **事件归属**：有负责人列 → 按列筛；**没有** → 「用户贴给你的行 = 你的范围」（PM 通常只贴自己那段）。
- **代码归属**：对每个事件 `git blame` registry / call-site → **别人写的代码一行不碰，即使事件归你**（典型：个人页 CreateWorld 事件归你、但代码是别人写的 → 只标注，不改）。用 `tracking_tool.py owner-split` 一键分组。

## §2 接线机制选型（从零接埋点）

| 触发形态 | 用 | 上报 |
|---|---|---|
| 固定 DOM 点击（按钮/卡片） | `{...tc('key')}` 展开到元素 | `cus.click_*` |
| 页面块 mount 曝光 | `{...tv('key')}` / `useTv` | `cus.view_*` |
| NiceModal 弹窗曝光 / 命令式 / 系统 / 失焦 / 带计算参数 | `tl('key', { params })` | 弹窗报 `cus.view_*`、其余按语义 |
| 同一按钮按状态分流（如 isPublished） | `tl` 带参数 | `cus.click_*` |

- registry 三表登记：`src/tracking/registry/{click,view,logic}.ts`，kebab key → `cus.{click|view|logic}_*` 三前缀对齐。
- 机制细节、捕获阶段委派、新旧 `@/tracking` vs `@/lib/track`、guard、神策 transport → **references/mechanism.md**。

## §3 参数规范（硬约束）

- **no PII**（email/phone/用户输入/token 不上报）
- **no 翻译文本**（`t('...')` 进参数会按 locale 炸统计 → 用稳定英文 enum / type code）
- 参数名**语义化**（不要 `A`/`B`/`type` 等不透明 token）
- **能前端算的别等后端**：file_size_kb（File.size）/ note_count（数响应条目）/ duration（前端掐表）都前端算，**别误标"待后端"**
- 链路参数（source / category）走「**组件 tracking-agnostic + 父级补业务参数**」：子组件只发回调，父级补 source/category

## §4 从零接线流程

1. `owner-split` 确认范围 → 2. 逐条按 §2 选机制接线 + registry 登记 + §3 参数 → 3. 跑 §6 验证 → 4. §8 四道闸。

## §5 双向核对（已有埋点）

PM 清单 ↔ 代码，三类问题：
- **缺口**：PM 有、registry/call-site 没有 → 补
- **多余**：registry/call-site 有、PM 没有 → 删（注意跨作者的别动）
- **不符**：事件名 / 参数 / 取值 与 PM 不一致 → 改

**先把每行 PM 描述映射到 `cus.*` 事件名**（人工，registry 注释里常有 A1/B2 编号可对），再交给 `audit` 做机械核对。

## §6 验证两层 ⭐

**① 静态自测（`tracking_tool.py audit`，无浏览器，挡 80%）**
- 缺口（cus.* 不在 registry / 无 call-site）
- 多余（registry 有该前缀事件、不在你的清单）
- **参数缺失**（call 的 params ⊄ PM 要求 → 抓"缺 source"类）
- **字面值不符**（代码里 `source:'home'` ≠ PM 的 `home_plus_dialog`）
- prefix 错位（tc→click / tv→view / tl→logic）、PII、翻译文本

**② 运行时（只剩"会不会真触发 + 动态值"，才需要人）**
- **弃神策 show_log**，用 console snippet 包 `sensors.track` 只打 `cus.*`（见 verify-gotchas.md）
- 配 HTML 勾选清单，点一个勾一个
- 要更自动 → Playwright 拦神策 endpoint 断言（重，关键事件，走 onlychat-test-engineer）

**验证踩坑（别处查不到，必读 references/verify-gotchas.md）**：tc 捕获阶段先于跳转触发、文件框暂停 console、跳转要 Preserve log、相似名事件区分、只在特定条件触发的事件、造测试数据。

## §7 生成核对 HTML（固化模板）

复刻 **references/checklist-template.html**（1:1 PM 行序镜像 + 勾选持久化 + 复制按钮 + 白天夜间 + 可达性徽章 + hover 可达路径气泡）。生成步骤见 **references/html-checklist.md**；气泡数据用 `tracking_tool.py tips` 抓真实 call site。

- 列：勾选 / ref / 模块 / 事件（可达性徽章 + hover 气泡）/ 代码事件名（📋 复制）/ 参数 / 状态 / 备注
- 状态四档：✅符合 / 🔧待改代码 / ⚠️待PM拍值 / 🚫不做
- 可达性徽章：浅(灰) / 弹窗(灰) / **深(红)** / 系统(灰)，文字非 emoji
- 气泡按深度：浅给位置 · 弹窗给触发路径 · 深给多步+前置 · 系统说明无 UI

## §8 四道闸（出活前必过）

1. `tsc --noEmit` 0 错
2. `tracking_tool.py orphan <prefix>` 无未用 registry key
3. `tracking_tool.py audit` 静态零残留（缺口/多余/参数/取值/prefix/PII 全清）
4. 核对 HTML 无 ❌（运行时已验）

## 脚本速查

```bash
python3 scripts/tracking_tool.py owner-split <prefix> <email>   # git blame 归属分组
python3 scripts/tracking_tool.py orphan <prefix>                # registry 无 call-site 的 key
python3 scripts/tracking_tool.py audit <input.tsv> <prefix>     # 静态自测：缺口/多余/参数/取值/prefix/PII
python3 scripts/tracking_tool.py tips <prefix>                  # 抓 call site → 气泡 TIPS 骨架
```
（在 OnlyChat 仓库根目录跑；默认 registry 路径 src/tracking/registry/）

## 执行步骤（核对流程，从零接线见 §4）

- **步骤 1 归属**：`owner-split` 分组，**必须**先确认范围；别人代码一行不碰。
- **步骤 2 映射**：把每行 PM 描述 → `cus.*` 事件名（人工，registry 注释有编号可对）。
- **步骤 3 静态自测**：`audit <清单.tsv> <prefix>`，缺口/多余/参数/取值/prefix/PII **必须**零残留（§6 层 1）。
- **步骤 4 运行时验**：console snippet（**不要**用神策 show_log）逐条点、逐条勾（§6 层 2）。
- **步骤 5 出 HTML**：复刻 `checklist-template.html` 换数据（§7），交付给人逐条对。
- **步骤 6 四道闸**：§8 全过才算完。

## 示例输出

`audit` 命中（静态层抓出的真实问题形态）：
```
== 埋点静态自测（前缀 worldcard-，清单 86 条）==
  ✗ 缺参数：cus.click_nav_create_world 少 ['source']（call 现有 无）
  ✗ 取值不符：cus.view_worldcard_create_card 的 source 代码='home' ≠ PM='home_plus_dialog'
  ✗ 多余·清单无（实现有 call-site）：cus.logic_worldcard_name_blur
共 3 处。修完再跑；运行时再验「会不会真触发 + 动态值」。
```

HTML 一行 + 对应气泡 TIPS（核对清单产物片段）：
```html
<tr><td class="ref">A12</td><td>命名弹窗</td><td>关闭弹窗（外部/esc/X）</td>
    <td><code>cus.logic_worldcard_name_dialog_dismiss</code></td><td class="p">—</td>
    <td><span class="badge b-ok">✅</span></td><td class="note">本轮新补</td></tr>
```
```js
'cus.logic_worldcard_name_dialog_dismiss':['弹','命名弹窗 · 关闭','弹窗内按 X/Esc/点外部','NameYourWorldDialog.tsx:48'],
```

## 反模式

1. **一上来就开浏览器肉眼验** → 先跑静态 `audit`，能抓的别用人
2. **用神策 show_log 翻面板** → 太吵，用 console snippet
3. **改到别人写的 call-site 代码** → 事件归你 ≠ 代码归你，blame 后只标注
4. **参数塞 `t('...')` / PII** → 炸统计 / 合规风险
5. **把"待后端"当默认** → file_size/note_count/duration 前端就能算
6. **HTML 不按 PM 行序** → 必须 1:1 镜像，方便逐条对
