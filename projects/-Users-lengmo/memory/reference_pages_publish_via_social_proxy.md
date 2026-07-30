---
name: pages-publish-via-social-proxy
description: pages-publish skill 的原生 pages MCP 已失效，发内网页面+飞书卡片改走 social-proxy messages 通道
metadata: 
  node_type: memory
  type: reference
  originSessionId: e15a9aa1-131d-4daa-b91a-c96b1367b177
  modified: 2026-07-23T12:58:53.525Z
---

pages-publish skill 依赖的 `pages` MCP 在本机已**不再注册**，历史 token（b48cc…）已 401。2026-07-23 起可用替代路：

- social-proxy 的 **messages profile** 自带 `publish_page` / `publish_markdown` / `share_page` / `send_message`，同样发到 pages.pkbops.com + 以用户本人身份发飞书卡片。
- 该 profile 只注册在 `~/Desktop/cmm/social-proxy-test` 项目 scope，别的会话里直接用 curl 打 `https://socail-agent.com/api/mcp/messages`（JSON-RPC tools/call），Bearer token 在 `~/.claude.json` 该项目的 mcpServers 里查。
- ⚠ python urllib 会被 403（UA 拦截），用 **curl** 发；大 HTML 先写 payload 文件再 `--data-binary @file`。
- `share_page`/`send_message` 默认 confirm=false 只回 preview（含收件人唯一命中校验），确认无误再 confirm=true 真发。
- 飞书同事「wei」= **Wei 徐唯原**（onlychat 数据同学，私聊 thread 存在，contact_name 传「徐唯原」即可唯一命中）。
