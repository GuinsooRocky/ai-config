---
name: feedback-memory-experiment-vs-adopted
description: "memory 里写过的\"升级/迁移实施记录\"≠项目已采用；判断技术栈先看 lockfile/package.json，再决定是否提及历史"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 720b3b9a-11ec-41d1-9ca7-11f8e445530d
---

memory 中存在 "X 升级实施记录" 类条目时，不能默认项目已采用 X。这些往往是用户本地的实验性分支，**没有推也没有合**。

**Why:** 2026-05-14 在 onlychat-world-book worktree 起 dev，pnpm install 报 node_modules missing。我看见 [[project_onlychat]] 里关联的 `11-bun升级实施记录.md`，就把 bun 当作"主仓已升级"的事实，给用户摆了一个"pnpm vs bun rebase vs symlink"三选一的问题。实际上 worktree 只有 `pnpm-lock.yaml`，`package.json` engines/packageManager 也只写 pnpm — lockfile 已经把答案写死了。用户回："那个只是我本地的一个测试，还没有推。"

**How to apply:**
- 判断项目用什么包管理器/构建工具的当下事实，**唯一可信源是当前 worktree 的 lockfile + package.json**，不是 memory 里的实施记录。
- memory 里 "升级实施记录 / 迁移记录" 类条目默认按 **个人实验分支** 对待；要确认是否合主线，去 `git log origin/develop` 或问用户。
- 如果 lockfile 已经回答了问题，就直接执行；不要为了显得"我记得这事"而把无关历史塞进选项。
- 关联记忆：[[project_onlychat]] 里提到的 11 号文档是实验记录，不是已落地状态。
