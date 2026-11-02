---
name: crushon-ai-perf-lab
description: 工作仓 cmm/crushon-ai-perf-lab（onlychat beta 核心 5 页性能合成测量）；规则真相=仓根 CLAUDE.md + docs/README.md；进度现读决策账最新条目；出卡方案 10-26 已定（卡片只给结论+自托管面板），card-and-report.md 已被取代；现阶段问「还有什么要搞」= 只答技术链路（测得更快、更准、测法更优），不提跑通/部署/pre/等 devops 等流程事项，汇报写成大白话文章，不用表格列表；小改（卡片文案、面板样式）合 main 不等 tests/all.mjs 全量，跑相关测试+反面验证就合，owner 说「直接合」就当场开 PR 自合
metadata:
  node_type: memory
  type: project
  originSessionId: c6ff384f-01f4-40b3-9442-38839626ddce
  modified: 2026-11-02T07:52:48.872Z
---

- 仓：`~/Desktop/cmm/crushon-ai-perf-lab`（gitea `peekaboo/crushon-ai-perf-lab`，工作仓：owner 不明说不 commit / push / 开 PR）。PR 目标手动选 `main`（gitea 默认分支仍指旧 skeleton，切换需管理员）。
- 接任务先读仓根 `CLAUDE.md` 和 `docs/README.md`；已定在 `docs/decisions.md`，未定在 `docs/open-questions.md`。别靠记忆复述项目口径。
- 集群现状看 `docs/cluster-2026-10-22/README.md`（实测数字在 PRD §13.8），但它是 10-22 快照，「下一步」第 1 条（按 card-and-report 做 M1/M2）已被决策账 10-26 两条取代（PR #27：卡片只给结论、细节进自托管面板 perf-lab.web.pkbsvc.com）。下一步以决策账最新条目为准。
- 部署通道：owner 个人账号在 Kuboard 只有 chat-test 权限、没有 kubeconfig；做法写在仓内 `deploy/README.md`「没有 kubectl 时」。往集群写资源前要 owner 在对话里明确授权（自动权限检查会拦），只动名字带 perf-lab 的资源。
- 该仓常有另一个会话并发改主工作树和 `scripts/notify.mjs`：checkout 前当场 status，见 [[feedback_git_pitfalls]]。


补充：集群测量机 10-22 已在 chat-test 跑通测量；进度与下一步现读决策账最新条目；出卡方案 10-26 已定（PR #27 卡片+自托管面板），card-and-report.md 已作废

## 汇报只讲技术链路

owner 问 perf-lab「还有哪些需要搞」时，要的是测量技术本身的改进：怎么测得更快、更准、测的方案怎么更优。跑通链路、上线步骤、测 pre、等 devops 放行、谁去 Kuboard 操作这类流程事项，现阶段一律不提。汇报写成大白话文章，不用表格和列表。

**Why:** 10-23 我把「项目还剩什么」答成了上线顺序和等人清单，owner 原话：「不不不 你不要管跑通 也不要管 pre 这种流程上的你也没办法现在解决 就不要在这个阶段跟我提 我需要你回答的是技术链路上的 比如更快 更准 测的方案更优」。

「更快」指整轮本身变快：owner 验证要跑整轮，少跑几格、只验单格链路、拿增量轮代替都算治标，不当提速方案提（10-26 原话「我是要跑整轮验证 1是治标不治本 所以2也不对」）。

问「性能有没有问题 / 核心看什么」要的是几行最终结论（有没有变慢、绝对水平、盯哪几个），不是指标全表加调研逐份点评（10-26 原话「我要个最终结论 不是你这么长篇大论」）。评出「没用」的文档要顺带给处置建议，别只评不处理（同日「没用为啥留着」）。

「验证下合理性 / 审一下这几批」同样只要每批一句「合理 / 有问题 + 最要紧的一条」，不要表格、F 编号、行号、报告路径、待拍清单——子 agent 的长报告留在 scratchpad，主对话只出结论（10-28 三批审查回了一张表加三个报告路径，原话「不不不 我需要结论 而不是报告」）。

「持续思考怎么优化」要一条从目标和实测推出来的主线，不是零碎清单（10-30 原话「持续思考如何进行优化 而不是找那种零碎的甚至做出了无意义的」）。每个点都换算成两个数：哪几格能看出的最小变化从多少变到多少（对照一期 20% 验收线），整轮多或少几分钟；说不出这两个数的不提。

**How to apply:** 每条建议都要落到仓里的实测数字或原始数据（PRD §13、results/ 原始 browsertime JSON），说清现在哪里不好、怎么改、怎么用调试模式低成本验证。先查决策账和归因文档的「不建议」，已经否掉的别再提，见 [[record-owner-decisions-and-check-before-listing-gaps]]。

## 小改不等全量就合

crushon-ai-perf-lab 的仓内 CLAUDE.md 写着「提 PR 前跑 `node tests/all.mjs`」，但 owner 当次说合时，卡片文案、面板样式这类小改不等全量（约 150 秒）：跑改到的那个测试文件（如 `node tests/notify.mjs`）＋换回 main 代码验反面，就开 PR 当场自合。

**Why:** 10-29 卡片加「内容变多」那行时，我在后台跑全量、说「跑完再合」，owner 回「用不了全量检查吧。。。 直接合」。当天还说过「直接合吧 都不用开pr了」——仓规不许直推 main，所以照旧开 PR 但当场自合，不等他点。

**How to apply:** 只改 `scripts/notify.mjs`、`scripts/panel.mjs` 文案或样式这类时，PR 描述写清跑了哪个测试文件、全量没跑（或跑完了就照实写）。改到比较、测量链路、登记表的仍按仓规跑全量。全局「验多少」规则见 ~/.claude/CLAUDE.md；相关 [[feedback_merge_without_owner_clickthrough]]。
