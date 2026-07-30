---
name: feedback_dk_commit_push_freely
description: dk(DK，原 chat-cc-bot) 项目可直接 commit+push 不必每次问
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1101eeb0-f88c-4cd6-935b-b4cbed2ba064
---

在 `~/Desktop/my-code/dk`（DK，个人项目，2026-06-18 从 chat-cc-bot 改名；remote=github.com/GuinsooRocky/dk）改完验证通过后**直接 commit + push**，不用每次征求同意。

**Why:** 用户明说"直接 commit+push 就好，省得你每次提"（2026-06-18）。个人自有仓，节奏要快。

**How to apply:** 验证过（smoke/单测/能跑）就分逻辑单元 commit + push origin HEAD。仍守：never commit .env/config.toml/.build/dist/db；提交前核对全量改动（`git status --porcelain=v1`）；不是我改的文件先看 diff 再决定是否一起提。此授权**仅限本项目**，不外溢到工作仓（见 [[feedback_commit_policy]] 全局仍是 push 不主动）。
