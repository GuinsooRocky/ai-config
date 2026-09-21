---
name: feedback-zsh-word-splitting-and-cd
description: Bash 工具跑在 zsh——未加引号的 $VAR 不按空格拆词、cd 会改掉会话工作目录；临时拆代码做反面验证前先断言备份真的生成了
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1dcd4bc9-e1eb-4db6-b5d6-ba34c583496c
  modified: 2026-09-11T07:14:22.168Z
---

Bash 工具的 shell 是用户的 zsh，不是 bash。两个坑今天各踩一次：

1. **未加引号的 `$VAR` 不按空格拆词**：`SRCS="a.ts b.ts"; for f in $SRCS` 在 zsh 里只循环一次，`f` 是整串；`cp "$f" "$f.bak"` 直接失败。
2. **`cd` 会改掉会话的工作目录**，而且会一直延续到后面的调用：子 agent 继承了新目录，把自己的记忆写进了用户的素材目录。

**Why:** 2026-09-11 付费图修复做反面验证（逐个拆掉 8 处修复、跑对应测试、再还原）时，备份因为第 1 条一个都没生成，每步「还原」都是空操作，8 处修复被一路累积拆光。最后一次全量重跑出现 9 条红，再对照 HEAD 看 diff 才发现，逐个补回。同一天的第 2 条让 visual-qa 的两条记忆落进了 `~/Desktop/cmm/相册/.claude/`，事后搬回项目目录。

**How to apply:**
- 多个文件分开写成多个变量（`$L $U $E`），或者用 zsh 数组（`files=(a b); for f in $files`），或者直接列出来。别把多个路径塞进一个带空格的字符串。
- 会临时改坏代码的脚本开头加 `set -e`。改之前先断言备份在，例如 `for f in ...; do [ -f "$f.bak" ] || exit 1; done`。每步还原后用 `git diff --stat` 核对，确认回到了预期状态。
- 不要 cd。一律写绝对路径、`git -C <dir>`，或者在 python 里用绝对路径。

相关：[[feedback_gates_must_fail_on_purpose]]（闸要验反面）、[[reference_bash_timeout_orphans_child]]
