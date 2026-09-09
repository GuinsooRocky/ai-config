---
name: dont-resize-browser-window
description: 浏览器走查时绝不改用户的窗口尺寸（resize_window / 全屏），用他当前窗口就行
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7e07a871-ed5a-4480-9c22-db44091cf96d
  modified: 2026-08-26T09:08:58.699Z
---

用 claude-in-chrome 走查时**不要调用 `resize_window`**，也不要把窗口弄成全屏。
用户当时正用着那个窗口，尺寸被改掉是打扰。

**Why**：2026-08-26 付费图走查，我为了「标准 1440×960 视口」顺手 resize 了一次，
用户当场说「你能别动浏览器全屏吗」。走查要的是看渲染对不对，不是像素级基准——
用户当前窗口完全够用；真需要特定断点时先问，不要默认自己动。

**How to apply**：
- 默认不传 `resize_window`，直接在现有窗口截图
- 视口太小导致 `zoom` 报「Region exceeds viewport boundaries」→ 先 `screenshot`
  看真实尺寸再框区域，不要靠 resize 绕开
- 确实要验响应式断点（PC/mobile 双轨）→ 先说一句「要改窗口宽度到 X，可以吗」再动

见 [[feedback_chrome_extension_on_demand]]。
