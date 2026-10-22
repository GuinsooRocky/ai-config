---
name: check-worktree-status-right-before-checkout
description: 切分支/checkout 前当场 git status；别的会话可能正在同一工作树改文件，几分钟前的「干净」不算数；要并行就开独立 worktree
metadata:
  node_type: memory
  type: feedback
  originSessionId: 316f106b-ada5-4a03-aab9-84d6c14172d2
  modified: 2026-10-22T07:24:47.307Z
---

切分支、checkout、stash 之前**当场**跑 `git status --short`，不信同一会话里几分钟前看到的「干净」。多个 Claude/Codex 会话常从 `~` 启动、用绝对路径改同一个工作树，主对话看不见它们。

**Why：** 2026-10-22 在 crushon-ai-perf-lab 主工作树上，开场 status 干净，十几分钟后直接 `git checkout` 到 docs 分支，结果带着别的会话正在改的 14 个文件（判据换血那批）一起切了过去；若对方那时 commit 就会落错分支。当场切回（checkout 会把未提交改动原样带回，diff --stat 前后一致）才没出事。

**How to apply：**
- checkout 紧挨着 status 跑，中间不隔别的长动作；status 非空且不是自己改的 → 不切，改开 `git worktree add <兄弟目录> <分支>` 做自己的活。
- 派子 agent 改仓时把工作目录指到独立 worktree，并在 prompt 里写明「绝不进入主工作树」。
- 一个分支只能被一个 worktree 占用；要在 worktree 里用的分支先确认主工作树没 checkout 它。
- 关联：[[session-id-by-content-not-mtime]]（同一台机多会话并发的另一种形状）。
