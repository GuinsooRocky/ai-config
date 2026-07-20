---
name: project_onlychat_dev_proxy_grpc_403
description: onlychat dev 全站 tRPC 403/UNAVAILABLE 排查——先查 dev 进程的 http_proxy=127.0.0.1:7897
metadata: 
  node_type: memory
  type: project
  originSessionId: b367b570-0ba6-4091-b1d0-39714ab0c9d9
---

onlychat dev 全站 tRPC 403/UNAVAILABLE → 第一嫌疑 dev 进程继承 `http_proxy=127.0.0.1:7897`（Clash 污染 grpc-js）；后端直连是好的，从 proxy-clean shell 重起 watchdog。

**确诊命令/修复步骤/永久兜底已迁入** `~/Desktop/cmm/onlychat-World-Path/03-环境变量说明.md` 末节（2026-07-06）。
