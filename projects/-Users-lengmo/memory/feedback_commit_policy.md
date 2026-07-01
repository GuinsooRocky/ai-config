---
name: Commit policy
description: Never commit or push unless user explicitly asks
type: feedback
originSessionId: 62222e4b-fd3d-4b5d-9f20-c6b5f75148fb
---
不要主动 commit 或 push 代码。只有用户明确说"commit"或"push"时才执行。

**例外（2026-06-17）：用户自己的个人项目（~/Desktop/my-code/*、GuinsooRocky/*）提不提交「无所谓」** —— 这类项目可自行判断提交（绿色里程碑存还原点），不必每次问。**push 仍不主动**。工作仓（onlychat/cmm、gitea）继续严守"不明说不提交"。

**Why:** 个人项目用户不在意提交节奏；工作仓才需要他亲自把关。

**How to apply:** 工作仓：改完只汇报，不 stage/commit/push。个人项目：可提交（功能分支，好的 message），但不 push；提交前仍按 [[feedback_git_porcelain_with_rtk]] 用 --porcelain 核对、确认无 .env/config.toml 等敏感文件入库。
