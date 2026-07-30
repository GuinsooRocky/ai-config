---
name: project_soliloquy
description: 独白(soliloquy)项目=个人 Tauri 桌面 AI 陪伴客户端，路径/形态/技术栈/台账位置指针
metadata: 
  node_type: memory
  type: project
  originSessionId: b9eb6b3a-39fa-4b21-97d6-c08b50f0e514
  modified: 2026-07-30T07:29:10.491Z
---

「独白」= **soliloquy**，路径 `~/Desktop/loop_project/soliloquy`（个人项目，非工作仓；已从 `~/Desktop/my-code/` 迁走，勿用旧路径）。

## 是什么

以你为中心的对话桌面客户端，三端同步。两类对象：**独白会话**（inbox，不调 AI 的记事/收件箱）+ **伙伴会话**（companion，有人格 + 三层混合记忆 + mood/亲密度的 AI 角色）。

**定位**：陪伴线，对标 CrushOn。干净线（学习伙伴/看板/收件箱）已整仓拆去 `~/Desktop/my-code/lich`，**拆完两仓完全独立互不同步**，搬功能只在你主动说的时候。

**2026-07-03 pivot**：OC 从"伙伴的私有人设"翻案为**可复用、可发布的角色素材**——OC 独立成表 ↔ 伙伴=实例，靠 `oc_id` 引用，状态留实例侧。这条 pivot 主动推翻了原 roadmap「不做 UGC 角色市场」的必输点。

## 关键设计不变量（改这块前先想清楚）

**实例化那一刻把 persona/gender/appearance 拷进 `conversations`，注入时读会话自己的那份，绝不 live-read `oc`。** 所以编辑 OC 不会牵连已有的老实例。（OC-1a 一度实现成 live-read，FIX-1 拨正过——别再滑回去。）

## 台账在哪（2026-07-30 核实的现行结构）

| 用途 | 位置 |
|---|---|
| 待办池 | `docs/prd/BACKLOG.md`（编号发放：下一个可用见文件头） |
| 已完成归档 | `docs/prd/DONE.md` |
| **红线单一真相** | `docs/prd/REDLINES.md` ← 别在别处抄红线，会漂 |
| 拍板箱 | `loop/decisions.md`（append-only，已 1500+ 行——**引用它只用标题搜，别记行号**） |
| 人工闸（要人眼/真机的） | `loop/manual-verify.md` |
| 设计文档 | `docs/prd/designs/` |

⚠ 旧口径作废：`loop/fix_plan.md` 和「BACKLOG 簇⑨」那套编号**已随 07-27 机制重构消失**，别再找。

## 技术栈

Tauri + React 19 + **Rsbuild**（已替 Vite）+ pnpm；后端自有 **Supabase**（RLS 全表开 + OTP 邮箱登录，按 user_id 隔离）；repo 契约层 `src/lib/repo/`（contract.ts 接口 + supabase.ts 唯一实现 + index.ts 指向）。

**改后端数据**：迁移走 `pnpm tsx scripts/run-migration.ts <file>`（用 `.env.setup` 的库 owner 直连）；验证/造数据可用 anon key（`.env.local`）跑临时脚本。

## 红线

**只有一条值得刻在这里**：未成年内容是无审查卖点下**唯一不可越的刑事红线**（`safetyGuard` 拦原文+增强后文本，出图侧另有闸）。

其余全部去 `docs/prd/REDLINES.md` 现读——那里每条带状态，**有翻案过的**（「不做群聊」2026-07-16 已翻案、「不做 UGC 角色市场」2026-07-03 已翻案），照旧记忆办事会办错。

## 当前真待办（2026-07-30 进仓核实）

1. **「四线施工决策包」还没跑** —— `designs/2026-07-26-四线施工决策包.md` 不存在。这是 07-26 四线调研（埋点/多语言/季付年付/图谱记忆）审判收官后唯一挂着的下一步：出依赖顺序 / 冲突矩阵 / 预算合并 / 合并待拍表。
2. **官方种子号 creator_id 迁不迁** —— 仍在 `BACKLOG.md` 的「待拍」节（T22 的根，权宜方案 b 现行）。dry-run 早备好，等你放行。
3. **T36 种子卡换图** —— 挂账中（07-11 owner 拍「不考虑版权」）。

## 已作废的旧口径（别再照着办）

- ~~T20 剩 4 步 / 真机验收~~ → **T20 发布硬前置 2026-07-15 已全清**，只剩 owner 软 A/B 验收且非发布阻断
- ~~selfie 保留、待 owner ack~~ → **已 ack 且反向**：T7 整条挂账不做（owner 07-13 拍）
- ~~N4b Sidebar 残留~~ → 全仓 0 命中，已消失
- ~~人工闸 ③迁移 / ④走查 / ⑤打包~~ → 编号体系不存在了，现在看 `loop/manual-verify.md`
- ~~四线拍板在 decisions.md :987-1020~~ → 行号已漂，按标题搜

## 历史

07-03→07-26 的逐批施工战报（OC 三步、市场卡片流、IA 重构、QA 马拉松、模型升级、内部账号门控等）原本抄在这里，**2026-07-30 移除**——仓已跑到 T155，`docs/prd/DONE.md` 才是那些东西的正式归档。要考古去 DONE.md 和 `loop/decisions.md`。原文备份在 `~/.Trash/memory-project_soliloquy-备份-20260730.md`。

相关：[[project_soliloquy_harness_loops]]（跑批线机制）、[[project_soliloquy_review_panel]]（14 席评审团）、[[project_co_model_eval_arena]]（anna 评测）、[[feedback_project_intel_stays_in_project_docs]]、[[feedback_cleanup_use_trash_not_rm]]
