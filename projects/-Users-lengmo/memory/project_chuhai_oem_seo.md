---
name: project_chuhai_oem_seo
description: "出海项目：标的=海外 AI 陪伴网站（soliloquy web 端即站，07-06 已拍）；现行真相已进 soliloquy 仓 docs/growth/SEO-GEO现行策略.md（archives v2 降为历史快照）；当前暂停，随 T296 改名换域，等 owner 明说恢复；原 OEM 尽调站方向已让位、弃留待拍；soliloquy 根路径归产品面市场，SEO 让路住内容页——别再拿可索引性反过来限制产品"
metadata: 
  node_type: memory
  type: project
  originSessionId: aeb6f304-3d01-445f-9ef3-6df4d1badae6
  modified: 2026-11-02T07:53:09.832Z
---

出海副业项目，2026-06-16 锁定方向，目标"先摸第一笔 $50 验证闭环"（非追大钱）。执行者=前端，每周约 4h。

**✅ 2026-07-06 标的与站型已拍：SEO/GEO 标的 = 海外 AI 陪伴网站，站型 = soliloquy web 端即站**（与 soliloquy OC 市场化同赛道；方案卡着的唯一前置决策由此解开）。产品化 PRD 落 [[project_soliloquy]] 仓 `docs/prd/designs/2026-07-06-SEO-web端即站.md`，同日前置的多语言方案在 `docs/prd/designs/done/2026-07-06-多语言i18n.md`（react-i18next、en 默认 + zh 首发；已挪进 `designs/done/`）。技术分叉已拍（PRD v2）：**整套 Next 壳、分两波迁移**（Wave 1 只建 SEO 面不动 SPA）。前置依赖=soliloquy credits 漏钱洞修复。

**✅ 2026-07-07 SEO 知识库收口，方案升 v2**：`archives/seo/` 按 00-PLAN 走完抓→学→落档全链（29 raw / 28 notes / 哥飞vs大牛对照表 / 22 条待实验清单，全过独立抽验零编造）。v2 当时是方案单一真相，**现已被 soliloquy 仓 `docs/growth/SEO-GEO现行策略.md` 取代（该文自称现行单一真相，旧方案只作假设来源；09-11 五路调研后改向）**，进度与判断一律去仓里现读；`archives/seo/gf/07.06-SEO-GEO方案.md` 已在开头自标 superseded（v1 快照，只作对照、别照此执行）；seo-planner skill 同步接地知识库（已证伪战术自动枪毙，meta-check 100）。PRD 待同步的 6 条增量列在方案 v2 §7。

**✅ 2026-09-13 多路查询（query fan-out）五路调研落档**：合成结论 + 七份原件在 soliloquy 仓 `docs/growth/research-2026-09-13/`（`00-合成结论.md` 含机制、被引共性、本站现状、每周 4 小时怎么分、不做清单），跨项目机制笔记在 `archives/seo/notes/09.13-GEO多路查询-五路调研合订.md`。第一批已上线（文章页可见更新日期、游戏角色页 CollectionPage dateModified、AI 面板改每题 3 趟并集）；S02 结构层补丁备在同目录；owner 拍板 8 篇冻结维持。owner 后台五个准入开关（Cloudflare AI 爬虫、GSC generative AI 开关与报表、preferred sources、Bing 索引）当时未核。

**原 P0 方向存档（已让位，弃留待 owner 拍）**：中立买方视角的**中国 OEM/ODM 工厂尽调站**（第一垂直=护肤/化妆品代工）。选它的理由是唯一咬住"能读中文工商记录 + 发中文询盘"这个不公平优势、且具名长尾 SERP 真空；变现走零点击（验厂机构 lead + 付费 shortlist，不挂 AdSense）；最大命门是 lead 供给侧关系=0。**从未起站**（W1 计划过期，本机没有对应站点代码），07-06 pivot 后整条让位。完整方案 + 三轮调研结论 + "别碰"清单在 `~/Desktop/archives/seo/gf/06.16-出海SEO选向-三轮调研与P0方案.md`（哥飞小册同目录），要捡回从那读。

**关键教训（2026 SEO/GEO 现实）**：纯事实 lookup 站死路——要么有独有数据护城河 + 零点击变现，要么被 AI Overview 零点击吃掉。三轮漏斗 pSEO 0/14 → 付费微产品 0/9（全死冷启动）→ SEO/GEO 修正版 3/11 存活。相关方法论见 `archives/seo/gf/` 的哥飞小册。

## 产品优先，SEO 让路

**soliloquy 的排序是「产品优先，SEO 让路」，不是反过来。** owner 反复讲过，计划第一段原话就是「SEO 页留在同域但**不挡道**」。

- `https://soliloquy.live/` = **产品面的角色市场**（`shared/ui/components/OcMarket`，就是现在 `/app` 那个：多列海报卡、热门/性别筛选、标签行、每张卡带开聊/收藏/点赞/聊天数、无限滚动）。
- 路由归属不变；公开访问现状看 `ops.product_access_state` 和功能控制现行规格：10-16 起转内部开放、注册关闭（匿名及普通账号看到 403 暂停页，不是故障），线上现值开工先核。
- 它是客户端渲染的 ⇒ **根路径对爬虫是空壳，owner 已明确接受**。SEO 由 `/characters`、`/character/[slug]`、`/blog`、`/pricing` 这些内容页承担。
- **别再提「服务端直出 + 客户端替换」的混合形态**：实测代价是秒级整页换脸（要等两次网络往返 + 解析大词典），已否决。

### 🔴 「市场」这个词有两个所指，先确认再动手
| | |
|---|---|
| **产品面市场**（owner 说的那个） | `(product)` 组、客户端、多列海报卡、能筛选/收藏/点赞/开聊/无限滚动 |
| **营销面角色列表**（不是他说的那个） | `(web)` 组、服务端直出、两列稀疏卡、点卡跳详情页、一页 24 张 |

**Why:** 2026-08-08 我把两者搞混了一整天，在营销面那个上反复压 hero 高度、删介绍带，越做越细也越做越偏。根因是**从没问过一句「你说的是哪个页面」**。

**How to apply:** owner 说「市场 / 首页 / 打开就是产品」时，先确认指的是哪一个（截图或路径），再动手。以及：他要聊的是**访客落在哪、点了去哪、卡在哪**（链路），不是版式——版式我判断不了，今天连错三次（详见 [[feedback_product_chat_stay_at_flow_altitude]]）。相关：[[project_soliloquy]]。

### 「产品」这个词 owner 已焊死（2026-08-15）

原话：**「我说的产品永远都是用户用的那一套」** = `(product)` 组 + 桌面客户端，共用 `shared/ui/components/OcDetail` 和 `shared/data/supabase.ts`。

- SEO 页（`(web)` 组、`/character/[slug]`）**不算产品**。它缺什么功能都不构成缺口——我把「官网详情页没查 `gallery_urls`、导入的图那儿看不到」当成阻塞报上去，被直接否掉：「官网 SEO 详情也不需要」。
- 报缺口前先分清是哪一面缺；只有 `(product)` 那面缺才值得说。

### 获客面不进走查（2026-08-16 明令）

走查/演示/「用户视角」默认指**产品面**；`(web)` 获客页只在 owner 点名时才碰。当天事故：移动端走查被登录墙挡在产品面外，我顺手扫了获客页，owner 被这页轮番轰炸到发火。仓内已落 `decision-0.1.0-seo-surface-never-shown-to-users`（登录用户访问获客路由一律送进产品面、产品内不得链去获客页），并在仓 CLAUDE.md / 坑位账 / `(web)/README` / dev 角标四层打了路标——先看仓内路标，别只凭这条记忆。
