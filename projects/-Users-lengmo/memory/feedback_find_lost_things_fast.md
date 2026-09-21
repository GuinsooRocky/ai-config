---
name: find-lost-things-fast
description: 找「前两天还在的东西」先问在哪看到 + 翻废纸篓/近期会话；搜会话 jsonl 用 python mmap，本机 grep 是 ugrep 别名会拒复杂正则、超长行带上下文会卡死
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5aa5080f-0c50-4b87-8e48-e11ae56e32e4
  modified: 2026-09-11T04:22:55.873Z
---

用户问「前两天还开着的 XX 是不是删了」时，第一步：`ls -lt ~/.Trash` + 最近几天会话记录；描述模糊（如「12m 峰值网络的脚本」）时一句话问清在哪看到（菜单栏/终端/网页/文件），别先扫全盘进程、launchd、项目文档。

**Why:** 2026-09-11 找「12M 峰值网络脚本」绕了十来轮（nettop/ccbar/soliloquy 文档/eval-arena 全扫一遍），被说「你怎么找东西这么费劲」。

**How to apply:**
- 搜 `~/.claude/projects/**/*.jsonl` 用 python `mmap` + 字节正则，只截命中前后 ~150 字节，并过滤掉 base64 段（截图 base64 里会碰巧拼出 `Mbps` 之类字母，造成假命中）
- 本机 `grep` 是 ugrep 别名：复杂正则直接报 `exceeds complexity limits`，要用 `/usr/bin/grep`
- `grep -oE '.{0,120}X.{0,120}'` 对超长 JSON 单行会卡到超时变后台孤儿，要手动 pkill（同病见 [[reference_bash_timeout_orphans_child]]）
- zsh 下 `--include=*.md` 不加引号会被当通配符吞掉（`no matches found`）
- `find … | xargs grep` 遇到带空格路径（`~/Library/Application Support/…`）会被切断、配合 `2>/dev/null` 静默漏掉——必须 `find -print0 | xargs -0`。那次脚本就躺在 `Application Support/NetworkMonitor/`，因此被误报「已删」
- 用户说「当时让 codex 搞的」→ 直接搜 `~/.codex/history.jsonl`（用户输入史，带 ts）+ `~/.codex/sessions/**`，一步到位
- 相关：[[feedback_session_id_by_content_not_mtime]]
