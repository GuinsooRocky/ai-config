---
name: Git dual identity setup
description: User has two git identities (work gitea + personal github) with auto-switching by directory via includeIf
type: user
originSessionId: d25a49e4-d6a1-4ee3-a4a6-2de91d4f55aa
---
# 用户的双 git 身份

## 身份映射

| 场景 | 平台 | git username | git email | SSH key |
|---|---|---|---|---|
| 个人 | GitHub | GuinsooRocky | guinsoo@163.com | `~/.ssh/id_ed25519` |
| 公司 | Gitea (gitea.peekaboo.tech) | zhanghao | zhanghao@peekaboogames.com | `~/.ssh/id_ed25519_work` |

**注意**：`lengmo` 只是用户的跨平台花名 / 分支前缀，**不是任何平台的 git username**。

## 自动切换机制（已配置）

`~/.gitconfig` 用 includeIf 规则按目录分派：

```gitconfig
[user]
    name = GuinsooRocky
    email = guinsoo@163.com

[includeIf "gitdir:~/Desktop/cmm/"]
    path = ~/.gitconfig-work
```

- 默认身份 = 个人 GuinsooRocky
- `~/Desktop/cmm/` 下的仓库 → 自动切成公司 zhanghao
- `~/Desktop/cmm/` 之外的其他位置 → 保持个人身份（包括 `~/Desktop/My-Daily-Push/` 等个人项目）

`~/.ssh/config` 按 host 路由 SSH key：
- `github.com` → `~/.ssh/id_ed25519`
- `gitea.peekaboo.tech` → `~/.ssh/id_ed25519_work`

HTTPS 凭证用 osxkeychain 缓存。

## 对 Claude 的影响

- 在 `~/Desktop/cmm/` 下的任何 git 操作，无需手动 `git config user.xxx`，身份会自动正确
- 如果用户想给 `~/Desktop/cmm/` 下的**个人学习笔记**（如 `onlychat-World-Path/`）做版本管理，需要在该子目录内**显式覆盖**身份为 GuinsooRocky，或给它单独加一条 includeIf 例外。否则 commit 作者会错打成公司身份
- gitea HTTPS 认证可能因 2FA/token 策略失败，**优先使用 SSH URL**（`git@gitea.peekaboo.tech:...`）clone 和操作
- gitea 仓库大，首次 clone 建议用 `--depth 1` 浅克隆，需要历史时再 `git fetch --unshallow`
