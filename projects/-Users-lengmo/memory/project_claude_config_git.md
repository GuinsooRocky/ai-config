---
name: project-claude-config-git
description: ~/.claude 是私有仓库 GuinsooRocky/ai-config 的直接 checkout；cc-防丢失快照已删；Desktop/cc-memory/ai-config 是同仓中立副本
metadata: 
  node_type: memory
  type: project
  originSessionId: 2389aa12-6873-4592-bd4d-1e4eacf9dc22
  modified: 2026-07-30T08:04:48.832Z
---

`~/.claude` 目录本身是私有仓库 [GuinsooRocky/ai-config](https://github.com/GuinsooRocky/ai-config) 的直接 checkout（2026-07-01 建，原名 claude-config，2026-07-22 改名并重构成 Claude/Codex 共用能力源）。白名单式 `.gitignore` 只跟踪可复用配置 + memory + 消毒过的 settings/mcp/launchd。

**同一仓库有两份工作副本，别当成两个仓库**：
- `~/.claude` —— 运行时（旧式直接 checkout，本机继续用这种方式）
- `~/Desktop/cc-memory/ai-config` —— 中立副本，装着安装器体系（`profiles/` + `scripts/install-*.sh`，新机器走安装器投影，不再推荐直接 clone 成 `~/.claude`）；发布协议是 `./scripts/prepare-update.sh patch` 校验后手动 commit/push

两边都可能脏，同步顺序：各自 commit → `pull --rebase` → push（07-30 实操过一轮，分叉可解）。

**How to apply**：
- 改 `~/.claude/skills|agents|...` 后可提醒 `git status`/`commit` 增量备份；个人仓 commit 可自行判断，push 不主动（[[feedback_commit_policy]]）
- `skills/xhs-writer` 已从 symlink **实体化为真实文件**（2026-07-30），单一真相在 `~/.claude`；`~/.agents/skills/khazix-writer` 反向改成了指向它的 symlink——改内容只改 `~/.claude` 这份
- `skills/firecrawl` 是指向 `~/.agents` 的外部 symlink，已 gitignore 不入库（官方安装器管理，新机器重装即得）
- 静态整机快照 `~/Desktop/cc-memory/cc-防丢失` **已于 2026-07-30 删除**（进 `~/.Trash/cc-防丢失-20260730`），独有内容（xhs-writer 全套）已入库，不再存在"两套备份"
