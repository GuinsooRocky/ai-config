# PRD 内容获取路径

PRD 来源由用户给。三条路径，按可用性排序：

## 路径 1 · 飞书 MCP（最快，但 MCP 可能掉线）

如果飞书 MCP 还连着，直接 `docx_v1_document_rawContent` 拉 raw content。

```
URL 形如：https://wh9a7emh1y.feishu.cn/docx/J7Mid0zgro3fRhx9JmbcFjVBnRv
                                              ↑ document_id 在这
```

调用：

```
mcp__lark__docx_v1_document_rawContent(
  path={"document_id": "J7Mid0zgro3fRhx9JmbcFjVBnRv"},
  useUAT=true
)
```

返回是 JSON array of `{type, text}`，但 PRD 大时会被截断写到 tool-results 文件。提取纯文本：

```bash
FILE=/Users/lengmo/.claude/projects/-Users-lengmo/<session>/tool-results/<file>.txt
jq -r '.content' "$FILE" 2>/dev/null > /tmp/prd.txt
# 如果 jq 失败（飞书返回的是 [{type, text}] 数组而非 {content}），改用：
# jq -r '.[].text' "$FILE" > /tmp/prd.txt
wc -l /tmp/prd.txt
```

## 路径 2 · WebFetch 飞书分享链接（MCP 掉线时备选）

PRD 公开 / 飞书分享允许游客访问时可用：

```
WebFetch(url=飞书分享链接, prompt="提取全部正文，保留章节标题层级")
```

劣势：飞书 share 页面有时返回登录提示而非内容；WebFetch 单次也有 token 上限。

## 路径 3 · 本地文件（fallback）

让用户飞书导出 .docx → 转成 .md / .txt → 放本地，Read 即可。

或直接让用户把 PRD 正文粘到对话里。

---

## 提章节目录的命令

PRD 文本拿到后，先扫骨架。grep 出"看起来像章节"的行：

```bash
grep -nE "^[0-9]+\.[0-9]|^[一二三四五六七八九十]+、" /tmp/prd.txt | head -60
```

或按关键词扫常见章节：

```bash
grep -nE "^(背景|目标|名词|里程碑|总原型|组件|通用规则|功能详细|发现|首页|世界卡|挂载|创建|管理|数据埋点|风险|附录)" /tmp/prd.txt | head -40
```

定边界靠两个相邻章节起点的行号。例：§3 是 79 行，§4 是 909 行 → §3 内容 = `awk 'NR>=79 && NR<=908'`。

## PRD 章节号识别注意

飞书 rawContent **不保留章节号**——PRD 里写 "8.4.1 Mobile Edit Notes 框架页"，rawContent 出来只剩 "Mobile - Edit Notes tab 条目框架页"（标题文字，无 §8.4.1 前缀）。

所以：

1. 反讲里的 `§X.X` 编号要靠**对照飞书原文档**手动 / 视觉确认（用户给的链接 → 浏览器打开看左侧目录树）
2. 或者从 PRD 自己的内部引用反推（PRD 里常写"详见 8.4.1"，可以 grep `详见` / `见 8` 反推编号树）
3. 不确定时，宁可写"对应 PRD §X.X 创建流程章节"这种半精确锚点，也别瞎编

## Refresh mode 额外步骤

PRD 改了重跑时，多做一步：

```bash
# 把旧反讲覆盖的 § 列表 grep 出来，对比新 PRD 看哪些 § 内容变了
grep -oE 'badge-prd">§[0-9.]+' ~/Desktop/cmm/onlychat-World-Path/MM.DD-需求名反讲.html | sort -u
```

然后针对每个 §，对比新旧内容定位变化。
