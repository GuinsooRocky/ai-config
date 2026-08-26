---
name: project_dk_sidecar_deploy
description: DK macapp 后端(sidecar)部署铁律——别 in-place 换+重签，会破 launchd self-spawn
metadata: 
  node_type: memory
  type: project
  originSessionId: 0bfe1fc4-f4f0-4519-a099-41dd432c58f7
---

DK 改后端**只能整体 `bash macapp/build_app.sh` 重建+一次性签，绝不 in-place 换 sidecar+反复重签**（破 launchd self-spawn，把 bot 搞停过）。

**铁律全文/验证旁路/应急恢复命令已迁入项目仓** `~/Desktop/my-code/dk/CLAUDE.md`（2026-07-06 新建，已 commit+push 到 ralph/auto 分支）。相关：[[feedback_commit_policy]]。
