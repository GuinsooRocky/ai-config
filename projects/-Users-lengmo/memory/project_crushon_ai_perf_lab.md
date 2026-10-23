---
name: crushon-ai-perf-lab
description: 工作仓 cmm/crushon-ai-perf-lab（onlychat beta 首页性能合成测量）；规则真相=仓根 CLAUDE.md + docs/README.md；集群测量机已在 dev-eks-ai-new/chat-test 跑通测量（10-22），进度与下一步=docs/cluster-2026-10-22/README.md，出卡方案=docs/card-and-report.md（待拍板）
metadata:
  node_type: memory
  type: project
  originSessionId: c6ff384f-01f4-40b3-9442-38839626ddce
  modified: 2026-10-23T03:52:17.413Z
---

- 仓：`~/Desktop/cmm/crushon-ai-perf-lab`（gitea `peekaboo/crushon-ai-perf-lab`，工作仓：owner 不明说不 commit / push / 开 PR）。PR 目标手动选 `main`（gitea 默认分支仍指旧 skeleton，切换需管理员）。
- 接任务先读仓根 `CLAUDE.md` 和 `docs/README.md`；已定在 `docs/decisions.md`，未定在 `docs/open-questions.md`。别靠记忆复述项目口径。
- 集群现状与下一步只看 `docs/cluster-2026-10-22/README.md`（实测数字在 PRD §13.8）；跑完出卡片/详情页的方案是 `docs/card-and-report.md`（M1–M4，§7 四项待 owner 拍板）。10-22 这批文档已随 PR #16 合入。10-23 回收了全部 worktree，只剩 `-gaps`（direction README §4.5 覆盖缺口表，没提交，等 owner 定进不进 main）和本地分支 `lengmo_20261022_feat_build-report`（1014518「一个 build 一份报告」，没进 main，远端也没有）。
- 部署通道：owner 个人账号在 Kuboard 只有 chat-test 权限、没有 kubeconfig；做法写在仓内 `deploy/README.md`「没有 kubectl 时」。往集群写资源前要 owner 在对话里明确授权（自动权限检查会拦），只动名字带 perf-lab 的资源。
- 该仓常有另一个会话并发改主工作树和 `scripts/notify.mjs`：checkout 前当场 status，见 [[check-worktree-status-right-before-checkout]]。
