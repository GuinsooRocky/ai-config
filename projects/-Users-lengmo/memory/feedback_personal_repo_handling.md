---
name: feedback-personal-repo-handling
description: 个人 GitHub 仓库（GuinsooRocky/*）分支结构 + commit/push 政策；skill 文件同时存在于 ~/.claude/skills 和个人仓库时两份同步
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5dbe88c8-7418-4ccf-a475-d831b5de17a6
---

## 个人仓库 = 自有项目，不当 fork

用户从开源项目 fork/copy 出来的个人 GitHub 仓库（典型：`GuinsooRocky/sf-reader-all`），按**自有项目**对待：
- **不要**主动 `gh pr create --repo <upstream>` 给上游提 PR
- **不要**主动 `git fetch upstream` / 加 upstream remote
- 例外：用户明说"提 PR 给上游" / "拉一下 upstream"

**Why**：用户原话"其实不应该叫 fork 了 少了这个概念会少绕跟多"——心智模型当个人项目处理，不带"还在跟 upstream 互动"的暗示。

## 分支结构：无需 feature 分支，可直推 main（合并自 feedback_branch_naming.md）

个人仓库（用户是唯一维护者，无团队/无 CI/无 review，典型如 `GuinsooRocky/sf-reader-all`）**可以直接在 main 上改**，不必开 feature 分支走 PR——feature 分支只是仪式。适用判断：仓库只有用户自己 push、没有 pre-push hook、没有协作者。Why：用户 2026-05-12 表态「personal 直接 push main 心智成本最低」。

工作仓库（gitea / onlychat / 团队 github）**不在此例外内**，仍按 [[feedback_branch_naming]] 的禁推规则走。

## commit 可自行判断，push 仍要问（2026-07-01 澄清，见 [[feedback_commit_policy]]）

**提交（commit）**：个人项目可自行判断，不必每次问（绿色里程碑存还原点）。
**推送（push）**：默认**仍不主动**，除非用户明说"push"——这条修正了本文件早期"直接 push 不用问"的表述（已过时作废，被 2026-06-17 的 [[feedback_commit_policy]] 收紧覆盖）。
**例外**：DK 项目（`~/Desktop/my-code/dk`）用户已单独明说可直接 commit+push 不必每次问，见 [[feedback_dk_commit_push_freely]]（仅限该项目，不外溢到其他个人仓库）。

## Skill 改动：~/.claude/skills/ 默认只自用，例外要同步

改 `~/.claude/skills/<name>/SKILL.md` 时：
- **默认**：只动 `~/.claude/skills/` 那份
- **例外**：同 skill 也分发在自己的项目仓库里（如 `~/Desktop/my-code/sf-reader-all/skills/<name>/`）→ 两份同步改 → commit（push 仍按上面的规则，不主动）

**Why**：skill 迭代私人化，不外推社区；但项目仓库里那份要同步，否则下次 clone 拿到旧版。
**现状（2026-07-06 核实）**：这条约定**并未被强制执行**——sf-reader-all 仓的 video/analyzer 与全局版 diff 已不同步、archive skill 全局无对应。视为"软约定"：改动时想得起来就同步，别把"两份一致"当可依赖事实。
