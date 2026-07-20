---
name: crushon-admin-pre-deploy
description: crushon-admin 封板→上 pre 的流程指针（全文在 cmm/crushon-admin上pre流程.md）
metadata: 
  node_type: memory
  type: project
  originSessionId: 1fd9fd67-fc8d-4b11-b3ae-67fffdb43626
---

crushon-admin 封板→上 pre 的完整 runbook 落在 **`~/Desktop/cmm/crushon-admin上pre流程.md`**，接到「admin 上 pre」任务先读它。

速记：cherry-pick 进 release（CI 自动出镜像）→ **onlychat 仓** `deploy-argocd.yml`（来自=**develop** 别选 release、项目=crushon-admin、7 位 hash）→ argocd-frontend PR 核一行 diff 后用「创建合并提交」合到 pre → 验 crushon-admin-pre.peekaboo.tech。

相关：[[feedback-project-intel-stays-in-project-docs]]（全文按此规矩落项目文档，memory 只留本指针）
