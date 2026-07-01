---
name: Prefer rebase over merge
description: User prefers git rebase over git merge for branch sync, to keep git graph linear
type: feedback
originSessionId: 1a7a3fd9-e45b-4340-926e-d5b7cb46ae29
---
用 `git rebase origin/<base>` 而不是 `git merge origin/<base>` 来同步分支。

**Why:** git graph 更好看，history 是线性的，不会产生多余的 merge commit。

**How to apply:** 每次需要把上游变更同步进功能分支时，默认用 rebase 而不是 merge。
