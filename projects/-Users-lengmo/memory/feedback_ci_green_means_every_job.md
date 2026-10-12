---
name: feedback_ci_green_means_every_job
description: owner 要「main 全绿 / CI 变绿」= 本地跑齐 PR 全量 CI 的每个 job（audit、harness、Playwright 两套、supply-chain），不是只跑 code-gate；e2e 套件可能已在 main 上烂了几周没人看
metadata:
  type: feedback
---

owner 说「main 整体要 test 通过，CI 变绿不要红」时，判定面是 PR 触发的**全部** CI job，不只是本地 `code-gate.sh`。soliloquy 10-12 实测：code-gate 绿之后 PR 级 CI 还跑 `audit:production`（高危依赖）、`gate:harness`、`e2e:product-matrix`、`e2e`、supply-chain——其中两套 Playwright 在 main 上已经红了约一个月（e2e mock 没跟后端合同、spec 选择器停在旧 UI），没人注意是因为 main 普通 push 只跑 quick 闸。

**Why:** 10-12 我报「code-gate 四红全是 main 既有」就准备收工，owner 一句「main 要全绿」后才发现 Playwright 两套合计 95 红全是 main 原有；少看一眼 ci.yml 的 job 清单就会把半截活当做完。

**How to apply:**
- 接到「CI 绿」类目标先读 `.github/workflows/*.yml`，列出 PR 事件会跑的每个 job 与其 `if:`，逐个在本地跑等价命令（注意 Playwright 共用端口只能串行、mock server 进程在一轮 run 内不会热更新）。
- 判「是不是分支引入」用干净 origin/main worktree 跑同一 spec（`git worktree add` + `pnpm install --offline`），别靠猜。
- e2e 红的常见根因按顺序排查：mock 缺新 RPC/表（404）、种子缺新列被过滤（如 channel=eq.web）、spec 选择器 / 文案停在旧 UI、hover 才露出的控件要先 hover 或走键盘、CSS 契约探针漏装挪走的样式文件或新 token。
- 相关：[[feedback_done_needs_runtime_before_saying_so]]、[[feedback_not_ground_truth]]、[[project_soliloquy_bugscan_20261011]]
