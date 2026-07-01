---
name: chrome-extension-on-demand
description: Chrome 扩展集成默认关闭，只在用户明确要求浏览器操作时才用，绝不主动调用
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f1980b1a-2d70-4bfd-a827-95c8bbaa3fd6
---

用户曾因 CC 过度主动调用 Chrome 扩展（claude-in-chrome）而手动禁用了扩展（2026-06 之前）。2026-06-11 已把 `~/.claude.json` 的 `claudeInChromeDefaultEnabled` 设为 false：平时会话不接入浏览器工具，需要时用户启动 `claude --chrome` 按需开启。

**Why:** 用户明确表示"不希望在我不想调用的时候 cc 自动去调用"。

**How to apply:** 即使某会话里浏览器工具可见（用户开了 --chrome），也只在用户明确要求浏览器操作时才调用；不要为"顺手验证一下"之类的理由主动开网页。相关：[[visual-qa]] 走查类任务属于用户明确要求，正常使用。
