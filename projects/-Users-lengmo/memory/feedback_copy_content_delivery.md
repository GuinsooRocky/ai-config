---
name: feedback_copy_content_delivery
description: 给用户复制的内容按长短分流——短的对话内纯文本，长的写 scratchpad 文件报路径（合并自 feedback_copy_ready_plain_text + feedback_copy_use_scratchpad）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b082b28e-b7d2-47fd-8bf7-f415f56f088a
  modified: 2026-07-26T05:54:27.453Z
---

用户从 iTerm 复制我的输出时遇到两类污染：① markdown 源码（`|` 表格、`>` 引用、`**` 等）会原样粘出；② 终端按窗口宽度 soft-wrap 长行，框选复制时 wrap 处变成真实换行。粘到有道云/小红书/纯文本框就乱。这两条污染，短文本靠"不用 markdown"就够治；长文本 soft-wrap 无解，只能换介质（文件+编辑器复制）。

**Why:** 2026-06-27 用户曾明确说"不写文件（太繁琐），直接对话里给纯文本就好"；3 天后 2026-06-30 又反过来要求"大段内容写 scratchpad 文件，别直接输出到对话"。两条乍看矛盾，但实际适用的场景不同（前者是短文案，后者是"大段"/"全量返回"）——按长短分流即可同时满足两条，不用二选一。

**How to apply:**
- **短内容**（几句话的文案/结论/短反馈，无论是否要存文档）：对话里直接给**纯文本**——不用表格/引用块/`#`/`**`，写成连续段落或单行。我自己在终端里的分析/结论可以照常用 markdown（表格便于看，见 [[feedback_table_for_structured_content]]）。soft-wrap 换行的残留用户自己接受，别主动推荐写文件。
- **长内容**（文档、报告、长文案、"全量返回"、"我贴进去"这类意图）：写进 scratchpad 文件，报路径让用户从编辑器复制。路径固定：`/private/tmp/claude-501/-Users-lengmo/<session-id>/scratchpad/<descriptive-name>.md`。Why：session 关闭后 scratchpad 自动清理（不留缓存）；编辑器复制比聊天框干净（无 soft-wrap、无 markdown 渲染干扰）；比写进 ~/Desktop/ 更轻。
- 界限不明显时（比如中等长度）以"是否几屏内能读完"判断，倾向对话内纯文本；用户嫌繁琐会直接说。
- **例外：交付物是 prompt 时一律直接贴对话**（2026-07-26 再次纠正："不需要你给我写doc，也不需要落档，prompt 返回给我就好"）。哪怕四份长 prompt 也贴对话——用户要的是当场复制粘去别的 session，落项目仓/scratchpad 都算过度动作。用代码块包裹保持纯文本。write-a-prompt skill 里"长 prompt 必须落文件"那条对本用户不适用。
