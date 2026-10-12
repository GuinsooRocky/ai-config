---
name: project_soliloquy_bugscan_20261011
description: 2026-10-11 soliloquy 全仓捉虫 + 10-12 并行修复；10-12 晚已 fast-forward 合进 origin/main（3e0aeb371，41 提交），两套 Playwright 与 code-gate 全绿；26 条迁移已全跑、Server 已发；Web 未单独补发（owner 定：留给下次任何 Web 发布顺带）；eval-arena 合同同步未做、迁移未在生产执行、owner 待拍清单在 FINAL §修复回执
metadata:
  type: project
---

**位置**：`~/Desktop/loop_project/soliloquy-bugscan-20261011/`——`FINAL.md`（扫描结论 + 「修复回执」节，唯一真相）、`reports/`（猎手 / 对抗 / DIGEST / QUALITY）、`fix/`（FIX_BRIEF、REVIEW_BRIEF、ROUTES 路单、`fix/reports/<路>.md` 与 `.review.md`）、`STATUS.md`（过程账）。修复 worktree `repo/`，分支 `lengmo_20261011_fix_bugscan`（基于 `origin/main e5ec727b9`，10-12 已推到 origin 并设 upstream；本机 HTTPS 到 GitHub 会被重置，推送要带 `-c url.git@github.com:.pushInsteadOf=https://github.com/` 走 SSH），依赖已离线装好。

**结果**：扫描 150 条经对抗（P1 19 条 / 18 根因）；修复 27 路 + 27 路独立审查（7 路退回返工后通过），跟踪 123 条：119 已修 / 3 部分 / 1 转他路修掉；35 个提交、342 文件、71 个新测试文件、25 份新迁移（已登记发布计划，**没在生产执行**）。质量备注 203 条未动（排在 bug 之后）。全量 code-gate 退出 1，4 红无一由分支引入：i18n-review-check（owner 重绑词典即绿）、archiveRowsIntegration ×2 与 observabilityDataHealthIntegration ×1（main 既有，`docs/ops/2026-10-09-角色画布-发布集成阻断.md` 记为 owner 允许）、测试收集哨兵（main `a6b8a8987` 放进 docs/ 的 recovery.spec.ts，main 自己的收尾项）。

**owner 要拍 / 要做**（全在 FINAL §修复回执）：7 条既定假设可否决（A1 无 OC 会话按账号级放行、A2 截断不扣点、A3 R2 改投不搬聊天图、A4 清卡脚本只认卡主、出图 / 语音 5xx 仍当场退点、名册失败拒绝写入、四语词典重绑需批准）；上线顺序硬约束（先迁移再发客户端、W06 与 eval-arena 同步顺序、Turnstile 两把 key 一致）；生产盘点 SQL；运行时走查未做（各路不起 dev）。

**Why:** owner 10-11「对整个 soliloquy 做代码捉虫，多路并行」、10-12「解决了吗，没解决多路并行解决」。
**How to apply:** 接到「发版 / 继续」先读 FINAL §修复回执末两节：发布顺序=26 条迁移（W06 160000 要先发 Server + eval-arena 同步、160300 先发 Server、F08 两份先于客户端）→ `release:vps` → `release:web` → eval-arena `sync_soliloquy_contracts.py`；迁移是生产库不可逆项，必须 owner 原话「跑」。hosted 库脚本在本机要 `NODE_EXTRA_CA_CERTS=~/.config/soliloquy/supabase-root-2021.pem` 且 worktree 要拷主仓 `.env.setup`；**别把根 `.env.local` 拷进 worktree**——`pnpm dev:desktop` 会读它连真 Supabase，e2e 的 OTP 首登链当场红（10-12 踩过）。相关：[[parallel-subagent-fix-pipeline]]、[[project_soliloquy]]
