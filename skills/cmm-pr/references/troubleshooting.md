# cmm-pr — 故障排查（完整版）

> 从 SKILL.md 拆出的按需加载细节。文中 §8.x 见 references/conflict-resolution.md，§2/§7 见主文件。

## 故障排查

- `tea: command not found` → `brew install tea`
- `tea pr create` 401 → token 过期 / 权限不够 → 重新 `tea login add`
- **commitlint 拒 subject**：草稿已强制全小写；若 user 改 msg 手抖加大写词（Figma / NotesSearchBar 等），重新 Edit 重提
- **tea CLI flag 漂移**：见 §7，必须运行时 `--help` 探测，别按"备忘"硬拼（如 `--head`）。**`--draft` 不是漂移——Gitea 没有这个 flag**；草稿走标题 `WIP:` 前缀（§7），别再让用户手动 Convert to draft
- **tea `path segment [0] is empty`**：SSH remote 解析不出 owner/repo → §7 默认带 `--repo`（从 `git config remote.origin.url` 解析）
- 远端没分支 → `git push -u` 一并建好
- PR 已存在同分支 → tea 报错；网页关旧 PR 或继续干旧 PR
- code-review 跑完 user 改了文件 → 跑后再 `git status`，dirty 时停下让 user 决定 amend / 新 commit / 撤回
- `git pull --rebase` 冲突 → 进 §8.2 解冲突子流程（不要让 user 自己手撸）
- **rebase --continue 后 staged 区出现 submodule/lockfile** → 这是 commit replay 把高敏感路径再次带出来，**必须重跑 §2 高敏感扫描**再继续 push
- **force-with-lease 拒绝**：远端有别人 commit → 不要自动升级到 `--force`，停下让 user 排查（可能是另一个 worktree 已 push、多人共用分支等）
- **链接式 worktree rebase 时凭空冒出别处分支的内容**（atom/测试/WIP，不在任何 commit、不是 user 改的）→ 是 Husky/lint-staged 在 `rebase --continue` 时把陈旧 stash 灌进工作区。**根治：§8.2 全程 `-c core.hooksPath=/dev/null`**。已发生就 abort → 关钩子重跑；残留 untracked 文件挪 `~/.Trash`（别 rm），tracked 的幽灵改动 abort 会清掉。（2026-06-01 PR #1155，单次坑 14min）
