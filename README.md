# ai-config

Claude Code 与 Codex 共用的一份能力源。默认安装 profile 只发布可迁移的规则、skills、agents、workflows、commands 和构建产物；安装时按当前机器拥有的运行环境分别投影，不要求仓库本身等于 `~/.claude` 或 `~/.codex`。

## 新机器安装

先登录需要使用的 Claude 或 Codex，并把私有仓库克隆到一个中立位置：

```bash
git clone git@github.com:GuinsooRocky/ai-config.git ~/ai-config
```

只有 Claude：

```bash
~/ai-config/scripts/install-claude.sh --dry-run
~/ai-config/scripts/install-claude.sh
```

只有 Codex：

```bash
~/ai-config/scripts/install-codex.sh --dry-run
~/ai-config/scripts/install-codex.sh
```

Claude 与 Codex 都有：

```bash
~/ai-config/scripts/install-all.sh --dry-run
~/ai-config/scripts/install-all.sh
```

Claude 安装器只管理 `~/.claude` 里的便携配置；Codex 安装器只管理 `~/.codex`。已有本机文件在覆盖前会备份，非 ai-config 管理的文件保持不动。默认都不安装 MCP、账号模型、OAuth、密钥、绝对路径权限或本机记忆服务，因此新机器不会因为缺少旧电脑依赖而反复报错。

Claude 的便携 `settings.json` 只包含仓库内真实存在的 hooks 与状态栏；Codex 默认只暴露高频能力，其余能力按任务读取。名称、路径或正文命中禁止规则的 skill 不会进入安装结果。

## 查看和获取更新

查看仓库版本，以及 Claude、Codex 各自是否真的有内容更新：

```bash
~/ai-config/scripts/status.sh
~/ai-config/scripts/status.sh claude
~/ai-config/scripts/status.sh codex
```

输出会区分：

- `已是最新`：版本和内容都一致。
- `内容已是最新，仅发布版本号不同`：这次发布没有改到当前运行环境，不必重复安装。
- `有内容更新`：当前环境的内容指纹发生了变化，应更新。

拉取并只更新当前拥有的环境：

```bash
~/ai-config/scripts/update-ai-config.sh claude
~/ai-config/scripts/update-ai-config.sh codex
~/ai-config/scripts/update-ai-config.sh all
```

更新使用 `git pull --rebase`。工作区存在未提交的已跟踪修改时会停止，不会替用户 stash、覆盖或合并。

## 发布自己的更新

仓库是唯一能力源。新增或修改共享能力时直接改仓库里的源文件，不把安装后的 `~/.claude`、`~/.codex` 当作第二份可双向覆盖的源。

常用源位置：

- Claude 全局便携规则：`profiles/CLAUDE.md`
- Claude 安全设置片段：`profiles/claude-settings.json`
- 共享能力：根目录的 `skills/`、`agents/`、`commands/`、`workflows/`、`hooks/`
- Codex 暴露范围：`codex/capabilities.json`

根目录旧 `settings.json`、旧 `CLAUDE.md` 和机器态备份不属于默认安装 profile；修改它们不会悄悄覆盖其他机器。

准备一次更新：

```bash
cd ~/ai-config
./scripts/prepare-update.sh patch
```

它会在共享 Claude 能力发生变化时重建 Codex 按需能力包，更新插件 cachebuster，将 ai-config 版本按 semver 升级，并执行内容指纹、秘密扫描和 profile 校验。最后只列出待发布文件，不会 stage、commit 或 push。

确认差异后再自行提交和推送：

```bash
git diff
git status
```

`ai-config.json` 保存人可读版本号；每个安装环境的回执保存在 `~/.config/ai-config/receipts/`。回执同时记录发布版本、Git commit 与该 profile 的 SHA-256 内容指纹，所以即使忘记升级版本号，真实内容变化仍能被发现。

## 不同步的内容

Claude/Codex 登录状态、OAuth、真实密钥、原始会话、SQLite 数据库、缓存和遥测不进入安装 profile。新机器仍需单独登录并授权需要的外部服务。

旧的“直接 clone 成 `~/.claude`”方式不再推荐；它会把源码仓库、运行时数据和单一产品目录混在一起，难以安全更新。
