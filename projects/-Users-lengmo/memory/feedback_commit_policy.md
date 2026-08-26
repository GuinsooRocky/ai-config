---
name: Commit policy
description: 提交/推送/发版/分支命名 全政策——仓×动作一张表；工作仓不明说不提交，个人仓可自行判断，DK 与 soliloquy 已放开 push
type: feedback
originSessionId: 62222e4b-fd3d-4b5d-9f20-c6b5f75148fb
modified: 2026-08-26T07:14:58.420Z
---

# 提交与发版政策（仓 × 动作）

| 仓 | commit | push | 发版/部署 |
|---|---|---|---|
| 工作仓（onlychat/cmm、gitea） | 不明说不提交 | 绝不主动 | 不适用（走团队流程） |
| 个人仓（~/Desktop/my-code/*、GuinsooRocky/*） | 可自行判断（绿色里程碑存还原点） | 默认不主动，用户明说才推 | — |
| DK（~/Desktop/my-code/dk，remote=GuinsooRocky/dk） | 验证过就直接 commit | 直接 push，不必每次问（2026-06-18 明说，仅限本项目） | — |
| soliloquy（~/Desktop/loop_project/soliloquy*） | 自行判断 | 到 main 都可自行，做完汇报（2026-08-03 拍板） | 自己按（见下） |

**通用底线（所有仓）**：提交前核对全量改动（`git status --porcelain=v1`）；绝不提交 .env/config.toml/.build/dist/db；不是我改的文件先看 diff 再决定是否一起提。

## 发版（soliloquy，2026-08-07 拍板）

| 场景 | 处置 |
|---|---|
| 把**已经公开**的东西换个版本（`pnpm release:web` / `pnpm release:vps`） | 自己按，按完汇报 |
| **第一次**把新东西曝出去（新域名/新公开页/应用商店/对外公告） | 停，等点头 |
| 真钱、生产库不可逆迁移 | 停，等点头 |

**Why:** 两条发布线都是蓝绿槽（备用槽先起、健康检查过才切、失败自动回滚、旧版秒级可退），换版本不是不可逆动作；owner 不想当自己产品的最后一公里。**但自动回滚保的是「服务器答得对不对」，不是「页面对不对」**——内容错的版本机器不拦，发版不豁免走查。项目内真相在 soliloquy 的 CLAUDE.md/AGENTS.md 提交约定节。

## 分支命名（跨项目通用）

格式 `lengmo_YYYYMMDD_<type>[_<slug>]`——前缀固定 `lengmo`（跨平台花名，不是 git username：github=GuinsooRocky、gitea=zhanghao）；type 五选一 `dev/fix/feat/refactor/chore`；slug 可选小写英文 `-` 连接。例：`lengmo_20260414_fix_login-modal`。同日重名先换 slug，再不行加 `_2`。

- 基分支：gitea 从 `develop` 拉；github 个人仓从 `main`；项目默认分支不同则按 `HEAD`
- **main/master/release/develop 永不直接 push，必须走 PR**（公司有 pre-push hook 会触发远程通知）
- 例外：个人仓（唯一维护者、无团队/CI/review）可直接在 main 上改，不必开 feature 分支——feature 分支在那只是仪式（2026-05-12 表态「personal 直接 push main 心智成本最低」）
- 建分支前先确认在对应基分支上，不是就先 `git checkout develop && git pull`

## 个人仓的身份认定

从开源 fork/copy 出来的个人仓（典型 `GuinsooRocky/sf-reader-all`）按**自有项目**对待：不主动给上游提 PR、不主动加 upstream remote，用户明说才做——用户原话"其实不应该叫 fork 了 少了这个概念会少绕跟多"。

**Skill 双份同步（软约定）**：改 `~/.claude/skills/<name>/` 时若同 skill 也分发在个人项目仓里（如 sf-reader-all/skills/），两份同步改再 commit。2026-07-06 核实这条并未被强制执行（已有 diff 不同步），改动时想得起来就同步，别把"两份一致"当可依赖事实。

参见 [[user_git_identity]]、[[feedback_rebase_over_merge]]。
