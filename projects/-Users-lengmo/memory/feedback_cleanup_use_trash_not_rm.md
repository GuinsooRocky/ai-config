---
name: feedback_cleanup_use_trash_not_rm
description: 帮用户「清理/删文件」时一律移到废纸篓，绝不用 rm（即使已获批准）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 61b57276-e6b0-43cc-b023-7a08ef231849
---

帮用户清理/删除任何文件时，**移到废纸篓**（macOS：`mv` 到 `~/.Trash/` 或用 `osascript` tell Finder to delete），**绝不用 `rm`**——即使用户已经勾选/批准了删除。

**Why:** 2026-05-22 帮用户清桌面散件，用 `rm -f` 直接删了 4 个文件，用户随后说"都是我要的"。`rm` 不进废纸篓、不可逆，只能靠翻 Claude Code 会话 jsonl（Read 快照 + 回放 Edit）救回 3 个文本文件；mp3 二进制彻底没了。若当初走废纸篓，一键还原即可。

**How to apply:**
- 清理操作默认 `mv "$f" ~/.Trash/`（重名加时间戳后缀），不要 `rm`
- 只有用户明确说"彻底删/不要进废纸篓"才用 rm
- 文本文件若已被 rm：会话 jsonl 里找 Write（原文）/ Edit（回放）/ Read 结果（删行号当 base），脚本重建（见本次 /tmp/recover*.py 思路）
- 关联 [[feedback_no_auto_delete]]
