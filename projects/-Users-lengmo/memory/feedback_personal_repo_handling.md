---
name: feedback-personal-repo-handling
description: 个人 GitHub 仓库（GuinsooRocky/*）按自有项目处理；skill 文件同时存在于 ~/.claude/skills 和个人仓库时两份同步
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5dbe88c8-7418-4ccf-a475-d831b5de17a6
---

## 个人仓库 = 自有项目，不当 fork

用户从开源项目 fork/copy 出来的个人 GitHub 仓库（典型：`GuinsooRocky/sf-reader-all`），按**自有项目**对待：
- 代码改完直接 commit + push 到自己 origin（personal repo 可直推 main）
- **不要**主动 `gh pr create --repo <upstream>` 给上游提 PR
- **不要**主动 `git fetch upstream` / 加 upstream remote
- 例外：用户明说"提 PR 给上游" / "拉一下 upstream"

**Why**：用户原话"其实不应该叫 fork 了 少了这个概念会少绕跟多"——心智模型当个人项目处理，不带"还在跟 upstream 互动"的暗示。

## Skill 改动：~/.claude/skills/ 默认只自用，例外要同步

改 `~/.claude/skills/<name>/SKILL.md` 时：
- **默认**：只动 `~/.claude/skills/` 那份
- **例外**：同 skill 也分发在自己的项目仓库里（如 `~/Desktop/my-code/sf-reader-all/skills/<name>/`）→ 两份同步改 → commit → push（personal repo 直推 main 可）

**Why**：skill 迭代私人化，不外推社区；但项目仓库里那份要同步，否则下次 clone 拿到旧版。
