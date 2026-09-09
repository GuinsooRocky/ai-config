---
name: reference_onlychat_cdn_batch_upload
description: onlychat 批量种图/拿 CDN fileURL 的 console 技法——全文已迁 onlychat-World-Path/CDN批量种图-console技法.md，这里只留指针
metadata:
  node_type: memory
  type: reference
  modified: 2026-09-09T00:00:00.000Z
---

把一批本地图片刷进 onlychat CDN 拿回 fileURL：在已登录的 onlychat 页面 DevTools Console 跑 `character.querySignedUploadUrlV2` 签名 + PUT 直传的 snippet。**全文（snippet + 关键点）= `~/Desktop/cmm/onlychat-World-Path/CDN批量种图-console技法.md`**。鉴权绕不开浏览器登录态，所以做不成 skill/agent。用于世界卡笔记默认配图等种图场景。相关 [[project_onlychat]]、[[feedback_worldcard_worktree]]。
