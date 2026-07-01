---
name: feedback_groq_key_in_zshrc
description: GROQ_API_KEY 在 ~/.zshrc（仅交互式 shell）；非交互 Bash 工具读不到→401，要从 .zshrc 抠出来
metadata: 
  node_type: memory
  type: project
  originSessionId: ae6c2eee-eb3c-4fe2-930e-8582aaa61f16
---

`GROQ_API_KEY`（whisper 转写用，video skill 等）export 在 **~/.zshrc** 里，只有交互式 zsh 才加载。Claude Code 的 Bash 工具跑的是**非交互 shell**，`$GROQ_API_KEY` 经常是空的 → Groq 返回 401 `invalid_api_key`（注意：这跟网络断的 000 是两回事）。

**取 key**：`KEY=$(grep -E '^\s*export\s+GROQ_API_KEY=' ~/.zshrc | head -1 | sed -E 's/.*GROQ_API_KEY=//; s/^["'\'']//; s/["'\''].*$//')`，或 `zsh -ic 'echo $GROQ_API_KEY'`。脚本里先查 env、空了就从 .zshrc fallback。

**配套坑**（2026-06 小宇宙整档转写踩过）：
- 沙箱直连 api.groq.com 会**间歇性 000**（egress 抽风，跟用户本机网络/梯子无关，别甩锅代理）；恢复后才暴露 key 为空的 401。
- 大文件单发易 **524**（网关超时）→ 切 8min/块、`response_format=json`（逐字稿不需要时间戳）。
- 快速连转 ~3h 音频会撞 **429**（免费额度 ~7200s/小时），脚本遇 429 sleep 60s 自动续。
- 小宇宙 `/podcast/` 页 SSR 只渲染最新 ~15 集，更早的（含 ch1-2）要登录态分页 API（匿名 401）→ 让用户给 `/episode/` 链接直接转。每集页 `__NEXT_DATA__` 里有官方 `shownotes`（零误差）可当术语校准源。
