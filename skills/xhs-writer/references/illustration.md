# 小黑式正文配图 · prompt 产出线

xhs-writer 的配图子线。触发：「配图」「出配图 prompt」「画个小黑」「shot list」「这篇哪里值得配图」。

**这条线只产出 prompt，不出图。** 本机没有出图 MCP/工具——产出 shot list + 可直接粘的 prompt，用户拿去**自己的出图网站**跑。别试图调 image_gen / 任何画图工具。

> 移植自 helloianneo/ian-xiaohei-illustrations（MIT）。方法论 + 小黑 IP 照搬。
> ⚠️ 小黑是原作者的固定视觉 IP。自用/试水可照搬；**公开大量发布前考虑换成自己的角色或纯抽象**，避免视觉撞签名。

---

## 它在做什么

不是"给文章配张装饰图"，而是把文章里**一个关键认知动作**（判断 / 流程 / 状态 / 隐喻）画成一张干净怪诞的手绘图，小黑承担核心动作。

一篇配 4-8 张，**只挑认知锚点**——核心判断、转折、输入输出回路、前后对比、角色切换——不要平均铺。

---

## 四步流程

### 第 1 步 · 先出 shot list（别急着出 prompt）

读完正文，列一张 shot list（4-8 张），每条写清：
- 放在文章哪里
- 视觉主题 + 核心意思
- 结构类型 + 小黑在干什么
- 建议元素 + 中文标注词

先给用户过 shot list，确认后再逐张出 prompt。

### 第 2 步 · 逐张出 prompt（一张一个，别拼）

套下面「生图提示词模板」，按这张图的内容替换变量。一次产出一张的完整 prompt，用户粘去自己网站。

### 第 3 步 · QA

用户出完图贴回来 / 或描述问题 → 按「QA 失败信号」判，给「图像编辑提示」或重写 prompt。

### 第 4 步 · 命名

最终图建议命名 `01-<主题>.png`、`02-…` 顺序排。

---

## 生图提示词模板

每张图单独生成。根据正文替换变量，不要把多张图拼一起。

```text
Generate one standalone {画幅} Chinese illustration.

Visual DNA:
Pure white background. Minimalist black hand-drawn line art. Slightly wobbly pen lines. Lots of empty white space. Sparse red/orange/blue handwritten Chinese annotations. Clean absurd product-sketch feeling. No gradients, no shadows, no paper texture, no complex background, no commercial vector style, no PPT infographic look, no cute mascot poster, no children's illustration, no realistic UI.

Recurring IP character required:
小黑, a small solid-black absurd creature with white dot eyes, tiny thin legs, blank serious expression, slightly uneven hand-drawn body shape. 小黑 must perform the core conceptual action, not decorate the scene. Make 小黑 serious, deadpan, and slightly bizarre, not cute.

Theme:
{正文配图主题}

Structure type:
{结构类型：Workflow / 系统局部 / 前后对比 / 角色状态 / 概念隐喻 / 方法分层 / 地图路线 / 小漫画分镜}

Core idea:
{这张图要表达的核心意思}

Composition:
{具体画面：小黑在哪里、正在做什么、主要物件是什么、信息如何流动}

Suggested elements:
{元素1} / {元素2} / {元素3} / {元素4}

Chinese handwritten labels:
{标注词1} / {标注词2} / {标注词3} / {标注词4} / {可选标注词5}

Color use:
Black for main line art and 小黑. Orange for main flow/path/arrows. Red only for key warnings/problems/results. Blue only for secondary notes or feedback/system state.

Constraints:
One image explains only one core structure. Keep the main subject around 40%-60% of the canvas. Preserve at least 35% blank white space. Use at most 5-8 short handwritten Chinese labels. Do not write a title in the top-left corner. Do not write the structure type on the image. Do not make it a formal diagram, course slide, or dense explainer. Do not copy prior examples or reuse known case compositions unless explicitly requested; invent a fresh visual metaphor for this specific article. It should be clear but not instructional, interesting but not childish, strange but clean.
```

**`{画幅}` 取值**：
- 整张卡当插画发 → `4:5 vertical (1080x1350)` 小红书 feed 流标准竖图
- 嵌进现有 9 图卡片当横插 → `16:9 horizontal`（小黑原生比例，留白最足）
- 公众号长文正文 → `16:9 horizontal`

### 图像编辑提示 · 去掉左上角标题
```text
Edit the provided image. Remove only the handwritten title "{要删除的文字}" and its underline from the top-left corner. Fill that area with the same clean white background, matching the surrounding blank paper. Preserve everything else exactly: characters, labels, paths, line style, composition, aspect ratio, and image quality. Do not add any new text or objects.
```

### 图像编辑提示 · 增强怪诞感
```text
Regenerate this illustration with the same core meaning and simple layout, but make 小黑 more central to the conceptual action. 小黑 should be doing the strange work that explains the idea, not standing beside the diagram. Keep it clean, sparse, hand-drawn, and not cute.
```

---

## 风格 DNA（校准用，写 prompt 时心里有数）

纯白、极简、手绘、留白、克制、怪诞、产品草图感、中文手写感、结构清楚但不像说明书。像一个长期做 AI/产品/设计/开发工具的人，在白纸上随手画的解释草图。

**颜色（克制，宁少不多）**：黑=主体线稿/角色/框线/主文字；红=重点/问题/情绪/关键提醒/结果；橙=主流程/路径/箭头/A→B 移动；蓝=补充说明/脑内状态/系统状态/AI 提示（不是每张必用）。

**绝对不要**：商业插画 / PPT 信息图 / 正式流程图 / 课件 / 可爱卡通海报 / 儿童插画 / 复杂架构图 / 精致扁平 / 科技感 UI / 真实 App 截图 / 复杂背景渐变阴影纹理 / 左上角写"Workflow·系统架构·常见坑·路线图"类型标题。

---

## 小黑 IP

黑色实心小怪物，白色圆点眼，细腿偶有细胳膊；身体可变圆柱/黑豆/黑盒/漏斗/影子/洞口；轮廓略不规则有手绘感；表情空、呆、冷静、认真。**不是吉祥物**——是认真参与系统运转的荒诞工作者：冷幽默、不卖萌、有点笨拙但不蠢。

**承担核心动作**：搬素材 / 拉线汇聚信息源 / 卡在断点 / 在机器里扳"判断"杆 / 变筛选漏斗 / 切素材鱼 / 盖章 / 牵承接路径 / 举警告牌 / 从洞里伸手接不住 / 搬砖搭桥开门分拣记录。

**判断标准**：去掉小黑，核心隐喻还完全成立 → 说明小黑太装饰了，重写让它成为动作主体。

---

## 结构类型（选一种，别混）

| 类型 | 适合 | 画法 |
|---|---|---|
| Workflow 流程 | 输入→处理→输出、内容生产、自动化链路 | 左输入·中小黑/怪机器处理·右输出·橙箭头主流向 |
| 系统局部 | 信息源、过滤器、库、agent 局部 | 只画 3-5 核心模块，小黑参与其一 |
| 前后对比 | 乱/序、手动/自动、分散/收拢、焦虑/稳 | 左乱右稳，中橙箭头，角色可夸张 |
| 角色状态 | 用户痛点、工具太多、信息焦虑、卡住到跑起来 | 2-4 个小状态，每个一短标注 |
| 概念隐喻 | 内容工厂、信息仓库、脑内黑盒、自动日报 | 一个大怪物件/机器，少量输入，一个输出，有记忆点 |
| 方法分层 | 方法论框架、能力栈、系统分层 | 一层层盒子（别正式金字塔），小黑在旁搬砖搭建 |
| 地图路线 | 想法到上线、用户路径、学习路线 | 一条弯路径少量节点，小黑牵线或走 |
| 小漫画分镜 | 失败到成功、真实过程、吐槽、前后变化 | 2-4 小格，每格一个动作 |

### 原创隐喻三步（每篇重新发明，禁照搬旧图）
1. 抽象概念 → 物理动作：卡住/漏掉/变重/分拣/沉淀/发酵/开门/折叠/拆包/回流
2. 系统结构 → 低科技物件：坏机器/纸箱/抽屉/水管/邮筒/怪表盘/秤/井/梯子/怪工位
3. 让小黑承担动作：卡在机器里/拉错线/守门/搬运/修补/称重/扶梯子/记录/塞进怪装置

物件池用时只选 1-2 个别堆满；小黑动作池：拉/扛/塞/捞/压/称/缝/剪/拧/守/推/接/拆/标记/回收。

---

## QA Checklist

**必过**：16:9 或指定画幅 · 干净白底 · 有小黑且承担核心动作 · 为本篇新发明的隐喻（非复刻）· 怪诞有创意 · 简洁主体≤60% · 一图一核心 · 中文标注少短可读 · 橙只用主路径/箭头 · 红只用重点/问题/结果 · 蓝只用补充/反馈/系统态。

**失败信号 → 重生成或局部编辑**：左上角有类型标题 · 小黑像吉祥物/表情包/可爱卡通 · 像 PPT/课件/正式流程图 · 元素箭头节点太多 · 文字成大段解释 · 背景有纸纹阴影渐变米色噪点 · 真实 UI 截图 · 中文错字/标注不可读 · 太死板没荒诞隐喻。

**迭代**：太普通→让小黑成动作主体+一个奇怪但成立的隐喻；太复杂→删节点只留一动作+3-5 短标注；太可爱→强调 deadpan/blank serious/not cute/not mascot；太 PPT→去标题边框网格箭头改手绘场景；文字错→优先局部编辑，错多则重生成并减标注数。

**交付判断**：好图让人先觉得"有点怪"，再 1 秒内看懂结构。第一眼像教程页而非白纸上的怪诞产品草图 = 不合格。
