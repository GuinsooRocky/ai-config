# 市面上的学习设计框架：各自贡献了骨架的哪一块

2026-09-10 检索整理。八个框架，没有一个单独够用；本 skill 的骨架是它们的交集加上本机偏好（大白话、贯穿例用真活、HTML 落地）。

## 一张表

| 框架 | 核心主张 | 进了骨架的哪里 |
|---|---|---|
| Merrill 首要教学原理 | 学习发生在解决真实问题的循环里：激活 → 演示 → 应用 → 整合 | 每章八块的主轴：情境 / 先做 / 演示 / 自己动手 / 攒规格 |
| UbD 逆向设计（Wiggins & McTighe） | 先定目标，再定「拿什么证明学会了」，最后才排内容；检验要求迁移不是复述 | 步骤 1 目标—检验表；冷测全部换场景 |
| 4C/ID（van Merriënboer） | 复杂技能按「整任务」从简到难排，脚手架递减；支持信息挂在任务类上 | 步骤 3 能力阶梯 + 脚手架递减；贯穿例 = 整任务 |
| Gagné 九事件 | 引起注意 → 告知目标 → 唤起旧知 → 呈现 → 引导 → 练习 → 反馈 → 评估 → 迁移 | 八块的顺序；第 0 章的目标表 |
| 认知负荷理论 / 样例效应（Sweller、Renkl） | 新手先看带全步骤的样例，再做「填空式」问题，最后独立解题；渐隐优于交替 | 演示块给全步骤；后几章只给任务 |
| Make It Stick（Brown、Roediger、McDaniel） | 提取 > 重读；间隔、交错、生成、精细化；「合意困难」 | 先做在概念之前；回头题；冷测隔三天 |
| Matuschak 记忆媒介（Quantum Country） | 书不管用是因为「读了就会」这个假设是错的；每 ~1500 词嵌一组问题并间隔复习 | 问题密度每 ~1000 字一停；答案折叠 |
| Diátaxis 教程（Procida） | 教程 = 做中学：可控环境、单一路径、具体、小步、早出结果 | 贯穿例单一路径；搭 + 破早出结果 |

## 各框架一段话

**Merrill**：五条原理——问题中心、激活、演示、应用、整合——按循环反复用，不是线性走一遍。对本 skill 的直接影响：每章都是一个完整小循环，不是「前半本讲理论后半本做题」。

**UbD**：三阶段——期望结果（持久理解 + 基本问题 + 知识技能）→ 评估证据（先设计表现任务）→ 学习计划。最容易被跳过的是第二阶段：大部分「学习文档」直接从第一阶段跳到第三阶段，自测是事后补的，所以只能复述。

**4C/ID**：四件套——学习任务、支持信息、程序信息、部分任务练习。学习任务是骨干，按复杂度分类，同一类内变化、脚手架逐渐撤掉。贯穿例逐章加一层就是它的「任务类」。

**Gagné**：九件事是模块不是剧本，可以重排、缩放。本 skill 把它压成八块，去掉了「告知目标」（提到第 0 章统一做）。

**样例效应**：新手直接解题反而学得差，因为工作记忆被搜索耗光；先给完整样例，再逐步抽掉步骤（完成型问题），最后独立做。演示块必须带中间步骤，就是为这个。

**Make It Stick**：重读和划线是「感觉学会了」的错觉；提取练习（自测）、间隔、交错、生成（先猜再看）才留得住。「先做」块放在概念之前，是生成效应；回头题是交错；冷测是间隔。

**Matuschak**：《Why books don't work》的论点是书和讲座都默认「传输主义」，而这是假的。Quantum Country 的做法是把提取练习直接嵌进正文并做间隔复习。静态 HTML 做不了自动间隔，本 skill 用「冷测隔三天」和 localStorage 进度替代。

**Diátaxis**：教程和 how-to 的区别在于教程负责让人学会，how-to 负责让人完成。教程的纪律：可控环境、单一路径不给选项、具体不抽象、小步、早出结果、反复。贯穿例不许中途换，就是「单一路径」。

## 来源

- Merrill：https://students.tippie.uiowa.edu/tippie-resources/technology/instructional-design/models/merrill ；https://elearningindustry.com/merrills-principles-instruction-definitive-guide
- UbD：https://files.ascd.org/staticfiles/ascd/pdf/siteASCD/publications/UbD_WhitePaper0312.pdf ；https://jaymctighe.com/resources/
- 4C/ID：https://www.4cid.org/about/ ；https://edutechwiki.unige.ch/en/4C-ID
- Gagné：https://www.niu.edu/citl/resources/guides/instructional-guide/gagnes-nine-events-of-instruction.shtml
- 样例效应：https://link.springer.com/article/10.1023/B:TRUC.0000021815.74806.f6 ；https://www.sciencedirect.com/science/article/abs/pii/S0747563208002161
- Make It Stick：https://www.retrievalpractice.org/make-it-stick ；https://cirl.etoncollege.com/desirable-difficulties/
- Matuschak：https://andymatuschak.org/books/ ；https://www.dwarkesh.com/p/andy-matuschak
- Diátaxis：https://diataxis.fr/tutorials/ ；https://diataxis.fr/tutorials-how-to/
