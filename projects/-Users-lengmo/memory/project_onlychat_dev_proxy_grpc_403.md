---
name: project_onlychat_dev_proxy_grpc_403
description: onlychat dev 全站 tRPC 403/UNAVAILABLE 排查——先查 dev 进程的 http_proxy=127.0.0.1:7897
metadata: 
  node_type: memory
  type: project
  originSessionId: b367b570-0ba6-4091-b1d0-39714ab0c9d9
---

onlychat 系列 dev server（含 world-book）若**全站 tRPC 报 `HTTP 403 / PERMISSION_DENIED`，或重启后变 `UNAVAILABLE / No connection established`**，第一嫌疑是 **dev 进程继承了 `http_proxy/https_proxy=http://127.0.0.1:7897`**（Clash Verge 默认 mixed 端口），grpc-js 认 `https_proxy` 把后端 `GRPC_HOST=co.grpc.pkbsvc.com:443` 强行导去 Clash。

**因果**：Clash 开着→上游出口 IP 被 Cloudflare 风控返 403；Clash 关掉→连 7897 都 ECONNREFUSED→UNAVAILABLE。**与业务代码、service token（`CRUSHON_BACKEND_AUTHORIZATION`，base64 解出 `crushon:AiK8vm4d`）、后端服务全无关**。

**确诊（30 秒）**：
- `ps eww -o command= -p <next-router-worker-pid> | tr ' ' '\n' | grep -iE '^https?_proxy='` → 看是否有 7897。注意 `ps eww` 取的是 exec 时 OS 环境；dotenv 注入的值看不到，但 proxy 是 shell 继承的所以能看到。
- 直连验证后端是好的：`curl --http2 -X POST -H 'content-type: application/grpc' -H 'te: trailers' --data-binary $'\x00\x00\x00\x00\x00' https://co.grpc.pkbsvc.com/intranet.UserService/GetSessionUser` → 应 `HTTP/2 200` + `x-envoy-upstream-service-time`（穿透 Cloudflare 到 Envoy，grpc-status 2/13 只因 payload 空）。curl 200 但 app 挂 = 代理在作怪。

**修复**：从 proxy-clean 的 shell 重起 watchdog（杀旧 watchdog+dev、清 3000/3001，再 `env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY nohup dev-watchdog.sh <worktree> &`）。验证：新 next 进程无 proxy 变量 + `curl -L localhost:3000/en/explore` 返 200 且日志 0 条 `Failed to connect to proxy / 403 / UNAVAILABLE`（`[Auth]` 只在失败时打日志，成功静默）。

**永久兜底（可选，需用户同意改全局）**：`~/.zshenv` 的 `no_proxy/NO_PROXY` 现仅含 localhost；加 `.pkbsvc.com,.crushon.ai` 后即便误带 https_proxy，grpc-js 也对后端直连。

相关：[[project_worldbook_dev_oom]]（watchdog 生命周期 / kill_port 连 3001）、[[project_onlychat]]、cmm-go skill 管 watchdog。
