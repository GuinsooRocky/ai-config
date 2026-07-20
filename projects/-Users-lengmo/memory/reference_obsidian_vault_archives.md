---
name: obsidian-vault-archives
description: Obsidian vault 就是 ~/Desktop/archives，零迁移直挂；写入侧不变（Claude 照旧写 md），Obsidian 只是回看层
metadata: 
  node_type: memory
  type: reference
  originSessionId: 26065dd6-65c5-4c4b-ade1-57e68807eb4a
---

2026-07-12 装的 Obsidian（brew cask，含 obsidian-cli），vault 直接指向 `~/Desktop/archives`（vault 注册在 `~/Library/Application Support/obsidian/obsidian.json`）。

- **定位**：只做已有 markdown 库的回看层（图谱/双链/搜索/白板）；写入侧完全不变——学习笔记照旧写 `技术总结/`，daily-recap 照旧写 `每日复盘.md`
- **明确砍掉的**：Obsidian MCP（多余一层）、PARA 重构（现有目录就是真实分类）、Calendar 日记插件（与 daily-recap 重叠）
- **剪藏**：`archives/剪藏/` 文件夹已建，配 Obsidian Web Clipper 浏览器扩展用
- 手机端看不了这个 vault（Obsidian mobile 只认 iCloud vault 或付费 Sync）；手机侧备份仍是用户手动拖有道云
- 相关笔记：`技术总结/04.20-三层记忆.md` 的 P2（Obsidian 长期层）由此落地，[[feedback-real-requirement-archive]]
