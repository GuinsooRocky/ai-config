---
name: project_soliloquy_product_over_seo
description: soliloquy 根路径归产品面市场，SEO 让路住内容页——别再拿可索引性反过来限制产品
metadata: 
  node_type: memory
  type: project
  originSessionId: b8a60c02-7961-46ec-8eb1-35465d5a15b7
  modified: 2026-08-15T18:33:49.653Z
---

**soliloquy 的排序是「产品优先，SEO 让路」，不是反过来。** owner 反复讲过，计划第一段原话就是「SEO 页留在同域但**不挡道**」。

- `https://soliloquy.live/` = **产品面的角色市场**（`shared/ui/components/OcMarket`，就是现在 `/app` 那个：多列海报卡、热门/性别筛选、标签行、每张卡带开聊/收藏/点赞/聊天数、无限滚动）。
- 它是客户端渲染的 ⇒ **根路径对爬虫是空壳，owner 已明确接受**。SEO 由 `/characters`、`/character/[slug]`、`/blog`、`/pricing` 这些内容页承担。
- **别再提「服务端直出 + 客户端替换」的混合形态**：实测代价是秒级整页换脸（要等两次网络往返 + 解析大词典），已否决。

## 🔴 「市场」这个词有两个所指，先确认再动手
| | |
|---|---|
| **产品面市场**（owner 说的那个） | `(product)` 组、客户端、多列海报卡、能筛选/收藏/点赞/开聊/无限滚动 |
| **营销面角色列表**（不是他说的那个） | `(web)` 组、服务端直出、两列稀疏卡、点卡跳详情页、一页 24 张 |

**Why:** 2026-08-08 我把两者搞混了一整天，在营销面那个上反复压 hero 高度、删介绍带，越做越细也越做越偏。根因是**从没问过一句「你说的是哪个页面」**。

**How to apply:** owner 说「市场 / 首页 / 打开就是产品」时，先确认指的是哪一个（截图或路径），再动手。以及：他要聊的是**访客落在哪、点了去哪、卡在哪**（链路），不是版式——版式我判断不了，今天连错三次（详见 [[feedback_product_chat_stay_at_flow_altitude]]）。相关：[[project_soliloquy]]。

## 「产品」这个词 owner 已焊死（2026-08-15）

原话：**「我说的产品永远都是用户用的那一套」** = `(product)` 组 + 桌面客户端，共用 `shared/ui/components/OcDetail` 和 `shared/data/supabase.ts`。

- SEO 页（`(web)` 组、`/character/[slug]`）**不算产品**。它缺什么功能都不构成缺口——我把「官网详情页没查 `gallery_urls`、导入的图那儿看不到」当成阻塞报上去，被直接否掉：「官网 SEO 详情也不需要」。
- 报缺口前先分清是哪一面缺；只有 `(product)` 那面缺才值得说。

## 获客面不进走查（2026-08-16 明令）

走查/演示/「用户视角」默认指**产品面**；`(web)` 获客页只在 owner 点名时才碰。当天事故：移动端走查被登录墙挡在产品面外，我顺手扫了获客页，owner 被这页轮番轰炸到发火。仓内已落 `decision-0.1.0-seo-surface-never-shown-to-users`（登录用户访问获客路由一律送进产品面、产品内不得链去获客页），并在仓 CLAUDE.md / 坑位账 / `(web)/README` / dev 角标四层打了路标——先看仓内路标，别只凭这条记忆。
