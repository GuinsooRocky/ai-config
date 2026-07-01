# 链接落档 / 替换 / 失效（cmm-go 反应式规则）

主 SKILL 已判定"该不该进这里"。**进了之后**按当前 URL 跟 features.md 对应字段的关系，走 a/b/c 三种触发之一。

## 字段映射

- `*.feishu.cn/docx/{token}` → PRD（整篇 docx，全局根指针，值得存）
- `figma.com/(file|design)/...` **无 `?node-id=`** → Figma 文件根，可存
- 字段标 `<按需贴，节点级>` → 不问（用户已表态这类不落，直接放过）

## 触发 a：字段是 `<待填>` / 空 → 首次落档

问法（必须亮项目名 + worktree 路径 + 字段名）：
```
🔗 飞书 docx 链接
   存到？  世界卡项目 · PRD
           features.md → ~/Desktop/cmm/onlychat-world-book
   当前    <待填飞书链接>
   y / skip / 其实是别的字段（说哪个）
```
- y → Edit features.md，回执 `✓ 已存 PRD → 世界卡项目`
- skip → 不动，session 内同 URL 不再问

## 触发 b：字段已填且 URL 不同 → 主动问换不换

```
🔗 飞书 docx 链接 ≠ 表里存的
   世界卡项目 · PRD（~/Desktop/cmm/onlychat-world-book）
   已存    https://...J7Mid0zgro3...
   你贴的  https://...新token...
   换 / 保留 / 这是别的字段（说哪个）
```
- 换 → Edit
- 保留 / 这是别的字段 → 按对应分支处理

## 触发 c：调 get_document / get_sheet 拉失败（404/403/空内容）

```
⚠ PRD 链接拉不到（错误：<reason>）
   世界卡项目 · PRD
   存的    https://...
   重贴一个 / 标失效暂留 / skip 这次
```
- 重贴 → 走触发 b 的流程
- 标失效 → features.md 那行尾巴加 `# ⚠ 失效 YYYY-MM-DD`，下次面板把该字段标 ⚠
- skip → 放弃本次

## 字段已填 + URL 相同

静默忽略（已在主 SKILL 入口判定，正常不会到这里；防御性兜底）。
