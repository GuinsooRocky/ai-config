---
name: feedback_browser_preview_reload_in_place
description: 刷新本地 HTML 预览用原地 reload，绝不 close+reopen（会把页面甩回顶部、丢用户滚动位置）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 08b0014e-83ca-4c70-8131-9d4f4c6ad80a
---

帮用户预览本地 HTML（如 talk 的 `OUTLINE-三支柱-v2.html`）时，改完文件刷新浏览器一律**原地 reload 当前标签页**，绝不 close 标签再 `open` 重开。

**Why:** 用户在逐行改稿、滚动位置就是他的工作焦点；close+reopen 每次都把页面甩回顶部，他得反复滚回去，极其打断。

**How to apply:** Chrome AppleScript 遍历 windows/tabs 命中目标 URL，对该 tab 调 `reload t`（不是 close+open）。若原地 reload 仍跳顶，再升级成 JS 记录 `scrollY` → reload → 恢复。只刷目标那个标签，别动用户其它标签（如 v.qq.com）。
