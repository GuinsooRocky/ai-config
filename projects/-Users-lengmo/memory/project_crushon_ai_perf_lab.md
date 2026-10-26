---
name: crushon-ai-perf-lab
description: 工作仓 cmm/crushon-ai-perf-lab（onlychat beta 核心 5 页性能合成测量）；规则真相=仓根 CLAUDE.md + docs/README.md；进度现读决策账最新条目；出卡方案 10-26 已定（卡片只给结论+自托管面板），card-and-report.md 已被取代
metadata:
  node_type: memory
  type: project
  originSessionId: c6ff384f-01f4-40b3-9442-38839626ddce
  modified: 2026-10-23T03:52:17.413Z
---

- 仓：`~/Desktop/cmm/crushon-ai-perf-lab`（gitea `peekaboo/crushon-ai-perf-lab`，工作仓：owner 不明说不 commit / push / 开 PR）。PR 目标手动选 `main`（gitea 默认分支仍指旧 skeleton，切换需管理员）。
- 接任务先读仓根 `CLAUDE.md` 和 `docs/README.md`；已定在 `docs/decisions.md`，未定在 `docs/open-questions.md`。别靠记忆复述项目口径。
- 集群现状看 `docs/cluster-2026-10-22/README.md`（实测数字在 PRD §13.8），但它是 10-22 快照，「下一步」第 1 条（按 card-and-report 做 M1/M2）已被决策账 10-26 两条取代（PR #27：卡片只给结论、细节进自托管面板 perf-lab.web.pkbsvc.com）。下一步以决策账最新条目为准。
- 部署通道：owner 个人账号在 Kuboard 只有 chat-test 权限、没有 kubeconfig；做法写在仓内 `deploy/README.md`「没有 kubectl 时」。往集群写资源前要 owner 在对话里明确授权（自动权限检查会拦），只动名字带 perf-lab 的资源。
- 该仓常有另一个会话并发改主工作树和 `scripts/notify.mjs`：checkout 前当场 status，见 [[check-worktree-status-right-before-checkout]]。
