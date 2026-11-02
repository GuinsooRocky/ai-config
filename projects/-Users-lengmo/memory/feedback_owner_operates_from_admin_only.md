---
name: feedback-owner-operates-from-admin-only
description: owner 日常只在后台（B 端）点，不在终端跑命令；需要他跑命令才能用的环节不进日常流程和验收清单，做成出事时再用的后备口子；要 owner 亲手做的网页步骤，第一次提就附可点的直达链接，别只写菜单路径
metadata: 
  node_type: memory
  type: feedback
  originSessionId: dfebc5d2-85e8-4ab0-8e88-992f580f14e9
  modified: 2026-11-02T07:53:08.284Z
---

给 owner 设计流程或写验收步骤时，所有动作都要能在后台页面上完成。需要他在终端跑命令的环节（起本地服务、跑脚本）不写进他的日常流程和验收清单；这类能力可以保留，当成出事时才用的后备。

**Why:** 2026-09-11 T252 收尾，我让他「在主目录跑 `pnpm -C apps/server dev` 再把后台切到本地」来验本地环境，他回：「那我不需要，为啥是需要跑命令切呢，我都在后台控制，留个口子下次后台崩了再说」。

**How to apply:**
- 验收清单只写后台里能点的步骤；需要命令的部分，由我自己用命令验完，在报告里交代结果
- 设计新功能时，凡是要 owner 开终端才能用的，先问自己能不能挪到后台；挪不了就明说它是后备口子，不当成主路径
- 相关：[[feedback_owner_decision_interaction]]、[[feedback-done-needs-runtime-before-saying-so]]


补充：09-11「为啥要跑命令切，我都在后台控制」

## 待 owner 做的步骤要带直达链接

凡是交给 owner 自己去网页上做的事（注册账号、改付款方式、点确认等），第一次说的时候就把直达 URL 贴出来，后面再跟"进去点哪"。只写"后台 → 账单 → 付款信息"这种路径不算。

**Why:** 2026-10-02 soliloquy 账号迁移，同一天被追问两次——NOWPayments 注册（"你不能给我个链接吗"）、Cloudflare 付款页（"这个你给我链接呀"）。当时 owner 已经因为在两个 AI 之间来回传话很烦，少一个链接就多一轮来回。

**How to apply:** 写"待 owner 做"的条目前自查有没有 URL；链接不确定时给一个已验证能开的兜底页并说明。
