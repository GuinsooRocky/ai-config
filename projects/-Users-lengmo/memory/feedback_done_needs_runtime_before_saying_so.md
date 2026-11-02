---
name: feedback-done-needs-runtime-before-saying-so
description: 报「做完/可以合」前先对照项目 CLAUDE.md 的完成定义自查；静态全绿 + 三件套过了仍会漏部署接线与真实调用才暴露的缺陷（09-11 T252 被问「做完了吗」后真跑挖出 5 处）；终端里验通 ≠ 用户点按钮那条路径能通，环境差异要在用户的入口上验；owner 要「main 全绿 / CI 变绿」= 本地跑齐 PR 全量 CI 的每个 job（audit、harness、Playwright 两套、supply-chain），不是只跑 code-gate，e2e 套件可能已在 main 上烂了几周没人看
metadata: 
  node_type: memory
  type: feedback
  originSessionId: dfebc5d2-85e8-4ab0-8e88-992f580f14e9
  modified: 2026-11-02T08:23:36.544Z
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
- 相关：[[feedback-delegate-impl-to-opus-subagent]] 第⑤条（跨仓喂真实字节）、本文件「终端验通≠用户那条路径通」节

## 终端验通≠用户那条路径通

交付「用户点一下就跑」的东西时，**在终端里跑通不算验证**。必须在用户真正的
入口上验（URL Handler / launchd / 服务进程），因为那条路径的环境是另一套。

**Why**：2026-08-27 收图按钮，一晚上三次「终端里通、按钮那条路径不通」，每次
我都以为补完了：
1. `PATH` 里没有 node（nvm 装的）→ 点了没反应
2. 没有 `NODE_EXTRA_CA_CERTS` → 一句没线索的「快照读失败」
3. 没有代理变量，且 **Node 的 fetch 默认不认 `http_proxy`**（要 `NODE_USE_ENV_PROXY`）
   → 领任务就崩，云端一个字都收不到

第 3 条还有更深一层：python 起 adapter 子进程时 `runtime_env` 是白名单式的，
上层辛苦导出的代理到那一层又被丢干净。**每多一层进程边界，就多一次环境被剥光
的机会。**

**How to apply**：
- 用 `env -i HOME=... PATH=/usr/bin:/bin` 模拟空环境跑一遍，别用自己的 shell
- 跨进程边界时查白名单（`env=`、`runtime_env=` 这类字典），别假设变量会传下去
- 判断「真的走代理了吗」用 `lsof -nP -p <pid> -i` 看 socket 打到哪，
  不看「跑得快了」——快慢会骗人
- 验界面的 fixture 别替真实链路做事：11-02 lich 微信撤回提示，我在 fixture 里手动过一遍转换再渲染，
  测试全绿，owner 在运行中的窗口看到样式变了、文字还是 XML。热更新只换代码，不换页面里已加载的数据；
  要改已加载内容的显示时，用改动前已在页面里的那份数据验，别叫 owner「切走再切回来」顶替验证
- 相关：[[feedback_gates_must_fail_on_purpose]]、[[feedback_not_ground_truth]]

## CI 绿=每个 job 都绿

owner 说「main 整体要 test 通过，CI 变绿不要红」时，判定面是 PR 触发的**全部** CI job，不只是本地 `code-gate.sh`。soliloquy 10-12 实测：code-gate 绿之后 PR 级 CI 还跑 `audit:production`（高危依赖）、`gate:harness`、`e2e:product-matrix`、`e2e`、supply-chain——其中两套 Playwright 在 main 上已经红了约一个月（e2e mock 没跟后端合同、spec 选择器停在旧 UI），没人注意是因为 main 普通 push 只跑 quick 闸。

**Why:** 10-12 我报「code-gate 四红全是 main 既有」就准备收工，owner 一句「main 要全绿」后才发现 Playwright 两套合计 95 红全是 main 原有；少看一眼 ci.yml 的 job 清单就会把半截活当做完。

**How to apply:**
- 接到「CI 绿」类目标先读 `.github/workflows/*.yml`，列出 PR 事件会跑的每个 job 与其 `if:`，逐个在本地跑等价命令（注意 Playwright 共用端口只能串行、mock server 进程在一轮 run 内不会热更新）。
- 判「是不是分支引入」用干净 origin/main worktree 跑同一 spec（`git worktree add` + `pnpm install --offline`），别靠猜。
- e2e 红的常见根因按顺序排查：mock 缺新 RPC/表（404）、种子缺新列被过滤（如 channel=eq.web）、spec 选择器 / 文案停在旧 UI、hover 才露出的控件要先 hover 或走键盘、CSS 契约探针漏装挪走的样式文件或新 token。
- 相关：[[feedback_not_ground_truth]]、[[project_soliloquy_bugscan_20261011]]
