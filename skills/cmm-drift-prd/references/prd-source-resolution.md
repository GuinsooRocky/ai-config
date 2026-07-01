# PRD 来源解析

## 解析顺序

1. 读 `~/Desktop/cc-memory/onlychat/features.md`
2. 没命中 → 当场问用户贴

**约束**：本 skill 不写回 features.md（用户自己维护 cc-memory）。

---

## features.md 探测策略

features.md 是用户自己维护的 worktree → PRD 映射表，格式宽松。**skill 不强求固定 schema**，按 fuzzy 探测。

### 探测流程

```python
import re
from pathlib import Path

FEATURES_MD = Path.home() / "Desktop/cc-memory/onlychat/features.md"

DOCX_URL_RE = re.compile(
    r"https://[^/\s]+\.feishu\.cn/(?:docx|wiki|sheets|base)/[a-zA-Z0-9_-]+"
)
BASE_HINT_RE = re.compile(
    r"(?:base|分支基于|从|base[_-]?branch)[:：\s]+([a-zA-Z0-9_/.\-]+)"
)

def resolve(worktree_name: str):
    if not FEATURES_MD.exists():
        return None
    text = FEATURES_MD.read_text(encoding="utf-8")
    lines = text.splitlines()

    # 找 worktree 名出现的行
    hits = [i for i, line in enumerate(lines) if worktree_name in line]
    if not hits:
        return None

    # 在每个 hit 附近 ±20 行窗口里扫 URL + base
    urls = []
    base = None
    for hit in hits:
        lo, hi = max(0, hit - 20), min(len(lines), hit + 21)
        window = "\n".join(lines[lo:hi])
        urls.extend(DOCX_URL_RE.findall(window))
        m = BASE_HINT_RE.search(window)
        if m and base is None:
            base = m.group(1)

    return {
        "worktree": worktree_name,
        "prd_urls": list(set(urls)),
        "base_branch": base,
    }
```

### 探测结果分支

| URL 数 | base | 动作 |
|---|---|---|
| ≥ 1 | 已找到 | 直接用 |
| ≥ 1 | 未找到 | 用 URL，问用户 base 分支（默认 `develop`） |
| 0 | 任意 | 进兜底问用户流程 |

---

## 兜底交互

features.md 没命中或部分缺失：

```
未在 ~/Desktop/cc-memory/onlychat/features.md 中找到 <worktree_name> 的 PRD 映射。

请贴：
1. PRD 飞书 URL（一行一个，可多份）：
   <等待用户输入>
2. base 分支（用于 git diff，默认 develop）：
   <等待用户输入或回车默认>
```

用户贴完：**不写回 features.md**。下次跑还是会问。

---

## docx token 抽取

```python
def extract_token(url: str) -> tuple[str, str]:
    """返回 (type, token)，type ∈ {docx, wiki, sheets, base}"""
    m = re.match(
        r"https://[^/]+\.feishu\.cn/(docx|wiki|sheets|base)/([a-zA-Z0-9_-]+)",
        url,
    )
    if not m:
        raise ValueError(f"Not a valid feishu URL: {url}")
    return m.group(1), m.group(2)
```

**类型处理**：

- `docx` → 直接 `get_document(document_id=token)`
- `wiki` → 直接传 URL 给 `get_document`，social-proxy 自动解到底层 docx
- `sheets` / `base` → 不支持作为 PRD 源，报错让用户改贴 docx URL

---

## 多 PRD 支持

一个 worktree 可能挂多份 PRD（主 PRD + 子需求 + 配置文档）。

### 数据结构

```python
prds = [
    {"url": "https://...feishu.cn/docx/docxA", "token": "docxA", "alias": "main"},
    {"url": "https://...feishu.cn/docx/docxB", "token": "docxB", "alias": "config"},
]
```

`alias` 可来自 features.md（如果用户标了）或 token 前缀截断（fallback）。

### 章节冲突消歧义

代码注释里 anchor 写法对应不同 PRD：

```ts
// PRD §3.2          ← 默认在所有 PRD 中找 §3.2
// PRD<main> §3.2    ← 指定主 PRD
// PRD: docxA §3.2   ← 指定 token
```

匹配逻辑：

1. 注释指定了 alias / token → 只在对应 PRD 中找
2. 注释只写章节号 → 在所有 PRD 中找：
   - 唯一命中 → ✅ 用之
   - 多份命中 → 标 `ambiguous: true`，进 🟡 让用户决断
   - 无命中 → 标 `not_found`，进 🟡

---

## 缓存 / 快照

获取的 PRD 内容快照写到：

```
<repo_root>/.git/prd-snapshots/<doc-token>-<YYYY-MM-DD>.json
```

格式：

```json
{
  "doc_token": "docxabc123",
  "fetched_at": "2026-05-28T14:30:00+09:00",
  "sections": {
    "3.2": {
      "title": "用户注册流程",
      "content": "..."
    },
    "3.2.1": {
      "title": "邮箱验证",
      "content": "..."
    }
  }
}
```

**索引方式**：按 anchor 涉及的章节号建索引，不存全文（减少快照体积）。

**比对**：找同 doc-token 最近一次的快照（按日期降序），对比当前 fetch 结果，列出变化的章节。

---

## 失败处理

| 场景 | 动作 |
|---|---|
| features.md 不存在 | 进兜底问用户 |
| features.md 有但 worktree 未命中 | 进兜底问用户 |
| 用户贴的 URL 非飞书域 | 报错，重新问 |
| 用户贴的 URL 是 sheets/base | 报错，要求改贴 docx |
| MCP get_document 失败 | 报错让用户重试或手动贴正文 |
| 多 PRD 中有一份拉不到 | 跳过该 PRD，对剩余继续 |
