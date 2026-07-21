# Claude ↔ Codex Continuity

Lengmo 的 Claude Code + Codex CLI 私有配置仓库。目标是让两边共享 skills、agents、workflows、commands、个人规则和安全的 MCP 定义，同时不把凭证、OAuth 状态、会话日志或 SQLite 记忆库提交进 Git。

## 包含什么

- `claude/`：Claude 的 skills、agents、workflows、commands、hooks、设计规范与精选 Markdown 记忆。
- `plugins/claude-continuity/`：Codex 可安装插件；将 Claude agent/workflow/command 转成 Codex 可触发的 skills。
- `shared/AGENTS.md`：Codex 全局个人规则。
- `scripts/`：快照、安装和秘密扫描。

原始 `~/.claude.json`、`~/.claude/settings.json`、MCP 明文密钥、`memory.db` 和会话 `.jsonl` 永不入库。Lark MCP 在运行时从本机现有 Claude 配置读取凭证。

## 新电脑恢复

```bash
git clone git@github.com:GuinsooRocky/ai-config.git ~/.claude
~/.claude/codex/scripts/verify-no-secrets.sh
~/.claude/codex/scripts/install-codex.sh
```

Codex 安装脚本会先备份目标文件，再安装共享规则、marketplace、插件和 Lark 凭证桥；不会把真实凭证写进 Git。

## 日常同步

```bash
~/.claude/codex/scripts/snapshot.sh
git -C ~/.claude status
```

`snapshot.sh` 会直接读取同仓库的 Claude 源文件并重建 Codex skills；旧版插件 skills 会先备份到 `~/.ai-continuity-backups/`。确认 diff 和秘密扫描通过后再提交。本仓库保持 private。
