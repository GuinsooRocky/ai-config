---
name: feedback-find-credentials-before-asking
description: "让 owner 补密钥前先穷尽自己能读的地方（.env*/本地配置/浏览器已登录页），拿不到再开口且说清\"哪把 key、缺在哪\""
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d6e7203e-1f70-41c6-ad63-2cf63d78ea21
---

2026-07-11 soliloquy T20 部署窗：我让 owner「补 VPS 的 OPENROUTER_API_KEY」，owner 回「我已经无语了，明明密钥都有的，你到底要什么密钥？」——key 就躺在项目 `.env.local` 的 `PUBLIC_OPENROUTER_API_KEY`，我一句 grep 就能拿到并自己填好。

**Why**：owner 视角里"密钥早就配过了"（Supabase secrets、本地 env 都有），我笼统一句"补 key"读起来像在要一个不存在的新东西。真正缺的只是"某个具体文件缺一份拷贝"，而拷贝源我自己就够得着。

**How to apply**：
1. 缺凭证时先穷尽自己可读的源：项目 `.env*` 全家（含 .env.setup/.env.local）、仓内配置、能 ssh 的机器上的 env 文件；用户说"开浏览器自己查"时也可以走已登录的浏览器页（先确认 --chrome 开着，见 [[feedback_chrome_extension_on_demand]]）。
2. 真拿不到再开口，且必须说清三件事：**哪把 key（服务名+用途）、现在缺在哪个文件/哪台机器、我为什么读不到**（如 Supabase secrets 只写不读）。
3. 说"owner 动作"前先自问：这个动作里有没有我其实能代劳的部分——能代劳的部分做掉，只把真正非 owner 不可的留给他。
