---
name: feedback_verify_subagent_patch_against_worktree
description: 收子 agent 的 worktree 改动后必须逐文件 diff 回它的树，git apply --3way 会静默吞 hunk
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b8a60c02-7961-46ec-8eb1-35465d5a15b7
  modified: 2026-08-06T22:13:17.754Z
---

从子 agent 的 worktree 收改动时，`git apply --3way` 打的补丁**会静默丢掉整个 hunk**——只要我自己在同一文件的邻近行也改过（哪怕改的是注释）。它打印 `Falling back to direct application...` 就走了，退码 0，看起来完全成功。

**收完必须逐文件比回去**：

```bash
WT=<agent worktree>
for f in $(git -C "$WT" diff --cached -M --name-only); do
  [ -f "$f" ] && [ -f "$WT/$f" ] && { diff -q "$f" "$WT/$f" >/dev/null || echo "≠ $f"; }
done
```

**Why**：2026-08-07 soliloquy 搬聊天页，agent 修了一条登记指向（consumer_drift），我在同一文件改过注释 → 三方合并吞了那笔 → 我提交并以为绿，干净树跑闸才炸出来。子 agent 报告里明写「已修」，我也确实把补丁应用成功了，两边都没撒谎，东西就是没进来。

**连带**：闸也别在主目录跑。主目录常混着别的会话的未提交改动，会掩盖真红——同一个提交，混合树全绿，干净 worktree 红。落主线前在 `git worktree add --detach <sha>` 的干净树上跑一遍。

相关：[[feedback_delegate_impl_to_opus_subagent]]、[[feedback_truncated_output_is_not_ground_truth]]
