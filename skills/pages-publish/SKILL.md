---
name: pages-publish
description: 把本地 HTML/Markdown 文件发布到内网 Pages 服务（pages.pkbops.com），返回可分享 URL；并可把已发布页面做成飞书卡片发出（内网域名飞书没有 og 预览，分享链接一律发卡片）。用代码读取文件内容并直传，无需把大段（含 base64 图片的）HTML 内联进工具调用。触发场景：「发布到内网页面」「用 pages 发布这个 html/报告」「更新/覆盖已发布的页面」「列出/删除内网页面」「发卡片给我」「把页面分享到飞书」（同义说法模型自动泛化不另列）。
---

# pages-publish

> ⚠ 2026-09-01 现状：本机 mcp 配置已无 `pages` server（`claude mcp get pages` 报 No MCP server named "pages"），下述脚本取不到 URL/token 会失败。现行发布通道 = social-proxy 的 `publish_page` / `share_page` 动作（execute_tool 调用，详见 memory: reference_pages_publish_via_social_proxy.md）。修复本 skill 的 token 来源前，发布一律走 social-proxy。

内网 Pages 服务（`pages.pkbops.com`）的命令行封装。**核心价值**：直接从文件路径读取内容并通过 HTTP 上传，绕开「模型把整份 HTML 逐字转录进 `publish_page(html=...)` 工具参数」——尤其是含 base64 内嵌图片的自包含 HTML，转录既贵又易截断损坏。

底层就是 `pages` MCP（HTTP / JSON-RPC，`https://pages.pkbops.com/mcp`）。脚本运行时从 `claude mcp get pages` 动态取 URL + token，不硬编码密钥。

## 何时用这个 skill 而非 pages MCP 工具

- **文件在磁盘上**（尤其自包含 HTML、带内嵌图片、体积 >10KB）→ **一律用本 skill 的脚本**，让代码读文件。
- 只有几行、现场手写的小片段 → 直接调 social-proxy 的 `publish_page` 动作也可以（`mcp__pages__*` 工具已随 pages MCP 下线）。
- 判断依据：只要你已经/将要把内容写到某个 `.html`/`.md` 文件，就走脚本。

## 用法

脚本：`scripts/pages_publish.py`（stdlib only，用 `python3` 跑）。

```bash
SKILL=~/.claude/skills/pages-publish/scripts/pages_publish.py

# 发布自包含 HTML（新页面，随机 slug）
python3 "$SKILL" publish /path/to/page.html

# 指定 slug + 标题（传已存在的 slug = 覆盖更新，URL 不变，90 天保留期重置）
python3 "$SKILL" publish /path/to/page.html --slug my-doc --title "我的文档"

# 发布 Markdown（服务端套统一模板，纯文字报告优先用这个，不用自己写 CSS）
python3 "$SKILL" markdown /path/to/report.md --slug weekly-report

# 列出已发布页面（全团队共用视图，按更新时间倒序）
python3 "$SKILL" list --limit 20

# 按 slug 删除
python3 "$SKILL" delete my-doc

# 把已发布页面做成飞书卡片发出（标题自动取页面 title，卡片可转发）
python3 "$SKILL" share my-doc --desc "一句话说清页面内容" --webhook "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

成功时脚本把最终 URL 打到 stdout（进度信息走 stderr），直接转述给用户即可。

## 参数说明

- `--slug`：留空 = 新页面随机 slug；传已存在 slug = **覆盖同一 URL**。想更新已发布页就复用原 slug。
- `--title`：留空时 HTML 取 `<title>`、Markdown 取文件名；仅用于 `list` 时辨识。
- 覆盖更新会重置 90 天保留期。

## 飞书卡片分享（share）

内网域名飞书抓不到 og 预览，直接贴链接没有卡片、日后难搜——**分享 pages 链接一律用 share 发卡片**，收到后长按转发给任何人/群（按钮和链接转发后保持可点）。

- **首次使用**：用户需要一个「发给自己」的目标——飞书拉一个只有自己的群 → 群设置 → 添加**自定义机器人** → 安全设置选「自定义关键词：`pages`」→ 把 webhook 告诉 Claude。**拿到后把 webhook 记进用户的 CLAUDE.md 或 memory**，之后用户说「发卡片给我」直接带上，不要每次再问。
- 目标三选一：`--webhook`（上面的自助方式）/ `--email` / `--open-id`（后两者走应用机器人 P2P，需服务端已配应用凭证）。
- `--desc` 卡片描述——**写法见下方「卡片文案」一节**，这是卡片好不好用的关键。
- 也可以直接调 MCP 工具 `share_page`（参数同名）；发布后顺手分享用脚本 `publish` + `share` 两步最顺。
- 服务端已强制校验飞书回包 `code==0`（飞书 webhook 失败也回 HTTP 200 的坑），报成功就是真送达。

### 卡片文案（标题 + 描述，写给「收到卡片的人」）

卡片的**标题**和**描述**是给第一次看到的同事读的，要让他一眼懂「这是什么、对我有什么用」。不是写给你自己看的备注。

- **标题**（= 页面 title，`publish --title` 或 HTML `<title>` 决定）：一句话说清内容/工具，能自解释。报告页就用报告主题；工具/功能页就说清它干嘛的。
- **描述**（`--desc`）：2-3 句电梯简报——**是什么 + 解决什么痛点 + 怎么用**。像介绍给不知情的同事。
- **禁止 meta 自指**：不要写「这张卡片带封面」「这就是效果示范」这种描述卡片自身的话——收卡人不关心卡片，只关心内容。
- 反例：`内网页面一句话发成飞书卡片 · 现在卡片自动带封面图…这张卡片本身就带封面`（在讲卡片自己，没讲内容）。
- 正例：`同事用 Claude 产的报告/分析，一句话发布成内网页面，再一句话变成可转发的飞书卡片。页面公众号式排版，手机读、图文都顺。内网链接没预览、日后难找的痛点，这工具解决了。`

**封面图文卡（2026-07-20 起自动生效）**：页面若含图（解码后 ≥3KB 的 png/jpg/gif/webp），share 时服务端自动抽**文档顺序第一张合格图**上传成飞书 `img_key`、作卡片封面 → 卡片长得像公众号图文卡（封面 + 标题 + 描述 + 「阅读全文」按钮）。

- **无需任何额外设置**：封面凭证（飞书自建应用 `FEISHU_APP_ID/SECRET`）已配在服务端 Secret，对所有人自动生效；连 webhook 自助路径也出封面（img_key 在自定义机器人卡片能正常渲染，已实测）。
- 纯文字页面（无 `<img>` 或图太小）→ 退回纯文字卡，正常不报错。
- 想指定封面 / 关掉封面：`share_page` 的 `cover` 参数——留空自动抽第一张、传 data URI 或站内 `/p/<slug>/<hash>.png` 指定、传 `none` 关闭。仅接受 data URI 与站内资产，不抓外网 URL（SSRF 红线）。
- 报成功时若结尾带 `(无封面: …)`，代表这页没出封面及原因（无图/太大/上传失败），share 本身仍送达。

### 给没有图的页面加封面（`scripts/make_cover.py`）

**封面 = 页面文档顺序第一张 `<img>`。** 带图表/截图的报告天然有封面；**纯文字页 / 工具介绍页**想要公众号式的设计感封面，用这支脚本生成一张品牌 banner，嵌成页面第一张图，再 publish + share，卡片就自动带上它。同事不用自己设计、不用自己配色。

```bash
COVER=~/.claude/skills/pages-publish/scripts/make_cover.py
python3 "$COVER" \
  --title "一句话，把内网页面[[发成飞书卡片]]" \  # [[词]] = 用主题色高亮
  --subtitle "封面图 · 标题 · 描述 · 可点按钮" \
  --chips "发卡片给我,公众号式阅读,大图不卡" \      # 逗号分隔，第一个实心高亮
  --theme amber \                                    # 见下方主题；想微调再叠 --accent "#xxxxxx"
  --out /tmp/cover.jpg
# stdout 打出图片路径；读成 base64 塞进页面 <body> 的第一个 <img src="data:image/jpeg;base64,...">
```

- **五套现成主题**（暗色调，一主色，遵循 taste-skill 不用纯黑/AI 紫）：`amber` 暖橙(默认)、`indigo` 冷蓝、`forest` 森绿、`rose` 玫红、`slate` 青灰。选一个即可；`--accent "#hex"` 覆盖强调色做微调。
- **文案要配页面内容**：`--title/--subtitle/--chips` 是给收卡人看的第一印象，写清「这页是什么」，同「卡片文案」一节的纪律。
- 实现：HTML+CSS 模板 → 系统 Chrome 无头渲染 2x → sips/PIL 压 1200 宽 JPEG（~160KB）。需要本机有 Chrome/Chromium；纯文字页本就没图，这是唯一「无中生有」造封面的途径。
- 一条龙：`make_cover.py` 生成 → 嵌成页面首图 → `publish` → `share`。让任何同事都能发出「带封面 + 说清内容」的公众号式卡片，不止你调过的那一张。

## 约定与坑

- **`publish` 要求单文件自包含**：CSS/JS/图片全部 inline（图片用 `data:` base64）。外链资源在内网页面不保证可达，务必内嵌。
- **服务端上限 50MB**：超限会直接报错（不会静默截断/压缩），报错时先压图再重传。
- **图片建议先压缩**：base64 会把体积放大 ~1.33×。生成自包含 HTML 前用 `sips`/`magick` 把图压到合理大小（示例：`sips -s format jpeg -s formatOptions 45 -Z 900 in.png --out out.jpg`），既减小页面又加快上传。
- **纯文字报告优先 `markdown`**：服务端有统一模板，不用自己写 HTML/CSS。
- **图文并茂 / 自定义排版 / 图表** → 用 `publish` 传 HTML（动手前先看下方「主题模板」一节）。
- 敏感信息：发布即上内网共享视图，别把密钥/隐私截图放进页面。

## 主题模板（themes/）

要精排版的 HTML 报告，**先从 `themes/` 挑主题改内容，不要从零写 CSS**。每份主题都是实际获好评的页面抽象来的：CSS 原样保留、`<body>` 换成【…】占位符、文件头注释写明结构约定与写作纪律——整份复制后只替换占位符即可。

| 主题 | 适用 |
|------|------|
| `report-cards.html` | 评审/建议/审计类报告：hero 表态框 + 优先级图例 + 红/琥珀分档卡片 + 蓝色建议块 + 结尾一览表 |

沉淀约定：现写的样式获用户好评 → 抽象成新主题存入 `themes/`（CSS 原样保留、内容换占位、头部注释写结构约定 + 各类名含义 + 好评原因），并在上表登记一行。

## 配置来源（脚本自动解析，一般无需关心）

1. 环境变量 `PAGES_MCP_URL` / `PAGES_MCP_TOKEN`（优先）
2. 否则解析 `claude mcp get pages` 的输出

若 `pages` MCP 未注册或换了地址，脚本会报错提示设置上述环境变量。
