---
name: refactor-risk-tiers
description: 评审提的结构重复/重构类改动按风险分三档：小改动直接改、中等只做 1:1 机械抽取、大或非 1:1 的不改只留 TODO+doc 对齐
metadata:
  type: feedback
---

评审（code review / ultrareview）报的「结构重复」类改动，owner 的口径是**保障没 bug 优先于对齐**，按风险分档：
- 小改动（类型必填、注释、纯机械）→ 直接改
- 中等改动 → 只做 **1:1 代码抽取**（外部行为逐字段/逐时机相同，能写出等价证明的）
- 大改动或抽不成 1:1 的（比如换了 hook 观察者生命周期、改了取数时机）→ **不改**，在代码留 TODO + 项目手册补一段对齐说明

**Why:** 2026-09-14 onlychat 付费图评审 F1/F2：F1 改的额度层线上恒 undefined、且已排在删除名单，F2 的弹窗那层抽 hook 会改 refetch 时机；owner 明说「大改动先不改、todo/doc 写一下；小改动可以改；中等 1:1 抽取不会太大问题——意思就是保障没 bug」。

**How to apply:** 接到评审改动先分档并把「为什么 1:1」写进方案（数学等价 / 同生命周期同入参）；派工时把不变量写死（哪层保留、哪个 prop 必填）；验收用改前基线按文件对照 + 反面验证。相关：[[feedback_fix_within_reported_scope]]、[[feedback_delegate_impl_to_opus_subagent]]
