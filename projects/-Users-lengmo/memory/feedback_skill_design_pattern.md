---
name: Skill design pattern preference
description: User's preference for "directory-style CLAUDE.md + content devolution to SKILL.md / references"
type: feedback
originSessionId: 290b7bd2-b4fa-4424-a3f9-1e45803de401
---
写 skill 或组织 CLAUDE.md 时遵循的模式：

## 结构
- CLAUDE.md 做索引目录（IF-ELSE 路由），不放规则正文
- SKILL.md 正文 < 500 行，细节下沉到 references/<TOPIC>.md
- references/ 每个文件单主题、< 200 行

## 规则写法
- 每条规则 = 粗体断言 + 一句话展开 + 具体数字/阈值
- 代码示例强制 ❌ 坏例 / ✅ 好例 对子
- 阈值用表格，不用段落

## Description
- 必须有具体触发词（如 "LCP", "rebase", "transparent header"）
- 避免抽象词（"优化"、"最佳实践"）

**Why:** 减少常驻 context 的 token 占用，让模型能按场景路由到正确文件。空泛的触发词会引起 skill 之间竞争，精准触发词让路由确定。

**How to apply:**
- 审查已有 skill / CLAUDE.md 时按此模板检查
- 新增规则优先加到对应 memory / skill 文件，而不是塞进 CLAUDE.md
- 当 CLAUDE.md 超过 100 行或涉及 > 3 类主题，启动一次下沉重构
