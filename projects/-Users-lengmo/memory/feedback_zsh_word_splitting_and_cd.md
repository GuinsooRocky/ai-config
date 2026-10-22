---
name: feedback-zsh-word-splitting-and-cd
description: Bash 工具跑在 zsh——未加引号的 $VAR 不按空格拆词、cd 会改掉会话工作目录；临时拆代码做反面验证前先断言备份真的生成了
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1dcd4bc9-e1eb-4db6-b5d6-ba34c583496c
  modified: 2026-10-12T07:49:45.104Z
---

Bash 工具的 shell 是用户的 zsh，不是 bash。两个坑今天各踩一次：

1. **未加引号的 `$VAR` 不按空格拆词**：`SRCS="a.ts b.ts"; for f in $SRCS` 在 zsh 里只循环一次，`f` 是整串；`cp "$f" "$f.bak"` 直接失败。
2. **`cd` 会改掉会话的工作目录**，而且会一直延续到后面的调用：子 agent 继承了新目录，把自己的记忆写进了用户的素材目录。

**Why:** 2026-09-11 付费图修复做反面验证（逐个拆掉 8 处修复、跑对应测试、再还原）时，备份因为第 1 条一个都没生成，每步「还原」都是空操作，8 处修复被一路累积拆光。最后一次全量重跑出现 9 条红，再对照 HEAD 看 diff 才发现，逐个补回。同一天的第 2 条让 visual-qa 的两条记忆落进了 `~/Desktop/cmm/相册/.claude/`，事后搬回项目目录。

**How to apply:**
- 多个文件分开写成多个变量（`$L $U $E`），或者用 zsh 数组（`files=(a b); for f in $files`），或者直接列出来。别把多个路径塞进一个带空格的字符串。
- 会临时改坏代码的脚本开头加 `set -e`。改之前先断言备份在，例如 `for f in ...; do [ -f "$f.bak" ] || exit 1; done`。每步还原后用 `git diff --stat` 核对，确认回到了预期状态。
- 不要 cd。一律写绝对路径、`git -C <dir>`，或者在 python 里用绝对路径。
- **以 `=` 开头的裸词会被当成命令路径展开**：`echo ====` / `echo =====` 报 `(eval):1: === not found`，同一行里 `;` 后面的命令也跟着不跑（2026-09-23 onlychat 推荐模型审计踩两次，第二次把后面的 `git diff` 吞了）。分隔线一律加引号：`echo "===="`，或者改用 `echo "-----"`。
- **测试文件清单塞进变量 = 假绿**：`T=$(git diff --name-only … | tr '\n' ' '); vitest run $T other.test.ts` 在 zsh 里 `$T` 是一个整参数，vitest 当成过滤串匹配不到任何文件，只跑了后面显式写的那些，照样报全绿（2026-10-11 soliloquy 画布：列了 27 个只跑 13 个）。要拆词写 `${=T}`；跑完核「Test Files N」等于预期文件数。
- **grep 的 `--include=*.ts` 在 zsh 会先被当成 glob 展开**，匹配不到就报 `no matches found`，整条命令不执行。要写成 `--include='*.ts'`。
- **管道吃掉退出码 = 假 PUSH_OK**：`git fetch 2>&1 | tail -1 && git push … | tail -1 && echo PUSH_OK` 里每段的退出码都是 `tail` 的 0，fetch/push 全部 `Connection reset by peer` 照样打印 PUSH_OK（2026-10-12 soliloquy SEO 整改推送，差点把「已推上 main」写进汇报）。网络类 git 命令不接管道：`if git fetch origin > /tmp/x.log 2>&1; then …`，最后再 `git merge-base --is-ancestor HEAD origin/main` 验真。
- **BSD sed 不认 `\?`**：`sed 's/<\/\?loc>//g'` 在 macOS 上一字不剥，下游 `comm` 交集直接变 0（同日把 /discover 与 sitemap 交集误报成 0/23，真值 9/23）。要用 `sed -E 's#</?loc>##g'`，并对中间文件 `head` 一眼。

相关：[[feedback_gates_must_fail_on_purpose]]（闸要验反面）、[[reference_bash_timeout_orphans_child]]

- `git show $REF:path` 在 zsh 里 `$REF:s...` 会被当成 `:s` 修饰符吃掉，打出来的是整个 commit 而不是文件；要写 `${REF}:path`（10-22 perf-lab 栽过，1.3MB 输出落盘才发现）
