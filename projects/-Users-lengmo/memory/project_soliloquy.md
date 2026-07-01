---
name: project_soliloquy
description: 独白(soliloquy)项目=个人 Tauri 桌面 AI 伴侣+收件箱客户端，路径/技术栈/文档位置指针
metadata: 
  node_type: memory
  type: project
  originSessionId: b9eb6b3a-39fa-4b21-97d6-c08b50f0e514
---

「独白」= **soliloquy** 项目，路径 `~/Desktop/my-code/soliloquy`（个人项目，非工作仓）。

- **是什么**：以你为中心的对话桌面客户端，三端同步。两类对象：独白会话(inbox，不调 AI 的记事/收件箱) + 伙伴会话(companion，有人格+三层混合记忆+mood/亲密度的 AI 角色，默认 seed 一个 cinco)。战略定位：「私人 AI 朋友圈 + 收件箱」，主打隐私/数据主权/桌面常驻。
- **技术栈**：Tauri + React + **Rsbuild**（已替 Vite）+ pnpm；后端自有 **Supabase**（全表 RLS 关、anon key 编进 bundle、单用户无登录）；repo 契约层 `src/lib/repo/`（contract.ts 接口 + supabase.ts 唯一实现 + index.ts 指向）。
- **改后端数据**：迁移走 `pnpm tsx scripts/run-migration.ts <file>`（用 .env.setup 的库 owner 直连）；验证/造数据可用 anon key（.env.local）跑临时脚本。
- **文档**：PRD 在仓根 `PRD.md`，路线图 `docs/v0.3-roadmap.md`（含 backlog B-01~B-04 + 必输点清单），设计文档按日期落 `docs/designs/`。
- **必输点(别撞)**：通用 AI 助手 / UGC 角色市场 / mobile mood 打卡 / 角色 IP 分发 / 高频付费档。红线：AI 不主动播报、no-auto-delete、news 零抓取代码进 app。
- 工作法沿用全局：项目情报落项目文档不进全局 memory(见 [[feedback_project_intel_stays_in_project_docs]])；删文件走废纸篓(见 [[feedback_cleanup_use_trash_not_rm]])。
