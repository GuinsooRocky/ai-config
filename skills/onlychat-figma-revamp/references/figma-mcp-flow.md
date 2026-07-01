# Figma MCP 工具返回值解读

## 三个工具必须并行调

```
mcp__figma-desktop__get_design_context(nodeId)
mcp__figma-desktop__get_variable_defs(nodeId)
mcp__figma-desktop__get_screenshot(nodeId)
```

用 Agent tool 并行发 3 个调用块，不要串行。

## `get_design_context`

返回一段 React + Tailwind 参考代码。**不要照抄**，因为：

1. 代码里的 class name 是原始 Figma Tailwind，不匹配项目 token（比如 `bg-[var(--主题色\/主题色-↔︎,#f75ecc)]`）
2. `var(--xxx, #fallback)` 的 fallback **通常只是默认模式的值**，对另一个模式错

**正确读法**：
- 看布局结构（嵌套层次、flex/grid、gap、padding）
- 看哪些 class 是 arbitrary（`[linear-gradient(...)]`、`[calc(...)]`），这些是必须原样搬的「具体值」
- 看 data-node-id，方便你回 Figma 定位

## `get_variable_defs` ← **核心**

返回这个节点用到的所有变量的**当前值**（键 = 变量名，值 = 具体 hex/rgba）。

例：
```json
{
  "中性色/中灰 → 深灰": "#707070",
  "主题色/主题色 ↔︎": "#923efc",
  "主题色/主题色↔︎ 20%": "#923efc33",
  "Dark_Primary Colors/D_Primary 500": "#f75ecc",
  "Light_Primary Colors/L_Primary 500": "#923efc",
  "Light_Secondary Colors/L_Secondary 500": "#3ba6f3"
}
```

**读法**：
- 变量名带 `↔︎` / `→` = 主题切换 token，这个返回的是**当前节点渲染时的值**（Figma 上看的是哪个模式就返哪个模式的值）
- 变量名带明确前缀 `Dark_/Light_` = 固定色 token（不随主题切换），两个模式同值
- 变量名带百分比 = 同色 + alpha 变体，数值就是 hex8（`#RRGGBBAA`）

## `get_screenshot`

返回节点渲染图。**写完代码必须对着截图肉眼比对**。

## 双模式必走流程

如果只拿到一个模式的节点 ID：

1. 停下来让用户给另一个模式的 node-id
2. 两个 node-id 都抓 `get_variable_defs`
3. 对照找差异：
   ```
   light: 主题色 = #923efc
   dark : 主题色 = #f75ecc
   → 项目 token：light3-primary / dark3-primary
   ```
4. 把差异整理成「light 默认 + `dark:` 变体」的 class

如果 Figma 只有一个模式的设计稿：
- 先**明确问用户**另一个模式是否需要还原
- 如果只要改一个模式，另一个保持现有实现即可，**不要凭空补**

## 节点 ID 提取

URL 形如 `...node-id=28583-84059...`，横杠格式传给工具是 `28583-84059`（工具接受 `a-b` 或 `a:b`）。

## 常见异常

### variable_defs 返回空
- 节点不是 component instance，没挂变量。用 `get_design_context` 的 arbitrary 值兜
- 或换更内层的节点 ID 再试

### design_context 返回巨大
- 节点层级太深（包含整页）。换更靠叶子的 node-id
- 实在不行加 `forceCode: true` 强制返代码（慎用，上下文开销大）

### screenshot 返回低分辨率
- 服务端限制，肉眼比对够用，精确色值以 variable_defs 为准

## MCP 不返回的东西

- **交互/动画/过渡时长**：Figma 里有 prototype 也不通过 MCP 透出。交互时长默认 `duration-200`（跟项目现有 pattern 一致）
- **hover/focus/active 态**：只返 default。多个态要分别抓对应 variant 节点（Figma 里一般叫 `tag/hover`、`tag/active`）
- **响应式断点**：MCP 返的是当前 artboard 宽度。移动端/桌面端要分别抓
