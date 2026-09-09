---
name: obsidian-vault-archives
description: Obsidian vault 就是 ~/Desktop/archives，零迁移直挂；写入侧不变（Claude 照旧写 md），Obsidian 只是回看层
metadata: 
  node_type: memory
  type: reference
  originSessionId: 26065dd6-65c5-4c4b-ade1-57e68807eb4a
  modified: 2026-09-01T08:50:03.481Z
---

2026-07-12 装的 Obsidian（brew cask），vault 直接指向 `~/Desktop/archives`（vault 注册在 `~/Library/Application Support/obsidian/obsidian.json`）。CLI 二进制叫 **`obsidian`**（`/opt/homebrew/bin/obsidian` → app 内的 obsidian-cli），`which obsidian-cli` 查不到。

- **定位**：只做已有 markdown 库的回看层（图谱/双链/搜索/白板）；写入侧完全不变——学习笔记照旧写 `技术总结/`
- **明确砍掉的**：Obsidian MCP（多余一层）、PARA 重构（现有目录就是真实分类）、Calendar 日记插件
- 手机端看不了这个 vault（Obsidian mobile 只认 iCloud vault 或付费 Sync）；手机侧备份仍是用户手动拖有道云
- 相关笔记：`技术总结/04.20-三层记忆.md` 的 P2（Obsidian 长期层）由此落地，[[feedback_real_requirement_archive]]
