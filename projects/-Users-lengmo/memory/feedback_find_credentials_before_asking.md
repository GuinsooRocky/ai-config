---
name: feedback-find-credentials-before-asking
description: "让 owner 补密钥前先穷尽自己能读的地方（.env*/本地配置/浏览器已登录页），拿不到再开口且说清\"哪把 key、缺在哪\"；GROQ_API_KEY 在 ~/.zshrc（仅交互式 shell），非交互 Bash 工具读不到→401，要从 .zshrc 抠出来；soliloquy 等个人项目的账号/密码/外部服务入口统一记在 ~/Desktop/loop_project/账号备忘/，不进仓内 docs/ops 台账"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d6e7203e-1f70-41c6-ad63-2cf63d78ea21
  modified: 2026-11-02T07:52:42.578Z
---

2026-07-11 soliloquy T20 部署窗：我让 owner「补 VPS 的 OPENROUTER_API_KEY」，owner 回「我已经无语了，明明密钥都有的，你到底要什么密钥？」——key 就躺在项目 `.env.local` 的 `PUBLIC_OPENROUTER_API_KEY`，我一句 grep 就能拿到并自己填好。

**Why**：owner 视角里"密钥早就配过了"（Supabase secrets、本地 env 都有），我笼统一句"补 key"读起来像在要一个不存在的新东西。真正缺的只是"某个具体文件缺一份拷贝"，而拷贝源我自己就够得着。

**How to apply**：
1. 缺凭证时先穷尽自己可读的源：项目 `.env*` 全家（含 .env.setup/.env.local）、仓内配置、能 ssh 的机器上的 env 文件；用户说"开浏览器自己查"时也可以走已登录的浏览器页（先确认 --chrome 开着，见 [[feedback_chrome_extension_on_demand]]）。
2. 真拿不到再开口，且必须说清三件事：**哪把 key（服务名+用途）、现在缺在哪个文件/哪台机器、我为什么读不到**（如 Supabase secrets 只写不读）。
3. 说"owner 动作"前先自问：这个动作里有没有我其实能代劳的部分——能代劳的部分做掉，只把真正非 owner 不可的留给他。


补充：07-11 OPENROUTER key 就在 .env.local 却让 owner 补，被无语

## GROQ key 在 zshrc

`GROQ_API_KEY`（whisper 转写用，video skill 等）export 在 **~/.zshrc** 里，只有交互式 zsh 才加载。Claude Code 的 Bash 工具跑的是**非交互 shell**，`$GROQ_API_KEY` 经常是空的 → Groq 返回 401 `invalid_api_key`（注意：这跟网络断的 000 是两回事）。

**取 key**：`KEY=$(grep -E '^\s*export\s+GROQ_API_KEY=' ~/.zshrc | head -1 | sed -E 's/.*GROQ_API_KEY=//; s/^["'\'']//; s/["'\''].*$//')`，或 `zsh -ic 'echo $GROQ_API_KEY'`。脚本里先查 env、空了就从 .zshrc fallback。

**配套坑**（2026-06 小宇宙整档转写踩过）：
- 沙箱直连 api.groq.com 会**间歇性 000**（egress 抽风，跟用户本机网络/梯子无关，别甩锅代理）；恢复后才暴露 key 为空的 401。
- 大文件单发易 **524**（网关超时）→ 切 8min/块、`response_format=json`（逐字稿不需要时间戳）。
- 快速连转 ~3h 音频会撞 **429**（免费额度 ~7200s/小时），脚本遇 429 sleep 60s 自动续。
- 小宇宙 `/podcast/` 页 SSR 只渲染最新 ~15 集，更早的（含 ch1-2）要登录态分页 API（匿名 401）→ 让用户给 `/episode/` 链接直接转。每集页 `__NEXT_DATA__` 里有官方 `shownotes`（零误差）可当术语校准源。

## 个人项目账号备忘

个人项目（soliloquy 为主）的账号、密码、恢复方式、外部服务入口 → `~/Desktop/loop_project/账号备忘/外部服务账号清单.md`（仓外、不进 git）；单把 key 另存同目录 0600 txt。

**Why:** 2026-09-30 把 Proton/Google 项目号记进 soliloquy 仓 `docs/ops/外部服务台账.md`，owner 判「没意义」，指出 loop_project 下有专门文件。
**How to apply:** owner 说「记下来/放 doc 里怕丢」的账号类信息，直接追加到该清单，只写终态（是什么、在哪），不写注册过程。相关：[[feedback-deliverable-is-final-state-not-process]]
