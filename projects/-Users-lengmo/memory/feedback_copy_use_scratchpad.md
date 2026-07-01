---
name: feedback_copy_use_scratchpad
description: 需要给用户复制的大段内容（文档、报告、长文案）写进 scratchpad 文件而非直接输出到对话
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 22c6db60-a9c3-4d13-bfd8-0f083fd131f5
---

把要让用户复制的内容写进 scratchpad 文件，然后报路径让用户从编辑器复制。

**Why:** session 关闭后 scratchpad 自动清理（不留缓存）；编辑器复制比聊天框干净（无 soft-wrap 换行、无 markdown 渲染干扰）；比写进 ~/Desktop/ 更轻（不占用户目录）。

**How to apply:** 凡是"给我可以 cv 的内容"、"全量返回"、"我贴进去"这类意图 → 写 scratchpad，不要直接在对话里输出大段文本。路径固定：`/private/tmp/claude-501/-Users-lengmo/<session-id>/scratchpad/<descriptive-name>.md`
