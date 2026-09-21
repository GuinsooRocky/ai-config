---
name: feedback-done-needs-runtime-before-saying-so
description: 报「做完/可以合」前先对照项目 CLAUDE.md 的完成定义自查；静态全绿 + 三件套过了仍会漏部署接线与真实调用才暴露的缺陷（09-11 T252 被问「做完了吗」后真跑挖出 5 处）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: dfebc5d2-85e8-4ab0-8e88-992f580f14e9
  modified: 2026-09-11T09:28:53.772Z
---

报完成前，先读项目 CLAUDE.md 的「完成定义」逐字对照；soliloquy 与 eval-arena 都写着「完成 = 运行时证据在手」。静态验收（定向测试、tsc、drift 闸、bug 三件套、跨仓握手）只是前置。

**Why:** 2026-09-11 T252 模型供给，两仓代码、三件套审查、跨仓握手全过后我报「代码层面可以合」，owner 只问一句「思考下 这个事情做完了吗」。按完成定义真跑下去，挖出五处任何静态检查都看不见的缺口：
- 线上 CI 构建后台时根本不传本地地址变量（GitHub env 只配了三个）
- CSP 读的变量在服务器私有 wrangler 配置里，我和 agent 都指成了 Mac 上那份
- dev 编排服务端从来不读 env 文件，「本地」这条路根本起不来
- 试跑缺结算密钥时静默记 5 个 unknown，一行日志都没有
- 平台对单账号聊天并发上限 3，试跑五条齐发永远最多 3/5

**How to apply:**
- 说「做完」之前先问三件：真服务起过没有、真请求打过没有、部署链路（CI 变量 / 私有配置 / 进程 env）逐项核过没有。任何一项没有，就说「代码好了，运行时还差 X」，并直接去做能做的那部分
- 本机能起的服务就起（非桌面 app，不抢焦点），用真 token 打真路由、把真回执喂给解析器；花钱的小样本（≤ 5 次调用）直接跑
- 部署缺口按「构建时变量 / 运行时私有配置 / 本机 env」三层各查一遍，别只看仓里的示例文件
- 相关：[[feedback-delegate-impl-to-opus-subagent]] 第⑤条（跨仓喂真实字节）、[[feedback_verify_on_users_path_not_terminal]]
