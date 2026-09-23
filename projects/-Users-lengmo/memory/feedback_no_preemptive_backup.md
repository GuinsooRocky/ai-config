---
name: feedback-no-preemptive-backup
description: 改代码前不要自作主张给工作区打备份包（tar/拷贝现场），owner 说不需要
metadata:
  node_type: memory
  type: feedback
  originSessionId: 2146a399-43c7-45a1-b786-107c3dd7d05e
  modified: 2026-09-23T04:57:45.170Z
---

改代码前别给工作区现场打 tar 包 / 拷贝备份当「保险」，直接改。

**Why:** 2026-09-23 onlychat-recmodel 接 proto 时，我在未提交的 78 个文件上改动前打了 `recmodel-wip-before-proto.tgz`，owner 回「不需要打包」。
**How to apply:** 可逆性靠 git（必要时临时 WIP commit，需 owner 同意）和「删文件一律 mv ~/.Trash」规则，不额外造备份物；汇报里也不用提备份。
