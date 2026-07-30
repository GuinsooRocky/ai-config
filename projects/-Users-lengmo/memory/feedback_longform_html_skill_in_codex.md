---
name: feedback-longform-html-skill-in-codex
description: 文章/学习笔记落 HTML 要用 codex 侧的 longform-html skill 模板，别手写版式
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a1aef402-112e-4fb7-8cb9-567388e62740
  modified: 2026-07-27T05:04:59.820Z
---

用户让"文章/笔记落 HTML"时，有现成 skill 在 **codex 侧**：`~/.codex/skills/longform-html/`（SKILL.md + assets/learning-handbook-template.html）。

**Why:** 07-27 手写了一版 HTML 排版，用户问"是不是用 skill 写的"——skill 存在但在 `~/.codex/skills/` 不在 `~/.claude/skills/`，只翻 Claude 侧会漏。

**How to apply:** 落 HTML 长文直接读该模板照 SKILL.md 规矩排（学习手册版式：左侧 190px 粘性目录、进度条、.matrix/.note/.steps/.diagram 组件、无 CDN），内容先过去 AI 味 pass。找 skill 时记得 codex 侧也有一份库存。
