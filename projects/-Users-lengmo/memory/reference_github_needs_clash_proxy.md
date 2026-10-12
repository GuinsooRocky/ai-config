---
name: github-needs-clash-proxy
description: 本机 Clash（127.0.0.1:7897）没开时 GitHub push/fetch/ls-remote 直连会 Connection reset / 超时；soliloquy 发版脚本的 ssh 也靠这个 SOCKS 口
metadata:
  node_type: memory
  type: reference
  originSessionId: c9f3a6b4-b78d-4290-816d-4f95877237f2
  modified: 2026-10-12T07:12:40.953Z
---

2026-10-12 实锤：`lsof -iTCP:7897` 无监听时，`git push/fetch origin`（github.com）连续 `Recv failure: Connection reset by peer`，`curl https://github.com` 15 秒超时 000；不是仓库或凭证问题。

**Why:** 日本住宅网到 GitHub 的直连会被中途切（soliloquy `docs/ops/2026-09-13-Web发版链路抖动与SOCKS绕行.md` 记过同源现象）；`~/.ssh/config` 里 soliloquy 生产机 `167.179.78.237` 也挂了 `ProxyCommand nc -X 5 -x 127.0.0.1:7897`，Clash 不开 `pnpm release:web` 第一步 ssh 就死。

**How to apply:** 推送/发版前先 `lsof -nP -iTCP:7897 -sTCP:LISTEN`；没监听 → 让 owner 开 Clash，别自己改网络设置、别无限重试。开着仍失败再查别的。brew 升级同样要它，见 [[brew-ca-certificates-hook-broken]]。
