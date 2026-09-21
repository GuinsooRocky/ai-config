---
name: feedback-owner-operates-from-admin-only
description: owner 日常只在后台（B 端）点，不在终端跑命令；需要他跑命令才能用的环节不进日常流程和验收清单，做成出事时再用的后备口子
metadata: 
  node_type: memory
  type: feedback
  originSessionId: dfebc5d2-85e8-4ab0-8e88-992f580f14e9
  modified: 2026-09-11T11:58:27.164Z
---

给 owner 设计流程或写验收步骤时，所有动作都要能在后台页面上完成。需要他在终端跑命令的环节（起本地服务、跑脚本）不写进他的日常流程和验收清单；这类能力可以保留，当成出事时才用的后备。

**Why:** 2026-09-11 T252 收尾，我让他「在主目录跑 `pnpm -C apps/server dev` 再把后台切到本地」来验本地环境，他回：「那我不需要，为啥是需要跑命令切呢，我都在后台控制，留个口子下次后台崩了再说」。

**How to apply:**
- 验收清单只写后台里能点的步骤；需要命令的部分，由我自己用命令验完，在报告里交代结果
- 设计新功能时，凡是要 owner 开终端才能用的，先问自己能不能挪到后台；挪不了就明说它是后备口子，不当成主路径
- 相关：[[feedback_owner_decision_interaction]]、[[feedback-done-needs-runtime-before-saying-so]]
