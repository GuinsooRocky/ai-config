---
name: pages-publish-via-social-proxy
description: pages-publish skill 的原生 pages MCP 已失效，发内网页面+飞书卡片直接用 social-proxy 的 publish_page / share_page
metadata: 
  node_type: memory
  type: reference
  originSessionId: e15a9aa1-131d-4daa-b91a-c96b1367b177
  modified: 2026-10-29T09:19:57.662Z
---

pages-publish skill 依赖的 `pages` MCP 在本机已**不再注册**，历史 token（b48cc…）已 401。替代路 = social-proxy：

- social-proxy 自带 `publish_page` / `publish_markdown` / `share_page` / `send_message`，同样发到 pages.pkbops.com + 以用户本人身份发飞书卡片。
- 本机 social-proxy 是 **profile=full（75 个动作）**，home scope 会话里直接 `execute_tool(name="publish_page", args={…})` 即可，不用绕路。参数不熟先 `search_tools({names:["publish_page"]})` 拿 schema。
- `share_page`/`send_message` 默认 confirm=false 只回 preview（含收件人唯一命中校验），确认无误再 confirm=true 真发。
- 飞书同事「wei」= **Wei 徐唯原**（onlychat 数据同学，私聊 thread 存在，contact_name 传「徐唯原」即可唯一命中）。
- 「liuxinyi」= **刘心仪**（「创建大群」成员，10-29 在群里提 Draft 存储规则需求的人）。「创建大群」成员里有两个同显示名的「刘心仪」，`@刘心仪` 必报 needs_clarification——直接用 send_message 的 `reply_to` 引用回复她的原消息，不带 @。
- share_page 的 description 不解析 @；要在群里 @ 人又要带页面链接，用 send_message format=card + 按钮（url=页面链接），一条消息搞定。
- ⚠ `~/.claude/skills/pages-publish/SKILL.md` 仍写着调 `mcp__pages__publish_page`（已死），照它做会失败——按本条走 social-proxy。
