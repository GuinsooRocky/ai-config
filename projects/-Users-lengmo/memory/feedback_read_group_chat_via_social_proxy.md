---
name: feedback_read_group_chat_via_social_proxy
description: 用户提到群里在聊什么/同事怎么说时，先用 social-proxy 自己读飞书群，别让用户截图
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d78a1e7c-eb9d-446f-81f4-042857417b09
  modified: 2026-09-09T09:14:09.786Z
---

排查 onlychat 线上/测试环境问题时，群里（飞书「创作者分成大需求群」等）往往已经有同事给出关键线索。
用户提到「群里说」「Alice 说」或贴同事截图时，先用 social-proxy 自己读：
`execute_tool(name="find_thread_by_name", args={"name":"<群名关键字>"})` 拿 thread_id，
再 `get_history(thread_id, limit)`；话题（topic）里的回复同步有几分钟延迟，最新几条可能还没入库。

**Why:** 2026-09-09 查付费图免费缩略图空白 bug，用户连贴 4 张群截图后说
「你多看看群信息就不用我给你截图了」。

**How to apply:** 接到 onlychat 排障任务先扫一遍相关群最近消息再动手；转述同事结论时注明来源和时间。
相关：[[project_onlychat]]
