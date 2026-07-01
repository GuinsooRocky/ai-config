# claude-config

我的 Claude Code 可复用配置（agents / skills / commands / hooks / workflows / design-spec / CLAUDE.md / RTK.md），git 直接跟踪 `~/.claude`，用 `.gitignore` 白名单排除掉隐私和运行时状态（对话历史、memory、session、cache、settings.json、mcp 凭据等）。

私有仓库。改了 skill/agent 之后 `git status` 能立刻看到 diff，随手 commit 就是增量备份；跟一次性静态快照（`~/Desktop/cc-memory/cc-防丢失`）不冲突，那份走 rsync 覆盖全部内容（含 memory/settings/mcp 密钥），换机器整机恢复用；这份是日常增量、只含可公开的配置本体。

## 已知限制

- `skills/xhs-writer` 是指向 `~/.agents/skills/khazix-writer` 的 symlink，git 按符号链接本身提交——换机器/克隆到新环境后这个链接会悬空，需要额外同步 `~/.agents/skills/khazix-writer` 的实际内容。
