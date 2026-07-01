---
name: project_worktree_dashboard
description: worktree-dashboard skill = cmm-go 的公开通用版；发公司 skillHub；受众全 Mac
metadata: 
  node_type: memory
  type: project
  originSessionId: a8014c45-8e3e-4672-a936-0c3296c4ac5c
---

`~/Desktop/worktree-dashboard/` 是 `cmm-go`（私有 OnlyChat 开工编排 skill）的**公开通用版**：抹掉 OnlyChat / 飞书 / 个人路径，泛化成 `myapp`/`feature-x`，MIT 授权，发到公司 skillHub 给同事用。2026-05-28 建。

**分发前提（已和用户确认 2026-05-29）**：
- 受众**全 Mac** → watchdog 用 macOS `footprint`、probe.sh 用 `pgrep -lf`，**非 Mac 不支持也不用管**（已决定）。
- 同事都有多 worktree 项目；飞书/文档抓取是外部能力，各自配自己的 MCP。

**两边同步**：新能力从 cmm-go 移植到 worktree-dashboard 时记得通用化 + 同步两份（同 [[feedback_personal_repo_handling]] 的双份同步思路）。已移植：**PRD 范围(scope)**（2026-05-29，SKILL.md §1/§4 + assets.md + features.example.ini，把飞书 `get_document`/50000 字泛化成 WebFetch/文档 MCP）。

**数据存储跟 skill 安装位置解耦**（用户最关心的点）：config = `~/.config/worktree-dashboard/features.ini`（3 级查找：env `$WORKTREE_DASHBOARD_CONFIG` → ~/.config → ./），state = `~/.local/state/worktree-dashboard/last-seen.json`（probe.sh 自动建+merge）。skillHub 装哪都不影响数据。

**分发 polish（已做 2026-05-29）**：① SKILL.md 加第 0 步「确认配置存在」——无 `features.ini` 时交互式引导建第一条；用户拒绝则**硬停**（输出 cp 模板后停住，绝不静默降级去列 worktree），不自动删（遵 [[feedback_no_auto_delete]]）；② cwd 兜底（`./features.ini`）在第 0 步做实，文档=行为一致。meta-check 95/A。
