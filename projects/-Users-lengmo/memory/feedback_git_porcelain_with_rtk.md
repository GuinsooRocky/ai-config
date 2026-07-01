---
name: feedback_git_porcelain_with_rtk
description: rtk 会摘要 git 输出藏文件；git 暂存/提交/push 前用 --porcelain 或 rtk proxy 拿原始真相
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a0882140-3486-4193-b2cc-22e554d1b1e1
---

rtk hook 会把 `git status` / `git diff --stat` 等输出做 token 摘要，**会漏列文件**。实测一次 `git diff --stat` 只显示 34 个文件，但 `git add -A` 时冒出未被列出的 `worldCard.router.ts`（真实改动）和 `proto` 子模块——差点把未察觉的改动一起 commit。

**Why:** 凭 rtk 摘要后的 diff/stat 决定 `git add -A` 范围会把看不见的改动一起提交，这是不可逆的对外操作。

**How to apply:** 涉及暂存/提交/push 前，git ground truth 一律走 `git -c core.pager=cat status --porcelain=v1`（拿全量文件列表）或 `rtk proxy git <cmd>`（跑未过滤的原始命令，如 `rtk proxy git show <sha> -- <path>` 拿完整 diff）。不要相信 rtk 摘要后的 `--stat` / diff 输出做范围判断。

关联 [[feedback_commit_policy]]
