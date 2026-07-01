---
name: feedback_sf_reader_concurrency
description: sf-reader-all 批量抓取要串行/低并发；12 并发会让 Playwright 浏览器互相饿死全部超时
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6d282902-a6aa-47b0-a5d2-ca193123dd4c
---

批量用 `sf-reader-all` 抓多条 URL 时，**必须串行或低并发（≤2）**，不要一个 agent 一条 URL 同时开十几个。

**Why**：每条微信/B站走的是 Playwright headless 浏览器兜底（Jina 那层撞风控）。单跑一条 ~16s 就过；但 12 条并发 = 12 个浏览器实例互相饿死，全部卡 30s 超时 → 看起来像"微信彻底风控"，其实是并发资源争抢。2026-05-30 在 redesign-006 workflow 踩过：12 抓取 agent 里 10 个失败，串行重抓后 8/8 全过。

**How to apply**：
- 抓 N 条 → 在**一个** Bash 里 `for` 循环串行跑，不要 fan-out 成 N 个并发 agent。
- 全文不在 stdout（只打印预览头）——在 `unified_inbox.json`（默认落 cwd，`INBOX_FILE` 可改）；按内容字数核验真正文，别只看 exit code（见 [[feedback_verify_capture_not_status]]）。
- 这类小批抓取本就该 inline 串行，不该开 background workflow（见 [[feedback_inline_over_background_workflow]]）。
