# AI Config for Codex

这套目录把同一份能力源发布给 Codex。目标是让 Claude 与 Codex 共享 skills、agents、workflows、commands 和个人规则，同时让 Codex-only 机器不依赖 `~/.claude`。

## 加载模型

- `capabilities.json`：定义默认 profile、直接暴露的能力、描述预算和禁止迁移的内容。
- `plugins/claude-continuity/skills/`：高频通用能力，进入 Codex 初始 skill 列表。
- `plugins/claude-continuity/assets/capabilities/`：其余可移植能力，不占初始 skill 列表，由 `ai-capability-router` 按任务查找。
- `shared/AGENTS.md`：Codex 全局个人规则。
- `scripts/`：构建、安装、验证和秘密扫描。

默认 `core` profile 会校验直接暴露的 description 总量，不让单体插件再次挤爆 Codex 的 skills context budget。`full` profile 只用于兼容性测试，不建议日常安装。

MCP 不再从插件 manifest 自动启动。这样没有 Figma、Lark 或本地项目服务的机器不会在启动时反复报连接错误。需要本地集成时显式使用 `--with-detected-mcp`，安装器只添加当时依赖完整、能够探测到的服务。

原始 `~/.claude.json`、MCP 明文密钥、OAuth 状态、SQLite 数据库和会话 `.jsonl` 永不入库。

## Codex-only 机器安装

```bash
git clone git@github.com:GuinsooRocky/ai-config.git ~/ai-config
~/ai-config/scripts/install-codex.sh --dry-run
~/ai-config/scripts/install-codex.sh
```

安装脚本会先验证秘密扫描和 capability profile，再备份并安装 `AGENTS.md`、marketplace 与便携核心插件。默认安装不会读取或修改本机 Claude 配置。

只有明确需要且本机依赖已经存在时才安装本地 MCP：

```bash
~/ai-config/codex/scripts/install-codex.sh --with-detected-mcp
```

更新另一台机器：

```bash
~/ai-config/scripts/update-ai-config.sh codex
```

## 能力源更新

在维护能力源的机器上优先运行根目录发布检查：

```bash
cd /path/to/ai-config
./scripts/prepare-update.sh patch
```

当共享 Claude 能力发生变化时，它会调用现有 snapshot/rebuild 流程，把旧版插件放进 `~/.ai-continuity-backups/`，生成核心能力与按需目录，更新插件 cachebuster，然后执行 profile 校验和秘密扫描。它只准备版本和工作树，不会 stage、commit 或 push。
