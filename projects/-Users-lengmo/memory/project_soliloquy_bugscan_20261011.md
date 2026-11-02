---
name: project_soliloquy_bugscan_20261011
description: 2026-10-11 soliloquy 全仓捉虫 + 10-12 并行修复的终态：10-12 合 main（3e0aeb371，41 提交）；26 条迁移已全跑、Server 已发，Web 已随 10-16 发布带上，eval-arena 合同已同步；原报告目录已不在本机，条目内留 7 条既定假设和操作坑；另记 2026-10-12 soliloquy 验证机制（CI 闸 / Engineering Verification / 性能实验室 / 跑批线）空壳审查，真相在仓内 docs/prd/research/2026-10-12-验证机制审查.md
metadata:
  node_type: memory
  type: project
  originSessionId: 7ea49df9-4ecd-41a9-999f-cd80a8377ddd
  modified: 2026-11-02T07:53:11.823Z
---

**现状**：修复分支 `lengmo_20261011_fix_bugscan` 已合 main（3e0aeb371，41 提交）；26 条迁移已全跑，Server 已发，Web 已随 10-16 发布带上，eval-arena 合同已同步。原报告目录 `~/Desktop/loop_project/soliloquy-bugscan-20261011/` 已不在本机，别去找。

**结果**：扫描 150 条经对抗（P1 19 条 / 18 根因）；修复 27 路 + 27 路独立审查（7 路退回返工后通过），跟踪 123 条：119 已修 / 3 部分 / 1 转他路修掉。质量备注 203 条未动（排在 bug 之后）。

**7 条既定假设（owner 可否决）**：A1 无 OC 会话按账号级放行、A2 截断不扣点、A3 R2 改投不搬聊天图、A4 清卡脚本只认卡主、出图 / 语音 5xx 仍当场退点、名册失败拒绝写入、四语词典重绑需批准。

**Why:** owner 10-11「对整个 soliloquy 做代码捉虫，多路并行」、10-12「解决了吗，没解决多路并行解决」。
**How to apply:** 这批已发完，别按旧发布顺序重做。操作坑：hosted 库脚本在本机要 `NODE_EXTRA_CA_CERTS=~/.config/soliloquy/supabase-root-2021.pem` 且 worktree 要拷主仓 `.env.setup`；**别把根 `.env.local` 拷进 worktree**——`pnpm dev:desktop` 会读它连真 Supabase，e2e 的 OTP 首登链当场红（10-12 踩过）；本机 HTTPS 到 GitHub 被重置时，推送带 `-c url.git@github.com:.pushInsteadOf=https://github.com/` 走 SSH。相关：[[feedback-delegate-impl-to-opus-subagent]]、[[project_soliloquy]]

## 验证机制审查（CI 闸 / Engineering Verification / 性能实验室 / 跑批线）

2026-10-12 用「闸到底验没验到东西」的角度审了 soliloquy 全部验证机制，结论文档落在仓内 `docs/prd/research/2026-10-12-验证机制审查.md`（已登记 docs/README research 索引），37 条问题（P0 4），3 条待拍（Engineering Full cron 停/接、deploy-edge 退役、reply+capacity 四场景撤目录）。

关键事实：main CI 09-08～10-14 无绿，2026-10-15 a31e5010e 已恢复绿（之后 e109a2644 那次被执行方手动取消、未出结果）；09-09 起 Actions 账单停摆，10-01～10-09 恢复期 42 次全红无人读；Engineering Full 每天 12/12 unavailable 结构上不可能红；生产发布脚本不引用任何验证裁决。

10-13 三条待拍已按推荐执行并合入 main（PR #15，merge 78264b236）：Full 停定时、deploy-edge 退役（仓库变量已删）、reply+capacity 四场景 disabled、Escape 放行修复一并合入。仍开着的坑：perf:web 仍 partial（28 样本缺 INP，V-17）；审查文档 V-05～V-23 其余 P1 未动。

**Why:** owner 当时记得「有个比架构高一层的框架放在 CI 上」，回查发现它半年空跑。
**How to apply:** 再碰 soliloquy CI / 性能采集 / Engineering Full 时先读那份文档，别重审。相关 [[soliloquy-harness-loops]]。
