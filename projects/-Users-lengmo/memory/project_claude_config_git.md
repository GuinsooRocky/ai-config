---
name: project-claude-config-git
description: ~/.claude 本体现在是私有 git 仓库 GuinsooRocky/claude-config，白名单 .gitignore 只跟踪可复用配置
metadata: 
  node_type: memory
  type: project
  originSessionId: 2389aa12-6873-4592-bd4d-1e4eacf9dc22
---

`~/.claude` 目录本身已 `git init` 并推到私有仓库 [GuinsooRocky/claude-config](https://github.com/GuinsooRocky/claude-config)（2026-07-01 建）。用白名单式 `.gitignore`（先 `/*` 忽略一切，再 `!` 放行）只跟踪：`agents/`、`skills/`、`commands/`、`hooks/`、`workflows/`、`design-spec/`、`CLAUDE.md`、`RTK.md`、`README.md`。

**Why**：想把 skill/agent/workflow 的迭代做成可 diff、可 commit 的版本历史，而不是每次手动 rsync 整份快照。真正排除不掉的只有机器专属的原始状态：`history.jsonl`、`projects/`（除 memory 外的原始会话 jsonl）、`sessions/`、`session-env/`、`telemetry/`、`cache/`、`stats-cache.json`。**`settings.json`/`mcp-servers.json`/`launchd/*.plist` 现在是跟踪的**（当天被后续 commit `7cd770c "Merge memory + sanitized settings/mcp/launchd into claude-config"` 并入白名单，经消毒确认无密钥泄漏后放行）——这与本记忆最初的说法相反，以此为准。

**How to apply**：
- 以后改 `~/.claude/skills|agents|commands|hooks|workflows|design-spec` 下的文件，可以提醒用户 `git status`/`commit` 做增量备份（他没主动要求就别自作主张 push，参考 [[feedback_commit_policy]]，但这是他自己的私有仓库不是工作仓，个人项目提交无所谓可自行判断）
- 跟静态整机快照 `~/Desktop/cc-memory/cc-防丢失`（rsync 全量，含 settings/mcp 密钥，换机器恢复用）是两回事，不要混淆或互相替代
- `skills/xhs-writer` 是指向 `~/.agents/skills/khazix-writer` 的 symlink，git 只存了链接本身，不是内容——克隆到新环境这个链接会悬空，呼应 [[feedback_personal_repo_handling]] 里 skill 双份同步的例外情形
- 已确认无密钥泄漏（推送前扫过 hooks/commands/workflows/design-spec，无 secret/token/api-key 硬编码）
