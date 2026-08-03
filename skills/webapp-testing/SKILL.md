---
name: webapp-testing
description: 用 headless Playwright 驱动本地 webapp 做功能验证——自动拉起 dev server、等端口就绪、跑脚本化交互、抓截图和 console 日志，全程不抢窗口焦点。触发词："跑一下看看能不能用"、"headless 验一下"、"用 playwright 测"、"起服务跑个脚本验"、"抓下 console 报错"、"点一下这个按钮看看"、"webapp testing"。不用于：需要真实登录态/Chrome 扩展的走查（归 visual-qa agent，先 `claude --chrome`）、PC×mobile 四象限 UI 截图验收（归 visual-qa）、写进仓库的正式测试用例（归 onlychat-test-engineer）、纯静态代码审查（归 code-review）。
---

# Webapp Testing（headless）

写一次性 Playwright 脚本验本地 webapp 的真实行为。**headless 跑，不抢窗口焦点**——这是它相对「起 dev app 手动点」的核心价值。

来源：官方 `anthropics/skills` 的 webapp-testing，示例已从 Python 改写为 Node（本机 Playwright 装在 Node 侧）。

## 何时使用

- 想确认一个改动**运行时真的跑得通**，但不值得写进仓库的正式测试
- 要抓 console 报错 / 网络失败 / 渲染断裂，而不是看代码猜
- 要点几下、填个表单、看跳转对不对

**不该用它的时候**：需要登录态或 Chrome 扩展 → `visual-qa` agent（记得先 `claude --chrome`）；要 PC/mobile × dark/light 四象限截图验收 → 也是 `visual-qa`；要沉淀成回归用例 → `onlychat-test-engineer`。

## 步骤 1 — 确认 Playwright 可用

```bash
ls node_modules/.bin/playwright   # 项目内已装？
```

本机现状：**全局没装 playwright，只有 `~/Desktop/cmm/onlychat` 装了**（含已下载的 chromium）。所以：

- 在 onlychat 里 → 直接用
- 在别的项目里临时验一下 → 借 onlychat 的，脚本里写绝对路径导入：
  ```js
  import { chromium } from '/Users/lengmo/Desktop/cmm/onlychat/node_modules/playwright/index.mjs';
  ```
- 要反复用 → 在该项目 `pnpm add -D playwright` + `npx playwright install chromium`（浏览器约 150MB，先问用户）

## 步骤 2 — 决定要不要托管 server

```
静态 HTML？
 ├─ 是 → 直接读 HTML 找选择器，用 file:// 打开
 └─ 否 → server 已经在跑？
     ├─ 在跑 → 直接连，跳到步骤 3
     └─ 没跑 → 用 scripts/with_server.py 托管（它负责起服务、等端口、跑完清理）
```

```bash
python3 ~/.claude/skills/webapp-testing/scripts/with_server.py \
  --server "pnpm dev" --port 3000 -- node my-check.mjs
```

多个服务（前端 + 后端）就重复 `--server` / `--port`，数量必须配对。先跑 `--help` 看用法，**别读它的源码**——当黑盒用，省上下文。

## 步骤 3 — 侦察，再动手

动态页面**必须先等 JS 执行完再找元素**，这是最高频的翻车点。

```js
import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
page.on('console', m => console.log(`[console.${m.type()}]`, m.text()));
page.on('pageerror', e => console.log('[pageerror]', e.message));

await page.goto('http://localhost:3000');
await page.waitForLoadState('networkidle');   // 关键：等 JS 跑完

await page.screenshot({ path: '<scratchpad>/inspect.png', fullPage: true });
console.log(await page.locator('button').allTextContents());

await browser.close();
```

拿到选择器后再写真正的交互动作。优先用 `getByRole` / `getByText` 这类语义选择器，别写脆的 CSS 层级链。

## 输出约束

- 截图一律写到 scratchpad 目录，别污染项目仓
- 报结论必须带证据：贴 console 原文 / 截图路径 / 断言结果，不要只说「验过了没问题」
- 脚本是一次性的，验完就删；要留下来的写成正式测试用例交给 `onlychat-test-engineer`

## 反模式

1. **没等 `networkidle` 就抓 DOM**——动态页面必然抓空或抓到骨架屏，然后误判成 bug。
2. **`headless: false`**——会抢窗口焦点，等于回到手动点的老问题。要看真实渲染找 `visual-qa`。
3. **读 `with_server.py` 源码**——它是黑盒工具，`--help` 就够，读源码纯浪费上下文。
4. **拿它当登录态走查**——headless 是干净上下文，没有你浏览器里的 cookie。要登录态就换 `visual-qa`。
5. **脚本堆断言堆成测试套件**——那是正式测试的活，这里只做一次性验证。
