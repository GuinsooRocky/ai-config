---
name: chrome-extension-on-demand
description: Chrome 扩展集成默认关闭，只在用户明确要求浏览器操作时才用，绝不主动调用
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f1980b1a-2d70-4bfd-a827-95c8bbaa3fd6
  modified: 2026-07-26T06:05:01.673Z
---

用户曾因 CC 过度主动调用 Chrome 扩展（claude-in-chrome）而手动禁用了扩展（2026-06 之前）。2026-06-11 已把 `~/.claude.json` 的 `claudeInChromeDefaultEnabled` 设为 false：平时会话不接入浏览器工具，需要时用户启动 `claude --chrome` 按需开启。

**Why:** 用户明确表示"不希望在我不想调用的时候 cc 自动去调用"。

**How to apply:** 即使某会话里浏览器工具可见（用户开了 --chrome），也只在用户明确要求浏览器操作时才调用；不要为"顺手验证一下"之类的理由主动开网页。相关：走查类任务（visual-qa）属于用户明确要求，正常使用。

**⚠ 别拿全局默认推断当前会话（2026-07-26 栽过）**：`claudeInChromeDefaultEnabled: false` 只是默认值，用户经常带 `--chrome` 起会话。要判断本次会话能不能走查，**跑一次 `list_connected_browsers` 探一下**（这是回答用户提问，不算"主动调浏览器"），别直接对用户说"这个会话没开、你得另起一个"——说错了会白白把活推回给用户。同理别据此劝退 visual-qa 派工。

**⚠ 「要运行时证据」时别追问用户，先自己复现（2026-08-19 栽过）**：多 tab bug 查到「需要看那条请求返回什么」时，我列了两个分支让用户去开 Network 面板看——用户回「你可以自己开两个 chrome 再本地 3000 自己复现啊」。本地 dev 在跑 + 浏览器工具能用 = **自己去复现**，这是查因不是「顺手验证」，不在本条禁止范围内。判据：我正准备向用户要一条只有跑一遍才能得到的事实（响应体 / 错误码 / 是不是真卡住）→ 先探浏览器工具，能跑就自己跑。

**浏览器截图不是渲染真相（2026-08-08）**：懒加载图片常已 `complete && naturalWidth>0`，截图里却仍是灰块——抓帧没等到合成。别拿截图当「图裂了」的证据，要判就查 DOM（`naturalWidth`/`complete` 计数）或直接 HEAD 图片 URL；曾为此追了五六轮假警报。
