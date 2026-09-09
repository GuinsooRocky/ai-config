---
name: feedback-run-scoped-tests-not-full-suite
description: 案例存档（规则主干已在 CLAUDE.md「验多少」）：全量被判「这个很蠢」、`--changed` 假增量实跑 11893、测试文件漏 lint 被拦 38 个 error
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5558d432-8159-4aac-bab7-6b7d3125be99
  modified: 2026-08-17T15:46:34.350Z
---

> **规则主干已提级 `~/.claude/CLAUDE.md` 写码行为守则「验多少」节**（每 session 强制加载）；本文件只留立法案例，别在这里找操作口径。

**How to apply**：验证动作照 CLAUDE.md「验多少」执行；本文件只在需要立法现场 / 复发史时回看。

**Why（立法现场，四次）**：

- **2026-08-17 立法**：改完一处就跑全量测试套件（soliloquy 桌面端 447 文件 / 5166 测试），owner 当场说「这个很蠢」。全量套件对一个 CSS 改动毫无判别力——既证明不了样式对，又把真正的证据（运行时渲染）挤到后面。owner 要的是「你验的东西能不能判定这次改动」。
- **2026-08-18 提级**：规则原住 memory（抽签召回、背景级），反复没被召回导致失效，正文写进 CLAUDE.md。
- **2026-08-19 复发（`--changed` 假增量）**：写了 `vitest run --changed` 就当作已经是增量了，实跑回来 11893 passed——`--changed` 会扇出成整库（改到被广泛 import 的文件 / base 选错都会），还照原样报给 owner。由此补出 CLAUDE.md 的「干跑先看清单 + 四位数熔断」两条。
- **2026-07-11 测试代码漏过 lint**：onlychat create-test 战役全程只跑 vitest+tsc，pre-commit 的 gts ESLint 一次拦下 38 个非自动修复 error——测试文件也是代码，也要过仓库 lint，别只看测试绿。（已提级为 CLAUDE.md「测试代码也是代码」那条）

参见 [[feedback_just_do_no_stop_suggestions]]、[[project_soliloquy]]。
