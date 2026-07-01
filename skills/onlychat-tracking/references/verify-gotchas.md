# 埋点验证手册 + 踩坑（skill 的灵魂）

> 静态能抓的先用 `tracking_tool.py audit`（无浏览器，挡 80%）。本文是**运行时**那一小半 + 别处查不到的坑。

## 验证两层

### 层 1：静态自测（先跑，无浏览器）
`python3 scripts/tracking_tool.py audit <清单.tsv> <prefix>` —— 抓：缺口 / 多余 / 参数缺失 / 字面值不符 / prefix 错位 / PII / 翻译文本。**这次落地的 bug 全在这层能抓**（缺 source、多余键、取值错）。

### 层 2：运行时（只剩"会不会真触发 + 动态算的值"）
**别开神策 `show_log`（太吵）。** 浏览器 Console 贴这个 snippet，只打 `cus.*`：
```js
const o = sensors.track.bind(sensors);
sensors.track = (e, p) => { e.startsWith('cus.') && console.log('%c'+e, 'color:#3fb950;font-weight:bold', p); return o(e, p); };
```
配核对 HTML 的勾选清单，点一个事件勾一个。要更自动 → Playwright 拦神策 endpoint（`sensor.web.pkbsvc.com/sensors/ue`）断言 event+params（重，关键事件，走 onlychat-test-engineer）。

## 踩坑（验证时最容易误判）

### 1. tc 捕获阶段 → 「点了好像没报」是假象
tc 是 document **捕获阶段**委派，点击瞬间先于 onClick 发出。若 onClick 里跳转，事件**已发**，只是：
- **原生文件选择框 / OS 弹窗会暂停页面 console 刷新** → 日志被压到弹窗关闭后才刷出来（看着像"选完文件才报"）。验证：点完直接**取消文件框**，日志照样在。
- **跳转事件**：DevTools Console 勾 **Preserve log**，否则跳转清空看不到。

### 2. 相似名事件别认错
- `cus.click_worldcard_view_guide`（创建方式选择页 View Guide） vs `cus.click_worldcard_editor_view_guide`（编辑器顶栏 View Guide）→ 过滤词用全名，别只 `view_guide`。
- 弹窗里的 CreateWorld 卡片点击事件 ≠ 下一页"选择创建方式"的按钮事件。
- 同一事件多入口（add-note 有 +号/StarterCard/横幅）靠 `entry` 参数区分，不是不同事件。

### 3. 只在特定条件触发的事件，平时验不出来
- 「文件过大 toast」只在 **.json 且 >5MB** 才弹；其它导入失败走**弹窗**不走 toast。验不出先确认是不是没满足条件。
- 二确弹窗多有前置（如 Public→Private 二确：**仅"已发布且被人用过"的卡 + 改 Public→Private**才弹）。
- 系统事件（上传成功/失败、保存成功/失败、发布成功、解析成功）**无 UI**，靠流程跑到那一步才发，别在页面上找元素。

### 4. 参数前端算 vs 后端 —— 别误判"待后端"
file_size_kb / note_count / duration 这类**前端就能算**（File.size、数响应条目、掐表）。看到"导入解析成功"别因为"后端 RPC"就标"待后端"——参数和后端没关系，只有"事件会不会触发"取决于后端是否实装。

## 造测试数据

- **>5MB 文件**（验文件过大 toast）：
  ```bash
  head -c 6000000 /dev/zero | tr '\0' a > ~/Desktop/big.json
  ```
- **撑大已有合法 mock 到 >5MB**（保留原内容，加可删 padding 字段）：
  ```bash
  node -e "const fs=require('fs');const p='x.json';const d=JSON.parse(fs.readFileSync(p,'utf8'));d._pad='a'.repeat(6*1024*1024);fs.writeFileSync(p,JSON.stringify(d,null,2));"
  ```
- 大小校验在 `JSON.parse` **之前**，所以 padding 内容随便、文件 >5MB 即可触发。

## 验证产物

逐条验完 → 在核对 HTML 勾掉 → 进度条到 N/N → 把仍 ❌（运行时确认没触发/参数错）的列成待办。静态 audit 0 残留 + HTML 全勾 = 这个范围的埋点验证完成。
