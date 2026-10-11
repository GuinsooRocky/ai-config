---
name: check-main-before-product-advice
description: 在叠在未合入分支上的工作树里给产品建议（尤其钱相关）前，先看 origin/main 最近改了什么，别拿分支底座的旧口径出主意
metadata:
  node_type: memory
  type: feedback
  originSessionId: 0909fad3-d9fe-4d37-871f-ad9addd721a3
  modified: 2026-10-11T04:30:45.503Z
---

分支叠在一条没合进 main 的功能分支上时，工作树里的 PRD、代码和文案都是那条分支开工时的样子。main 在这期间可能已经换了产品口径，分支里看不出来。

**Why:** 2026-10-11 soliloquy 画布优化收尾，我按画布 PRD（10-09）的「花钱前必须露价」建议保留出图和试聊的扣费确认，还在报告里写了「一张 20 点」。其实 main 在 10-10 已经上了额度系统（T290），用户只看剩余百分比，内部点数不给用户看。owner 回：「为什么要有价格 你看下代码 我们都尽量少价格吧。。。。 走的不是百分比嘛」。

**How to apply:**
- 给 owner 列待拍、提产品建议、写「保留/去掉 X」之前，先跑 `git fetch` 加 `git log origin/main --oneline -200 | grep <领域关键词>`，再看对应的现行规格和 PRD 在 main 上的版本（`git show origin/main:<路径>`）。
- 分支底座与 main 口径冲突时，以 main 和 owner 最新的话为准。冲突本身要写进汇报，不要默默沿用旧口径。
- soliloquy 的具体计费口径不记在这里，去仓里的 `docs/logic/模型供给与会员现行规格.md` 和额度 PRD 现读。

相关：[[feedback_not_ground_truth]]、[[feedback_project_intel_stays_in_project_docs]]
