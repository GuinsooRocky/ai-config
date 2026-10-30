---
name: check-project-prohibitions-before-saying-right
description: owner 问「这么做对吗、对就放行」时，先查项目 CLAUDE.md「不许做的事」和决策账，再答对不对；与项目铁律冲突要先说出来让他拍
metadata:
  node_type: memory
  type: feedback
  originSessionId: 21f8e6e4-a2f8-488b-9901-f2795af537ee
  modified: 2026-10-30T09:09:52.256Z
---

owner 问「你觉得这么做对吗，对就放行」，是把判断交给我；答「对」之前，要先把项目自己写死的禁令过一遍（项目 CLAUDE.md 的「不许做的事」「边界」、决策账），冲突就当场说出来，让他决定要不要推翻。

**Why:** 10-30 perf-lab 换尺子后，owner 提议「直接改之前的数据」省掉 A/A，问我对不对。我只从统计角度论证了可行，就答「对」，并改写了 5 轮旧数据的 config_sha。之后比较器又以「每档测量次数不一样」拒比，我才读到仓根 CLAUDE.md 白纸黑字写着「不许混比 config_sha 不同的轮次……拒比不绕」「不给旧记录补造字段让它变得可比」。

**How to apply:** 碰到「改历史数据 / 绕过检查 / 混比」这类动作，先 grep 项目 CLAUDE.md 和决策账里的禁令，再给判断。owner 仍要做，就在决策账追加一条推翻对应规则，再动手。见 [[record-owner-decisions-and-check-before-listing-gaps]]、[[crushon-ai-perf-lab]]。
