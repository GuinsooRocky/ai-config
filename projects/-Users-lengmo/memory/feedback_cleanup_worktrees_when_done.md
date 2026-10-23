---
name: feedback_cleanup_worktrees_when_done
description: 一批活合进 main 就当场回收 worktree（兄弟目录 + .claude/worktrees 子 agent 的）、合并过的本地分支、空挂的 Monitor；先按内容核再 mv 进废纸篓
metadata:
  node_type: memory
  type: feedback
  originSessionId: 62ab6c34-8f99-43bc-85ab-728b379481b6
  modified: 2026-10-23T03:52:13.339Z
---

一批活合进 main 后，同一个会话里就把现场收掉，别留给 owner 来提醒。要收的有四样：兄弟 worktree（`<仓>-xxx`）、`.claude/worktrees/agent-*`（Agent 隔离自动建的，最容易漏）、已合并的本地分支、盯日志的 `tail -F | grep` Monitor（跑完不会自己退出，会以 PPID=1 一直占着 cwd）。

**Why:** 2026-10-23 perf-lab 一天开出 22 个 worktree（owner 只看到兄弟目录里的 5 个，另有 15 个藏在 `.claude/worktrees/`），共约 2.5G，还有 2 个前一晚的 Monitor 挂了 14 小时。owner 原话「这个项目的worktree 做完要清理的哇」。

**How to apply:**
- 判能不能清要按内容核，别看「分支有没有合并」：squash/rebase 会换 hash，`git cherry -v origin/main <b>` 加上「main 里有同标题提交」两样都不中才算独有。未提交改动逐文件和 origin/main 比对，被 gitignore 的 `results/` 也要看一眼。
- 删除方式是 `mv` 到 `~/.Trash/<仓>-wt-<名>-<日期>`，然后 `git worktree prune`。不用 `git worktree remove --force`，它是真删（见全局 CLAUDE.md）。分支用 `branch -D` 删时把 SHA 打出来留底。
- 先 `lsof | grep <路径>` 看有没有进程占着，有就先确认它盯的那一轮已经跑完再停。
- 有独有提交、或者有没进 main 的文档改动的：分支留着，工作区交给 owner 拍板，不替他决定扔掉。
- 主检出要是停在已合并的旧分支上，切回 main 并 ff。

相关：[[feedback_delegate_impl_to_opus_subagent]] ⑦（派工收尾）、[[feedback_git_pitfalls]]（`--contains` 不可信）、[[feedback_long_run_report_to_main_chat]]（Monitor 的用法）。
