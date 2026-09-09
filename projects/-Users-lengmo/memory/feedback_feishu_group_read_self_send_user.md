---
name: feedback_feishu_group_read_self_send_user
description: 飞书群一进一出：消息自己用 social-proxy 读（find_thread_by_name→get_history，话题回复有几分钟延迟）别要截图；给同事的消息只给纯文本让用户自己发，不走 send_message 代发
metadata:
  node_type: memory
  type: feedback
  modified: 2026-09-09T00:00:00.000Z
---

## 读：群里在聊什么，自己去读

排查 onlychat 线上/测试环境问题时，群里（飞书「创作者分成大需求群」等）往往已经有同事给出关键线索。用户提到「群里说」「XX 说」或贴同事截图时，先用 social-proxy 自己读：`execute_tool(name="find_thread_by_name", args={"name":"<群名关键字>"})` 拿 thread_id，再 `get_history(thread_id, limit)`。话题（topic）里的回复入库有几分钟延迟，最新几条可能还没到。

**Why:** 2026-09-09 查付费图免费缩略图空白 bug，用户连贴 4 张群截图后说「你多看看群信息就不用我给你截图了」。

**How to apply:** 接到 onlychat 排障任务先扫一遍相关群最近消息再动手；转述同事结论时注明来源和时间。

## 发：给同事的消息，纯文本交给用户自己发

给同事或工作群（飞书）的消息：起草好后**直接把纯文本贴在对话里让用户自己复制发送**，不走 social-proxy send_message 的 preview→confirm 代发流程。

**Why:** 2026-09-01 动图埋点联调，让用户给后端同事发 character id，我走了 send_message preview + AskUserQuestion 确认，被打断：「你直接返回给我 让我发」。工作群消息他要用自己的手发。

**How to apply:** 用户说「给 XX 发/回一下 XX」且对象是同事/工作群时，产出可直接粘贴的纯文本（[[feedback_copy_content_delivery]]：短文案不带 markdown 装饰）。send_message 代发只留给用户明说「帮我发出去」的场景。改动说明怎么写见 [[feedback_no_jargon_plain_product_language]]。相关 [[project_onlychat]]。
