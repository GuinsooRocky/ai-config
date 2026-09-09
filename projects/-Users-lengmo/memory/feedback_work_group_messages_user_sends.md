---
name: feedback-work-group-messages-user-sends
description: 给同事/工作群的消息起草后直接给纯文本让用户自己发，别走 send_message 代发确认流程
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3b19a712-a4d7-4919-9b58-23c3a5bf1683
  modified: 2026-09-01T07:32:13.253Z
---

给同事或工作群（飞书）的消息：起草好后**直接把纯文本贴在对话里让用户自己复制发送**，不要走 social-proxy send_message 的 preview→confirm 代发流程。

**Why:** 2026-09-01 动图埋点联调，让用户给后端同事发 character id，我走了 send_message preview + AskUserQuestion 确认，被打断："你直接返回给我 让我发"。工作群消息他要用自己的手发，代发多两轮交互还不如直接给文案。

**How to apply:** 用户说"给XX发/回一下XX"且对象是同事/工作群时，产出可直接粘贴的纯文本（[[feedback_copy_content_delivery]]：短文案不带 markdown 装饰）。send_message 代发保留给用户明说"帮我发出去"的场景。
