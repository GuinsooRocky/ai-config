---
name: feedback-no-auto-start-dev-app
description: 改完代码别自己起 dev（Tauri/桌面 app 会抢窗口焦点），验证走静态检查，跑 app 交给 owner
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 879cf500-7ec5-4237-af9e-84bf80e6fa7b
  modified: 2026-07-30T06:45:43.989Z
---

改完代码不要自己 `pnpm tauri dev` / 起 dev server —— 桌面 app 一启动就抢窗口焦点，打断 owner 手上的事。

**Why:** 2026-07-30 lich 项目落地 PRD 批次时，为验证 capabilities 生效起了一次 tauri dev，owner 当场喊停「代码改动不要启动 dev 好吗 不然总抢窗口」。

**How to apply:** 自己能做的验证只做静态的（tsc --noEmit、build:ui、把纯逻辑抠成 node 脚本跑真文件系统）；需要真在 app 里点的验收条目，如实列成「待 owner 点」清单交回去，别为了勾验收去启动 app。跟 [[feedback_delegate_impl_to_opus_subagent]] 里「浏览器走查派 visual-qa」是两回事——桌面原生窗口 visual-qa 也驱动不了。
