---
name: onlychat-prd-reflection
description: OnlyChat 项目 PRD 反讲文档生成 — 把 PRD 不完美的地方（矛盾 / 缺文案 / 反直觉）现在摆桌上解决，不在代码里发现。每节锚到 PRD §X.X，PRD 改了重跑刷新即可。仅产出 HTML 到 ~/Desktop/cmm/onlychat-World-Path/。我审的是 PRD 本身（矛盾/缺文案/反直觉）；查代码注释跟 PRD 同没同步那是 cmm-drift-prd。触发词：反讲、需求反讲、PRD 反讲、讲一遍 PRD、把需求过一遍、扫一遍 PRD、把 PRD 过一遍、PRD 有没有矛盾。裸"对一下 PRD/看下 PRD"意图不明，不直接触发本 skill——按全局 CLAUDE.md 的 PRD 路由先分诊。
---

# OnlyChat PRD 反讲

仅用于 onlychat 项目。反讲是 **PRD 的反向调试器**——把 PRD 矛盾 / 漏洞 / 反直觉摆桌上**现在解决**，不在代码里发现。PRD 改了重跑这个 skill 出新版本即可。

本 skill **自包含**：风格规范、自检清单全在本文，HTML 底稿在同目录 `assets/handbook-template.html`，不依赖任何外部 skill。

## 何时使用

- 用户粘 PRD（飞书链接 / 本地文本）+ "反讲" / "讲一遍 PRD" / "扫一遍 PRD"
- PRD 大版本改完，重跑刷新反讲文档
- 新功能开发前的需求消化阶段

## 何时不用

- 已经动手开发，要技术方案 → 普通开发流程
- PRD 还没出（只有口头需求）→ 先催 PRD
- 小细节改动（< 半天工作量）→ 不值得做反讲
- 查代码注释跟 PRD 同没同步 → 那是 `cmm-drift-prd`，不是本 skill

## 核心原则

1. **章节编号全用 PRD §X.X，绝不引入自己的 01/02/03** — PM 一眼跳回 PRD
2. **严格按 PRD 自上而下顺序串讲** — PRD 怎么排反讲就怎么排
3. **跨节合并必须 blockquote 显式说明** — 例 PRD §8.4 Mobile + §8.5 PC 合成一节讲时，头部要一句话讲清楚为什么合
4. **跨页面零件 inline 到首次使用处** — PRD §3 的图像上传 / 搜索框等公共组件，inline 进首次依赖章节，不抽公共节让读者来回翻
5. **弹窗用 `弹窗 N` 全文唯一编号** — 跨章节不重置；**不用 🪟 / 任何 emoji icon**
6. **📱/🖥️ 差异内联标** — 同一段 list/table 里用 emoji 区分，不分两份文档
7. **dev 第一人称 + 主动挑刺** — "我范围内"、"我没把握"；PRD 矛盾直接 ⚠️ warn block + 文末待决策表点名
8. **每个论点都能 trace 到 PRD** — 章节用 §X.X 锚定，细节 bullet 该带 PRD 关键词 / 行号也别省

## 风格红线

- ✅ 手边有一份已确认过的反讲 HTML 就拿来当风格锚点；没有就照本文 §核心原则 + §HTML 生成规范 走（版式一律用 `assets/handbook-template.html`，别另起炉灶）
- ✅ 第一人称、敢下判断："这块 PRD 没写清，我倾向 A，因为……"
- ❌ 别打官腔："本文档旨在..." / "建议产品同学进一步明确..." 都不行
- ❌ 别看到 PRD 矛盾不说，自己脑补一个版本写进去 —— 矛盾要进 ⚠️ warn block + 待决策表
- ❌ 别堆形容词凑篇幅；一句能讲清的不写三句

## PRD 获取

按手头线索取 PRD 原文（替代旧 prd-extract 流程）：

1. **飞书 URL** → 用 `social-proxy-documents` MCP 的 `get_document` 拉全文。大文档默认前 50000 字 + has_more，按 offset 翻页**直到覆盖所有要讲的章节**（漏翻会把没读到的章节误判成「缺」）。
2. **本地文本 / 文件** → 用户直接粘的，或 `--prd-file <路径>`，Read 即可。
3. **只给了项目昵称没给链接** → 查 `~/Desktop/cc-memory/onlychat/features.md` 里该 worktree 的 `PRD:` 字段拿飞书链接，再走第 1 条。

## 工作流

### 模式判定

落地路径固定：`~/Desktop/cmm/onlychat-World-Path/MM.DD-<需求名>反讲.html`

- 路径**不存在** → Fresh mode（首次反讲）
- 路径**已存在** → Refresh mode（PRD 改了重跑，按 delta 更新）

### Fresh mode（首次反讲）

1. **拉 PRD** → 见 §PRD 获取
2. **提章节目录** — 从 PRD 提出 §X.X 骨架，决定反讲 h2 / h3 顺序
3. **起 HTML 骨架** — `cp` 本 skill 的 `assets/handbook-template.html` 当底稿（左侧粘性目录 + 进度条 + 暗亮双模已配好），不要手写版式；细则见 §HTML 生成规范
4. **按 PRD 顺序填内容** — 每节一个 h2 带 `<span class="badge badge-prd">§X.X</span>`；弹窗用 `<span class="modal-tag">弹窗 N</span>`
5. **同步开待决策列表** — 读 PRD 时遇到矛盾 / 缺文案 / 反直觉直接塞 Q1 / Q2 ...，每条**必须**带 PRD 出处（§X.X 或行号）
6. **挑刺自检** — 见 §自检清单
7. **文末收 N 个待决策** — P0 用 `.qrow` 卡片（必须含 PRD 出处），P1 用 ul

### Refresh mode（PRD 改完重跑）

判定：落地路径已存在 → 刷新而非重写。

1. **拉新 PRD** + Read 旧反讲 HTML
2. **diff PRD § 树**：
   - 旧反讲覆盖了哪些 §？提取 `<h2>...§X.X</h2>` 列表
   - 新 PRD 哪些 § 改了内容 / 新增了 / 删除了
3. **定向重写受影响的节**，unchanged 节保留原文（别全文重跑浪费 + 引入 drift）
4. **顶部 cover 加"更新记录"块**：用 blockquote 列出本次刷新覆盖了 PRD 哪几节、增删了什么、新增 / 解决了哪些 Q
5. **待决策表迭代**：PM 已答的 Q **保留编号**改成 ✅（或移到"已决"分组），不要让 Q2 升格 Q1（保历史 trace）；新发现的矛盾插到 P0 / P1

**Refresh 必做检查**：
- 保留旧 Q 编号
- 待决策 Q 删除时，正文 `（见 QN）` 交叉引用同步清理（grep `见 Q` 验证）

## HTML 生成规范

单文件 HTML，`<style>` 内联，**不外链**。暗 / 亮双模（跟随系统 + 顶部一个手动切换按钮）。可发飞书 / 群、可打印。

**必备 CSS 类（类名固定，下游靠它认结构）**：

| 类名 | 用途 |
|---|---|
| `.badge-prd` | 章节徽章，显示 §X.X，跳回 PRD 用（底稿里就叫这个，别写成 `badge badge-prd`） |
| `.modal-tag` | 弹窗 N 唯一编号标记 |
| `.warn` | PRD 矛盾 / 风险的 ⚠️ 警示块 |
| `.qrow` | 文末 P0 待决策卡片（含 PRD 出处） |
| `.big-card` | 整页一句话的大字强调卡（克制用，全帖 1~2 张） |
| `.plat-pc` / `.plat-mobile` | 🖥️ / 📱 平台差异内联标 |

**底稿：`assets/handbook-template.html`（cp 一份改，别再手写版式）**

反讲动辄十几节 + 十几个 Q，PM 在会上要来回跳 —— 单栏无目录的页面撑不住。底稿是学习手册式：

- 顶端标题栏 + **左侧 190px 粘性目录** + 正文最大宽 1120px + 顶部阅读进度条
- 900px 以下自动收起目录转单栏；`@media print` 已配好（去目录/进度条/切换钮，warn 与 qrow 不跨页断）
- 暗 / 亮双模：跟随系统 + 右上角手动切换按钮

> 底稿来自 codex 侧 `~/.codex/skills/longform-html/assets/learning-handbook-template.html`，
> 已在本 skill 的 assets 下**落成独立副本**并补了暗色 token（原稿是 light-only，与自检第 12 条冲突）
> 与反讲专属组件。**用本地这份，不要跨 skill 目录引用**，本 skill 仍是自包含的。

**除上表的必备类外，底稿还带这些通用组件**（够用就别自造）：

| 类名 | 用途 |
|---|---|
| `.matrix` | 对照表（表头深绿反白），凡是「N 项 × 属性」一律用它，别写成散文 |
| `.card` / `.cards` | 单卡 / 双列卡片组 |
| `.note` | 蓝色信息块（**中性说明**，与 `.warn` 分工：warn 只给 PRD 矛盾） |
| `.steps` | 带序号圆点的施工步骤流 |
| `.diagram` | 深色等宽块，画链路 / 流程 ASCII 图 |
| `.scope` | 绿色范围声明块（只反讲部分章节时，开头必放） |
| `.section-kicker` | h2 上方的小号橙字眉标 |

**用法**：cp 底稿 → 换 `{{TITLE}}` → `<nav>` 里逐节补 `<a href="#s-3-1">§3.1 …</a>`（**每项必须指向真实 section 的 id**）→ `<main>` 里每节一个 `<section id="s-X-X">`。

## 自检清单

落档前逐条过（对应 §核心原则，全 ✅ 才算交付）：

1. 章节号全是 PRD 的 §X.X，没有自创 01/02/03？
2. 反讲顺序 == PRD 自上而下顺序？
3. 跨节合并处都有 blockquote 讲清为什么合？
4. 公共零件（上传 / 搜索框等）inline 在首次使用处，没单抽公共节？
5. 弹窗编号全文唯一、不重置、无 emoji icon？
6. 📱/🖥️ 差异用内联标，没拆成两份文档？
7. 每个 PRD 矛盾都进了 ⚠️ `.warn` 块 + 文末待决策表，没有脑补版本？
8. 每个论点都能 trace 回 §X.X（带关键词 / 行号）？
9. 全文第一人称、有判断、无官腔？
10. 待决策每条都带 PRD 出处？P0 用 `.qrow`、P1 用 ul？
11. 飞书大文档分页翻全了，没有把没读到的章节误判成「缺」？
12. 只产出 `.html`，没留中间 `.md`？暗/亮双模都正常？
13. 左侧目录每一项都指向真实存在的 `section` id，点了真能跳？没有孤儿锚点 / 漏掉的节？
14. 「N 项 × 属性」的内容都进了 `.matrix` 表，没有摊成散文让读者自己重拆？

## 输出

- 路径：`~/Desktop/cmm/onlychat-World-Path/MM.DD-<需求名>反讲.html`
- 格式：单文件 HTML，自带 CSS（暗 / 亮双模式），可发飞书 / 群、可打印
- 只产出 `.html`，**不要中间 `.md`**

## 示例输出（结构骨架）

```html
<!-- nav 里：<a href="#s-3-1">§3.1 用户注册</a> -->
<section id="s-3-1">
  <h2>用户注册 <span class="badge-prd">§3.1</span></h2>
  <p>我的理解：注册要走邮箱 + 手机双验证……</p>
  <table class="matrix"><tr><th>字段</th><th>必填</th></tr>…</table>
  <div class="warn">⚠️ PRD §3.1 说"必填手机"，但 §3.4 流程图里手机是可跳过的 —— 打架，见 Q2。</div>
  <p>弹窗 <span class="modal-tag">弹窗 1</span>：验证码错误 toast……</p>
</section>
...
<section id="s-q">
  <h2>待决策</h2>
  <div class="qrow"><span class="qid">Q2</span> <span class="src">（PRD §3.1 vs §3.4）</span><br>
  手机号到底必填还是可跳过？我倾向必填，因风控。</div>
</section>
```

## 跟其他 skill 的关系

- 反讲完 → PM 确认 → 若 PRD 再改就重跑本 skill（Refresh mode）
- 查代码注释跟 PRD 漂移 → `cmm-drift-prd`（本 skill 只审 PRD 自身）
- 真正开发用 `onlychat-figma-revamp`（有 Figma 时）或普通开发流程
