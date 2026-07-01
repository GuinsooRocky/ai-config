# claude-config

我的 Claude Code 完整可迁移配置，git 直接跟踪 `~/.claude`，用 `.gitignore` 白名单放行：

- 可复用配置：`agents/` `skills/` `commands/` `hooks/` `workflows/` `design-spec/` `CLAUDE.md` `RTK.md`
- 机器态配置（已消毒）：`settings.json`、`mcp-servers.json`（lark app-secret 已替换成 `${LARK_APP_SECRET}` 占位符，真实值不进 git）、`launchd/`（3 个定时任务 plist）
- `projects/-Users-lengmo/memory/`：auto memory 全部记忆文件

私有仓库。改了 skill/agent/memory 之后 `git status` 能立刻看到 diff，随手 commit 就是增量备份。

**排除不了、也不该进 git 的**：`history.jsonl` / `sessions/` / `session-env/`（未经审查的原始对话全文，可能夹杂任何贴过的内容）、`telemetry/` / `cache/` / `stats-cache.json`（纯运行时数据，可自动重建）。这部分只能靠 Time Machine 之类的整机备份兜底，不做 git 化。

## 换机器恢复

```bash
git clone git@github.com:GuinsooRocky/claude-config.git ~/.claude
# 1. lark app-secret 手动替换回真实值（自己的密码管理器里查）
# 2. settings.json 里的绝对路径（hook 脚本等）核对一遍
# 3. launchd/*.plist 拷到 ~/Library/LaunchAgents/ 再 launchctl load
```

## 已知限制

- `skills/xhs-writer` 是指向 `~/.agents/skills/khazix-writer` 的 symlink，git 按符号链接本身提交——换机器/克隆到新环境后这个链接会悬空，需要额外同步 `~/.agents/skills/khazix-writer` 的实际内容。
