---
name: feedback_path_add_does_not_scope_commit
description: 逐路径 git add 挡不住 commit——commit 提交的是整个索引，别的会话预先 stage 的文件会被一起扫走
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f18ee7e9-ae2f-490d-85fe-1b432f5ffa13
  modified: 2026-08-16T17:14:24.551Z
---

**逐路径 `git add <file>` 只控制"我加了什么"，控制不了"commit 提交什么"**——`git commit` 提交的是**整个索引**。并发会话里，如果别人已经把文件 stage 了（哪怕你一个字节没碰），你的 commit 会把它一起扫进去。

**Why**：多会话并发写同一个仓是本机常态（codex 跑批线、别的 Claude session、迁移 agent 同时在动 soliloquy/eval-arena）。"我只 add 了自己的文件"是安全错觉——2026-08-17 迁移批 6 返修时，一次 commit 就把另一个会话预先 stage 的 `lab-oc-content-snapshot.ts` 扫了进去。

**How to apply**：
- 并发仓里提交前先看 `git diff --cached --name-only`，不是只看自己 add 了什么
- 只想提交自己那几个文件：`git commit -- <path>...`（pathspec 形式，绕过索引其余部分），或先 `git stash push --staged` 挪走别人的
- 扫进去了怎么复原：`git rm --cached <file>` 撤回 + **原样重新 stage**（别人的 status 要完全复位，磁盘零改动）
- 相关：[[feedback_verify_subagent_patch_against_worktree]]（闸别在混着别的会话改动的主目录跑）
