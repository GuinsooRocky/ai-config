---
name: Branch naming convention
description: User's cross-project git branch naming rule — format, prefix, base branch, push restrictions
type: feedback
originSessionId: d25a49e4-d6a1-4ee3-a4a6-2de91d4f55aa
---
# 分支命名规则（跨所有项目通用）

## 格式

```
lengmo_YYYYMMDD_<type>[_<slug>]
```

- **前缀**：固定 `lengmo`（用户的跨平台花名，**不是** git username）
- **日期**：`YYYYMMDD`，例如 `20260414`
- **type**：必填，五选一
  - `dev` — 日常开发、杂项
  - `fix` — 修 bug
  - `feat` — 新功能
  - `refactor` — 重构
  - `chore` — 构建、配置、依赖、文档等杂活
- **slug**：可选，小写英文短描述，用 `-` 连接，例如 `login-modal` / `payment-retry`

## 示例

- `lengmo_20260414_dev`
- `lengmo_20260414_fix_login-modal`
- `lengmo_20260414_feat_voice-recording`
- `lengmo_20260415_refactor_auth-middleware`

## 基分支（从哪拉）

- **gitea 项目**（公司，zhanghao 身份）：默认从 `develop` 拉
- **github 项目**（个人，GuinsooRocky 身份）：默认从 `main`（没有则 `master`）拉
- 如果项目的默认分支不是上面说的，按项目 `HEAD` 指向的分支为准

## 冲突处理（同一天建多条分支）

1. 优先用不同 `slug` 区分（`..._fix_login-a`、`..._fix_login-b`）
2. 实在重名，追加 `_2` / `_3` 序号

## 禁止直接推送的分支

**永远不直接 push** 到：
- `main`
- `master`
- `release`
- `develop`

以上分支**必须走 PR / Merge Request 合入**。

### 例外：personal repo（含已脱离原 upstream 的 fork）

用户作为唯一维护者的个人仓库（如 `GuinsooRocky/sf-reader-all`）：
- **可以直接 push main**，无需 feature 分支
- 无团队、无 CI、无 review，feature 分支只是仪式
- Why：用户 2026-05-12 表态「personal 直接 push main 心智成本最低」+「不应该叫 fork 了 少了这个概念会少绕跟多」
- 适用判断：仓库只有用户自己 push、没有 pre-push hook、没有协作者

工作仓库（gitea / onlychat / 团队 github）**不在此例外内**，仍按上面禁推规则走。

## Why

用户是跨平台工作（github 个人 + gitea 公司），需要统一的分支命名规范：
1. 前缀统一用 `lengmo` 而非 git username，是因为两个平台用户名不同（github=GuinsooRocky，gitea=zhanghao），但希望团队内有统一的个人标识
2. 日期作为第二段方便时间回溯，不用查 git log
3. type 分类让分支名本身就能表达工作性质，减少上下文负担
4. 禁止直推主干是常规团队 workflow 的安全线（公司有 pre-push hook 会触发远程通知）

## How to apply

当用户说「新建分支」「建个分支」「开个分支」等类似表述时：
1. 读取今天日期（YYYYMMDD）
2. 询问或推断 type（如果从上下文明显，直接选；不明显时简短确认）
3. 询问是否需要 slug（如果用户没主动提，默认不加）
4. 用 `git checkout -b <branch>` 执行
5. 在执行前**先确认当前是否在对应的基分支**，如果不是，先 `git checkout develop && git pull` 再建

不要自作主张跳过规则。如果用户明确要求不同命名，按用户指定的来并提醒一次"这和保存的规则不同"。
