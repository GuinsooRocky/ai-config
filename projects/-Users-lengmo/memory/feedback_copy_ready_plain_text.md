---
name: feedback_copy_ready_plain_text
description: 给用户复制的成品文案一律纯文本不用 markdown；终端 soft-wrap 换行靠写文件+编辑器复制解决
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b082b28e-b7d2-47fd-8bf7-f415f56f088a
---

用户从 iTerm 复制我的输出时遇到两类污染：① markdown 源码（`|` 表格、`>` 引用、`**` 等）会原样粘出；② 终端按窗口宽度 soft-wrap 长行，框选复制时 wrap 处变成真实换行。粘到有道云/小红书/纯文本框就乱。

**Why:** 终端复制的是「markdown 源码 + 可视折行」，不是渲染后的样子。markdown 符号我能控制；soft-wrap 换行取决于用户终端宽度，我从输出端无法消除——文字再连续，窄窗口照样折。

**How to apply:** 凡是给用户**复制的成品文案**（无论是否要存文档）一律纯文本：不用表格/引用块/`#`/`**`，写成连续段落或单行。我自己在终端里的分析/结论可以照常用 markdown（表格便于看，见 [[feedback_table_for_structured_content]]）。用户已拍板（2026-06-27）：**不写文件**（文件增删改查太繁琐），就在对话里直接给纯文本即可——「至少不是 MD 就好」。soft-wrap 换行的残留用户自己接受，别再主动推荐写文件那条路。临时可提加宽 iTerm 窗口减少折行。
