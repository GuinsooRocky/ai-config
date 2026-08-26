---
name: feedback-run-scoped-tests-not-full-suite
description: 验证改动只跑相关测试别全量；`--changed` 会退化成全量要先干跑看清单，四位数测试数即熔断；纯 CSS 改动跳单测走运行时
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5558d432-8159-4aac-bab7-6b7d3125be99
  modified: 2026-08-17T15:46:34.350Z
---

改完一处就跑全量测试套件（soliloquy 桌面端 447 文件 / 5166 测试）被 owner 当场说「这个很蠢」。
按改动面选测试：碰了哪个组件就跑那个组件的测试文件；纯 CSS / 样式改动没有单测覆盖，
直接跑运行时截图 + 像素取样走查即可，别拿全量套件充验证。

**Why**：全量套件几十秒到几分钟，对一个 CSS 改动毫无判别力——它既证明不了样式对，
又把真正的证据（运行时渲染）挤到后面。owner 要的是「你验的东西能不能判定这次改动」。

**How to apply**：
- **首选让工具算，别自己猜**：`vitest run --changed`（未提交改动）/ `vitest run --changed origin/develop`（整分支），
  vitest 顺 import 图反算受影响测试；实测 onlychat + soliloquy 的 vitest 4 都支持
- 改了组件 A（工具不可用时）→ `vitest run <A的测试文件>`
- 改了 CSS / 布局 → 跳过单测，直接 headless 截图 + `getBoundingClientRect` / canvas 取像素
- 要证明某个失败是既有的（不是自己碰出来的）→ `git stash` 后单跑那一个文件对比，别全量跑两遍
- 全量只在真正的大面积重构 / 升级批次收尾时跑一次

**2026-08-19 复发（`--changed` 假增量）**：写了 `vitest run --changed` 就当作已经是增量了，
实跑回来 11893 passed —— `--changed` 扇出成整库（改到被广泛 import 的文件 / base 选错都会），
还照原样报给 owner。两条补丁已进 CLAUDE.md：跑前先干跑清单 `npx vitest list --filesOnly --changed [base]`
（vitest 4 实测可用；soliloquy 全库 1042 个测试文件做量级参照），数量四位数就是全量回来了；
已经跑起来才发现的当场 Ctrl-C，跑完了才发现的那次不算增量验证、报告里不许写成增量。

**2026-08-18 已提级**：本规则正文写进 `~/.claude/CLAUDE.md` 写码守则「验多少」段——
memory 是抽签召回 + 背景级，反复没被召回导致规则失效；CLAUDE.md 每 session 强制加载。本文件留作案例存档。

**测试代码本身也要过 lint**：onlychat create-test 战役（2026-07-11）全程只跑 vitest+tsc，pre-commit 的 gts ESLint 一次拦下 38 个非自动修复 error——测试文件也要过仓库 lint，别只看测试绿。

参见 [[feedback_no_pending_verification_lists]]、[[project_soliloquy]]。
