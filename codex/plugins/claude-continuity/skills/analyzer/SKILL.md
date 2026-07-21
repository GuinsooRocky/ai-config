---
name: analyzer
description: 抓取 + 分析 + 多源调研 5 个平台的 URL 内容：微信公众号（mp.weixin.qq.com）、小红书（xiaohongshu.com/xhslink.com）、X/Twitter（x.com、twitter.com）、YouTube（youtube.com、youtu.be）、B 站（bilibili.com、b23.tv）。这 5 个平台强制走 `sf-reader-all`，禁止直接 WebFetch（会拿到风控页）。单篇模式触发词："抓下"、"抓一下"、"抓取"、"读一下"、"看看这个"、"这篇讲了啥"、"分析这篇"、"要点"、"analyze"、"/analyze"。多源调研模式（≥2 个 URL，或单篇但明说深挖）触发词："调研这几篇"、"看看关联"、"对照分析"、"找反方"、"追引用"，细则见 references/research-mode.md。通用网页/RSS/arxiv PDF 可作调研模式输入但单独丢过来不触发；开放议题研究归 deep-research，给定来源集合的学习归本 skill。
---

# Content Analyzer Skill

> Any content → structured analysis report with actionable insights

## Trigger

When user sends content (URL, text, or transcript) with analysis intent:
- `/analyze [URL]`
- "Analyze this article"
- "What are the key takeaways?"
- Auto-triggered after video/podcast transcription (from video skill)

## Pipeline

### Step 1: Get Content

**首选 `sf-reader-all`**（本机 Python CLI，`/Users/lengmo/.local/bin/sf-reader-all`），它内部按平台三层 fallback（Jina → Playwright headless → 登录态浏览器），微信/小红书/B 站这种风控站点也能抓。

| Input | Tool |
|-------|------|
| 任何 URL（微信/小红书/X/YouTube/B 站/RSS/通用网页） | `sf-reader-all <url>` |
| sf-reader-all 不支持的格式 / 抓取失败 | `WebFetch` 或 Jina Reader 兜底 |
| Local file | Read file directly |
| Transcript from video skill | Use directly |

**执行方式**：
```bash
sf-reader-all <url>
```
抓完落到 `~/unified_inbox.json`，从里面拿对应 url 项的 `content` 字段（中文正文已抽好）。需要登录态时（小红书等）先跑 `sf-reader-all login <platform>` 一次。

**不要**直接 WebFetch 微信公众号 / 小红书链接——会拿到风控页。

**批量抓取红线（事故换来的，必须遵守）**：
- 多 URL **必须**串行或 ≤2 并发——12 并发 Playwright 互相饿死全超时的事故在案
- 抓完**必须**按内容特征校验真正文（标题命中/正文长度/关键词），绝不凭状态码或条数报"全量完成"
- X/Twitter 的全文在 `unified_inbox.json`，不在 stdout
- 视频源（YouTube/B 站）抓取时**必须**同时保留简介 description 字段——视频里提到的论文/链接，真实载体是简介而非口播转写

### Step 2: Multi-Dimensional Analysis

Scan content across these dimensions. Only output dimensions with actual content — skip empty ones.

```markdown
## 📖 Summary

[1-3 sentence core thesis]

**Source**: [author/publisher] · [date]
**Type**: [tweet/article/video/podcast/report]

---

## 💡 Key Insights

### 🎯 Core Arguments
- **Thesis**: [Main argument or finding]
- **Evidence**: [Supporting data or reasoning]
- **Strength**: [How convincing? What's missing?]

### 🤖 Tools & Methods
- **What**: [Tools, frameworks, or techniques mentioned]
- **How**: [How they're used or applied]
- **Relevance**: [Where you'd use this]

### ⚙️ Workflow Ideas
- **Optimization**: [Process improvements mentioned]
- **Automation**: [What to automate]
- **Integration**: [How to fit into existing workflow]

### 📊 Data & Numbers
- **Key metrics**: [Important numbers mentioned]
- **Trends**: [Patterns in the data]
- **Gaps**: [What data is missing]

### ⚠️ Risks & Warnings
- **Pitfalls**: [Explicitly mentioned risks]
- **Blind spots**: [What the author is missing]
- **Counter-arguments**: [Alternative perspectives]

### 🔗 Resources
- **Tools/APIs**: [Mentioned tools or data sources]
- **People**: [Worth following or referencing]
- **Further reading**: [Related content]

### 🧠 Mental Model Shifts
- **Before**: [Common assumption]
- **After**: [New understanding from this content]
- **Impact**: [How this changes decisions]

---

## ✅ Action Items

### Quick Wins (< 30 min)
- [ ] [Action 1] — Impact: ★★★★ | Effort: Easy
- [ ] [Action 2] — Impact: ★★★ | Effort: Easy

### Deeper Work (1-3 hours)
- [ ] [Action 3] — Impact: ★★★ | Effort: Medium
- [ ] [Action 4] — Impact: ★★ | Effort: Medium

### Exploration (needs validation)
- [ ] [Action 5] — Impact: ★★★ | Effort: Hard | Nature: Exploratory
```

### Step 3: Personalized Relevance (Customizable)

Map insights to YOUR context. Edit the dimensions below to match your own projects, interests, and systems.

```markdown
## 🔄 How This Applies to Me

### My Projects
- **onlychat**（工作 · Next.js AI 角色聊天）: [世界卡/前端工程/工作流相关吗]
- **MK**（macOS 语音输入 · Swift + sherpa-onnx）: [ASR/延迟/菜单栏 app 相关吗]
- **meat-encyclopedia**（RN/Expo 买肉对照 app，待建 web 端）: [数据/SEO/上架相关吗]
- **pageforge**（PRD+Figma 生码工作流）: [生码管线/评测/agent 工程相关吗]

### My Knowledge Base
- **Update**: [Which notes/docs to update]
- **New entry**: [What to add to my knowledge system]

### My Decision Log
- **Changed my mind about**: [what and why]
- **Confirmed my belief that**: [what]
```

> **Customization**: Edit the dimensions in Step 2 and Step 3 to match your own
> domain. A trader might add "Market Impact" and "Risk Assessment". A developer
> might add "Architecture Patterns" and "Tech Debt". Make it yours.

## 多源调研模式（≥2 个来源时升级）

触发：一次给 ≥2 个 URL，或明确说"调研 / 关联 / 对照 / 找反方 / 追引用"。
单篇看要点走上面的默认管线，**不要**为单篇启动本模式；单篇要项目建议直接用 project-suggest。

进入本模式**必须**先 Read `references/research-mode.md`（工人 prompt、反方硬规则、引用回流规则都在里面），流程骨架：

1. **Intake**：按平台分流抓取（红线同 Step 1），每篇标注引用可达等级（arxiv/PDF=full、微信/X/视频=仅提及、小红书=无）
2. **精读扇出**：每篇 spawn 一个 subagent 产精读卡（= Step 2 卡片裁剪版 + 新增《提及/引用作品清单》字段；薄源例外见 references 精读工人段），N 篇全文不进主对话，只回卡片
3. **关联合成**：主对话吃卡片做跨篇一致/冲突/共同预设分析；"找反方"是 opt-in 加强档；报告**必须**含「教学层」与「大牛视角」两段（规则见 references）
4. **裁决落盘**：每篇按 Step 3 项目画像给「沾哪个项目 + 一句为什么 / 纯学习」一行裁决，报告末尾附「落盘清单」，用户**单次确认**后按三 sink 批量落盘

## Output Modes

| Mode | Trigger | Output |
|------|---------|--------|
| **Full** (default) | `/analyze [URL]` | All dimensions |
| **Sparse** | `/analyze [URL] --sparse` | Only hit dimensions, skip empty |
| **Brief** | `/analyze [URL] --brief` | Action items only |

## Best Practices

1. **Scan all dimensions, but don't force-fill** — skip empty dimensions cleanly
2. **Actions must be specific** — not "learn about X" but "read X docs chapter Y"
3. **Distinguish fact from opinion** — mark the author's claims vs verified facts
4. **Source everything** — tag where each insight comes from in the original content
5. **ROI awareness** — not every action is worth doing, assess effort vs impact

多源调研报告的示例输出 / 参考格式：见 `references/research-mode.md` 的「报告骨架」段——通用骨架，不锚定具体笔记文件，**不要**另建模板文件。

## 反模式 / 已知坑

- **绝不**直接 WebFetch 微信/小红书链接——只会拿到风控页
- **绝不** >2 并发跑 sf-reader-all——12 并发互相饿死全超时的事故在案
- 登录态失效（小红书常见）→ 先 `sf-reader-all login <platform>` 再重试，**不要**反复裸抓
- 微信正文里的 URL 几乎全是图床代理（mmbiz.qpic.cn / wsrv.nl）——**不要**当成"文中引用"
- 说"全量完成"之前**必须**逐条校验过正文内容特征，状态码 200 不等于拿到真正文
- 抓取工具链中途坏掉（yt-dlp / 证书 / cookie / 登录态）→ 修复尝试**封顶 1 次**，再失败立即降级（兜底通道 / 简介·元数据 / 记入「未覆盖清单」）继续调研，工具修复另开任务——同 cmm-pr 熔断铁律，别在 run 里挖兔子洞；"登录态失效先 login 再重试"的那次 login 即计为这 1 次

## Codex compatibility

Preserve this workflow's intent and evidence rules. Translate Claude-specific tool names to the available Codex tools.
