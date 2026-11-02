---
name: find-lost-things-fast
description: 找「前两天还在的东西」先问在哪看到 + 翻废纸篓/近期会话；搜会话 jsonl 用 python mmap，本机 grep 是 ugrep 别名会拒复杂正则、超长行带上下文会卡死；owner 提到「之前说过/细节在别的会话」先翻 claude+codex 会话记录再答，别让他重讲或给出和旧结论打架的建议；Claude 会话记录只留 30 天（cleanupPeriodDays=30），用 jsonl 做统计或找旧现场前先核真实时间窗；认当前 session 的 jsonl 按内容指纹，别用 mtime
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5aa5080f-0c50-4b87-8e48-e11ae56e32e4
  modified: 2026-11-02T07:52:35.836Z
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
- 相关：本文件「认 session 按内容非 mtime」节


补充：本机 grep=ugrep 拒复杂正则、长行带上下文会卡死

## 指向旧上下文先翻会话

owner 指向过往上下文时（「我告诉过你」「细节在 codex 里」），先搜 `~/.claude/projects/-Users-lengmo/*.jsonl` 和 `~/.codex/sessions/**` 的近几天记录，读完再答。

**Why:** 2026-09-30 聊 Google 号停用：09-29 会话里原因、两次申诉、论坛 Diamond 专家「无升级渠道」都已讲清，我没翻就反复让他补原因、重复推论坛，被怼「告诉过你很多次了，信你还是信别人」。
**How to apply:** 搜法见本文件开头（python 逐行 json 解析，只抽 user/assistant 文本）；答时先复述已知事实表明读过，再给增量判断；自己旧结论与 owner 听来的说法冲突时，分「可核实/不可核实」摆出来，不硬压。

**接手 codex 停下的活（2026-10-22 lich 实例）：** codex rollout 里只有 user/assistant 文本可读，子 agent 消息与部分工具参数是加密串（`gAAAA…`），看不到它验到哪一步。可靠现场是 `git worktree list` 找它的分支与未提交 diff，加上 `/private/tmp/<项目>-*` 下它留的临时验收脚本和 report.json（含 failure 字段）。它自报的「验收通过」要自己重跑，那次它的临时脚本其实卡在一个过期按钮名上。

## 会话记录只留 30 天

`~/.claude/settings.json` 的 `cleanupPeriodDays` 是 30，`~/.claude/projects/*/*.jsonl` 里更早的会话已被清掉。

- 按「某日以来」扫会话时，mtime 过滤只是上限，样本实际只回溯约 30 天。报数前先取每个会话首条 timestamp 的最小值，写明真实窗口。
- 更早的事故现场要从项目 git 记录和仓内 docs 重建，翻不到不等于没发生过。

10-30 审开工三问时，我把一个月的样本说成「08-17 以来」，复核时才发现。

## 认 session 按内容非 mtime

问"当前 session id"时，**不要**用 `ls -t ~/.claude/projects/-Users-lengmo/*.jsonl | head -1`（最近 mtime）来认——`-Users-lengmo/` 这个 project 目录下**同时有多个并发会话在写**（chat-cc-bot、telegram bot、cron agent 等），mtime 是竞态，抓到的"最近改动"经常是别的会话。

**Why:** 2026-06-17 我把 mtime 最新的 `1101eeb0` 当成当前 session 报给用户，实际那是 chat-cc-bot 会话（grep 命中 chat-cc-bot×621、agg 内容 0）；本对话（agg eval 重锚活）真身是 `643b1eb6`。几分钟后两个文件 mtime 还互相反超，证明 mtime 不可作身份依据。

**How to apply:** 按**内容指纹**认——grep 各候选 jsonl 找只有当前对话才有的字符串（本轮如 `6d487fa99`/`pin-gold`/`重锚`/`世界卡`/`agg-tuning`），命中的那个才是。mtime 顶多在"多个都内容命中"时做次级排序。相关：[[project_codegen_workflow]]。任何扫 jsonl 的活都同理：按内容归属，别假设一个目录 = 一个会话。

**追加（2026-08-04，找"丢失的 session"）：** 用 `rg` 搜 `~/.claude/projects/` 必须带 `--hidden --no-ignore`——rg 默认静默跳过隐藏目录内容，裸跑会零命中，看起来像"transcript 不存在"（实际都在）。cwd 在别处（如 onlychat 仓）开的会话未必落在对应 project 目录，`-Users-lengmo/` 下大杂烩，还是按内容指纹认。用户说"session 找不到了"≠文件没了，先 rg 指纹再下结论。
