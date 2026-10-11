---
name: public-means-public
description: soliloquy 公开面分级口径的演化：07-21「公开就是公开」已被 08-10 恢复三档取代（公开面只出全年龄）；别再当 bug 报、别再问第二遍，也别拿旧句翻闸
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 243bce9a-1376-4308-9452-cb239901cdbf
  modified: 2026-10-11T23:30:00.000Z
---

**现行口径（2026-08-10 owner 拍板，REDLINES #16）**：公开面（官网角色列表 / 首页封面墙 / A-Z / sitemap）由 `apps/web/lib/publicSurface.ts` 一处统一，生产总闸 `PUBLIC_CONTENT_SPLIT_OFF=false` → 公开面只出全年龄；成人分档只活在登录并确认年龄后的产品面（SFW / 18+ / 无限制三档）。代码注释里的「历史地层」写明：07-21 / 07-27 的「公开就是公开、不按 rating 过滤」已被 08-10 取代。

**历史（留痕防反复）**：07-21 owner 立「公开就是公开」，07-27 重申；07-26 我照审查报告给 `/characters` 加 `.eq('rating','sfw')` 被要求撤回；owner 原话「为啥一直一直一直问我这个问题」。

**Why:** 2026-10-11 全仓捉虫时 web2 分区发现 REDLINES #15 仍标「✅ 有效」、与代码注释和 08-28 对外 Safety 文案三处矛盾。核日期后确认是登记册文字过期，不是代码错。

**How to apply:**
- 审查报告把「公开面有 / 没有过滤成人卡」报成 bug 时，先按本条判：现行是「只出全年龄」，是 owner 08-10 的决定，不是缺陷；也**别再问第二遍**。
- 别拿 07 月那句「公开就是公开」当依据把总闸翻回 true；真要变口径只能 owner 当次明说。
- REDLINES #15 的文字该改成 ⚠️ 演化中、指向 #16（10-11 已列入 FINAL 的文档漂移清单）。
- 判据 `rating` 列打标不准（sfw 里混擦边图），收紧时要另补审核信号。
- 相关：[[project_soliloquy]]、[[project_soliloquy_bugscan_20261011]]
